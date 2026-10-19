import pytest
from component_inspector.evaluation.metrics import evaluate


def test_gate_uses_counts_latency_memory_and_missing_denominators():
    from component_inspector.evaluation.runner import screen
    rows=[{'id':str(i),'status':'scored','score':float(i),'flagged':i<9 or i in (10,11)} for i in range(30)]
    metrics=evaluate(rows,{str(i):int(i<10) for i in range(30)})
    result={'metrics':metrics,'warm_p95_pipeline_seconds':1.0}
    measurement={'status':'completed','peak_sampled_rss_bytes':1024}
    assert metrics['precision']['rate']==pytest.approx(9/11)
    assert screen(result,measurement)['passed']
    result['warm_p95_pipeline_seconds']=5.01
    assert not screen(result,measurement)['passed']
    result['warm_p95_pipeline_seconds']=1
    metrics['accepted_normal_fpr']['rate']=None
    assert not screen(result,measurement)['passed']


def test_completion_graph_rejects_tampered_calibration(tmp_path):
    from component_inspector.evaluation.runner import verify_completion
    from component_inspector.data.acquire import sha256
    import json
    target=tmp_path/'cal.json';target.write_text('{}')
    (tmp_path/'calibration_complete.json').write_text(json.dumps({'file_hashes':{'cal.json':sha256(target)}}))
    verify_completion(tmp_path,'calibration')
    target.write_text('changed')
    with pytest.raises(ValueError,match='hash'):
        verify_completion(tmp_path,'calibration')
