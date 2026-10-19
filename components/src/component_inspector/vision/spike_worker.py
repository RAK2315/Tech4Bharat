"""One-recipe P0 worker; selected fit and development records only."""
import argparse
import json
import logging
from pathlib import Path
import time

import numpy as np
from PIL import Image
import torch
import timm
from safetensors.torch import load_file

from component_inspector.contracts import ImageRecord
from component_inspector.data.acquire import sha256
from component_inspector.data.split import select_for
from component_inspector.vision.geometry import prepare, restore_map
from component_inspector.vision.padim_adapter import PadimAdapter


WEIGHT_HASH='80c49dee3da4822c009c5a7fe591e9223c5a2cfcf95a4067ca4dfb5a7b89c612'


def pretrained_adapter(recipe, cfg, weight_path):
    from anomalib.models.image.padim.torch_model import PadimModel
    if sha256(weight_path) != WEIGHT_HASH:
        raise ValueError('Pretrained provider weight hash mismatch')
    torch.manual_seed(4217)
    model = PadimModel(backbone='resnet18',layers=['layer1','layer2','layer3'],pre_trained=False,n_features=100)
    state = load_file(str(weight_path), device='cpu')
    target = model.feature_extractor.feature_extractor
    expected = set(target.state_dict())
    missing = expected-set(state)
    if missing:
        raise ValueError(f'Pretrained backbone state mismatch: {sorted(missing)}')
    target.load_state_dict({k:v for k,v in state.items() if k in expected},strict=True)
    weight_cfg = timm.models.get_pretrained_cfg('resnet18').to_dict()
    weights = {'provider':'timm/resnet18.a1_in1k','revision':'491b427b45c94c7fb0e78b5474cc919aff584bbf',
        'file':'model.safetensors','sha256':WEIGHT_HASH,
        'source_url':'https://huggingface.co/timm/resnet18.a1_in1k/tree/491b427b45c94c7fb0e78b5474cc919aff584bbf',
        'published_download_etag_sha256':WEIGHT_HASH,'license':weight_cfg.get('license'),
        'mean':list(weight_cfg['mean']),'std':list(weight_cfg['std']),
        'ignored_unused_keys':sorted(set(state)-expected),'pretrained_config':weight_cfg}
    return PadimAdapter(model,recipe,(cfg['input']['height'],cfg['input']['width']),weights)


def run(request_path):
    request = json.loads(Path(request_path).read_text(encoding='utf-8'))
    torch.set_num_threads(4); torch.set_num_interop_threads(1)
    cfg, recipe = request['recipe_config'],request['recipe_id']
    fit = select_for([ImageRecord(**r) for r in request['fit_records']], 'fit')
    development = select_for([ImageRecord(**r) for r in request['development_records']], 'develop')
    if len(fit) != len({r.group for r in fit}) or not 2 <= len(fit) <= 128:
        raise ValueError('Fit IDs must be unique normal groups within cap')
    init_tick=time.perf_counter()
    adapter = pretrained_adapter(recipe,cfg,request['weight_path'])
    init_seconds=time.perf_counter()-init_tick
    def arrays():
        for i,r in enumerate(fit):
            if i%16==0:print(f'{recipe}: normal fit {i}/{len(fit)}',flush=True)
            if sha256(r.path) != r.hashes['sha256']:
                raise ValueError('Fit source hash changed')
            with Image.open(r.path) as image:
                yield prepare(image,cfg).rgb_float32
    tick=time.perf_counter();adapter.fit(arrays());fit_seconds=time.perf_counter()-tick
    print(f'{recipe}: Gaussian fit complete in {fit_seconds:.2f} s',flush=True)
    artifact=Path(request['artifact_path'])
    adapter.save(artifact,{'fit_manifest_hash':request['manifest_sha256'],
        'membership_hash':request['membership_hash'],'fit_ids':[r.id for r in fit],
        'geometry':cfg['input'],'source_code_hashes':request['source_code_hashes']})
    reference_channels=adapter.model.idx.tolist()
    gaussian_shapes={'mean':list(adapter.model.gaussian.mean.shape),'inverse_covariance':list(adapter.model.gaussian.inv_covariance.shape)}
    predictions=[];times=[];parity_pending=True
    output=Path(request['output_path']);output.mkdir(parents=True,exist_ok=False)
    for i,r in enumerate(development):
        if i%100==0:print(f'{recipe}: development {i}/{len(development)}',flush=True)
        if sha256(r.path) != r.hashes['sha256']:
            raise ValueError('Development source hash changed')
        tick=time.perf_counter()
        with Image.open(r.path) as image:p=prepare(image,cfg)
        score,raw=adapter.predict_array(p.rgb_float32,p.valid_roi)
        original=restore_map(raw,p.geometry)
        elapsed=time.perf_counter()-tick;times.append(elapsed)
        if original.shape!=p.original_shape or not np.isfinite(score):
            raise ValueError('Prediction map geometry/score invalid')
        if parity_pending:
            # Release the original large Gaussian before loading to keep the parity
            # check within the same process resource cap.
            import gc
            before_raw=raw.copy();before_score=score
            del adapter;gc.collect()
            adapter=PadimAdapter.load(artifact,expected_recipe=recipe)
            after_score,after_raw=adapter.predict_array(p.rgb_float32,p.valid_roi)
            if (not np.allclose(before_raw,after_raw,atol=1e-5,rtol=1e-5)
                    or not np.isclose(before_score,after_score,atol=1e-5,rtol=1e-5)
                    or adapter.model.idx.tolist()!=reference_channels):
                raise ValueError('Trusted saved artifact parity failed')
            np.save(output/'development_sample_map.npy',original,allow_pickle=False)
            parity_pending=False
        predictions.append({'id':r.id,'role':'development','score':score,'threshold':None,'flagged':None,'seconds':elapsed})
    result={'status':'development_only_uncalibrated','recipe_id':recipe,'backend':'anomalib_p0',
        'input_shape':list(adapter.input_shape),'normal_fit_images':len(fit),'init_seconds':init_seconds,
        'fit_seconds':fit_seconds,'cold_pipeline_seconds':times[0] if times else None,
        'warm_p95_pipeline_seconds':float(np.percentile(times[1:],95)) if len(times)>1 else None,
        'development_images':len(predictions),'model_bytes':sum(p.stat().st_size for p in artifact.iterdir() if p.is_file()),
        'artifact_path':str(artifact),'gaussian_shapes':gaussian_shapes,'retained_channels':reference_channels,
        'weights':adapter.weights_metadata,'save_load_parity':'atol=rtol=1e-5',
        'threshold':None,'flagged':None,'predictions':predictions}
    (output/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--request',required=True)
    args=parser.parse_args();run(args.request)
