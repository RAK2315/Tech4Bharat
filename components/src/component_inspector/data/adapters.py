"""Explicit RGB-only adapters; mask content supplies KSDD2 image labels."""
from pathlib import Path
import json
from PIL import Image

from component_inspector.contracts import ImageRecord


def load_records(dataset_id, root, release_hash):
    root = Path(root).resolve()
    records = []
    if dataset_id == 'mvtec_3d_ad':
        tree = root / 'cable_gland'
        if root.name == 'cable_gland':
            tree = root
        classes = None
        if (tree/'class_ids.json').is_file():
            classes = json.loads((tree/'class_ids.json').read_text(encoding='utf-8'))
            if (set(classes.values()) != {'good', 'bent', 'cut', 'hole', 'thread'}
                    or classes.get('0') != 'good'
                    or any(not k.isdigit() or not 0 <= int(k) <= 255 for k in classes)):
                raise ValueError('Unknown mask class-ID mapping')
        for partition in ('train', 'validation', 'test'):
            for path in sorted((tree / partition).glob('*/rgb/*.png')):
                kind = path.parent.parent.name
                if partition != 'test' and kind != 'good':
                    raise ValueError('Unexpected nonnormal official train/validation category')
                if kind not in {'good', 'bent', 'cut', 'hole', 'thread'}:
                    raise ValueError('Unknown cable-gland taxonomy')
                label = int(kind != 'good')
                mask = path.parent.parent / 'gt' / path.name
                reason = 'missing_mask' if label and not mask.is_file() else None
                relative = path.relative_to(tree).as_posix()
                positive = next((int(k) for k, v in classes.items() if v == kind), 255) if classes else 255
                records.append(ImageRecord(dataset_id, release_hash, 'mvtec_3d_cable_gland_rgb',
                    f'{dataset_id}:{release_hash}:{relative}', path.as_posix(),
                    mask.as_posix() if mask.is_file() else None, partition, label,
                    kind if label else None, quarantine_reason=reason,
                    provenance={'source_relative_path': relative, 'modality': 'rgb',
                                'mask_positive_value': positive if label else 0}))
    elif dataset_id == 'ksdd2':
        for partition in ('train', 'test'):
            for path in sorted((root / partition).glob('*.png')):
                if path.stem.endswith('_GT'):
                    continue
                mask = path.with_name(path.stem + '_GT.png')
                reason, label = None, None
                if not mask.is_file():
                    reason = 'missing_mask'
                else:
                    try:
                        with Image.open(mask) as m:
                            if m.width*m.height > 20_000_000 or getattr(m, 'n_frames', 1) != 1:
                                raise ValueError('mask decode limit')
                            label = int(m.convert('L').getextrema()[1] > 0)
                    except (OSError, ValueError, Image.DecompressionBombError):
                        reason = 'corrupt_mask'
                relative = path.relative_to(root).as_posix()
                records.append(ImageRecord(dataset_id, release_hash, 'ksdd2_surface',
                    f'{dataset_id}:{release_hash}:{relative}', path.as_posix(),
                    mask.as_posix() if mask.is_file() else None, partition, label,
                    'anomaly' if label else None, quarantine_reason=reason,
                    provenance={'source_relative_path': relative, 'modality': 'rgb'}))
    else:
        raise ValueError('Unsupported dataset identity')
    if not records:
        raise ValueError('No source images found')
    return records
