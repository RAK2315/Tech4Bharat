"""Content-locked experiment identity and exclusive calibration/test phase gates."""
from datetime import datetime, timezone
import json
from pathlib import Path
import uuid
from importlib.metadata import version

import yaml

from component_inspector.data.acquire import sha256, _no_links
from component_inspector.data.prepare import verify_source
from component_inspector.vision.develop import load_manifest


def create_snapshot(root, run, details, paths):
    root,run=Path(root).resolve(),Path(run).resolve()
    if not run.is_relative_to(root/'runs'):
        raise ValueError('Frozen run must stay within project runs')
    hashes={}
    for value in paths:
        path=Path(value).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError('Invalid frozen file path')
        _no_links(path)
        hashes[path.relative_to(root).as_posix()]=sha256(path)
    run.mkdir(parents=True,exist_ok=False)
    payload={'schema_version':1,'created_at_utc':datetime.now(timezone.utc).isoformat(),
             'details':details,'file_hashes':hashes}
    with (run/'freeze.json').open('x',encoding='utf-8') as handle:
        json.dump(payload,handle,indent=2,sort_keys=True);handle.write('\n')
    return payload


def verify_freeze(run):
    run=Path(run).resolve();root=run.parent.parent
    if run.parent.name!='runs':raise ValueError('Invalid frozen-run root')
    snapshot=json.loads((run/'freeze.json').read_text(encoding='utf-8'))
    for relative,want in snapshot['file_hashes'].items():
        path=root/relative
        if not path.resolve().is_relative_to(root) or not path.is_file():
            raise ValueError('Frozen file missing/escaped')
        _no_links(path)
        if sha256(path)!=want:raise ValueError('Frozen file hash changed')
    for name,want in snapshot['details'].get('versions',{}).items():
        if version(name)!=want:raise ValueError('Frozen environment version changed')
    return snapshot


def reserve_phase(run, phase):
    run=Path(run).resolve()
    verify_freeze(run)
    if phase not in ('calibration','evaluate','stress'):raise ValueError('Unknown phase')
    if phase=='evaluate' and not (run/'calibration_complete.json').is_file():
        raise ValueError('Finished calibration required before evaluation')
    if phase=='stress' and not (run/'evaluation_complete.json').is_file():
        raise ValueError('Original evaluation required before stress')
    try:
        with (run/f'{phase}_started.json').open('x',encoding='utf-8') as handle:
            json.dump({'phase':phase,'started_at_utc':datetime.now(timezone.utc).isoformat(),
                       'freeze_sha256':sha256(run/'freeze.json')},handle,indent=2)
    except FileExistsError as exc:
        raise ValueError('Phase already started; do not silently repeat held-out work') from exc


def expected_fit_order(records, selected_ids, method):
    # PaDiM worker consumes select_for's stable record order. B0 metadata stores
    # the selected reference list; model state hashes lock actual bank ordering.
    if method=='padim':
        selected=set(selected_ids)
        return [r.id for r in records if r.id in selected]
    return list(selected_ids)


def freeze_experiment(config, manifest_path, baseline_summary, candidate_summary, reconciliation):
    config=Path(config).resolve();root=config.parent.parent
    manifest_path=Path(manifest_path).resolve()
    manifest, records=load_manifest(root,manifest_path)
    protocol=yaml.safe_load(config.read_text(encoding='utf-8'))
    if protocol!=manifest['protocol']:raise ValueError('Protocol differs from audited roles')
    baseline_summary,candidate_summary,reconciliation=map(lambda p:Path(p).resolve(),
        [baseline_summary,candidate_summary,reconciliation])
    baseline=json.loads(baseline_summary.read_text(encoding='utf-8'))
    candidate=json.loads(candidate_summary.read_text(encoding='utf-8'))
    resolution=json.loads(reconciliation.read_text(encoding='utf-8'))
    if baseline['status']!='development_only_uncalibrated' or candidate['status']!='development_only_uncalibrated':
        raise ValueError('Both methods require completed native development evidence')
    if candidate.get('superseded'):raise ValueError('Superseded feasibility evidence cannot freeze')
    candidate_report=root/candidate['report_path']
    if sha256(candidate_report)!=candidate['report_sha256']:raise ValueError('Candidate evidence hash mismatch')
    b0_results=root/baseline['results_path']
    if sha256(b0_results)!=baseline['results_sha256']:raise ValueError('Baseline evidence hash mismatch')
    if resolution.get('status')!='download_origin_recorded_local_research_release_uncertainty_retained':
        raise ValueError('Cable-gland source notice has no recorded local research resolution')
    if not resolution.get('download_url','').startswith('https://www.mydrive.ch/'):
        raise ValueError('Cable-gland exact download origin missing')
    paths=[config,manifest_path,baseline_summary,candidate_summary,reconciliation,candidate_report,b0_results,
           root/'requirements-p0.lock',root/'pyproject.toml']
    artifacts={}
    for recipe in protocol['recipes']:
        source=manifest['sources'][recipe]
        key='mvtec_3d_cable_gland' if source['dataset']=='mvtec_3d_ad' else 'ksdd2'
        if verify_source(root,key)!=source:raise ValueError('Source changed before freeze')
        if source['dataset']=='mvtec_3d_ad' and resolution['archive_sha256']!=source['archive']['sha256']:
            raise ValueError('Source resolution belongs to another archive')
        cfg_path=config.parent/f'{recipe}.yaml'
        current=yaml.safe_load(cfg_path.read_text(encoding='utf-8'))
        current['release_hash']=source['archive']['sha256']
        if source['dataset']=='ksdd2':current['input']['rotation_clockwise_degrees']=manifest['effective_recipes'][recipe]['input']['rotation_clockwise_degrees']
        if current!=manifest['effective_recipes'][recipe]:raise ValueError('Recipe changed before freeze')
        paths += [cfg_path,root/'data/manifests'/f'{key}_source.json',root/source['archive']['path'],root/source['inventory']['path']]
        measure=candidate['recipes'][recipe]['resource_measurement']
        if (measure['status']!='completed' or measure.get('measurement_scope')!='owned process tree RSS sum'
                or measure['peak_sampled_rss_bytes']>min(measure['rss_cap_bytes'],4*1024**3)):
            raise ValueError('Primary backend lacks valid native resource evidence')
        artifacts[recipe]={}
        for method,info in [('reference',baseline['recipes'][recipe]),('padim',candidate['recipes'][recipe])]:
            location=Path(info['artifact_path']);location=location if location.is_absolute() else root/location
            location=location.resolve()
            if not location.is_relative_to(root/'models'):raise ValueError('Artifact escapes trusted project models')
            metadata_path=location/'metadata.json';meta=json.loads(metadata_path.read_text(encoding='utf-8'))
            if meta['recipe_id']!=recipe or meta.get('threshold') is not None or meta['fit_manifest_hash']!=sha256(manifest_path):
                raise ValueError('Artifact identity/calibration/fit-manifest mismatch')
            rr=[r for r in records if r.recipe==recipe]
            rr_ids={r.id for r in rr}
            expected=[i for i in manifest['splits']['reference_ids' if method=='reference' else 'fit_ids'] if i in rr_ids]
            expected=expected_fit_order(rr,expected,method)
            if meta['reference_ids' if method=='reference' else 'fit_ids']!=expected:
                raise ValueError('Artifact fit IDs differ from audited selected normals')
            state=location/('bank.npy' if method=='reference' else 'state.pt')
            state_hash=meta['bank_sha256' if method=='reference' else 'state_sha256']
            if sha256(state)!=state_hash:raise ValueError('Artifact state hash mismatch')
            artifacts[recipe][method]={'artifact_path':location.relative_to(root).as_posix(),
                'metadata_sha256':sha256(metadata_path),'state_sha256':state_hash,
                'backend':'reference' if method=='reference' else 'anomalib_p0'}
            paths += [state,metadata_path]
    # Lock numerical/data/evaluation runtime, not future CLI/application additions.
    runtime=root/'src/component_inspector'
    paths += [runtime/'contracts.py']
    for area in ('data','vision','evaluation'):
        paths += list((runtime/area).rglob('*.py'))
    details={'status':'frozen_before_calibration_and_test','primary_method':'padim','backend':'anomalib_p0',
        'selection_rule':'Per recipe: primary PaDiM must pass all provisional screens. Baseline-only pass requires explicit scope decision; neither pass is no-go. No test-driven tuning or holdout rerun.',
        'protocol':protocol,'effective_recipes':manifest['effective_recipes'],'artifacts':artifacts,
        'manifest_path':manifest_path.relative_to(root).as_posix(),'manifest_sha256':sha256(manifest_path),
        'membership_hash':manifest['splits']['membership_hash'],'source_resolution':resolution,
        'versions':{name:version(name) for name in ['torch','torchvision','anomalib','timm','numpy','scipy','Pillow','scikit-learn']}}
    run=root/'runs'/('frozen-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8])
    create_snapshot(root,run,details,paths)
    return {'status':details['status'],'run_path':run.relative_to(root).as_posix(),'freeze_sha256':sha256(run/'freeze.json')}
