# Recall experiment ledger

Created 19 October 2026; updated 20 October 2026. **Latest result: corrected-model validation failed the 95% recall target.** The frozen primary scored **100/110 defects (90.91%) and 69/894 normal false alarms (7.72%)** on the already observed official benchmark. All three corrected cold-start seeds also failed recall (90.00%–91.82%). Exact replay and independent recount passed; no new independent factory batch is available. See [validation results](2026-10-20-validation-results.md).

Baseline, bounded R01–R10 review and alignment correction are complete. Earlier development results were: best numerical checkpoint **97.56% / 5.28%** (unstable original retraining); three corrected fixed seeds **95.12%–96.34% / 6.95%–7.67%**; one corrected continuation **97.56% / 5.76%**. Those development targets did not generalize to the official test. R07 is deferred with a task-specific reason. See [round 1](2026-10-19-round1-results.md), [round 2](2026-10-20-round2-results.md) and [alignment correction](2026-10-20-alignment-results.md).

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
| V01 | Frozen corrected primary plus three fixed seeds / already observed official test benchmark | Completed; target failed | Primary 100/110 defects, 69/894 alarms; seeds 99–101/110, 53–62/894 | 90.91% / 7.72% primary; all seeds below 95%; fresh independent data still required |

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

Preserve all earlier development checkpoints and the failed repeat. The aligned objective removed the demonstrated training/scoring conflict, but **the frozen corrected primary and all three cold-start seeds failed the 95% recall target on the official test benchmark**. Their 90.00%–91.82% test recall supersedes any implication that the earlier development success validated the goal. Original-image replay is exact and metric/split audits pass; those checks do not establish generalization. More training and hard examples changed together in refinement, so their net gain is not attributable exclusively to mining. Improve using training and separated development data, then obtain a genuinely new sealed batch; do not tune the now-observed official test until it passes. No factory acceptance is established and the original Stage 5 no-go remains unchanged historical evidence.

## V01 completed attempt

Frozen source commit `495ddbb`; protocol `0d4b112f51488773ef28b670de7ae6774e4c9b0821e4d327e70203f4b9a32d3e`. Primary head `ffca032083bd4c7a003c198b70b7dc5eb10c4d7dee40392fd7a81c9160f560d9`, existing strict threshold -1.684261679649353, no fitting or calibration changes. Status **completed; failed recall point and confidence targets**. All 1,004 test images scored twice in separate processes, with reverse order on replay: every score and decision equal. All 3,335 usable originals reaudited; no train/test duplicate or fitting/calibration leakage found; physical independence unknown. Primary exact 95% intervals: recall 83.92%–95.55%, FPR 6.05%–9.67%. Training/development/test recall was 100% / 97.56% / 90.91%, consistent with an optimism/generalization gap; its unique cause is unproven. The at-most-0.5%-area defect slice caught only 13/17; this is exploratory, not a tuning decision. First-pass p95 for all four heads was 0.2651 s; peak owned-process-tree RSS 0.540 GiB. All four phases completed within caps, all 126 historical archive files unchanged, 120 software tests passed. Exact package versions, lock hash, timing, source and model hashes, prediction rows, defect slices, and independent verification: [full results](2026-10-20-validation-results.md) and [export index](validation/export-index.json). No separately new labeled data is available; independent confirmation is incomplete.
