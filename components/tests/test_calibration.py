"""Hand-derived normal-only quantile and equal-image display scaling checks."""
import importlib
import importlib.util
import numpy as np
import pytest


def api():
    name='component_inspector.evaluation.calibration'
    assert importlib.util.find_spec(name), 'calibration not implemented'
    return importlib.import_module(name)


def test_finite_sample_quantile_n8_fails_n9_max_and_n44_rank41():
    module=api()
    with pytest.raises(ValueError,match='insufficient'):
        module.calibrate(list(range(8)))
    assert module.calibrate(list(range(9)))['threshold']==8
    result=module.calibrate(list(reversed(range(44))))
    assert result['k']==41 and result['threshold']==40 and result['n']==44
    assert module.flag(40,result) is False
    assert module.flag(40.01,result) is True


def test_calibration_ties_nonfinite_and_equal_image_display_weights():
    module=api()
    record=module.calibrate([2.0]*10)
    assert record['empirical_fpr']==0
    for values in [[float('nan')]*10,[float('inf')]*10,[]]:
        with pytest.raises(ValueError):module.calibrate(values)
    # A single high-valued image must keep equal weight even with few pixels.
    result=module.display_scale([np.zeros(10000),np.full(4,10.0)])
    assert result['maximum']==10.0
    assert module.display_scale([np.zeros(20)])['degenerate'] is True
