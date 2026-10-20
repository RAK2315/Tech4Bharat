# Tech4Bharat component inspection assistant

An experimental image inspection assistant for visible component defects, with
human review and explicit inspection records. This repository contains research,
the execution plan, a historical PCB experiment and the initial component scaffold.
It does not establish production readiness or buyer acceptance.

## Start here

- [Latest KSDD2 recall results and training correction](docs/research/2026-10-20-alignment-results.md)
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
The original Stage 5 benchmark returned no-go. A later KSDD2 development comparison
reproduced PaDiM and tested the ten researched strategies with bounded variants.
The best saved checkpoint reached **97.56% defect recall at 5.28% normal false
alarms**, but its training recipe failed one repeat initialization. Correcting
the training/scoring conflict reached **95.12%–96.34% recall at 6.95%–7.67% false
alarms across all three fixed seeds**. One corrected continuation of the earlier
best checkpoint reached **97.56% / 5.76%**. These meet the requested development
point targets; they are not independent factory validation. Application development
remains pending, and the original archived no-go result is unchanged.
The original metal-nut recipe is deferred. See the latest results above and the
[RGB cable-gland scope](components/docs/CABLE_GLAND_SCOPE.md).

## Repository contents

Source code, tests, configuration, dependency locks, plans and historical JSON
metrics are tracked. Virtual environments, dependency caches, downloaded datasets,
model weights, generated image assets and arrays are excluded. Recreate local
dependencies using the component README; obtain data only after reviewing source
licences and the acquisition plan. Historical report image links require the local
generated assets and will not all resolve in a fresh clone.
