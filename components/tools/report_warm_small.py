"""Generate the warm-study report only after independent verification."""
import argparse
import json
from pathlib import Path


def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def pct(value): return f'{100*value:.2f}%'


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True); args=parser.parse_args()
    root=args.root.resolve(); p=read(root/'protocol.json'); s=read(root/'summary.json'); v=read(root/'verification.json')
    paired=read(root/'paired-changes.json')['comparisons']
    cfg=p['config']; method=s['selected_method']; alpha=s['selected_alpha']; checks=s['checks']
    assert s['protocol_identity']==v['protocol_identity']==p['identity']
    outcome=('All twelve predeclared internal checks meet the point targets.' if s['all_twelve_internal_goals_met'] else
             'The requested across-fold consistency target is not achieved in this study.')
    lines=['# Warm-recipe small-defect study: verified internal results','',f'**{outcome}**', '',
           f'The locked development selection is **{method}, normal-calibration alpha {alpha:.2f}**. '
           f'All nine development checks passed: **{s["all_nine_development_goals_met"]}**. '
           f'All three second-partition checks passed: **{s["all_three_second_partition_goals_met"]}**. '
           'Each required recall >=95% and normal false-positive rate <10%. A pooled average '
           'cannot rescue a failing fold or seed.', '',
           'These are KSDD2 industrial surface-defect images from the official training set. '
           'All 1,914 originals had already been observed in the project. The second partition '
           'changes fitting/calibration/evaluation membership and initialization; it does not '
           'supply unseen factory images or erase historical selection exposure. The official '
           'test remained closed, the 417 reserved normals remained unused, and no independent '
           'production guarantee is established. Recall here means correctly flagging a defective '
           'image, including the small-defect subset; pixel localization accuracy is a separate claim.', '',
           '## Every development candidate and fixed calibration policy','',
           '| Method | Alpha | Passed cases / 9 | Worst recall | Worst normal FPR | Worst small / 15 |',
           '|---|---:|---:|---:|---:|---:|']
    for m in cfg['methods']:
        for a in cfg['alphas']:
            rows=[checks[f'dev-f{f}-s{seed}-{m}/{a:.2f}'] for seed in cfg['development_seeds'] for f in range(3)]
            lines.append(f'| {m} | {a:.2f} | {sum(r["point_goal_met"] for r in rows)}/9 | {pct(min(r["recall"] for r in rows))} | {pct(max(r["fpr"] for r in rows))} | {min(r["small_defects"]["detected"] for r in rows)}/15 |')
    lines += ['', 'All methods and both policies were fixed before the first new feature-cache or '
              'fit phase. Alpha .05 and .08 are two declared development policies, not a threshold '
              'scan on the official test. Every threshold uses only 200 disjoint normal training '
              'originals with strict score > threshold. Selection sees only the nine development '
              'cases per policy. No best seed is chosen.', '',
              '## Paired aggregates, kept separate for each seed','',
              '| Stage | Seed | Recipe / policy | TP / 246 | FP / 1,668 | Recall | Normal FPR | Small / 45 |',
              '|---|---:|---|---:|---:|---:|---:|---:|']
    def aggregate(stage,seed,m,a):
        rows=[checks[f'{stage}-f{f}-s{seed}-{m}/{a:.2f}'] for f in range(3)]
        tp=sum(r['counts']['TP'] for r in rows); fp=sum(r['counts']['FP'] for r in rows)
        small=sum(r['small_defects']['detected'] for r in rows)
        return tp,fp,small
    for stage,seeds in [('dev',cfg['development_seeds']),('confirm',[cfg['confirmation_seed']])]:
        for seed in seeds:
            for m,a in dict.fromkeys([('baseline84',.08),('baseline84',alpha),(method,alpha)]):
                tp,fp,small=aggregate(stage,seed,m,a)
                lines.append(f'| {stage} | {seed} | {m} / {a:.2f} | {tp}/246 | {fp}/1,668 | {pct(tp/246)} | {pct(fp/1668)} | {small}/45 |')
    lines += ['', 'Each aggregate uses exactly 246 defects and 1,668 normals for that seed and '
              'partition. The same images recur across seeds and partitions; denominators are '
              'not added to fabricate a larger independent sample. Raw scores from different '
              'models are not pooled into AUROC/AP. The same-alpha baseline comparison separates '
              'training changes from calibration-policy changes; baseline alpha .08 also keeps '
              'the prior common operating policy visible.', '',
              '## Locked second-partition results','',
              '| Fold | Method | Alpha | TP / 82 | FP / 556 | Recall | Normal FPR | Small / 15 | Point goal |',
              '|---|---|---:|---:|---:|---:|---:|---:|---|']
    for f in range(3):
        for m,a in dict.fromkeys([('baseline84',.08),('baseline84',alpha),(method,alpha)]):
            r=checks[f'confirm-f{f}-s{cfg["confirmation_seed"]}-{m}/{a:.2f}']; c=r['counts']
            lines.append(f'| {f} | {m} | {a:.2f} | {c["TP"]}/82 | {c["FP"]}/556 | {pct(r["recall"])} | {pct(r["fpr"])} | {r["small_defects"]["detected"]}/15 | {"Pass" if r["point_goal_met"] else "Fail"} |')
    lines += ['', '## Detections gained and lost against the same-policy baseline','',
              '| Stage | Seed | Small gained / lost | Large gained / lost | Normal alarms added / avoided |',
              '|---|---:|---:|---:|---:|']
    for stage,seeds in [('dev',cfg['development_seeds']),('confirm',[cfg['confirmation_seed']])]:
        for seed in seeds:
            if method=='baseline84':
                lines.append(f'| {stage} | {seed} | 0 / 0 | 0 / 0 | 0 / 0 |'); continue
            changes=[paired[f'{stage}-f{f}-s{seed}-{method}/{alpha:.2f}'] for f in range(3)]
            pairs=[]
            for stratum in ('small_defects','large_defects','normals'):
                pairs.append(' / '.join(str(sum(len(r[stratum][key]) for r in changes))
                             for key in ('newly_flagged_ids','no_longer_flagged_ids')))
            lines.append(f'| {stage} | {seed} | '+ ' | '.join(pairs)+' |')
    lines += ['', 'Gains and losses refer to the exact same originals and alpha within each '
              'fold/seed pair. For defects, newly flagged means a detection gained; for normal '
              'items, it means a false alarm added. Full per-original IDs and all candidate '
              'comparisons are retained in [paired changes](warm-small/paired-changes.json). '
              'Large-defect counts are stored separately alongside small-defect counts in '
              '[summary](warm-small/summary.json).', '',
              'The selected method and alpha were frozen before any second-partition '
              'inference. No change in candidate, threshold, seed, number of epochs, crop geometry '
              'or small-defect definition followed these results. The baseline and selected '
              'recipe use identical fitting and calibration parent identities within each pair.', '',
              '## What was actually changed','',
              'The full baseline is the prior 60+12+12 recipe. Its three audited seed4217 '
              'development checkpoints are reused byte-for-byte; all other baselines are fresh '
              'fits. Each continuation adds 24 fixed aligned-objective epochs from the same '
              'fold/seed baseline, with the same optimizer reset, presentation order, and '
              'fitting parents. longer108 is the matched continuation control. small108 weights '
              'small-positive loss by 3. tiles108 substitutes a native 160x160 crop for a full '
              'image with probability .5, enlarged to 256x256. tiles_small108 combines those '
              'two factors. None changes backbone weights, head capacity, or baseline moments.', '',
              'Positive training crops are chosen from the fitting parent’s positive GT crops; '
              'normal parents use any crop. At inference, masks, labels and size strata do not '
              'choose views: tiled recipes score the full image and all ten overlapping crops, '
              'taking their maximum. The complete score is calibrated on normal training '
              'parents, accounting for the additional opportunities to flag an image. Every '
              'view remains attached to its original parent; crops are not independent samples.', '',
              'Sources and all implementation limits are in the '
              '[preregistered protocol](2026-10-20-warm-small-protocol.md). This is an adaptation '
              'of slicing and mask-supervised inspection ideas using our existing frozen '
              'ResNet18 features, not a claim to reproduce full SAHI or SegDec-Net results.', '',
              '## Verifiable evidence and limits','',
              f'The separate arithmetic/role verifier checked **{v["feature_artifact_hashes_checked"]} '
              f'feature artifacts**, derived labels and size fractions from **{v["raw_training_mask_hashes_and_labels_checked"]} '
              'hashed original masks, independently reconstructed the second partition, '
              f'{v["normalization_sets_reconstructed"]} normalization sets, '
              f'{v["hard_normal_scores_reconstructed"]} hard-normal candidate scores from saved '
              f'epoch60 weights, and {v["training_crop_choices_reconstructed"]} training-crop '
              'choices from registered generators. It verified unchanged normalization and '
              'unused classifier weights in continuations, every calibration quantile, all '
              'metric rows, the development-only selection, and the paired role exclusions.', '',
              f'It also recomputed **{v["calibration_scores_reconstructed_from_weights"]} calibration '
              'scores** directly from saved convolution weights, independently of the experiment’s '
              'head/scoring functions, and checked the dependency lock, installed library versions '
              'and pretrained backbone hash.', '',
              f'Full native replay regenerated **{s["native_head_evaluations"]} head scores** and '
              f'**{s["native_threshold_evaluations"]} decisions** on the same 1,914 original RGB '
              'images without cached features or GT masks. Scores matched within 1e-5 and every '
              'decision matched; the three replay records report exact equality separately. '
              'These are repeated implementation checks, not additional independent images. '
              'The verifier was authored in this same work session; third-party certification '
              'is not claimed.', '',
              'Preflight: 131 software tests passed with 45 upstream warnings; old baseline '
              'scores matched on the two checked originals; all ten native crop feature '
              'shapes/values passed the smoke check. Historical evidence remains unchanged. '
              'Worker resources include all measured elapsed times and owned-process-tree RSS '
              'peaks; the fixed limits are four threads, 1,800 seconds and min(4GiB,60% free RAM) '
              'per phase. Timings are measurements of these runs, not controlled hardware claims.', '',
              'Overlapping training sets, repeated original images, prior project exposure and '
              'unknown physical-product identity limit statistical interpretation. Binomial '
              'intervals stored per record are descriptive, not formal exact CV confidence or '
              'a production guarantee. A new sealed, blindly labeled factory batch is still '
              'required for independent confirmation; see the '
              '[collection plan](2026-10-20-fresh-confirmation-plan.md).', '',
              f'Frozen source commit: `{p["source_commit"]}`. Protocol identity: `{p["identity"]}`. '
              'The snapshot was published before new cache/fitting phases. Model tensors and '
              'arrays remain local, with hashes; exported records preserve exact IDs, thresholds, '
              'predictions, losses, parent/view usage and logs.', '',
              'Evidence: [summary](warm-small/summary.json), '
              '[selection](warm-small/selection.json), [verification](warm-small/verification.json), '
              '[export hash index](warm-small/export-index.json), '
              '[preregistration snapshot](2026-10-20-warm-small-preregistration.json).', '',
              '## Every development fold and seed','',
              '| Method | Alpha | Seed | Fold | TP / 82 | FP / 556 | Small / 15 | Point goal |',
              '|---|---:|---:|---:|---:|---:|---:|---|']
    for m in cfg['methods']:
        for a in cfg['alphas']:
            for seed in cfg['development_seeds']:
                for f in range(3):
                    r=checks[f'dev-f{f}-s{seed}-{m}/{a:.2f}']; c=r['counts']
                    lines.append(f'| {m} | {a:.2f} | {seed} | {f} | {c["TP"]}/82 | {c["FP"]}/556 | {r["small_defects"]["detected"]}/15 | {"Pass" if r["point_goal_met"] else "Fail"} |')
    lines += ['', '## Reproduce','',
              'Use the locked environment and official-training originals/parent cache. Audit '
              'this preserved run into a new empty export path with verify_warm_small.py. '
              'A new fit requires new empty paths and a newly published preregistration '
              'snapshot; pass its path using --registration. New timestamps, paths and source '
              'commits produce a new protocol identity, not a copy of this study’s identity.', '',
              '```powershell',
              'components/.venv-p0/Scripts/python.exe -m component_inspector.research.ksdd2_warm_small --phase freeze --root components/outputs/recall-warm-small',
              '# Publish matching protocol/preflight snapshots before starting new cache or fit phases.',
              'components/.venv-p0/Scripts/python.exe components/tools/run_warm_small.py --root components/outputs/recall-warm-small',
              '# Run replay_warm_small.py serially for --fold 0, then 1, then 2.',
              'components/.venv-p0/Scripts/python.exe components/tools/verify_warm_small.py --root components/outputs/recall-warm-small --export docs/research/warm-small',
              '```','']
    with args.output.open('x',encoding='utf-8',newline='\n') as f: f.write('\n'.join(lines))
    print(args.output)


if __name__=='__main__': main()
