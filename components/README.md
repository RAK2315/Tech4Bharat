# Tech4Bharat component inspector

Initial project setup for the [Codex execution plan](../Tech4Bharat_Codex_Execution_Plan.md).

## Current scope

- Python 3.12 isolated environment at `.venv-p0`.
- Editable Python package, setup diagnostics, draft recipe/protocol configuration,
  test location, and directories for future data/models/results/UI.
- No dataset downloads, model weights, anomaly inference, web application or training yet.
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

The only implemented CLI command at this stage is `doctor`. Planned commands such
as `acquire`, `fit`, `calibrate`, `evaluate` and `serve` must fail rather than imply
that those capabilities already exist.

## Recreate the setup environment

Use the same Python 3.12 interpreter and `uv` (do not replace an existing environment):

```powershell
uv venv --python 3.12 .venv-p0
uv pip install --python .venv-p0/Scripts/python.exe -r requirements-setup.lock
uv pip install --python .venv-p0/Scripts/python.exe --no-deps -e .
```

`requirements-setup.lock` is generated from the actual resolved setup/dev packages;
it does not install PyTorch or Anomalib. Full reproducibility and dataset/version
records will be extended during later tasks.
