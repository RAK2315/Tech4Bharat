"""Sequential, bounded, one-time frozen experimental phases."""
import json
from pathlib import Path
import sys

from component_inspector.data.acquire import sha256
from component_inspector.evaluation.freeze import reserve_phase, verify_freeze
from component_inspector.vision.resources import run_bounded


def write(path, value):
    with Path(path).open('x', encoding='utf-8') as handle:
        json.dump(value,handle,indent=2,sort_keys=True,allow_nan=False)
        handle.write('\n')


def verify_completion(run, phase):
    run=Path(run)
    value=json.loads((run/f'{phase}_complete.json').read_text(encoding='utf-8'))
    for relative,want in value['file_hashes'].items():
        path=run/relative
        if not path.resolve().is_relative_to(run.resolve()) or sha256(path)!=want:
            raise ValueError('Completed phase file hash mismatch')
    return value


def screen(result, measurement):
    metrics=result['metrics']
    def bound(key,cut,minimum):
        value=metrics[key]['rate']
        return value is not None and (value>=cut if minimum else value<=cut)
    latency=result.get('warm_p95_pipeline_seconds')
    checks={'recall':bound('recall',.9,True),
        'accepted_normal_fpr':bound('accepted_normal_fpr',.1,False),
        'coverage':bound('coverage',.9,True),
        'warm_latency':latency is not None and latency<=5,
        'memory':measurement['status']=='completed' and measurement['peak_sampled_rss_bytes']<=4*1024**3}
    return {'passed':all(checks.values()),'checks':checks}


def execute(run, phase):
    run=Path(run).resolve()
    snapshot=verify_freeze(run)
    if phase in ('evaluate','stress'):verify_completion(run,'calibration')
    if phase=='stress':verify_completion(run,'evaluation')
    reserve_phase(run,phase)
    output=run/({'evaluate':'evaluation'}.get(phase,phase))
    output.mkdir(exist_ok=False)
    requests=run/'requests';requests.mkdir(exist_ok=True)
    profiles={};hashes={};gates={}
    for recipe in snapshot['details']['protocol']['recipes']:
        gates[recipe]={}
        for method in ('reference','padim'):
            verify_freeze(run)
            key=f'{recipe}_{method}'
            request=requests/f'{phase}_{key}.json'
            write(request,{'run':str(run),'phase':phase,'recipe':recipe,'method':method,
                'freeze_sha256':sha256(run/'freeze.json'),'output':str(output/key)})
            print(f'Starting {phase}: {key}',flush=True)
            measurement=run_bounded([sys.executable,'-m','component_inspector.evaluation.phase_worker',
                '--request',str(request)],output/f'{key}.log',max_rss_bytes=4*1024**3,max_seconds=3600)
            profiles[key]=measurement
            write(output/f'{key}_resources.json',measurement)
            if measurement['status']!='completed':
                raise RuntimeError(f'{key} failed: {measurement}; retain phase reservation and logs')
            result_path=output/key/f'{key}.json'
            result=json.loads(result_path.read_text(encoding='utf-8'))
            # Canonical calibration files are the worker's immutable originals;
            # downstream workers use these single-level paths.
            if phase=='calibration':
                canonical=output/f'{key}.json'
                write(canonical,result)
                hashes[canonical.relative_to(run).as_posix()]=sha256(canonical)
            hashes[result_path.relative_to(run).as_posix()]=sha256(result_path)
            resources=output/f'{key}_resources.json'
            hashes[resources.relative_to(run).as_posix()]=sha256(resources)
            if phase=='evaluate':gates[recipe][method]=screen(result,measurement)
    complete={'phase':phase,'freeze_sha256':sha256(run/'freeze.json'),
              'file_hashes':hashes,'resources':profiles}
    if phase=='evaluate':
        complete['screens']=gates
        complete['eligible_primary_recipes']=[r for r,g in gates.items() if g['padim']['passed']]
        complete['baseline_only_scope_decision_required']=[r for r,g in gates.items()
            if g['reference']['passed'] and not g['padim']['passed']]
        complete['decision']='go' if complete['eligible_primary_recipes'] else (
            'conditional_baseline_scope_decision' if complete['baseline_only_scope_decision_required'] else 'no_go')
    name={'evaluate':'evaluation'}.get(phase,phase)
    write(run/f'{name}_complete.json',complete)
    return complete
