# Tech4Bharat component inspector

Research scaffold and safe source acquisition for the [Codex execution plan](../Tech4Bharat_Codex_Execution_Plan.md).

## Current scope

- Python 3.12 isolated environment at `.venv-p0`.
- Editable Python package, setup diagnostics, draft recipe/protocol configuration,
  test location, and directories for future data/models/results/UI.
- Safe acquisition is implemented; see `docs/DATA_SOURCES.md` for actual download/blocker status.
- No model weights, anomaly inference, web application or training yet.
- `configs/backend-targets.yaml` contains proposed ML versions, not an installed ML lock.
- Existing PCB experiment and prior plans remain unchanged.

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
