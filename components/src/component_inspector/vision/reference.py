"""B0 bank matching in squared RGB units; never performs classification tuning."""
import math
import json
from pathlib import Path
import numpy as np
from scipy.ndimage import gaussian_filter

from component_inspector.data.acquire import sha256


class ReferenceModel:
    def __init__(self, bank, recipe_id, chunk_size=4):
        self.bank = np.asarray(bank, dtype=np.float32)
        if (self.bank.ndim != 4 or self.bank.shape[-1] != 3 or not 1 <= len(self.bank) <= 16
                or not np.isfinite(self.bank).all() or self.bank.min() < 0 or self.bank.max() > 1):
            raise ValueError('Invalid reference bank')
        if not 1 <= chunk_size <= 4:
            raise ValueError('Comparison chunk must be 1..4')
        self.recipe_id, self.chunk_size = recipe_id, chunk_size

    def predict_array(self, rgb_float32, valid_roi):
        query = np.asarray(rgb_float32, dtype=np.float32)
        roi = np.asarray(valid_roi, dtype=bool)
        if (query.shape != self.bank.shape[1:] or roi.shape != query.shape[:2]
                or not roi.any() or not np.isfinite(query).all()):
            raise ValueError('Invalid inference shape/values')
        best_mean, best_map = float('inf'), None
        for start in range(0, len(self.bank), self.chunk_size):
            residual = np.square(self.bank[start:start+self.chunk_size] - query).mean(axis=-1)
            scores = residual[:, roi].mean(axis=1)
            winner = int(np.argmin(scores))
            if float(scores[winner]) < best_mean:
                best_mean, best_map = float(scores[winner]), residual[winner].copy()
        # Normalized smoothing prevents zero-filled padding suppressing edge values.
        smooth = gaussian_filter(np.where(roi, best_map, 0), sigma=1)
        weights = gaussian_filter(roi.astype(np.float32), sigma=1)
        smooth = np.divide(smooth, weights, out=np.zeros_like(smooth), where=weights>0)
        smooth[~roi] = 0
        valid = smooth[roi]
        n = max(1, math.ceil(.01*len(valid)))
        score = float(np.partition(valid, len(valid)-n)[-n:].mean())
        return score, smooth


def save_model(model, destination, context):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    np.save(destination/'bank.npy', model.bank, allow_pickle=False)
    metadata = {**context, 'method': 'reference', 'recipe_id': model.recipe_id,
                'bank_sha256': sha256(destination/'bank.npy'), 'threshold': None,
                'validation_status': 'development_uncalibrated',
                'code_sha256': sha256(Path(__file__))}
    (destination/'metadata.json').write_text(json.dumps(metadata, indent=2, sort_keys=True)+'\n', encoding='utf-8')
    return metadata


def load_model(destination, *, expected_recipe):
    destination = Path(destination)
    metadata = json.loads((destination/'metadata.json').read_text(encoding='utf-8'))
    if metadata['recipe_id'] != expected_recipe or metadata.get('method') != 'reference':
        raise ValueError('Artifact recipe/method mismatch')
    path = destination/'bank.npy'
    if path.stat().st_size > 64*1024**2 or sha256(path) != metadata['bank_sha256']:
        raise ValueError('Artifact bank hash/size mismatch')
    if metadata['code_sha256'] != sha256(Path(__file__)):
        raise ValueError('Artifact code hash mismatch')
    model = ReferenceModel(np.load(path, allow_pickle=False), metadata['recipe_id'])
    return model, metadata
