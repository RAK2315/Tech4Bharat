"""Deterministic reversible full-frame RGB letterboxing; no label input."""
from PIL import Image, ImageOps
import numpy as np

from component_inspector.contracts import PreparedImage


def prepare(image, recipe):
    cfg = recipe.get('input', recipe)
    height, width = cfg['height'], cfg['width']
    rotation = cfg.get('rotation_clockwise_degrees')
    if rotation not in (0, 90) or height <= 0 or width <= 0:
        raise ValueError('Unresolved/unsupported recipe geometry')
    if image.width*image.height > 20_000_000 or getattr(image, 'n_frames', 1) != 1:
        raise ValueError('Unsupported decode size or animated image')
    rgb = ImageOps.exif_transpose(image).convert('RGB')
    if min(rgb.size) < 128:
        raise ValueError('Image too small')
    original = (rgb.height, rgb.width)
    if rotation == 90:
        rgb = rgb.transpose(Image.Transpose.ROTATE_270)
    scale = min(width/rgb.width, height/rgb.height)
    resized = (max(1, round(rgb.width*scale)), max(1, round(rgb.height*scale)))
    left, top = (width-resized[0])//2, (height-resized[1])//2
    pixels = np.zeros((height, width, 3), np.float32)
    pixels[top:top+resized[1], left:left+resized[0]] = np.asarray(
        rgb.resize(resized, Image.Resampling.BILINEAR), dtype=np.float32)/255
    valid = np.zeros((height, width), bool)
    valid[top:top+resized[1], left:left+resized[0]] = True
    geometry = {'original_shape': original, 'rotation_clockwise_degrees': rotation,
                'resized_width': resized[0], 'resized_height': resized[1],
                'left': left, 'top': top, 'input_shape': (height, width)}
    return PreparedImage(pixels, valid, geometry, original)


def restore_map(values, geometry):
    values = np.asarray(values, dtype=np.float32)
    if values.shape != tuple(geometry['input_shape']) or not np.isfinite(values).all():
        raise ValueError('Invalid map shape/values')
    left, top = geometry['left'], geometry['top']
    cropped = values[top:top+geometry['resized_height'], left:left+geometry['resized_width']]
    original_h, original_w = geometry['original_shape']
    rotated_size = ((original_h, original_w) if geometry['rotation_clockwise_degrees'] == 90
                    else (original_w, original_h))
    result = Image.fromarray(cropped).resize(rotated_size, Image.Resampling.BILINEAR)
    if geometry['rotation_clockwise_degrees'] == 90:
        result = result.transpose(Image.Transpose.ROTATE_90)
    return np.asarray(result, dtype=np.float32)
