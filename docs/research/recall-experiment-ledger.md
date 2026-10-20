# Recall experiment ledger

Created 19 October 2026; updated 20 October 2026. **Baseline reproduction and R01–R03 completed.** Best development result: **93.90% recall / 6.47% normal FPR**, below the requested 95%+ recall goal. R04–R10 remain outside this round. See the [completed round 1 report](2026-10-19-round1-results.md).

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
| R01 | Real-mask supervised segmentation plus image classifier / P0 | Completed; retain | 77/82 defects; 27/417 normal alarms | 93.90% recall / 6.47% FPR; interrupted first attempt preserved, streamed second attempt completed |
| R02 | Compact PatchCore / P0 with matched normal IDs | Completed | 66/82 defects; 32/417 normal alarms | 80.49% recall / 7.67% FPR; improves on P0 but below R01 |
| R03 | Representative normals, then larger normal pool / selected parent | Completed | 128: 67/82 defects, 32/417 alarms; 256: 65/82 defects, 42/417 alarms | 128 marginally improves R02; 256 fails the FPR target and worsens recall |
| R04 | Native detail and overlap tiles / fixed geometry parent | Awaiting go | Not run | Detail-loss diagnostics, edge/coordinate checks and tile memory/time |
| R05 | Balanced loss/sampling and hard examples / R01 | Awaiting go | Not run | Parent training pipeline and clean inner/outer groups |
| R06 | Robust image aggregation / P0 maps | Awaiting go | Not run | New raw development maps and tiny-defect comparisons |
| R07 | Conservative foreground/pose / selected parent | Awaiting go | Not run | Peaks outside foreground or pose-linked normal extremes |
| R08 | Permitted illumination variation / selected parent | Awaiting go | Not run | Training policy and original/stress paired metrics |
| R09 | Stable covariance and channel dimension / P0 | Awaiting go | Not run | Conditioning diagnostics and fixed nested channel IDs |
| R10 | Complementary calibrated pair / two selected parents | Awaiting go | Not run | Cross-fitted miss overlap, fused FPR and total resources |

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

Retain R01 as the best development candidate. Reject the expanded 256-normal PatchCore variant; treat the diversity-selected 128 variant as a marginal alternative, not a confirmed win. No candidate achieved the requested 95%+ recall with under-10% FPR. Before any final confirmation, freeze the chosen pipeline and document calibration/exposure identities. No independent confirmation cohort was obtained in this round.
