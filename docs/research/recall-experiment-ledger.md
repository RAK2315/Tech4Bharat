# Recall experiment ledger

Created 19 October 2026; updated 20 October 2026. **Baseline and bounded R01–R10 strategy review completed.** Best round 2 single-run result: **97.56% recall / 5.28% normal FPR**, but one repeat collapses to **3.66% / 10.07%**. The recipe is not established as repeatable. A correction aligning training with localized inference is running on all three fixed seeds. R07 is deferred with a task-specific reason. See [round 1](2026-10-19-round1-results.md), [round 2](2026-10-20-round2-results.md) and [alignment correction](2026-10-20-alignment-results.md).

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
| R05 | Focal loss and hard examples / R01 | Completed; correction underway | Focal/localized: 80/82 defects, 29/417 alarms; refined: 80/82, 22/417 | Best reaches 97.56% / 5.28%, but seed4219 collapses; continuation-only control not run |
| R06 | Robust image aggregation / supervised maps | Completed; selected with R05 | Parent top 0.1% mean: 79/82 defects, 27/417 alarms | 96.34% / 6.47%; applying the same rule to focal/refined maps improves further |
| R07 | Conservative foreground/pose / selected parent | Deferred with reason | Normal peak diagnostic saved | KSDD2 surface texture has no justified removable background/pose transform; padding already excluded |
| R08 | Permitted illumination variation / R01 | Completed; not selected | Raw: 77/82 defects, 30/417 alarms; localized: 78/82, 26/417 | Lighting and combined training do not beat selected recipe; fixed-cutoff stress reveals bright/blur false-alarm failures |
| R09 | Channel dimension / P0 | Completed; reject | 58/82 defects, 38/417 alarms | 70.73% / 9.11%; lower recall and more false alarms than original 100 channels |
| R10 | Complementary calibrated pair / selected head + PatchCore | Completed; not selected | Initial weighted: 77/82, 21/417; refined weighted: 79/82, 22/417 | Useful initial FPR reduction, but fusion loses one catch versus refined single head with same FP count |

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

Round 2's frozen focal/localized/refined checkpoint detects 80/82 defects with 22/417 false alarms, but its training recipe fails the fixed seed4219 check. Preserve this real best-single-run result and its failure record; do not recommend the recipe as reliably 95%+. Correct the learned-classifier/localized-score objective conflict and rerun all three fixed seeds without cherry-picking. More training and hard examples changed together in refinement, so their net gain is not attributable exclusively to mining. No independent confirmation cohort has been obtained; the original Stage 5 no-go remains unchanged historical evidence.
