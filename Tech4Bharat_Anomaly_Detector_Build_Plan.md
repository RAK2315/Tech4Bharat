# Tech4Bharat Component Anomaly Detector Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL at implementation time: use `executing-plans` for native task-by-task execution, or `subagent-driven-development` only if the user explicitly selects delegation. Steps use checkbox tracking. **This document authorises no implementation: the current request is to save the plan only.**

**Goal:** evaluate and, only if gates pass, build a human-reviewed component inspection assistant using MVTec AD metal nuts and KSDD2 as separate tasks.

**Architecture:** one shared image/manifest/evaluation pipeline, two independently fitted product recipes and thresholds, native CPU inference first. A TypeScript review interface calls a local Python service and saves human decisions and truthful batch records. An observation map shows recorded inspections; factory simulation, causal diagnosis and 3D modelling are excluded.

**Tech Stack:** Python 3.12, existing compatible CPU PyTorch/torchvision versions, NumPy, Pillow/OpenCV, scikit-learn, SQLite, FastAPI/Pydantic, React/TypeScript; optional ONNX only after native validation.

**Spec:** the user's attached “Create a detailed, executable Markdown build plan…” instructions, [team brief](TEAM_PROJECT_BRIEF.md), [components shortlist](COMPONENT_DATASETS.md), and the authoritative failure evidence in [experiment report](experiment/artifacts/EXPERIMENT_REPORT.md). This plan supersedes the earlier PCB1-first recommendation **for the proposed next experiment**, not its historical results.

**Status/date:** 17 October 2026. Planning only; no new datasets downloaded, models fitted, API/UI implemented, or deployment performed in this task. Dataset pair is the planner's recommendation, not a recorded user selection.

## Global constraints

- Components only; first recipe one metal-nut category; second recipe one KSDD2 surface-image task.
- “No hardware is to be use” is interpreted from the discussion as no added factory/capture hardware; existing computer use is permitted.
- “Only free API keys should be used”; prefer local processing with no API key. Ask before paid usage.
- Do not assume factory access, representative phone images, GPU compute availability, manufacturer/buyer contacts or additional teammate capacity.
- “This task is to create and save the plan, not implement the project.”
- “Keep reference/training, calibration/validation, and untouched test data separate.”
- “Split originals before augmenting training data.”
- “Do not claim experiments have run unless actual results exist in this chat.”
- “Do not assume browser/mobile compatibility without an experiment.”
- “Preserve the narrow inspection-assistant scope; exclude unsupported root-cause and factory-wide digital-twin claims.”
- Owner acknowledgement applies to records of what was actually inspected, never to inferred whole-batch quality.

## Review focus

1. A rotated but normal nut must not be silently “corrected” into a different face; alignment is in-plane only, with failures recorded (Tasks 3–4).
2. A malformed, huge, mislabeled or unsupported upload must produce rejection/retake without a false acceptable disposition (Tasks 7–8).
3. Duplicate photos, cross-product reuse and rework must preserve product identity and history without inflating coverage (Task 8).
4. Calibration/test duplicates or same-item views must be grouped/quarantined; a missing identifier must be disclosed, not guessed (Task 2).
5. Missing/stale model artifacts or a recipe mismatch must block inference rather than fall back to a different product's model (Tasks 7–9).

## 1. Recovered context and assumptions

| Item | Recovered fact or explicit planning assumption |
|---|---|
| Builder/skills | One person using Codex; TypeScript frontend preferred. Personal ML experience and extra teammates' availability not established |
| Timing | Earlier research recorded registration 10 Nov, idea 15 Nov, prototype 15 Dec, finale 27 Dec 2026; exact rules/dates need reconfirmation |
| Eligibility | Earlier sources conflicted on team size/student requirements; unresolved |
| Budget | No paid inference, training or hosting; no new hardware |
| Existing tested hardware | Previous experiment records Ryzen 7 260, 8 physical/16 logical cores; CPU-only inference tested. An RTX 5050 was detected, but driver/training usability is not established or required |
| Existing environment | Experiment uses Python 3.12.14, torch 2.6.0+cpu, torchvision 0.21.0+cpu; preserve it as historical/reproducibility evidence |
| Data/contacts | Public datasets only; no target-factory photographs or expert labels |
| Deployment assumption | Local native-inference demo first; deployed frontend/replay fallback. A free continuously hosted inference backend is not assumed |
| Outputs | Save this plan beside the existing user-facing Markdown documents in project root |

The [hackathon page](https://hackculture.io/hackathons/tech4bharat-gavs-hackathon) was inaccessible through the research tool during the earlier document update. Dates above are retained findings, not freshly verified rules. Task 1 must reconfirm them before scheduling submission. No invented judging weights.

### Existing evidence to preserve

VisA PCB1 reference matching found 15/80 defects with 1/100 false flags; compact PaDiM found 45/80 with 15/100 false flags. Both failed the frozen screen. CPU speed and limited laptop browser parity worked; field reliability and human time savings remain unproven. See [complete evidence](experiment/artifacts/EXPERIMENT_REPORT.md). A simpler-looking product does not guarantee improvement.

## 2. Dataset pair and exactly what to detect

### Dataset A: MVTec AD, `metal_nut`

- **Official source:** [provider page, licence and downloads](https://www.mvtec.com/research-teaching/datasets/mvtec-ad); [original CVPR 2019 paper](https://www.mvtec.com/fileadmin/Redaktion/mvtec.com/05_research_teaching/datasets/mvtec_ad.pdf).
- **Version:** original MVTec AD, not AD 2; selected archive/date/hash will identify the actual release. Archive not retrieved yet.
- **Product:** the dataset's metal nut design, visible face and background. Initial real-capture recipe would require comparable framing and diffuse illumination; this has not been tested.
- **Expected anomaly folders to verify during ingest:** `bent`, `color`, `flip`, `scratch`. Their existence and spelling must be asserted against the downloaded release before UI copy or per-type reporting is frozen.
- **Meaning:** visible deformation, unusual surface colour, incorrect face/orientation and scratches. `flip` is a recipe/orientation violation, not necessarily physical damage. Do not label every anomaly “damaged.” No functional, hidden-crack, precise dimensional or material assurance.
- **Outputs:** image-level flag/no flag and continuous localisation map. Defect family is ground-truth reporting metadata or a human annotation, **not a predicted subtype**.
- **Published counts:** 220 normal training images; test 22 normal +93 anomalous, four defect families. Nuts have random in-plane rotation and normal surface variation. Real captured images include deliberately generated defects under controlled acquisition; they are not a random factory reject sample. [Original paper, Table 1 and dataset discussion](https://www.mvtec.com/fileadmin/Redaktion/mvtec.com/05_research_teaching/datasets/mvtec_ad.pdf).
- **Labels/masks:** official train is normal only; anomalous test regions have pixel annotations. Validate exact dimensions/label consistency after download.
- **Access/licence:** provider download workflow; CC BY-NC-SA 4.0. Non-commercial research use is the planning basis. Check hackathon/demo display and redistribution terms; commercialisation requires clearance or replacement data. Code/weights have separate terms. [Official terms](https://www.mvtec.com/research-teaching/datasets/mvtec-ad).
- **Size:** no current archive bytes verified. Reserve **1 GB** for the selected category and working copies; a full-dataset-only download may require several GB. These are disk budgets, not observed sizes. Record Content-Length where supplied, actual bytes and extracted bytes in Task 1.
- **Relevance:** recognisable discrete component and reusable benchmark protocol. **Contradictory evidence:** the original paper reports rotation/surface variation challenging classical methods; therefore “simpler” means narrower visual/product scope, not established easier detection.

### Dataset B: KolektorSDD2 / KSDD2

- **Official source:** [ViCoS provider, paper and download](https://www.vicos.si/resources/kolektorsdd2/); research paper *Mixed supervision for surface-defect detection: from weakly to fully supervised learning*, 2021.
- **Version:** original KSDD2 release, not KSDD; freeze archive checksum/date after access.
- **Product/task:** provider's production-item surface image, not a generic metal-nut image. Verify physical product context from release documentation; until then name the recipe **KSDD2 component surface**, not “metal nut line B.”
- **Anomalies:** visible scratches, minor spots and surface imperfections; binary anomaly detection/localisation, no invented subtype labels.
- **Official counts:** training 2,085 normal +246 defective; test 894 normal +110 defective. Typical image size about 230×630. Industrial controlled acquisition. [Provider description](https://www.vicos.si/resources/kolektorsdd2/).
- **Labels/masks:** audit the published image/mask pairing and mask semantics on retrieval; normal masks should be generated as zeros only after validating image-level normal labels. Missing masks on defective examples are an error, not an all-zero mask.
- **Access/licence:** provider links download; CC BY-NC-SA 4.0, commercial use requires provider contact. Download not performed here. [Provider terms](https://www.vicos.si/resources/kolektorsdd2/).
- **Size:** archive bytes not verified; reserve **1 GB** for raw/extracted/derived data. Confirm instead of promising a download size.
- **Relevance:** more normal examples and a different narrow surface task; tests pipeline reuse without pretending to establish cross-product transfer. Controlled lighting remains a field-validity limitation.

### Two-dataset strategy — primary decision

**Use separate normal-only fitting, calibration and evaluation per recipe.** Share code and optionally a frozen feature extractor; never pool normal statistics, image-score thresholds or benchmark scores across these products. Selecting the recipe is explicit, not automatic product recognition.

- **Joint training:** excluded initially. Different products, aspect ratios and normal appearances do not justify a pooled normal distribution. Conditional multi-product learning would require a later protocol and evidence of value over separate models.
- **Cross-dataset generalisation:** not a pass criterion. Nut-trained scoring on KSDD2 largely tests product/domain mismatch, not useful transfer. Optional later negative-control experiment must retain source thresholds, use no target labels for adaptation and be labelled out-of-domain; avoid implying target defect recognition.
- **No subtype detector:** current task is binary anomaly flagging plus localisation, not YOLO class prediction. Existing masks support evaluating attention maps; they do not give the model reliable semantic causes.

## 3. Scope, journey and acceptance

### User and inspection contract

Line worker/supervisor reviews one declared component recipe, one surface/view, one product ID at a time. Full relevant surface visible, no major occlusion; no unverified side/size/lighting transfer. A limited quality gate checks basic image suitability, not defect visibility or product identity. The user confirms recipe/view; this is not automated verification.

### Complete MVP journey

1. Create batch and declare expected unique-product count; select a validated recipe/version.
2. Add product ID and upload a photograph (or disclosed benchmark demo image).
3. Gate accepts for scoring or requests retake with reason. An unsupported image never becomes “normal.”
4. Run native inference; show experimental anomaly score, threshold, flag and map with a fixed colour scale. Scores are not defect probabilities.
5. Human selects acceptable, defective, uncertain or rework required and records a note/category if known.
6. Reinspection creates a new attempt without overwriting history or double-counting the product.
7. Batch page shows expected, uploaded, model-assessed, human-reviewed, resolved, uncertain, rework and uninspected counts.
8. Export draft report with evidence, limits and owner acknowledgement. All expected products must be resolved before final acknowledgement in the MVP; partial reports remain drafts, rather than implying complete coverage.

### Provisional engineering screens

These are early stop/go targets, not buyer/industrial requirements or predicted performance. Apply **independently** to each recipe on the frozen test set.

| Measure | Provisional screen / rationale |
|---|---|
| All-defect flagging recall | ≥90%, counting abstained defects as not caught; prevents hiding misses by abstention |
| FPR among accepted normal images | ≤10%; also report false flags/all normals and counts |
| Model-assessed coverage | ≥90%; gate must not discard hard examples to improve metrics |
| CPU warm p95 | ≤5 s/image, batch 1 including decode/gate/preprocess/tiles/map/score; usable pilot response budget |
| Process peak RSS | ≤4 GiB during batch-1 inference on available machine; provisional local resource cap |
| Localisation assistance gate | ≥80% of scored anomalous images have peak map point inside ground-truth defect mask, plus qualitative failure review; provisional, can favour large regions |
| Record integrity | Zero failed identity/duplicate/rework/approval invariants in defined fixtures |
| Human utility | No savings claim until timed manual/assisted review; report both time and errors, not time alone |

Report AUROC/AP and localisation metrics regardless of screens. If image screens pass but localisation fails, offer image-level review only and label localisation experimental; do not quietly redefine a heatmap as validated segmentation. Small samples constrain conclusions: 22 test normals make a 10% FPR screen especially uncertain.

### Exclusions

Factory-wide 3D twin, automatic root causes, live machines/cameras, continuous line tracking, unattended acceptance, prediction on all components, functional/electrical testing, calibrated metrology, phone/browser compatibility claims, buyer certification and unmeasured defect-reduction/time-saving claims. No simulation engine in the critical path; optional map is observation-based only.

## 4. Data pipeline and locked protocols

### Immutable sources and common record

Archive and extraction roots are read-only by policy; generated derivatives have separate paths. Reject archive path traversal, escaping symlinks and excessive expansion. Record source URL, licence snapshot, archive/extracted hashes and tool version. Never execute downloaded scripts or deserialize foreign model pickle files.

`ImageRecord` in `src/tech4bharat/data/schema.py`:

```text
schema_version, record_id, dataset_id, release_hash, category_id,
relative_image_path, mask_path|null, image_sha256, decoded_sha256,
phash64, source_group_id|null, grouping_confidence,
official_split, experiment_split, label(0|1), defect_type|null,
width, height, provenance(real_capture|deliberately_defected_capture|synthetic|transformed),
parent_record_id|null, quarantine_reason|null
```

Adapter signatures: `read_mvtec(root: Path, category: str) -> list[ImageRecord]` and `read_ksdd2(root: Path) -> list[ImageRecord]`. Adapters retain original labels/splits; a separate split manifest assigns experiment roles. IDs are dataset/release/category scoped. Masks never enter inference inputs.

Check byte hash and decoded hash; create conservative near-duplicate candidates using pHash Hamming ≤2 and 64×64 RGB mean absolute difference ≤2/255, then record review decisions. These are appearance checks, not physical identity proof. Group physical IDs where supplied. Corrupt/missing/contradictory items are quarantined with reasons and counts, never silently removed.

### Primary protocol: official test held intact, normal-only calibration

For both datasets, reserve deterministic **20% of eligible official-training normal groups** for calibration, seed 4217. Remainder fits the model. Split groups, not rows; order group IDs by SHA256(seed + dataset + group ID). Assign whole groups until closest to 20%, record actual count. With unique images, expected MVTec split is 176 fit /44 normal calibration; KSDD2 approximately 1,668 fit /417 normal calibration. Counts are provisional until audit.

- Do not use any official-test image, mask or score for fitting, threshold selection, parameter selection, pose templates or gate calibration.
- MVTec has no training anomalies for validation in this protocol: accept the limitation and select thresholds using normal calibration only. Do not secretly carve labelled test anomalies into calibration.
- KSDD2's **246 official-training anomalies are development-only**, never normal-model fitting. Use their labels/masks for a limited predeclared model configuration comparison if needed; final normal calibration remains held out. This is a normal-only learning use of its split, not reproduction of the authors' supervised training benchmark.
- Official test audit may inspect file metadata/grouping to detect leakage, not model outputs. If a duplicate group spans official train/test, quarantine contaminated test items and report both published and cleaned counts. Do not claim unchanged official-protocol comparability.
- If no adequate normal calibration remains, stop. Do not borrow test images. Require more training-normal data or predeclare grouped cross-validation entirely inside official training. Small normal calibration cannot establish high-confidence FPR guarantees.
- No augmentation first run. If later justified, augment **fit originals only** and retain parent/group IDs. Never augment before splitting.
- Archive test predictions once after configuration, thresholds and code/config hashes are locked. Any later changes require a new independent holdout for deployment claims; test re-evaluation is exploratory, not fresh confirmation.

### Development configuration budget

Run the stated default baseline and PaDiM settings first. At most one additional crop/rotation configuration per method may be selected from training-only grouped development folds, using KSDD2 development anomalies where available. Metal-nut tuning without genuine development anomalies uses normal consistency only; label it as such, and do not invent defective-validation recall. Freeze final settings before evaluating either official test.

## 5. Models and preprocessing

### Simple baseline: nearest normal reference residual

Reuse the concept, not mutable imports tied to PCB1 globals, from `experiment/inspection.py`. Keep the historical experiment unchanged.

- Recipe preprocessing produces RGB [0,1] arrays and reversible geometry metadata; no per-image brightness-centering because it may suppress metal-nut colour anomalies.
- Compare against up to 128 deterministic fit-only references, evenly selected by sorted group hash if more exist. Pick minimum mean RGB squared residual; smooth map with Gaussian sigma 1 and score mean of top 1% valid pixels.
- Metal nuts: default in-plane rotation search at 10° increments, shared fixed rotation centre and fit-derived foreground ROI. Transform references only, exclude padded pixels, preserve original face; no reflection/flip augmentation. Cache reference rotations; chunk comparisons to cap memory. Record selected angle and mapping. This is an engineering baseline, not guaranteed useful alignment.
- KSDD2: no rotation/flip assumption. Use positional patch references and stitch residual maps. A registration failure requests review; never use the best score over arbitrary side flips.

### Established candidate: compact PaDiM / frozen ResNet18

[PaDiM](https://arxiv.org/abs/2011.08785) fits spatial Gaussian normal-feature distributions and supports anomaly maps. Choose it for native CPU feasibility and reuse of tested engineering, not novelty or promised accuracy.

- Pin torch 2.6.0+cpu / torchvision 0.21.0+cpu initially; frozen `resnet18(weights=ResNet18_Weights.IMAGENET1K_V1).eval()`, no gradient training. Record weight URL/checksum; cached local copy permitted. [Version-matched API](https://docs.pytorch.org/vision/0.21/models/generated/torchvision.models.resnet18.html).
- Extract `layer1/2/3`, upsample features to the same spatial grid, concatenate; deterministic 50-channel subset, covariance +0.01I, Mahalanobis map, sigma-4 smoothing. Save means/covariance factors, channel indices and all geometry. This is our compact configured implementation, not the authors' exact recipe.
- Replace hard-coded 56×56/224 assumptions in the historical concept with recipe-derived shapes; use batched Cholesky solves or equivalent stable covariance handling. Fail with a diagnostic on insufficient fit samples/nonfinite covariance rather than emitting a normal score.
- Start with batch 1 inference / four CPU threads. Fitting uses bounded batches, no whole-dataset feature tensor in RAM. Measure memory/time; GPU optimisation is optional only after verifying hardware separately.
- No centre crop: official classifier transforms include a crop, which may remove edge defects. Apply explicit resize/padding and ImageNet mean/std, and test consistency. [Transform behaviour](https://docs.pytorch.org/vision/0.21/models/generated/torchvision.models.resnet18.html); [feature-extraction API](https://docs.pytorch.org/vision/0.21/feature_extraction.html).

### Recipe geometry

- **Metal nut:** whole image aspect-preserving resize/letterbox to 256×256; exclude padding from score/metrics. No learned detector to find the product initially. PaDiM default uses original orientation; normal calibration must reveal alignment instability. Baseline's rotation search is explicit; report it as a method difference.
- **KSDD2:** preserve native aspect/detail; use 256×256 tiles with 64-pixel overlap, stride 192, pad only boundary tiles, and include a final anchored tile at the far edge. Stitch maps with overlap averaging excluding padding; compute image score from the stitched valid map, not per-tile labels. Freeze tile policy from training only.
- For KSDD2's fixed framing, fit a separate reference bank/Gaussian state per tile-position index within the recipe bundle; do not pool spatially different tile positions as interchangeable normals. Every fit image contributes at most one tile to each position. Assert identical expected image geometry, or return unsupported; adapting to new aspect ratios requires a new recipe. Image/group counts, rather than tile counts, remain the independent evaluation units.
- Restore maps to original image coordinates; resize masks with nearest-neighbour for evaluation, never image interpolation. Main pixel metrics use original-size maps/masks; report tile counts and full-image latency.
- Baseline and PaDiM use the same recipe geometry but different scoring. Do not claim source-paper benchmark equivalence.

### Calibration and artifacts

Image threshold per method/recipe uses only accepted normal calibration images: rank `k=ceil((n+1)*0.90)` in ascending score order; threshold the kth score and flag only scores strictly greater. If k>n, fail calibration. Report sample size, ties and empirical FPR; finite-sample uncertainty and non-exchangeability preclude a factory guarantee.

Quality gate: reject decode errors, minimum side <224, mean luma outside [0.05,0.95], clipped fraction >0.50 or 256-normalised Laplacian variance <20. These are inherited **provisional** checks, not verified phone suitability. Freeze before tests and measure rejection counts; no post-test gate tuning. No anomaly-score “confidence” abstention until separately calibrated.

Pixel threshold for descriptive IoU/Dice: 99.5th percentile of a deterministic maximum 10,000 valid map pixels per accepted normal calibration image, equally weighted per image. This is a pixel-level operating rule, not a defect-recall guarantee. Save exact sampling seed and threshold. Per-image min/max heatmap rescaling is forbidden for comparative severity; render using one calibration-derived display range, clipped with a labelled legend.

Artifact bundle: recipe ID/version, method/config, backbone checksum, fit/calibration manifest hashes, preprocessing version, thresholds, valid geometry, normalisation/display ranges, training code revision/content hash, dependency lock, timestamps, inference schema version and licence provenance. Load only trusted locally produced state dictionaries/NPZ arrays; never arbitrary uploaded weights.

**Alternative only after failure diagnosis:** PatchCore may address some spatial-normal variation, but its bank/search cost needs a CPU spike and a new protocol. It is not an unbounded model search after test failures. No YOLO/LLM API required.

## 6. Evaluation contract

- One row per method × recipe; never average raw anomaly scores across datasets.
- Report TP/FN/FP/TN, abstained normal/defective, accepted counts, all-defect recall, accepted-only recall/FPR, all-normal FPR, precision at **actual test prevalence**, coverage and retake counts. No division by zero: return null with reason.
- Image ranking: AUROC plus **average precision (AP)** as the chosen AUPRC summary; name it precisely, not trapezoidal PR area. Accepted-only ranking metrics include their coverage denominator; screens also count abstained defects as misses. [AUROC API](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html), [AP API](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html). Pin implementation version rather than relying on changing stable docs.
- Localisation: pixel AUROC/AP across valid original pixels, anomalous-image macro IoU/Dice at the frozen pixel threshold, normal-image falsely marked area, and peak-in-mask hit count. Record zero-mask/invalid-mask handling; skip invalid masks with explicit counts, do not fabricate zeros. Pixel metrics are diagnostic; background dominance can obscure poor small-defect localisation.
- Compute AUPRO to FPR 0.30 only as optional source-compatible extension; define connected components/interpolation and test the implementation before naming the metric. Do not substitute a homemade score under the official name.
- Per defect-family recall for metal nuts only after taxonomy verification. KSDD2 binary labels do not establish subtype recall.
- Macro summary = arithmetic mean of the two separately reported recipe metrics. Micro confusion sum is optional with pooled counts/prevalence disclosed; large KSDD2 must not hide metal-nut failure. Never pool raw-score AUROC.
- Wilson 95% intervals for recall/FPR/precision and image-group bootstrap 1,000 replicates for AUROC/AP if group IDs exist; otherwise image bootstrap with physical independence limitation. Never use pixels as independent subjects for confidence intervals. Tiny defect-family samples are descriptive.
- Measure cold init, fit time, warm batch-1 decode/gate/preprocess/inference/stitch latency median/p95, end-to-end API latency, peak RSS and artifact bytes. Ten warmups on development images; time every final-test item once in fixed seeded order. Give sample sizes, thread count and hardware; retakes separately.
- Synthetic robustness: brightness ×0.6 /×1.4 and Gaussian blur radius 2 on test copies after base evaluation. Label transformed, keep parent/group IDs, unchanged thresholds; report paired changes, not extra independent products. Do not retrain from stress-test failures and reuse the same holdout as untouched.
- Review false negatives, false positives, pose/crop/lighting failures and large/small defect regions. Publish failure gallery and unfiltered prediction tables.
- Scenario precision at hypothetical prevalence p may be calculated from recall/FPR, explicitly assuming unchanged performance; never call it measured factory precision.
- Human exercise: build a new counterbalanced manual/assisted pilot with disjoint matched images and recorded item IDs, time and errors; disclose convenience sample, no expert truth and benchmark prevalence. Existing PCB exercise cannot validate nut assistance. No contact or fabricated feedback.

## 7. Application architecture and interfaces

### Modules and files to create later

```text
configs/{mvtec_metal_nut,ksdd2_surface}.yaml
configs/experiment_protocol.yaml
pyproject.toml / requirements-cpu.lock
src/tech4bharat/
  cli.py
  data/{schema,acquire,adapters,audit,splits}.py
  vision/{preprocess,gate,reference,features,padim,artifacts}.py
  evaluation/{calibration,metrics,benchmark,stress,report}.py
  service/{contracts,registry,inference,api}.py
  workflow/{store,ledger,export}.py
web/{package.json,package-lock.json,src/...}
tests/{test_data,test_geometry,test_models,test_calibration,test_metrics,
       test_api,test_ledger,test_exports}.py
tests/fixtures/                         # tiny explicit software fixtures
data/{archives,raw,derived,manifests}/   # ignored; immutable raw
runs/<run_id>/{protocol,metrics,predictions,failures,environment}.*
models/<recipe>/<version>/              # ignored trusted artifacts
outputs/{reports,demo}/                 # generated user deliverables
docs/{DATA_SOURCES,MODEL_CARDS,DEMO}.md
```

Do not edit `experiment/` outputs or its frozen protocol. Reuse proven logic by extracting/copying with tests into the new namespace, not importing hard-coded PCB paths. Existing Markdown documents remain context, not live configuration.

### Typed contracts

```text
preprocess(image: PIL.Image, recipe: RecipeConfig) -> PreparedImage
PreparedImage = {tiles, valid_masks, geometry, original_size}
fit(records: list[ImageRecord], config: RecipeConfig) -> ArtifactBundle
predict(image: PIL.Image, bundle: ArtifactBundle) -> Prediction
Prediction = {status: scored|retake|unsupported, reasons: list[str],
 score: float|null, threshold: float, flagged: bool|null,
 map_original: float[H,W]|null, recipe_id, model_version,
 preprocess_version, timings_ms}
calibrate(normal_scores: list[float], target_fpr: float) -> ThresholdRecord
evaluate(rows: list[EvaluationRow]) -> MetricsReport
```

Pydantic contracts validate API responses; Python types above are design interfaces, not implemented classes. CPU inference runs under a bounded worker/semaphore, not blocking an async event loop with unlimited requests. Use SQLite transactions and unique indexes for local identities; no PostgreSQL or cloud account needed.

| API | Contract / behaviour |
|---|---|
| `GET /api/recipes` | List loaded recipe/version and validation status; omit model file paths |
| `POST /api/batches` | JSON `{batch_id, recipe_id, expected_product_ids}`; unique IDs, max 1,000 products |
| `POST /api/inspections` | Multipart `batch_id`, `product_id`, `recipe_id`, `Idempotency-Key`, `image`; 202 with `inspection_id` and status URL after validated acceptance |
| `GET /api/inspections/{id}` | `queued|running|scored|retake|failed` plus prediction fields and evidence URL; no fabricated human disposition |
| `GET /api/inspections/{id}/heatmap` | Authorised PNG overlay only; underlying float map retained locally for evaluation |
| `POST /api/inspections/{id}/decision` | `{decision: acceptable|defective|uncertain|rework_required, note, observed_defect|null, reviewer}`; append event |
| `GET /api/batches/{id}` | Unique-product counts, latest status, complete event history, observed denominator |
| `POST /api/batches/{id}/acknowledgement` | Owner role and all expected products resolved; demo role is not verified legal signature |
| `GET /api/batches/{id}/report?format=html|csv` | Draft/acknowledged status, coverage and provenance; CSV injection escaped |

Errors: 413 oversized bytes, 415 unsupported media, 422 invalid decode/IDs, 409 recipe conflict/cross-product photo reuse/pending acknowledgement, 503 missing artifact/queue capacity. Same idempotency key + same payload returns same inspection; changed payload returns 409.

### Storage and workflow rules

- Local uploads outside web public root, random server paths; preserve content hash, strip metadata in display derivatives, never concatenate client filenames into paths.
- Maximum upload 10 MiB, decoded maximum 20 megapixels, allow JPEG/PNG only, reject animated/multipage files and decompression bombs. Reject unauthorised requests before decoding.
- Same photo + same product returns existing attempt unless an explicit new attempt references a genuine new capture; same photo + different product blocks pending review. A hash is not proof of a physical item.
- Distinguish model-assessed from human-reviewed. A retake/failed attempt is not completed inspection; uncertain/rework remains unresolved. Current disposition is latest resolved state only when no newer unresolved attempt exists.
- Acknowledgement records a snapshot hash; new decision/rework invalidates acknowledgement and returns batch to draft. Historical signatures/decisions are retained.
- Optional 2D observation map groups records by declared station; show inspected and unknown counts separately. A high observed defect rate shows numerator/window/sample size, never automatic station cause attribution.

## 8. Ordered build tasks

All steps below are **future work**. Commands use the proposed CLI and must be verified when implemented. Each task ends with a reviewable deliverable; commit only if a Git repository is present and the task's relevant checks pass.

### Task 1 — Freeze source access, scope and environment

**Purpose/dependencies:** unblock data, licence and CPU execution; no earlier task required. **Files:** create `configs/*.yaml`, `pyproject.toml`, `requirements-cpu.lock`, `docs/DATA_SOURCES.md`, `src/tech4bharat/cli.py`, `data/acquisition.json`. **Interfaces:** `acquire(source_id: str, destination: Path) -> AcquisitionRecord` in `data/acquire.py`; consumes provider archive/manual path, produces hash/size/licence/version record.

- [ ] Confirm the proposed pair, defect semantics, research-demo permission and organiser dates/eligibility; record unresolved items explicitly.
- [ ] Implement manifest/source validation tests: missing licence/source/hash blocks adoption; archive extraction cannot escape destination.
- [ ] Create a new environment using the existing CPU pair; do not modify the historical `.venv`. Install API/frontend dependencies only during later implementation, then lock verified versions. No latest-version guess in a lockfile.
- [ ] Acquire provider samples/archives through permitted download workflow; inspect real files, record bytes/checksums and available RAM/disk. No bypass of access forms.
- [ ] Run `python -m tech4bharat.cli doctor` and `pytest tests/test_data.py -k acquisition -v`; require import/version/CPU/model-weight checks and safe extraction tests to pass.

**Completion/deliverable:** reproducible environment/source ledger and small readable sample per dataset. **Effort:** 2–4 hours hands-on; access/form turnaround and full archive size unpredictable. **Stop:** inaccessible data or unresolved use permission; do not silently substitute a mirror or different dataset.

### Task 2 — Adapters, audit and immutable splits

**Depends:** 1. **Files:** `data/{schema,adapters,audit,splits}.py`, `tests/test_data.py`, manifests. **Interfaces:** adapter signatures in section 4; `audit(records) -> AuditReport`; `make_splits(records, seed=4217) -> SplitManifest`.

- [ ] Write fixtures asserting mask pairing, normal zero-mask semantics, missing defective mask quarantine, duplicate grouping and whole-group splits.
- [ ] Run those tests and confirm expected failures before implementing adapters.
- [ ] Implement adapters and inventory actual counts/taxonomy/dimensions; retain official split, all rejected records and grouping uncertainty.
- [ ] Implement deterministic split policy; assert no fit/calibration/test group overlap and no transforms in raw originals. Detect cross-official-split collisions and quarantine per protocol.
- [ ] Run `python -m tech4bharat.cli prepare --config configs/experiment_protocol.yaml` and `pytest tests/test_data.py -v`; manually review audit table, lock manifests before inference.

**Completion/deliverable:** `data/manifests/{inventory,audit,splits}.json`, label examples and frozen protocol. **Effort:** 3–5 h; uncertainty is dataset schema/physical identifiers.

### Task 3 — Geometry, quality gate and reference baseline

**Depends:** 2. **Files:** `vision/{preprocess,gate,reference}.py`, `tests/test_geometry.py`, `tests/test_models.py`. **Interfaces:** `preprocess(...) -> PreparedImage`, `gate(...) -> GateResult`, `Reference.fit(...)`, `Reference.predict(...) -> Prediction`.

- [ ] Write tests for RGB/grayscale/EXIF handling, full-frame edge preservation, tile cover/no gaps, reversible overlay geometry and ignored padding.
- [ ] Write tests that synthetic known-angle rotation maps back correctly, no reflection is allowed, and failed alignment cannot emit an acceptable disposition.
- [ ] Implement baseline and fixed geometry/gate policies; store raw-unit maps/scores and diagnostic registration failures.
- [ ] Run `pytest tests/test_geometry.py tests/test_models.py -k 'geometry or reference or gate' -v`; exact fixtures check map coordinates, finite outputs and padding exclusion.
- [ ] Fit/infer development-only images via `python -m tech4bharat.cli develop --method reference --recipe mvtec_metal_nut`; record time/memory without opening test predictions.

**Completion/deliverable:** genuine baseline predictions and map in original coordinates on development images. **Effort:** 4–7 h; rotation search cost and foreground ROI are principal uncertainties.

### Task 4 — Native PaDiM and trusted artifacts

**Depends:** 2–3. **Files:** `vision/{features,padim,artifacts}.py`, `tests/test_models.py`. **Interfaces:** `Padim.fit(records, config) -> ArtifactBundle`; common `predict` contract.

- [ ] Write tests for trusted save/load parity, nonfinite features/covariance failure, category mismatch, fit-only record access and deterministic channel indices.
- [ ] Implement frozen feature extractor with version-matched API and dynamic recipe geometry, bounded feature-statistic fitting and valid-pixel map restoration.
- [ ] Fit each recipe independently using eligible normal-fit groups only. Save model card, hashes, thresholds initially unset, and development timing/RSS.
- [ ] Run `pytest tests/test_models.py -v`; same bundle/input must reproduce score within `atol=1e-5, rtol=1e-5` and identical flags once calibrated. No required discrimination success on synthetic toy defects.
- [ ] Run development sanity comparisons: normal distribution, tile boundary artefacts and rotation-sensitive normal examples. Freeze the bounded configuration before test use.

**Completion/deliverable:** two trusted native model bundles, no test evaluation yet. **Effort:** 4–7 h; numerical stability, tiling and normal variation may require a scoped stop/replan.

### Task 5 — Calibration and early end-to-end milestone

**Depends:** 3–4. **Files:** `evaluation/calibration.py`, `service/{contracts,registry,inference,api}.py`, `workflow/{store,ledger}.py`, minimal `web/src/Review.tsx`, `tests/test_calibration.py`, `tests/test_api.py`.

**Interfaces:** `calibrate(...) -> ThresholdRecord`; `Registry.load(recipe_id, version) -> ArtifactBundle`; `InferenceService.inspect(image_bytes, recipe_id) -> Prediction`; `Ledger.record_decision(inspection_id, decision) -> DecisionEvent`.

- [ ] Write calibration tests: only calibration IDs accepted; quantile index/ties correct; too few normals/nonfinite scores fail; final-test path forbidden.
- [ ] Score calibration normals once, freeze image/pixel/display thresholds and hashes separately for method/recipe; record gate coverage.
- [ ] Implement one-image API and minimal human decision page using the defined contracts, local SQLite transaction and status polling.
- [ ] Run a **development image → real native inference → score/map → human decision → saved record → reload**. The person makes the decision; no simulated human acceptance hidden in the milestone.
- [ ] Run `pytest tests/test_calibration.py tests/test_api.py -v` and frontend type/build checks. Verify missing model/recipe mismatch blocks inference.

**Completion/deliverable:** first working end-to-end local milestone, explicitly experimental and not benchmark-approved. **Effort:** 5–8 h; dependencies/schema integration are main uncertainty. Do this before polishing the full UI.

### Task 6 — Frozen independent evaluation and gate decision

**Depends:** 5 and signed-off protocol/config freeze. **Files:** `evaluation/{metrics,benchmark,stress,report}.py`, `tests/test_metrics.py`, `runs/<run_id>/...`.

**Interfaces:** `benchmark(bundle, manifest, split='test') -> list[EvaluationRow]`; `evaluate(rows) -> MetricsReport`; `write_report(...) -> Path`.

- [ ] Write tests with hand-computable confusion counts, abstentions, one-class/empty data, AP/AUROC input errors, zero masks, map shape and no pooled-score aggregation.
- [ ] Validate metric implementations against pinned scikit-learn on fixed fixtures; preserve original-coordinate masks/maps and per-image IDs.
- [ ] Lock code/config/artifact hashes, then evaluate each method/recipe once on the official test partition; save complete predictions and untouched-base results before stress tests.
- [ ] Generate per-type/count/interval tables, timing/RSS/artifact sizes and failure gallery; evaluate transformed stress copies separately.
- [ ] Run `pytest tests/test_metrics.py -v`; review pass/fail per recipe. Record honest no-go if neither method meets screens; do not tune and rebrand this holdout as new.

**Completion/deliverable:** reproducible results and gate decision; only passing recipe(s) may enter “validated benchmark recipe” UI. **Effort:** 4–6 h hands-on; compute/runtime unknown until Tasks 3–4. If neither passes, stop product integration and deliver the research result.

### Task 7 — Harden inference and upload contract

**Depends:** 6 passing recipe or explicit decision to retain only research demo. **Files:** service modules, `tests/test_api.py`, upload storage. **Interfaces:** full API table in section 7.

- [ ] Write API tests for >10 MiB payload, >20 MP decoded image, invalid JPEG/PNG, animated/multipage media, path-like IDs, unsupported category and missing/stale artifact hash.
- [ ] Implement bounded queue/concurrency 1, transaction-backed request status/idempotency and upload limits before inference. Do not assume async makes CPU work parallel safely.
- [ ] Enforce local authentication/session for demo roles; same-origin requests, no wildcard authenticated CORS. Bind localhost by default.
- [ ] Test queued/running/scored/retake/failed states; 503 returns no invented prediction, restart cannot mark incomplete jobs acceptable.
- [ ] Run `pytest tests/test_api.py -v`; record API latency separately from model time using development uploads.

**Completion/deliverable:** bounded, testable native service and explicit failure contract. **Effort:** 4–6 h; public deployment would add security work beyond this local baseline.

### Task 8 — Batch ledger, full review UI and exports

**Depends:** 7. **Files:** workflow modules, `web/src/{Batch,Review,Report}.tsx`, `tests/{test_ledger,test_exports}.py`. **Interfaces:** API decision/batch/acknowledgement/export contracts.

- [ ] Write fixture assertions: six products; duplicate same-product upload no count increase; cross-product reuse blocked; new rework attempt pending invalidates resolved status; incomplete batch cannot acknowledge.
- [ ] Implement append-only history, unique-product counts and snapshot acknowledgement invalidation in transactions. Never use photo count as coverage.
- [ ] Build human confirmation, recipe/version display, fixed-scale overlay, retake/uncertain flow and batch summary. Optional observation map only after these work.
- [ ] Generate HTML/CSV from the same ledger snapshot; escape HTML and spreadsheet formulas, preserve provenance, threshold/version and partial coverage. No certificate wording.
- [ ] Run `pytest tests/test_ledger.py tests/test_exports.py -v`, `npm --prefix web run typecheck`, `npm --prefix web run build`; compare report/API/UI counts on the fictional fixture and complete one actual manual review.

**Completion/deliverable:** complete local MVP journey and truthful sample report. **Effort:** 6–10 h; review usability and report design may need iteration.

### Task 9 — Optional export/browser parity

**Depends:** 6, 8; optional, cut first if schedule tight. **Files:** `vision/export.py`, `web/src/browser/`, `tests/test_export_parity.py`.

**Interfaces:** `export_bundle(bundle, target='onnx') -> ExportRecord`; browser must return the same Prediction schema.

- [ ] Export only after native gates; save opset/runtime versions, bytes and content hash. Include preprocessing/normalisation or define an exact shared contract.
- [ ] Test native/ONNX same tensors then independent raw-image decode/resize/tiling/score/map on calibration fixtures and explicit boundary-score fixtures; compare restored map geometry and frozen decisions.
- [ ] Require score/map tolerances `atol=1e-4, rtol=1e-4`; investigate every decision difference rather than adjusting thresholds to hide export drift.
- [ ] Test actual laptop browser load, network/model size, cold/warm latency, memory failure and runtime asset paths. Full browser test-set accuracy comparison is required before replacing native serving.
- [ ] Record failures and fallback. No phone claim until an actual identified phone/browser test exists; no guaranteed speedup or quantisation gain.

**Completion/deliverable:** parity/feasibility report, not mandatory browser deployment. **Effort:** 4–8 h; conversion/WASM/platform issues can exceed timebox. [ONNX Runtime Web primary guide](https://onnxruntime.ai/docs/get-started/with-javascript/web.html).

### Task 10 — Human pilot, deployment packaging and handoff

**Depends:** 8; 9 only if browser is selected. **Files:** `docs/{DEMO,MODEL_CARDS}.md`, `outputs/demo/`, feedback materials, deployment config and reproducibility README.

**Interfaces:** package consumes frozen recipe/report artifacts; no new model tuning.

- [ ] Prepare at least 24 disjoint benchmark review items, balanced and counterbalanced by participant/order where feasible. Record manual/assisted timing, decisions and help requests; disclose artificial prevalence and unmatched difficulty. Never complete it on the user's behalf.
- [ ] Audit current hosting terms, memory/disk/request limits, sleep behaviour and model-file limits for a free target. No account or always-on capacity assumed; stop before paid usage.
- [ ] Package local native demo plus a deployable static frontend using **labelled precomputed benchmark predictions** if free live inference is unavailable. Disable unsupported live uploads in replay mode; human review must be clearly demo/local storage with no shared durability claim.
- [ ] Test clean setup, restart persistence, report download, stale-model handling and offline fallback. Run full relevant backend tests/typecheck/build once; repeat only for new changes/failures.
- [ ] Record actual measurements, limitations, source attributions and unactioned gaps; final user-facing go/conditional/no-go with a link to deploy/local instructions. No automatic external outreach.

**Completion/deliverable:** reproducible demo, honest deployment mode, sample report and pilot results if participant completed it. **Effort:** 4–7 h plus participant/hosting delays. User feedback may reveal a no-go even if benchmarks pass.

## 9. Reproducible command contract — future, not executed

The following specifies CLI behaviour to implement, not commands that already work. Source acquisition may require a provider's manual form. Run from project root in the new environment after installation (`pip install -e .`); freeze the successful dependency resolution.

```powershell
python -m tech4bharat.cli doctor
python -m tech4bharat.cli acquire --dataset mvtec_ad --category metal_nut
python -m tech4bharat.cli acquire --dataset ksdd2
python -m tech4bharat.cli prepare --config configs/experiment_protocol.yaml
python -m tech4bharat.cli develop --method reference --recipe mvtec_metal_nut
python -m tech4bharat.cli fit --method padim --recipe mvtec_metal_nut
python -m tech4bharat.cli fit --method reference --recipe mvtec_metal_nut
python -m tech4bharat.cli fit --method padim --recipe ksdd2_surface
python -m tech4bharat.cli fit --method reference --recipe ksdd2_surface
python -m tech4bharat.cli calibrate --config configs/experiment_protocol.yaml
python -m tech4bharat.cli freeze --config configs/experiment_protocol.yaml
python -m tech4bharat.cli evaluate --frozen-run RUN_ID
python -m tech4bharat.cli stress --frozen-run RUN_ID
python -m tech4bharat.cli report --run RUN_ID
python -m pytest tests -q
python -m tech4bharat.cli serve --host 127.0.0.1 --port 8766
npm --prefix web ci
npm --prefix web run typecheck
npm --prefix web run build
```

`freeze` must reject missing artifact/split/calibration hashes; `evaluate` must reject mutable/unfrozen configs. Existing `experiment/serve.py` uses port 8765, so use 8766 for the new service. No project scaffold or installation occurs while writing this plan.

### Environment and resource budget

- Start a new `.venv-components`; reuse compatible pinned CPU package versions, not the previous results directory. Add exact tested FastAPI/Pydantic/test/frontend versions during implementation; generate a lock rather than inventing current compatible version pins.
- Weight download is roughly 45 MB according to the torchvision documentation; actual bytes/checksum recorded on acquisition. [ResNet18 docs](https://docs.pytorch.org/vision/0.21/models/generated/torchvision.models.resnet18.html).
- Reserve **10 GiB free disk** for possible full archives, dependencies, extracted data and runs; not a measured requirement. Check archive/expansion estimates before download. Fit memory depends on patch grid/channels, so stream statistics and measure peak RSS.
- Seeds, CPU threads, BLAS/Torch versions and hardware logged per run; deterministic seeds do not guarantee bit-identical results across platforms.
- Native public hosting, browser file-size feasibility and installed GPU readiness remain unresolved measurements, not prerequisites disguised as facts.

## 10. Schedule, critical path and cuts

**Hands-on planning budget:** Tasks 1–10 excluding optional 9 total **36–60 hours**, approximately 6–10 focused six-hour days. This is a new plan allocation, **not a validated delivery forecast**, and excludes access delays, failures, user availability and major model rework. Re-estimate after Task 5; the previous PCB-based full-MVP estimate remains withdrawn. Optional browser work adds 4–8 h. Neither dataset has performance measurements here.

| Milestone | Target relative to execution start | Retained hackathon constraint |
|---|---|---|
| Sources/eligibility/scope and data freeze | Days 1–2 | Resolve before relying on registration 10 Nov |
| One-image end-to-end milestone | Days 3–5 | Aim to demonstrate genuine inference before idea submission 15 Nov |
| Frozen two-recipe evaluation | Days 5–6 | Keep failed/limited results in idea narrative |
| Review/report/local demo | Days 7–10, only if gate permits | Leave substantial buffer before prototype 15 Dec |
| Rehearsal/deployment verification | Before prototype deadline; date rechecked | Freeze reproducible artifacts before finale 27 Dec |

Dates are conversation-derived milestones pending organiser verification, not commitments to work on a calendar without a start date. Team availability is unknown. No automation/scheduled work is created by this plan.

**Critical path:** access/licence → audit/split → native models → normal calibration → first real review → frozen evaluation → go/no-go → robust batch/report → deployment mode. Frontend polish cannot resolve a failed detector gate.

**Must have:** dataset provenance/splits, two separately evaluated methods/recipes, actual inference, human decision, honest counts/report, failure analysis and reproducible setup. If one recipe fails, deploy only the passing recipe and disclose the failed second benchmark; do not present two supported products.

**Cut order:** browser export, observation map, synthetic stress visual polish (retain basic separate stress metrics), optional AUPRO, additional defect subtype UI, GPU optimisation. Never cut leakage checks, independent test evaluation, source disclosure, human confirmation or accurate coverage.

## 11. Risks, decision gates and what changes the verdict

| Risk | Evidence/uncertainty | Response / gate |
|---|---|---|
| Metal nuts still difficult | Random rotations and normal surface variation documented | Test development alignment/normal stability; no promised accuracy; switch task only under new frozen protocol |
| Small calibration/test normals | Expected metal-nut calibration 44, test 22 | Report counts/intervals; normal quantile not a field guarantee; no hidden test tuning |
| KSDD2 context unclear | Surface images are not automatically a named metal component | Verify release context; use neutral recipe name, or reconsider its domain fit |
| Thin scratches lost | Resize/tiling may hide small signals | Preserve aspect/details, edge coverage and original-coordinate evaluation; training-only resolution decision |
| Data identity unknown | No guaranteed physical IDs | Group available sources/duplicates; report remaining physical leakage uncertainty |
| Quality gate admits bad images | Earlier PCB gate did not reject transformations | Explicitly limited gate; real capture study needed; retake/unsupported never acceptable |
| Model fails screens | Prior PCB configuration failed | Stop at Task 6; do not hide failures with a factory animation |
| Research-only terms | Both proposed datasets non-commercial | Research demo only until permitted; use own licensed factory data for later commercial work |
| Free service cannot host inference | Model/RAM/download limits unknown | Local native demo; disclosed static replay; no paid fallback without asking |
| Human workload worsens | Capture/review time unmeasured | Pilot times and errors; avoid skipping unflagged products |
| No customer demand | No manufacturer/buyer access | Feedback exercise when contacts exist; compare current practice and extra steps; no invented adoption |
| Deadline/eligibility wrong | Source conflict, current official page not verified | Confirm before submission; exact rubric/eligibility can change entry strategy |

### Gate decisions

- **G0, Task 1:** confirm pair/access/use and eligibility. If blocked, save the blocker; do not start a large replacement training exercise without updating the plan.
- **G1, Task 5:** real inference-to-decision persistence works on a development image and resource use is practical. This is engineering feasibility, not accuracy approval.
- **G2, Task 6:** independently assess every recipe against section 3 screens, uncertainty and failures. Go for a limited benchmark demonstrator only for passing recipes; otherwise no-go on reliable inspection claims.
- **G3, Task 10:** user completes pilot and reports acceptable error/workload trade-offs; no strong claim from a small convenience exercise. Field usefulness still requires representative capture and user evidence.
- **G4, deployment:** verified free packaging and licensed data display. If unavailable, explicitly local/replay demonstration, not claimed live deployed inspection.

**Strongest evidence against building a full application now:** prior actual detection failed, both new tasks remain untested, and user benefit/demand are unknown. **Evidence that could change the verdict:** clean independent results, meaningful human pilot, representative capture validation and actual manufacturer/buyer feedback.

## 12. Open decisions for the user

1. **Dataset pair:** proposed MVTec `metal_nut` + KSDD2, separate recipes; alternatives remain in [components shortlist](COMPONENT_DATASETS.md). No need to choose a new model family before seeing native results.
2. **Deployment requirement:** is a research-only static replay plus a working local live-inference demo acceptable if no free inference host fits? The plan assumes yes as fallback; it does not equate that with live cloud inference.
3. **Operational product:** metal nuts are the proposed first product. KSDD2 is a second benchmark until its exact physical product/context is verified, not a second factory line.

Unknown organiser rules and later dataset access are Task 1 checks, not unanswered questions that prevent saving this plan. Implementation starts only after the plan is reviewed and explicitly requested. Native execution is the default recommendation; no subagents were used to create this document.

## 13. Verification and skill notes

- Skills actually used: **brainstorming** to consolidate the chosen narrow direction and assumptions; **senior-computer-vision** for task/geometry/model/deployment review; **writing-plans** for file/interface/task decomposition; **literature-review** for primary-source selection and uncertainty; **fastapi** for API-boundary guidance. Generic skill benchmark numbers, hardware claims and augmentation-before-split examples were not adopted; this project's evidence and leakage rules take precedence.
- Primary technical references were checked on 17 October 2026. Version-matched torchvision 0.21 APIs support the existing compatible CPU environment; a newer stable documentation page is not a reason to upgrade mid-experiment.
- Method acknowledgement: Kassis, T., Agarwal, V., He, Y., Patel, D., and Brueckner, A. M. (2026), [Scientific Agent Skills](https://doi.org/10.48550/arXiv.2609.00065), a workflow reference, not model-performance evidence.
- Plan self-review: data/task scope mapped to Tasks 1–2; baseline/geometry to 3; candidate/artifacts to 4; calibration and first end-to-end milestone to 5; metrics/gates to 6; API/security to 7; human/ledger/exports to 8; optional parity to 9; pilot/deployment/handoff to 10. Review-focus cases have owning tests. Commands remain future contracts, not reported successes.
