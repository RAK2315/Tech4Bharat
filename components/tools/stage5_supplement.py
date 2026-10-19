"""Post-prediction reporting only: never loads a model or scores an image."""
import argparse
import json
from pathlib import Path
import numpy as np
from sklearn.metrics import roc_auc_score,average_precision_score
from component_inspector.data.acquire import sha256
from component_inspector.evaluation.freeze import verify_freeze
from component_inspector.evaluation.runner import verify_completion,write
from component_inspector.evaluation.metrics import rate


def secondary(records, rows, iterations=1000):
    by_id={r['id']:r for r in rows};folders={};groups={}
    for record in records:
        row=by_id.get(record['id'],{})
        if record['label'] and record['recipe']=='mvtec_3d_cable_gland_rgb':
            parts=record['provenance']['source_relative_path'].split('/')
            folder=parts[1] if len(parts)>2 and parts[0]=='test' else None
            if folder in ('bent','cut','hole','thread'):
                c=folders.setdefault(folder,[0,0]);c[1]+=1
                c[0]+=int(row.get('status')=='scored' and row.get('flagged') is True)
        if row.get('status')=='scored':
            groups.setdefault(record['group'],[]).append((record['label'],row['score']))
    keys=sorted(groups);rng=np.random.default_rng(4217);aucs=[];aps=[]
    if len(keys)>=2:
        for _ in range(iterations):
            pairs=[p for i in rng.integers(0,len(keys),len(keys)) for p in groups[keys[i]]]
            y,s=map(list,zip(*pairs))
            if len(set(y))<2:continue
            aucs.append(float(roc_auc_score(y,s)));aps.append(float(average_precision_score(y,s)))
    return {'per_verified_defect_folder_recall':{k:rate(*v) for k,v in sorted(folders.items())},
        'defect_folder_note':'KSDD2 has no verified defect-type folders; none invented.',
        'ranking_group_bootstrap':{'seed':4217,'requested_replicates':iterations,
            'valid_replicates':len(aucs),'group_count':len(keys),'population':'scored subset only',
            'auroc_95':np.percentile(aucs,[2.5,97.5]).tolist() if aucs else None,
            'average_precision_95':np.percentile(aps,[2.5,97.5]).tolist() if aps else None,
            'physical_independence_verified':False,
            'caution':'Appearance groups are not verified physical-product identities; intervals do not establish physical independence.'}}


def main(run):
    run=Path(run).resolve();root=run.parent.parent;snapshot=verify_freeze(run)
    verify_completion(run,'calibration');verify_completion(run,'evaluation');verify_completion(run,'stress')
    manifest=json.loads((root/snapshot['details']['manifest_path']).read_text(encoding='utf-8'))
    result={'freeze_sha256':sha256(run/'freeze.json'),'analysis_code_sha256':sha256(Path(__file__)),
        'analysis_status':'post_prediction_reporting_no_rescoring_no_threshold_changes',
        'reporting_limitations':[
            'Pixel average precision was not collected by the frozen worker and is unavailable.',
            'Full raw test maps were not archived. Fixed-scale gallery visualizations and macro per-anomalous-image pixel AUROC are available.',
            'No repeat test inference was performed to recover missing secondary outputs. These require a future independently frozen experiment.'],
        'recipes':{}}
    for recipe in snapshot['details']['protocol']['recipes']:
        records=[r for r in manifest['splits']['records'] if r['recipe']==recipe and r['experiment_role']=='test']
        result['recipes'][recipe]={}
        for method in ('reference','padim'):
            key=f'{recipe}_{method}';value=json.loads((run/f'evaluation/{key}/{key}.json').read_text(encoding='utf-8'))
            result['recipes'][recipe][method]=secondary(records,value['rows'])
    artifacts={p.relative_to(run).as_posix():sha256(p) for p in run.rglob('*.png')}
    result['gallery_file_hashes']=artifacts
    result['phase_completion_hashes']={name:sha256(run/f'{name}_complete.json') for name in ('calibration','evaluation','stress')}
    write(run/'SUPPLEMENT.json',result)
    with (run/'REPORT.md').open('a',encoding='utf-8') as handle:
        handle.write('\n## Additional saved-prediction analysis\n\nSee SUPPLEMENT.json for verified defect-folder recall, appearance-group bootstrap intervals (seed 4217, 1000 replicates), gallery hashes and limitations. Physical independence is unknown.\n\n')
        handle.write('\n'.join('- '+x for x in result['reporting_limitations'])+'\n')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--run',required=True)
    value=main(parser.parse_args().run)
    print(json.dumps({'status':value['analysis_status'],'run':parser.parse_args().run}))
