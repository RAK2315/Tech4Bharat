from pathlib import Path
import runpy


def test_secondary_metrics_use_saved_flags_and_verified_folders_only():
    api=runpy.run_path(str(Path(__file__).parents[1]/'tools/stage5_supplement.py'))
    records=[{'id':str(i),'label':int(i<2),'group':str(i),'recipe':'mvtec_3d_cable_gland_rgb',
        'provenance':{'source_relative_path':f'test/{"bent" if i<2 else "good"}/rgb/{i}.png'}} for i in range(4)]
    rows=[{'id':str(i),'status':'scored','score':float(4-i),'flagged':i==0} for i in range(4)]
    result=api['secondary'](records,rows,iterations=30)
    assert result['per_verified_defect_folder_recall']['bent']['rate']==.5
    assert result['ranking_group_bootstrap']['auroc_95']==[1.,1.]
    assert result['ranking_group_bootstrap']['physical_independence_verified'] is False
