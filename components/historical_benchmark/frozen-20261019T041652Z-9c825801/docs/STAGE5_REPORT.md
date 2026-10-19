# Stage 5 results — 19 October 2026

Calibration, one-time original evaluation, paired stress runs and reporting are
finished. **Decision: no-go. Neither method qualifies on either dataset.**
Stages 6–10 are stopped under the build plan's gate; no reliable-inspector app or
factory-readiness claim is supported by this experiment.

| Dataset / method | TP | FN | FP | TN | Recall | Normal FPR | Coverage | Warm p95 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Cable gland / reference | 3 | 84 | 1 | 20 | 3.45% | 4.76% | 100% | 0.0580 s |
| Cable gland / PaDiM | 11 | 76 | 1 | 20 | 12.64% | 4.76% | 100% | 0.1683 s |
| KSDD2 / reference | 74 | 36 | 75 | 819 | 67.27% | 8.39% | 100% | 0.1482 s |
| KSDD2 / PaDiM | 84 | 26 | 77 | 817 | 76.36% | 8.61% | 100% | 0.3617 s |

Required recall was at least 90%. All four methods passed the other provisional
screens: accepted-normal FPR at most 10%, scoring coverage at least 90%, warm p95
at most 5 seconds and owned-process-tree peak RSS at most 4 GiB. Technical rejects
were zero. Quality warnings did not exclude images. Point estimates are
provisional screens, not guarantees; Wilson intervals are retained in result JSON.

## Calibration and frozen identity

Freeze: `49cecd4d593536eecfba7974f61968570581b44885606ab97d424ba5d86cff40`.
Both methods, both recipes, data roles, model states, numerical runtime and
dependency versions were frozen before calibration or final prediction.

| Dataset | Normal calibration images | Rank k | Reference threshold | PaDiM threshold |
|---|---:|---:|---:|---:|
| Cable gland | 44 | 41 | 0.30545759201049805 | 51.89221954345703 |
| KSDD2 | 417 | 377 | 0.017160728573799133 | 47.66035842895508 |

Only scores strictly greater than the relevant threshold are flagged. Display
scales also came from normal calibration images. Scores are not probabilities and
are not pooled across recipes or methods. No thresholds or models were tuned
against these final results. Source and earlier-stage identities were reverified.

## Stress and failure analysis

All 12 paired method/dataset/transform combinations completed: brightness ×0.6,
brightness ×1.4 and Gaussian blur radius 2. Original thresholds remained unchanged.
These are transformed copies of existing test items, not independent validation.

KSDD2 reference brightness ×0.6 flags all 894 normal items. PaDiM KSDD2 recall
remains below 90% for all three stress conditions; blur raises its normal FPR to
14.09%. See the [failure analysis](STAGE5_FAILURE_ANALYSIS.md) for examples,
interpretation and a bounded future experiment. Do not rerun this holdout until
it passes. Future design decisions must treat this holdout as already observed.

## Evidence and limits

- [Full immutable-run report](../runs/frozen-20261019T041652Z-9c825801/REPORT.md)
- [Failure gallery](../runs/frozen-20261019T041652Z-9c825801/gallery.html)
- [Defect-folder recall, bootstrap intervals and gallery hashes](../runs/frozen-20261019T041652Z-9c825801/SUPPLEMENT.json)
- [Implementation and verification ledger](IMPLEMENTATION_PROGRESS.md)
- [Reproduction commands and one-time run rules](REPRODUCE.md)

Software suite: **99 passed, 45 upstream deprecation warnings**, 60.16 seconds.
Software tests passing does not mean the detectors passed the recall target.
Metric/role tests include fictional hand-computable cases, calibration boundaries,
changed-file rejection and prevention of worker repeats through alternate folders.

Report review was performed by the implementing agent; no independent reviewer was
used. Pixel AP was not collected and full raw test maps were not archived. These
secondary outputs remain unavailable; original inference was not repeated to
recover them. Macro per-anomalous-image pixel AUROC is available and is explicitly
different from pooled dataset pixel AUROC. Physical-product independence is unknown;
appearance-group bootstrap intervals cannot establish it. Human inspection time
has not been measured.

Cable-gland download origin and exact local archive are recorded, with the supplied
early-review notice retained. Current provider-release/checksum authentication is
not established. This is local noncommercial RGB research on identified bytes.
