"""Decode solely for split integrity; never select model settings from test data."""
from collections import Counter
from dataclasses import replace
import hashlib
import json
import logging
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps
from scipy.fft import dctn

from component_inspector.contracts import AuditReport
from component_inspector.data.acquire import sha256


def audit(records):
    if len({r.id for r in records}) != len(records):
        raise ValueError('Duplicate record IDs')
    ordered = sorted(records, key=lambda r: r.id)
    checked, thumbnails, phashes = [], {}, {}
    parents = {r.id: r.id for r in ordered}

    def find(key):
        while parents[key] != key:
            parents[key] = parents[parents[key]]
            key = parents[key]
        return key

    def join(a, b):
        a, b = find(a), find(b)
        parents[max(a, b)] = min(a, b)

    by_hash, by_physical, pairs = {}, {}, []
    for index, record in enumerate(ordered):
        if index % 250 == 0:
            logging.getLogger(__name__).info('Integrity decode %s/%s', index, len(ordered))
        if record.quarantine_reason:
            checked.append(record)
            continue
        reason, hashes, shape = None, {}, None
        try:
            with Image.open(record.path) as source:
                if (source.format not in ('PNG', 'JPEG') or source.width*source.height > 20_000_000
                        or getattr(source, 'n_frames', 1) != 1):
                    raise ValueError('unsupported_image')
                rgb = ImageOps.exif_transpose(source).convert('RGB')
                rgb.load()
                shape = (rgb.height, rgb.width, 3)
                decoded = hashlib.sha256(json.dumps(shape).encode() + rgb.tobytes()).hexdigest()
                hashes = {'sha256': sha256(record.path), 'decoded_sha256': decoded}
                if record.mask_path:
                    with Image.open(record.mask_path) as mask:
                        if mask.size != rgb.size:
                            raise ValueError('mask_shape_mismatch')
                        if getattr(mask, 'n_frames', 1) != 1:
                            raise ValueError('unsupported_mask')
                        pixels = np.asarray(mask.convert('L'))
                        foreground = record.provenance.get('mask_positive_value', 255)
                        if not set(np.unique(pixels)).issubset({0, foreground}):
                            raise ValueError('nonbinary_mask')
                        if bool(pixels.any()) != bool(record.label):
                            raise ValueError('mask_label_mismatch')
                    hashes['mask_sha256'] = sha256(record.mask_path)
                elif record.label != 0:
                    raise ValueError('missing_mask')
                if record.label not in (0, 1):
                    raise ValueError('unknown_label')
                thumbnails[record.id] = np.asarray(rgb.resize((64, 64), Image.Resampling.BILINEAR), dtype=np.int16)
                small = np.asarray(rgb.convert('L').resize((32, 32), Image.Resampling.LANCZOS), dtype=np.float64)
                low = dctn(small, type=2, norm='ortho')[:8, :8].ravel()
                bits = low > np.median(low[1:])
                bits[0] = False
                phashes[record.id] = int.from_bytes(np.packbits(bits).tobytes(), 'big')
                hashes['phash64'] = f'{phashes[record.id]:016x}'
                key = (record.dataset, decoded)
                if key in by_hash:
                    other = by_hash[key]
                    join(record.id, other)
                    pairs.append({'a': other, 'b': record.id, 'kind': 'decoded_exact'})
                by_hash[key] = record.id
                if record.physical_group:
                    pk = (record.dataset, record.physical_group)
                    if pk in by_physical:
                        join(record.id, by_physical[pk])
                    by_physical[pk] = record.id
        except (OSError, ValueError, Image.DecompressionBombError) as exc:
            reason = str(exc) if isinstance(exc, ValueError) else 'corrupt_image_or_mask'
        checked.append(replace(record, hashes=hashes, original_shape=shape, quarantine_reason=reason))
    good = [r for r in checked if not r.quarantine_reason]
    logging.getLogger(__name__).info('Duplicate comparison: %s usable records', len(good))
    for i, a in enumerate(good):
        for b in good[:i]:
            if a.dataset != b.dataset or find(a.id) == find(b.id):
                continue
            distance = (phashes[a.id] ^ phashes[b.id]).bit_count()
            if distance <= 2:
                difference = float(np.abs(thumbnails[a.id] - thumbnails[b.id]).mean())
                if difference <= 2:
                    if a.label != b.label:
                        pairs.append({'a': a.id, 'b': b.id,
                                      'kind': 'near_candidate_distinct_labels_not_grouped',
                                      'phash_hamming': distance, 'thumbnail_mae_255': difference})
                        continue
                    join(a.id, b.id)
                    pairs.append({'a': a.id, 'b': b.id, 'kind': 'near_conservative_group',
                                  'phash_hamming': distance, 'thumbnail_mae_255': difference})
    # Appearance groups are conservative leakage protection, not physical-ID proof.
    grouped = [replace(r, group=hashlib.sha256(find(r.id).encode()).hexdigest(),
                       grouping_confidence='physical_id' if r.physical_group else 'appearance_only_physical_identity_unknown')
               for r in checked]
    labels = {}
    for r in grouped:
        if not r.quarantine_reason:
            labels.setdefault(r.group, set()).add(r.label)
    grouped = [replace(r, quarantine_reason='duplicate_label_conflict')
               if len(labels.get(r.group, set())) > 1 else r for r in grouped]
    summary = {'images': len(grouped),
        'partition_labels': dict(Counter(f'{r.dataset}/{r.official_split}/{r.label}' for r in grouped)),
        'dimensions': dict(Counter(str(r.original_shape) for r in grouped)),
        'quarantine_reasons': dict(Counter(r.quarantine_reason for r in grouped if r.quarantine_reason)),
        'unknown_physical_ids': sum(r.physical_group is None for r in grouped),
        'duplicate_pairs': len(pairs), 'groups': len({r.group for r in grouped})}
    return AuditReport(grouped, summary, pairs)
