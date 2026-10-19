"""Fictional images exercise schema, mask and leakage contracts, not accuracy."""
import importlib
import importlib.util
from dataclasses import replace
from pathlib import Path

import pytest
from PIL import Image


def api(name):
    module = 'component_inspector.data.' + name
    assert importlib.util.find_spec(module), f'{name} not implemented'
    return importlib.import_module(module)


def image(path, value=40, mask=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new('L' if mask else 'RGB', (16, 24), value).save(path)


def test_cable_adapter_only_rgb_preserves_validation_and_pairs_test_mask(tmp_path):
    image(tmp_path / 'cable_gland/train/good/rgb/000.png')
    image(tmp_path / 'cable_gland/validation/good/rgb/000.png', 100)
    image(tmp_path / 'cable_gland/test/thread/rgb/000.png', 150)
    image(tmp_path / 'cable_gland/test/thread/gt/000.png', 255, True)
    (tmp_path / 'cable_gland/train/good/xyz').mkdir()
    (tmp_path / 'cable_gland/train/good/xyz/000.tiff').write_bytes(b'inert')
    records = api('adapters').load_records('mvtec_3d_ad', tmp_path, 'fixture')
    assert len(records) == 3
    assert {r.official_split for r in records} == {'train', 'validation', 'test'}
    defect = next(r for r in records if r.label == 1)
    assert defect.mask_path.endswith('test/thread/gt/000.png')
    assert all('/rgb/' in r.path.replace('\\', '/') for r in records)


def test_ksdd2_labels_come_from_masks_and_missing_masks_are_quarantined(tmp_path):
    for name in ['a', 'b', 'c']:
        image(tmp_path / f'train/{name}.png')
    image(tmp_path / 'train/a_GT.png', 0, True)
    image(tmp_path / 'train/b_GT.png', 255, True)
    records = api('adapters').load_records('ksdd2', tmp_path, 'fixture')
    by_id = {Path(r.path).stem: r for r in records}
    assert by_id['a'].label == 0
    assert by_id['b'].label == 1
    assert by_id['c'].label is None
    assert by_id['c'].quarantine_reason == 'missing_mask'


def test_audit_rejects_defect_without_mask_and_dimension_mismatch(tmp_path):
    image(tmp_path / 'cable_gland/test/cut/rgb/a.png')
    image(tmp_path / 'cable_gland/test/hole/rgb/b.png')
    image(tmp_path / 'cable_gland/test/hole/gt/b.png', 255, True)
    Image.new('L', (2, 2), 255).save(tmp_path / 'cable_gland/test/hole/gt/b.png')
    records = api('adapters').load_records('mvtec_3d_ad', tmp_path, 'fixture')
    report = api('audit').audit(records)
    assert {r.quarantine_reason for r in report.records} == {'missing_mask', 'mask_shape_mismatch'}


def records(count=20):
    cls = importlib.import_module('component_inspector.contracts').ImageRecord
    return [cls(dataset='fixture', release_hash='fixture', recipe='fixture',
                id=f'normal-{i:02}', path=f'normal-{i:02}.png', mask_path=None,
                official_split='train', label=0, group=f'g-{i:02}') for i in range(count)]


def test_split_deterministic_counts_normal_only_and_validation_development():
    split = api('split')
    source = records()
    extra = [replace(source[0], id='v', path='v.png', group='gv', official_split='validation'),
             replace(source[0], id='d', path='d.png', group='gd', label=1),
             replace(source[0], id='t', path='t.png', group='gt', official_split='test', label=1)]
    first = split.split(source + extra)
    second = split.split(list(reversed(source + extra)))
    assert first.membership_hash == second.membership_hash
    by_role = {role: [r for r in first.records if r.experiment_role == role]
               for role in ['fit', 'development', 'calibration', 'test']}
    assert [len(by_role[x]) for x in by_role] == [12, 6, 4, 1]
    assert all(r.label == 0 for r in by_role['fit'] + by_role['calibration'])
    assert len(first.reference_ids) == 12


def test_duplicate_group_cannot_cross_fit_calibration_or_official_partitions():
    split = api('split')
    source = records()
    with pytest.raises(ValueError, match='group'):
        split.assert_disjoint([replace(source[0], experiment_role='fit'),
                               replace(source[0], id='other', experiment_role='calibration')])
    result = split.split(source + [replace(source[0], id='leaked-test', official_split='test')])
    leaked = next(r for r in result.records if r.id == 'leaked-test')
    assert leaked.experiment_role == 'quarantine'
    assert leaked.quarantine_reason == 'cross_official_split_duplicate'


def test_access_guard_blocks_test_calibration_defects_and_unused_fit():
    split = api('split')
    source = records(230)
    result = split.split(source)
    assert len(result.fit_ids) == 128
    assert len(result.reference_ids) == 16
    for role, label in [('test', 0), ('calibration', 0), ('fit', 1), ('unused_fit', 0)]:
        with pytest.raises(ValueError):
            split.select_for([replace(source[0], experiment_role=role, label=label)], 'fit')
    assert split.select_for(result.records, 'fit', ids=result.fit_ids)


def test_audit_groups_identical_pixels_even_when_png_bytes_differ(tmp_path):
    from PIL.PngImagePlugin import PngInfo
    image(tmp_path / 'train/a.png')
    meta = PngInfo(); meta.add_text('fixture', 'different encoding metadata')
    Image.open(tmp_path / 'train/a.png').save(tmp_path / 'train/b.png', pnginfo=meta)
    for name in ['a', 'b']:
        image(tmp_path / f'train/{name}_GT.png', 0, True)
    report = api('audit').audit(api('adapters').load_records('ksdd2', tmp_path, 'fixture'))
    assert len({r.group for r in report.records}) == 1
    assert len({r.hashes['sha256'] for r in report.records}) == 2
    assert len({r.hashes['decoded_sha256'] for r in report.records}) == 1


def test_prepare_publishes_immutable_manifest_and_detects_raw_tampering(tmp_path):
    import hashlib
    import json
    import random
    import yaml
    from PIL import Image
    raw = tmp_path / 'data/raw/ksdd2'
    inventory = []
    for i in range(25):
        path = raw / f'train/{i}.png'
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.frombytes('RGB', (16, 24), random.Random(i).randbytes(16*24*3)).save(path)
        image(raw / f'train/{i}_GT.png', 0, True)
    for path in raw.rglob('*.png'):
        inventory.append({'path': path.relative_to(raw).as_posix(), 'bytes': path.stat().st_size,
                          'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    manifests = tmp_path / 'data/manifests'; manifests.mkdir(parents=True)
    inv = manifests / 'inventory.json'; inv.write_text(json.dumps(inventory))
    archive = tmp_path / 'data/archive'; archive.write_bytes(b'fixture archive identity only')
    source = {'dataset': 'ksdd2', 'status': 'acquired', 'raw_path': 'data/raw/ksdd2',
              'license': 'CC-BY-NC-SA-4.0', 'source_url': 'https://www.vicos.si/resources/kolektorsdd2/',
              'archive': {'path': 'data/archive', 'sha256': hashlib.sha256(archive.read_bytes()).hexdigest()},
              'inventory': {'path': 'data/manifests/inventory.json', 'sha256': hashlib.sha256(inv.read_bytes()).hexdigest()}}
    (manifests/'ksdd2_source.json').write_text(json.dumps(source))
    configs = tmp_path/'configs'; configs.mkdir()
    (configs/'protocol.yaml').write_text(yaml.safe_dump({'seed': 4217, 'recipes': ['ksdd2_surface']}))
    (configs/'ksdd2_surface.yaml').write_text(yaml.safe_dump({'dataset': 'ksdd2', 'recipe_id': 'ksdd2_surface',
        'raw_root': 'data/raw/ksdd2', 'release_hash': None, 'input': {'rotation_clockwise_degrees': None}}))
    prepare = api('prepare')
    first = prepare.prepare_project(configs/'protocol.yaml')
    second = prepare.prepare_project(configs/'protocol.yaml')
    assert first['membership_hash'] == second['membership_hash']
    assert (tmp_path/first['manifest_path']).is_file()
    (raw/'train/0.png').write_bytes(b'tampered')
    with pytest.raises(ValueError, match='hash'):
        prepare.prepare_project(configs/'protocol.yaml')


def test_near_normal_and_tiny_defect_are_not_discarded_as_duplicate_label_conflict(tmp_path):
    import random
    (tmp_path/'train').mkdir()
    picture = Image.frombytes('RGB', (16, 24), random.Random(19).randbytes(16*24*3))
    picture.save(tmp_path/'train/a.png')
    image(tmp_path/'train/a_GT.png', 0, True)
    pixel = picture.getpixel((4, 5))
    picture.putpixel((4, 5), tuple(min(255, x+2) for x in pixel))
    picture.save(tmp_path/'train/b.png')
    mask = Image.new('L', (16, 24), 0); mask.putpixel((4, 5), 255)
    mask.save(tmp_path/'train/b_GT.png')
    result = api('audit').audit(api('adapters').load_records('ksdd2', tmp_path, 'fixture'))
    assert all(r.quarantine_reason is None for r in result.records)
    assert len({r.group for r in result.records}) == 2


def test_cable_class_id_masks_are_valid_binary_anomaly_regions(tmp_path):
    import json
    image(tmp_path/'cable_gland/test/thread/rgb/a.png')
    image(tmp_path/'cable_gland/test/thread/gt/a.png', 252, True)
    (tmp_path/'cable_gland/class_ids.json').write_text(json.dumps({'0': 'good', '252': 'thread',
        '253': 'hole', '254': 'cut', '255': 'bent'}))
    result = api('audit').audit(api('adapters').load_records('mvtec_3d_ad', tmp_path, 'fixture'))
    assert result.records[0].label == 1
    assert result.records[0].quarantine_reason is None
    assert result.records[0].provenance['mask_positive_value'] == 252
