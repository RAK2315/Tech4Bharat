"""Small mathematical checks for round 2 scoring, loss and calibration fusion."""
import numpy as np
import pytest
import torch
from torch.nn import functional as F

from component_inspector.research.ksdd2_round2 import score_rules, focal_loss, cdf_transform


def test_aggregation_excludes_padding_and_normalizes_local_edge_windows():
    values = torch.full((5, 5), 2.)
    roi = torch.zeros(5, 5, dtype=torch.bool)
    roi[1:4, 1:4] = True
    values[~roi] = 999.
    scores = score_rules(values, roi)
    assert all(v == pytest.approx(2.) for v in scores.values())
    with pytest.raises(ValueError, match='Invalid scoring map'):
        score_rules(values, torch.zeros_like(roi))


def test_focal_gamma_zero_matches_parent_weighted_bce_and_has_finite_gradients():
    x = torch.tensor([-2., 0., 3.], requires_grad=True)
    y = torch.tensor([0., 1., 1.])
    expected = F.binary_cross_entropy_with_logits(x, y, pos_weight=torch.tensor(8.), reduction='none')
    assert torch.allclose(focal_loss(x, y, gamma=0), expected)
    loss = focal_loss(x, y, gamma=2)
    assert (loss <= expected).all()
    loss.sum().backward()
    assert torch.isfinite(x.grad).all()


def test_normal_cdf_uses_reference_only_and_handles_ties_monotonically():
    out = cdf_transform([1., 2., 2., 4.], [-1., 1., 2., 3., 4., 99.])
    assert np.allclose(out, [0., .2, .6, .6, .8, .8])
    assert (np.diff(out) >= 0).all()
