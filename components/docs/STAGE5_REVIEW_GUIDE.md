# Stage 5 reviewer guide

## Purpose

This is the entry point for reviewing the Stage 5 component-inspection
experiment. It explains what was implemented, what failed, what the saved
evidence proves, what remains uncertain, and how a future experiment can make a
fair comparison.

Stage 5 is a research benchmark, not a production inspection system. Its frozen
decision is **no-go**: neither method achieved the required defect recall on
either dataset. Application stages 6–10 were therefore stopped.

The immutable historical copy is at:

`historical_benchmark/frozen-20261019T041652Z-9c825801/`

Its `ARCHIVE_MANIFEST.json` records the source run, freeze identity, document
hashes, and preservation policy. The 122 copied run files were verified against
the original run by SHA-256 when archived.

## What was implemented

Two anomaly-detection methods were fitted separately for two dataset recipes,
producing four detector/dataset combinations:

1. **Reference baseline** — selects up to 16 normal reference images. A new
   image is compared with its closest reference, and the strongest 1% of the
   smoothed RGB residual map determines the image score.
2. **PaDiM** — uses frozen pretrained ResNet-18 features from layers 1–3. It
   retains 100 feature channels and fits a Gaussian model of normal features at
   each spatial location using at most 128 normal fit samples. The maximum raw
   anomaly-map value inside the valid image region is the image score.

The dataset recipes were:

- **MVTec 3D-AD cable gland, RGB only** — resized with aspect-preserving
  letterboxing to 256 x 256. XYZ/depth and camera-calibration data were excluded.
- **KSDD2 surface inspection** — rotated according to the frozen recipe and
  letterboxed to 256 x 640.

The common data flow was:

`acquire -> adapt -> audit -> split -> fit -> freeze -> calibrate -> evaluate -> stress`

Normal groups were deterministically divided into fit, development and
calibration roles. Official test membership was preserved. Duplicate groups
could not cross protected roles. Model, source, configuration, dependency and
manifest identities were frozen before calibration and final evaluation.

## How the models were evaluated

Each method and dataset had its own threshold. Thresholds were calculated from
normal calibration images only using a finite-sample upper-rank rule. An image
was flagged only when its score was **strictly greater** than the threshold.
Scores are raw anomaly values, not probabilities or percentages.

The final test phase was reserved and executed once. Technical failures counted
against coverage and defective images that could not be scored would count as
misses. In the recorded run, all expected images were scored and there were no
technical rejections.

The provisional acceptance screens were:

- Defect recall at least 90%.
- Accepted-normal false-positive rate at most 10%.
- Technical coverage at least 90%.
- Warm p95 inference time at most 5 seconds.
- Owned-process-tree peak memory at most 4 GiB.

After the original evaluation, the frozen thresholds were retained for paired
brightness and blur stress tests. These transformed copies are diagnostics, not
independent validation samples.

## Original Stage 5 results

| Dataset / method | TP | FN | FP | TN | Recall | Normal FPR | Coverage | Warm p95 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Cable gland / reference | 3 | 84 | 1 | 20 | 3.45% | 4.76% | 100% | 0.0580 s |
| Cable gland / PaDiM | 11 | 76 | 1 | 20 | 12.64% | 4.76% | 100% | 0.1683 s |
| KSDD2 / reference | 74 | 36 | 75 | 819 | 67.27% | 8.39% | 100% | 0.1482 s |
| KSDD2 / PaDiM | 84 | 26 | 77 | 817 | 76.36% | 8.61% | 100% | 0.3617 s |

PaDiM performed better than the reference baseline on both datasets, but all
four combinations failed the 90% recall requirement. Speed, memory, coverage and
normal-FPR screens passed in the original evaluation. Passing those engineering
screens does not compensate for missed defects.

Cable-gland PaDiM recall by verified defect folder was:

| Defect folder | Detected / total | Recall |
|---|---:|---:|
| bent | 3 / 21 | 14.29% |
| cut | 3 / 22 | 13.64% |
| hole | 5 / 22 | 22.73% |
| thread | 0 / 22 | 0% |

KSDD2 has no verified defect-type folders in the retained metadata, so no KSDD2
subtypes were invented.

## Heatmaps versus whole-image decisions

PaDiM's macro per-defective-image pixel AUROC was approximately 0.974 for cable
gland and 0.976 for KSDD2. This means that, within defective images, annotated
defect pixels generally ranked above non-defect pixels. It does **not** mean that
97% of defects were located correctly, nor that 97% of images were classified
correctly.

The whole-image decision used a different operation: the maximum valid heatmap
value became one image score, which was compared with the normal-calibrated
threshold. For cable-gland PaDiM:

- Frozen threshold: 51.8922.
- Median normal test score: 25.1305.
- Median defective test score: 30.5028.
- Defective-score 10th to 90th percentile: approximately 23.2376 to 53.5773.
- Image-ranking AUROC: approximately 0.731.

Most defective images therefore remained below the frozen threshold even when
their defect pixels were relatively prominent within the heatmap. Normal and
defective image scores also overlapped. Lowering the threshold after observing
the test results would increase recall but can also increase normal false alarms;
it would be test-driven tuning, not a fair correction.

## Confirmed findings

The saved evidence establishes the following:

- All four method/dataset combinations failed the required recall screen.
- PaDiM outperformed the reference baseline on recall for both datasets.
- Cable-gland PaDiM missed 76 of 87 defects and every `thread` example.
- KSDD2 PaDiM ranked images well (AUROC approximately 0.932) but still missed 26
  of 110 defects at the frozen operating threshold.
- High pixel AUROC did not translate into acceptable image-level recall.
- Cable-gland normal and defective PaDiM image-score distributions overlap.
- The reference method is highly brightness-sensitive on KSDD2: under brightness
  x0.6 it flagged all 894 normal images, and under brightness x1.4 it flagged
  893 of 894.
- KSDD2 PaDiM stayed below 90% recall under all three stress transformations;
  blur increased its normal FPR to 14.09%.
- No threshold or model was tuned using the original Stage 5 test outcomes.
- Physical-product independence is unknown. Appearance-group bootstrap intervals
  do not prove that images came from independent physical components.

## Hypotheses that are not yet proven

The following are reasonable development hypotheses, not established causes:

- Resizing cable-gland images to 256 x 256 may weaken small defects.
- Normal pose, component edges or threaded regions may create stronger responses
  than some real defects.
- Using one maximum heatmap value as the image score may make the decision overly
  sensitive to isolated normal responses.
- ImageNet ResNet-18 features may not represent subtle surface and geometric
  defects sufficiently well.
- The 128-normal-sample fit cap or 100 retained PaDiM channels may underrepresent
  normal appearance.
- One threshold may be insufficient if the dataset contains distinct normal pose
  or appearance groups.
- Cable-gland XYZ/depth information may help geometric defects, but it was not
  evaluated and would define a new multimodal method.

These hypotheses must be tested on development data. The historical test set
must not be repeatedly queried until a preferred design appears to pass.

## Evidence that was not preserved

- Full raw anomaly maps for every test image were not archived.
- Pixel average precision was not collected.
- A pooled dataset-level pixel AUROC was not collected. The recorded pixel metric
  is a macro average over defective images.
- Precise overlap measures such as IoU were not collected.
- Physical component identifiers were unavailable.
- Human inspection time and decisions were not measured.
- Cable-gland provider-release identity and provider checksum authentication were
  not established. The exact local archive hash and recovered origin are recorded.

Do not rerun the historical holdout merely to fill these missing secondary
metrics. Collect them prospectively in a newly frozen experiment.

## Recommended next experiment

### 1. Development-only diagnosis

Create or designate a labelled defect-development set that is separate from both
normal calibration and the observed Stage 5 test set. On development data:

- Plot recall and normal FPR across every possible image threshold.
- Determine whether any threshold can reach recall >= 90% and normal FPR <= 10%.
- Compare image scores based on maximum pixel, top-k mean, high-percentile mean,
  and the largest connected suspicious region.
- Analyse misses by verified defect type, mask area, location, contrast and pose.
- Analyse false positives by location, component edge, thread region, reflection,
  brightness and pose.

If no threshold reaches both targets, lowering the threshold cannot solve the
problem; feature extraction, resolution or score construction must change.

### 2. Resolution study

Compare the historical 256 x 256 cable-gland input with 384 x 384, 512 x 512,
and overlapping native-resolution tiles. Record recall by defect-mask size plus
latency and peak memory. Change no other variable in this experiment.

### 3. Bounded model comparison

Retain the reference method as a cheap sanity-check baseline, but do not invest
substantial development effort in it. Compare:

- Frozen historical reference baseline.
- Frozen historical PaDiM.
- Revised PaDiM scoring/resolution candidate.
- PatchCore as the first stronger normal-only candidate.

EfficientAD or Reverse Distillation can follow only if the bounded comparison
justifies another model. Avoid changing model, resolution, scoring and threshold
policy simultaneously.

### 4. Freeze and independent confirmation

Pre-register the candidate-selection rule and provisional screens. Freeze the
selected code, model, configuration, data memberships and threshold before using
a new untouched confirmation set. Track physical component identity if possible.
Run the confirmation evaluation once and compare it with this archived Stage 5
benchmark.

The Stage 5 test set is now observed. It remains useful as historical evidence,
but a new score on the same images is not independent confirmation.

## Reviewer file map

Start with these files, in order:

1. `docs/STAGE5_REPORT.md` — concise result table, thresholds, gate and limits.
2. `docs/STAGE5_FAILURE_ANALYSIS.md` — saved examples, stress observations and
   cautious interpretation.
3. `historical_benchmark/frozen-20261019T041652Z-9c825801/REPORT.md` — complete
   immutable-run report.
4. `historical_benchmark/frozen-20261019T041652Z-9c825801/gallery.html` — selected
   TP, FN, FP and TN examples.
5. `historical_benchmark/frozen-20261019T041652Z-9c825801/SUPPLEMENT.json` —
   per-folder recall, bootstrap intervals and gallery hashes.
6. `historical_benchmark/frozen-20261019T041652Z-9c825801/freeze.json` — exact
   dataset, model, protocol, dependency and file identities.
7. `historical_benchmark/frozen-20261019T041652Z-9c825801/calibration/` — saved
   normal calibration rows and thresholds.
8. `historical_benchmark/frozen-20261019T041652Z-9c825801/evaluation/` — every
   original saved image score, flag and aggregate metric.
9. `historical_benchmark/frozen-20261019T041652Z-9c825801/stress/` — paired
   brightness and blur predictions.
10. `src/component_inspector/vision/padim_adapter.py` and
    `src/component_inspector/vision/reference.py` — model and image-score logic.
11. `src/component_inspector/evaluation/calibration.py`, `metrics.py`,
    `phase_worker.py`, `freeze.py` and `runner.py` — thresholding, metrics,
    protected evaluation and gate logic.
12. `configs/protocol.yaml`, `configs/mvtec_3d_cable_gland_rgb.yaml` and
    `configs/ksdd2_surface.yaml` — experiment policy and preprocessing.
13. `tests/` — executable checks for acquisition, splitting, leakage controls,
    models, calibration, metrics, frozen phases, resources and reporting.

## Known documentation issue

In `SUPPLEMENT.json`, the `defect_folder_note` under the two cable-gland method
entries incorrectly repeats the KSDD2 sentence. The cable-gland numerical folder
results are present and the metric values are unaffected. Treat the note as a
reporting metadata defect; do not rewrite the immutable historical file. This
guide supplies the corrected interpretation.
