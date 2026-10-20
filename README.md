# Tech4Bharat component inspection assistant

An experimental image inspection assistant for visible component defects, with
human review and explicit inspection records. This repository contains research,
the execution plan, a historical PCB experiment and the initial component scaffold.
It does not establish production readiness or buyer acceptance.

## Start here

- [Latest corrected-model validation: 95% recall target failed](docs/research/2026-10-20-validation-results.md)
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

Dataset auditing, model fitting and the original frozen evaluation are implemented.
The latest frozen corrected checkpoint reached **90.91% defect recall and 7.72%
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
and the original archived Stage 5 no-go result is unchanged.
The original metal-nut recipe is deferred. See the latest results above and the
[RGB cable-gland scope](components/docs/CABLE_GLAND_SCOPE.md).

## Repository contents

Source code, tests, configuration, dependency locks, plans and historical JSON
metrics are tracked. Virtual environments, dependency caches, downloaded datasets,
model weights, generated image assets and arrays are excluded. Recreate local
dependencies using the component README; obtain data only after reviewing source
licences and the acquisition plan. Historical report image links require the local
generated assets and will not all resolve in a fresh clone.
