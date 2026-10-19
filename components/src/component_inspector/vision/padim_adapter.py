"""Thin CPU adapter around pinned Anomalib PaDiM; raw valid-ROI score only."""
from importlib.metadata import version
import json
from pathlib import Path

import numpy as np
import torch

from component_inspector.data.acquire import sha256


class PadimAdapter:
    def __init__(self, model, recipe_id, input_shape, weights_metadata):
        self.model = model.cpu()
        self.recipe_id, self.input_shape = recipe_id, tuple(input_shape)
        self.weights_metadata = weights_metadata
        self.mean = torch.tensor(weights_metadata['mean'], dtype=torch.float32).reshape(1,3,1,1)
        self.std = torch.tensor(weights_metadata['std'], dtype=torch.float32).reshape(1,3,1,1)
        if not torch.isfinite(self.mean).all() or not torch.isfinite(self.std).all() or (self.std <= 0).any():
            raise ValueError('Invalid weight normalization configuration')
        for parameter in self.model.parameters():
            parameter.requires_grad_(False)
        self.model.eval(); self.fitted = False

    def _tensor(self, array):
        array = np.asarray(array, dtype=np.float32)
        if (array.shape != (*self.input_shape, 3) or not np.isfinite(array).all()
                or array.min() < 0 or array.max() > 1):
            raise ValueError('Invalid RGB inference shape/values')
        tensor = torch.from_numpy(array.transpose(2,0,1).copy()).unsqueeze(0)
        return (tensor-self.mean)/self.std

    @torch.inference_mode()
    def fit(self, arrays):
        self.model.memory_bank = []
        self.model.train()
        # nn.Module.train() recurses; keep pretrained BN statistics frozen explicitly.
        self.model.feature_extractor.eval()
        count = 0
        try:
            for array in arrays:
                if count >= 128:
                    raise ValueError('Normal fit group cap exceeded')
                self.model(self._tensor(array)); count += 1
            if count < 2:
                raise ValueError('At least two normal fit samples required')
            self.model.fit()
            if not all(torch.isfinite(v).all() for v in
                       [self.model.gaussian.mean, self.model.gaussian.inv_covariance]):
                raise ValueError('Nonfinite Gaussian fit')
            self.fitted = True
            self.fit_count = count
        finally:
            self.model.memory_bank = []
            self.model.eval()

    @torch.inference_mode()
    def predict_array(self, array, valid_roi):
        if not self.fitted:
            raise ValueError('Model must be fit before prediction')
        roi = np.asarray(valid_roi, dtype=bool)
        if roi.shape != self.input_shape or not roi.any():
            raise ValueError('Invalid valid ROI')
        result = self.model(self._tensor(array))
        raw = result.anomaly_map[0,0].detach().cpu().numpy()
        if raw.shape != self.input_shape or not np.isfinite(raw).all():
            raise ValueError('Invalid PaDiM raw map')
        return float(raw[roi].max()), raw

    def save(self, destination, context):
        if not self.fitted:
            raise ValueError('Cannot save unfitted model')
        path = Path(destination); path.mkdir(parents=True, exist_ok=False)
        torch.save(self.model.state_dict(), path/'state.pt')
        metadata = {**context, 'backend': 'anomalib_p0', 'recipe_id': self.recipe_id,
            'input_shape': self.input_shape, 'weights': self.weights_metadata,
            'fit_count': self.fit_count, 'retained_channels': self.model.idx.tolist(),
            'state_sha256': sha256(path/'state.pt'), 'adapter_sha256': sha256(Path(__file__)),
            'versions': {x: version(x) for x in ['torch','torchvision','anomalib','timm','numpy']},
            'threshold': None, 'validation_status': 'development_uncalibrated',
            'gaussian_regularization': .01, 'gaussian_extra_stabilization': 1e-5,
            'map_sigma': 4, 'score': 'maximum_raw_map_over_valid_roi'}
        (path/'metadata.json').write_text(json.dumps(metadata, indent=2, sort_keys=True)+'\n', encoding='utf-8')
        return metadata

    @classmethod
    def load(cls, destination, *, expected_recipe):
        from anomalib.models.image.padim.torch_model import PadimModel
        path = Path(destination)
        metadata = json.loads((path/'metadata.json').read_text(encoding='utf-8'))
        if metadata['recipe_id'] != expected_recipe or metadata.get('backend') != 'anomalib_p0':
            raise ValueError('Artifact recipe/backend mismatch')
        state_path = path/'state.pt'
        if state_path.stat().st_size > 1024**3 or sha256(state_path) != metadata['state_sha256']:
            raise ValueError('Artifact state hash/size mismatch')
        if metadata['adapter_sha256'] != sha256(Path(__file__)):
            raise ValueError('Artifact adapter hash mismatch')
        if any(version(name) != want for name,want in metadata['versions'].items()):
            raise ValueError('Artifact backend version mismatch')
        model = PadimModel(backbone='resnet18',layers=['layer1','layer2','layer3'],
                           pre_trained=False,n_features=100)
        model.load_state_dict(torch.load(state_path,map_location='cpu',weights_only=True),strict=True)
        if model.idx.tolist() != metadata['retained_channels']:
            raise ValueError('Artifact channel identity mismatch')
        adapter = cls(model,expected_recipe,metadata['input_shape'],metadata['weights'])
        adapter.fitted = True; adapter.fit_count = metadata['fit_count']
        return adapter
