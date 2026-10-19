"""Own and supervise the real P0 feasibility runs; no calibration/test access."""
from dataclasses import asdict
from importlib.metadata import distribution, version
import json
import logging
from pathlib import Path
import sys
import uuid

import psutil
import yaml

from component_inspector.data.acquire import sha256
from component_inspector.data.prepare import verify_source
from component_inspector.data.split import select_for, digest
from component_inspector.vision.develop import load_manifest
from component_inspector.vision.resources import run_bounded


def spike(config, manifest_path, weight_path):
    config=Path(config).resolve();root=config.parent.parent
    manifest_path=Path(manifest_path).resolve();weight_path=Path(weight_path).resolve()
    manifest, records=load_manifest(root,manifest_path)
    protocol=yaml.safe_load(config.read_text(encoding='utf-8'))
    if manifest['protocol']!=protocol:
        raise ValueError('Protocol differs from audited manifest')
    for recipe in protocol['recipes']:
        source=manifest['sources'][recipe]
        key='mvtec_3d_cable_gland' if source['dataset']=='mvtec_3d_ad' else 'ksdd2'
        if verify_source(root,key)!=source:
            raise ValueError('Source changed since audit')
        current=yaml.safe_load((config.parent/f'{recipe}.yaml').read_text(encoding='utf-8'))
        effective=manifest['effective_recipes'][recipe]
        current['release_hash']=source['archive']['sha256']
        if source['dataset']=='ksdd2':
            current['input']['rotation_clockwise_degrees']=effective['input']['rotation_clockwise_degrees']
        if current!=effective:
            raise ValueError('Current recipe differs from audited configuration')
    if not weight_path.is_relative_to(root/'models'):
        raise ValueError('Pretrained weights must be a project-local trusted model file')
    versions={name:version(name) for name in ['torch','torchvision','anomalib','timm','numpy','scipy','Pillow']}
    if versions['torch']!='2.10.0+cpu' or versions['torchvision']!='0.25.0+cpu' or versions['anomalib']!='2.7.0':
        raise ValueError('P0 requires the pinned CPU backend')
    code={name:sha256(Path(__file__).with_name(name)) for name in
          ['padim_adapter.py','spike_worker.py','spike.py','resources.py','geometry.py']}
    for relative in ['models/image/padim/torch_model.py','models/image/padim/anomaly_map.py',
                     'models/components/stats/multi_variate_gaussian.py','models/components/feature_extractors/timm.py']:
        code[f'anomalib/{relative}']=sha256(distribution('anomalib').locate_file('anomalib/'+relative))
    identity=digest({'manifest':sha256(manifest_path),'code':code,'weights':sha256(weight_path),'versions':versions})
    run_id=identity[:24]+'-'+uuid.uuid4().hex[:8]
    output=root/'outputs/stage4'/run_id;output.mkdir(parents=True,exist_ok=False)
    report={'run_id':run_id,'backend':'anomalib_p0','manifest_sha256':sha256(manifest_path),
        'membership_hash':manifest['splits']['membership_hash'],'source_code_hashes':code,
        'versions':versions,'weights_sha256':sha256(weight_path),'recipes':{},'status':'running'}
    for recipe in protocol['recipes']:
        subset=[r for r in records if r.recipe==recipe]
        chosen=[i for i in manifest['splits']['fit_ids'] if i in {r.id for r in subset}]
        fit=select_for(subset,'fit',ids=chosen)
        dev=select_for(subset,'develop',ids=[r.id for r in subset if r.experiment_role=='development'])
        cfg=manifest['effective_recipes'][recipe]
        artifact=root/'models'/recipe/f'padim-p0-{run_id}'
        request={ 'recipe_id':recipe,'recipe_config':cfg,'fit_records':[asdict(r) for r in fit],
            'development_records':[asdict(r) for r in dev],'weight_path':str(weight_path),
            'artifact_path':str(artifact),'output_path':str(output/recipe),
            'manifest_sha256':report['manifest_sha256'],'membership_hash':report['membership_hash'],
            'source_code_hashes':code}
        request_path=output/f'{recipe}_request.json'
        request_path.write_text(json.dumps(request,indent=2),encoding='utf-8')
        available=psutil.virtual_memory().available
        cap=int(min(4*1024**3,.60*available))
        logging.getLogger(__name__).info('P0 %s: %s fit groups, %s development; RSS cap %.2f GiB',recipe,len(fit),len(dev),cap/1024**3)
        measured=run_bounded([sys.executable,'-u','-m','component_inspector.vision.spike_worker',
                              '--request',str(request_path)],output/f'{recipe}_worker.log',
                              max_rss_bytes=cap,max_seconds=1800)
        entry={'resource_measurement':measured,'available_ram_at_launch_bytes':available,
               'worker_log':(output/f'{recipe}_worker.log').relative_to(root).as_posix()}
        report['recipes'][recipe]=entry
        if measured['status']!='completed':
            entry['status']='feasibility_failed';report['status']='p0_feasibility_failed'
            (output/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8')
            return {'status':report['status'],'report_path':(output/'report.json').relative_to(root).as_posix(),
                    'recipes':report['recipes']}
        result_path=output/recipe/'results.json'
        result=json.loads(result_path.read_text(encoding='utf-8'))
        entry.update({k:v for k,v in result.items() if k not in ('predictions','retained_channels')})
        entry['results_path']=result_path.relative_to(root).as_posix()
        entry['results_sha256']=sha256(result_path)
        entry['status']='native_development_feasible'
        (output/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    report['status']='development_only_uncalibrated'
    (output/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return {'status':report['status'],'report_path':(output/'report.json').relative_to(root).as_posix(),
            'report_sha256':sha256(output/'report.json'),'recipes':report['recipes']}
