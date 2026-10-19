"""Run B0 only on allowed fit/development IDs; no calibration or test predictions."""
from dataclasses import asdict
import json
import logging
from pathlib import Path
import threading
import time
from importlib.metadata import version

import numpy as np
from PIL import Image
import psutil

from component_inspector.contracts import ImageRecord
from component_inspector.data.acquire import sha256
from component_inspector.data.prepare import verify_source
from component_inspector.data.split import select_for, digest, assert_disjoint
from component_inspector.vision.geometry import prepare, restore_map
from component_inspector.vision.reference import ReferenceModel, save_model, load_model


class MemoryMonitor:
    def __enter__(self):
        self.stop = threading.Event()
        self.peak = psutil.Process().memory_info().rss
        def sample():
            while not self.stop.wait(.02):
                self.peak = max(self.peak, psutil.Process().memory_info().rss)
        self.worker = threading.Thread(target=sample, daemon=True); self.worker.start()
        return self

    def __exit__(self, *_):
        self.stop.set(); self.worker.join()
        self.peak = max(self.peak, psutil.Process().memory_info().rss)


def load_manifest(root, path):
    root, path = Path(root).resolve(), Path(path).resolve()
    if not path.is_relative_to(root/'data/manifests/stage2'):
        raise ValueError('Manifest must be a project-local audited bundle')
    manifest = json.loads(path.read_text(encoding='utf-8'))
    if digest(manifest) != path.parent.name:
        raise ValueError('Manifest content hash mismatch')
    records = [ImageRecord(**r) for r in manifest['splits']['records']]
    assert_disjoint(records)
    return manifest, records


def develop_reference(config, manifest_path):
    config = Path(config).resolve(); root = config.parent.parent
    manifest_path = Path(manifest_path).resolve()
    manifest, records = load_manifest(root, manifest_path)
    if manifest['protocol'] != __import__('yaml').safe_load(config.read_text(encoding='utf-8')):
        raise ValueError('Current protocol differs from audited protocol')
    for recipe, source in manifest['sources'].items():
        key = 'mvtec_3d_cable_gland' if source['dataset'] == 'mvtec_3d_ad' else 'ksdd2'
        if verify_source(root, key) != source:
            raise ValueError('Source record changed since audit')
        cfg_path = config.parent/f'{recipe}.yaml'
        current = __import__('yaml').safe_load(cfg_path.read_text(encoding='utf-8'))
        effective = manifest['effective_recipes'][recipe]
        # Only the two declared resolution fields may differ from a draft source config.
        current['release_hash'] = source['archive']['sha256']
        if source['dataset'] == 'ksdd2':
            current['input']['rotation_clockwise_degrees'] = effective['input']['rotation_clockwise_degrees']
        if current != effective:
            raise ValueError('Recipe differs from audited geometry/configuration')
    identities = {name: sha256(Path(__file__).with_name(name)) for name in ['develop.py', 'geometry.py', 'reference.py']}
    run_id = digest({'manifest': sha256(manifest_path), 'code': identities})
    output = root/'outputs/stage3'/run_id
    if output.exists():
        raise ValueError('Development run already exists; inspect saved evidence rather than overwrite')
    output.mkdir(parents=True)
    results = {'run_id': run_id, 'manifest_sha256': sha256(manifest_path),
               'membership_hash': manifest['splits']['membership_hash'], 'code_hashes': identities,
               'environment': {name: version(name) for name in ['numpy', 'scipy', 'Pillow']},
               'status': 'development_only_uncalibrated', 'recipes': {}}
    with MemoryMonitor() as monitor:
        for recipe in manifest['protocol']['recipes']:
            cfg = manifest['effective_recipes'][recipe]
            rr = [r for r in records if r.recipe == recipe]
            references = [i for i in manifest['splits']['reference_ids'] if i in {r.id for r in rr}]
            fit = select_for(rr, 'fit', ids=references)
            if len(fit) != 16:
                raise ValueError('Baseline requires 16 selected normal fit references')
            development = select_for(rr, 'develop', ids=[r.id for r in rr if r.experiment_role == 'development'])
            logging.getLogger(__name__).info('B0 %s: fitting 16 references, %s development queries', recipe, len(development))
            start = time.perf_counter(); bank = []
            for r in fit:
                if sha256(r.path) != r.hashes['sha256']:
                    raise ValueError('Fit image hash changed')
                with Image.open(r.path) as image:
                    bank.append(prepare(image, cfg).rgb_float32)
            model = ReferenceModel(np.stack(bank), recipe)
            fit_seconds = time.perf_counter()-start
            model_path = root/'models'/recipe/f'reference-{run_id}'
            save_model(model, model_path, {'fit_manifest_hash': results['manifest_sha256'],
                'reference_ids': references, 'geometry': cfg['input'], 'membership_hash': results['membership_hash']})
            restored, metadata = load_model(model_path, expected_recipe=recipe)
            rows, times = [], []
            for index, r in enumerate(development):
                if index % 100 == 0:
                    logging.getLogger(__name__).info('B0 %s development %s/%s', recipe, index, len(development))
                if sha256(r.path) != r.hashes['sha256']:
                    raise ValueError('Development image hash changed')
                tick = time.perf_counter()
                with Image.open(r.path) as image:
                    prepared = prepare(image, cfg)
                score, raw = model.predict_array(prepared.rgb_float32, prepared.valid_roi)
                original = restore_map(raw, prepared.geometry)
                elapsed = time.perf_counter()-tick; times.append(elapsed)
                if not np.isfinite(score) or original.shape != prepared.original_shape:
                    raise ValueError('Nonfinite/misaligned reference prediction')
                if index == 0:
                    parity = restored.predict_array(prepared.rgb_float32, prepared.valid_roi)
                    if score != parity[0] or not np.array_equal(raw, parity[1]):
                        raise ValueError('Saved reference raw-score/map parity failed')
                    np.save(output/f'{recipe}_development_sample_map.npy', original, allow_pickle=False)
                rows.append({'id': r.id, 'role': 'development', 'score': score,
                             'threshold': None, 'flagged': None, 'seconds': elapsed})
            report = {'references': references, 'selected_fit_groups': len({r.group for r in fit}),
                'development_images': len(rows), 'fit_seconds': fit_seconds,
                'cold_pipeline_seconds': times[0] if times else None,
                'warm_p95_pipeline_seconds': float(np.percentile(times[1:],95)) if len(times)>1 else None,
                'model_bytes': sum(p.stat().st_size for p in model_path.iterdir() if p.is_file()),
                'artifact_path': model_path.relative_to(root).as_posix(), 'save_load_parity': 'exact',
                'threshold': None, 'flagged': None, 'predictions': rows}
            results['recipes'][recipe] = report
    results['peak_sampled_rss_bytes'] = monitor.peak
    if monitor.peak > 4*1024**3:
        raise ValueError('Baseline process exceeded resource cap')
    (output/'results.json').write_text(json.dumps(results, indent=2, sort_keys=True)+'\n', encoding='utf-8')
    return {'status': results['status'], 'results_path': (output/'results.json').relative_to(root).as_posix(),
            'results_sha256': sha256(output/'results.json'), 'peak_sampled_rss_bytes': monitor.peak,
            'recipes': {k: {a:b for a,b in v.items() if a not in ('predictions','references')} for k,v in results['recipes'].items()}}
