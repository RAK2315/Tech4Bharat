"""Frozen calibration/evaluation worker. Truth never enters model prediction."""
import argparse
import json
from pathlib import Path
import time

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from sklearn.metrics import roc_auc_score

from component_inspector.contracts import ImageRecord
from component_inspector.data.acquire import sha256
from component_inspector.data.split import select_for
from component_inspector.evaluation.freeze import verify_freeze
from component_inspector.evaluation.calibration import calibrate, flag, display_scale
from component_inspector.evaluation.metrics import evaluate
from component_inspector.vision.geometry import prepare, restore_map
from component_inspector.vision.media import decode_media, MediaError


def _load_model(root, details, recipe, method):
    path=root/details['artifacts'][recipe][method]['artifact_path']
    if method=='reference':
        from component_inspector.vision.reference import load_model
        return load_model(path,expected_recipe=recipe)[0]
    import torch
    torch.set_num_threads(4);torch.set_num_interop_threads(1)
    from component_inspector.vision.padim_adapter import PadimAdapter
    return PadimAdapter.load(path,expected_recipe=recipe)


def _calibration(run, recipe, method):
    complete=json.loads((run/'calibration_complete.json').read_text(encoding='utf-8'))
    relative=f'calibration/{recipe}_{method}.json'
    if sha256(run/relative)!=complete['file_hashes'][relative]:
        raise ValueError('Calibration hash changed before final predictions')
    record=json.loads((run/relative).read_text(encoding='utf-8'))
    if record['freeze_sha256']!=sha256(run/'freeze.json'):
        raise ValueError('Calibration belongs to another frozen experiment')
    return record


def _write(path, value):
    with Path(path).open('x',encoding='utf-8') as handle:
        json.dump(value,handle,indent=2,sort_keys=True,allow_nan=False);handle.write('\n')


def run(request_path):
    request=json.loads(Path(request_path).read_text(encoding='utf-8'))
    directory=Path(request['run']).resolve();root=directory.parent.parent
    snapshot=verify_freeze(directory);details=snapshot['details']
    phase,recipe,method=request['phase'],request['recipe'],request['method']
    if sha256(directory/'freeze.json')!=request['freeze_sha256']:
        raise ValueError('Frozen-run identity mismatch')
    marker=json.loads((directory/f'{phase}_started.json').read_text(encoding='utf-8'))
    if marker['freeze_sha256']!=request['freeze_sha256']:
        raise ValueError('Phase not reserved against this freeze')
    if phase not in ('calibration','evaluate','stress') or method not in ('reference','padim'):
        raise ValueError('Unknown frozen phase/method')
    if recipe not in details['artifacts']:raise ValueError('Unknown frozen recipe')
    manifest=json.loads((root/details['manifest_path']).read_text(encoding='utf-8'))
    records=[ImageRecord(**r) for r in manifest['splits']['records'] if r['recipe']==recipe]
    role='calibration' if phase=='calibration' else 'test'
    selected=select_for(records,'calibrate' if phase=='calibration' else 'evaluate',
                        ids=[r.id for r in records if r.experiment_role==role])
    cfg=details['effective_recipes'][recipe]
    calibration=None if phase=='calibration' else _calibration(directory,recipe,method)
    if phase=='stress' and not (directory/'evaluation_complete.json').is_file():
        raise ValueError('Original tests must finish before stress')
    output=Path(request['output']);output.mkdir(parents=True,exist_ok=True)
    if not output.resolve().is_relative_to(directory):raise ValueError('Phase output escapes frozen run')
    # Reserve each unit before any model prediction, including on a manual worker rerun.
    reservations=directory/'unit_reservations';reservations.mkdir(exist_ok=True)
    _write(reservations/f'{phase}_{recipe}_{method}.json',
           {'phase':phase,'freeze_sha256':request['freeze_sha256']})
    init_tick=time.perf_counter();model=_load_model(root,details,recipe,method)
    init_seconds=time.perf_counter()-init_tick
    rows=[];maps=[];pixel_aucs=[];gallery={};times=[]
    transforms={'brightness_0p6':lambda im:ImageEnhance.Brightness(im).enhance(.6),
                'brightness_1p4':lambda im:ImageEnhance.Brightness(im).enhance(1.4),
                'blur_radius_2':lambda im:im.filter(ImageFilter.GaussianBlur(2))}
    stress_rows={key:[] for key in transforms}
    truth={r.id:r.label for r in selected}
    for index,record in enumerate(selected):
        if index%100==0:print(f'{phase} {recipe}/{method} {index}/{len(selected)}',flush=True)
        if sha256(record.path)!=record.hashes['sha256']:
            raise ValueError('Frozen input byte hash changed')
        tick=time.perf_counter()
        try:
            media=decode_media(Path(record.path).read_bytes())
        except MediaError as exc:
            rejected={'id':record.id,'status':'not_scored','score':None,'flagged':None,
                      'reasons':[str(exc)],'error_code':exc.status_code,'warnings':[]}
            if phase=='stress':
                for target in stress_rows.values():target.append(rejected.copy())
            else:rows.append(rejected)
            continue
        if phase=='stress':
            for name,transform in transforms.items():
                stress_tick=time.perf_counter()
                p=prepare(transform(media.image),cfg)
                score,stress_raw=model.predict_array(p.rgb_float32,p.valid_roi)
                restore_map(stress_raw,p.geometry)
                stress_rows[name].append({'id':record.id,'status':'scored','score':score,
                    'flagged':flag(score,calibration['threshold_record']),
                    'seconds':time.perf_counter()-stress_tick,'warnings':media.warnings})
            continue
        prepared=prepare(media.image,cfg)
        score,raw=model.predict_array(prepared.rgb_float32,prepared.valid_roi)
        original=restore_map(raw,prepared.geometry) if phase=='evaluate' else None
        elapsed=time.perf_counter()-tick;times.append(elapsed)
        row={'id':record.id,'status':'scored','score':score,
             'flagged':None if calibration is None else flag(score,calibration['threshold_record']),
             'seconds':elapsed,'warnings':media.warnings,'quality_diagnostics':media.diagnostics}
        rows.append(row)
        if phase=='calibration':
            # Only valid pixels, sampled at equal image weights by display_scale.
            pixels=raw[prepared.valid_roi]
            if len(pixels)>10000:
                rng=np.random.default_rng(4217+index)
                pixels=pixels[rng.choice(len(pixels),10000,replace=False)]
            maps.append(pixels)
        else:
            mask=None
            if record.mask_path:
                if sha256(record.mask_path)!=record.hashes['mask_sha256']:
                    raise ValueError('Frozen ground-truth mask hash changed')
                with Image.open(record.mask_path) as im:mask=np.asarray(im.convert('L'))>0
                if mask.shape!=original.shape:raise ValueError('Original map/mask geometry mismatch')
                if mask.any() and not mask.all():
                    pixel_aucs.append(float(roc_auc_score(mask.ravel(),original.ravel())))
            case=('TP' if row['flagged'] else 'FN') if record.label else ('FP' if row['flagged'] else 'TN')
            if case not in gallery:
                target=output/'gallery';target.mkdir(exist_ok=True)
                image_name=f'{case}_original.png';overlay_name=f'{case}_overlay.png'
                media.image.save(target/image_name)
                maximum=calibration['display_scale']['maximum']
                intensity=np.clip(original/maximum,0,1)[...,None]
                base=np.asarray(media.image,dtype=np.float32)
                red=np.zeros_like(base);red[...,0]=255
                overlay=(base*(1-.55*intensity)+red*(.55*intensity)).clip(0,255).astype(np.uint8)
                Image.fromarray(overlay).save(target/overlay_name)
                if mask is not None:Image.fromarray(mask.astype(np.uint8)*255).save(target/f'{case}_mask.png')
                gallery[case]={'id':record.id,'score':score,'threshold':calibration['threshold_record']['threshold'],
                    'original':f'gallery/{image_name}','overlay':f'gallery/{overlay_name}',
                    'mask':f'gallery/{case}_mask.png' if mask is not None else None,
                    'legend':'anomaly intensity, not probability/severity; fixed calibration display range'}
    common={'recipe_id':recipe,'method':method,'freeze_sha256':request['freeze_sha256'],
            'init_seconds':init_seconds,'expected_images':len(selected)}
    if phase=='calibration':
        scores=[p['score'] for p in rows if p['status']=='scored']
        result={**common,'status':'calibrated_normal_only','threshold_record':calibrate(scores),
                'display_scale':display_scale(maps),'role':'calibration','rows':rows,
                'pixel_sampling':'up to 10000 valid pixels per image; generator seed 4217+sorted record index',
                'artifact_identity':details['artifacts'][recipe][method]}
        _write(output/f'{recipe}_{method}.json',result)
    elif phase=='evaluate':
        result={**common,'status':'frozen_original_test','rows':rows,'metrics':evaluate(rows,truth),
            'calibration_sha256':sha256(directory/f'calibration/{recipe}_{method}.json'),
            'cold_pipeline_seconds':times[0] if times else None,
            'warm_p95_pipeline_seconds':float(np.percentile(times[1:],95)) if len(times)>1 else None,
            'pixel_diagnostic':{'metric':'macro per-anomalous-image pixel AUROC, not pooled dataset pixel AUROC',
                                'value':float(np.mean(pixel_aucs)) if pixel_aucs else None,'images':len(pixel_aucs)},
            'gallery':{case:gallery.get(case,{'status':'no_decodable_example'}) for case in ('TP','FN','FP','TN')}}
        _write(output/f'{recipe}_{method}.json',result)
    else:
        result={**common,'status':'paired_stress_not_independent_validation',
            'calibration_sha256':sha256(directory/f'calibration/{recipe}_{method}.json'),
            'transforms':{name:{'rows':preds,'metrics':evaluate(preds,truth)} for name,preds in stress_rows.items()}}
        _write(output/f'{recipe}_{method}.json',result)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--request',required=True)
    run(parser.parse_args().request)
