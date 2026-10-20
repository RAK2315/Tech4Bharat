# Tech4Bharat component inspection assistant

An experimental image inspection assistant for visible component defects, with
human review and explicit inspection records. This repository contains research,
the execution plan, a historical PCB experiment and the initial component scaffold.
It does not establish production readiness or buyer acceptance.

## Start here

- [Latest KSDD2 recall experiments and results](docs/research/2026-10-19-round1-results.md)
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
reproduced PaDiM and tested supervised learning, compact PatchCore and normal-sample
coverage. Its best candidate reached **93.90% defect recall at 6.47% normal false
alarms**, below the requested 95%+ recall goal. This is a single development split,
not independent factory validation; application development remains pending.
The original metal-nut recipe is deferred. See the latest results above and the
[RGB cable-gland scope](components/docs/CABLE_GLAND_SCOPE.md).

## Repository contents

Source code, tests, configuration, dependency locks, plans and historical JSON
metrics are tracked. Virtual environments, dependency caches, downloaded datasets,
model weights, generated image assets and arrays are excluded. Recreate local
dependencies using the component README; obtain data only after reviewing source
licences and the acquisition plan. Historical report image links require the local
generated assets and will not all resolve in a fresh clone.
