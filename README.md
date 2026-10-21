# Tech4Bharat component inspection assistant

An experimental image inspection assistant for visible component defects, with
human review and explicit inspection records. This repository contains research,
the execution plan, a historical PCB experiment and the initial component scaffold.
It does not establish production readiness or buyer acceptance.

## Start here

- [Latest verified warm-recipe results: consistency target failed](docs/research/2026-10-20-warm-small-results.md)
- [Registered three-seed ensemble: in progress](docs/research/2026-10-21-seed-ensemble-protocol.md)
- [Latest small-defect study: no verified improvement](docs/research/2026-10-20-small-defects-results.md)
- [Earlier corrected-model test validation: 95% recall target failed](docs/research/2026-10-20-validation-results.md)
- [Development recall results and training correction](docs/research/2026-10-20-alignment-results.md)
- [Remaining strategies, comparisons and failed repeat run](docs/research/2026-10-20-round2-results.md)
- [Ten researched improvement strategies](docs/research/2026-10-19-recall-strategies.md)
- [Current execution plan](Tech4Bharat_Codex_Execution_Plan.md)
- [Copy-paste Codex prompts and manual checks](docs/superpowers/plans/2026-10-18-codex-build-playbook.md)
- [Component setup and commands](components/README.md)
- [Setup status](components/docs/STATUS.md)
- [Component datasets](COMPONENT_DATASETS.md)
- [Reviewed build plan](Tech4Bharat_Anomaly_Detector_Build_Plan_Reviewed.md)
- [Historical experiment report](experiment/artifacts/EXPERIMENT_REPORT.md)
- [Historical experiment instructions](experiment/README.md)

The verified warm-recipe sweep selected **24 extra training epochs**. Across
three fixed seeds its pooled recall ranged **92.68%–96.34%**, with **7.01%–8.69%
normal false alarms** and **33–39 of 45 small defects** caught. Its worst fold
had **90.24% recall**. A locked second partition reached **95.12% / 6.59%**
overall but failed recall in one fold. **The across-fold consistency goal failed.**
Size weighting and zoomed crops also failed; all methods and failures are documented.
Every one of 65,076 native replay decisions matched exactly. Verification checked
6,234 feature artifacts, source roles, calibration, mining and metrics.

The separately registered three-seed average is now running with two additional
fresh initialization seeds. Its primary policy and formula were fixed before
the main selection and second-partition predictions. It has no result yet.
The original standby interruption and exact recovery remain documented. The
official test remains closed; these reused training images provide no new
independent factory confirmation.

The preceding seven-method, training-only nested study reached **93.90% recall / 8.63%
normal false alarms**; both fixed seed repeats also reached 93.90% recall.
It did not beat the paired coarse control (94.31% / 7.91%). The full prior recipe
averaged **95.93% / 8.81%**, but failed a recall or false-alarm target in two of
three folds. Small-defect catches were 34/45 for the new procedure and 39/45 for
the full prior recipe. These reused training images do not establish reliable
95% performance. Every original-image replay decision matched; the independent
audit and checkpoint archive are linked in the report.

Dataset auditing, model fitting and the original frozen evaluation are implemented.
The earlier frozen corrected checkpoint reached **90.91% defect recall and 7.72%
normal false alarms** on all 1,004 official KSDD2 test images. **The requested 95%
recall goal failed.** All three corrected cold-start seeds also failed it
(90.00%–91.82% recall). Exact full replay and independent metric recount passed.

The earlier **97.56% / 5.76%** corrected-checkpoint result was measured on repeatedly
observed development data and did not hold on test images excluded from fitting.
The official test set itself was previously observed by the project in Stage 5,
so this is benchmark evidence, not pristine independent factory confirmation.
There is no separate new factory batch available. The ten-strategy study and
training correction remain documented; further model work and a genuinely new
sealed confirmation batch are needed. Application development remains pending,
and the original archived Stage 5 no-go result is unchanged. The official test
set stayed closed throughout the latest small-defect study.
The original metal-nut recipe is deferred. See the latest results above and the
[RGB cable-gland scope](components/docs/CABLE_GLAND_SCOPE.md).

## Repository contents

Source code, tests, configuration, dependency locks, plans and historical JSON
metrics are tracked. Virtual environments, dependency caches, downloaded datasets,
model weights, generated image assets and arrays are excluded. Recreate local
dependencies using the component README; obtain data only after reviewing source
licences and the acquisition plan. Historical report image links require the local
generated assets and will not all resolve in a fresh clone.
