"""Reject-accounting regressions for the external evaluation, using fictional rows."""
import ast
from collections import Counter
from copy import deepcopy
import math
from pathlib import Path

import numpy as np
import pytest
from scipy.stats import binomtest

from component_inspector.evaluation.metrics import evaluate

source = Path(__file__).resolve().parents[1] / "tools/verify_external_transfer.py"
tree = ast.parse(source.read_text(encoding="utf-8"))
nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in ("rate", "recount")]
namespace = {"Counter": Counter, "math": math, "np": np, "binomtest": binomtest, "evaluate": evaluate}
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(source), "exec"), namespace)
recount = namespace["recount"]


def fixture():
    truth = {"d1": 1, "d2": 1, "n1": 0, "n2": 0, "n3": 0}
    predictions = [{"id": "d1", "status": "scored", "score": .8, "flagged": True},
                   {"id": "d2", "status": "rejected", "score": None, "flagged": None, "reason": "too small"},
                   {"id": "n1", "status": "scored", "score": .8, "flagged": True},
                   {"id": "n2", "status": "scored", "score": .1, "flagged": False},
                   {"id": "n3", "status": "rejected", "score": None, "flagged": None, "reason": "too small"}]
    return predictions, truth


def test_rejected_defects_are_misses_and_rejected_normals_are_not_true_negatives():
    predictions, truth = fixture(); result = recount(predictions, truth)
    assert result["counts"] == {"TP": 1, "FN": 1, "FP": 1, "TN": 1, "rejected_anomalies": 1, "rejected_normals": 1}
    assert result["recall"]["rate"] == .5
    assert result["accepted_normal_fpr"]["rate"] == .5
    assert result["false_flags_all_normals"]["rate"] == 1 / 3
    assert result["coverage"]["rate"] == 3 / 5


@pytest.mark.parametrize("forgery", ["missing", "duplicate", "fake_normal", "nan", "wrong_id"])
def test_invalid_external_accounting_is_rejected(forgery):
    predictions, truth = fixture(); predictions = deepcopy(predictions)
    if forgery == "missing": predictions.pop()
    elif forgery == "duplicate": predictions.append(deepcopy(predictions[0]))
    elif forgery == "fake_normal": predictions[1]["score"] = 0.
    elif forgery == "nan": predictions[0]["score"] = float("nan")
    else: predictions[0]["id"] = "unknown"
    with pytest.raises(AssertionError): recount(predictions, truth)


def test_no_scored_normals_does_not_report_zero_false_alarm_rate():
    result = recount([{"id": "n", "status": "rejected", "score": None, "flagged": None, "reason": "too small"}], {"n": 0})
    assert result["accepted_normal_fpr"]["rate"] is None
    assert result["counts"]["TN"] == 0


def test_empty_descriptive_size_slice_stays_unavailable():
    result = recount([], {})
    assert result["recall"]["rate"] is None and result["precision"]["rate"] is None
