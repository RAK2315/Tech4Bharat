"""Known coordinates catch lost edges, extra normalization and reversed rotations."""
import importlib
import importlib.util

import numpy as np
from PIL import Image
import pytest


def api():
    name = 'component_inspector.vision.geometry'
    assert importlib.util.find_spec(name), 'geometry not implemented'
    return importlib.import_module(name)


def test_letterbox_aspect_roi_and_inverse_edge_mark():
    module = api()
    source = Image.new('RGB', (320, 160), (255, 0, 0))
    prepared = module.prepare(source, {'height': 256, 'width': 256, 'rotation_clockwise_degrees': 0})
    assert prepared.rgb_float32.shape == (256, 256, 3)
    assert prepared.rgb_float32.dtype == np.float32
    assert prepared.valid_roi.sum() == 128*256
    assert prepared.rgb_float32[64, 0].tolist() == [1, 0, 0]
    assert not prepared.valid_roi[63, 0]
    mark = np.zeros((256, 256), np.float32); mark[64:192, -1] = 1
    restored = module.restore_map(mark, prepared.geometry)
    assert restored.shape == (160, 320)
    assert restored[:, -1].max() > .5
    assert restored[:, 0].max() == 0


def test_fixed_clockwise_rotation_and_grayscale_roundtrip():
    module = api()
    source = Image.new('L', (128, 256), 0)
    source.paste(255, (0, 0, 128, 16))
    p = module.prepare(source, {'height': 128, 'width': 256, 'rotation_clockwise_degrees': 90})
    assert p.rgb_float32[:, -16:].min() == 1
    assert p.rgb_float32[:, :16].max() == 0
    restored = module.restore_map(p.rgb_float32[:, :, 0], p.geometry)
    assert restored.shape == (256, 128)
    assert restored[:16].min() == 1


def test_exif_orientation_applied_once_and_bad_inputs_rejected():
    module = api()
    source = Image.new('RGB', (256, 128))
    source.getexif()[274] = 6
    p = module.prepare(source, {'height': 256, 'width': 256, 'rotation_clockwise_degrees': 0})
    assert p.original_shape == (256, 128)
    with pytest.raises(ValueError, match='small'):
        module.prepare(Image.new('RGB', (127, 128)), {'height': 256, 'width': 256, 'rotation_clockwise_degrees': 0})
    with pytest.raises(ValueError):
        module.prepare(Image.new('RGB', (128, 128)), {'height': 256, 'width': 256, 'rotation_clockwise_degrees': None})
