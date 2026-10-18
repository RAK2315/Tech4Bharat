# Tech4Bharat component inspection assistant

An experimental image inspection assistant for visible component defects, with
human review and explicit inspection records. This repository contains research,
the execution plan, a historical PCB experiment and the initial component scaffold.
It does not establish production readiness or buyer acceptance.

## Start here

- [Current execution plan](Tech4Bharat_Codex_Execution_Plan.md)
- [Component setup and commands](components/README.md)
- [Setup status](components/docs/STATUS.md)
- [Component datasets](COMPONENT_DATASETS.md)
- [Reviewed build plan](Tech4Bharat_Anomaly_Detector_Build_Plan_Reviewed.md)
- [Historical experiment report](experiment/artifacts/EXPERIMENT_REPORT.md)
- [Historical experiment instructions](experiment/README.md)

The current component implementation provides environment diagnostics only.
Dataset acquisition, model fitting and application development remain future work.
Follow the current execution plan when earlier documents differ.

## Repository contents

Source code, tests, configuration, dependency locks, plans and historical JSON
metrics are tracked. Virtual environments, dependency caches, downloaded datasets,
model weights, generated image assets and arrays are excluded. Recreate local
dependencies using the component README; obtain data only after reviewing source
licences and the acquisition plan. Historical report image links require the local
generated assets and will not all resolve in a fresh clone.
