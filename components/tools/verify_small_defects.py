"""Independent nested-study recount, provenance checks, and evidence export."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import subprocess

import numpy as np
from PIL import Image
from scipy.stats import beta
import torch


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def identity(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def write(path, value):
    with Path(path).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(value, f, indent=2, sort_keys=True, allow_nan=False); f.write('\n')


def check_identity(value):
    other = dict(value); expected = other.pop('identity')
    assert identity(other) == expected


def threshold_from_rows(rows, alpha):
    values = sorted(r['score'] for r in rows)
    n = len(values); k = math.ceil((n+1)*(1-alpha))
    assert 1 <= k <= n
    return values[k-1]


def recount(record, truth, areas):
    rows = record['predictions']
    assert len(rows) == len(truth) and {r['id'] for r in rows} == set(truth)
    threshold = record['threshold_record']['threshold']
    assert threshold_from_rows(record['calibration_scores'], .08) == threshold
    counts = Counter(TP=0, FN=0, FP=0, TN=0, rejected_anomalies=0, rejected_normals=0)
    for row in rows:
        assert row['status'] == 'scored' and row['label'] == truth[row['id']]
        assert np.isfinite(row['score']) and row['flagged'] == (row['score'] > threshold)
        counts[('TP' if row['flagged'] else 'FN') if row['label'] else ('FP' if row['flagged'] else 'TN')] += 1
    assert dict(counts) == record['metrics']['counts']
    positives, normals = sum(truth.values()), len(truth)-sum(truth.values())
    assert record['metrics']['recall']['rate'] == counts['TP']/positives
    assert record['metrics']['accepted_normal_fpr']['rate'] == counts['FP']/normals
    small = [r for r in rows if r['label'] and areas[r['id']] <= .005]
    assert record['small_defects'] == {'detected': sum(r['flagged'] for r in small), 'total': len(small)}
    return dict(counts)


def ranking(candidates):
    # Separately implemented from the worker selector.
    def key(item):
        name, rows = item
        fpr = [r['metrics']['counts']['FP']/r['metrics']['accepted_normal_fpr']['denominator'] for r in rows]
        recalls = [r['metrics']['counts']['TP']/r['metrics']['recall']['denominator'] for r in rows]
        total_small = sum(r['small_defects']['total'] for r in rows)
        small_rate = sum(r['small_defects']['detected'] for r in rows)/total_small if total_small else 0.
        worst = max(fpr)
        return (worst >= .1, worst if worst >= .1 else 0., -min(recalls),
                -sum(recalls)/len(recalls), -small_rate, sum(fpr)/len(fpr), name)
    return sorted(candidates, key=lambda name: key((name, candidates[name])))[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--export', type=Path, required=True)
    args = parser.parse_args(); root, target = args.root.resolve(), args.export.resolve()
    torch.set_num_threads(4)
    p, selected = read(root/'protocol.json'), read(root/'selection.json')
    check_identity(p); check_identity(selected)
    for file, expected in p['source_sha256'].items(): assert sha(file) == expected, file
    parent = read(Path(p['parent'])/'manifest.json'); check_identity(parent)
    assert parent['identity'] == p['parent_manifest_identity']
    by = {r['id']: r for r in parent['records']}
    pool, reserved = set(p['pool_ids']), set(p['reserved_normal_calibration_ids'])
    assert pool.isdisjoint(reserved) and len(pool) == 1914 and len(reserved) == 417
    assert all(by[i]['official_split'] == 'train' for i in pool | reserved)
    assert all(by[i]['label'] == 0 for i in reserved)
    assert sum(by[i]['label'] for i in pool) == 246
    for i, fraction in p['positive_source_area_fraction'].items():
        assert i in pool and by[i]['label'] == 1
        assert sha(by[i]['mask_path']) == by[i]['hashes']['mask_sha256']
        with Image.open(by[i]['mask_path']) as im:
            actual = float((np.asarray(im.convert('L')) > 0).mean())
        assert actual == fraction
    group_roles = {}
    for i in pool | reserved:
        role = p['folds'][i] if i in pool else 'reserved'
        group = by[i]['group']
        assert group not in group_roles or group_roles[group] == role
        group_roles[group] = role
    marker = read(root/'cache-complete.json')
    assert sha(root/'features/index.json') == marker['index_sha256']
    index = read(root/'features/index.json')
    assert set(index['rows']) == pool and marker['native_parity_count'] == 1914
    # Verify every feature artifact once; no official-test image is accessed.
    checked = 0
    for row in index['rows'].values():
        for key, value in row.items():
            if key.endswith('_path'):
                assert sha(value) == row[key[:-5]+'_sha256'], value
                checked += 1
    coverage = {}
    for grid in ('coarse', 'fine'):
        empty, partial = [], []
        for i in p['positive_source_area_fraction']:
            entry = index['rows'][i]
            target_array = np.load(entry[grid+'_target_path'], allow_pickle=False) > 0
            roi_array = np.load(entry[grid+'_roi_path'], allow_pickle=False)
            if not (target_array & roi_array).any(): empty.append(i)
            if (target_array & ~roi_array).any():
                partial.append({'id': i, 'outside_valid': int((target_array & ~roi_array).sum()),
                                'valid_positive': int((target_array & roi_array).sum())})
        coverage[grid] = {'positive_images': 246, 'empty_valid_target_ids': empty,
                          'partial_roi_boundary_targets': partial}
        assert not empty
    assert coverage == read(root/'target-coverage-audit.json')

    completed = [m for m in p['config']['methods'] if all((root/f'inner-{m}-{f}/complete.json').exists() for f in range(3))]
    inner, details = {}, {}
    normalization_cache = {}

    def verify_model(directory, cfg):
        plan, training = read(directory/'plan.json'), read(directory/'training.json')
        state = torch.load(directory/'model.pt', map_location='cpu', weights_only=True)
        assert sha(directory/'model.pt') == training['model_sha256']
        fit = set(plan['fitting_ids']); cal = set(plan.get('calibration_ids', []))
        assert training['fitting_ids'] == plan['fitting_ids']
        assert fit.isdisjoint(cal | reserved) and len(fit) == len(plan['fitting_ids'])
        if cal:
            assert len(cal) == 200 and all(by[i]['label'] == 0 for i in cal)
        if cfg['family'] == 'supervised':
            assert set(training['actual_learning_ids']) == fit
            assert len(training['history']) == cfg['epochs'] == 30
            assert all(np.isfinite(r['loss']) for r in training['history'])
        elif cfg['family'] == 'morphology':
            assert not training['actual_learning_ids'] and not training['normalization_ids']
        else:
            assert set(training['actual_learning_ids']) == {i for i in fit if not by[i]['label']}
            assert not training['history']
        for value in state.values():
            if isinstance(value, torch.Tensor): assert torch.isfinite(value).all()
        if cfg['family'] != 'morphology':
            normal_ids = sorted(i for i in fit if not by[i]['label'])
            assert set(normal_ids) == set(training['normalization_ids']) and len(normal_ids) == 256
            # Independently reconstruct channel moments from permitted normals.
            cache_key = (cfg['grid'], cfg['channels'], tuple(normal_ids))
            if cache_key not in normalization_cache:
                c = cfg['channels']; sums = np.zeros(c); squares = np.zeros(c); n = 0
                for i in normal_ids:
                    entry = index['rows'][i]
                    x = np.load(entry[cfg['grid']+'_path'], mmap_mode='r', allow_pickle=False)[:c]
                    roi = np.load(entry[cfg['grid']+'_roi_path'], allow_pickle=False)
                    x = x[:, roi].astype(np.float64)
                    sums += x.sum(1); squares += np.square(x).sum(1); n += x.shape[1]
                mean = sums/n; std = np.sqrt(np.maximum(squares/n-np.square(mean), .01))
                normalization_cache[cache_key] = (mean, std)
            mean, std = normalization_cache[cache_key]
            assert np.allclose(state['mean'].numpy().ravel(), mean, atol=1e-6, rtol=1e-6)
            assert np.allclose(state['std'].numpy().ravel(), std, atol=1e-6, rtol=1e-6)
            if cfg['family'] == 'patchcore': assert list(state['bank'].shape) == [512, 192]
            if cfg['family'] == 'pca':
                assert list(state['basis'].shape) == [192, 64]
                assert torch.allclose(state['basis'].T@state['basis'], torch.eye(64), atol=1e-5)
        return plan, training

    for method in completed:
        for train_fold in range(3):
            directory = root/f'inner-{method}-{train_fold}'
            plan, training = verify_model(directory, p['config']['methods'][method])
            assert all(p['folds'][i] == train_fold for i in plan['fitting_ids']+plan['calibration_ids'])
            for val_fold in range(3):
                if val_fold == train_fold: continue
                record = read(directory/f'eval-{val_fold}.json')
                expected = {i: by[i]['label'] for i in pool if p['folds'][i] == val_fold}
                counts = recount(record, expected, p['positive_source_area_fraction'])
                assert {r['id'] for r in record['calibration_scores']} == set(plan['calibration_ids'])
                inner[(method, train_fold, val_fold)] = record
                details[f'{method}:{train_fold}->{val_fold}'] = counts
    final_inputs = {m: [] for m in completed}
    for outer in range(3):
        allowed = [f for f in range(3) if f != outer]
        candidates = {m: [inner[(m, allowed[0], allowed[1])], inner[(m, allowed[1], allowed[0])]] for m in completed}
        assert ranking(candidates) == selected['outer_choices'][str(outer)]['method']
        for method, records in candidates.items(): final_inputs[method].extend(records)
        for files in selected['outer_choices'][str(outer)]['input_files'].values():
            for file in files:
                assert sha(file['path']) == file['sha256']
                record = read(file['path'])
                assert all(p['folds'][r['id']] != outer for r in record['predictions']+record['calibration_scores'])
    assert ranking(final_inputs) == selected['final_method']
    nested, outer_checks = [], {}
    for fold in range(3):
        directory = root/f'outer-{fold}'; method = selected['outer_choices'][str(fold)]['method']
        plan, training = verify_model(directory, p['config']['methods'][method])
        assert plan['method'] == method and plan['selection_identity'] == selected['identity']
        assert all(p['folds'][i] != fold for i in plan['fitting_ids']+plan['calibration_ids'])
        record = read(directory/f'eval-{fold}.json')
        expected = {i: by[i]['label'] for i in pool if p['folds'][i] == fold}
        counts = recount(record, expected, p['positive_source_area_fraction'])
        replay = read(directory/'replay.json'); assert replay['all_scores_exact']
        nested.extend(record['predictions']); outer_checks[str(fold)] = counts
    assert len(nested) == len(pool) and {r['id'] for r in nested} == pool
    summary = read(root/'nested-results.json')
    totals = Counter(TP=0, FN=0, FP=0, TN=0, rejected_anomalies=0, rejected_normals=0)
    for counts in outer_checks.values(): totals.update(counts)
    assert dict(totals) == summary['nested_metrics']['counts']
    tp, fp = totals['TP'], totals['FP']
    lower = 0. if tp == 0 else float(beta.ppf(.025, tp, 246-tp+1))
    upper = 1. if fp == 1668 else float(beta.ppf(.975, fp+1, 1668-fp))
    ci = summary['nested_confidence']
    assert abs(lower-ci['simultaneous_95_recall_lower']) < 1e-10
    assert abs(upper-ci['simultaneous_95_fpr_upper']) < 1e-10
    assert ci['point_goal_met'] == (tp/246 >= .95 and fp/1668 < .1)
    control_plan = read(root/'paired-control-plan.json'); check_identity(control_plan)
    assert control_plan['protocol_identity'] == p['identity']
    assert sha(Path(__file__).parent/'run_control_small_defects.py') == control_plan['source_sha256']
    control_totals = Counter(TP=0, FN=0, FP=0, TN=0, rejected_anomalies=0, rejected_normals=0)
    control_predictions = {}
    for fold in range(3):
        directory = root/f'control-outer-{fold}'
        plan, training = verify_model(directory, p['config']['methods']['coarse_control'])
        other_plan = read(root/f'outer-{fold}/plan.json')
        assert plan['paired_control_identity'] == control_plan['identity']
        assert plan['fitting_ids'] == other_plan['fitting_ids']
        assert plan['calibration_ids'] == other_plan['calibration_ids']
        expected = {i: by[i]['label'] for i in pool if p['folds'][i] == fold}
        record = read(directory/f'eval-{fold}.json')
        counts = recount(record, expected, p['positive_source_area_fraction'])
        control_totals.update(counts)
        control_predictions.update({r['id']: r for r in record['predictions']})
    assert set(control_predictions) == pool
    selected_predictions = {r['id']: r for r in nested}
    gains = [i for i in pool if by[i]['label'] and selected_predictions[i]['flagged'] and not control_predictions[i]['flagged']]
    losses = [i for i in pool if by[i]['label'] and not selected_predictions[i]['flagged'] and control_predictions[i]['flagged']]
    cleared = [i for i in pool if not by[i]['label'] and not selected_predictions[i]['flagged'] and control_predictions[i]['flagged']]
    new_alarms = [i for i in pool if not by[i]['label'] and selected_predictions[i]['flagged'] and not control_predictions[i]['flagged']]
    paired = {'selected_nested_counts': dict(totals), 'fixed_control_counts': dict(control_totals),
              'selected_minus_control_recall': (totals['TP']-control_totals['TP'])/246,
              'selected_minus_control_fpr': (totals['FP']-control_totals['FP'])/1668,
              'defects_gained_ids': sorted(gains), 'defects_lost_ids': sorted(losses),
              'false_alarms_cleared_ids': sorted(cleared), 'new_false_alarms_ids': sorted(new_alarms),
              'control_small_defects': {'detected': sum(r['flagged'] for i, r in control_predictions.items()
                                                       if by[i]['label'] and p['positive_source_area_fraction'][i] <= .005),
                                         'total': 45},
              'interpretation': 'same outer originals and fit/calibration IDs; internal paired estimate, no independence or factory-certification claim'}
    assert len(gains)-len(losses) == totals['TP']-control_totals['TP']
    assert len(new_alarms)-len(cleared) == totals['FP']-control_totals['FP']
    write(root/'paired-comparison.json', paired)
    frozen = read(root/'final/frozen.json'); check_identity(frozen)
    assert frozen['method'] == selected['final_method'] and frozen['selection_identity'] == selected['identity']
    assert sha(root/'final/model.pt') == frozen['model_sha256'] == summary['final_model_sha256']
    final_plan, _ = verify_model(root/'final', p['config']['methods'][frozen['method']])
    assert set(r['id'] for r in frozen['calibration_scores']) == reserved
    assert threshold_from_rows(frozen['calibration_scores'], .08) == frozen['threshold_record']['threshold']
    assert frozen['max_native_cache_score_difference'] <= 1e-5 and frozen['all_native_cache_decisions_equal']
    resources = {path.name: read(path) for path in root.glob('*-resources.json')}
    timing = {}
    for name, record in resources.items():
        resource_path = root/name
        worker_path = root/(name.removesuffix('-resources.json')+'-worker.log')
        def utc_birth(path):
            stat = path.stat()
            return datetime.fromtimestamp(getattr(stat, 'st_birthtime', stat.st_ctime), timezone.utc).isoformat()
        timing[name] = {'worker_log_created_utc': utc_birth(worker_path),
                        'resource_record_created_utc': utc_birth(resource_path),
                        'measured_elapsed_seconds': record['elapsed_seconds'],
                        'peak_sampled_rss_bytes': record['peak_sampled_rss_bytes'],
                        'status': record['status']}
        if record['status'] == 'completed':
            assert record['peak_sampled_rss_bytes'] <= record['rss_cap_bytes']
    write(root/'timing-and-storage.json', {
        'timing': timing,
        'timestamp_scope': 'filesystem creation of exclusive worker log and resource file; approximate phase bounds, not retroactively instrumented process UTC start/end',
        'model_artifacts': {str(path.relative_to(root)): {'sha256': sha(path), 'bytes': path.stat().st_size}
                            for path in root.rglob('model.pt')},
        'new_feature_array_bytes': sum(path.stat().st_size for path in (root/'features').glob('*.npy')),
    })
    protected = ['components/historical_benchmark', 'components/data/manifests', 'docs/research/validation',
                 'docs/research/round1', 'docs/research/round2', 'docs/research/alignment']
    changed = subprocess.check_output(['git', 'diff', '--name-only', p['source_commit'], '--', *protected], text=True)
    assert not changed.strip()
    verification = {'protocol_identity': p['identity'], 'verifier_sha256': sha(Path(__file__)),
                    'completed_methods': completed, 'inner_recounts': details, 'outer_recounts': outer_checks,
                    'independent_confidence_bounds': [lower, upper], 'feature_artifact_hashes_checked': checked,
                    'normal_only_moments_independently_reconstructed': len(normalization_cache),
                    'outer_selection_independently_verified': True, 'final_inner_selection_independently_verified': True,
                    'fixed_paired_control_independently_recounted': True,
                    'protected_old_benchmarks_unchanged': True, 'official_test_scored': False,
                    'new_independent_factory_validation_complete': False,
                    'pooled_cv_binomial_bounds_are_descriptive_not_formal_cv_confidence': True,
                    'resources': {n: r['status'] for n, r in resources.items()}}
    write(root/'verification.json', verification)
    target.mkdir(parents=True, exist_ok=False); exported = {}
    for path in sorted(root.rglob('*')):
        if path.suffix not in ('.json', '.log') or not path.is_file(): continue
        name = '--'.join(path.relative_to(root).parts)
        (target/name).write_bytes(path.read_bytes())
        assert sha(target/name) == sha(path)
        exported[name] = {'sha256': sha(path), 'bytes': path.stat().st_size}
    write(target/'export-index.json', {'protocol_identity': p['identity'], 'files': exported,
                                     'excluded': 'image arrays and model tensors remain local; their hashes are recorded'})
    print(json.dumps({'counts': dict(totals), 'bounds': [lower, upper], 'exported_files': len(exported),
                      'feature_hash_checks': checked}, indent=2))


if __name__ == '__main__': main()
