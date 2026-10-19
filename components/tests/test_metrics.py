"""Literal confusion/ranking results include rejected defects as misses."""
import importlib
import importlib.util
import pytest


def api():
    name='component_inspector.evaluation.metrics'
    assert importlib.util.find_spec(name), 'metrics not implemented'
    return importlib.import_module(name)


def test_confusion_ranking_and_rejected_defect_denominators():
    predictions=[{'id':'a','status':'scored','score':.9,'flagged':True},
                 {'id':'b','status':'scored','score':.8,'flagged':True},
                 {'id':'c','status':'scored','score':.7,'flagged':False},
                 {'id':'d','status':'scored','score':.1,'flagged':False},
                 {'id':'e','status':'not_scored','score':None,'flagged':None}]
    result=api().evaluate(predictions,{'a':1,'b':0,'c':1,'d':0,'e':1})
    assert result['counts']=={'TP':1,'FN':2,'FP':1,'TN':1,'rejected_anomalies':1,'rejected_normals':0}
    assert result['recall']['rate']==pytest.approx(1/3)
    assert result['accepted_normal_fpr']['rate']==.5
    assert result['coverage']['rate']==.8
    assert result['precision']['rate']==.5
    assert result['ranking_scored_only']['auroc']==.75
    assert result['ranking_scored_only']['average_precision']==pytest.approx(5/6)


def test_null_denominators_and_missing_predictions_are_not_fake_perfect_scores():
    result=api().evaluate([],{'unscored':1})
    assert result['recall']['rate']==0
    assert result['accepted_normal_fpr']['rate'] is None
    assert result['precision']['rate'] is None
    assert result['ranking_scored_only']['auroc'] is None
    assert result['counts']['FN']==1 and result['coverage']['rate']==0
    with pytest.raises(ValueError):
        api().evaluate([{'id':'x','status':'scored','score':1,'flagged':True}],{'other':0})


def test_wilson_interval_contains_rate_and_small_normal_sample_is_uncertain():
    result=api().rate(2,21)
    assert result['rate']==pytest.approx(2/21)
    assert result['wilson_95'][0]<2/21<result['wilson_95'][1]
    assert result['wilson_95'][1]>.2
