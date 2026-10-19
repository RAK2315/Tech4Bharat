"""Research boundaries and model primitives on fictional, hand-computable data."""
import copy
import numpy as np
import pytest
import torch

from component_inspector.research.ksdd2_round1 import (
    guard, farthest_points, bank_score, DefectHead, image_array, gaussian_by_position,
)


def row(role='normal_fit', label=0):
    return {'recipe': 'ksdd2_surface', 'official_split': 'train',
            'quarantine_reason': None, 'label': label, 'group': 'a', 'v2_role': role}


def test_research_rejects_test_and_cross_role_groups_before_any_decode():
    r = row()
    guard([r])
    wrong = copy.deepcopy(r)
    wrong['official_split'] = 'test'
    with pytest.raises(ValueError, match='training originals'):
        image_array(wrong, {})
    wrong = row('normal_calibration')
    with pytest.raises(ValueError, match='crosses roles'):
        guard([r, wrong])
    with pytest.raises(ValueError, match='normal-only'):
        guard([row('normal_fit', 1)])


def test_diversity_selection_covers_extremes_without_duplicates_or_labels():
    x = np.array([[0., 0.], [1., 0.], [10., 0.], [11., 0.]], np.float32)
    chosen = farthest_points(x, 3)
    assert len(set(chosen)) == 3
    assert {0, 3}.issubset(set(chosen))
    assert chosen == farthest_points(x, 3)
    # Even all-identical vectors cannot yield duplicate indices.
    assert len(set(farthest_points(np.zeros((5, 2), np.float32), 5))) == 5


def test_patchcore_score_ignores_padding_and_matches_direct_nearest_distance():
    feature = np.array([[[0., 999.], [3., 999.]], [[0., 999.], [4., 999.]]], np.float32)
    roi = np.array([[True, False], [True, False]])
    bank = torch.tensor([[0., 0.], [1., 0.]])
    assert bank_score(feature, roi, bank, chunk=1) == pytest.approx(np.sqrt(20))
    with pytest.raises(ValueError, match='Invalid query'):
        bank_score(feature, np.zeros((2, 2), bool), bank)


def test_supervised_head_gradients_and_tensor_artifact_prediction_parity(tmp_path):
    torch.manual_seed(3)
    head = DefectHead(4, 3)
    x = torch.rand(2, 4, 8, 8)
    roi = torch.ones(2, 8, 8, dtype=torch.bool)
    pixel, image = head(x, roi)
    assert pixel.shape == (2, 8, 8) and image.shape == (2,)
    loss = pixel.square().mean()+image.square().mean()
    loss.backward()
    assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in head.parameters())
    path = tmp_path/'head.pt'
    torch.save(head.state_dict(), path)
    restored = DefectHead(4, 3)
    restored.load_state_dict(torch.load(path, weights_only=True))
    assert torch.equal(head(x, roi)[1], restored(x, roi)[1])


def test_chunked_gaussian_matches_pinned_library_fit_equations():
    from anomalib.models.components.stats.multi_variate_gaussian import MultiVariateGaussian
    torch.manual_seed(9)
    embedding = torch.randn(8, 4, 3, 5)
    expected_mean, expected_inverse = MultiVariateGaussian().fit(embedding)
    mean, inverse = gaussian_by_position(embedding.reshape(8, 4, 15).numpy(), chunk=4)
    assert torch.allclose(mean, expected_mean, atol=1e-6, rtol=1e-6)
    assert torch.allclose(inverse, expected_inverse, atol=1e-6, rtol=1e-6)
