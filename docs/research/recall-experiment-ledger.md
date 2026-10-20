# Recall experiment ledger

Created 19 October 2026; updated 20 October 2026. **Baseline, bounded R01–R10 review and alignment correction completed.** Best numerical checkpoint: **97.56% recall / 5.28% normal FPR**. Its original training recipe fails one repeat; the corrected recipe meets the goal in **all three fixed seeds: 95.12%–96.34% recall / 6.95%–7.67% FPR**. One corrected continuation reaches **97.56% / 5.76%**. R07 is deferred with a task-specific reason. See [round 1](2026-10-19-round1-results.md), [round 2](2026-10-20-round2-results.md) and [alignment correction](2026-10-20-alignment-results.md).

Research and source rationale: [ten strategies](2026-10-19-recall-strategies.md). Saved-score-only diagnostic: [audit JSON](2026-10-19-observed-score-audit.json).

## Fixed historical comparator

| Recipe / method | TP | FN | FP | TN | Recall | Normal FPR | Run |
|---|---:|---:|---:|---:|---:|---:|---|
| KSDD2 / PaDiM | 84 | 26 | 77 | 817 | 76.36% | 8.61% | frozen-20261019T041652Z-9c825801 |
| Cable gland RGB / PaDiM | 11 | 76 | 1 | 20 | 12.64% | 4.76% | frozen-20261019T041652Z-9c825801 |

Original decision: no-go. Observed-score threshold envelopes do not change it.

## Planned attempts

| ID | Hypothesis / parent | Current status | Measured outcome | Next evidence needed |
|---|---|---|---|---|
| P0 | Reproduce baseline with exact local identities | Completed | 60/82 defects; 28/417 normal alarms | Calibration score parity passed; 73.17% recall / 6.71% FPR on the common development set |
| R01 | Real-mask supervised segmentation plus image classifier / P0 | Completed; retained parent | 77/82 defects; 27/417 normal alarms | 93.90% recall / 6.47% FPR; stronger round 2 descendant selected |
| R02 | Compact PatchCore / P0 with matched normal IDs | Completed | 66/82 defects; 32/417 normal alarms | 80.49% recall / 7.67% FPR; improves on P0 but below R01 |
| R03 | Representative normals, then larger normal pool / selected parent | Completed | 128: 67/82 defects, 32/417 alarms; 256: 65/82 defects, 42/417 alarms | 128 marginally improves R02; 256 fails the FPR target and worsens recall |
| R04 | Finer latent detail / fixed RGB geometry | Completed; reject tested variant | Raw head: 72/82 defects, 28/417 alarms; localized: 74/82, 43/417 | Neither beats the parent; localized FPR 10.31% fails budget; overlap tiling not tested |
| R05 | Focal loss and hard examples / R01 | Completed; corrected | Best old checkpoint: 80/82 defects, 22/417 alarms | Original seed4219 collapses; corrected objective removes learned-classifier conflict and survives all three tested seeds |
| R06 | Robust image aggregation / supervised maps | Completed; selected with R05 | Parent top 0.1% mean: 79/82 defects, 27/417 alarms | 96.34% / 6.47%; applying the same rule to focal/refined maps improves further |
| R07 | Conservative foreground/pose / selected parent | Deferred with reason | Normal peak diagnostic saved | KSDD2 surface texture has no justified removable background/pose transform; padding already excluded |
| R08 | Permitted illumination variation / R01 | Completed; not selected | Raw: 77/82 defects, 30/417 alarms; localized: 78/82, 26/417 | Lighting and combined training do not beat selected recipe; fixed-cutoff stress reveals bright/blur false-alarm failures |
| R09 | Channel dimension / P0 | Completed; reject | 58/82 defects, 38/417 alarms | 70.73% / 9.11%; lower recall and more false alarms than original 100 channels |
| R10 | Complementary calibrated pair / selected head + PatchCore | Completed; not selected | Initial weighted: 77/82, 21/417; refined weighted: 79/82, 22/417 | Useful initial FPR reduction, but fusion loses one catch versus refined single head with same FP count |
| R05/R06 correction | Train the exact positive-oriented localized inference score | Completed; use for future retraining | Canonical 79/82, 32/417; repeats each 78/82, with 29 and 30/417 alarms | All three meet 95%+ / under-10%; extra continuation of old best: 80/82, 24/417 |

## Required record for every actual attempt

Append an entry rather than overwriting an earlier run. Use status `completed`, `failed`, `resource_stopped`, `inconclusive` or `deferred_with_reason`. Never populate unmeasured fields with zero. Distinguish a 30-minute pilot from a completed full training configuration.

```text
Attempt ID / UTC timestamps / method ID:
Status and reason:
Recipe and intended claim (development / observed benchmark / new confirmation):
Code commit, dirty-file hashes, environment lock and numerical versions:
Source identity, manifest hash, original/group/parent IDs and prior exposure:
Parent baseline and exactly one changed factor:
Fitting IDs, inner/outer fold IDs, seed and label access rules:
Backbone provider/revision/hash, model artifact/hash and feature/cache geometry:
Hyperparameters, actual fit duration and stopping rule:
Image score and threshold source/rule (selection versus final calibration):
TP/FN/FP/TN; rejected defects/normals; recall/FPR/precision/coverage:
AP/AUROC; small-defect/per-folder slices; fixed stress results:
Recall difference at the same FPR budget and paired uncertainty:
Cold start / warm p95 / peak process-tree RSS / artifact and cache bytes:
Score, label-join, raw-map, diagnostic gallery and resource-log paths/hashes:
Software checks actually run and outcome:
What improved, what worsened, likely cause versus untested hypothesis:
Retain / reject / next bounded test and decision rationale:
```

## Final candidate decision record

Preserve round 2's 80/82, 22/417 checkpoint as the best numerical result, together with the failed repeat. Use the aligned objective for future retraining: all three fixed runs meet the development point target, including seed4219 which previously caught only 3/82. The one corrected continuation preserves 80 catches with 24 false alarms; it does not beat the earlier 22-alarm checkpoint. Original-image parity is exact on all checked images and all saved results pass split/threshold/metric audits. More training and hard examples changed together in refinement, so their net gain is not attributable exclusively to mining. Freeze candidates for new independent confirmation; no factory acceptance is established and the original Stage 5 no-go remains unchanged historical evidence.
