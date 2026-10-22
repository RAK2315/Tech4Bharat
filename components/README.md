# Tech4Bharat component inspector

Local anomaly-detection research implementation for the [Codex execution plan](../Tech4Bharat_Codex_Execution_Plan.md).

Latest verified work: [warm-recipe small-defect results](../docs/research/2026-10-20-warm-small-results.md).
The selected extra-24-epoch control varied from **92.68% to 96.34% recall** across
three fixed seeds, with **7.01%–8.69% normal FPR** and 33–39/45 small defects caught.
Its worst fold reached 90.24% recall. The locked second partition pooled 95.12%
recall / 6.59% FPR but failed one fold. **Consistency failed.** All 65,076 native
replay decisions matched exactly; independent metric/data checks passed.

The [completed three-seed ensemble](../docs/research/2026-10-21-seed-ensemble-results.md)
passed three of six primary-alpha-.05 cases. Its predeclared diagnostic alpha .08
passed all six, with 95.12%–97.56% recall and 6.12%–8.63% normal false alarms.
This promising diagnostic does not rescue the failed primary qualification.
Small catches were 40/45 and 37/45 per partition, below 95%. All 7,656 ensemble
replay decisions matched; final software checks passed 148 tests. The
[fitting-gap diagnostic](../docs/research/2026-10-21-fitting-gap-results.md)
found 100% fitting recall in every head and lower held-out recall.
See the [plain-English decision](../docs/research/2026-10-22-recall-status.md).
The original
[standby recovery](../docs/research/2026-10-21-warm-small-recovery.md) remains recorded.
The official test remains closed. These observed training images provide no new
factory confirmation or production guarantee.

Previous completed research: [small-defect and overfitting study](../docs/research/2026-10-20-small-defects-results.md).
Seven fixed methods were evaluated using training-only nested cross-validation.
The new procedure reached **93.90% recall / 8.63% normal FPR**; both fixed seed
repeats also reached 93.90% recall. It did not improve on the paired coarse
control. The full prior recipe averaged **95.93% / 8.81%**, but failed a target
in two of three folds. Small-defect catches were 34/45 versus 39/45 for that
reference. These are internal results on previously observed training images.
All 11,484 native replay evaluations matched exactly; the report links the
independent audit, every experiment, and the local checkpoint archive.

Earlier [corrected-model test validation](../docs/research/2026-10-20-validation-results.md):
The frozen corrected primary reached **90.91% recall / 7.72% normal FPR** on all
1,004 official KSDD2 test images: **95% recall failed**. The earlier development
success did not generalize; all three corrected cold-start seeds also fell below
95%. Full replay was exact and independent recount passed. The official test was
previously observed by the project, so fresh factory confirmation remains needed.
See the [training correction](../docs/research/2026-10-20-alignment-results.md)
and the unchanged historical Stage 5 no-go.

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
Fresh-machine setup and source links: [reproduction guide](docs/REPRODUCTION.md).
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
