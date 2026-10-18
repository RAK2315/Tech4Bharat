# Disposable inspection validation experiment

- Status: actual inference completed; frozen configuration fails the provisional detection screen. Not a full app, factory twin, production inspector, or buyer certification system.
- Start with `artifacts/EXPERIMENT_REPORT.md`, `PROTOCOL.md`, and `artifacts/failure_gallery.html`.
- Results: reference 15/80 defects flagged, 1/100 false flags; compact PaDiM 45/80 defects flagged, 15/100 false flags. No retakes on original images. Both fail. Full counts, intervals and transformed stress results in `results/summary.json`.
- User exercise: `artifacts/review_exercise.html`. Not completed on user's behalf. Export `review_responses.json` when finished. Do not inspect `review_answer_key.json` first. The answer key is local and accessible; this is not a blinded clinical/industrial study.
- Sample report: `artifacts/sample_batch_report.html`. Benchmark observations real; ledger and human decisions fictional; no actual owner approval.
- Feedback script: `feedback.md`. Nobody has been contacted.

## Run existing environment from workspace root

```powershell
.\experiment\.venv\Scripts\python.exe experiment/test_accounting.py
.\experiment\.venv\Scripts\python.exe -m unittest discover -s experiment -p 'test_*.py' -v
.\experiment\.venv\Scripts\python.exe experiment/serve.py
```

- Review exercise: http://localhost:8765/artifacts/review_exercise.html
- Browser parity: http://localhost:8765/browser/index.html
- Stop local server with Ctrl+C. It binds only to 127.0.0.1. Browser-results POST writes only `results/browser_results.json`; no remote services.
- To grade a completed human exercise, use the actual downloaded response path:

```powershell
.\experiment\.venv\Scripts\python.exe experiment/grade_review.py "C:\path\to\review_responses.json"
```

## Recreate and rerun

- Python 3.12 is required for the pinned Windows CPU wheels. Bundled interpreter used here: `C:\Users\laksh\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`.
- From the workspace root, with a Python installation that has pip, create a separate environment with `python -m venv --without-pip experiment/.venv`. Use that parent interpreter's `python -m pip --python experiment/.venv/Scripts/python.exe install -r experiment/requirements-lock.txt --extra-index-url https://download.pytorch.org/whl/cpu`. The parent pip installs into the selected environment; this bypasses the bundled interpreter's failed ensurepip bootstrap. No global package setup is necessary.
- `requirements-lock.txt` captures installed versions. Browser packages and their integrity hashes are pinned in `browser/package-lock.json`; restore with `npm --prefix experiment/browser ci --ignore-scripts --no-audit --no-fund`.
- Run in this order:

```powershell
.\experiment\.venv\Scripts\python.exe experiment/download.py
.\experiment\.venv\Scripts\python.exe experiment/prepare.py
.\experiment\.venv\Scripts\python.exe experiment/run.py
.\experiment\.venv\Scripts\python.exe experiment/make_artifacts.py
.\experiment\.venv\Scripts\python.exe experiment/summarize.py
.\experiment\.venv\Scripts\python.exe -m unittest discover -s experiment -p 'test_*.py' -v
```

- Download needs public internet access, no API key, login, or paid usage. Files remain local. Downloaded data ~297 MB and official original classifier weights ~46.8 MB, plus extracted images, fitted artifacts and dependencies. Do not assume this is a tiny phone download.
- `download.py` pins mirror revision and hashes files. `prepare.py` saves exact split/duplicate manifest. `run.py` writes calibration thresholds before final test inference; run settings are in the frozen protocol. Repeated reruns are reproducibility checks, not independent validation.
- Browser comparison needs `run.py`'s exported model and ten fixtures. Start server, open parity page, click run. The native-only `export_parity.json` is not browser evidence; browser results are saved separately. Browser quality gate is not implemented; only inference and resize parity were tested.
- First browser attempt failed due to a relative runtime module URL; retained as `results/browser_attempt1.json`. Corrected to absolute local asset URL, then completed. No model/threshold change.
- Prepared human task uses 24 disjoint images: 12 manual, 12 assisted, six dataset-normal and six dataset-defective in each. Manual is first, so order effects and unmatched difficulty remain. Artificial 50% prevalence, precomputed AI hints, no capture time. It cannot establish production time savings.
- No phone, real factory, machine connector, manufacturer, buyer, or expert labeler was tested. Binary mirror masks prevent defect-subtype recall. No physical board IDs, so physical-instance leakage cannot be excluded despite zero exact/conservative near-duplicate matches.
- Scores are not probabilities. Heatmaps are scaled per image for display and are not quantitative defect severity.

## Sources and attribution

- VisA: Zou, Yang; Jeong, Jongheon; Pemula, Latha; Zhang, Dongqing; Dabeer, Onkar. *SPot-the-Difference Self-Supervised Pre-training for Anomaly Detection and Segmentation*, ECCV 2022. https://github.com/amazon-science/spot-diff — data CC BY 4.0, original code Apache 2.0. Images obtained from BrachioLab/visa revision d185c42584b49f1df81fe12bde627559ed88d483, not verified byte-for-byte against original archive. Mirror mask labels are binary. Original defect taxonomy retrieved separately; no new subtype labels invented.
- PaDiM: Defard, Thomas; Setkov, Aleksandr; Loesch, Angelique; Audigier, Romaric. https://arxiv.org/abs/2011.08785 — configured local reimplementation of spatial Gaussian patch model, not authors' exact benchmark recipe.
- Official ResNet18 weights: https://docs.pytorch.org/vision/main/models/generated/torchvision.models.resnet18 ; URL/checksum in `data/download_manifest.json`. Torchvision source has BSD-style licensing; pretrained weights/datasets have separate considerations. No blanket commercial deployment permission claimed.
- ONNX Runtime Web: https://onnxruntime.ai/docs/get-started/with-javascript/web.html ; runtime installed from official npm package.
