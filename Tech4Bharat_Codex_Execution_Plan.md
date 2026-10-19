# Tech4Bharat Anomaly Detector — Codex Execution Plan

> **For agentic workers:** use the installed `executing-plans` skill and execute tasks in order. Use `subagent-driven-development` only if the human explicitly selects delegation. Follow repository instructions, preserve prior evidence, and mark checkboxes only after verification. **Creating this document is planning, not authorisation to implement it.**

**Date/status:** 18 October 2026 · Updated for RGB-only MVTec 3D-AD cable gland + KSDD2. Safe acquisition is implemented; both archives are imported. Data audit, model fitting and application remain pending. See [scope amendment](components/docs/CABLE_GLAND_SCOPE.md).

**Goal:** build a narrow, human-reviewed component anomaly detector only after a reproducible native experiment supports its limited usefulness.

**Architecture:** explicit dataset adapters and immutable splits → separate reference/PaDiM fits per product recipe → development checks → frozen calibration/test evaluation → local inference/review → batch history/report → honestly labelled deployment mode.

**Tech stack:** Python 3.12, PyTorch CPU, Anomalib PaDiM, NumPy/Pillow/OpenCV/scikit-learn, FastAPI/Pydantic, SQLite, React/TypeScript/Vite. No paid APIs, GPU dependency, LLM classifier or 3D engine.

**Spec:** [reviewed plan and evidence ledger](Tech4Bharat_Anomaly_Detector_Build_Plan_Reviewed.md). Use this file as the ordered execution guide; the reviewed plan explains evidence and trade-offs. [Original plan](Tech4Bharat_Anomaly_Detector_Build_Plan.md), [dataset catalogue](DATASET_CATALOGUE.md), [components shortlist](COMPONENT_DATASETS.md) and [PCB experiment](experiment/artifacts/EXPERIMENT_REPORT.md) remain historical/reference material. Do not resume the earlier PCB-first or rotation-bank designs by accident.

> The user-selected cable-gland amendment in components/docs/CABLE_GLAND_SCOPE.md supersedes historical metal-nut scope in the reviewed/background plans. Those earlier experiments and measurements are not cable-gland evidence.

## 1. Fixed decisions: what we are actually building

| Decision | Instruction for Codex |
|---|---|
| Product first | MVTec 3D-AD **`cable_gland`**, RGB-only mechanical-component inspection |
| Second dataset | **KolektorSDD2 / KSDD2**, separate component-surface benchmark, not a second cable-gland line |
| Baseline B0 | Nearest RGB residual from **16 normal reference images**, no rotation search |
| Main candidate P0 | **PaDiM**, frozen **ResNet18**, layers `layer1`, `layer2`, `layer3`, **100 retained features**, via a thin Anomalib adapter |
| PaDiM fitting data | At most **128 normal fit groups per recipe**; no defective images in normal statistics |
| Training style | Fit reference/Gaussian normal models; do not train a neural network from scratch |
| Primary model | P0 selected before final tests if it passes development/resource checks; B0 remains the fixed comparator |
| Fallback P1 | Existing native **ResNet18 + compact 50-channel PaDiM** concept, extracted into new modules; one bounded fallback before calibration/test, not a new architecture search |
| Mixing datasets | **No joint training**, pooled normal statistics, common score threshold or automatic product recognition |
| Inference first | Native **CPU**, one request at a time, batch size 1 |
| Output | Image anomaly flag plus optional continuous attention map; human final decision |
| UI | React/TypeScript, upload/review/batch/report only |
| Storage | Local SQLite plus local image/artifact files |
| First deployment | Working local live inference; static deployed replay if free live hosting is not verified |
| Excluded | Factory simulation/twin, automatic causes, machine integration, all-component detector, phone inference, YOLO subtype detection and automatic batch acceptance |

These are routine implementation selections for this plan. Model accuracy, capture usefulness and cloud deployment feasibility are still **experiments**, not settled capabilities. Do not interpret “exact plan” as a guarantee of success.

## Global constraints

- One Codex-assisted builder; no extra teammate capacity assumed. Frontend TypeScript preferred.
- Free dependencies/public sources/local compute only; **ask before any paid usage**. Do not purchase hosting or assume credits.
- No added factory hardware, factory access, representative phone images, manufacturer/buyer contacts or expert labels assumed.
- Preserve `experiment/` and all previous results. Do not edit either older plan to hide corrected assumptions.
- No external outreach, account terms acceptance, hackathon submission or owner signature on the human's behalf.
- Fit/development/calibration/test roles remain disjoint; original images split before crops/transforms.
- No test-derived preprocessing, thresholds, model choice or repeated holdout tuning.
- Ground truth is for evaluation, not an inference input. Scores are not probabilities and maps are not defect severity.
- All actual human decisions must come from a person; fictional ledger test records must be labelled fictional.
- Report failure and uncertainty. A gate failure stops dependent product work; it does not justify fabricating a successful demo.

## Review focus

1. Anomalib default validation/threshold callbacks must not access test images: explicit manifest access tests in T02/T04/T05.
2. Letterboxing/rotation/padding must preserve edge defects and original map coordinates: fixtures in T03.
3. Rejected media, missing models and recipe mismatch must never become an acceptable inspection: T04/T07.
4. Duplicates, rework and later uncertain decisions must not inflate coverage or reuse old acceptance: T08.
5. A timeout, duplicate request or late inference must not overwrite a newer human decision: T07/T08.

## 2. Human versus Codex: who does what?

| Activity | Codex responsibility | Human responsibility | Does it block technical work? |
|---|---|---|---|
| Start implementation | Read this plan, inspect workspace and execute once instructed | Request implementation when ready | Yes, current request is plan creation only |
| Product/model choices | Use the fixed decisions above; document evidence-driven changes | No hyperparameter or architecture selection required initially | No |
| Dataset download | Find official source, download public archives, audit/hash/extract safely | Complete a required CAPTCHA/login/provider form or personally accept terms, if encountered | Only that source; continue unaffected setup/tests |
| Dataset use terms | Record licence/attribution/restrictions; identify exact intended-use ambiguity | Decide/obtain permission if terms require it; Codex cannot grant commercial rights | Affected public/commercial use; not unrelated local software tests |
| Setup/dependencies | Create isolated environments, install compatible free packages, verify and lock | Approve any necessary OS/admin prompt personally; provide credentials only through the application's secure login | Only if no permitted portable alternative works |
| Data/labels | Parse supplied labels/masks; quarantine ambiguous/corrupt records | No manual relabelling needed for the first public-data experiment | No; unresolved labels are excluded/disclosed |
| Training/evaluation | Run all fits, calibration, tests, metrics, profiling and failure reports | Read the summary; no manual training commands needed | No |
| Human inspection | Prepare the UI and persist the person's decision | Review images and choose acceptable/defective/uncertain/rework | Needed for a real review record; fixtures can test software first |
| Timed review exercise | Prepare counterbalanced exercise, record/analyse responses | Complete the exercise honestly; do not inspect answer keys first | Needed for human-workload findings, not native benchmark metrics |
| Owner acknowledgement | Enforce role/state/snapshot rules and show the report | Personally acknowledge only the record reviewed | Needed for actual acknowledgement; demo identities remain disclosed |
| Factory validation | Prepare capture instructions, label sheet and feedback questions | Later obtain permitted real captures/expert feedback/contacts | Not required to run benchmark demo; required for field claims |
| Hosting | Package and test a concrete zero-cost option or static fallback; supply preview | Sign in/create account if necessary and decide whether public replay is sufficient | Affects deployment mode; local work can continue |
| Hackathon | Prepare technical summary, evidence, demo and limitations | Confirm eligibility/team details and submit entry | Needed for entry, not local model feasibility |
| Failed accuracy gate | Save honest results and propose smallest next experiment | Decide whether to change product/scope after seeing evidence | Blocks reliable-inspector app scope; no repeated permission for routine fixes |

**The human does not need to:** merge all datasets, label thousands of images, provision a GPU, manually fit models, choose thresholds, write backend/frontend code or run the reproducibility commands. Those are Codex tasks once implementation is requested.

## 3. Datasets, anomalies and when each is used

### D1 — MVTec 3D-AD `cable_gland`: RGB-only component experiment

- **Official source:** [MVTec 3D-AD](https://www.mvtec.com/research-teaching/datasets/mvtec-3d-ad). Local archive identity and source uncertainty are recorded in DATA_SOURCES.md; the exact download URL and early-review notice require reconciliation before freeze.
- **Imported layout:** 223 normal training RGB images, 23 normal validation RGB images; test 21 normal +87 anomalous RGB images. Audit labels, masks, groups and release identity before treating these as verified benchmark counts.
- **Expected folders:** `bent`, `cut`, `hole`, `thread`; verify downloaded taxonomy before finalising defect-family reporting.
- **What to flag:** visible cable-gland deformation, cuts, holes and thread anomalies in RGB. Geometry-only defects may not be visible in RGB; no 3D sensitivity is claimed.
- **What the model predicts:** anomaly/no anomaly and an attention map. It does **not** reliably name the defect subtypes, measure thread tolerances, test material strength or establish function.
- **Why first:** simpler-looking discrete component and a clear product narrative; rotation/normal surface variation still make it technically nontrivial. No performance improvement assumed.
- **Use:** T02 data audit; T03 geometry/baseline; T04 first PaDiM development fit; T05 locked calibration/evaluation; T07 first live-review screen if supported.

### D2 — KSDD2: second independent benchmark

- **Official source:** [ViCoS KSDD2](https://www.vicos.si/resources/kolektorsdd2/); [official dataset layout reference](https://github.com/vicoslab/mixed-segdec-net-comind2021/blob/master/datasets/README.md).
- **Published count:** train 2,085 normal +246 anomalous; test 894 normal +110 anomalous. Images approximately 230×630; audit actual sizes/masks.
- **What to flag:** visible scratches, spots and surface imperfections as **binary anomalies**. Do not invent subtype labels or equate this surface dataset with cable-gland parts.
- **Why second:** checks whether the same software can support a separate surface-inspection recipe. It is not evidence that the cable-gland model generalises to other components.
- **Use:** audit/split alongside D1 in T02; fit and development checks after D1 in T04; independent thresholds and result table in T05. UI recipe is exposed as benchmark-tested only if its own gates pass.

### Licence and provenance rule

Both proposed datasets specify **CC BY-NC-SA 4.0**. Treat the first build as research, retain attribution, check intended public-demo/redistribution terms and do not claim commercial permission. Framework code/weights have separate terms. Archive identity is the downloaded hash/date until a provider release ID is confirmed. Actual archive sizes and initial inventories are recorded in components/docs/DATA_SOURCES.md; the full data audit remains pending. Reserve **10 GiB disk as a provisional budget**, then record actual compressed/extracted bytes before proceeding. [D1 terms](https://www.mvtec.com/research-teaching/datasets/mvtec-3d-ad), [D2 terms](https://www.vicos.si/resources/kolektorsdd2/).

### Dataset/model timeline

| Stage | D1 cable gland (RGB only) | D2 KSDD2 | Forbidden |
|---|---|---|---|
| Acquire/audit | Inspect source, labels, masks and groups | Same independently | Random mirror substitutions without provenance |
| Prepare roles | Split official-training normals | Split official-training normals; preserve 246 anomalies for development | Borrowing test anomalies for tuning |
| Fit | B0 bank +P0 normal distribution | New B0 bank +new P0 distribution | Sharing either recipe's Gaussian/threshold |
| Development | Normal feasibility/geometry; no genuine training-anomaly recall available | Normals plus declared training anomalies | Tuning against calibration or test |
| Freeze | Both recipes and backends frozen **before either final test is scored** | Same freeze | Using D1 test failures to redesign D2 silently |
| Calibration | D1 normal calibration scores only | D2 normal calibration scores only | F1 optimisation on test labels |
| Final test | Separate published/cleaned membership and metrics | Separate metrics | Pooled raw-score AUROC or merged “accuracy” |
| Application | Primary operational candidate if supported | Optional second research recipe if independently supported | Advertising both as supported because one passed |

**VisA PCB1 is not training data for this build.** Preserve its failed experiment as history. Only RGB files from the cable-gland 3D-AD archive enter modelling. XYZ TIFFs and camera calibration files remain inert source evidence. No 3D engine, multi-view fusion, textile or maintenance task is added.

## 4. Exact data roles and leakage rules

Seed **4217**. Decode originals, validate labels/masks and form known physical-item/duplicate groups **before** role allocation. Preserve official train/test membership in one field and experimental role in another.

- From eligible official-training **normal groups**, assign **60% fit /20% development /20% calibration**, whole groups. Hash group IDs with seed/dataset, sort deterministically; first 60% fit, next 20% development, remainder calibration. Use nearest integer group counts with the remainder assigned to calibration; report actual image/group counts.
- If every image is independent: D1 expected 134/45/44; D2 expected 1,251/417/417. These are arithmetic expectations, not audited results.
- D1 official validation normals are development-only, never fit/calibration/test. If independent, they add 23 to the 45 training-development images (68 development normals). Quarantine cross-partition duplicates; do not move official test members into any development role.
- Fit pool: first **128** normal fit groups at most, one canonical image per duplicate group. Baseline takes first **16** of those. Save exact used IDs; unused normal fit images remain unused, not silently moved.
- D2 training anomalies (246) are development only, not PaDiM normal fitting. D1 has no genuine training anomalies; do not report development recall that does not exist.
- Official test images remain untouched until both configurations and calibration are frozen. Test labels/masks are accessible only to final evaluation and split-integrity audit, not preprocessing/model functions.
- Missing/corrupt/mismatched records go to quarantine with reason/count. Defective image missing mask is not a normal image. Normal zero masks are generated only from verified normal labels.
- Exact byte/decoded hashes and pHash+thumbnail near-duplicate candidates support auditing; they do not establish physical-product uniqueness. Record manual/grouping decisions and unknown IDs.
- Cross-official-split duplicate groups: quarantine contaminated test members and disclose changed subset/comparability. Never silently remove hard test cases.
- No augmentation in the default experiment. If a later protocol uses augmentation, split originals first and inherit parent/group IDs. Synthetic stress copies stay in separate outputs.
- Normal calibration selects thresholds/display scale once, never architecture or preprocessing. No Anomalib default test-derived validation or adaptive F1 threshold callback. [Inspected MVTec loader defaults](https://github.com/open-edge-platform/anomalib/blob/main/src/anomalib/data/datamodules/image/mvtecad.py).

## 5. Models and preprocessing: exact default experiment

### B0 — reference-image baseline

1. Convert to RGB float32 [0,1] using the recipe geometry below; preserve colour, no mean/brightness centring.
2. Store 16 deterministic normal fit references. Compare ≤4 at once; choose minimum mean squared RGB residual over valid pixels.
3. Smooth selected residual map with Gaussian sigma **1**; image score is mean of its highest **1%** valid pixels (at least one).
4. Return score and original-coordinate residual map. No rotations/registration, flips, tiled banks or defect-class labels.

### P0 — primary candidate

- **Algorithm:** PaDiM using pretrained frozen **ResNet18**, feature layers `layer1`, `layer2`, `layer3`, **100 retained channels**, seed 4217.
- **Implementation target:** **Anomalib 2.7.0**, low-level `PadimModel` behind our adapter; no default datamodule/Engine evaluation. Current API is documented, but pinned-wheel behaviour must pass T04. [Release](https://pypi.org/project/anomalib/2.7.0/), [PaDiM documentation](https://anomalib.readthedocs.io/en/latest/markdown/guides/reference/models/image/padim.html).
- Fit only selected normal images; do not fine-tune pretrained convolutional weights or use an optimiser/epochs for supervised learning.
- Preserve library Gaussian regularisation/map smoothing in the pinned implementation; record their exact values/code revision rather than claiming the old custom `.01I/sigma4` recipe is identical.
- Candidate adapter applies the verified pretrained backbone's input normalisation **exactly once**. Record actual weight provider, URL/config/checksum. Do not assume timm and old torchvision weights are identical.
- Derive our operational image score as the **maximum raw candidate map value over valid non-padding pixels**, regardless of the library's whole-map score. Retain both diagnostic library output and operational score with distinct names if useful.
- Save separate Gaussian/artifact state for D1 and D2. No spatial-normal pooling between products.

### Environment decision and bounded fallback

- First attempt: Python **3.12**, `anomalib==2.7.0`, CPU **torch 2.10.0 /torchvision 0.25.0** as target constraints. Public release pages exist; Windows CPU wheels, transitive dependencies and import/fit/save/load remain untested on this setup. Verify resolution before install and lock successful exact packages/hashes. [Anomalib requirements](https://github.com/open-edge-platform/anomalib/releases), [torch release](https://pypi.org/project/torch/2.10.0/), [torchvision release](https://pypi.org/project/torchvision/0.25.0/).
- Do not compile PyTorch from source, install CUDA, use `[full]`, or mutate `experiment/.venv`. Use `components/.venv-p0` for this path.
- Maximum **four hands-on hours** for P0 compatibility integration inside T04. If it fails, make one logged fallback to `components/.venv-p1`, using the existing compatible CPU **torch 2.6.0+cpu /torchvision 0.21.0+cpu**, trusted local ResNet18 weights and extracted compact **50-channel** PaDiM logic.
- P1 must support the declared 256×256 and 256×640 geometries with tests; do not import PCB1's hard-coded file paths/grid sizes or alter historical code. No new custom streaming/tile framework.
- Select one successful backend path for **both recipes before freeze**. If P0 fails one recipe's resource check and P1 is chosen, rerun development fits for both as P1; results remain clearly labelled P1.
- If neither works within T04's budget, record failure and stop dependent product work. Do not silently add PatchCore, YOLO, a paid cloud GPU or another dataset.

### Recipe geometry and resource caps

| Recipe | Geometry | Padding/mapping |
|---|---|---|
| `mvtec_3d_cable_gland_rgb` | Full image aspect-preserving letterbox to **H256×W256** | Centre padding, fixed RGB zero fill; no centre crop, rotation or registration; read only train/validation/test RGB PNGs, never XYZ TIFFs |
| `ksdd2_surface` | If portrait, fix recipe-wide **90° clockwise** orientation from training inventory, then letterbox to **H256×W640** | Same transform for all images/masks; no label-dependent rotation; record inverse transform |

Image resampling bilinear; evaluation masks nearest-neighbour. All map outputs restored to original coordinates; exclude padding from scoring/metrics. Padding may still influence nearby features/smoothing; record that limitation and inspect edge failures. No tiles in the first build.

- CPU batch 1, up to four Torch threads, DataLoader workers 0; log actual configuration.
- Monitor fit process RSS; stop if it exceeds **min(4 GiB, 60% of available RAM at process launch)**. Measure model-init/fit/inference separately. Library PaDiM may retain embeddings across batches, so batch 1 alone does not bound memory. [Model source](https://github.com/open-edge-platform/anomalib/blob/main/src/anomalib/models/image/padim/torch_model.py).
- Hard technical rejection: invalid JPEG/PNG, animation/multipage, >10 MiB bytes, >20 MP decoded, minimum side <128, unknown recipe or missing/mismatched calibrated artifact. A malformed upload never becomes “normal.”
- Exposure/blur are **warnings**, not benchmark exclusions. Log mean luma, clipped fraction and focus diagnostic; do not claim the old gate was validated. No new warning thresholds affect acceptance or model metrics.

### Calibration and artefacts

Per method/recipe, sort accepted normal-calibration image scores. Let **k=ceil(0.90×(n+1))**, one-based; threshold is kth score and flag only **score > threshold**. Fail if k>n or insufficient usable normals. Report n/ties/empirical FPR. This is normal-only FPR-oriented calibration, not industrial assurance or defect-recall optimisation.

Display map range: zero to 99.5th percentile of a seed-4217 sample of up to 10,000 valid pixels per normal calibration image; equal image weights. Clip higher intensities; preserve raw maps. Degenerate range uses epsilon plus a diagnostic. Label **“anomaly intensity—not probability or severity.”** No binary segmentation threshold/IoU gate in the default build.

Bundle includes dataset/archive and fit/calibration manifest hashes, recipe/geometry, backend/dependency lock, feature/weight/channel identity, Gaussian state/reference bank, operational score rule, threshold, display scale, code hash, metric status and licences. Development bundles can lack thresholds; operational API must reject uncalibrated bundles.

## 6. Evaluation gates and what happens after failure

Freeze **both** recipes' defaults/backends, data roles and primary-method choice before final calibration/test. Do not tune while inspecting official-test predictions.

### Provisional screens, per recipe

| Measure | Target | Counting rule |
|---|---|---|
| All-defect flag recall | ≥90% | Rejected/not-scored defective images count as misses |
| FPR on accepted normal images | ≤10% | Also report false flags/all normals |
| Technical scoring coverage | ≥90% | Scored images /all eligible test images |
| Warm native p95 | ≤5 s/image | Decode, geometry, inference and map restoration included |
| Inference peak process RSS | ≤4 GiB | Report model init and fit RSS too |

Targets are provisional engineering screens, not industry requirements. For unmodified D1 test counts, recall needs at least 79/87 anomalies flagged; FPR permits at most 2/21 normal false flags. Counts and intervals matter; 21 normals provide weak assurance. D2 results are independent.

**Required report:** TP/FN/FP/TN, rejected counts/reasons, recall, FPR, precision at observed prevalence, coverage, image AUROC and AP, pixel AUROC/AP where masks are valid, per-verified-defect-folder recall, cold/fit/warm timing, peak RSS, model bytes and failures. Wilson 95% intervals for proportions; image/group bootstrap for ranking metrics if meaningful. No pixel-independent confidence intervals, raw-score pooling or made-up class labels.

- Model score/mask evaluation is separate from human correctness and product acceptance.
- Pixel maps are diagnostic; do not claim segmentation reliability from attractive overlays or a peak inside a large mask.
- Run synthetic brightness ×0.6 /×1.4 and blur radius 2 on labelled paired copies only after original test; unchanged thresholds, separate tables.
- P0 (or pre-test P1 fallback) is primary; B0 comparison is fixed. If B0 passes and primary fails, report this as evidence for a baseline-only research demo, with test-based selection disclosed. Stronger deployment claims require independent confirmation.
- Both recipes fail → deliver experiment/failure report and stop full app work. Do not recycle the same holdout to tune until passing.
- Only one passes → app exposes only that recipe as benchmark-supported. The failed recipe remains in results, not silently deleted.
- Both pass → app may expose two independent recipe choices. Still no arbitrary component, phone or real-factory claim.

## 7. Proposed implementation structure and contracts

Create only after implementation is requested:

```text
components/
  pyproject.toml
  requirements-p0.lock /requirements-p1.lock     # only actual selected path locked
  .venv-p0/ /.venv-p1/                         # ignored; never overwrite old experiment
  configs/{protocol,mvtec_3d_cable_gland_rgb,ksdd2_surface}.yaml
  src/component_inspector/
    cli.py
    contracts.py
    data/{acquire,adapters,audit,split}.py
    vision/{geometry,reference,padim_adapter,artifact_store}.py
    evaluation/{calibrate,metrics,runner,reports,stress}.py
    application/{api,store,ledger,export}.py
  tests/{test_sources,test_splits,test_geometry,test_reference,
         test_padim,test_calibration,test_metrics,test_api,test_ledger,test_export}.py
  web/{package.json,package-lock.json,src/{App,Review,Batch,Report}.tsx}
  data/{archives,raw,manifests}/
  models/<recipe>/<model_id>/
  runs/<run_id>/{freeze,calibration,predictions,metrics,failures,environment,...}
  outputs/{reports,human_exercise,demo}/
  docs/{STATUS,REPRODUCE,DATA_SOURCES,MODEL_CARDS,DEPLOYMENT}.md
```

Choose/verify free frontend/API tooling versions at their implementation task and commit their lockfiles. Do not invent already-tested version pins or install unrelated tools just to match a template. New code uses the new namespace; no hard-coded PCB1 imports.

### Contracts in `contracts.py`

```text
ImageRecord: dataset, release_hash, recipe, id, path, mask_path|null,
 hashes, physical_group|null, grouping_confidence, original_shape,
 official_split, experiment_role, label, defect_type|null,
 provenance, parent_id|null, quarantine_reason|null

PreparedImage: rgb_float32, valid_roi, geometry, original_shape
ArtifactBundle: model_id, recipe_id, backend, config, fit_manifest_hash,
 weight_hash, model_state, threshold|null, display_range|null,
 calibration_hash|null, environment_hash, validation_status
Prediction: status(scored|not_scored), reasons[], warnings[],
 score|null, threshold|null, flagged|null, map_original|null,
 recipe_id, model_id, preprocess_id, timing_ms

load_records(dataset_id: str, root: Path) -> list[ImageRecord]
audit(records: list[ImageRecord]) -> AuditReport
split(records: list[ImageRecord], seed: int) -> SplitManifest
prepare(image: PIL.Image, recipe: RecipeConfig) -> PreparedImage
fit(method_id: str, fit_records, recipe_config) -> ArtifactBundle
predict(prepared: PreparedImage, artifact: ArtifactBundle) -> Prediction
calibrate(scores: list[float], alpha: float=0.10) -> ThresholdRecord
evaluate(predictions, labels_and_masks) -> MetricsReport
record_decision(inspection_id: str, decision: str, reviewer: str, note: str) -> DecisionEvent
batch_snapshot(batch_id: str) -> BatchSnapshot
```

Baseline consumes `rgb_float32` directly. PaDiM adapter normalises a tensor according to its verified weight configuration once. Model/inference functions never accept labels/masks. `Prediction.flagged` stays null if not scored or development artifact is uncalibrated; operational endpoint requires calibration. Artefact registry checks recipe/model/hashes before any inference.

## 8. Ordered tasks for Codex

**General task discipline:** inspect applicable repository instructions; write meaningful failing tests for new behaviour, confirm failure, implement the smallest change, run named checks, record evidence. If Git is available, commit verified logical units; do not initialise/publish a repository, move user files or create a PR unless requested. Keep `docs/STATUS.md` updated with completed work, blockers and next task so execution can resume across chats.

### T01 — Workspace, runtime and source readiness

**Owner:** Codex. **Human:** only required account/form/terms/admin action if encountered. **Depends:** implementation request. **Files:** package scaffold, `data/acquire.py`, `tests/test_sources.py`, `docs/{STATUS,DATA_SOURCES}.md`. **Budget:** 2–3 h hands-on plus external waiting.

- [ ] Read this guide and the reviewed plan; snapshot hashes of previous evidence and inspect existing workspace instructions/runtime paths.
- [ ] Create the isolated `components/` package and source acquisition ledger. Record CPU/RAM/disk, Python/Node availability and no-paid settings. If a runtime needs setup, Codex handles a permitted isolated/portable setup first.
- [ ] Inspect current official download flow for D1/D2. Support public download and `--archive PATH`; never automate accepting personal terms or bypass access forms. Record the exact human action if blocked.
- [ ] Test safe extraction, root escape/symlink/archive-bomb rejection and source/hash/licence records; keep raw sources immutable and uncommitted.
- [ ] Acquire/audit archive bytes and readable samples. Run `pytest tests/test_sources.py -v`; stop affected adoption if source/terms/schema are unusable.

**Deliverable:** reproducible workspace/source ledger, archive hashes/samples or a precise access blocker. Human need not manually run download scripts.

### T02 — Adapters, inventories and frozen data roles

**Owner:** Codex. **Human:** none for ordinary public labels. **Depends:** T01 usable archives. **Files:** `data/{adapters,audit,split}.py`, contracts/configs, `tests/test_splits.py`. **Budget:** 2–3 h.

- [ ] Test mask pairing, zero-mask normal logic, missing-defect-mask quarantine, group leakage and deterministic role membership.
- [ ] Implement D1/D2 adapters independently; preserve original split and actual taxonomy, dimension/count audit and physical-ID uncertainty.
- [ ] Audit decoded/exact/near duplicates; group originals and allocate section 4 roles. Save exact used/unused fit IDs; block test records from fitting/calibration functions.
- [ ] Save `data/manifests/{sources,inventory,audit,splits}.json`; freeze roles before model inference and document any published-count deviations.
- [ ] Run `pytest tests/test_sources.py tests/test_splits.py -v`; require zero unreported cross-role groups. Keep a summary for the human; no manual “approve every file” step.

**Deliverable:** immutable two-dataset manifests and usable samples for development.

### T03 — Shared geometry and B0 reference baseline

**Owner:** Codex. **Human:** none. **Depends:** T02. **Files:** `vision/{geometry,reference}.py`, `tests/{test_geometry,test_reference}.py`. **Budget:** 2–3 h.

- [ ] Write fixtures for aspect preservation, original-coordinate edge mark, grayscale/EXIF handling, fixed recipe-wide KSDD2 rotation and padding exclusion.
- [ ] Implement section 5 geometry and B0 bank/score. Model inputs cannot include mask/label/folder metadata. Use technical rejects and warning diagnostics, not quality filtering of hard benchmark examples.
- [ ] Fit B0 on D1 references first, then a separate D2 bank. Save raw units/geometry and scores/maps on development images only.
- [ ] Test reference selection determinism, finite scores, original map shape and chunked comparison equivalence.
- [ ] Run geometry/reference tests; profile development latency/memory. Do not add rotation banks merely because an unrotated example looks difficult.

**Deliverable:** real CPU baseline predictions/maps for both recipes, without thresholds or final-test results.

### T04 — P0 integration, bounded fallback and native feasibility

**Owner:** Codex. **Human:** only unavoidable system permission; no GPU setup needed. **Depends:** T03. **Files:** `vision/{padim_adapter,artifact_store}.py`, `tests/test_padim.py`, backend lock/config. **Budget:** 4–6 h, including ≤4 h for P0 compatibility integration.

- [ ] Inspect exact Anomalib wheel/source and target dependency resolution; create `.venv-p0`, install only CPU-compatible dependencies and record hashes/versions. If target pins do not resolve, investigate within timebox; do not unpin silently.
- [ ] Test normalisation exactly once, frozen parameters, stored channel selection, shape/valid-ROI score, trusted load parity and recipe mismatch rejection.
- [ ] Fit P0 on ≤128 **D1 normals first**, then a separate D2 fit. Score only development data; log accessed IDs and prevent library validation on test/calibration.
- [ ] Measure actual feature shapes, model bytes, fit/inference RSS/time and numerical failures under resource caps. If path fails, log P1 fallback and rerun both recipes' development fits with its separate environment before freeze.
- [ ] Run model tests and save/load checks; raw score/map parity target `atol=1e-5, rtol=1e-5` on the same backend. Any failure is investigated, not threshold-tuned away. If both paths fail, stop and deliver feasibility report.

**Deliverable:** one selected backend, separate trusted D1/D2 model bundles and native development feasibility evidence. No final accuracy claims yet.

### T05 — Protocol freeze, calibration and untouched evaluation

**Owner:** Codex. **Human:** read decision summary; no manual threshold selection. **Depends:** T04 resource/engineering pass. **Files:** `evaluation/*.py`, `tests/{test_calibration,test_metrics}.py`, `runs/<run_id>/...`. **Budget:** 3–5 h.

- [ ] Write hand-computable metric/quantile tests, null-denominator checks and calibration/test access restrictions. Validate AP/AUROC against pinned scikit-learn.
- [ ] Freeze **both** recipe configs, backend, primary method, roles and code hashes. Default is no extra alignment/resolution variant; a failure needing a changed protocol is logged before further tuning.
- [ ] Calibrate each B0/P0-or-P1 bundle from its own normal calibration split only; save threshold/display hashes before reading final predictions.
- [ ] Evaluate D1 official test, then D2 official test using already-frozen configs. No changes between them in response to D1 scores; a discovered correctness bug invalidates affected results and must be disclosed.
- [ ] Save all per-image predictions/counts/intervals, per-recipe metrics, native timing/RSS, failure gallery and gate decisions. Then run separate transformed stress tests. Run calibration/metric tests; issue a go/conditional/no-go with exact evidence.

**Deliverable:** benchmark report for both datasets and named eligible recipe(s). **Gate:** if no usable recipe, T06–T10 stop unless the human explicitly asks for an educational failure demo. No automatic full model search.

### T06 — Application foundation and trusted inference service

**Owner:** Codex. **Human:** none for local setup. **Depends:** T05 eligible limited-assistance scope. **Files:** `application/{api,store}.py`, model registry in artifact store, `tests/test_api.py`, frontend package/lock. **Budget:** 3–5 h.

- [ ] Create FastAPI/Pydantic and React/TypeScript/Vite app using verified locked free dependencies; no cloud account required. SQLite local schema/transactions, no PostgreSQL dependency.
- [ ] Implement synchronous bounded `POST /api/inspect` with concurrency 1, calibrated artifact checks, recipe selection and image limits. Return 503 when busy rather than queueing.
- [ ] Test malformed/huge media, unknown recipe, mismatched model hash, uncalibrated bundle, duplicate key and client disconnect/timeout. Keep lock until native inference ends; no late overwrite.
- [ ] Define response/error schemas in section 9; return no fake normal score on failure. Original/model artifacts stay outside public assets.
- [ ] Run API tests/typecheck/build. Record full API latency separately from model latency; localhost only by default.

**Deliverable:** real local native inference API, with explicit failure responses.

### T07 — First end-to-end human review

**Owner:** Codex for UI/persistence; **human** for the actual decision. **Depends:** T06. **Files:** `web/src/{App,Review}.tsx`, `application/ledger.py`, API/ledger tests. **Budget:** 3–5 h plus short human action.

- [ ] Implement one-image upload using an eligible recipe; show input/attention overlay/score/threshold/version/warnings. Interface text says “not flagged,” never “approved by AI.”
- [ ] Add acceptable/defective/uncertain/rework actions and save immutable decision events. Separate model result from human disposition.
- [ ] Run automated fixture UI/API checks and reload tests before requesting the person's participation.
- [ ] Present a development image in the working local interface; human reviews and chooses an outcome. Record actual input/decision, then reload and verify persistence.
- [ ] If person unavailable, keep actual human step pending and continue independent software fixtures; do not substitute a fabricated decision and claim milestone complete.

**Deliverable:** **image → real inference → score/map → actual human decision → saved/reloaded record**. This is the first complete end-to-end milestone, before batch/report polish.

### T08 — Batch history, rework and truthful export

**Owner:** Codex; **human** only for genuine report acknowledgement. **Depends:** T07's software path (actual human participation can remain explicitly pending). **Files:** ledger/export modules, `web/src/{Batch,Report}.tsx`, ledger/export tests. **Budget:** 6–10 h.

- [ ] Test six expected product IDs with duplicate same-product upload, cross-product image reuse block, new rework capture, later uncertainty, uninspected IDs and acknowledgement invalidation.
- [ ] Implement batch counters/history under transactions. Definitions: `current_scored` and `current_reviewed` refer to the latest attempt of each unique product; `ever_scored`/`ever_reviewed` are separate historical counts. Never mix attempts with unique products.
- [ ] A new attempt reopens resolution; old acceptance cannot cover a newer uncertain/rework state. All expected products must be resolved for final acknowledgement in the minimal workflow; partial exports remain drafts.
- [ ] Export HTML/CSV from one snapshot with counts, original image links, model/calibration identity, decisions, source attribution and limits. Escape HTML/spreadsheet formulas. Acknowledgement is a human snapshot record, not shipment certification.
- [ ] Run ledger/export/API tests and frontend checks; reconcile UI/API/report counters on the explicitly fictional fixture. Prepare a sample with real benchmark model observations and fictional batch IDs clearly separated.

**Deliverable:** complete batch user journey and honest draft report.

### T09 — Timed human review pilot and feedback materials

**Owner:** Codex prepares/analyses; **human** participates. **Depends:** T08. **Files:** `outputs/human_exercise/`, analysis/feedback docs. **Budget:** 4–7 h plus actual participant time.

- [ ] Prepare 24 disjoint benchmark items: 12 manual, 12 assisted, balanced normal/anomalous per arm; stratify verified defect family/size where feasible. Randomise arm order and record seed; no image repeats across arms. More participants can counterbalance order.
- [ ] Freeze exercise/analysis before responses; export actual time, decision, uncertainty and hints-used records. Do not show answer keys before completion.
- [ ] Human completes exercise. Codex analyses error counts/time jointly; no time-saving claim if capture time is absent or assistance worsens errors.
- [ ] State small convenience sample, synthetic prevalence, matching/order limitations and lack of expert/factory validation.
- [ ] Draft manufacturer/buyer feedback questions about current alternatives, report utility, extra steps and missing evidence. Do not contact anyone or invent answers.

**Deliverable:** real pilot findings or prepared exercise marked pending. Does not establish factory efficacy.

### T10 — Packaging, deployment mode and handoff

**Owner:** Codex prepares/tests; **human** handles required sign-in, final product choice and submission. **Depends:** T08; T09 results/pending disclosed. **Files:** deployment/reproduction docs, `outputs/demo/`, final model cards. **Budget:** 5–8 h plus hosting/account delays.

- [ ] Package clean local startup and reproducibility commands; verify restart persistence, missing artifacts, reset behaviour, resource limits and report download.
- [ ] Investigate a concrete zero-cost live option only if it meets account/terms, RAM, model download, latency and persistence needs. No paid plan assumed or purchased. Treat any new route as a deployment experiment, not promised infrastructure.
- [ ] Prepare static replay fallback with precomputed benchmark predictions and declared fictional batch IDs. Disable unsupported live uploads; label browser-local demo decisions as non-shared/non-durable.
- [ ] Before public publication, prepare the exact build, intended content, licence notes and deployment configuration for review; use existing authorisation if sufficient. Human completes account/terms prompts personally. No production-data uploads.
- [ ] Run full relevant tests/typecheck/build once after final changes; rehearse success, miss, false alarm, duplicate/rework and incomplete batch. Save final evidence and go/conditional/no-go. Human submits hackathon entry.

**Deliverable:** local live detector plus verified deployment mode, source/reproduce instructions, model cards, sample report and known limitations. A static replay is **not** a deployed live inference service.

## 9. API, state and local security contract

| Endpoint | Required behaviour |
|---|---|
| `GET /api/recipes` | Only loaded/calibrated eligible recipes, model version and research status |
| `POST /api/batches` | JSON batch ID, recipe ID, expected unique product IDs; reject duplicates, cap 1,000 IDs |
| `POST /api/inspect` | Multipart batch ID/product ID/recipe ID/image plus idempotency header; synchronous response with inspection ID and Prediction |
| `POST /api/inspections/{id}/decision` | Append decision/reviewer/note; never alter model observation |
| `GET /api/batches/{id}` | Consistent unique-product current/historical counts and event history |
| `POST /api/batches/{id}/acknowledgement` | Owner acknowledgement of current resolved snapshot; do not forge identity |
| `GET /api/batches/{id}/report?format=html|csv` | Snapshot-derived draft/acknowledged report |

Errors: 413 encoded/decoded size; 415 unsupported format; 422 invalid decode/fields; 409 recipe/idempotency/content-reuse/state conflict; 503 busy/missing artifact. No internal paths/secrets in responses. Same key+payload returns same result; changed payload 409. Never cancel a native thread and release concurrency as if inference ended.

Local role labels are explicitly demo identities. Public shared uploads/storage require an additional authentication/authorisation/CSRF/retention/rate-limit design before enabling that mode. Bind **127.0.0.1:8766** by default; preserve existing experiment port 8765. Keep uploads outside public root, use generated filenames, strip metadata in display copies and never fetch arbitrary user URLs. Trusted locally created weights only.

## 10. Future commands Codex will implement and run

**These commands are a CLI contract, not commands that currently exist.** Codex implements each before using it; the human is not asked to run them manually. Run from `components/` using the selected environment's Python (`.venv-p0/Scripts/python.exe` or `.venv-p1/Scripts/python.exe`).

```powershell
python -m component_inspector.cli doctor
python -m component_inspector.cli acquire --dataset mvtec_3d_ad --category cable_gland --archive "C:\Users\laksh\OneDrive\Desktop\Tech4Bharat\components\data\archives\cable_gland.tar.xz"
python -m component_inspector.cli acquire --dataset ksdd2
python -m component_inspector.cli prepare --config configs/protocol.yaml
python -m component_inspector.cli fit --recipe mvtec_3d_cable_gland_rgb --method reference
python -m component_inspector.cli fit --recipe mvtec_3d_cable_gland_rgb --method padim
python -m component_inspector.cli fit --recipe ksdd2_surface --method reference
python -m component_inspector.cli fit --recipe ksdd2_surface --method padim
python -m component_inspector.cli develop --config configs/protocol.yaml
python -m component_inspector.cli freeze --config configs/protocol.yaml
python -m component_inspector.cli calibrate --frozen-run RUN_ID
python -m component_inspector.cli evaluate --frozen-run RUN_ID
python -m component_inspector.cli stress --frozen-run RUN_ID
python -m component_inspector.cli report --run RUN_ID
python -m pytest tests -q
python -m component_inspector.cli serve --host 127.0.0.1 --port 8766
npm --prefix web ci
npm --prefix web run typecheck
npm --prefix web run build
```

`method=padim` resolves the **frozen** selected P0/P1 backend; the run cannot quietly change it. `fit/develop` reject calibration/test paths. `freeze` saves configs/roles/code/artifact hashes and primary method, `calibrate` appends immutable thresholds from calibration IDs only, and `evaluate` refuses an incomplete/unfrozen bundle. `stress` writes separate paired results, never overwrites original test results.

## 11. Stop conditions, effort and checkpoints

| Checkpoint | Codex can proceed when… | If not… |
|---|---|---|
| After T01/T02 | Actual sources/terms, labels/masks and roles usable | Report exact missing human action or dataset blocker; continue unaffected tests |
| After T04 | A named backend produces finite repeatable native outputs within resource caps | One declared P1 fallback, then stop if it fails; no unbounded installation/model search |
| After T05 | A recipe supports the provisional limited benchmark claim | Stop reliable-inspector app work if both fail; report failures and bounded next experiment |
| After T07 | Real human decision saved/reloaded | Leave actual-participant milestone pending; do not fabricate completion |
| After T09 | Actual human exercise completed | No inspection-time benefit claim if pending or unsupported |
| After T10 | Deployment mode tested and accurately described | Deliver local demo and precise limitation; never rename replay as live inference |

**Planning allocation:** T01–T05 **13–20 h**; T06–T10 **21–35 h**; contingency **8–15 h**; total **42–70 h**, plus participant/access waiting. These are proposed budgets, not measured durations. Re-estimate after T04/T05. Additional export/mobile/field-validation work is outside these figures.

Retained hackathon milestones are registration 10 Nov, idea 15 Nov, prototype 15 Dec and finale 27 Dec 2026; **current rules and team eligibility remain to reconfirm**, as the organiser page was inaccessible during the review. Codex researches/prepares the checklist; the human supplies personal/team details and submits. No calendar start/date commitment assumed.

**Cut first:** browser/ONNX export, phone support, observation map, animation, third dataset, subtype classifier, custom registration/tiling, multi-user cloud backend. Do not cut leakage checks, normal-only calibration, honest failure tables, human confirmation or accurate coverage.

**Optional later export:** only after native gates, a separately timeboxed native→ONNX→actual laptop-browser parity test covering geometry/normalisation/map/score/decisions, cold/warm latency, download bytes and failure cases. No quantisation speedup or phone compatibility assumed. It is not required to complete T01–T10.

## 12. Completion checklist and human handoff

- [ ] Source/licence/release and exact fit/calibration/test IDs recorded for both datasets.
- [ ] B0 and selected P0/P1 results reported separately per recipe; failed recipes retained in evidence.
- [ ] Native inference and trusted save/load tested; preprocessing/normalisation and map coordinates verified.
- [ ] Frozen thresholds/code/config; no contaminated test results passed off as untouched.
- [ ] Actual human review milestone completed or visibly pending.
- [ ] Duplicates/rework/uncertain/uninspected counts and acknowledgement invalidation verified.
- [ ] Sample HTML/CSV report includes provenance, coverage and limitations; no certification claim.
- [ ] Human pilot results or pending status explicit; no invented manufacturer/buyer feedback.
- [ ] Deployment labelled **local live**, **hosted live** or **static replay**, with tested instructions and fallbacks.
- [ ] Final README/model cards list measured results, failure examples, resource requirements and unresolved field risks.
- [ ] No paid usage, external outreach, private upload, user signature or hackathon submission performed without applicable authorisation.

### Human's minimum practical checklist

1. Request implementation when this plan is ready to execute.
2. Complete a provider form/account prompt only if Codex cannot access official data publicly.
3. Review at least one image in the working app and later complete the timed exercise.
4. Review the report before personally acknowledging it; do not treat benchmark data as an inspected factory consignment.
5. Decide whether deployed replay +local live inference is sufficient **if** a zero-cost live public backend cannot be verified.
6. Confirm hackathon/team details and submit the prepared entry yourself.

No requirement to obtain factory contacts or a GPU before the benchmark build. Later real-world/production claims require representative captures, expert/worker feedback and appropriate data permissions; Codex cannot substitute public benchmark success for that evidence.

## 13. Sources, skill use and document status

- Primary dataset and model sources linked beside decisions were checked on **18 October 2026**; full research reasoning remains in the reviewed plan. Exact package pages were verified to exist; dependency/wheel/runtime compatibility has **not** been tested by creating this file.
- Skills actually used for this guide: **writing-plans** for task/interfaces/checks and **senior-computer-vision** for data/model/preprocessing sequencing. Existing research/audit was reused; no broad research or implementation rerun was necessary.
- This file supersedes older task ordering for the proposed next build. It does not alter past evidence, establish new accuracy or authorise implementation by itself.
- Before execution, Codex must inspect any new user/repository instructions. Routine reversible implementation decisions stay with Codex; scope, paid usage, actual human decisions and external account/submission actions stay with the human as described above.
