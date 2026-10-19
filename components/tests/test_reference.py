"""Literal scores and chunk equivalence verify a real normal-reference model."""
import importlib
import importlib.util

import numpy as np
import pytest


def api():
    name = 'component_inspector.vision.reference'
    assert importlib.util.find_spec(name), 'reference not implemented'
    return importlib.import_module(name)


def test_reference_chooses_nearest_bank_entry_and_score_is_in_rgb_squared_units():
    model = api().ReferenceModel(np.array([np.zeros((128,128,3)), np.ones((128,128,3))], dtype=np.float32), 'fixture')
    score, residual = model.predict_array(np.full((128,128,3), .75, np.float32), np.ones((128,128), bool))
    assert score == pytest.approx(.0625)
    assert residual.shape == (128,128)
    assert np.allclose(residual, .0625)


def test_padding_cannot_raise_score_and_chunked_matches_unchunked():
    module = api()
    rng = np.random.default_rng(19)
    bank = rng.random((9,128,128,3), dtype=np.float32)
    query = bank[3].copy()
    roi = np.zeros((128,128), bool); roi[32:96] = True
    query[~roi] = 100
    a = module.ReferenceModel(bank, 'fixture', chunk_size=1).predict_array(query, roi)
    b = module.ReferenceModel(bank, 'fixture', chunk_size=4).predict_array(query, roi)
    assert a[0] == pytest.approx(0)
    assert b[0] == pytest.approx(0)
    assert np.array_equal(a[1], b[1])


def test_reference_rejects_nan_or_shape_mismatch():
    module = api()
    model = module.ReferenceModel(np.zeros((1,128,128,3),np.float32), 'fixture')
    with pytest.raises(ValueError):
        model.predict_array(np.zeros((20,20,3),np.float32),np.ones((20,20),bool))
    with pytest.raises(ValueError):
        model.predict_array(np.full((128,128,3),np.nan,np.float32), np.ones((128,128),bool))


def test_reference_saved_bank_parity_and_hash_recipe_mismatch_rejected(tmp_path):
    module = api()
    rng = np.random.default_rng(7)
    bank = rng.random((3,128,128,3),dtype=np.float32)
    model = module.ReferenceModel(bank, 'fixture')
    path = tmp_path/'model'
    module.save_model(model, path, {'fit_manifest_hash': 'fixture-fit', 'reference_ids': ['a','b','c']})
    restored, metadata = module.load_model(path, expected_recipe='fixture')
    query = rng.random((128,128,3),dtype=np.float32); roi=np.ones((128,128),bool)
    assert np.array_equal(model.predict_array(query,roi)[1], restored.predict_array(query,roi)[1])
    assert metadata['threshold'] is None
    with pytest.raises(ValueError, match='recipe'):
        module.load_model(path, expected_recipe='other')
    with (path/'bank.npy').open('ab') as handle:
        handle.write(b'tampering')
    with pytest.raises(ValueError, match='hash'):
        module.load_model(path, expected_recipe='fixture')


def test_development_runner_follows_protocol_order_and_never_scores_test_records(tmp_path, monkeypatch):
    import json
    from dataclasses import asdict
    from PIL import Image
    import yaml
    from component_inspector.contracts import ImageRecord
    from component_inspector.data.acquire import sha256
    from component_inspector.data.split import digest
    from component_inspector.vision import develop
    recipes = ['mvtec_3d_cable_gland_rgb', 'ksdd2_surface']
    config_dir = tmp_path/'configs'; config_dir.mkdir()
    protocol = {'recipes': recipes}
    (config_dir/'protocol.yaml').write_text(yaml.safe_dump(protocol))
    sources, configs, records, refs = {}, {}, [], []
    for recipe, dataset, key in [(recipes[0], 'mvtec_3d_ad', 'mvtec_3d_cable_gland'),
                                 (recipes[1], 'ksdd2', 'ksdd2')]:
        raw = tmp_path/'data/raw'/key; raw.mkdir(parents=True)
        archive = tmp_path/'data'/f'{key}.archive'; archive.write_bytes(b'fictional')
        cfg = {'recipe_id': recipe, 'dataset': dataset, 'raw_root': raw.relative_to(tmp_path).as_posix(),
               'release_hash': sha256(archive), 'input': {'height': 128, 'width': 128, 'rotation_clockwise_degrees': 0}}
        configs[recipe] = cfg
        (config_dir/f'{recipe}.yaml').write_text(yaml.safe_dump(cfg))
        inventory = []
        for i in range(18):
            path = raw/f'{i}.png'; Image.new('RGB',(128,128),(i*10,0,0)).save(path)
            item = {'path': path.name, 'sha256': sha256(path), 'bytes': path.stat().st_size}; inventory.append(item)
            identity=f'{recipe}-{i}'
            records.append(ImageRecord(dataset=dataset, release_hash=sha256(archive),recipe=recipe,
                id=identity,path=str(path),mask_path=None,official_split='train' if i<17 else 'test',
                label=0,group=identity,hashes={'sha256': item['sha256']},
                experiment_role='fit' if i<16 else 'development' if i==16 else 'test'))
            if i<16:refs.append(identity)
        invdir=tmp_path/'data/manifests';invdir.mkdir(exist_ok=True)
        inv=invdir/f'{key}_inventory.json';inv.write_text(json.dumps(inventory))
        source={'dataset':dataset,'status':'acquired','raw_path':raw.relative_to(tmp_path).as_posix(),
                'license':'fixture','source_url':'https://example.invalid/fictional',
                'archive':{'path':archive.relative_to(tmp_path).as_posix(),'sha256':sha256(archive)},
                'inventory':{'path':inv.relative_to(tmp_path).as_posix(),'sha256':sha256(inv)}}
        sources[recipe]=source;(invdir/f'{key}_source.json').write_text(json.dumps(source))
    manifest={'protocol':protocol,'effective_recipes':configs,'sources':sources,
              'splits':{'records':[asdict(r) for r in records],'reference_ids':refs,'membership_hash':'fictional'}}
    folder=tmp_path/'data/manifests/stage2'/digest(manifest);folder.mkdir(parents=True)
    path=folder/'manifest.json';path.write_text(json.dumps(manifest,sort_keys=True))
    order=[];original=develop.ReferenceModel
    def tracked(bank,recipe_id):
        order.append(recipe_id);return original(bank,recipe_id)
    monkeypatch.setattr(develop,'ReferenceModel',tracked)
    result=develop.develop_reference(config_dir/'protocol.yaml',path)
    assert order==recipes
    report=json.loads((tmp_path/result['results_path']).read_text())
    assert all(x['development_images']==1 for x in report['recipes'].values())
    assert all(p['role']=='development' and p['id'].endswith('-16')
               for x in report['recipes'].values() for p in x['predictions'])
