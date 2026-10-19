# Stage 5 failure analysis — 19 October 2026

Frozen run: `runs/frozen-20261019T041652Z-9c825801`.
Original evaluation decision: **no-go**. All paired stress runs are complete;
their results are reported separately, without changing this original decision.

| Dataset / method | Defects detected / total | Recall | Normal false alarms / total | Normal FPR |
|---|---:|---:|---:|---:|
| Cable gland / reference | 3 / 87 | 3.45% | 1 / 21 | 4.76% |
| Cable gland / PaDiM | 11 / 87 | 12.64% | 1 / 21 | 4.76% |
| KSDD2 / reference | 74 / 110 | 67.27% | 75 / 894 | 8.39% |
| KSDD2 / PaDiM | 84 / 110 | 76.36% | 77 / 894 | 8.61% |

All four runs scored 100% of expected test images without technical rejections.
Speed, memory and normal-FPR screens passed; all four missed the 90% recall screen.
Fast predictions and low normal false-alarm rates do not establish adequate defect
detection. Application stages 6–10 are stopped under the plan's no-go gate.

The image-ranking AUROC is 0.731 for cable-gland PaDiM and 0.932 for KSDD2
PaDiM. Macro per-defective-image pixel AUROC is 0.974 and 0.976, respectively.
These diagnostics do not override the poor recall at the frozen image threshold.
A heatmap can rank defect pixels relatively highly while an image still falls
below its operational detection threshold. Cable-gland test prevalence is 87/108;
its high image average precision must be interpreted alongside that prevalence,
not advertised as a 91.8% detection rate.

## What the saved examples show

The first cable-gland PaDiM false negative has a small annotated defect near the
bottom of the component. The false-positive example shows strong responses around
the component's upper/threaded regions. Its normal ground-truth label is retained.
The gallery overlay is fixed-scale intensity, not a segmentation or probability.

The first KSDD2 PaDiM false negative contains a visible diagonal scratch that is
also present in its ground-truth mask. The first false-positive original contains
surface texture and bright points, but the provider labels it normal. These are
examples, not a verified causal explanation or a complete survey of every error.

Possible development hypotheses include sensitivity to object pose, broad normal
appearance variation, and loss of small-defect detail after resizing. These have
not been established by this test. Neither lowering thresholds after seeing these
examples nor repeating this holdout until it passes is an acceptable correction.

## Bounded next experiment

Keep these artifacts unchanged. If a new experiment is authorized, diagnose pose
and resolution effects using development images first, select a revised protocol
before confirmation testing, and obtain an untouched confirmation set with better
physical-product identity tracking. Treat the present holdout as already observed
for future design decisions. Do not claim new independent validation by rescoring
these same images.

## Completed stress observations

KSDD2's reference method flags every normal image under brightness ×0.6
(894/894), and 893/894 normal images under brightness ×1.4. Its 100% defect recall
under those brightness changes is therefore not successful inspection: almost
everything is flagged. Blur reduces its defect recall to 44/110 (40%).

Cable-gland reference brightness ×1.4 increases defect recall to 52/87, but also
falsely flags 16/21 normal items. The PaDiM cable-gland stress runs retain low
recall (10/87 for blur/darker images; 13/87 for brighter images). These fixed-cutoff
paired results strengthen the sensitivity warning; they do not replace original
test metrics or justify a threshold change. KSDD2 PaDiM also remains below 90%
recall under all three transforms: darker images 77/110 (70%), brighter images
88/110 (80%), and blur 90/110 (81.82%). Blur increases normal false alarms to
126/894 (14.09%), beyond the provisional 10% normal-FPR target.

## Reporting limits

The supplied cable-gland archive has an early-review notice. Exact downloaded bytes
and recovered download origin are recorded; current provider-release identity and
provider checksum authentication are not established. Results describe local
noncommercial RGB research on those bytes.

Image-level metrics, Wilson intervals, recorded resource measurements and macro
per-anomalous-image pixel AUROC are available. Pixel AP was not collected, and full
raw test maps were not archived. Report these secondary outputs as unavailable;
do not rescore the holdout to fill the gap. Appearance-group bootstrap intervals
cannot prove physical-product independence. Human review time remains unmeasured.
