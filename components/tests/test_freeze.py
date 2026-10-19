"""Immutable file graph and one-time phase gates prevent silent holdout retries."""
import importlib
import importlib.util
from pathlib import Path
import pytest


def api():
    name='component_inspector.evaluation.freeze'
    assert importlib.util.find_spec(name), 'freeze gate not implemented'
    return importlib.import_module(name)


def test_fit_identity_respects_record_order_for_padim_not_selection_list_order():
    module=api()
    from types import SimpleNamespace
    records=[SimpleNamespace(id='b'),SimpleNamespace(id='a'),SimpleNamespace(id='unused')]
    assert module.expected_fit_order(records,['a','b'],'padim')==['b','a']
    assert module.expected_fit_order(records,['a','b'],'reference')==['a','b']


def test_frozen_file_graph_detects_changed_model_before_phase_access(tmp_path):
    module=api();model=tmp_path/'model.bin';model.write_bytes(b'fictional')
    run=tmp_path/'runs/fictional'
    module.create_snapshot(tmp_path,run,{'primary_method':'padim'},[model])
    assert module.verify_freeze(run)['details']['primary_method']=='padim'
    model.write_bytes(b'changed')
    with pytest.raises(ValueError,match='hash'):
        module.verify_freeze(run)
    with pytest.raises(ValueError):
        module.reserve_phase(run,'evaluate')


def test_evaluation_requires_finished_calibration_and_cannot_start_twice(tmp_path):
    module=api();config=tmp_path/'config';config.write_text('fictional')
    run=tmp_path/'runs/fictional';module.create_snapshot(tmp_path,run,{},[config])
    with pytest.raises(ValueError,match='calibration'):
        module.reserve_phase(run,'evaluate')
    (run/'calibration_complete.json').write_text('{}')
    module.reserve_phase(run,'evaluate')
    with pytest.raises(ValueError,match='already'):
        module.reserve_phase(run,'evaluate')
