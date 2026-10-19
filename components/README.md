# Tech4Bharat component inspector

Local anomaly-detection research implementation for the [Codex execution plan](../Tech4Bharat_Codex_Execution_Plan.md).

## Current scope

- Python 3.12 isolated environment at `.venv-p0`.
- Editable Python package, source auditing, reproducible dataset roles, two detector
  implementations, frozen evaluation commands and automated tests.
- Safe acquisition is implemented. Cable gland (MVTec 3D-AD, RGB only) and KSDD2 are imported; see [current scope](docs/CABLE_GLAND_SCOPE.md) and `docs/DATA_SOURCES.md`.
- The original metal-nut recipe is deferred; archived evidence is retained.
- Baseline and pretrained-feature PaDiM development runs are complete for both recipes.
- Stage 5 calibration, one-time original evaluation and paired stress runs are complete.
  Both methods failed recall on both datasets; application stages 6–10 are stopped by the no-go gate.
- `requirements-p0.lock` records installed CPU backend pins and dependency hashes.
- Existing PCB experiment and prior plans remain unchanged.

Progress and evidence: [implementation ledger](docs/IMPLEMENTATION_PROGRESS.md).
Results and limitations: [stage 5 report](docs/STAGE5_REPORT.md).
Reviewer entry point: [Stage 5 reviewer guide](docs/STAGE5_REVIEW_GUIDE.md).
Fresh-machine setup and source links: [colleague reproduction guide](docs/COLLEAGUE_REPRODUCTION.md).
Frozen commands and one-time run restrictions: [reproduction guide](docs/REPRODUCE.md).

## Local dataset folders

Cable-gland archive: `data/archives/cable_gland.tar.xz`.
Extracted source: `data/raw/mvtec_3d_cable_gland/cable_gland/`.
KSDD2 remains at `data/raw/ksdd2/`. These files are ignored, not shipped in Git.
The build plan documents the exact layout and RGB-only selection rules.

## Use the environment

From this directory in PowerShell, explicit paths avoid changing your shell policy:

```powershell
.\.venv-p0\Scripts\python.exe -m component_inspector.cli doctor --json
.\.venv-p0\Scripts\python.exe -m pytest tests -v
```

Optional activation:

```powershell
.\.venv-p0\Scripts\Activate.ps1
```

Implemented CLI commands: `doctor` and `acquire`. Planned commands such as `fit`,
`calibrate`, `evaluate` and `serve` still fail. Doctor readiness flags describe the
scaffold, not actual acquisition; consult the per-dataset source manifests.

For tested acquisition commands, bounds, archive import and recovery instructions,
see [REPRODUCE.md](docs/REPRODUCE.md). A blocked source exits 3, a failure exits 1,
and a completed acquisition exits 0. No source data is included in Git.

## Recreate the setup environment

Use the same Python 3.12 interpreter and `uv` (do not replace an existing environment):

```powershell
uv venv --python 3.12 .venv-p0
uv pip install --python .venv-p0/Scripts/python.exe -r requirements-setup.lock
uv pip install --python .venv-p0/Scripts/python.exe --no-deps -e .
```

`requirements-setup.lock` is generated from the actual resolved setup/dev packages;
it includes Pillow 12.1.0 for a training-only decode check and does not install
PyTorch or Anomalib. Full image/mask auditing and data splits belong to stage 2.
