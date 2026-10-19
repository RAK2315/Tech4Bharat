"""Real B0 scoring on fictional images verifies phase isolation end to end."""
from dataclasses import asdict
import json
from pathlib import Path
import numpy as np
from PIL import Image
import pytest


def test_calibration_worker_excludes_test_and_final_worker_is_single_use(tmp_path):
    from component_inspector.contracts import ImageRecord
    from component_inspector.data.acquire import sha256
    from component_inspector.evaluation.freeze import create_snapshot,reserve_phase
    from component_inspector.evaluation.phase_worker import run
    from component_inspector.vision.reference import ReferenceModel,save_model
    raw=tmp_path/'raw';raw.mkdir()
    records=[];paths=[]
    for index,value in enumerate([50,51,52,53,54,55,56,57,58,55,200]):
        path=raw/f'{index}.png';Image.new('RGB',(128,128),(value,value,value)).save(path)
        mask_path=None;hashes={'sha256':sha256(path)};paths.append(path)
        if index==10:
            mask_path=raw/'defect_mask.png';Image.new('L',(128,128),255).save(mask_path)
            hashes['mask_sha256']=sha256(mask_path);paths.append(mask_path)
        role='calibration' if index<9 else 'test'
        records.append(ImageRecord(dataset='fictional',release_hash='fictional',recipe='fictional',
            id=f'item-{index}',path=str(path),mask_path=str(mask_path) if mask_path else None,
            official_split='train' if index<9 else 'test',experiment_role=role,label=int(index==10),
            group=f'group-{index}',hashes=hashes))
    model_dir=tmp_path/'models/fictional'
    save_model(ReferenceModel(np.zeros((1,128,128,3),np.float32),'fictional'),model_dir,
               {'fit_manifest_hash':'fictional','reference_ids':['fictional-fit']})
    paths.extend(model_dir.iterdir())
    manifest=tmp_path/'manifest.json'
    manifest.write_text(json.dumps({'splits':{'records':[asdict(r) for r in records]}}));paths.append(manifest)
    details={'manifest_path':'manifest.json','effective_recipes':{'fictional':{'input':
             {'height':128,'width':128,'rotation_clockwise_degrees':0}}},
             'artifacts':{'fictional':{'reference':{'artifact_path':'models/fictional'}}}}
    directory=tmp_path/'runs/fictional';create_snapshot(tmp_path,directory,details,paths)
    reserve_phase(directory,'calibration')
    request={'run':str(directory),'phase':'calibration','recipe':'fictional','method':'reference',
             'freeze_sha256':sha256(directory/'freeze.json'),'output':str(directory/'calibration')}
    request_file=directory/'request.json';request_file.write_text(json.dumps(request));run(request_file)
    calibration=directory/'calibration/fictional_reference.json'
    result=json.loads(calibration.read_text())
    assert result['threshold_record']['n']==9
    assert all(r['flagged'] is None for r in result['rows'])
    (directory/'calibration_complete.json').write_text(json.dumps({'file_hashes':
        {'calibration/fictional_reference.json':sha256(calibration)}}))
    reserve_phase(directory,'evaluate')
    request.update(phase='evaluate',output=str(directory/'evaluation'))
    request_file.write_text(json.dumps(request));run(request_file)
    result=json.loads((directory/'evaluation/fictional_reference.json').read_text())
    assert len(result['rows'])==2
    assert result['metrics']['counts']=={'TP':1,'FN':0,'FP':0,'TN':1,'rejected_anomalies':0,'rejected_normals':0}
    assert all(r['status']=='scored' for r in result['rows'])
    assert all('low_focus' in r['warnings'] for r in result['rows'])
    with pytest.raises(FileExistsError):run(request_file)
    request['output']=str(directory/'alternate-output')
    request_file.write_text(json.dumps(request))
    with pytest.raises(FileExistsError):run(request_file)
