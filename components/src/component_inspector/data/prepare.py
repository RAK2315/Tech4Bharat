"""Verify sources, audit labels and publish content-addressed immutable roles."""
from collections import Counter
from dataclasses import asdict
import json
import logging
import os
from pathlib import Path
import tempfile

import yaml

from component_inspector.data.acquire import sha256, _no_links, _safe_path
from component_inspector.data.adapters import load_records
from component_inspector.data.audit import audit
from component_inspector.data.split import split, digest


def verify_source(root, key):
    root = Path(root)
    source_path = root/'data/manifests'/f'{key}_source.json'
    source = json.loads(source_path.read_text(encoding='utf-8'))
    if source['status'] != 'acquired' or not source.get('license') or not source.get('source_url'):
        raise ValueError('Source is not ready or missing provenance')
    archive, inventory_path = root/source['archive']['path'], root/source['inventory']['path']
    for path in (archive, inventory_path, root/source['raw_path']):
        if not path.resolve().is_relative_to(root.resolve()):
            raise ValueError('Source path escapes project')
        _no_links(path)
    if sha256(archive) != source['archive']['sha256'] or sha256(inventory_path) != source['inventory']['sha256']:
        raise ValueError('Source archive/inventory hash mismatch')
    inventory = json.loads(inventory_path.read_text(encoding='utf-8'))
    raw = root/source['raw_path']
    actual = {p.relative_to(raw).as_posix() for p in raw.rglob('*') if p.is_file()}
    if actual != {entry['path'] for entry in inventory}:
        raise ValueError('Raw inventory membership mismatch')
    checked_directories = set()
    for index, entry in enumerate(inventory):
        if index % 500 == 0:
            logging.getLogger(__name__).info('Source %s hashes %s/%s', key, index, len(inventory))
        path = raw/_safe_path(entry['path'])
        if path.parent not in checked_directories:
            _no_links(path.parent)
            checked_directories.add(path.parent)
        if path.is_symlink() or path.is_junction():
            raise ValueError('Raw inventory link rejected')
        if sha256(path) != entry['sha256']:
            raise ValueError('Raw file hash mismatch')
    return source


def prepare_project(config):
    config = Path(config).resolve()
    root = config.parent.parent
    protocol = yaml.safe_load(config.read_text(encoding='utf-8'))
    keys = {'mvtec_3d_ad': 'mvtec_3d_cable_gland', 'ksdd2': 'ksdd2'}
    manifests = root/'data/manifests'
    manifests.mkdir(parents=True, exist_ok=True)
    lock = manifests/'.prepare.lock'
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ValueError('Preparation already active; inspect stale lock manually') from exc
    os.close(fd)
    try:
        reports, effective, sources, records = {}, {}, {}, []
        for recipe in protocol['recipes']:
            logging.getLogger(__name__).info('Preparing recipe %s', recipe)
            cfg = yaml.safe_load((config.parent/f'{recipe}.yaml').read_text(encoding='utf-8'))
            if cfg['recipe_id'] != recipe or cfg['dataset'] not in keys:
                raise ValueError('Recipe identity mismatch')
            source = verify_source(root, keys[cfg['dataset']])
            if cfg.get('release_hash') not in (None, source['archive']['sha256']):
                raise ValueError('Recipe/source archive hash mismatch')
            raw = (root/source['raw_path']).resolve()
            configured_raw = (root/cfg['raw_root']).resolve()
            if configured_raw != raw and configured_raw != raw/'cable_gland':
                raise ValueError('Recipe raw root mismatch')
            source_records = load_records(cfg['dataset'], raw, source['archive']['sha256'])
            result = audit(source_records)
            cfg['release_hash'] = source['archive']['sha256']
            if cfg['dataset'] == 'ksdd2':
                portrait = {r.original_shape[0] > r.original_shape[1] for r in result.records
                            if r.official_split == 'train' and not r.quarantine_reason}
                if len(portrait) != 1:
                    raise ValueError('Training inventory has ambiguous orientation')
                cfg['input']['rotation_clockwise_degrees'] = 90 if portrait == {True} else 0
            records += result.records
            effective[recipe] = cfg
            sources[recipe] = source
            reports[recipe] = {'summary': result.summary, 'duplicate_pairs': result.duplicate_pairs}
        roles = split(records, protocol.get('seed', 4217))
        for recipe, info in reports.items():
            selected = [r for r in roles.records if r.recipe == recipe]
            info['role_counts'] = dict(Counter(r.experiment_role for r in selected))
            info['quarantine_reasons'] = dict(Counter(r.quarantine_reason for r in selected if r.quarantine_reason))
            info['normal_calibration_count'] = sum(r.experiment_role == 'calibration' for r in selected)
        payload = {'schema_version': 1, 'status': 'audited_roles_not_model_evaluated',
                   'protocol': protocol, 'effective_recipes': effective, 'sources': sources,
                   'audit': reports, 'splits': asdict(roles),
                   'source_code_hashes': {p.name: sha256(p) for p in
                        [Path(__file__), Path(__file__).with_name('audit.py'),
                         Path(__file__).with_name('adapters.py'), Path(__file__).with_name('split.py')]}}
        bundle_hash = digest(payload)
        directory = manifests/'stage2'/bundle_hash
        data = (json.dumps(payload, indent=2, sort_keys=True)+'\n').encode()
        if directory.exists():
            if (directory/'manifest.json').read_bytes() != data:
                raise ValueError('Existing immutable manifest mismatch')
        else:
            directory.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(prefix='.prepare-', dir=directory.parent) as scratch:
                temp = Path(scratch)/'bundle'; temp.mkdir()
                (temp/'manifest.json').write_bytes(data)
                for recipe in effective:
                    part = {'recipe': effective[recipe], 'source': sources[recipe], 'audit': reports[recipe],
                            'records': [asdict(r) for r in roles.records if r.recipe == recipe],
                            'membership_hash': roles.membership_hash}
                    (temp/f'{recipe}.json').write_text(json.dumps(part, indent=2, sort_keys=True)+'\n', encoding='utf-8')
                temp.rename(directory)
        return {'status': payload['status'], 'membership_hash': roles.membership_hash,
                'manifest_sha256': sha256(directory/'manifest.json'),
                'manifest_path': (directory/'manifest.json').relative_to(root).as_posix(),
                'audit': {k: {'summary': v['summary'], 'role_counts': v['role_counts'],
                              'quarantine_reasons': v['quarantine_reasons']} for k, v in reports.items()}}
    finally:
        lock.unlink(missing_ok=True)
