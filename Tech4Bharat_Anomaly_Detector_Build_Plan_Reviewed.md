# Tech4Bharat Component Inspection Assistant — Reviewed Build Plan

> **For execution:** use the installed `executing-plans` skill for native task-by-task work; delegation requires explicit user selection. **Status: audit and planning only. Do not implement from this request.** Checkboxes below describe future work, not completed tests.

**Review date:** 17 October 2026. **Verdict:** conditional go for a bounded two-dataset native experiment; dependent application work remains conditional. No-go for production, automatic acceptance or a validated factory digital twin.

**Goal:** determine whether one simple reference baseline or an established anomaly model can usefully flag visible component anomalies, then build a minimal human-reviewed inspection record only for recipes with adequate evidence.

**Architecture:** explicit dataset adapters and locked manifests → separate per-recipe models and calibration → native CPU evaluation → one-image review → truthful batch ledger/report. No pooled normal distribution, factory simulation engine or mandatory browser inference.

**Stack:** Python 3.12; maintained Anomalib PaDiM as the first integration candidate in a new environment; bounded fallback to the existing native implementation; React/TypeScript and a small FastAPI/SQLite service only after experiment gates. New package compatibility is a test, not an established fact.

**Read alongside:** [original plan, preserved unchanged](Tech4Bharat_Anomaly_Detector_Build_Plan.md), [local experiment evidence](experiment/artifacts/EXPERIMENT_REPORT.md), [components catalogue](COMPONENT_DATASETS.md).

**Original SHA256 at review start:** `C60A218016F40E8C245C814D56AB567D9DAE830E09DAB640C5EA9F4D61679EA3`.

## 1. Consequential changes

| Original decision | Reviewed decision | Why |
|---|---|---|
| Metal nuts proposed as the simpler-looking next task, with difficulty already caveated | Retain the narrow task but make the diagnostic experiment the immediate deliverable | Rotation and normal surface variation are documented; do not promise easier accuracy |
| 128 references ×36 cached rotations | 16 unrotated full-frame references, chunked comparisons | Old float32 reference cache alone is about 3.4 GiB; not a cheap baseline |
| Write dynamic, streaming PaDiM and per-position tile models immediately | First spike a maintained implementation; cap fit bank, use full-frame rectangular input | Reduces custom numerical, tiling and registration work before usefulness is known |
| Keep previous torch 2.6/torchvision 0.21 while considering new libraries | New isolated environment for current Anomalib; preserve old experiment | Anomalib 2.7 raises the minimums to torch 2.10 /torchvision 0.25 |
| Generic validation/calibration wording | Explicit fit/development/calibration/test roles and path-access assertions | Library defaults may validate using test data; normal-only validation cannot measure defect recall |
| Arbitrary focus/exposure gate requests retakes | Hard technical rejection; soft quality warnings initially | Earlier focus/exposure gate did not establish suitability; no silent filtering of benchmark failures |
| Localisation peak-hit ≥80% as acceptance | Diagnostic only; no validated segmentation claim | Large masks can pass the peak test despite poor region localisation |
| Build API/review before final feasibility result | Native resource/data spike first; tiny review milestone next, full app after results | Avoid a substantial UI around an inadequate detector |
| Async queue/polling and per-role auth immediately | Single synchronous bounded inference service for local demo | Less state/restart complexity; public identity/access is a separate deployment gate |
| Possible free compute hosting left vague | Local live inference plus explicitly labelled deployed static replay is the default fallback | No verified zero-budget live backend; current hosting documentation contains plan restrictions |
| 36–60 h full plan budget | 12–20 h initial experiment budget; 30–50 h conditional application budget | Previous estimate underweighted access, geometry, numerical and deployment uncertainty |

## 2. Recovered constraints and scope

- One Codex-assisted builder; TypeScript frontend preference. Additional teammate time/ML skills are unknown.
- No paid usage or added hardware. No factory access, representative phone captures, manufacturer/buyer contacts or expert labels assumed.
- Previous CPU experiment recorded Ryzen 7 260, 8 physical/16 logical cores and Python 3.12.14. A GPU was detected, but usable GPU training is untested and not required.
- Retained conversation dates: registration **10 November**, idea **15 November**, prototype **15 December**, finale **27 December 2026**. Current [organiser page](https://hackculture.io/hackathons/tech4bharat-gavs-hackathon) could not be fetched during this review. Dates and team/student eligibility remain unverified, not a reliable current submission checklist.
- First user: worker/supervisor reviewing one declared component/view; owner acknowledges the record. No existing customer demand or willingness to use the report is established.
- First operational candidate: one metal-nut benchmark recipe. KSDD2 is a second surface-inspection benchmark, not a second nut design or factory line.
- Must deliver two datasets in the research experiment; need not expose both as operationally supported products if one fails.

**Prior actual evidence:** reference matching detected 15/80 VisA PCB1 anomalies with 1/100 normal false flags; compact PaDiM detected 45/80 with 15/100 false flags. Both failed. New recipes, library integration and performance have **not** been tested here. [Saved report](experiment/artifacts/EXPERIMENT_REPORT.md).

### Supported task and user journey

Detect **image-level visual anomaly**, optionally locate suspicious regions. Output `flagged`, `not_flagged` or `not_scored`; none means human acceptance. A selected recipe is required; automatic product identity checking is absent.

1. Select a recipe/version; create a batch with expected product IDs.
2. Upload one image of the required face/view for a product ID; confirm view/recipe manually.
3. Reject technically invalid media, or score it and show any quality warnings.
4. Display raw anomaly score/threshold, model flag and optional fixed-scale attention map.
5. Human records acceptable/defective/uncertain/rework required. Semantic defect labels, if entered, are human observations, not model-class predictions.
6. A new capture/rework retains prior history and reopens resolution. Duplicates do not create extra products.
7. Export a draft report with actual model coverage, human review, unresolved/uninspected items and evidence versions.
8. Owner acknowledgement covers the snapshot and its declared coverage. In the minimal demo, partial records remain draft; new events invalidate acknowledgement. Demo identity is not a verified legal signature.

**Exclusions:** automatic root cause, live machines/cameras, 3D factory/twin, process-control advice, calibrated dimensions, electrical function, hidden defects, generic component support, unattended acceptance, buyer certification, time-saving claims without a participant test. No observation map until the core journey works.

## 3. Evidence ledger

Status means **Verified** in a source/local artifact, **Partially supported** with a material qualification, **Contradicted** by code/documentation/calculation, or **Unverified** on our setup. A documented capability is not a measured local outcome.

The ledger tests both implementation assumptions and tempting overclaims. Several overclaims were **already rejected in the original plan** (commercial permission, score probabilities, joint-product normality, industrial readiness and unique demand). Their “Contradicted” status does not mean the original endorsed them; the substantive corrections are identified in the change log.

| ID | Decision-critical claim | Status and evidence type | Consequence / next check |
|---|---|---|---|
| E01 | Metal nuts are necessarily easier than PCB1 | **Partially supported** only as a narrower visual task; paper documents random rotation/normal surface variation [MVTec paper](https://www.mvtec.com/fileadmin/Redaktion/mvtec.com/05_research_teaching/datasets/mvtec_ad.pdf) | Run bounded experiment; no expected accuracy |
| E02 | Metal-nut published split is 220 train-normal, 22 test-normal, 93 test-anomalous | **Verified**, original paper Table 1, not downloaded files [paper](https://www.mvtec.com/fileadmin/Redaktion/mvtec.com/05_research_teaching/datasets/mvtec_ad.pdf) | Reconcile actual release before freezing |
| E03 | KSDD2 split is 2,085/246 normal/anomalous train, 894/110 test | **Verified**, provider [ViCoS](https://www.vicos.si/resources/kolektorsdd2/) | Audit masks/source IDs; not tested locally |
| E04 | Either dataset freely permits a commercial application | **Contradicted**, both specify CC BY-NC-SA 4.0 [MVTec terms](https://www.mvtec.com/research-teaching/datasets/mvtec-ad), [ViCoS terms](https://www.vicos.si/resources/kolektorsdd2/) | Research/demo scope, check event/display terms; clear or replace data before commercial use |
| E05 | Current archives, exact bytes and expected anomaly folders are verified | **Unverified**, source pages only | R0 records actual files, masks, dimensions, taxonomy, bytes and hashes |
| E06 | The datasets define the same normal product | **Contradicted**, different products/acquisition | Separate fits, preprocessing, thresholds and result rows |
| E07 | Normal-only calibration measures defect recall | **Contradicted**, no positive labels in that subset | Calibrate FPR only; use declared training-development anomalies where available |
| E08 | Library defaults preserve our untouched test protocol | **Contradicted**, Anomalib MVTec defaults to `SAME_AS_TEST` validation [source](https://github.com/open-edge-platform/anomalib/blob/main/src/anomalib/data/datamodules/image/mvtecad.py) | Own manifest/DataLoaders; no default datamodule or automatic adaptive thresholds |
| E09 | Latest Anomalib fits the existing torch 2.6 stack | **Contradicted**, 2.7 raises required versions [release notes](https://github.com/open-edge-platform/anomalib/releases) | Isolated compatibility spike; no mutation of historical environment |
| E10 | PaDiM needs supervised gradient training or a GPU | **Contradicted** as a requirement; documented frozen-feature Gaussian fitting [PaDiM docs](https://anomalib.readthedocs.io/en/latest/markdown/guides/reference/models/image/padim.html) | CPU candidate, but local fit/inference resources remain unmeasured |
| E11 | PaDiM fit memory is bounded solely by minibatch size | **Contradicted** for inspected library implementation: embeddings retained then stacked [model source](https://github.com/open-edge-platform/anomalib/blob/main/src/anomalib/models/image/padim/torch_model.py) | Cap fitting normals; measure RSS before scaling |
| E12 | Original rotation baseline is lightweight | **Contradicted**, arithmetic, not a benchmark: 128×36×256×256×3×4 bytes ≈3.4 GiB before buffers | Remove exhaustive cached rotations from default |
| E13 | KSDD2 requires identical native geometry and custom tiled models | **Unverified** assumption; provider says approximately 230×630, not a guaranteed fixed schema [ViCoS](https://www.vicos.si/resources/kolektorsdd2/) | Audit dimensions; full-frame letterbox first; tiling is a later protocol |
| E14 | Inherited blur/exposure thresholds establish suitability | **Contradicted** as a conclusion by prior ineffective gate [local report](experiment/artifacts/EXPERIMENT_REPORT.md) | Technical rejection plus disclosed warnings; measure real retakes later |
| E15 | Anomaly score is probability or heatmap is severity | **Contradicted**, raw distance scoring, not calibrated semantics | Show raw units and fixed legend, no probability/severity claim |
| E16 | 90% recall /10% FPR proves industrial reliability | **Unverified**, engineering choices only; tiny normal test | Use screens with counts/intervals, not certification |
| E17 | Browser export is guaranteed equivalent | **Unverified** locally; open related mismatch report [issue 3726](https://github.com/open-edge-platform/anomalib/issues/3726) | Optional later parity gate; do not transfer PatchCore incident directly to PaDiM |
| E18 | A free-hourly CPU Space implies free account creation | **Contradicted** by current documentation's plan requirement [Spaces](https://huggingface.co/docs/hub/spaces-overview) | No default Docker/Gradio host; do not start paid plan |
| E19 | Prior exported model fits any static-host asset limit | **Contradicted** for Cloudflare Pages: 25 MiB asset cap [limits](https://developers.cloudflare.com/pages/platform/limits/) | Static replay carries no model; separate validated hosting needed for browser weights |
| E20 | Existing CPU timings transfer to new geometry/library | **Unverified**, different input and pipeline | Benchmark complete new image pipeline, fit time/RSS separately |
| E21 | Human review/reporting is unique | **Contradicted** as uniqueness: Anomalib Studio and vendors already cover inspection workflows [Anomalib](https://github.com/open-edge-platform/anomalib), [Cognex](https://www.cognex.com/en/products/machine-vision-software/visionpro-deep-learning) | Opportunity is unvalidated workflow fit, not feature novelty |
| E22 | Users need and will adopt our coverage/report workflow | **Unverified**, no interviews | Timed pilot and permission-based field feedback required |
| E23 | Old full-plan estimate is empirically grounded | **Unverified**, no component implementation | Replace with staged budgets and stop/re-estimate gates |
| E24 | Registration/deadline/eligibility are currently confirmed | **Unverified**, inaccessible official page | Reconfirm before submission; do not infer rules from old conversation |

## 4. Existing implementations: reuse, not re-invention

| Resource | What it already supplies | Reuse decision and limits |
|---|---|---|
| [Anomalib](https://github.com/open-edge-platform/anomalib), Apache-2.0 | Models, data utilities, evaluation/export tooling; Studio also offers a training/deployment UI | First model integration candidate, not whole-app fork. Active releases establish maintenance activity, not our runtime compatibility or accuracy |
| [Version 2.7 release notes](https://github.com/open-edge-platform/anomalib/releases) and [package configuration](https://github.com/open-edge-platform/anomalib/blob/main/pyproject.toml) | Current dependency/backend/export requirements | New Python 3.12 environment; minimum torch 2.10 and torchvision 0.25. Resolve exact CPU-compatible versions and lock only after import/fit/load tests. Mutable `main` is inspected evidence, not an execution pin |
| [PaDiM low-level model source](https://github.com/open-edge-platform/anomalib/blob/main/src/anomalib/models/image/padim/torch_model.py) | Frozen features, feature selection, Gaussian fit, raw maps/max score | Prefer a thin adapter around a pinned implementation. Default ResNet18 feature count is 100, unlike our earlier 50-channel custom configuration; different weight provider/normalisation must be recorded |
| [Official KSDD2 mixed-supervision implementation](https://github.com/vicoslab/mixed-segdec-net-comind2021) | Dataset layout, masks, split references and a supervised/mixed-supervised comparison | Use documentation/schema as reference; do not copy old training stack into main app. Code and data have non-commercial terms; README reports Python 3.8 /torch 1.6 or 1.8 /CUDA tests, not our current CPU compatibility |
| [Original PatchCore implementation](https://github.com/amazon-science/patchcore-inspection), Apache-2.0 | Established nearest-patch memory method and reproduction scripts | Alternative only after failure diagnosis. Documented Python 3.8/GPU-FAISS workflow is not plug-and-play Windows CPU support. Do not transfer its leaderboard scores |
| [Independent PaDiM reproduction](https://github.com/taikiinoue45/PaDiM), MIT | Compact reference and category-specific reproduction results | Useful comparison, not author code or a maintenance promise; discrepancies across categories warn against assuming “PaDiM” configurations are equivalent |
| [Cognex VisionPro Deep Learning](https://www.cognex.com/en/products/machine-vision-software/visionpro-deep-learning) and [MVTec MERLIC](https://www.mvtec.com/products/merlic) | Established inspection/vision products with software workflows | Existing alternatives. Vendor capabilities do not establish our target's cost barrier or independent performance; prices/affordability and demand remain unvalidated |

**Could the baseline be enough?** Yes, if it meets the declared operating targets and review needs. Do not force AI complexity to improve a pitch. If only a classical method passes, present that honestly and verify whether the organiser accepts the resulting Applied AI scope.

**Candidate differentiation, not a moat:** explicit inspected/uninspected coverage, uncertain decisions, traceable rework and report limitations for a small unit. These are copyable features; evidence of reduced workload, useful reports and a practical capture recipe would be needed to justify a product. No validated customer gap has been found in this review.

## 5. Dataset and two-recipe protocol

### Dataset A — `mvtec_metal_nut`

Use original MVTec AD, not AD 2, `metal_nut` only. Official source is [MVTec's page](https://www.mvtec.com/research-teaching/datasets/mvtec-ad). Archive version is its retrieval date/hash until a release identifier is confirmed. Expected anomaly folders `bent`, `color`, `flip`, `scratch` must be verified on ingest; do not make predicted subtype claims from folder names. A flipped face is an inspection-recipe anomaly, not automatically damaged material.

Source images/masks and the paper's published split support benchmark detection/localisation. Deliberately produced defects and controlled capture are not representative consignment prevalence. Random in-plane rotation and normal appearance variation challenge spatial models. [Original paper](https://www.mvtec.com/fileadmin/Redaktion/mvtec.com/05_research_teaching/datasets/mvtec_ad.pdf).

### Dataset B — `ksdd2_surface`

Use KSDD2, not KSDD. [Provider source](https://www.vicos.si/resources/kolektorsdd2/) and [official layout/adapter documentation](https://github.com/vicoslab/mixed-segdec-net-comind2021/blob/master/datasets/README.md). Binary visible surface imperfections; do not invent per-type labels or the physical component's identity. Check native dimensions, image/mask pairing and train/test membership against the release. Missing defective masks are quarantined, not assigned zero masks.

### Licence, access and sizes

Both image releases specify CC BY-NC-SA 4.0. Preserve licence/attribution, inspect the terms for the intended research demonstration, and do not promise commercial deployment rights. The framework's Apache licence does not override data restrictions. Actual archives have not been downloaded, current archive byte counts and availability are unverified. Reserve **10 GiB disk as a planning budget**, inspect headers/archives before large download, record actual compressed/extracted bytes; expand budget or stop if needed. Avoid obsolete hard-coded mirror URLs; a provider's manual workflow is acceptable.

### Strategy

- Separate models, reference banks, normal statistics, thresholds and result tables per recipe; share code and a frozen backbone only where the tested adapter supports it.
- No joint training, score pooling or automatic product switching. Different normal appearances and field-of-view definitions make a pooled normal Gaussian unjustified.
- Cross-dataset nut→surface scoring is at most an optional domain-shift negative control. It is not defect generalisation or an MVP acceptance experiment.
- Maintain original official-test membership; derive development/calibration from official training. Any quarantined overlap changes the evaluated subset and must be disclosed. Holding back training normals already makes our recipe different from using the complete published training set; **do not call it a paper reproduction**.

### Common immutable manifest

`ImageRecord = {id, dataset, release_hash, recipe, path, mask_path|null, byte_sha256, decoded_sha256, phash, physical_group|null, group_confidence, official_split, experiment_role, label, defect_type|null, width, height, provenance, parent_id|null, quarantine_reason|null}`.

- Raw archives/extraction immutable; derived images/maps elsewhere. Extract safely against path traversal, symlink escape and archive bombs. No execution of downloaded scripts/pickle split files; inspect documented split membership without untrusted deserialisation.
- Decode/mask/dimension/label checks; exact/near-duplicate audit before role assignment. pHash ≤2 +small thumbnail difference is only a candidate rule; record grouping decisions, do not assert physical identity from it.
- Split originals before augmentation/crops. Views/source-board images with known shared identity remain together. Unknown physical IDs and the limits of duplicate detection stay in the report.
- Whole mask group is held out with its image. Inference never receives labels/masks/defect-folder names; test labels only enter the evaluator after configuration freeze.

### Fit/development/calibration/test roles

Seed 4217; group order by SHA256(seed +dataset +group ID). Allocate eligible official-training normals **60% fit /20% development /20% calibration**, whole groups, report actual counts. If each image is independent, expected nut counts 132/44/44; KSDD2 1,251/417/417. These are calculations before audit, not measured manifests.

- For first fit, use **at most 128 fit-normal groups**, deterministic prefix, one canonical example per duplicate group; remaining fit groups unused. Both methods receive the same fit pool; baseline uses a declared 16-reference subset. Cap is an engineering memory limit, not a known sufficient data requirement.
- Development normals are for technical/geometry/resource checks only. KSDD2's 246 official-training anomalies may be used as a fixed development set for failure diagnosis; never fit normal statistics on them. Do not access final calibration to choose model settings.
- MVTec has no official training anomalies. Freeze nut settings without real defective-development recall, explicitly acknowledging this weakness; no borrowing official-test anomalies. A synthetic training-only stress copy can test geometry/software but cannot supply genuine defect validation.
- To prevent unbounded tuning, default baseline and default PaDiM only. One predeclared follow-up (alignment or resolution) is allowed **before final calibration/test**, using development data; document it and the selection rule. No late architecture search.
- Reserve official tests for locked evaluation. Do not use Anomalib's default MVTec datamodule (`SAME_AS_TEST`) or adaptive F1 thresholding. Build explicit manifest DataLoaders and inspect accessed IDs. [Default source](https://github.com/open-edge-platform/anomalib/blob/main/src/anomalib/data/datamodules/image/mvtecad.py).
- If duplicates cross roles, group first and rebalance training roles. If official train/test overlap, quarantine contaminated test items and label cleaned-subset results. Never silently substitute them or declare physical-instance independence.

## 6. Model/preprocessing decision — bounded spike first

### Baseline

**B0:** nearest RGB reference residual, no registration, 16 deterministic fit-normal references, batch/chunk ≤4 references; float32 [0,1], no per-image mean removal, sigma-1 residual smoothing, mean of top 1% valid residual pixels as image score. Original colour is retained because colour can be anomalous. Return raw residual map in original coordinates.

This baseline is deliberately cheap and may fail rotated normal nuts. That failure is informative. Do not add a 36-angle bank by default; a training-development alignment follow-up must have a time/memory budget and record face-preservation assumptions. At 256²×3 float32, B0 bank is about **12 MiB** versus old **3,456 MiB** rotated cache, excluding buffers. These are calculated array sizes, not measured RSS or latency.

### Candidate

**P0:** maintained Anomalib PaDiM, ResNet18 features `layer1/2/3`, 100 retained features, separate Gaussian state per recipe, raw map/image distance output. No supervised gradient optimisation. Preserve backbone/timm weight configuration/hash and channel selection; do not assume it uses the identical torchvision weights as the local PCB experiment. [Model documentation](https://anomalib.readthedocs.io/en/latest/markdown/guides/reference/models/image/padim.html).

Prefer a thin adapter around `PadimModel` from a verified pinned release to avoid Engine/datamodule preprocessing, test-derived calibration and double normalisation. Exact low-level import/signature, device behaviour and raw-output contract must pass R1 on the pinned wheel/source; current `main` is not sufficient as an executable pin.

**Environment selection:** new environment for Anomalib 2.7 CPU-compatible dependencies, Python 3.12, `num_workers=0`, one fitting/inference process, batch 1 initially. CPU extras and minimum dependencies are documented; successful Windows wheel/import/fit/load is untested. Do not install `[full]`, CUDA, OpenVINO or loggers for the first spike. Preserve `experiment/.venv` untouched. [Release/configuration](https://github.com/open-edge-platform/anomalib/releases).

**Fallback at the end of R1's timebox:** use a small extracted copy of the existing trusted native ResNet18/compact PaDiM logic in its known CPU stack, still capped to 128 normals. Label 50-channel custom results separately; do not call them Anomalib 100-feature results. If both integration paths exceed budget/resource limits, stop at feasibility report instead of inventing a third framework migration.

### Geometry and resources

- Nut: RGB full-frame aspect-preserving letterbox to **256×256**; no centre crop, side flip, normalising away colour or learned foreground detector.
- KSDD2: rotate **all** images/masks by one fixed 90° transform if required to make long side horizontal, then aspect-preserving letterbox into **256×640**. No defect-dependent rotation. Handle recorded dimension variation through the same transform; do not reject merely for differing original dimensions.
- Valid ROI excludes padding from image score and pixel metrics. Map back to original coordinates; image interpolation bilinear, masks nearest neighbour. Retain edge defects; verify a synthetic edge-mark coordinate fixture.
- No tiles, per-position models, contour registration or new numerical streaming implementation in the first pass. Resolution may miss tiny scratches; full-frame mapping is an explicit prototype trade-off, assessed in development and final failures.
- For 128 normals, 100 features and a stride-4 feature grid, retained feature arrays are approximately **200 MiB nut /500 MiB surface**; square covariance storage approximately **156 MiB /391 MiB** at float32. These are conditional shape calculations, excluding vstack copies, full-backbone tensors, BLAS workspace, Python and smoothing; actual shapes/peak RSS must be measured. CPU memory estimates are not a guarantee that the standard fit meets 4 GiB.
- Library fit retains embeddings before stacking, so minibatch 1 does not bound accumulated fit memory. Cap and RSS check are required; if over budget, use the predefined 50-channel fallback or stop, not silent out-of-memory retry with a changed experiment. [Inspected model implementation](https://github.com/open-edge-platform/anomalib/blob/main/src/anomalib/models/image/padim/torch_model.py).
- No generic GPU/VRAM need or inference speed is inferred from paper scores or previous 224² PCB timings.
- For R1, stop a fitting process if its RSS exceeds the smaller of **4 GiB or 60% of available RAM recorded at launch**; leave headroom for the operating system. This is a provisional experiment cap, not a measured requirement. A backend that cannot fit within it fails the resource spike even if inference would fit later.

### Hard rejection, soft warnings

Hard rejects: malformed media, unsupported format, animation/multiple frames, >10 MiB encoded or >20 MP decoded, below 128 pixels minimum side, unknown recipe, missing/mismatched model. These are engineering input limits, not industrial capture rules.

Basic exposure/focus diagnostics are **warnings** in the first benchmark, not grounds for filtering images. Freeze warning values using development data, then retain all technically valid test images in metrics. Do not reuse old Laplacian/luma thresholds as validated retake criteria. Record manually confirmed required view; the model cannot guarantee identity, visibility or lighting suitability. No arbitrary score-confidence abstention.

### Threshold and artifact contract

- For each method/recipe, after configuration freeze, use only normal calibration image scores. Sort ascending, choose one-based `k=ceil(0.90*(n+1))`, flag `score > score[k]`; if k>n or no sufficient calibration, fail. Normal target FPR 10% is provisional. Calibration has no defective-recall information.
- Save empirical calibration false flags, n/ties, recipe transform and raw score units. Exchangeability with factory images is not established; no field FPR guarantee or probability interpretation.
- First localisation outputs are **continuous attention maps**, not binary defect masks. Freeze a calibration-derived display range; never independently rescale images into apparently comparable severity. Pixel AUROC/AP do not need a segmentation threshold.
- Define that display range concretely: 0 to the 99.5th percentile of a fixed seed-4217 sample of up to 10,000 valid map pixels per normal calibration image, equally weighted by image. Clip higher values at the displayed maximum; preserve raw maps for evaluation and label the legend “anomaly intensity, not severity.” Degenerate zero range uses an explicit fallback epsilon and diagnostic, never a fabricated probability scale.
- Binary masks/IoU/Dice remain optional later: choose pixel threshold from calibration only and report sensitivity to the chosen rule. Do not gate MVP usefulness on an unvalidated 99.5th-pixel percentile or peak point.
- Bundle: method/backend/version, dependency lock, model source revision, pretrained config/hash, selected channels, Gaussian parameters, manifest hashes, recipe geometry/valid ROI, score rule, image threshold, display range, code hash, metrics status and licence/attribution. Only trusted locally produced weights are loadable.

## 7. Evaluation and decision rules

### Pre-register before final calibration/test

Provisional screens per recipe: **all-defect recall ≥90%, accepted-normal FPR ≤10%, technical-scoring coverage ≥90%, warm batch-1 p95 ≤5 seconds, peak batch-1 inference RSS ≤4 GiB**. Also measure fitting RSS/time separately. These are workflow engineering screens, not industrial requirements. If final-test labels include 93 defective/22 normal nut images, at least **84/93 flagged** and at most **2/22 false flags** are needed for point-estimate screens; uncertainty remains substantial. Counts change if quarantine occurs.

- Score all technically valid images; count technically rejected anomalies as misses in all-defect recall. Give TP/FN/FP/TN, rejected normal/anomalous counts, reason, accepted-only recall/FPR, all-normal FPR, precision, coverage and prevalence.
- Image AUROC and AP (average precision, not trapezoidal PR area) on scored images with coverage disclosed; undefined one-class/zero-denominator metrics return null/reason. Use pinned scikit-learn implementations, not handwritten ranking metrics. [AP definition](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html).
- Pixel AUROC/AP over valid original-coordinate masks/maps; report anomalous-only and all-image context, mask counts and per-image region/size failures. Pixel background dominance is a limitation; pixels are not independent products for intervals. Optional binary IoU/Dice and AUPRO deferred until their exact threshold/protocol is specified.
- Peak-in-mask hit is diagnostic only; do not use it as evidence that a map accurately segments a defect or helps people.
- Per-category/defect-folder recall where verified; never infer KSDD2 subtype ground truth. Raw score distributions are not comparable across datasets.
- Main tables per method ×recipe. Macro means optional only after individual rows. Pooled confusion counts may be shown with denominators; no pooled-score AUROC. Passing one recipe cannot cover failure of another.
- Wilson 95% intervals for recall/FPR/precision; group bootstrap 1,000 replicates for AUROC/AP if meaningful group IDs, otherwise disclose image-level independence limitations. Point targets alone are not high-confidence assurance.
- Measure cold model init, fit time/RSS, warm decode/preprocess/inference/postprocess/map end-to-end median/p95 and sample count; time every final-test item once after ten development warmups. Batch 1, four CPU threads where backend supports it; record actual thread/RAM/hardware.
- Synthetic brightness ×0.6 /×1.4 and blur radius 2 on paired copies only **after** base test; unchanged thresholds; separate tables. Not additional independent captured products or proof of glare robustness.
- Freeze one candidate as **primary before test** based on development feasibility. Test reports comparison of the fixed baseline and candidate. If test outcomes cause a change in selected method/recipe, label selection exploratory and require new independent confirmation before stronger use claims; do not use the same holdout repeatedly to “pass.”
- Build a failure gallery with original, map, mask and source ID, retaining false negatives and false positives. No expected accuracy is invented.

### Benchmark versus real use

Benchmark passing supports a constrained research demo only. Field capture, physical-product grouping, human error/workload and buyer record usefulness remain untested. Do not let unflagged products skip human inspection on benchmark evidence alone. No buyer acceptance, consignment rejection reduction or monetary savings is measured.

The new human exercise should counterbalance manual/assisted order and use disjoint images of comparable types; record errors as well as time. A single-participant 24-item convenience pilot can expose gross usability failures but cannot establish factory efficacy. The prior PCB exercise does not validate these recipes. No external outreach authorised.

## 8. Executable task sequence — blocked work is explicitly conditional

### Proposed repository boundary

```text
components/
  pyproject.toml / requirements.lock
  configs/{protocol,mvtec_metal_nut,ksdd2_surface}.yaml
  src/component_inspector/
    cli.py
    data/{acquire,manifest,audit,splits}.py
    vision/{geometry,reference,padim_adapter,artifacts}.py
    evaluate/{calibrate,metrics,run,report}.py
    app/{api,ledger,export}.py
  tests/{test_data,test_geometry,test_models,test_calibration,
         test_metrics,test_api,test_ledger,test_export}.py
  web/{package.json,package-lock.json,src/...}
  data/{archives,raw,manifests}/         # not committed; raw immutable
  models/<recipe>/<version>/           # trusted artifacts
  runs/<run_id>/                      # immutable protocol/results
  outputs/{reports,demo}/
```

Existing `experiment/` and original plan remain unchanged. `components/` is a **proposed path**, not created in this review.

### Shared interfaces to implement

```text
load_records(dataset: str, root: Path) -> list[ImageRecord]
audit(records) -> AuditReport
split(records, seed: int) -> SplitManifest
prepare(image: PIL.Image, recipe: RecipeConfig) -> PreparedImage
PreparedImage = {tensor, valid_roi, inverse_geometry, original_shape}
fit(method: str, records, config) -> ArtifactBundle
predict(prepared: PreparedImage, bundle) -> Prediction
Prediction = {status: scored|not_scored, reasons: list[str], warnings: list[str],
 score: float|null, threshold: float|null, flagged: bool|null,
 map_original|null, recipe_id, model_id, preprocess_id, timing_ms}
calibrate(normal_scores, alpha=0.10) -> ThresholdRecord
evaluate(rows) -> MetricsReport
record_decision(inspection_id, decision, note) -> DecisionEvent
batch_snapshot(batch_id) -> BatchSnapshot
```

Uncalibrated bundles may produce development raw scores but never operational flags; calibrated endpoint requires a threshold. No ambiguous “normal = acceptable” field.

### R0 — Source/data/split readiness

**Purpose/dependencies:** none; resolve dataset access and implement only experiment scaffolding after authorisation. **Files:** package/configs, `data/*.py`, `tests/test_data.py`. **Effort budget:** 3–5 h hands-on, access delays excluded.

- [ ] Record current organiser rules/deadlines, source/terms and no-paid constraint. Inspect release/sample and archive compressed/extracted bytes; no blind full framework install/download.
- [ ] Write tests asserting safe extraction, missing-defect-mask quarantine, normal-label consistency, duplicate groups and whole-group split disjointness.
- [ ] Implement adapters/manifests; verify actual recipe taxonomy/dimensions/counts without inference. Record unknown physical IDs.
- [ ] Freeze 60/20/20 normal roles, KSDD2 defective-development membership and final official tests. Audit exact/near-duplicate conflicts and explain removals.
- [ ] Run `python -m pytest tests/test_data.py -v`; completion requires manifest assertions, licence/source record and readable samples, not a merely created directory.

**Deliverable:** immutable source and role manifests. **Stop:** inaccessible archive, incompatible mask semantics or unresolved intended use; save blocker rather than substituting unrecorded data.

### R1 — Bounded native model/resource spike

**Purpose/dependencies:** R0. **Files:** `vision/*.py`, `tests/test_geometry.py`, `tests/test_models.py`, backend lock. **Effort budget:** 5–8 h; at most four hours of this on current-library installation/API integration before the one fallback.

- [ ] Write geometry tests for edge preservation, grayscale→RGB, deterministic whole-image rotation, padding exclusion and original-coordinate map restoration. No mask passed to model.
- [ ] Create isolated Anomalib environment; verify exact release/tag, install CPU-compatible dependencies, `num_workers=0`; record source/wheel and weight hashes. No change to old environment.
- [ ] Implement B0 and thin P0 adapter with explicit no-double-normalisation and raw-output checks. Cap fit groups 128; no default datamodule/Engine calibration.
- [ ] Fit only eligible normals, score development examples; measure fit/inference RSS, elapsed time, artifact bytes, repeat/load parity and actual input/feature shapes. Assert finite covariance/maps and recipe mismatch rejection.
- [ ] Run `python -m pytest tests/test_geometry.py tests/test_models.py -v`. If current library fails within timebox, run the named native 50-channel fallback once; record backend change. If both fail, stop.

**Deliverable:** native development prediction and feasibility report for both datasets. **Completion:** real score/map, reproducible load and practical resource budget; **not** defect accuracy approval. No custom streaming covariance or new PatchCore migration in this spike.

### R2 — Freeze protocol, calibrate and evaluate

**Purpose/dependencies:** R1 pass. **Files:** `evaluate/*.py`, `tests/test_calibration.py`, `tests/test_metrics.py`, run/artifact manifests. **Effort budget:** 4–7 h.

- [ ] Write fixture tests for quantile rank/ties, no-test access, zero denominator, rejection-as-miss, mask geometry, independent per-recipe metrics and no pooled-score AUROC.
- [ ] Freeze geometry/backend/config, primary method and one-variant development history. Compute thresholds from separate normal calibration only. Persist hashes before final-test scoring.
- [ ] Run fixed methods once on each untouched test; save all predictions, counts, AP/AUROC/localisation, actual timing/RSS and intervals before stress analysis.
- [ ] Generate unfiltered failure gallery; run paired transformations separately. Include anomalies deliberately created in original datasets as a provenance caveat, not digitally transformed stress images.
- [ ] Run `python -m pytest tests/test_calibration.py tests/test_metrics.py -v`; record per-recipe conditional/no-go. If neither usable, dependent app tasks stop and research outputs are the deliverable.

**Deliverable:** two-dataset evaluation report and explicit gate. **Initial total R0–R2:** **12–20 h planning allocation**, not observed duration or a performance forecast. Re-estimate after R1.

### A0 — Early one-image human-review milestone (conditional)

**Depends:** R2 supports a limited research assistant, or user explicitly requests an educational failure demo. **Files:** `app/{api,ledger}.py`, minimal `web/src/Review.tsx`, `tests/test_api.py`, `tests/test_ledger.py`. **Effort budget:** 5–8 h.

- [ ] Write tests for invalid/oversized decode, unknown recipe/model, absent threshold, timeout/busy response and no implicit acceptance.
- [ ] Implement synchronous local `POST /api/inspect` with concurrency cap 1; reject new busy requests with 503 instead of queueing. Return scored/not_scored JSON or 413/415/422/409/503. A client timeout must not release the inference lock until underlying work ends or permit a late result to overwrite a newer human decision. Test that case explicitly; do not pretend thread cancellation stops native inference. No background job queue or polling state machine.
- [ ] Add minimal review page: one development image → **real** native score/map → person decision → SQLite append event → reload; human action is actual, not generated fixture data.
- [ ] Test browser/API displayed recipe/version, overlay orientation and persistence; record full API latency separately from inference.
- [ ] Run API/ledger tests and frontend typecheck/build. Completion requires saved/reloaded human decision; no deployment or benchmark claim inferred from a screenshot.

**Deliverable:** early end-to-end milestone, clearly experimental. Use development images for this milestone; not a second round of test-driven tuning.

### A1 — Batch accounting and truthful report (conditional)

**Depends:** A0. **Files:** ledger/export modules, `web/src/{Batch,Report}.tsx`, `tests/test_ledger.py`, `tests/test_export.py`. **Effort budget:** 8–13 h.

- [ ] Test six expected IDs with duplicates, cross-product photo reuse, new rework capture, uncertain decision, uninspected items and acknowledgement invalidation. Assert unique-product rather than photo denominators.
- [ ] Implement immutable inspection/decision history, current status and snapshot-based owner acknowledgement; partial batch stays draft. No tamper-proof/verified-identity claim.
- [ ] Add report/UI counters: expected, uploaded, model-scored, human-reviewed, resolved, uncertain/rework and uninspected. Distinguish “not flagged” from human acceptable.
- [ ] Generate HTML/CSV from one snapshot with hashes, calibration/model versions, coverage, sources and limitations; escape HTML and spreadsheet formulas.
- [ ] Run ledger/export tests, typecheck/build and compare fixture/API/report counts. Any actual photo→fictional product mapping is disclosed.

**Deliverable:** one complete local batch journey, not a certificate.

### A2 — Human usefulness pilot (conditional)

**Depends:** A1 and a real participant. **Files:** `outputs/review_exercise/`, `outputs/reports/human_pilot.md`, analysis script/tests. **Effort budget:** 4–7 h preparation/analysis plus participant time.

- [ ] Freeze manual/assisted sets, randomisation/order and analysis before responses; use disjoint matched items and report defect prevalence/task difficulty limits.
- [ ] Record actual participant time/errors, uncertainty and hints used; no response fabrication. Counterbalance order where feasible; disclose single-participant learning effects.
- [ ] Report capture time as unmeasured if only benchmark review occurs. Compare assisted error and time jointly; no assumed speed gain.
- [ ] Keep manufacturer/buyer feedback as a drafted exercise until contacts and permission exist; compare against current alternatives, added steps and missing evidence.
- [ ] Decide whether UI assistance is worth continuing; benchmark screens alone cannot approve a factory pilot.

**Deliverable:** pilot findings or explicitly pending participant exercise.

### A3 — Package and deploy the honest demo mode (conditional)

**Depends:** A1, plus A2 results/pending status disclosed. **Files:** deployment configuration, `outputs/demo/`, `docs/REPRODUCE.md`, model cards. **Effort budget:** 6–10 h.

- [ ] Package local native service with strict upload limits, random storage paths, SQLite transactions and no external exposure by default. Ignore raw data/models/secrets in version control.
- [ ] Choose live native hosting only after current zero-cost/account/licensing/resource checks pass. No paid plan or token assumed.
- [ ] Default fallback: deployed static **replay**, no model weights/live uploads, labelled precomputed inference and local demo decisions. Downloadable reports say simulated batch IDs; no durable shared backend claim.
- [ ] Test clean startup/restart, model/hash mismatch, missing artifacts, report export and offline local fallback. Run all meaningful tests/typecheck/build; record outcomes, not planned passes.
- [ ] Rehearse one missed anomaly and false alarm as well as a successful review; hand off reproduction instructions, measured limits and final verdict.

**Deliverable:** honest deployed replay plus local live demo, or a separately verified zero-cost live mode. This does not satisfy “deployed live inference” if that is mandatory; raise that remaining choice explicitly.

### X0 — Optional export experiment, outside delivery-critical path

**Depends:** R2/A1 and explicit time allocation. **Files:** export adapter/parity fixtures and report only. **Budget:** 4–8 h; stop at timebox.

- [ ] Use the pinned version's supported exporter, exact preprocessing/weights/threshold bundle and documented output fields; verify APIs rather than copying old `metadata.json` workflows.
- [ ] Compare native→ONNX same tensors, then independent raw-image geometry/normalisation/map/score. Use initial score/map tolerance `atol=1e-4, rtol=1e-4`; inspect differences and every boundary decision, not threshold changes to hide drift.
- [ ] In an actual laptop browser measure model/runtime download bytes, cold/warm end-to-end latency and failures. Export success alone is not browser support.
- [ ] Full fixed-test parity comparison is required before replacing native inference; repeated evaluation is backend verification, not a fresh accuracy trial. No phone claim without a named phone/browser experiment.
- [ ] If unsupported, keep native/replay; no time-expanding quantisation/3D/GPU branch.

## 9. Storage/API/security details for app tasks

- Backend local-only, trusted benchmark/demo images. JPEG/PNG only; actual bytes/decode checked, not filename/MIME alone. Handle EXIF orientation once; reject animation/multipage and decompression bombs before expensive work.
- Store original uploads outside public assets with generated filenames, exact content hash and metadata-stripped display derivatives. No client path concatenation or arbitrary remote image URL fetching.
- `POST /api/batches` creates expected unique product IDs/recipe. `POST /api/inspect` consumes batch/product/recipe/idempotency key/image and returns inspection ID +Prediction. `POST /api/inspections/{id}/decision` appends human result; `GET /api/batches/{id}` and report endpoints share one snapshot.
- Same key/payload returns previous result; key with changed payload is 409. Same image/same product duplicate returns old attempt; same image/different product blocks pending review. This is content reuse detection, not guaranteed physical identity.
- New capture after rework creates attempt; newer uncertain/rework makes current product unresolved; no acceptable fallback from history. Acknowledgement invalidated on later events.
- Local role labels are explicitly demo identities. Public persistent multi-user use needs real authentication, authorisation, CSRF/session controls, HTTPS, storage retention/deletion and rate limits; it is a separate scoped task before enabling public uploads. Static replay has no server secrets or shared approval identity.
- Defaults: bind `127.0.0.1:8766`; existing experiment may use 8765. Fail missing/stale artifacts, never silently use the other recipe. Trust locally produced artifact formats only.

## 10. Deployment and export findings

Current [Hugging Face Spaces documentation](https://huggingface.co/docs/hub/spaces-overview) states that creating Gradio/Docker compute Spaces requires a paid plan, while static Spaces are free; it also lists a restricted ZeroGPU route for qualifying free accounts. CPU Basic's zero hourly rate is not enough to establish eligibility at zero total cost. We have not inspected the user's account, accepted terms or created anything. **Do not depend on a paid-plan workaround or assumed ZeroGPU access.**

[Cloudflare Pages limits](https://developers.cloudflare.com/pages/platform/limits/) specify 25 MiB per asset. The prior ≈43.1 MB exported PCB model would exceed that; the new models' sizes are unknown. Static replay avoids a model download. Another asset store or chunking is a separate tested hosting design, not assumed free capacity.

Current Anomalib release/export APIs differ from older examples. Exported raw and normalised scores/thresholds must be traced explicitly; a 0.5 UI threshold is not our native raw-distance threshold. No runtime-specific speed or parity is assumed. Local CPU measurements cannot be transferred to server hardware or WASM.

## 11. Failure evidence: what is still relevant?

| Evidence chain | Version/status checked | Interpretation for us |
|---|---|---|
| [PaDiM memory discussion 1123](https://github.com/open-edge-platform/anomalib/discussions/1123) | 2023 report on 1.0.0; current inspected model still retains/then stacks embeddings | Historical incident alone is not a current benchmark, but code confirms accumulation design. Cap/spike, not blanket “PaDiM cannot work” |
| [MVTec URL PR 3673](https://github.com/open-edge-platform/anomalib/pull/3673) | Merged 17 July 2026; release notes include download fixes | A stale-download complaint is not evidence latest release remains broken. Pin/check actual endpoint and report whether it works |
| [ONNX metadata issue 2620](https://github.com/open-edge-platform/anomalib/issues/2620) | Closed; reported against 2.0; closure rationale/comments not fully retrievable | Do not call it a present missing-metadata defect or a verified fix. Current artifact/output schema must be tested |
| [Export mismatch issue 3726](https://github.com/open-edge-platform/anomalib/issues/3726) | Open when read, reported 20 Aug 2026 against 2.6.0 PatchCore/wide_resnet101_2 | Relevant reason to require parity, not proof PaDiM 2.7 fails. Linked discussion/earlier issue belong to one evidence chain, not three independent reports |
| [Current release notes](https://github.com/open-edge-platform/anomalib/releases) | 2.7 removes legacy exporter path and raises dependency floors | Old export recipes/dependency pins are not blindly reusable; optional export budget only |
| [Independent PaDiM reproduction](https://github.com/taikiinoue45/PaDiM) | README reports different results by category/configuration | Supports implementation sensitivity, not our expected recall/FPR; metric may differ from our decision screen |
| [Original MVTec paper](https://www.mvtec.com/fileadmin/Redaktion/mvtec.com/05_research_teaching/datasets/mvtec_ad.pdf) | Controlled capture/deliberately created anomalies and rotation caveats | Benchmark/domain limits remain; vendor/research accuracy cannot validate factory usefulness |

No paper/vendor benchmark, unresolved user report or repository popularity is counted as our own performance measurement. Further broad search would not answer the remaining local memory/accuracy/demand questions; the bounded experiment is now the cheaper evidence source.

## 12. Time, gates and stop conditions

- **Now:** review document only. No environment, model or app implementation performed.
- **Gate G0 /R0:** sources usable, intended research demonstration terms acceptable, schema/identifiers/splits audited. If not, document blocker before choosing replacement data.
- **Gate G1 /R1:** native score/map, save/load and measured resource feasibility on development images. If neither named integration path works within timebox, stop; no full API/UI.
- **Gate G2 /R2:** fixed per-recipe results and uncertainty. Proceed only with recipe(s) whose limited assistance claim is supported; if both fail, deliver research report, not a reliable-inspector pitch.
- **Gate G3 /A0:** first real inference→human decision→reload milestone. No synthetic human acceptance masquerading as a completed review.
- **Gate G4 /A2–A3:** actual human pilot and verified deployment mode. Missing participant/field data remains pending, not a pass.

**Budget:** R0–R2 **12–20 h**, A0–A3 **23–38 h**, contingency **7–12 h**, total **42–70 h** if all proceed; optional X0 adds 4–8 h. Front-summary “30–50 h conditional application budget” means A0–A3 plus contingency, **not** a second extra allocation. These are bounded planning ranges, not measured effort or a guarantee. Archive access, dependency failures, participant time and major model changes can exceed them; stop/re-estimate at gates rather than silently extending.

For one builder this is roughly 7–12 focused six-hour days excluding optional export and waiting. Reconfirm actual daily availability and deadlines before promising dates. Aim to finish the native experiment well before the retained 15 November idea milestone and package a frozen demo with buffer before 15 December; those milestones remain unverified until organiser confirmation.

**Cut first:** export/browser/mobile, map/animation, queues/public multi-user service, model subtype classifier, custom tiled/streaming/registration systems, additional datasets. Never cut source/label audits, calibration separation, honest failures, human confirmation or truthful coverage.

## 13. Proposed commands — not implemented or executed

Future CLI lives under `components/`; install that package in its verified isolated environment, then run from that directory. These are interface requirements for later implementation, not existing runnable commands.

```powershell
python -m component_inspector.cli doctor
python -m component_inspector.cli acquire --dataset mvtec_ad --category metal_nut
python -m component_inspector.cli acquire --dataset ksdd2
python -m component_inspector.cli prepare --config configs/protocol.yaml
python -m component_inspector.cli spike --config configs/protocol.yaml
python -m component_inspector.cli freeze --config configs/protocol.yaml
python -m component_inspector.cli calibrate --frozen-run RUN_ID
python -m component_inspector.cli evaluate --frozen-run RUN_ID
python -m component_inspector.cli report --run RUN_ID
python -m pytest tests -q
python -m component_inspector.cli serve --host 127.0.0.1 --port 8766
npm --prefix web ci
npm --prefix web run typecheck
npm --prefix web run build
```

`spike` must reject test IDs, `freeze` locks backend/config/roles/primary method, `calibrate` appends immutable thresholds from calibration only, and `evaluate` requires a complete calibrated frozen bundle. No filesystem magic or test-path fallback. Provider manual downloads are supported by documented `--archive PATH`; acquisition must not bypass provider forms.

## 14. Search log, source limitations and traceability

| Date | Query / route | Source types and result |
|---|---|---|
| 17 Oct 2026 | Complete original plan and local `experiment/` evidence | Read original, including targeted reread of middle sections after initial output truncation; preserve recorded failures |
| 17 Oct 2026 | `anomalib padim CPU memory`, `validation test split threshold leakage` | Official docs, model/datamodule source and historical discussion; defaults and accumulated-memory risks identified |
| 17 Oct 2026 | `anomalib padim onnx export`, release notes, issue 3726 | Open/closed issue status, changelog and export API changes; related reports deduplicated |
| 17 Oct 2026 | Anomalib release 2.7/package requirements, original PatchCore and PaDiM reproduction | Compatibility/licence/maintenance evidence; not runtime testing |
| 17 Oct 2026 | KSDD2 provider and original mixed-supervision implementation/layout | Identity/counts/licence and dataset reader references; no archive extraction |
| 17 Oct 2026 | MVTec provider and original paper | Official split/capture caveats; raw folder taxonomy remains to verify |
| 17 Oct 2026 | Cognex VisionPro, MVTec MERLIC, Anomalib Studio | Existing solution overlap; no independent pricing/adoption validation |
| 17 Oct 2026 | Hugging Face Spaces overview and Cloudflare Pages limits | Current account/hosting constraints; no account provisioning |
| 17 Oct 2026 | Organiser URL | Inaccessible through tool; no current rules verification |

Primary pages/code were preferred. Mutable `main` and `latest` docs were inspected for current behaviour but must be replaced with immutable version/commit references at R1. Several raw-tag URLs and some deep documentation URLs could not be fetched; no claim of tagged source equivalence is made. Issue closure is not proof of a fix, and an open issue on another model is not proof our version is broken. This is a single-reviewer technical scoping audit, not a systematic literature review or field study.

## 15. Remaining uncertainty and final verdict

**Conditional go:** a small native experiment with the two separate datasets and a maintained-library-first integration spike. **No-go today:** full reliable inspection product, commercial use of research-only data without clearance, unattended acceptance, factory-wide twin/root causes, or promised free live public inference.

The next evidence should come from **R0–R2**, not more UI features: actual source/schema access, resource profile and independently locked operating-point results. A passing benchmark still needs representative captures and human/user evidence.

**One material choice still needed:** if zero-cost live public inference cannot be verified, is a deployed labelled replay plus a working local live-inference demo sufficient? This reviewed plan preserves it as a fallback proposal, not user-approved equivalence. No other routine implementation choice requires a new decision before the experiment.

**Skills used:** literature-review for source/evidence tracking; senior-computer-vision for dataset/model/geometry/resource audit; writing-plans for task/interface/gate revision; hf-cli guidance for checking Hub access/hosting without assuming credentials. No CLI installation, training, deployment or subagent work was performed. Method acknowledgement: [Scientific Agent Skills, Kassis et al., 2026](https://doi.org/10.48550/arXiv.2609.00065), a workflow reference, not product validation.

**Consistency checklist for this revision:** original retained; two recipe IDs used consistently; no same-product joint training; no test-derived thresholds; app tasks depend on experiment gates; localisation is diagnostic; resources/effort are labelled estimates; hosting mode distinguished; commands are future contracts; source access and actual experimental outcomes remain explicitly separate.
