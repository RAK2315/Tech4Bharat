"""Deterministic whole-group roles with explicit model-access guards."""
from dataclasses import asdict, replace
import hashlib
import json

from component_inspector.contracts import SplitManifest


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def assert_disjoint(records):
    groups = {}
    for r in records:
        if r.experiment_role == 'quarantine':
            continue
        if not r.group:
            raise ValueError('Missing audited group')
        key = (r.dataset, r.group)
        if key in groups and groups[key] != r.experiment_role:
            raise ValueError('Duplicate group crosses experiment roles')
        groups[key] = r.experiment_role


def split(records, seed=4217):
    if len({r.id for r in records}) != len(records):
        raise ValueError('Duplicate IDs')
    partitions = {}
    for r in records:
        if not r.group:
            raise ValueError('Records require audited groups')
        if not r.quarantine_reason:
            partitions.setdefault((r.dataset, r.group), set()).add(r.official_split)
    clean = []
    for r in records:
        p = partitions.get((r.dataset, r.group), set())
        reason = r.quarantine_reason
        if len(p) > 1 and r.official_split != ('train' if 'train' in p else 'validation'):
            reason = reason or 'cross_official_split_duplicate'
        clean.append(replace(r, quarantine_reason=reason))
    assigned, fit_ids, reference_ids = [], [], []
    for dataset in sorted({r.dataset for r in clean}):
        subset = [r for r in clean if r.dataset == dataset]
        train = [r for r in subset if r.official_split == 'train' and r.label == 0 and not r.quarantine_reason]
        groups = sorted({r.group for r in train}, key=lambda g: digest([seed, dataset, g]))
        nfit, ndev = round(len(groups)*.6), round(len(groups)*.2)
        allocation = {g: ('fit' if i < nfit else 'development' if i < nfit+ndev else 'calibration')
                      for i, g in enumerate(groups)}
        canonical = {g: min(r.id for r in train if r.group == g) for g in groups}
        used = [canonical[g] for g in groups[:min(nfit, 128)]]
        fit_ids += used; reference_ids += used[:16]
        for r in subset:
            if r.quarantine_reason:
                role = 'quarantine'
            elif r.official_split == 'test':
                role = 'test'
            elif r.official_split == 'validation' or (r.official_split == 'train' and r.label == 1):
                role = 'development'
            elif r.official_split == 'train' and r.label == 0:
                role = allocation[r.group]
                # Whole groups share a role; only canonical selected fit IDs are consumable.
                if role == 'fit' and canonical[r.group] not in used:
                    role = 'unused_fit'
            else:
                raise ValueError('Unknown partition/label')
            assigned.append(replace(r, experiment_role=role))
    assigned.sort(key=lambda r: r.id)
    assert_disjoint(assigned)
    membership = [{'id': r.id, 'group': r.group, 'role': r.experiment_role,
                   'hashes': r.hashes, 'quarantine_reason': r.quarantine_reason} for r in assigned]
    return SplitManifest(assigned, fit_ids, reference_ids,
                         digest({'records': membership, 'fit_ids': fit_ids, 'reference_ids': reference_ids, 'seed': seed}))


def select_for(records, purpose, *, ids=None):
    allowed = {'fit': {'fit'}, 'develop': {'development'},
               'calibrate': {'calibration'}, 'evaluate': {'test'}}
    if purpose not in allowed:
        raise ValueError('Unknown access purpose')
    selected = list(records) if ids is None else [r for r in records if r.id in set(ids)]
    if ids is not None and len(selected) != len(set(ids)):
        raise ValueError('Missing/duplicate requested IDs')
    assert_disjoint(selected)
    for r in selected:
        if r.quarantine_reason or r.experiment_role not in allowed[purpose]:
            raise ValueError('Forbidden experiment role access')
        if purpose in ('fit', 'calibrate') and r.label != 0:
            raise ValueError('Normal-only access required')
    return selected
