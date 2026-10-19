# Tech4Bharat Technical Progress Report

## Executive summary

**Audit date: 19 October 2026 (Asia/Kolkata / IST). Status: Stage 5 completed; detector qualification is no-go; application Stages 6–10 stopped.**

Tech4Bharat has a working local research pipeline for image-based component anomaly detection, an earlier PCB experiment, and limited historical browser integration evidence. It does not yet have a validated inspection product. Current reference matching and 100-feature Anomalib PaDiM were fitted separately for RGB cable gland and KSDD2, calibrated on normal-only data and evaluated once on their held-out memberships. All four original evaluations missed the provisional 90% recall requirement. Original false-alarm, coverage, warm CPU latency and sampled memory point estimates passed the other provisional screens.

The strongest current result is KSDD2 PaDiM: 84/110 defects detected (76.36% recall), 77/894 normal false alarms (8.61%), image AUROC 0.93214 and warm p95 0.36171 s. Cable-gland PaDiM detected only 11/87 defects. High pixel-ranking metrics do not establish adequate image detection. Stress tests expose lighting sensitivity and blur-related false alarms.

New read-only audit checks verified 124 frozen-run/phase/gallery hash references and 7,132 manifest-linked image/mask files with no missing files or hash mismatches; recounted all four current original confusion matrices; matched all eight frozen dependency versions; and syntax-parsed 53 Python files. No training, model inference, held-out rerun, dependency installation or browser/server launch occurred. Historical tests are not represented as newly rerun tests.

A major continuation risk is preservation: HEAD ends at Stage 1, while substantial Stage 2–5 implementation is modified/untracked, and datasets/models/runs are intentionally ignored. A clone of HEAD cannot reproduce the local experiment. Stale documentation/status fields, local repacked dependencies, missing Stage 5 pixel AP/raw maps, unknown physical-product identities, absent independent review and unmeasured human benefit remain important gaps.

## Table of contents

1. [Audit identity and scope](#1-audit-identity-and-scope)
2. [Project objective and status](#2-project-objective-and-status)
3. [Development timeline](#3-development-timeline)
4. [Data inventory and preparation](#4-data-inventory-and-preparation)
5. [Model and experiment inventory](#5-model-and-experiment-inventory)
6. [Evaluation results](#6-evaluation-results)
7. [Software tests, integration and failed attempts](#7-software-tests-integration-and-failed-attempts)
8. [Failure and limitation analysis](#8-failure-and-limitation-analysis)
9. [Reproducibility and technical gaps](#9-reproducibility-and-technical-gaps)
10. [Conclusions and prioritized next steps](#10-conclusions-and-prioritized-next-steps)
11. [File-to-purpose index](#11-file-to-purpose-index)
12. [Detailed metric and artifact appendices](#12-detailed-metric-and-artifact-appendices)

## 1. Audit identity and scope

- Repository: `C:/Users/laksh/OneDrive/Desktop/Tech4Bharat`.
- Branch: `stage-1-safe-acquisition`.
- HEAD: `cbd1c45169199d0075ea57a21b596b7911402ae9`.
- Working tree was dirty before this audit. Existing code/data/configuration/output files were preserved; this report is the only new deliverable.
- Current run: `components/runs/frozen-20261019T041652Z-9c825801/`.
- Freeze SHA256: `49cecd4d593536eecfba7974f61968570581b44885606ab97d424ba5d86cff40`.

Reviewed root briefs/plans/catalogues; historical `experiment/` scripts, protocol, source/split metadata, prediction JSON, checkpoints, raw-map presence and browser assets; current `components/` source/tests/configs/locks, source/audit manifests, states/metadata, Stage 3/4 results, Stage 5 phases and logs; Git history and ignore rules. No project notebooks were found outside dependency environments. This is a script-based project.

**Evidence labels:** “Verified” means directly inspected bytes/code/Git or a new deterministic audit check. “Recorded” identifies historical output or narrative, not freshly rerun execution. “Inference” is interpretation, not experimentally confirmed causality. “Not recorded” and “Could not verify” indicate missing support. Source line citations refer to the local working tree, which is newer than committed HEAD.

The audit did not deserialize model states into executable models, relabel datasets, independently inspect every image visually, rebuild environments, rerun functional tests or benchmark hardware. External provider release/checksum authentication, current hosting restrictions, remote visibility and current external documentation were not freshly checked. Local hashes establish consistency against local records, not independent authenticity or timestamps. Complete unrecorded experimental history cannot be proven absent.

## 2. Project objective and status

The intended product is a narrow human-reviewed visual inspection assistant for small manufacturers: flag suspicious component images, show attention maps, persist the person's disposition, count inspection coverage honestly and produce batch records for supervisor/owner review. Manufacturer demand, buyer acceptance, actual baseline defect-miss rates and inspection-time savings have not been established. Challenge-context statistics are not project measurements.

The implemented approach models normal RGB appearance separately per recipe. Audited roles feed reference banks or frozen pretrained features plus spatial Gaussian fitting. Normal-only calibration sets thresholds; one-time final evaluation checks sensitivity, false alarms and CPU resource use. Scores are distances, not probabilities. Attention intensity is not defect severity. XYZ data are not used. There is no reliable subtype naming, cause diagnosis, electrical/functional testing or automated batch acceptance.

Evidence: `Tech4Bharat_Codex_Execution_Plan.md`, fixed decisions/global constraints; `TEAM_PROJECT_BRIEF.md:13`; `components/docs/IMPLEMENTATION_PROGRESS.md`, final checkpoint; actual CLI in `components/src/component_inspector/cli.py`.

| Workstream | Status | Evidence / boundary |
|---|---|---|
| Earlier PCB1 reference/compact PaDiM | Implemented, fitted, calibrated, test/stress evaluated; no-go | `experiment/results/summary.json` |
| Earlier ONNX/browser experiment | Limited integration succeeded after initial WASM failure | 10 selected desktop fixtures, not full browser validation |
| Environment and safe acquisition, Stages 0–1 | Completed locally | Diagnostics, isolated environment, bounded import/inventories |
| Current audit and data roles, Stage 2 | Completed locally | 354 cable RGB +3,335 usable KSDD2; 2 extra quarantine records |
| Current B0, Stage 3 | Implemented/fitted/development-tested/finally evaluated | Separate 16-reference banks |
| Current PaDiM P0, Stage 4 | Implemented/fitted/development-tested/finally evaluated | 128 fit normals per recipe, frozen pretrained backbone |
| Frozen calibration/test/stress/report, Stage 5 | Completed, no-go | Four original evaluations, 12 paired stress combinations |
| Metal-nut recipe | Deferred after source-access blocker and cable amendment | Acquisition compatibility/configuration, not real model results |
| P1 native compact fallback on current datasets | Proposed, not exercised | Historical PCB code is separate evidence |
| Broader simulation/digital twin/causal work | Earlier proposal/research; excluded or superseded | No implemented simulator or causal model found |
| FastAPI/SQLite/React component app | Planned; Stages 6–10 stopped | `application/__init__.py` and `web/README.md` are scaffold/boundary |
| Human timing study | Exercise prepared historically; actual completion unverified | No demonstrated workload benefit or real owner approval |
| Deployment/factory/phone validation | Not established | Historical localhost server is not factory integration |
| PatchCore/EfficientAD/DRAEM/supervised alternatives | Proposed/discussed only | No project fit/checkpoint/evaluation found |

## 3. Development timeline

Git author dates and explicit saved UTC markers support the entries below. Dates printed in documents establish a dated claim, not exact execution time. No later commits timestamp individual Stage 2–5 edits. Developer hours and exact duration of the overall project are Not recorded.

| Date / ordering basis | Change and reason | Evidence |
|---|---|---|
| 17 Oct 2026, dated protocol/report | PCB1 experiment tested CPU reference/compact PaDiM and optional browser feasibility; both detector screens failed | `experiment/PROTOCOL.md`; `experiment/artifacts/EXPERIMENT_REPORT.md` |
| 17–18 Oct, plans | Broader workbench/simulation narrowed to gated component research. Maintained PaDiM introduced; older rotation-bank/tiling proposals superseded | `TEAM_PROJECT_BRIEF.md`; reviewed build plan |
| 18 Oct 13:19:20 IST | Initial research/component scaffold commit | `d30447b11b5b7f48242e69994967f5afd8a2e6ba` |
| 18 Oct 14:13:58 IST | Stage 0 verification documentation | `b36d144b6a56382fb92fb615e6e305f8ed873380` |
| 18 Oct 14:30:15 IST, source ledger | KSDD2 acquired from official redirected source; metal nut required provider access flow | `components/docs/DATA_SOURCES.md` |
| 18 Oct 14:55:17 IST | Bounded acquisition/provenance committed; current HEAD | `cbd1c45169199d0075ea57a21b596b7911402ae9` |
| 18 Oct 22:06:48 IST, import timestamp | User-supplied cable archive imported; scope amendment replaced metal nut with cable gland RGB | `CABLE_GLAND_SCOPE.md`; `DATA_SOURCES.md` |
| 19 Oct, ledger ordering | Mask/duplicate audits and deterministic roles implemented; incorrect cable mask foreground assumption corrected before accepting final audit | `STAGE2_AUDIT_SUMMARY.json`; implementation ledger |
| 19 Oct, ledger ordering | Geometry/ROI and B0 implemented; initial sorted-key dataset order superseded by D1-first protocol-order development run | Stage 3 old `0fa409f4...` vs selected `4a1602d3...` |
| 19 Oct, logs/ledger | CPU Anomalib installed, pinned timm weights loaded; Windows publish denial addressed; initial launcher-only memory evidence invalidated and corrected process-tree fits rerun | Stage 4 old `e12ea8b5...` vs selected `38fc0d1f...` |
| 19 Oct 09:46:55.559 IST | Freeze payload created before calibration/final predictions | `freeze.json` `created_at_utc=2026-10-19T04:16:55.559007+00:00` |
| 19 Oct 09:47:13.619 IST | Calibration phase began | `calibration_started.json` |
| 19 Oct 09:56:34.055 IST | Original evaluation began after calibration; no-go followed | `evaluate_started.json`; `evaluation_complete.json` |
| 19 Oct 10:08:03.814 IST | Stress began after original evaluation; report/supplement followed | `stress_started.json`; `stress_complete.json`; `SUPPLEMENT.json` |
| 19 Oct, this audit | Read-only technical inspection and report | Newly performed checks in §7 |

Freeze directory name contains `20261019T041652Z`; actual freeze payload creation was three seconds later. Completion files do not record exact completion wall-clock timestamps. PCB exact run time and all intermediate development attempt times Could not be verified. Only three commits are reachable across local Git refs; none records Stage 2–5 as a committed snapshot.

## 4. Data inventory and preparation

### 4.1 Historical VisA PCB1

Source is `BrachioLab/visa` mirror revision `d185c42584b49f1df81fe12bde627559ed88d483`, PCB1 only (`experiment/download.py`; `experiment/data/download_manifest.json`). Original VisA byte equivalence is unverified. Recorded source terms are CC BY 4.0. Original defect-name taxonomy is documentation; mirror masks are binary 0/255 and do not support measured subtype recall.

`experiment/results/leakage_audit.json` records 904 source-training normals, 100 source-test normals and 100 source-test anomalies. Custom experimental allocation: reference 100 normal; calibration 100 normal +20 anomalies; final test 100 normal +80 anomalies; unused 704 normal. No detected duplicate pairs/quarantine. Physical board IDs unavailable. Seed 4217 governs deterministic appearance-group ordering. This is not official VisA benchmark membership because 20 source-test anomalies were reassigned to calibration.

Full-frame bilinear RGB resize to 224×224, float [0,1]; reference method additionally centers spatial mean per channel. Historical quality gate abstains for minimum side <224, mean luminance outside [0.05,0.95], clipping fraction >0.50 or Laplacian variance <20. Threshold selection used normal and defective calibration samples, maximizing recall under ≤10% normal FPR, with stated tie breaks. This differs from current normal-only calibration.

### 4.2 Current datasets and roles

| Dataset | Local version identity | Official usable membership | Audited experimental roles |
|---|---|---|---|
| MVTec 3D-AD cable_gland RGB | Archive SHA256 `63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed`; provider release unknown | 223 train normal, 23 validation normal; test 21 normal +87 anomalous | Fit role 129 images/128 groups, 128 canonical consumed; 5 unused fit; development 68; calibration 44; test 108; B0 refs 16 |
| KSDD2 | Archive SHA256 `edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8`; provider release ID not established | Train 2,085 normal +246 anomalous; test 894 normal +110 anomalous | Fit 128; unused fit 1,123; development 663 (417 normal +246 anomalous); calibration 417; test 1,004; 2 extra quarantine records; B0 refs 16 |

Cable archive: 354,399,396 bytes, 820 extracted files, 759,081,950 extracted bytes. KSDD2 archive: 853,126,555 bytes, 6,677 files, 852,612,567 extracted bytes. Cable content-addressed copy ends `.tar` but retains original XZ-compressed bytes; actual format is detected by content. Raw roots are `components/data/raw/mvtec_3d_cable_gland/cable_gland/` and `components/data/raw/ksdd2/`.

Audit checks decoded-pixel identity, masks and conservative near pairs: pHash distance ≤2 and 64×64 RGB thumbnail MAE ≤2/255. Two same-label cable training pairs were grouped. Opposite-label near candidates are preserved to avoid deleting tiny defects. No cross-official-partition contamination was recorded. Appearance grouping is not physical independence. All 3,691 candidate image records lack verified physical identities.

Cable class mapping: 0 good, 255 bent, 254 cut, 253 hole, 252 thread. Correct foreground value is validated before binary nonzero evaluation. Earlier 255-only logic would have quarantined 66 valid defects; that incomplete audit was rejected/corrected. KSDD2 labels come from masks. Extra `train/10301 (copy).png` and `train/10301_GT (copy).png` lack valid pairs under the schema and are quarantined, not extra normals. Five `split_weakly_*.pyb` files remain inert.

Normal groups split deterministically 60/20/20 before a 128-fit-group cap. Cable official validation is development-only. KSDD2's 246 training anomalies are development-only. Neither enters normal fitting/calibration. Official final-test membership is preserved after audit. Cable has no development defects; borrowing its observed test defects for supervised training would change the experiment's roles.

Effective preprocessing: EXIF orientation, RGB conversion, bilinear aspect-preserving letterbox, zero padding and float [0,1]. Cable H256 W256, 0°; KSDD2 H256 W640, 90° clockwise resolved from training inventory. Valid ROI excludes padding from image scoring; maps restore original coordinates. No augmentation, crop, registration or rotation search. XYZ/calibration files are not model inputs.

Evidence: `components/docs/STAGE2_AUDIT.md`; `data/adapters.py`, `audit.py`, `split.py`, `prepare.py`; `vision/geometry.py`. Full immutable manifest:
`components/data/manifests/stage2/b769d8598112008728d354145526815eceeaaf32e477861af22c25a541a1ecc9/manifest.json`.
Manifest SHA256 `f1fdd9113745565f00827529f475989192465562e881478a3f6d3d31f59b4863`; membership hash `6d24d51d1858c67b08d14340998310c8a4e419ab7f232270d4f322a7bcd53ca2`. Corrected repeated preparations match those identities.

### 4.3 Provenance and researched alternatives

Cable download origin was recovered from local Windows Zone.Identifier and recorded in `components/docs/CABLE_GLAND_SOURCE_RECONCILIATION.json`. Early-review notice remains; provider current release/checksum is not authenticated. Local hashes identify bytes and do not grant commercial rights. Active datasets are recorded as CC BY-NC-SA 4.0; no commercial/redistribution authorization is established by this audit.

`DATASET_CATALOGUE.md`, `COMPONENT_DATASETS.md` and the team brief research additional assets including causalAssembly, PerfCam and SECOM. No completed causal, event replay, manufacturing-risk, textile or maintenance model experiment was found. Metal nut remains a deferred acquisition/configuration lineage, not an evaluated detector dataset.

## 5. Model and experiment inventory

### 5.1 Model comparison and lifecycle

| Model / meaningful variant | Lifecycle established | Exact implementation/configuration | Checkpoint/output evidence |
|---|---|---|---|
| PCB-B0, mean-centered nearest RGB reference | Implemented, bank fitted, calibrated/tested/stressed | `experiment/inspection.py:80`, `run.py`, `PROTOCOL.md` | `experiment/models/reference_bank.npy`; `results/reference_*.json` |
| PCB-P0, native compact PaDiM / ResNet18 ImageNet1K V1 /50 features | Implemented, Gaussian fitted; frozen backbone; evaluated; limited ONNX/browser integration | `experiment/inspection.py:44`, `:58`; `experiment/run.py` | `experiment/models/resnet18-f37072fd.pth`, `padim.pt`, `padim.onnx` |
| Current B0 / cable | Implemented, 16-normal bank fitted, development/calibration/test/stress | `components/src/component_inspector/vision/reference.py`, `develop.py`; cable YAML | Selected `bank.npy`/metadata; exact paths in appendix |
| Current B0 / KSDD2 | Same method, separate fit/threshold/evaluation | Same source, `ksdd2_surface.yaml` | Separate `bank.npy`/metadata |
| Current P0 / cable, Anomalib 2.7.0 PaDiM /timm ResNet18 /100 features | Implemented, 128-normal Gaussian fit, development/calibration/test/stress | `vision/padim_adapter.py`, `spike.py`, `spike_worker.py`; protocol/backend/cable YAML | Selected `state.pt`/metadata; pretrained safetensors |
| Current P0 / KSDD2 | Same architecture, separate Gaussian/model state | Same source; separate geometry/config | Separate selected `state.pt`/metadata |
| B0 initial dataset-order development run | Executed, superseded; not a separate final model qualification | `components/outputs/stage3/0fa409f4dea68ac3fb1e83cafbca03ac212ac5f4c412ac787f4ba26601baa1da/results.json` | Retained output/model lineage |
| Initial P0 feasibility memory run | Real fits/development outputs; memory evidence invalidated | `components/outputs/stage4/e12ea8b5a6396872a8e26e6f-8f32aeb2/report.json` | Retained per-recipe states; not selected at freeze |
| P1 current-recipe native compact PaDiM /50 channels | Proposed fallback only; no current fit/test established | `components/configs/backend-targets.yaml`; reviewed plan | No current P1 checkpoint found |
| Random-backbone PaDiM fixtures | Software tests only, not accuracy experiments | `components/tests/test_padim.py` | Temporary test state, not research model |
| Metal-nut recipe | Deferred proposal/configuration | `components/configs/mvtec_metal_nut.yaml` | No real trained/evaluated state established |
| Rotation-bank/tiling designs | Historical proposals superseded; execution not verified | Plan supersession text | No executed matching variant established |
| PatchCore/EfficientAD/DRAEM/supervised segmentation | Alternatives only | PatchCore mentioned in reviewed plan; others discussed in chat | No source/checkpoint/result found |
| YOLO/SAM/DINO/FastFlow/LLM classifier/fine-tuned model | No project experiment established | Installed-library modules/citations are not usage evidence | Not recorded |

### 5.2 Exact architecture/settings and changes

**PCB-B0:** 100 references, per-channel spatial mean centering to 0.5, nearest normal by global squared RGB difference, sigma-1 residual blur, mean of top approximately 1% pixels. Full-frame 224-square resize. No optimizer/epochs/loss applies to stored-bank fitting.

**PCB-P0:** torchvision ResNet18 original ImageNet1K V1 weights (`resnet18-f37072fd.pth`); layer1/2/3; concatenate 448 features, nearest upsample to 56×56, NumPy seed-4217 subset of 50 channels. Gaussian covariance +0.01 I; Mahalanobis distance; bilinear upsample to 224×224, separable sigma-4 reflected smoothing, maximum image score. Fit embeds batches up to 8 from 100 reference normals. Mean [0.485,0.456,0.406], std [0.229,0.224,0.225] embedded in graph. No gradient fine-tuning. ONNX opset 17 exports normalization/Gaussian/score/map.

**Current B0:** ≤16 references; raw RGB without historical mean centering, valid-ROI nearest-reference mean squared residual, chunk ≤4; normalized sigma-1 smoothing prevents padded edges suppressing valid anomalies; mean of ceil(1% valid pixels). This is a materially different brightness response from PCB-B0.

**Current P0:** Anomalib 2.7.0 low-level `PadimModel(backbone='resnet18', layers=['layer1','layer2','layer3'], n_features=100)`. Separate spatial Gaussian per recipe; regularization 0.01 I plus library stabilization 1e-5 I; bilinear map resize, sigma-4 smoothing, valid-ROI raw maximum. Parameters frozen, feature-extractor BN held in eval during statistics fit. Seed 4217; CPU batch 1; four Torch threads, one interop thread in workers; zero loader workers; no augmentation. No supervised optimizer/learning rate/epochs/training loss was used.

Current pretrained provider `timm/resnet18.a1_in1k`, revision `491b427b45c94c7fb0e78b5474cc919aff584bbf`, SHA256 `80c49dee3da4822c009c5a7fe591e9223c5a2cfcf95a4067ca4dfb5a7b89c612`; local `components/models/backbones/resnet18_a1/model.safetensors`. Used feature keys loaded strictly; unused classifier/layer4 keys disclosed. ImageNet normalization occurs once. Classifier default crop/interpolation metadata does not override full-frame inspection geometry. Current timm weights are not identical to historical torchvision V1 weights.

Current freeze versions: Python 3.12.14 recorded; torch 2.10.0+cpu, torchvision 0.25.0+cpu, Anomalib 2.7.0, timm 1.0.30, NumPy 2.2.4, SciPy 1.15.2, Pillow 12.1.0, scikit-learn 1.9.1. Eight package versions match the audit interpreter's installed metadata. Historical PCB used torch 2.6.0+cpu, torchvision 0.21.0+cpu, Pillow 11.1.0, ONNX 1.17.0, ONNX Runtime 1.21.0 (complete snapshot in `experiment/results/environment.json`).

Historical protocol records Windows 11, AMD Ryzen 7 260 (8 physical/16 logical cores), RTX 5050/integrated graphics detected but CPU selected. No GPU/phone inference was established. Hardware was not freshly benchmarked.

### 5.3 Fitting and development evidence

Selected B0 run is `4a1602d3105cf3655039231a5d4a6a4aabd5fdf12bd178b9e93791294e136338`; corrected P0 run is `38fc0d1f768474c62ecf4aa3-0ac3bf5e`. Exact artifact paths, timings, sizes and hashes are appended below from saved summaries/freeze.

B0 development: cable 68 queries, fit 0.18478 s, warm p95 0.05672 s; KSDD2 663 queries, fit 0.18088 s, p95 0.16176 s. Run peak sampled RSS 208,347,136 bytes. Exact bank save/reload parity recorded.

P0: cable 128 fit normals, 68 development queries, fit 12.46870 s, p95 0.15851 s, peak owned-tree RSS 1,627,570,176 bytes. KSDD2 128 fit normals, 663 queries, fit 27.92246 s, p95 0.36986 s, peak 3,173,732,352 bytes. Reload parity atol=rtol=1e-5. Gaussian mean/inverse shapes cable [100,4096]/[4096,100,100]; KSDD2 [100,10240]/[10240,100,100]. These are development feasibility outputs with null thresholds/flags, not validation accuracy/recall.

Historical PCB reference fit 2.02050 s; PaDiM initialization 0.31870 s, fit 2.14128 s, native run 224.74961 s excluding setup/export/artifact rendering. Source: `experiment/results/environment.json`. Developer effort and every earlier attempt duration are Not recorded.

## 6. Evaluation results

Detailed original, calibration, stress, intervals, resource and subtype results are appended automatically from saved JSON in §12. That appendix is part of this report, not a pointer requiring inference reruns.

Recall counts every expected defect (technical rejects are misses); normal FPR uses accepted/scored normals; coverage means scored images, not human-inspected products. Precision depends on prevalence. AUROC/image AP are ranking diagnostics, not threshold qualification. Pixel metric is macro per-anomalous-image pixel AUROC, not pooled pixel AUROC, pixel AP, IoU or Dice.

Accuracy and F1 in comparison tables are **new arithmetic from saved confusion counts**, not recorded optimization metrics: accuracy=(TP+TN)/N; F1=2TP/(2TP+FP+FN). No training/validation loss curves, mAP, Dice or IoU were recorded. Historical PCB AUROC/AP were not recorded. Development runs were uncalibrated. Do not compare cross-dataset accuracy/AP as equivalent tasks: prevalence differs (PCB 44.44%, cable 80.56%, KSDD2 10.96%), alongside weights/geometry/channels/reference counts/calibration rules.

Current normal calibration uses k=ceil(0.9(n+1)), strict score > kth score; cable n=44/k=41, KSDD2 n=417/k=377. Thresholds: cable reference 0.30545759201049805, PaDiM 51.89221954345703; KSDD2 reference 0.017160728573799133, PaDiM 47.66035842895508. Display ranges derive from equal-image weighted 99.5th percentile normal map values, sampled up to 10,000 pixels/image. Scores/maps are not pooled across methods/recipes. No threshold was chosen from final labels.

Historical calibration uses 100 normals +20 defects and yields thresholds reference 0.2463272660970688, compact PaDiM 11.106827735900879. It is a different operating-point protocol; historical/current recall differences are not a controlled model ablation.

All four current original units have zero technical rejects and 100% coverage; recall failed every screen. Original FPR ≤10%, warm p95 ≤5 s, peak sampled owned-tree RSS ≤4 GiB passed as provisional point estimates. Cable 1/21 FPR has Wilson upper bound ~22.67%; KSDD2 FPR upper bounds also exceed 10%. Passing point estimates is not a population guarantee.

Warm p95 excludes initialization and first measured image. P0 load/init in original runs took ~30–38 s, separate from warm latency. Future app startup would need explicit handling. RSS is sampled every 50 ms over owned process tree; shared pages may be double-counted and brief peaks missed. It is neither exact allocation maximum nor GPU memory.

Stress is paired transformed copies of existing test images, not new validation. KSDD2 B0 brightness ×0.6 flags all 894 normals, ×1.4 flags 893; its 100% stress recall is not useful inspection. KSDD2 P0 blur FPR 14.09% and brighter FPR 10.51% fail the FPR point screen. Current stress timing excludes original file decode, so it is not directly comparable to original pipeline timing. Code attaches original-image quality warnings before transforms; these do not measure warning sensitivity to transformed inputs.

Current P0 cable AUROC 0.73071/pixel AUROC 0.97358 and KSDD2 AUROC 0.93214/pixel AUROC 0.97647 do not override insufficient fixed-threshold recall. Cable image AP 0.91780 is not 91.8% detection recall. Cable verified folder counts are bent21/cut22/hole22/thread22; PaDiM detects 3/3/5/0 respectively. KSDD2 has no verified subtype folders. Bootstrap uses seed 4217 / 1,000 appearance-group replicates; physical independence remains unverified.

## 7. Software tests, integration and failed attempts

### 7.1 Historical software verification

Final saved component test output is `components/.cache/stage5-verified-tests.txt`: **99 passed, 45 warnings in 60.16 s**. This was inspected, not rerun. Similarly named `stage5-final-tests.txt` instead records 97 passed/54.70 s; `stage5-full-tests.txt` records 97/55.20 s. Earlier PCB report records 13 tests; counts from repeated suites should not be summed.

Test families inspected:

- Acquisition: ZIP/TAR/XZ roundtrip; traversal, Windows device/ADS/path rejection; links/special files/collisions; CRC/truncation; bounded payload/metadata/expansion; forged ZIP directory; redirect/download restrictions; no overwrite; source reuse/tamper; expected blocked-access exits; precise transient Windows publication retries.
- Dataset roles: RGB-only enumeration; mask-derived labels, missing/shape/class-ID validation; exact decoded duplicates; opposite-label near candidates; deterministic roles; group/canonical fit restrictions; cross-partition/role guards; immutable manifests and changed raw bytes.
- Geometry/models: EXIF/rotation/grayscale, letterbox edge/padding preservation, original-coordinate restoration; finite shapes; nearest-reference/chunk parity; saved bank hashes/recipe mismatch; once-only normalization; frozen backbone/BN; valid ROI maximum; channel identities; saved P0 raw-map/score parity.
- Evaluation: finite-sample calibration minimum n/ties/nonfinite inputs; equal-image display weighting; rejected/missing denominator accounting; Wilson intervals; frozen file/version graph; changed-model rejection; phase prerequisites; repeated workers through alternate output folders; ordered fit IDs; escaped gallery and missing categories; saved-prediction subtype/bootstrap supplement.
- Resources: oversized child termination and nested-child allocations detecting launcher-only measurement.

These are implementation invariants, not empirical detector qualification. Random-backbone fixtures are not pretrained accuracy evidence. Warnings mentioning DINO-related Anomalib imports do not establish that a DINO detector was run. No component frontend build, API concurrency/load, database or factory acceptance test was found.

### 7.2 Historical ONNX, browser and review integration

`experiment/run.py` exports the SAME fitted compact PaDiM, opset17, including normalization, Gaussian state, score and map. Saved model is 43,125,528 bytes. `experiment/results/export_parity.json` compares 10 selected fixtures, maximum native/ONNX score difference 4.76837e-6.

`browser_attempt1.json` preserves failure: WASM module specifier `node_modules/onnxruntime-web/dist/ort-wasm-simd-threaded.mjs` could not resolve. Asset-path correction, without detector/threshold change, led to `browser_results.json` complete=true. Recorded Chrome155/Windows/WASM one-thread results: flags agree 10/10, exact-tensor maximum score difference ~3.81470e-6, independently resized image score difference ~0.00204849. Pixel resize difference ~1/255, not bit-identical.

Recorded local model fetch 170.3 ms, session initialization 500.7 ms, decode/resize/inference median 330.55 ms and p95 441.91 ms. Selected desktop localhost fixture results do not establish phone/internet/sustained-load/all-test performance. Browser quality gate was not ported. A historical 25 MiB static-host asset cap was a packaging concern, not proof of attempted/successful deployment; current host restrictions were not rechecked.

`experiment/serve.py` binds127.0.0.1 and serves local prototypes, accepting browser-results output locally. `experiment/accounting.py` exercises a fictional six-product ledger: duplicates, multiple photos, rework/history, unresolved/uninspected status and blocked owner approval. Real benchmark observations were placed in a visibly fictional sample batch ledger. No actual owner signature exists in this evidence.

`review_exercise.html` prepares 24 disjoint images: 12 manual and 12 assisted, each six normal/six defective. Manual-first order, artificial 50% prevalence, unmatched difficulty/precomputed hints and no capture time limit interpretation. Actual participant completion/timing and human benefit Could not be verified. Feedback questions were prepared; no manufacturer/buyer outreach established.

### 7.3 Failed, corrected and superseded attempts

| Issue / attempt | Evidence | Disposition / limit |
|---|---|---|
| Dependency download failure and zero-byte wheel placeholders | Implementation ledger; offline dependency record | Repacked installed NumPy/SciPy verified RECORD bytes; not original provider wheels |
| freia0.2 all-wheel restriction | Ledger preflight; `stage4-lock.txt` | Allowed pure-Python source dependency; retained torch/torchvision wheels; not model failure |
| Cable mask foreground interpretation | Ledger Stage2; class-ID regression | Wrong assumption would quarantine66 defects; incomplete run stopped, mapping corrected before accepted preparation |
| Opposite-label near-duplicate grouping fixture | Ledger/tests | First fixture inadequate; textured regression added; tiny defects preserved instead of auto-removal |
| B0 sorted dataset order | Initial Stage3 output vs selected output | Development-only initial run superseded by protocol-order run |
| WinError5 directory publication | `stage4-full-tests.txt` 1failed/79passed; repeat also1failed/79passed | Added bounded precise-error retry with destination no-overwrite recheck; subsequent suite passed |
| Launcher-only RSS | Old P0 run `e12ea8b5a6396872a8e26e6f-8f32aeb2` | ~4 MiB invalid feasibility reading; nested-child regression caught issue; process-tree monitor/refits used for final freeze |
| Initial missing module/invariant RED tests | `stage2-red.txt`, `stage3-red.txt`, `stage5-metrics-red.txt` | Development regressions followed by implementation; not additional final-test failures |
| Worker repeat via alternate output | Ledger Stage5; worker tests | Per-run per-method unit reservations added before original evaluation |
| Freeze fit-ID ordering mismatch | `stage5-freeze-error.txt` | Same128/128 membership but different ordering; expected worker order corrected and tested; no refit/holdout tuning |
| Missing pixel AP/raw test map archive | Frozen worker and final reporting | Explicitly unavailable; no inference rerun to recover secondary outputs |
| Detector operating gate | Original JSON/screens/stress | Honest no-go retained; application stopped |

Some intermediate redirected JSON files are empty (`stage2-prepare-first.json`, `stage5-freeze-result.json`), so they cannot substantiate successful runs. Corrections are supported by inspected code/logs/ledger, not newly reproduced regressions. Markers prevent accidental repetition within a recorded run; they are not OS-enforced immutability or proof no unrecorded run ever happened.

### 7.4 New checks performed during this audit

1. Git status/branch/HEAD/all refs inspected: three reachable commits; existing dirty state preserved.
2. Rehashed 124 references across freeze graph, calibration/evaluation/stress completion graphs and supplement gallery hashes: zero missing/mismatch. Non-gallery graph reads totalled 1,864,232,941 bytes. These references include source archives, model states, source/config/manifest bytes and results. References need not be unique files.
3. Independently rehashed 7,132 unique manifest-linked image/mask paths: zero missing/mismatch. This covers records with saved image/mask hashes, not every inert archive payload or quarantined unpaired file.
4. Joined saved original predictions to manifest truth and recounted all four confusion matrices: exact agreement with saved TP/FN/FP/TN. No model called.
5. Matched all eight frozen installed package-version metadata entries. No clean reinstall/import smoke test was performed.
6. Parsed 53 project Python source/test/tool files with `ast.parse`: no syntax errors. This is not functional testing.
7. Enumerated states/metadata/outputs and historical PCB 360 raw test maps. No project notebooks found outside environments.

No pytest, model fitting, model inference, original/stress rerun, server/browser launch or ONNX re-export was performed. Historical metrics remain historical execution evidence. Report generation and arithmetic on saved counts are new audit work.

## 8. Failure and limitation analysis

### 8.1 Individual approach assessments

- **PCB reference:** missed65/80 defects despite low FPR. Brightness/blur stress retains poor sensitivity. Confirmed inadequate threshold-level sensitivity, underlying cause unproven.
- **PCB compact PaDiM:** missed35/80 and15% normal false alarms. Better recall than reference, fails recall and FPR. Export/browser parity largely succeeds within10-fixture scope; do not call this an export failure.
- **Cable B0:** missed84/87, image AUROC0.52819 near chance on this sample; blur detects zero defects; brightening flags normal and defective images. Unsuitable frozen configuration.
- **Cable P0:** missed76/87, thread recall0/22, improved image/pixel ranking but inadequate fixed-threshold detection. High AP reflects a defect-heavy test population as well as rankings.
- **KSDD2 B0:** missed36/110; near-universal false alarms after brightness changes. Original result better than cable, robustness inadequate.
- **KSDD2 P0:** strongest current sensitivity/ranking, but26/110 misses;84/161 original flags correct. Blur/brighter FPR exceed screen. Useful research baseline, not qualified inspector.
- **Acquisition, role/hash guards, stored-state parity, bounded CPU execution and limited historical browser inference:** successful within measured scope; detector failures do not make every engineering component unsuccessful.
- **P1, metal nut, alternative models, supervised approaches:** no supporting current performance experiment; success/failure unknown.

### 8.2 Causes, confidence and discriminating tests

Confidence concerns the explanation; observed counts themselves are recorded outputs verified by recount. Future tests below require development data or a newly frozen experiment, not tuning this observed holdout.

| Factor / status | Supporting evidence | Confidence | Concrete confirming/rejecting test |
|---|---|---|---|
| Current raw-RGB B0 brightness sensitivity | No mean-centering; KSDD2 both brightness transforms flag nearly every normal | High for sensitivity; not full original-miss explanation | Development-normal score shifts under controlled exposure; one predefined normalization candidate at matched FPR |
| Small-defect detail lost by resizing | PCB224 square/current cable256; recorded small cable FN; no resolution ablation | Plausible, low–moderate | Development-only resolution/crop comparison stratified by mask defect size; lock before fresh confirmation |
| Pose variation challenges spatial matching/Gaussians | Spatial models; reported threaded/edge responses; no pose measurements | Plausible, moderate | Quantify development pose/score relationship and compare one fixed registration method |
| Incomplete normal variability representation | 16 references/128 fit normals; many KSDD2 normals unused; no learning curve | Plausible, low–moderate | Development reference/fit-count curve with same validation operating point and process-tree memory |
| Inadequate operating point | KSDD2 P0 AUROC.932 vs recall.764 at normal-only cutoff | High for operating-point inadequacy; cause of overlap unknown | Separate labelled development recall/FPR frontier, then fresh untouched confirmation of preselected cutoff |
| Representation/model suitability | Cable B0 AUROC.528/P0.731; misses across folders | High for imperfect separation; mechanism uncertain | One predefined patch-model or supervised comparator on allowed development data plus fresh confirmation |
| Preprocessing mismatch | Current tests check normalization/geometry; historical browser differs~1/255 | Confirmed small browser difference, little evidence it caused original misses | Non-holdout tensor/map parity across intended native/export paths |
| Remaining label/data error | Two invalid KSDD2 pairs and cable mask bug corrected; final count recount matches | Confirmed resolved issues; remaining causal role unverified | Blind expert development-label review/source-mask reconciliation; version any correction |
| Class imbalance | KSDD2 normal-heavy; cable final test defect-heavy | High for metric interpretation, not training failure | Per-class PR/ROC/count reporting and separately measured factory prevalence; do not invent weighted-loss fix for Gaussian fit |
| Leakage/physical dependence | Appearance groups disjoint; physical IDs absent | Unresolved, leakage not proven | Product/lot/capture identities and group-disjoint confirmation split |
| Overfitting/underfitting | No supervised optimization/learning curves | Could not diagnose | Development learning curves/score distributions; avoid claiming epoch/LR failure |
| Factory domain shift | Benchmark captures plus synthetic perturbations only | High that transfer unvalidated; actual degradation unknown | Representative permitted captures across devices/lighting/lots/operators with expert labels |
| Quality/abstention validity | Current warning-only diagnostics; stress warnings computed pre-transform | High implementation limitation | Separate capture-quality set validating retake criteria; count rejected defects as misses |
| Runtime integration | Current speed/coverage passed; memory monitor corrected | High for measured local pipeline; production unknown | Later bounded API/load/timeout/state tests if app scope resumes |

No evidence supports assigning low recall to too many/few epochs, wrong learning rate, absent GPU, confirmed leakage or corrupt final labels. Qualitative examples in `STAGE5_FAILURE_ANALYSIS.md` are implementing-agent observations, not new independent visual review here. Potential causes remain hypotheses until discriminating experiments.

## 9. Reproducibility and technical gaps

### 9.1 Preservation and environment

HEAD ends at acquisition. Many later source/test/doc/tool files and locks are untracked; root plans/CLI/acquisition/configuration are modified. Frozen hashes bind current bytes to outputs but do not create a distributable committed release. Dataset/model/run artifacts are ignored; clone-only reproduction is unavailable. Exact working-tree state must be preserved separately from HEAD.

NumPy2.2.4/SciPy1.15.2 were repacked from installed RECORD-verified bytes after network failures; original provider wheel equivalence is not claimed. `components/docs/OFFLINE_AUDIT_DEPENDENCIES.json`, `.cache/offline-wheels/PROVENANCE.json`, `requirements-audit.lock` and offline wheels are essential. Zero-byte placeholders cannot reconstruct dependencies. Exact P0 lock/extra is needed beyond base pyproject dependencies; evaluation imports include scikit-learn. A clean environment rebuild was not performed here.

`doctor` defaults `models_ready=False` and `datasets_downloaded=False`; code explicitly labels these conservative defaults, not full source/model audits. Package-version parity does not prove installation portability. Sampled RSS is not exact high-water memory. Frozen model loaders reject state/recipe/code/version changes; preserve the matching runtime.

### 9.2 Contradictions and stale documentation

| Location | Problem | Evidence-based resolution |
|---|---|---|
| Root README/execution-plan opening/DATA_SOURCES/CABLE_GLAND_SCOPE | Say audit/fitting remain pending | Later source/manifests/results prove completed research; app still stopped |
| components README command list/CLI opening docstring | Only doctor/acquire claimed; model commands unavailable | Actual CLI also implements prepare/develop/spike/freeze/calibrate/evaluate/stress/report; generic fit/train/serve absent |
| protocol YAML/frozen embedded protocol | draft_not_frozen, implementation_status pending | Outer freeze and completed phases establish execution; stale copied descriptive fields |
| Recipe YAML and effective recipe statuses | acquired_not_audited_or_split/not_evaluated; source KSDD2 rotation/hash unresolved | Frozen effective geometry/hash resolved through manifest; saved result establishes evaluation |
| Cable source notice status | pending_before_freeze persists | Explicit freeze source_resolution permits identified local research with provider-release uncertainty |
| SUPPLEMENT cable defect_folder_note | Incorrect copied sentence says KSDD2 has no verified defect folders | Cable folder metric object correctly contains bent/cut/hole/thread; metadata copy-text defect |
| Stage2 checkpoint wording | Model work has not run | Historical stage-local statement, not current status |
| Earlier simulation conditional-go vs current no-go | Could imply completed or approved reliable app | Earlier proposal; current gate stops dependent app; no simulator implemented |
| Multiple saved states/results | Superseded fits can look authoritative | Only corrected Stage3/4 paths referenced in freeze belong to final evaluation |
| Similar pytest filenames | final97 vs verified99 | 99/60.16s belongs specifically to stage5-verified-tests.txt |
| Historical PCB rerun instructions | run.py writes/replaces results and lacks current global phase guard | Never rerun observed final holdout as new validation or harmless report regeneration |
| Browser package.json ^1.21.0 | Range rather than exact dependency | package-lock pins resolved graph; npm ci, not manifest alone, reproduces it |

Do not edit frozen files in place solely to tidy stale statuses: their hashes would change. Add an external current-status layer or a future version after preserving this experiment. No such existing code/config changes were made by this audit.

### 9.3 Missing or unverifiable evidence

- Stage5 pixel AP and full raw test maps: unavailable, not zero. Historical PCB maps do not fill this gap.
- Supervised loss curves/epochs/fine-tuning checkpoints: not applicable to implemented statistical fits; no proposed supervised experiment recorded.
- Independent review, expert label audit, product/lot IDs, representative factory/phone captures, buyer feedback and human timing: not established.
- All-test browser accuracy, current P0 export, operational component API/UI/database, load/security/deployment tests: not completed/verified.
- Provider-authenticated current cable release/checksum, original PCB byte equivalence: unresolved. KSDD2 hash identifies local bytes, not provider attestation.
- Exact execution time/order of every intermediate attempt, complete later Git chronology and measured developer effort: unavailable.
- Local self-consistent hashes cannot prove no malicious rewriting or unrecorded runs; appearance grouping cannot prove physical independence.

### 9.4 Existing entry points and reproduction boundaries

PowerShell from repository root; commands below were not executed as model experiments during audit.

```powershell
# Diagnostics / CLI inventory
.\components\.venv-p0\Scripts\python.exe -m component_inspector.cli doctor --json
.\components\.venv-p0\Scripts\python.exe -m component_inspector.cli --help
# Software tests, when separately requested; tests create temporary fixtures/cache
.\components\.venv-p0\Scripts\python.exe -m pytest components/tests -q -p no:cacheprovider
```

Acquisition/source-reuse commands are in `components/docs/REPRODUCE.md`. They can publish files/download/reverify inventories and are not needed for merely reading saved results. `prepare --config components/configs/protocol.yaml` audits/publishes manifests.

Existing fitting entry points for a separately authorized development run:

```powershell
.\components\.venv-p0\Scripts\python.exe -m component_inspector.cli develop --config components/configs/protocol.yaml --manifest components/data/manifests/stage2/b769d8598112008728d354145526815eceeaaf32e477861af22c25a541a1ecc9/manifest.json
.\components\.venv-p0\Scripts\python.exe -m component_inspector.cli spike --config components/configs/protocol.yaml --manifest components/data/manifests/stage2/b769d8598112008728d354145526815eceeaaf32e477861af22c25a541a1ecc9/manifest.json --weights components/models/backbones/resnet18_a1/model.safetensors
```

Functions: `vision/develop.py:develop_reference`, `spike.py:spike`, `spike_worker.py:run`; trusted inference primitives `reference.py:load_model/predict_array`, `padim_adapter.py:PadimAdapter.load/predict_array`. They consume prepared RGB/ROI, not a finished public API. Generic `fit`/`serve` is not implemented.

`freeze` takes config/manifest/baseline-summary/candidate-summary/reconciliation. Current `calibrate`, `evaluate`, `stress --run components/runs/frozen-20261019T041652Z-9c825801` phases are already consumed. **Do not delete markers or bypass workers to rerun them.** `report --run ...` regenerates saved-output artifacts but writes files; it is unnecessary for this audit. `components/tools/stage5_supplement.py` analyzes existing predictions without loading models.

Historical sequence in `experiment/README.md`: download.py →prepare.py →run.py →make_artifacts.py →summarize.py. `run.py` fits, scores original holdout, exports and overwrites results; it is not read-only report regeneration. Historical local UI: `.\experiment\.venv\Scripts\python.exe experiment/serve.py`; browser graph restore uses `npm --prefix experiment/browser ci --ignore-scripts --no-audit --no-fund`. Exercise grading requires a real participant response path. No human response/time should be fabricated.

## 10. Conclusions and prioritized next steps

1. **Preserve implementation/evidence first.** Review/commit existing Stage2–5 source/tests/docs/locks as appropriate, and create a manifest-backed backup of ignored data/model/run assets under suitable access restrictions. HEAD alone is insufficient. Do not publish restricted raw data to fix preservation.
2. **Publish accurate current status outside frozen files.** Resolve README/CLI/status contradictions, identify selected/superseded states and note copied supplement text without altering old numerical identities.
3. **Verify clean-environment reproducibility separately from model accuracy.** Reconstruct exact dependencies/offline wheels and exercise stored-state parity on allowed non-holdout fixtures. Do not repeat original inference to fill missing metrics.
4. **Choose one bounded development question.** Cable: test resolution/pose/normal variability on allowed development material, obtaining new labelled defects where necessary. KSDD2: one supervised/mixed-supervision or PatchCore comparator can be investigated using permitted development labels. These are hypotheses, not expected success. Retain recall/FPR/resource constraints.
5. **Obtain untouched confirmation evidence with physical/lot IDs.** Current holdouts are observed. Capture representative devices/lighting/lots, expert labels and group-disjoint roles before model/threshold choice. Public benchmark success alone cannot validate factory transfer.
6. **Predeclare complete outputs next time.** Persist raw maps or explicit bounded policy, intended pixel AP, exact per-image/aggregate metrics, cold/warm/load timing, memory scope, state/dependency hashes, roles and failed attempts. Missing secondary outputs and earlier RSS defect show why.
7. **Add independent review and real human evaluation.** Review metric/role logic, then use a counterbalanced measured capture/retake/review/report exercise before time-saving claims. Human dispositions must come from humans.
8. **Resume application only under justified scope.** No final detector qualified. A research replay/failure-analysis artifact is different from a reliable inspector. Require new frozen confirmation meeting operating targets with uncertainty and robustness before final-model or factory-readiness claims.

Engineering foundations—safe source handling, accounting, hashes, CPU inference and saved-state checks—substantially work. Defect sensitivity remains a separate unmet requirement. The evidence supports continued bounded research, not declaring the intended inspection product successful.

## 11. File-to-purpose index

The generated index below cites exact local repository-relative paths and line numbers. Large referenced artifacts exist locally but many are ignored and absent from a clone. All line numbers refer to the audit working tree, not necessarily HEAD.
| Exact file/line | Purpose |
|---|---|
| `README.md:1` | Repository entry point, partly stale |
| `TEAM_PROJECT_BRIEF.md:13` | Historical product/simulation proposal |
| `DATASET_CATALOGUE.md:1` | Researched dataset candidates, not adopted-model evidence |
| `COMPONENT_DATASETS.md:1` | Dataset shortlist |
| `Tech4Bharat_Codex_Execution_Plan.md:17` | Ordered execution contract |
| `Tech4Bharat_Anomaly_Detector_Build_Plan.md:1` | Build decisions/gates, supersession |
| `Tech4Bharat_Anomaly_Detector_Build_Plan_Reviewed.md:194` | Reviewed methods/alternatives/risks |
| `docs/superpowers/plans/2026-10-18-codex-build-playbook.md:1` | Stage prompts and manual gates |
| `experiment/PROTOCOL.md:20` | Historical frozen custom roles/models/screens |
| `experiment/download.py:7` | Pinned PCB mirror/model acquisition |
| `experiment/prepare.py:1` | PCB duplicate audit and roles |
| `experiment/inspection.py:44` | Historical features/PaDiM/reference/quality/metrics |
| `experiment/run.py:5` | Historical fit/test/stress/ONNX pipeline |
| `experiment/make_artifacts.py:1` | Failure/review/sample report generation |
| `experiment/summarize.py:1` | Historical readable report generation |
| `experiment/accounting.py:1` | Fictional ledger rules |
| `experiment/serve.py:1` | Local browser assets/results recording |
| `experiment/grade_review.py:1` | Grades actual participant response file |
| `experiment/test_accounting.py:1` | Accounting fixture checks |
| `experiment/test_evaluation.py:1` | Historical evaluation invariants |
| `experiment/requirements-lock.txt:1` | Historical dependency pins |
| `experiment/browser/index.html:1` | ONNX browser fixture parity page |
| `experiment/browser/package-lock.json:1` | Resolved browser dependency graph |
| `experiment/data/download_manifest.json:1` | Source/model byte hashes and URLs |
| `experiment/data/splits.json:1` | Exact historical roles |
| `experiment/results/summary.json:1` | Historical calibration/test/stress metrics |
| `experiment/results/environment.json:1` | Historical environment and fit duration |
| `experiment/results/leakage_audit.json:1` | Historical counts/group uncertainty |
| `experiment/results/frozen_thresholds.json:1` | Historical threshold identities |
| `experiment/results/export_parity.json:1` | Native ONNX parity evidence |
| `experiment/results/browser_attempt1.json:1` | WASM module path failure |
| `experiment/results/browser_results.json:1` | Successful limited browser fixture results |
| `experiment/artifacts/EXPERIMENT_REPORT.md:1` | Historical conclusions and limits |
| `components/pyproject.toml:1` | Package dependencies and CLI |
| `components/requirements-setup.lock:1` | Setup dependencies |
| `components/requirements-audit.lock:1` | Audit dependencies/offline hashes |
| `components/requirements-p0.lock:1` | Current CPU backend dependency graph |
| `components/configs/protocol.yaml:1` | Seed/roles/gates and stale statuses |
| `components/configs/mvtec_3d_cable_gland_rgb.yaml:1` | Cable recipe/source/geometry |
| `components/configs/ksdd2_surface.yaml:1` | Surface recipe, unresolved source rotation resolved in manifest |
| `components/configs/mvtec_metal_nut.yaml:1` | Deferred recipe |
| `components/configs/backend-targets.yaml:1` | P0 and unexercised P1 targets |
| `components/docs/IMPLEMENTATION_PROGRESS.md:241` | Execution/correction ledger |
| `components/docs/DATA_SOURCES.md:1` | Source provenance and historical blockers |
| `components/docs/CABLE_GLAND_SCOPE.md:1` | User-selected RGB scope amendment |
| `components/docs/CABLE_GLAND_SOURCE_RECONCILIATION.json:1` | Download origin/notice/provider uncertainty |
| `components/docs/OFFLINE_AUDIT_DEPENDENCIES.json:1` | Repacked wheel identities |
| `components/docs/STAGE2_AUDIT_SUMMARY.json:1` | Roles/counts/manifest identities |
| `components/docs/STAGE3_DEVELOPMENT_SUMMARY.json:1` | Selected reference-development evidence |
| `components/docs/STAGE4_FEASIBILITY_SUMMARY.json:1` | Selected corrected P0 feasibility evidence |
| `components/docs/STAGE5_REPORT.md:1` | Final no-go summary |
| `components/docs/STAGE5_FAILURE_ANALYSIS.md:1` | Recorded examples/stress/limits |
| `components/docs/STAGE5_VERIFICATION.json:1` | Historical verification/access identities |
| `components/docs/REPRODUCE.md:148` | Commands/one-time rules |
| `components/src/component_inspector/cli.py:69` | Actual implemented commands |
| `components/src/component_inspector/contracts.py:1` | Data contracts |
| `components/src/component_inspector/data/acquire.py:1` | Bounded extraction/download/source validation |
| `components/src/component_inspector/data/adapters.py:9` | RGB/mask enumeration |
| `components/src/component_inspector/data/audit.py:17` | Labels/masks/duplicate integrity |
| `components/src/component_inspector/data/split.py:26` | Seeded roles and access guards |
| `components/src/component_inspector/data/prepare.py:1` | Content-addressed manifest publication |
| `components/src/component_inspector/vision/geometry.py:8` | EXIF/rotation/ROI/map restoration |
| `components/src/component_inspector/vision/reference.py:21` | B0 scoring/state/hash checks |
| `components/src/component_inspector/vision/develop.py:49` | B0 development orchestration |
| `components/src/component_inspector/vision/padim_adapter.py:34` | P0 fit/load/predict/normalization |
| `components/src/component_inspector/vision/spike.py:20` | P0 resource orchestration |
| `components/src/component_inspector/vision/spike_worker.py:24` | Pinned pretrained fitting worker |
| `components/src/component_inspector/vision/resources.py:9` | Owned-tree RSS/time monitor |
| `components/src/component_inspector/vision/media.py:21` | Bounded actual decoding/quality warnings |
| `components/src/component_inspector/evaluation/freeze.py:74` | Hash/version graph and phase locking |
| `components/src/component_inspector/evaluation/calibration.py:6` | Quantile/display scale |
| `components/src/component_inspector/evaluation/phase_worker.py:48` | One-time original/calibration/stress worker |
| `components/src/component_inspector/evaluation/metrics.py:18` | Counts/rates/Wilson/AUROC/AP |
| `components/src/component_inspector/evaluation/runner.py:27` | Sequential workers/completion/gates |
| `components/src/component_inspector/evaluation/reports.py:1` | Saved-output gallery/report |
| `components/tools/stage5_supplement.py:1` | Saved-prediction subtype/bootstrap supplement |
| `components/src/component_inspector/application/__init__.py:1` | Application placeholder |
| `components/web/README.md:1` | Unimplemented frontend boundary |
| `components/.cache/stage5-verified-tests.txt:1` | Actual saved final99-test log |
| `components/.cache/stage5-freeze-error.txt:1` | Fit-ID ordering freeze rejection |
| `components/.cache/stage4-full-tests.txt:1` | Historical Windows publish failure |

### Test file index

| File | Test functions (parameterization can increase executed count) |
|---|---|
| components/tests/test_calibration.py | test_finite_sample_quantile_n8_fails_n9_max_and_n44_rank41; test_calibration_ties_nonfinite_and_equal_image_display_weights |
| components/tests/test_doctor.py | test_doctor_reports_actual_environment_without_claiming_model_readiness; test_unimplemented_training_command_fails_instead_of_implying_training_ran |
| components/tests/test_evaluation_worker.py | test_calibration_worker_excludes_test_and_final_worker_is_single_use |
| components/tests/test_experiment_report.py | test_gallery_escapes_identifiers_and_discloses_missing_examples |
| components/tests/test_experiment_runner.py | test_gate_uses_counts_latency_memory_and_missing_denominators; test_completion_graph_rejects_tampered_calibration |
| components/tests/test_freeze.py | test_fit_identity_respects_record_order_for_padim_not_selection_list_order; test_frozen_file_graph_detects_changed_model_before_phase_access; test_evaluation_requires_finished_calibration_and_cannot_start_twice |
| components/tests/test_geometry.py | test_letterbox_aspect_roi_and_inverse_edge_mark; test_fixed_clockwise_rotation_and_grayscale_roundtrip; test_exif_orientation_applied_once_and_bad_inputs_rejected |
| components/tests/test_media.py | test_dark_blurry_image_is_decoded_with_warnings_not_rejected; test_bad_bytes_and_encoded_overflow_have_specific_rejections; test_gif_and_too_small_images_are_not_scored_as_normal |
| components/tests/test_metrics.py | test_confusion_ranking_and_rejected_defect_denominators; test_null_denominators_and_missing_predictions_are_not_fake_perfect_scores; test_wilson_interval_contains_rate_and_small_normal_sample_is_uncertain |
| components/tests/test_padim.py | test_padim_normalizes_once_and_keeps_backbone_frozen_in_eval; test_padim_requires_fit_finite_shapes_and_uses_only_valid_roi_max; test_padim_saved_state_preserves_channels_map_scores_and_rejects_mismatch |
| components/tests/test_reference.py | test_reference_chooses_nearest_bank_entry_and_score_is_in_rgb_squared_units; test_padding_cannot_raise_score_and_chunked_matches_unchunked; test_reference_rejects_nan_or_shape_mismatch; test_reference_saved_bank_parity_and_hash_recipe_mismatch_rejected; test_development_runner_follows_protocol_order_and_never_scores_test_records |
| components/tests/test_resources.py | test_resource_supervisor_rejects_oversized_child_and_records_exit; test_resource_supervisor_measures_descendants_not_only_python_launcher |
| components/tests/test_sources.py | test_zip_roundtrip_inventory_hashes_and_no_overwrite; test_tar_roundtrip; test_rejects_unsafe_portable_paths_without_partial_output; test_rejects_tar_links_and_special_files; test_rejects_zip_symlink; test_rejects_collisions; test_rejects_bounded_expansion_and_member_count; test_rejects_corrupt_archive; test_local_archive_records_provenance_samples_inventory_and_is_idempotent; test_invalid_training_sample_does_not_publish_raw; test_mvtec_network_request_records_form_blocker_without_downloading; test_cli_acquire_runs_actual_local_import_and_unsupported_commands_still_fail; test_rejects_invalid_dataset_category_combinations; test_download_rejects_overflow_truncation_forms_and_untrusted_destinations; test_download_streams_bytes_and_records_redirect; test_reimport_detects_raw_tampering; test_cli_blocked_access_has_nonzero_exit_and_no_false_success; test_tar_gzip_expansion_is_bounded_even_for_hidden_pax_metadata; test_zip_member_limit_checked_before_opening_payloads; test_rejects_forged_oversized_zip_directory_before_parser_allocation; test_crc_failure_removes_partial_extraction; test_reimport_rejects_unrecorded_raw_files; test_download_refuses_to_overwrite_existing_archive; test_xz_tar_from_local_provider_archive; test_tiny_tar_member_limit_does_not_reject_header_blocks; test_zip_directory_limit_does_not_trust_forged_entry_count; test_cable_gland_import_selects_training_rgb_and_keeps_separate_identity; test_cable_gland_cli_records_access_blocker_without_archive; test_cable_gland_rejects_wrong_categories; test_transient_windows_publish_denial_retries_without_overwriting |
| components/tests/test_splits.py | test_cable_adapter_only_rgb_preserves_validation_and_pairs_test_mask; test_ksdd2_labels_come_from_masks_and_missing_masks_are_quarantined; test_audit_rejects_defect_without_mask_and_dimension_mismatch; test_split_deterministic_counts_normal_only_and_validation_development; test_duplicate_group_cannot_cross_fit_calibration_or_official_partitions; test_access_guard_blocks_test_calibration_defects_and_unused_fit; test_audit_groups_identical_pixels_even_when_png_bytes_differ; test_prepare_publishes_immutable_manifest_and_detects_raw_tampering; test_near_normal_and_tiny_defect_are_not_discarded_as_duplicate_label_conflict; test_cable_class_id_masks_are_valid_binary_anomaly_regions |
| components/tests/test_stage5_supplement.py | test_secondary_metrics_use_saved_flags_and_verified_folders_only |

## 12. Detailed metric and artifact appendices

Values below are copied from saved aggregate JSON, except explicitly derived accuracy/F1 and new saved-row accounting. Per-image source paths identify exact experiment units. Null or absent values must not be interpreted as zero. No model was called to populate these tables.

### 12.1 Original experiment results comparison

| Dataset/run | Method | TP/FN/FP/TN | Recall | Normal FPR | Precision | Accuracy derived | F1 derived | p95 s | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| Historical PCB1 | reference | 15/65/1/99 | 18.750% | 1.000% | 93.750% | 63.333% | 31.250% | 0.1556517650001069 | experiment/results/summary.json |
| Historical PCB1 | padim | 45/35/15/85 | 56.250% | 15.000% | 75.000% | 72.222% | 64.286% | 0.09733005000020967 | experiment/results/summary.json |
| mvtec_3d_cable_gland_rgb | reference | 3/84/1/20 | 3.448% | 4.762% | 75.000% | 21.296% | 6.593% | 0.05797066999803064 | components/runs/frozen-20261019T041652Z-9c825801/evaluation/mvtec_3d_cable_gland_rgb_reference/mvtec_3d_cable_gland_rgb_reference.json |
| mvtec_3d_cable_gland_rgb | padim | 11/76/1/20 | 12.644% | 4.762% | 91.667% | 28.704% | 22.222% | 0.16827192999480758 | components/runs/frozen-20261019T041652Z-9c825801/evaluation/mvtec_3d_cable_gland_rgb_padim/mvtec_3d_cable_gland_rgb_padim.json |
| ksdd2_surface | reference | 74/36/75/819 | 67.273% | 8.389% | 49.664% | 88.944% | 57.143% | 0.14822098000295228 | components/runs/frozen-20261019T041652Z-9c825801/evaluation/ksdd2_surface_reference/ksdd2_surface_reference.json |
| ksdd2_surface | padim | 84/26/77/817 | 76.364% | 8.613% | 52.174% | 89.741% | 61.993% | 0.3617116000066744 | components/runs/frozen-20261019T041652Z-9c825801/evaluation/ksdd2_surface_padim/ksdd2_surface_padim.json |

All six original rows have 100% scoring coverage/no rejects. Historical PCB PaDiM also failed FPR. All current original rows failed recall; other current provisional screens passed. Accuracy is dominated by class composition and is not the acceptance gate.

### 12.2 Current original metrics, intervals and resources

#### mvtec_3d_cable_gland_rgb / reference / original

Source: `components/runs/frozen-20261019T041652Z-9c825801/evaluation/mvtec_3d_cable_gland_rgb_reference/mvtec_3d_cable_gland_rgb_reference.json:1`.

| Metric | Recorded value |
|---|---|
| accepted_normal_fpr | {"denominator":21,"numerator":1,"rate":0.047619047619047616,"wilson_95":[0.008455987809826399,0.22669360074122563]} |
| anomaly_coverage | {"denominator":87,"numerator":87,"rate":1.0,"wilson_95":[0.9577124930558795,0.9999999999999999]} |
| counts | {"FN":84,"FP":1,"TN":20,"TP":3,"rejected_anomalies":0,"rejected_normals":0} |
| coverage | {"denominator":108,"numerator":108,"rate":1.0,"wilson_95":[0.9656526402534428,0.9999999999999999]} |
| false_flags_all_normals | {"denominator":21,"numerator":1,"rate":0.047619047619047616,"wilson_95":[0.008455987809826399,0.22669360074122563]} |
| normal_coverage | {"denominator":21,"numerator":21,"rate":1.0,"wilson_95":[0.8453609810751531,1]} |
| observed_prevalence | {"denominator":108,"numerator":87,"rate":0.8055555555555556,"wilson_95":[0.7209648351663079,0.8691562227663517]} |
| precision | {"denominator":4,"numerator":3,"rate":0.75,"wilson_95":[0.30064184258240184,0.9544127391902995]} |
| ranking_scored_only | {"auroc":0.5281882868089764,"average_precision":0.8203815606363262,"n":108,"population":"scored subset only"} |
| recall | {"denominator":87,"numerator":3,"rate":0.034482758620689655,"wilson_95":[0.011795820527505975,0.09654082386874399]} |
| pixel_diagnostic | {"images":87,"metric":"macro per-anomalous-image pixel AUROC, not pooled dataset pixel AUROC","value":0.9048964892036404} |
| init_seconds | 0.024839699995936826 |
| cold_pipeline_seconds | 0.07326940000348259 |
| warm_p95_pipeline_seconds | 0.05797066999803064 |
| resource record (components/runs/frozen-20261019T041652Z-9c825801/evaluation/mvtec_3d_cable_gland_rgb_reference_resources.json) | {"elapsed_seconds":18.078000000008615,"max_observed_processes":3,"measurement_scope":"owned process tree RSS sum","peak_sampled_rss_bytes":190263296,"returncode":0,"rss_cap_bytes":4294967296,"sample_interval_seconds":0.05,"status":"completed","time_cap_seconds":3600} |

New saved-row diagnostic count (not inference): warning occurrences `{}`. Warnings do not exclude rows.

#### mvtec_3d_cable_gland_rgb / padim / original

Source: `components/runs/frozen-20261019T041652Z-9c825801/evaluation/mvtec_3d_cable_gland_rgb_padim/mvtec_3d_cable_gland_rgb_padim.json:1`.

| Metric | Recorded value |
|---|---|
| accepted_normal_fpr | {"denominator":21,"numerator":1,"rate":0.047619047619047616,"wilson_95":[0.008455987809826399,0.22669360074122563]} |
| anomaly_coverage | {"denominator":87,"numerator":87,"rate":1.0,"wilson_95":[0.9577124930558795,0.9999999999999999]} |
| counts | {"FN":76,"FP":1,"TN":20,"TP":11,"rejected_anomalies":0,"rejected_normals":0} |
| coverage | {"denominator":108,"numerator":108,"rate":1.0,"wilson_95":[0.9656526402534428,0.9999999999999999]} |
| false_flags_all_normals | {"denominator":21,"numerator":1,"rate":0.047619047619047616,"wilson_95":[0.008455987809826399,0.22669360074122563]} |
| normal_coverage | {"denominator":21,"numerator":21,"rate":1.0,"wilson_95":[0.8453609810751531,1]} |
| observed_prevalence | {"denominator":108,"numerator":87,"rate":0.8055555555555556,"wilson_95":[0.7209648351663079,0.8691562227663517]} |
| precision | {"denominator":12,"numerator":11,"rate":0.9166666666666666,"wilson_95":[0.646120088858883,0.9851349055950829]} |
| ranking_scored_only | {"auroc":0.7307060755336617,"average_precision":0.9177963533247315,"n":108,"population":"scored subset only"} |
| recall | {"denominator":87,"numerator":11,"rate":0.12643678160919541,"wilson_95":[0.07208952879445547,0.21237814880747352]} |
| pixel_diagnostic | {"images":87,"metric":"macro per-anomalous-image pixel AUROC, not pooled dataset pixel AUROC","value":0.9735787172802076} |
| init_seconds | 30.488262400001986 |
| cold_pipeline_seconds | 0.17692220000026282 |
| warm_p95_pipeline_seconds | 0.16827192999480758 |
| resource record (components/runs/frozen-20261019T041652Z-9c825801/evaluation/mvtec_3d_cable_gland_rgb_padim_resources.json) | {"elapsed_seconds":77.23500000000058,"max_observed_processes":3,"measurement_scope":"owned process tree RSS sum","peak_sampled_rss_bytes":857022464,"returncode":0,"rss_cap_bytes":4294967296,"sample_interval_seconds":0.05,"status":"completed","time_cap_seconds":3600} |

New saved-row diagnostic count (not inference): warning occurrences `{}`. Warnings do not exclude rows.

#### ksdd2_surface / reference / original

Source: `components/runs/frozen-20261019T041652Z-9c825801/evaluation/ksdd2_surface_reference/ksdd2_surface_reference.json:1`.

| Metric | Recorded value |
|---|---|
| accepted_normal_fpr | {"denominator":894,"numerator":75,"rate":0.08389261744966443,"wilson_95":[0.06745219655553857,0.10389371012910413]} |
| anomaly_coverage | {"denominator":110,"numerator":110,"rate":1.0,"wilson_95":[0.9662560647018358,0.9999999999999999]} |
| counts | {"FN":36,"FP":75,"TN":819,"TP":74,"rejected_anomalies":0,"rejected_normals":0} |
| coverage | {"denominator":1004,"numerator":1004,"rate":1.0,"wilson_95":[0.996188429452794,0.9999999999999999]} |
| false_flags_all_normals | {"denominator":894,"numerator":75,"rate":0.08389261744966443,"wilson_95":[0.06745219655553857,0.10389371012910413]} |
| normal_coverage | {"denominator":894,"numerator":894,"rate":1.0,"wilson_95":[0.9957214508386147,1]} |
| observed_prevalence | {"denominator":1004,"numerator":110,"rate":0.10956175298804781,"wilson_95":[0.0917092070311931,0.13039066479052952]} |
| precision | {"denominator":149,"numerator":74,"rate":0.4966442953020134,"wilson_95":[0.41746244831818713,0.5759948242849672]} |
| ranking_scored_only | {"auroc":0.8942749644091926,"average_precision":0.6963800599951372,"n":1004,"population":"scored subset only"} |
| recall | {"denominator":110,"numerator":74,"rate":0.6727272727272727,"wilson_95":[0.5805088757294906,0.7532886738947798]} |
| pixel_diagnostic | {"images":110,"metric":"macro per-anomalous-image pixel AUROC, not pooled dataset pixel AUROC","value":0.8083666393038815} |
| init_seconds | 0.06696359999477863 |
| cold_pipeline_seconds | 0.1857179999933578 |
| warm_p95_pipeline_seconds | 0.14822098000295228 |
| resource record (components/runs/frozen-20261019T041652Z-9c825801/evaluation/ksdd2_surface_reference_resources.json) | {"elapsed_seconds":152.04700000000594,"max_observed_processes":3,"measurement_scope":"owned process tree RSS sum","peak_sampled_rss_bytes":223010816,"returncode":0,"rss_cap_bytes":4294967296,"sample_interval_seconds":0.05,"status":"completed","time_cap_seconds":3600} |

New saved-row diagnostic count (not inference): warning occurrences `{}`. Warnings do not exclude rows.

#### ksdd2_surface / padim / original

Source: `components/runs/frozen-20261019T041652Z-9c825801/evaluation/ksdd2_surface_padim/ksdd2_surface_padim.json:1`.

| Metric | Recorded value |
|---|---|
| accepted_normal_fpr | {"denominator":894,"numerator":77,"rate":0.08612975391498881,"wilson_95":[0.06946397062011714,0.10633706559847908]} |
| anomaly_coverage | {"denominator":110,"numerator":110,"rate":1.0,"wilson_95":[0.9662560647018358,0.9999999999999999]} |
| counts | {"FN":26,"FP":77,"TN":817,"TP":84,"rejected_anomalies":0,"rejected_normals":0} |
| coverage | {"denominator":1004,"numerator":1004,"rate":1.0,"wilson_95":[0.996188429452794,0.9999999999999999]} |
| false_flags_all_normals | {"denominator":894,"numerator":77,"rate":0.08612975391498881,"wilson_95":[0.06946397062011714,0.10633706559847908]} |
| normal_coverage | {"denominator":894,"numerator":894,"rate":1.0,"wilson_95":[0.9957214508386147,1]} |
| observed_prevalence | {"denominator":1004,"numerator":110,"rate":0.10956175298804781,"wilson_95":[0.0917092070311931,0.13039066479052952]} |
| precision | {"denominator":161,"numerator":84,"rate":0.5217391304347826,"wilson_95":[0.4449748441307706,0.5974902010713241]} |
| ranking_scored_only | {"auroc":0.9321435834858655,"average_precision":0.7430341949560175,"n":1004,"population":"scored subset only"} |
| recall | {"denominator":110,"numerator":84,"rate":0.7636363636363637,"wilson_95":[0.6761922754696253,0.8332881950095244]} |
| pixel_diagnostic | {"images":110,"metric":"macro per-anomalous-image pixel AUROC, not pooled dataset pixel AUROC","value":0.9764694733999199} |
| init_seconds | 38.09777239999676 |
| cold_pipeline_seconds | 0.3496281999978237 |
| warm_p95_pipeline_seconds | 0.3617116000066744 |
| resource record (components/runs/frozen-20261019T041652Z-9c825801/evaluation/ksdd2_surface_padim_resources.json) | {"elapsed_seconds":384.32799999999406,"max_observed_processes":3,"measurement_scope":"owned process tree RSS sum","peak_sampled_rss_bytes":1285394432,"returncode":0,"rss_cap_bytes":4294967296,"sample_interval_seconds":0.05,"status":"completed","time_cap_seconds":3600} |

New saved-row diagnostic count (not inference): warning occurrences `{}`. Warnings do not exclude rows.

### 12.3 Current calibration and phase resources

**mvtec_3d_cable_gland_rgb_reference** — `components/runs/frozen-20261019T041652Z-9c825801/calibration/mvtec_3d_cable_gland_rgb_reference.json:1`.

| Field | Recorded value |
|---|---|
| status | "calibrated_normal_only" |
| expected_images | 44 |
| threshold_record | {"alpha":0.1,"comparison":"strict_greater","empirical_fpr":0.06818181818181818,"k":41,"n":44,"threshold":0.30545759201049805,"ties_at_threshold":1} |
| display_scale | {"degenerate":false,"label":"anomaly intensity - not probability or severity","maximum":0.2304483950138092,"minimum":0.0,"percentile":99.5,"pixel_sample_cap_per_image":10000,"seed":4217,"weighting":"equal_image"} |
| pixel_sampling | "up to 10000 valid pixels per image; generator seed 4217+sorted record index" |
| init_seconds | 0.029566500001237728 |
| artifact_identity | {"artifact_path":"models/mvtec_3d_cable_gland_rgb/reference-4a1602d3105cf3655039231a5d4a6a4aabd5fdf12bd178b9e93791294e136338","backend":"reference","metadata_sha256":"bcff08e4bafd16d03165d022edeadcef5171bc7d2ca0290ef53435664edba72b","state_sha256":"da37d9e7f2d04c680e4c1d69d8fc52f22d032e98194a568963f2f8dbb5d9c54b"} |

Calibration resource: `{"elapsed_seconds":10.452999999994063,"max_observed_processes":3,"measurement_scope":"owned process tree RSS sum","peak_sampled_rss_bytes":189071360,"returncode":0,"rss_cap_bytes":4294967296,"sample_interval_seconds":0.05,"status":"completed","time_cap_seconds":3600}`.

**mvtec_3d_cable_gland_rgb_padim** — `components/runs/frozen-20261019T041652Z-9c825801/calibration/mvtec_3d_cable_gland_rgb_padim.json:1`.

| Field | Recorded value |
|---|---|
| status | "calibrated_normal_only" |
| expected_images | 44 |
| threshold_record | {"alpha":0.1,"comparison":"strict_greater","empirical_fpr":0.06818181818181818,"k":41,"n":44,"threshold":51.89221954345703,"ties_at_threshold":1} |
| display_scale | {"degenerate":false,"label":"anomaly intensity - not probability or severity","maximum":32.475852966308594,"minimum":0.0,"percentile":99.5,"pixel_sample_cap_per_image":10000,"seed":4217,"weighting":"equal_image"} |
| pixel_sampling | "up to 10000 valid pixels per image; generator seed 4217+sorted record index" |
| init_seconds | 35.91473400000541 |
| artifact_identity | {"artifact_path":"models/mvtec_3d_cable_gland_rgb/padim-p0-38fc0d1f768474c62ecf4aa3-0ac3bf5e","backend":"anomalib_p0","metadata_sha256":"f69870c8ae3de27b1f4a30ab558a5c3d8d435ae01f808c575e9c10ea05fd91da","state_sha256":"6b1d1acf856cd4052fbc8a2d5055564ea4d16dd954243b12b36347dbbe5d987d"} |

Calibration resource: `{"elapsed_seconds":53.61000000000058,"max_observed_processes":2,"measurement_scope":"owned process tree RSS sum","peak_sampled_rss_bytes":794116096,"returncode":0,"rss_cap_bytes":4294967296,"sample_interval_seconds":0.05,"status":"completed","time_cap_seconds":3600}`.

**ksdd2_surface_reference** — `components/runs/frozen-20261019T041652Z-9c825801/calibration/ksdd2_surface_reference.json:1`.

| Field | Recorded value |
|---|---|
| status | "calibrated_normal_only" |
| expected_images | 417 |
| threshold_record | {"alpha":0.1,"comparison":"strict_greater","empirical_fpr":0.09592326139088729,"k":377,"n":417,"threshold":0.017160728573799133,"ties_at_threshold":1} |
| display_scale | {"degenerate":false,"label":"anomaly intensity - not probability or severity","maximum":0.012435759417712688,"minimum":0.0,"percentile":99.5,"pixel_sample_cap_per_image":10000,"seed":4217,"weighting":"equal_image"} |
| pixel_sampling | "up to 10000 valid pixels per image; generator seed 4217+sorted record index" |
| init_seconds | 0.060328899999149144 |
| artifact_identity | {"artifact_path":"models/ksdd2_surface/reference-4a1602d3105cf3655039231a5d4a6a4aabd5fdf12bd178b9e93791294e136338","backend":"reference","metadata_sha256":"16ccca55e38a3c52ade245387f63254f2a30e6f0e3831e0648101af87dcd7603","state_sha256":"c754e08b781b1cf76daf274159e94101e9908d20fc9a99979de4db2faf1efafb"} |

Calibration resource: `{"elapsed_seconds":65.78099999998813,"max_observed_processes":2,"measurement_scope":"owned process tree RSS sum","peak_sampled_rss_bytes":346259456,"returncode":0,"rss_cap_bytes":4294967296,"sample_interval_seconds":0.05,"status":"completed","time_cap_seconds":3600}`.

**ksdd2_surface_padim** — `components/runs/frozen-20261019T041652Z-9c825801/calibration/ksdd2_surface_padim.json:1`.

| Field | Recorded value |
|---|---|
| status | "calibrated_normal_only" |
| expected_images | 417 |
| threshold_record | {"alpha":0.1,"comparison":"strict_greater","empirical_fpr":0.09592326139088729,"k":377,"n":417,"threshold":47.66035842895508,"ties_at_threshold":1} |
| display_scale | {"degenerate":false,"label":"anomaly intensity - not probability or severity","maximum":24.95188331604004,"minimum":0.0,"percentile":99.5,"pixel_sample_cap_per_image":10000,"seed":4217,"weighting":"equal_image"} |
| pixel_sampling | "up to 10000 valid pixels per image; generator seed 4217+sorted record index" |
| init_seconds | 33.89537849999033 |
| artifact_identity | {"artifact_path":"models/ksdd2_surface/padim-p0-38fc0d1f768474c62ecf4aa3-0ac3bf5e","backend":"anomalib_p0","metadata_sha256":"36a3a354799c1303e9969c42e94c6d0036fa6a099837efddeb5ddede4baec2d7","state_sha256":"b19d4c422578868759460b8d9f1ac252669443517b83fb7ecab8a9395e23365c"} |

Calibration resource: `{"elapsed_seconds":161.64100000000326,"max_observed_processes":3,"measurement_scope":"owned process tree RSS sum","peak_sampled_rss_bytes":1335357440,"returncode":0,"rss_cap_bytes":4294967296,"sample_interval_seconds":0.05,"status":"completed","time_cap_seconds":3600}`.

### 12.4 All paired stress confusion matrices

| Dataset | Method | Transform | TP/FN/FP/TN | Recall | Normal FPR | Coverage |
|---|---|---|---|---|---|---|
| Historical PCB1 | reference | brightness_0.6 | 1/79/1/99 | 1.250% | 1.000% | 100.000% |
| Historical PCB1 | reference | brightness_1.4 | 8/72/1/99 | 10.000% | 1.000% | 100.000% |
| Historical PCB1 | reference | blur_2.0 | 11/69/1/99 | 13.750% | 1.000% | 100.000% |
| Historical PCB1 | padim | brightness_0.6 | 44/36/9/91 | 55.000% | 9.000% | 100.000% |
| Historical PCB1 | padim | brightness_1.4 | 58/22/27/73 | 72.500% | 27.000% | 100.000% |
| Historical PCB1 | padim | blur_2.0 | 44/36/14/86 | 55.000% | 14.000% | 100.000% |
| mvtec_3d_cable_gland_rgb | reference | blur_radius_2 | 0/87/1/20 | 0.000% | 4.762% | 100.000% |
| mvtec_3d_cable_gland_rgb | reference | brightness_0p6 | 2/85/0/21 | 2.299% | 0.000% | 100.000% |
| mvtec_3d_cable_gland_rgb | reference | brightness_1p4 | 52/35/16/5 | 59.770% | 76.190% | 100.000% |
| mvtec_3d_cable_gland_rgb | padim | blur_radius_2 | 10/77/0/21 | 11.494% | 0.000% | 100.000% |
| mvtec_3d_cable_gland_rgb | padim | brightness_0p6 | 10/77/0/21 | 11.494% | 0.000% | 100.000% |
| mvtec_3d_cable_gland_rgb | padim | brightness_1p4 | 13/74/0/21 | 14.943% | 0.000% | 100.000% |
| ksdd2_surface | reference | blur_radius_2 | 44/66/17/877 | 40.000% | 1.902% | 100.000% |
| ksdd2_surface | reference | brightness_0p6 | 110/0/894/0 | 100.000% | 100.000% | 100.000% |
| ksdd2_surface | reference | brightness_1p4 | 110/0/893/1 | 100.000% | 99.888% | 100.000% |
| ksdd2_surface | padim | blur_radius_2 | 90/20/126/768 | 81.818% | 14.094% | 100.000% |
| ksdd2_surface | padim | brightness_0p6 | 77/33/43/851 | 70.000% | 4.810% | 100.000% |
| ksdd2_surface | padim | brightness_1p4 | 88/22/94/800 | 80.000% | 10.515% | 100.000% |

### 12.5 Complete current stress aggregates

#### mvtec_3d_cable_gland_rgb / reference

Source: `components/runs/frozen-20261019T041652Z-9c825801/stress/mvtec_3d_cable_gland_rgb_reference/mvtec_3d_cable_gland_rgb_reference.json:1`.

Worker resource: `{"elapsed_seconds":28.5,"max_observed_processes":3,"measurement_scope":"owned process tree RSS sum","peak_sampled_rss_bytes":180908032,"returncode":0,"rss_cap_bytes":4294967296,"sample_interval_seconds":0.05,"status":"completed","time_cap_seconds":3600}`.

**blur_radius_2**

| Aggregate field | Recorded value |
|---|---|
| metrics | {"accepted_normal_fpr":{"denominator":21,"numerator":1,"rate":0.047619047619047616,"wilson_95":[0.008455987809826399,0.22669360074122563]},"anomaly_coverage":{"denominator":87,"numerator":87,"rate":1.0,"wilson_95":[0.9577124930558795,0.9999999999999999]},"counts":{"FN":87,"FP":1,"TN":20,"TP":0,"rejected_anomalies":0,"rejected_normals":0},"coverage":{"denominator":108,"numerator":108,"rate":1.0,"wilson_95":[0.9656526402534428,0.9999999999999999]},"false_flags_all_normals":{"denominator":21,"numerator":1,"rate":0.047619047619047616,"wilson_95":[0.008455987809826399,0.22669360074122563]},"normal_coverage":{"denominator":21,"numerator":21,"rate":1.0,"wilson_95":[0.8453609810751531,1]},"observed_prevalence":{"denominator":108,"numerator":87,"rate":0.8055555555555556,"wilson_95":[0.7209648351663079,0.8691562227663517]},"precision":{"denominator":1,"numerator":0,"rate":0.0,"wilson_95":[0,0.7934506856227626]},"ranking_scored_only":{"auroc":0.565407772304324,"average_precision":0.8369429026369484,"n":108,"population":"scored subset only"},"recall":{"denominator":87,"numerator":0,"rate":0.0,"wilson_95":[0,0.04228750694412034]}} |

**brightness_0p6**

| Aggregate field | Recorded value |
|---|---|
| metrics | {"accepted_normal_fpr":{"denominator":21,"numerator":0,"rate":0.0,"wilson_95":[0,0.154639018924847]},"anomaly_coverage":{"denominator":87,"numerator":87,"rate":1.0,"wilson_95":[0.9577124930558795,0.9999999999999999]},"counts":{"FN":85,"FP":0,"TN":21,"TP":2,"rejected_anomalies":0,"rejected_normals":0},"coverage":{"denominator":108,"numerator":108,"rate":1.0,"wilson_95":[0.9656526402534428,0.9999999999999999]},"false_flags_all_normals":{"denominator":21,"numerator":0,"rate":0.0,"wilson_95":[0,0.154639018924847]},"normal_coverage":{"denominator":21,"numerator":21,"rate":1.0,"wilson_95":[0.8453609810751531,1]},"observed_prevalence":{"denominator":108,"numerator":87,"rate":0.8055555555555556,"wilson_95":[0.7209648351663079,0.8691562227663517]},"precision":{"denominator":2,"numerator":2,"rate":1.0,"wilson_95":[0.34238022750665303,1]},"ranking_scored_only":{"auroc":0.645320197044335,"average_precision":0.8838005794865098,"n":108,"population":"scored subset only"},"recall":{"denominator":87,"numerator":2,"rate":0.022988505747126436,"wilson_95":[0.006327085105926007,0.0799931801396141]}} |

**brightness_1p4**

| Aggregate field | Recorded value |
|---|---|
| metrics | {"accepted_normal_fpr":{"denominator":21,"numerator":16,"rate":0.7619047619047619,"wilson_95":[0.5490882631704924,0.8937198697736354]},"anomaly_coverage":{"denominator":87,"numerator":87,"rate":1.0,"wilson_95":[0.9577124930558795,0.9999999999999999]},"counts":{"FN":35,"FP":16,"TN":5,"TP":52,"rejected_anomalies":0,"rejected_normals":0},"coverage":{"denominator":108,"numerator":108,"rate":1.0,"wilson_95":[0.9656526402534428,0.9999999999999999]},"false_flags_all_normals":{"denominator":21,"numerator":16,"rate":0.7619047619047619,"wilson_95":[0.5490882631704924,0.8937198697736354]},"normal_coverage":{"denominator":21,"numerator":21,"rate":1.0,"wilson_95":[0.8453609810751531,1]},"observed_prevalence":{"denominator":108,"numerator":87,"rate":0.8055555555555556,"wilson_95":[0.7209648351663079,0.8691562227663517]},"precision":{"denominator":68,"numerator":52,"rate":0.7647058823529411,"wilson_95":[0.6514483202805676,0.8496550897970421]},"ranking_scored_only":{"auroc":0.32512315270935965,"average_precision":0.7368153426052867,"n":108,"population":"scored subset only"},"recall":{"denominator":87,"numerator":52,"rate":0.5977011494252874,"wilson_95":[0.49264741201064083,0.6944918107703932]}} |

#### mvtec_3d_cable_gland_rgb / padim

Source: `components/runs/frozen-20261019T041652Z-9c825801/stress/mvtec_3d_cable_gland_rgb_padim/mvtec_3d_cable_gland_rgb_padim.json:1`.

Worker resource: `{"elapsed_seconds":96.0619999999908,"max_observed_processes":3,"measurement_scope":"owned process tree RSS sum","peak_sampled_rss_bytes":789573632,"returncode":0,"rss_cap_bytes":4294967296,"sample_interval_seconds":0.05,"status":"completed","time_cap_seconds":3600}`.

**blur_radius_2**

| Aggregate field | Recorded value |
|---|---|
| metrics | {"accepted_normal_fpr":{"denominator":21,"numerator":0,"rate":0.0,"wilson_95":[0,0.154639018924847]},"anomaly_coverage":{"denominator":87,"numerator":87,"rate":1.0,"wilson_95":[0.9577124930558795,0.9999999999999999]},"counts":{"FN":77,"FP":0,"TN":21,"TP":10,"rejected_anomalies":0,"rejected_normals":0},"coverage":{"denominator":108,"numerator":108,"rate":1.0,"wilson_95":[0.9656526402534428,0.9999999999999999]},"false_flags_all_normals":{"denominator":21,"numerator":0,"rate":0.0,"wilson_95":[0,0.154639018924847]},"normal_coverage":{"denominator":21,"numerator":21,"rate":1.0,"wilson_95":[0.8453609810751531,1]},"observed_prevalence":{"denominator":108,"numerator":87,"rate":0.8055555555555556,"wilson_95":[0.7209648351663079,0.8691562227663517]},"precision":{"denominator":10,"numerator":10,"rate":1.0,"wilson_95":[0.7224672001371107,0.9999999999999999]},"ranking_scored_only":{"auroc":0.6650246305418719,"average_precision":0.9024205389953928,"n":108,"population":"scored subset only"},"recall":{"denominator":87,"numerator":10,"rate":0.11494252873563218,"wilson_95":[0.06364547795653458,0.19880582049468454]}} |

**brightness_0p6**

| Aggregate field | Recorded value |
|---|---|
| metrics | {"accepted_normal_fpr":{"denominator":21,"numerator":0,"rate":0.0,"wilson_95":[0,0.154639018924847]},"anomaly_coverage":{"denominator":87,"numerator":87,"rate":1.0,"wilson_95":[0.9577124930558795,0.9999999999999999]},"counts":{"FN":77,"FP":0,"TN":21,"TP":10,"rejected_anomalies":0,"rejected_normals":0},"coverage":{"denominator":108,"numerator":108,"rate":1.0,"wilson_95":[0.9656526402534428,0.9999999999999999]},"false_flags_all_normals":{"denominator":21,"numerator":0,"rate":0.0,"wilson_95":[0,0.154639018924847]},"normal_coverage":{"denominator":21,"numerator":21,"rate":1.0,"wilson_95":[0.8453609810751531,1]},"observed_prevalence":{"denominator":108,"numerator":87,"rate":0.8055555555555556,"wilson_95":[0.7209648351663079,0.8691562227663517]},"precision":{"denominator":10,"numerator":10,"rate":1.0,"wilson_95":[0.7224672001371107,0.9999999999999999]},"ranking_scored_only":{"auroc":0.8166392993979201,"average_precision":0.9418418562995111,"n":108,"population":"scored subset only"},"recall":{"denominator":87,"numerator":10,"rate":0.11494252873563218,"wilson_95":[0.06364547795653458,0.19880582049468454]}} |

**brightness_1p4**

| Aggregate field | Recorded value |
|---|---|
| metrics | {"accepted_normal_fpr":{"denominator":21,"numerator":0,"rate":0.0,"wilson_95":[0,0.154639018924847]},"anomaly_coverage":{"denominator":87,"numerator":87,"rate":1.0,"wilson_95":[0.9577124930558795,0.9999999999999999]},"counts":{"FN":74,"FP":0,"TN":21,"TP":13,"rejected_anomalies":0,"rejected_normals":0},"coverage":{"denominator":108,"numerator":108,"rate":1.0,"wilson_95":[0.9656526402534428,0.9999999999999999]},"false_flags_all_normals":{"denominator":21,"numerator":0,"rate":0.0,"wilson_95":[0,0.154639018924847]},"normal_coverage":{"denominator":21,"numerator":21,"rate":1.0,"wilson_95":[0.8453609810751531,1]},"observed_prevalence":{"denominator":108,"numerator":87,"rate":0.8055555555555556,"wilson_95":[0.7209648351663079,0.8691562227663517]},"precision":{"denominator":13,"numerator":13,"rate":1.0,"wilson_95":[0.7719046276458016,0.9999999999999999]},"ranking_scored_only":{"auroc":0.6792556102900931,"average_precision":0.908703608457916,"n":108,"population":"scored subset only"},"recall":{"denominator":87,"numerator":13,"rate":0.14942528735632185,"wilson_95":[0.0894544325105219,0.23904600339282686]}} |

#### ksdd2_surface / reference

Source: `components/runs/frozen-20261019T041652Z-9c825801/stress/ksdd2_surface_reference/ksdd2_surface_reference.json:1`.

Worker resource: `{"elapsed_seconds":414.14100000000326,"max_observed_processes":3,"measurement_scope":"owned process tree RSS sum","peak_sampled_rss_bytes":218292224,"returncode":0,"rss_cap_bytes":4294967296,"sample_interval_seconds":0.05,"status":"completed","time_cap_seconds":3600}`.

**blur_radius_2**

| Aggregate field | Recorded value |
|---|---|
| metrics | {"accepted_normal_fpr":{"denominator":894,"numerator":17,"rate":0.01901565995525727,"wilson_95":[0.011905841065380774,0.030241309134609432]},"anomaly_coverage":{"denominator":110,"numerator":110,"rate":1.0,"wilson_95":[0.9662560647018358,0.9999999999999999]},"counts":{"FN":66,"FP":17,"TN":877,"TP":44,"rejected_anomalies":0,"rejected_normals":0},"coverage":{"denominator":1004,"numerator":1004,"rate":1.0,"wilson_95":[0.996188429452794,0.9999999999999999]},"false_flags_all_normals":{"denominator":894,"numerator":17,"rate":0.01901565995525727,"wilson_95":[0.011905841065380774,0.030241309134609432]},"normal_coverage":{"denominator":894,"numerator":894,"rate":1.0,"wilson_95":[0.9957214508386147,1]},"observed_prevalence":{"denominator":1004,"numerator":110,"rate":0.10956175298804781,"wilson_95":[0.0917092070311931,0.13039066479052952]},"precision":{"denominator":61,"numerator":44,"rate":0.7213114754098361,"wilson_95":[0.5982856941182984,0.8181145610743403]},"ranking_scored_only":{"auroc":0.8792861500915192,"average_precision":0.6419124838110316,"n":1004,"population":"scored subset only"},"recall":{"denominator":110,"numerator":44,"rate":0.4,"wilson_95":[0.31331923819013874,0.4934295488694941]}} |

**brightness_0p6**

| Aggregate field | Recorded value |
|---|---|
| metrics | {"accepted_normal_fpr":{"denominator":894,"numerator":894,"rate":1.0,"wilson_95":[0.9957214508386147,1]},"anomaly_coverage":{"denominator":110,"numerator":110,"rate":1.0,"wilson_95":[0.9662560647018358,0.9999999999999999]},"counts":{"FN":0,"FP":894,"TN":0,"TP":110,"rejected_anomalies":0,"rejected_normals":0},"coverage":{"denominator":1004,"numerator":1004,"rate":1.0,"wilson_95":[0.996188429452794,0.9999999999999999]},"false_flags_all_normals":{"denominator":894,"numerator":894,"rate":1.0,"wilson_95":[0.9957214508386147,1]},"normal_coverage":{"denominator":894,"numerator":894,"rate":1.0,"wilson_95":[0.9957214508386147,1]},"observed_prevalence":{"denominator":1004,"numerator":110,"rate":0.10956175298804781,"wilson_95":[0.0917092070311931,0.13039066479052952]},"precision":{"denominator":1004,"numerator":110,"rate":0.10956175298804781,"wilson_95":[0.0917092070311931,0.13039066479052952]},"ranking_scored_only":{"auroc":0.6934411226357535,"average_precision":0.36468863638604504,"n":1004,"population":"scored subset only"},"recall":{"denominator":110,"numerator":110,"rate":1.0,"wilson_95":[0.9662560647018358,0.9999999999999999]}} |

**brightness_1p4**

| Aggregate field | Recorded value |
|---|---|
| metrics | {"accepted_normal_fpr":{"denominator":894,"numerator":893,"rate":0.9988814317673378,"wilson_95":[0.9936913681275673,0.9998025179440707]},"anomaly_coverage":{"denominator":110,"numerator":110,"rate":1.0,"wilson_95":[0.9662560647018358,0.9999999999999999]},"counts":{"FN":0,"FP":893,"TN":1,"TP":110,"rejected_anomalies":0,"rejected_normals":0},"coverage":{"denominator":1004,"numerator":1004,"rate":1.0,"wilson_95":[0.996188429452794,0.9999999999999999]},"false_flags_all_normals":{"denominator":894,"numerator":893,"rate":0.9988814317673378,"wilson_95":[0.9936913681275673,0.9998025179440707]},"normal_coverage":{"denominator":894,"numerator":894,"rate":1.0,"wilson_95":[0.9957214508386147,1]},"observed_prevalence":{"denominator":1004,"numerator":110,"rate":0.10956175298804781,"wilson_95":[0.0917092070311931,0.13039066479052952]},"precision":{"denominator":1003,"numerator":110,"rate":0.10967098703888335,"wilson_95":[0.09180146906767625,0.1305189934636124]},"ranking_scored_only":{"auroc":0.7794183445190157,"average_precision":0.5240688969060417,"n":1004,"population":"scored subset only"},"recall":{"denominator":110,"numerator":110,"rate":1.0,"wilson_95":[0.9662560647018358,0.9999999999999999]}} |

#### ksdd2_surface / padim

Source: `components/runs/frozen-20261019T041652Z-9c825801/stress/ksdd2_surface_padim/ksdd2_surface_padim.json:1`.

Worker resource: `{"elapsed_seconds":862.5470000000059,"max_observed_processes":2,"measurement_scope":"owned process tree RSS sum","peak_sampled_rss_bytes":1237340160,"returncode":0,"rss_cap_bytes":4294967296,"sample_interval_seconds":0.05,"status":"completed","time_cap_seconds":3600}`.

**blur_radius_2**

| Aggregate field | Recorded value |
|---|---|
| metrics | {"accepted_normal_fpr":{"denominator":894,"numerator":126,"rate":0.14093959731543623,"wilson_95":[0.11966383809569674,0.16528787170476106]},"anomaly_coverage":{"denominator":110,"numerator":110,"rate":1.0,"wilson_95":[0.9662560647018358,0.9999999999999999]},"counts":{"FN":20,"FP":126,"TN":768,"TP":90,"rejected_anomalies":0,"rejected_normals":0},"coverage":{"denominator":1004,"numerator":1004,"rate":1.0,"wilson_95":[0.996188429452794,0.9999999999999999]},"false_flags_all_normals":{"denominator":894,"numerator":126,"rate":0.14093959731543623,"wilson_95":[0.11966383809569674,0.16528787170476106]},"normal_coverage":{"denominator":894,"numerator":894,"rate":1.0,"wilson_95":[0.9957214508386147,1]},"observed_prevalence":{"denominator":1004,"numerator":110,"rate":0.10956175298804781,"wilson_95":[0.0917092070311931,0.13039066479052952]},"precision":{"denominator":216,"numerator":90,"rate":0.4166666666666667,"wilson_95":[0.3529367960490268,0.4833088320817341]},"ranking_scored_only":{"auroc":0.9213138092332723,"average_precision":0.7760211397392787,"n":1004,"population":"scored subset only"},"recall":{"denominator":110,"numerator":90,"rate":0.8181818181818182,"wilson_95":[0.7357859471105165,0.8791042758815609]}} |

**brightness_0p6**

| Aggregate field | Recorded value |
|---|---|
| metrics | {"accepted_normal_fpr":{"denominator":894,"numerator":43,"rate":0.04809843400447427,"wilson_95":[0.03590281159074352,0.06416102255064263]},"anomaly_coverage":{"denominator":110,"numerator":110,"rate":1.0,"wilson_95":[0.9662560647018358,0.9999999999999999]},"counts":{"FN":33,"FP":43,"TN":851,"TP":77,"rejected_anomalies":0,"rejected_normals":0},"coverage":{"denominator":1004,"numerator":1004,"rate":1.0,"wilson_95":[0.996188429452794,0.9999999999999999]},"false_flags_all_normals":{"denominator":894,"numerator":43,"rate":0.04809843400447427,"wilson_95":[0.03590281159074352,0.06416102255064263]},"normal_coverage":{"denominator":894,"numerator":894,"rate":1.0,"wilson_95":[0.9957214508386147,1]},"observed_prevalence":{"denominator":1004,"numerator":110,"rate":0.10956175298804781,"wilson_95":[0.0917092070311931,0.13039066479052952]},"precision":{"denominator":120,"numerator":77,"rate":0.6416666666666667,"wilson_95":[0.5527053600179013,0.7218392094967996]},"ranking_scored_only":{"auroc":0.9307606263982103,"average_precision":0.7631244837214728,"n":1004,"population":"scored subset only"},"recall":{"denominator":110,"numerator":77,"rate":0.7,"wilson_95":[0.6088013903272275,0.7777010355535067]}} |

**brightness_1p4**

| Aggregate field | Recorded value |
|---|---|
| metrics | {"accepted_normal_fpr":{"denominator":894,"numerator":94,"rate":0.10514541387024609,"wilson_95":[0.08669972086081906,0.1269699163963822]},"anomaly_coverage":{"denominator":110,"numerator":110,"rate":1.0,"wilson_95":[0.9662560647018358,0.9999999999999999]},"counts":{"FN":22,"FP":94,"TN":800,"TP":88,"rejected_anomalies":0,"rejected_normals":0},"coverage":{"denominator":1004,"numerator":1004,"rate":1.0,"wilson_95":[0.996188429452794,0.9999999999999999]},"false_flags_all_normals":{"denominator":894,"numerator":94,"rate":0.10514541387024609,"wilson_95":[0.08669972086081906,0.1269699163963822]},"normal_coverage":{"denominator":894,"numerator":894,"rate":1.0,"wilson_95":[0.9957214508386147,1]},"observed_prevalence":{"denominator":1004,"numerator":110,"rate":0.10956175298804781,"wilson_95":[0.0917092070311931,0.13039066479052952]},"precision":{"denominator":182,"numerator":88,"rate":0.4835164835164835,"wilson_95":[0.41200906529053993,0.5557053508678642]},"ranking_scored_only":{"auroc":0.9319402074435632,"average_precision":0.7364600578383049,"n":1004,"population":"scored subset only"},"recall":{"denominator":110,"numerator":88,"rate":0.8,"wilson_95":[0.7157046653839023,0.8640489734371992]}} |

### 12.6 Complete historical PCB calibration/test/stress aggregates

#### PCB1 / reference / calibration

Source: `experiment/results/summary.json`, `reference.calibration`.

| Metric | Recorded value |
|---|---|
| count | 120 |
| defects | 20 |
| normals | 100 |
| TP | 5 |
| FN_unflagged_accepted | 15 |
| FN_abstained | 0 |
| FP | 2 |
| TN | 98 |
| abstained_normals | 0 |
| recall_all_defects | {"numerator":5,"denominator":20,"rate":0.25,"wilson95":[0.11186005278940309,0.4687050099580636]} |
| recall_accepted_defects | {"numerator":5,"denominator":20,"rate":0.25,"wilson95":[0.11186005278940309,0.4687050099580636]} |
| fpr_accepted_normals | {"numerator":2,"denominator":100,"rate":0.02,"wilson95":[0.005501852234968185,0.07001316294199365]} |
| fp_all_normals | {"numerator":2,"denominator":100,"rate":0.02,"wilson95":[0.005501852234968185,0.07001316294199365]} |
| precision_observed | {"numerator":5,"denominator":7,"rate":0.7142857142857143,"wilson95":[0.35892909014821267,0.9177828342909844]} |
| observed_prevalence | {"numerator":20,"denominator":120,"rate":0.16666666666666666,"wilson95":[0.11055912012704824,0.24345439391023813]} |
| coverage | {"numerator":120,"denominator":120,"rate":1.0,"wilson95":[0.9689797289440706,1.0]} |
| retake_requests | 0 |
| latency_ms | {"median":146.28700000002937,"p95":162.55609999998342,"accepted_p95":162.55609999998342,"total_processing_seconds":17.69856250000157} |
| human_review_time | "UNMEASURED; timed exercise pending" |
| capture_time | "UNMEASURED" |
| total_inspection_time | "UNMEASURED" |
| provisional_screen_pass | false |

#### PCB1 / reference / test

Source: `experiment/results/summary.json`, `reference.test`.

| Metric | Recorded value |
|---|---|
| count | 180 |
| defects | 80 |
| normals | 100 |
| TP | 15 |
| FN_unflagged_accepted | 65 |
| FN_abstained | 0 |
| FP | 1 |
| TN | 99 |
| abstained_normals | 0 |
| recall_all_defects | {"numerator":15,"denominator":80,"rate":0.1875,"wilson95":[0.11705207812728378,0.2865852570380757]} |
| recall_accepted_defects | {"numerator":15,"denominator":80,"rate":0.1875,"wilson95":[0.11705207812728378,0.2865852570380757]} |
| fpr_accepted_normals | {"numerator":1,"denominator":100,"rate":0.01,"wilson95":[0.0017673865655472645,0.0544875247609346]} |
| fp_all_normals | {"numerator":1,"denominator":100,"rate":0.01,"wilson95":[0.0017673865655472645,0.0544875247609346]} |
| precision_observed | {"numerator":15,"denominator":16,"rate":0.9375,"wilson95":[0.7167073163197013,0.9888809426916687]} |
| observed_prevalence | {"numerator":80,"denominator":180,"rate":0.4444444444444444,"wilson95":[0.37376583474975517,0.5174448596741402]} |
| coverage | {"numerator":180,"denominator":180,"rate":1.0,"wilson95":[0.9791037501849418,1.0]} |
| retake_requests | 0 |
| latency_ms | {"median":138.1261500000619,"p95":155.6517650001069,"accepted_p95":155.6517650001069,"total_processing_seconds":25.187912300003973} |
| human_review_time | "UNMEASURED; timed exercise pending" |
| capture_time | "UNMEASURED" |
| total_inspection_time | "UNMEASURED" |
| provisional_screen_pass | false |

#### PCB1 / reference / brightness_0.6

Source: `experiment/results/summary.json`, `reference.synthetic_stress.brightness_0.6`.

| Metric | Recorded value |
|---|---|
| count | 180 |
| defects | 80 |
| normals | 100 |
| TP | 1 |
| FN_unflagged_accepted | 79 |
| FN_abstained | 0 |
| FP | 1 |
| TN | 99 |
| abstained_normals | 0 |
| recall_all_defects | {"numerator":1,"denominator":80,"rate":0.0125,"wilson95":[0.002209918618306224,0.06746432423965451]} |
| recall_accepted_defects | {"numerator":1,"denominator":80,"rate":0.0125,"wilson95":[0.002209918618306224,0.06746432423965451]} |
| fpr_accepted_normals | {"numerator":1,"denominator":100,"rate":0.01,"wilson95":[0.0017673865655472645,0.0544875247609346]} |
| fp_all_normals | {"numerator":1,"denominator":100,"rate":0.01,"wilson95":[0.0017673865655472645,0.0544875247609346]} |
| precision_observed | {"numerator":1,"denominator":2,"rate":0.5,"wilson95":[0.09452865480086614,0.9054713451991339]} |
| observed_prevalence | {"numerator":80,"denominator":180,"rate":0.4444444444444444,"wilson95":[0.37376583474975517,0.5174448596741402]} |
| coverage | {"numerator":180,"denominator":180,"rate":1.0,"wilson95":[0.9791037501849418,1.0]} |
| retake_requests | 0 |
| latency_ms | {"median":149.59109999972497,"p95":164.06309999963466,"accepted_p95":164.06309999963466,"total_processing_seconds":27.183148899997832} |
| human_review_time | "UNMEASURED; timed exercise pending" |
| capture_time | "UNMEASURED" |
| total_inspection_time | "UNMEASURED" |
| provisional_screen_pass | false |

#### PCB1 / reference / brightness_1.4

Source: `experiment/results/summary.json`, `reference.synthetic_stress.brightness_1.4`.

| Metric | Recorded value |
|---|---|
| count | 180 |
| defects | 80 |
| normals | 100 |
| TP | 8 |
| FN_unflagged_accepted | 72 |
| FN_abstained | 0 |
| FP | 1 |
| TN | 99 |
| abstained_normals | 0 |
| recall_all_defects | {"numerator":8,"denominator":80,"rate":0.1,"wilson95":[0.05154699917768554,0.18510878983397458]} |
| recall_accepted_defects | {"numerator":8,"denominator":80,"rate":0.1,"wilson95":[0.05154699917768554,0.18510878983397458]} |
| fpr_accepted_normals | {"numerator":1,"denominator":100,"rate":0.01,"wilson95":[0.0017673865655472645,0.0544875247609346]} |
| fp_all_normals | {"numerator":1,"denominator":100,"rate":0.01,"wilson95":[0.0017673865655472645,0.0544875247609346]} |
| precision_observed | {"numerator":8,"denominator":9,"rate":0.8888888888888888,"wilson95":[0.5649937852319399,0.9801096286728695]} |
| observed_prevalence | {"numerator":80,"denominator":180,"rate":0.4444444444444444,"wilson95":[0.37376583474975517,0.5174448596741402]} |
| coverage | {"numerator":180,"denominator":180,"rate":1.0,"wilson95":[0.9791037501849418,1.0]} |
| retake_requests | 0 |
| latency_ms | {"median":157.89940000013303,"p95":180.49289999992197,"accepted_p95":180.49289999992197,"total_processing_seconds":28.8028907000039} |
| human_review_time | "UNMEASURED; timed exercise pending" |
| capture_time | "UNMEASURED" |
| total_inspection_time | "UNMEASURED" |
| provisional_screen_pass | false |

#### PCB1 / reference / blur_2.0

Source: `experiment/results/summary.json`, `reference.synthetic_stress.blur_2.0`.

| Metric | Recorded value |
|---|---|
| count | 180 |
| defects | 80 |
| normals | 100 |
| TP | 11 |
| FN_unflagged_accepted | 69 |
| FN_abstained | 0 |
| FP | 1 |
| TN | 99 |
| abstained_normals | 0 |
| recall_all_defects | {"numerator":11,"denominator":80,"rate":0.1375,"wilson95":[0.07854633679551142,0.22967297199630554]} |
| recall_accepted_defects | {"numerator":11,"denominator":80,"rate":0.1375,"wilson95":[0.07854633679551142,0.22967297199630554]} |
| fpr_accepted_normals | {"numerator":1,"denominator":100,"rate":0.01,"wilson95":[0.0017673865655472645,0.0544875247609346]} |
| fp_all_normals | {"numerator":1,"denominator":100,"rate":0.01,"wilson95":[0.0017673865655472645,0.0544875247609346]} |
| precision_observed | {"numerator":11,"denominator":12,"rate":0.9166666666666666,"wilson95":[0.6461140782014047,0.9851352905492264]} |
| observed_prevalence | {"numerator":80,"denominator":180,"rate":0.4444444444444444,"wilson95":[0.37376583474975517,0.5174448596741402]} |
| coverage | {"numerator":180,"denominator":180,"rate":1.0,"wilson95":[0.9791037501849418,1.0]} |
| retake_requests | 0 |
| latency_ms | {"median":199.91345000016736,"p95":236.96956500011765,"accepted_p95":236.96956500011765,"total_processing_seconds":36.55048899999838} |
| human_review_time | "UNMEASURED; timed exercise pending" |
| capture_time | "UNMEASURED" |
| total_inspection_time | "UNMEASURED" |
| provisional_screen_pass | false |

#### PCB1 / padim / calibration

Source: `experiment/results/summary.json`, `padim.calibration`.

| Metric | Recorded value |
|---|---|
| count | 120 |
| defects | 20 |
| normals | 100 |
| TP | 14 |
| FN_unflagged_accepted | 6 |
| FN_abstained | 0 |
| FP | 6 |
| TN | 94 |
| abstained_normals | 0 |
| recall_all_defects | {"numerator":14,"denominator":20,"rate":0.7,"wilson95":[0.4810232237710206,0.854524726031006]} |
| recall_accepted_defects | {"numerator":14,"denominator":20,"rate":0.7,"wilson95":[0.4810232237710206,0.854524726031006]} |
| fpr_accepted_normals | {"numerator":6,"denominator":100,"rate":0.06,"wilson95":[0.02778574526665662,0.12476968531222507]} |
| fp_all_normals | {"numerator":6,"denominator":100,"rate":0.06,"wilson95":[0.02778574526665662,0.12476968531222507]} |
| precision_observed | {"numerator":14,"denominator":20,"rate":0.7,"wilson95":[0.4810232237710206,0.854524726031006]} |
| observed_prevalence | {"numerator":20,"denominator":120,"rate":0.16666666666666666,"wilson95":[0.11055912012704824,0.24345439391023813]} |
| coverage | {"numerator":120,"denominator":120,"rate":1.0,"wilson95":[0.9689797289440706,1.0]} |
| retake_requests | 0 |
| latency_ms | {"median":77.29844999994384,"p95":85.87636499978544,"accepted_p95":85.87636499978544,"total_processing_seconds":9.2941257999978} |
| human_review_time | "UNMEASURED; timed exercise pending" |
| capture_time | "UNMEASURED" |
| total_inspection_time | "UNMEASURED" |
| provisional_screen_pass | false |

#### PCB1 / padim / test

Source: `experiment/results/summary.json`, `padim.test`.

| Metric | Recorded value |
|---|---|
| count | 180 |
| defects | 80 |
| normals | 100 |
| TP | 45 |
| FN_unflagged_accepted | 35 |
| FN_abstained | 0 |
| FP | 15 |
| TN | 85 |
| abstained_normals | 0 |
| recall_all_defects | {"numerator":45,"denominator":80,"rate":0.5625,"wilson95":[0.4534093786865696,0.6658631542803586]} |
| recall_accepted_defects | {"numerator":45,"denominator":80,"rate":0.5625,"wilson95":[0.4534093786865696,0.6658631542803586]} |
| fpr_accepted_normals | {"numerator":15,"denominator":100,"rate":0.15,"wilson95":[0.09305903191162297,0.23283733332157835]} |
| fp_all_normals | {"numerator":15,"denominator":100,"rate":0.15,"wilson95":[0.09305903191162297,0.23283733332157835]} |
| precision_observed | {"numerator":45,"denominator":60,"rate":0.75,"wilson95":[0.6276768905451521,0.8422361442158816]} |
| observed_prevalence | {"numerator":80,"denominator":180,"rate":0.4444444444444444,"wilson95":[0.37376583474975517,0.5174448596741402]} |
| coverage | {"numerator":180,"denominator":180,"rate":1.0,"wilson95":[0.9791037501849418,1.0]} |
| retake_requests | 0 |
| latency_ms | {"median":84.72990000018399,"p95":97.33005000020967,"accepted_p95":97.33005000020967,"total_processing_seconds":15.474530299989965} |
| human_review_time | "UNMEASURED; timed exercise pending" |
| capture_time | "UNMEASURED" |
| total_inspection_time | "UNMEASURED" |
| provisional_screen_pass | false |

#### PCB1 / padim / brightness_0.6

Source: `experiment/results/summary.json`, `padim.synthetic_stress.brightness_0.6`.

| Metric | Recorded value |
|---|---|
| count | 180 |
| defects | 80 |
| normals | 100 |
| TP | 44 |
| FN_unflagged_accepted | 36 |
| FN_abstained | 0 |
| FP | 9 |
| TN | 91 |
| abstained_normals | 0 |
| recall_all_defects | {"numerator":44,"denominator":80,"rate":0.55,"wilson95":[0.4411931301173402,0.6542248962562025]} |
| recall_accepted_defects | {"numerator":44,"denominator":80,"rate":0.55,"wilson95":[0.4411931301173402,0.6542248962562025]} |
| fpr_accepted_normals | {"numerator":9,"denominator":100,"rate":0.09,"wilson95":[0.04807199516388488,0.16226374696643667]} |
| fp_all_normals | {"numerator":9,"denominator":100,"rate":0.09,"wilson95":[0.04807199516388488,0.16226374696643667]} |
| precision_observed | {"numerator":44,"denominator":53,"rate":0.8301886792452831,"wilson95":[0.7077446317626587,0.9080015822777624]} |
| observed_prevalence | {"numerator":80,"denominator":180,"rate":0.4444444444444444,"wilson95":[0.37376583474975517,0.5174448596741402]} |
| coverage | {"numerator":180,"denominator":180,"rate":1.0,"wilson95":[0.9791037501849418,1.0]} |
| retake_requests | 0 |
| latency_ms | {"median":88.06420000018989,"p95":102.94601499999769,"accepted_p95":102.94601499999769,"total_processing_seconds":16.119450099996357} |
| human_review_time | "UNMEASURED; timed exercise pending" |
| capture_time | "UNMEASURED" |
| total_inspection_time | "UNMEASURED" |
| provisional_screen_pass | false |

#### PCB1 / padim / brightness_1.4

Source: `experiment/results/summary.json`, `padim.synthetic_stress.brightness_1.4`.

| Metric | Recorded value |
|---|---|
| count | 180 |
| defects | 80 |
| normals | 100 |
| TP | 58 |
| FN_unflagged_accepted | 22 |
| FN_abstained | 0 |
| FP | 27 |
| TN | 73 |
| abstained_normals | 0 |
| recall_all_defects | {"numerator":58,"denominator":80,"rate":0.725,"wilson95":[0.618557347158301,0.8108237715226401]} |
| recall_accepted_defects | {"numerator":58,"denominator":80,"rate":0.725,"wilson95":[0.618557347158301,0.8108237715226401]} |
| fpr_accepted_normals | {"numerator":27,"denominator":100,"rate":0.27,"wilson95":[0.1926946091766482,0.3643230022623127]} |
| fp_all_normals | {"numerator":27,"denominator":100,"rate":0.27,"wilson95":[0.1926946091766482,0.3643230022623127]} |
| precision_observed | {"numerator":58,"denominator":85,"rate":0.6823529411764706,"wilson95":[0.5773362018838148,0.7715994318733441]} |
| observed_prevalence | {"numerator":80,"denominator":180,"rate":0.4444444444444444,"wilson95":[0.37376583474975517,0.5174448596741402]} |
| coverage | {"numerator":180,"denominator":180,"rate":1.0,"wilson95":[0.9791037501849418,1.0]} |
| retake_requests | 0 |
| latency_ms | {"median":92.60140000060346,"p95":102.41862500038224,"accepted_p95":102.41862500038224,"total_processing_seconds":16.71044279999751} |
| human_review_time | "UNMEASURED; timed exercise pending" |
| capture_time | "UNMEASURED" |
| total_inspection_time | "UNMEASURED" |
| provisional_screen_pass | false |

#### PCB1 / padim / blur_2.0

Source: `experiment/results/summary.json`, `padim.synthetic_stress.blur_2.0`.

| Metric | Recorded value |
|---|---|
| count | 180 |
| defects | 80 |
| normals | 100 |
| TP | 44 |
| FN_unflagged_accepted | 36 |
| FN_abstained | 0 |
| FP | 14 |
| TN | 86 |
| abstained_normals | 0 |
| recall_all_defects | {"numerator":44,"denominator":80,"rate":0.55,"wilson95":[0.4411931301173402,0.6542248962562025]} |
| recall_accepted_defects | {"numerator":44,"denominator":80,"rate":0.55,"wilson95":[0.4411931301173402,0.6542248962562025]} |
| fpr_accepted_normals | {"numerator":14,"denominator":100,"rate":0.14,"wilson95":[0.08526265754464905,0.22137360383807236]} |
| fp_all_normals | {"numerator":14,"denominator":100,"rate":0.14,"wilson95":[0.08526265754464905,0.22137360383807236]} |
| precision_observed | {"numerator":44,"denominator":58,"rate":0.7586206896551724,"wilson95":[0.6346977437031315,0.8504126027303373]} |
| observed_prevalence | {"numerator":80,"denominator":180,"rate":0.4444444444444444,"wilson95":[0.37376583474975517,0.5174448596741402]} |
| coverage | {"numerator":180,"denominator":180,"rate":1.0,"wilson95":[0.9791037501849418,1.0]} |
| retake_requests | 0 |
| latency_ms | {"median":138.07900000028894,"p95":167.13609500056916,"accepted_p95":167.13609500056916,"total_processing_seconds":25.23859799999991} |
| human_review_time | "UNMEASURED; timed exercise pending" |
| capture_time | "UNMEASURED" |
| total_inspection_time | "UNMEASURED" |
| provisional_screen_pass | false |

### 12.7 Defect-folder recall and bootstrap intervals

| Recipe | Method | Folder | Detected | Total | Recall | Wilson95% |
|---|---|---|---|---|---|---|
| mvtec_3d_cable_gland_rgb | padim | bent | 3 | 21 | 14.286% | [0.04981012499725268,0.34636060280620945] |
| mvtec_3d_cable_gland_rgb | padim | cut | 3 | 22 | 13.636% | [0.04749003714055253,0.33334987166571717] |
| mvtec_3d_cable_gland_rgb | padim | hole | 5 | 22 | 22.727% | [0.10123039985248516,0.4343995317522171] |
| mvtec_3d_cable_gland_rgb | padim | thread | 0 | 22 | 0.000% | [0,0.14865487460862087] |
| mvtec_3d_cable_gland_rgb | reference | bent | 1 | 21 | 4.762% | [0.008455987809826399,0.22669360074122563] |
| mvtec_3d_cable_gland_rgb | reference | cut | 0 | 22 | 0.000% | [0,0.14865487460862087] |
| mvtec_3d_cable_gland_rgb | reference | hole | 1 | 22 | 4.545% | [0.00806942762126385,0.21798045838657332] |
| mvtec_3d_cable_gland_rgb | reference | thread | 1 | 22 | 4.545% | [0.00806942762126385,0.21798045838657332] |

**ksdd2_surface/padim** bootstrap: `{"auroc_95":[0.9064877964649785,0.9548203163411199],"average_precision_95":[0.6629189749401456,0.8142941423072632],"caution":"Appearance groups are not verified physical-product identities; intervals do not establish physical independence.","group_count":1004,"physical_independence_verified":false,"population":"scored subset only","requested_replicates":1000,"seed":4217,"valid_replicates":1000}`.

**ksdd2_surface/reference** bootstrap: `{"auroc_95":[0.8608536410436671,0.9251289924921844],"average_precision_95":[0.6221490580764815,0.76860973730541],"caution":"Appearance groups are not verified physical-product identities; intervals do not establish physical independence.","group_count":1004,"physical_independence_verified":false,"population":"scored subset only","requested_replicates":1000,"seed":4217,"valid_replicates":1000}`.

**mvtec_3d_cable_gland_rgb/padim** bootstrap: `{"auroc_95":[0.6138282937321626,0.8373163082437276],"average_precision_95":[0.8509739450333773,0.9667554344564716],"caution":"Appearance groups are not verified physical-product identities; intervals do not establish physical independence.","group_count":108,"physical_independence_verified":false,"population":"scored subset only","requested_replicates":1000,"seed":4217,"valid_replicates":1000}`.

**mvtec_3d_cable_gland_rgb/reference** bootstrap: `{"auroc_95":[0.3935166240409207,0.6540086806488897],"average_precision_95":[0.7239573075896728,0.912876391711812],"caution":"Appearance groups are not verified physical-product identities; intervals do not establish physical independence.","group_count":108,"physical_independence_verified":false,"population":"scored subset only","requested_replicates":1000,"seed":4217,"valid_replicates":1000}`.

Source: `components/runs/frozen-20261019T041652Z-9c825801/SUPPLEMENT.json`; no verified KSDD2 subtype labels. Intervals are appearance-group descriptive uncertainty, not physical-independence proof.

### 12.8 Selected checkpoint inventory

| Recipe | Method | State | Bytes | State SHA256 | Metadata | Metadata SHA256 |
|---|---|---|---|---|---|---|
| ksdd2_surface | padim | components/models/ksdd2_surface/padim-p0-38fc0d1f768474c62ecf4aa3-0ac3bf5e/state.pt | 424884545 | b19d4c422578868759460b8d9f1ac252669443517b83fb7ecab8a9395e23365c | components/models/ksdd2_surface/padim-p0-38fc0d1f768474c62ecf4aa3-0ac3bf5e/metadata.json | 36a3a354799c1303e9969c42e94c6d0036fa6a099837efddeb5ddede4baec2d7 |
| ksdd2_surface | reference | components/models/ksdd2_surface/reference-4a1602d3105cf3655039231a5d4a6a4aabd5fdf12bd178b9e93791294e136338/bank.npy | 31457408 | c754e08b781b1cf76daf274159e94101e9908d20fc9a99979de4db2faf1efafb | components/models/ksdd2_surface/reference-4a1602d3105cf3655039231a5d4a6a4aabd5fdf12bd178b9e93791294e136338/metadata.json | 16ccca55e38a3c52ade245387f63254f2a30e6f0e3831e0648101af87dcd7603 |
| mvtec_3d_cable_gland_rgb | padim | components/models/mvtec_3d_cable_gland_rgb/padim-p0-38fc0d1f768474c62ecf4aa3-0ac3bf5e/state.pt | 176666945 | 6b1d1acf856cd4052fbc8a2d5055564ea4d16dd954243b12b36347dbbe5d987d | components/models/mvtec_3d_cable_gland_rgb/padim-p0-38fc0d1f768474c62ecf4aa3-0ac3bf5e/metadata.json | f69870c8ae3de27b1f4a30ab558a5c3d8d435ae01f808c575e9c10ea05fd91da |
| mvtec_3d_cable_gland_rgb | reference | components/models/mvtec_3d_cable_gland_rgb/reference-4a1602d3105cf3655039231a5d4a6a4aabd5fdf12bd178b9e93791294e136338/bank.npy | 12583040 | da37d9e7f2d04c680e4c1d69d8fc52f22d032e98194a568963f2f8dbb5d9c54b | components/models/mvtec_3d_cable_gland_rgb/reference-4a1602d3105cf3655039231a5d4a6a4aabd5fdf12bd178b9e93791294e136338/metadata.json | bcff08e4bafd16d03165d022edeadcef5171bc7d2ca0290ef53435664edba72b |

### 12.9 All locally present model artifacts and lineage

| File | Bytes |
|---|---|
| components/models/backbones/resnet18_a1/model.safetensors | 46807446 |
| components/models/ksdd2_surface/padim-p0-38fc0d1f768474c62ecf4aa3-0ac3bf5e/metadata.json | 18161 |
| components/models/ksdd2_surface/padim-p0-38fc0d1f768474c62ecf4aa3-0ac3bf5e/state.pt | 424884545 |
| components/models/ksdd2_surface/padim-p0-e12ea8b5a6396872a8e26e6f-8f32aeb2/metadata.json | 18161 |
| components/models/ksdd2_surface/padim-p0-e12ea8b5a6396872a8e26e6f-8f32aeb2/state.pt | 424884545 |
| components/models/ksdd2_surface/reference-0fa409f4dea68ac3fb1e83cafbca03ac212ac5f4c412ac787f4ba26601baa1da/bank.npy | 31457408 |
| components/models/ksdd2_surface/reference-0fa409f4dea68ac3fb1e83cafbca03ac212ac5f4c412ac787f4ba26601baa1da/metadata.json | 2359 |
| components/models/ksdd2_surface/reference-4a1602d3105cf3655039231a5d4a6a4aabd5fdf12bd178b9e93791294e136338/bank.npy | 31457408 |
| components/models/ksdd2_surface/reference-4a1602d3105cf3655039231a5d4a6a4aabd5fdf12bd178b9e93791294e136338/metadata.json | 2359 |
| components/models/mvtec_3d_cable_gland_rgb/padim-p0-38fc0d1f768474c62ecf4aa3-0ac3bf5e/metadata.json | 19748 |
| components/models/mvtec_3d_cable_gland_rgb/padim-p0-38fc0d1f768474c62ecf4aa3-0ac3bf5e/state.pt | 176666945 |
| components/models/mvtec_3d_cable_gland_rgb/padim-p0-e12ea8b5a6396872a8e26e6f-8f32aeb2/metadata.json | 19748 |
| components/models/mvtec_3d_cable_gland_rgb/padim-p0-e12ea8b5a6396872a8e26e6f-8f32aeb2/state.pt | 176666945 |
| components/models/mvtec_3d_cable_gland_rgb/reference-0fa409f4dea68ac3fb1e83cafbca03ac212ac5f4c412ac787f4ba26601baa1da/bank.npy | 12583040 |
| components/models/mvtec_3d_cable_gland_rgb/reference-0fa409f4dea68ac3fb1e83cafbca03ac212ac5f4c412ac787f4ba26601baa1da/metadata.json | 2490 |
| components/models/mvtec_3d_cable_gland_rgb/reference-4a1602d3105cf3655039231a5d4a6a4aabd5fdf12bd178b9e93791294e136338/bank.npy | 12583040 |
| components/models/mvtec_3d_cable_gland_rgb/reference-4a1602d3105cf3655039231a5d4a6a4aabd5fdf12bd178b9e93791294e136338/metadata.json | 2490 |
| experiment/models/padim.onnx | 43125528 |
| experiment/models/padim.pt | 43162798 |
| experiment/models/reference_bank.npy | 60211328 |
| experiment/models/resnet18-f37072fd.pth | 46830571 |

Selected B0 development results: `components/outputs/stage3/4a1602d3105cf3655039231a5d4a6a4aabd5fdf12bd178b9e93791294e136338/results.json`; superseded ordering run: `components/outputs/stage3/0fa409f4dea68ac3fb1e83cafbca03ac212ac5f4c412ac787f4ba26601baa1da/results.json`. Selected P0 report: `components/outputs/stage4/38fc0d1f768474c62ecf4aa3-0ac3bf5e/report.json`; superseded memory report: `components/outputs/stage4/e12ea8b5a6396872a8e26e6f-8f32aeb2/report.json`. Request, worker logs and per-recipe results reside below those output roots.

### 12.10 Recorded selected and superseded development aggregates

**components/outputs/stage3/0fa409f4dea68ac3fb1e83cafbca03ac212ac5f4c412ac787f4ba26601baa1da/results.json**

| Field | Recorded value |
|---|---|
| code_hashes | {"develop.py":"93f4317570a0f58f1dfad61f9aebe1028d7f1e58ea42c0131b5705a5bb779a89","geometry.py":"dce8e09a3d9fe343c02ab412fb53c13d1fb1c91129b7821d1672b008272d31d8","reference.py":"c6e08509bbf8d7c62efea0866e79b8425eb68202bf826e926fb1c4ffcf20cb83"} |
| environment | {"Pillow":"12.1.0","numpy":"2.2.4","scipy":"1.15.2"} |
| manifest_sha256 | "f1fdd9113745565f00827529f475989192465562e881478a3f6d3d31f59b4863" |
| membership_hash | "6d24d51d1858c67b08d14340998310c8a4e419ab7f232270d4f322a7bcd53ca2" |
| peak_sampled_rss_bytes | 206503936 |
| run_id | "0fa409f4dea68ac3fb1e83cafbca03ac212ac5f4c412ac787f4ba26601baa1da" |
| status | "development_only_uncalibrated" |

Recipe **ksdd2_surface**

| Field | Recorded value |
|---|---|
| artifact_path | "models/ksdd2_surface/reference-0fa409f4dea68ac3fb1e83cafbca03ac212ac5f4c412ac787f4ba26601baa1da" |
| cold_pipeline_seconds | 0.16353710000112187 |
| development_images | 663 |
| fit_seconds | 0.2500360999983968 |
| flagged | null |
| model_bytes | 31459767 |
| references | ["ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/10269.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/10857.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/10606.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/10551.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/11907.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/12129.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/10299.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/11332.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/10036.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/12151.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/12079.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/11689.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/11211.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/10684.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/10280.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/10217.png"] |
| save_load_parity | "exact" |
| selected_fit_groups | 16 |
| threshold | null |
| warm_p95_pipeline_seconds | 0.16624606999685054 |

Recipe **mvtec_3d_cable_gland_rgb**

| Field | Recorded value |
|---|---|
| artifact_path | "models/mvtec_3d_cable_gland_rgb/reference-0fa409f4dea68ac3fb1e83cafbca03ac212ac5f4c412ac787f4ba26601baa1da" |
| cold_pipeline_seconds | 0.06576559999666642 |
| development_images | 68 |
| fit_seconds | 0.16511159999936353 |
| flagged | null |
| model_bytes | 12585530 |
| references | ["mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/048.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/001.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/199.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/156.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/072.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/059.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/015.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/006.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/106.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/150.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/046.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/062.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/086.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/012.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/030.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/110.png"] |
| save_load_parity | "exact" |
| selected_fit_groups | 16 |
| threshold | null |
| warm_p95_pipeline_seconds | 0.06800652000238187 |

**components/outputs/stage3/4a1602d3105cf3655039231a5d4a6a4aabd5fdf12bd178b9e93791294e136338/results.json**

| Field | Recorded value |
|---|---|
| code_hashes | {"develop.py":"2c8518f124300258d3e1f0a34ebd9f716cc16a994fd905de1945b6f0da50e46f","geometry.py":"dce8e09a3d9fe343c02ab412fb53c13d1fb1c91129b7821d1672b008272d31d8","reference.py":"c6e08509bbf8d7c62efea0866e79b8425eb68202bf826e926fb1c4ffcf20cb83"} |
| environment | {"Pillow":"12.1.0","numpy":"2.2.4","scipy":"1.15.2"} |
| manifest_sha256 | "f1fdd9113745565f00827529f475989192465562e881478a3f6d3d31f59b4863" |
| membership_hash | "6d24d51d1858c67b08d14340998310c8a4e419ab7f232270d4f322a7bcd53ca2" |
| peak_sampled_rss_bytes | 208347136 |
| run_id | "4a1602d3105cf3655039231a5d4a6a4aabd5fdf12bd178b9e93791294e136338" |
| status | "development_only_uncalibrated" |

Recipe **ksdd2_surface**

| Field | Recorded value |
|---|---|
| artifact_path | "models/ksdd2_surface/reference-4a1602d3105cf3655039231a5d4a6a4aabd5fdf12bd178b9e93791294e136338" |
| cold_pipeline_seconds | 0.11821970000164583 |
| development_images | 663 |
| fit_seconds | 0.18088440000428818 |
| flagged | null |
| model_bytes | 31459767 |
| references | ["ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/10269.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/10857.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/10606.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/10551.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/11907.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/12129.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/10299.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/11332.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/10036.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/12151.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/12079.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/11689.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/11211.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/10684.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/10280.png","ksdd2:edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8:train/10217.png"] |
| save_load_parity | "exact" |
| selected_fit_groups | 16 |
| threshold | null |
| warm_p95_pipeline_seconds | 0.16176392499037312 |

Recipe **mvtec_3d_cable_gland_rgb**

| Field | Recorded value |
|---|---|
| artifact_path | "models/mvtec_3d_cable_gland_rgb/reference-4a1602d3105cf3655039231a5d4a6a4aabd5fdf12bd178b9e93791294e136338" |
| cold_pipeline_seconds | 0.05219070000748616 |
| development_images | 68 |
| fit_seconds | 0.18477809999603778 |
| flagged | null |
| model_bytes | 12585530 |
| references | ["mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/048.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/001.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/199.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/156.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/072.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/059.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/015.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/006.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/106.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/150.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/046.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/062.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/086.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/012.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/030.png","mvtec_3d_ad:63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed:train/good/rgb/110.png"] |
| save_load_parity | "exact" |
| selected_fit_groups | 16 |
| threshold | null |
| warm_p95_pipeline_seconds | 0.05671958999300841 |

**components/outputs/stage4/38fc0d1f768474c62ecf4aa3-0ac3bf5e/report.json**

| Field | Recorded value |
|---|---|
| backend | "anomalib_p0" |
| manifest_sha256 | "f1fdd9113745565f00827529f475989192465562e881478a3f6d3d31f59b4863" |
| membership_hash | "6d24d51d1858c67b08d14340998310c8a4e419ab7f232270d4f322a7bcd53ca2" |
| run_id | "38fc0d1f768474c62ecf4aa3-0ac3bf5e" |
| status | "development_only_uncalibrated" |
| versions | {"Pillow":"12.1.0","anomalib":"2.7.0","numpy":"2.2.4","scipy":"1.15.2","timm":"1.0.30","torch":"2.10.0+cpu","torchvision":"0.25.0+cpu"} |
| weights_sha256 | "80c49dee3da4822c009c5a7fe591e9223c5a2cfcf95a4067ca4dfb5a7b89c612" |

Recipe **ksdd2_surface**

| Field | Recorded value |
|---|---|
| artifact_path | "C:\\Users\\laksh\\OneDrive\\Desktop\\Tech4Bharat\\components\\models\\ksdd2_surface\\padim-p0-38fc0d1f768474c62ecf4aa3-0ac3bf5e" |
| available_ram_at_launch_bytes | 5741998080 |
| backend | "anomalib_p0" |
| cold_pipeline_seconds | 0.3210375000053318 |
| development_images | 663 |
| fit_seconds | 27.922461900001508 |
| flagged | null |
| gaussian_shapes | {"inverse_covariance":[10240,100,100],"mean":[100,10240]} |
| init_seconds | 8.047324400002253 |
| input_shape | [256,640] |
| model_bytes | 424902706 |
| normal_fit_images | 128 |
| recipe_id | "ksdd2_surface" |
| resource_measurement | {"elapsed_seconds":283.5149999999994,"max_observed_processes":3,"measurement_scope":"owned process tree RSS sum","peak_sampled_rss_bytes":3173732352,"returncode":0,"rss_cap_bytes":3445198848,"sample_interval_seconds":0.05,"status":"completed","time_cap_seconds":1800} |
| results_path | "outputs/stage4/38fc0d1f768474c62ecf4aa3-0ac3bf5e/ksdd2_surface/results.json" |
| results_sha256 | "5871a73567153c03761bc47dad8f77e97d0712d9d681c0cf6a8c0566bca6424b" |
| save_load_parity | "atol=rtol=1e-5" |
| status | "native_development_feasible" |
| threshold | null |
| warm_p95_pipeline_seconds | 0.3698617749985714 |
| worker_log | "outputs/stage4/38fc0d1f768474c62ecf4aa3-0ac3bf5e/ksdd2_surface_worker.log" |

Recipe **mvtec_3d_cable_gland_rgb**

| Field | Recorded value |
|---|---|
| artifact_path | "C:\\Users\\laksh\\OneDrive\\Desktop\\Tech4Bharat\\components\\models\\mvtec_3d_cable_gland_rgb\\padim-p0-38fc0d1f768474c62ecf4aa3-0ac3bf5e" |
| available_ram_at_launch_bytes | 5573922816 |
| backend | "anomalib_p0" |
| cold_pipeline_seconds | 0.1445908000023337 |
| development_images | 68 |
| fit_seconds | 12.468698500000755 |
| flagged | null |
| gaussian_shapes | {"inverse_covariance":[4096,100,100],"mean":[100,4096]} |
| init_seconds | 8.25827279999794 |
| input_shape | [256,256] |
| model_bytes | 176686693 |
| normal_fit_images | 128 |
| recipe_id | "mvtec_3d_cable_gland_rgb" |
| resource_measurement | {"elapsed_seconds":54.969000000011874,"max_observed_processes":3,"measurement_scope":"owned process tree RSS sum","peak_sampled_rss_bytes":1627570176,"returncode":0,"rss_cap_bytes":3344353689,"sample_interval_seconds":0.05,"status":"completed","time_cap_seconds":1800} |
| results_path | "outputs/stage4/38fc0d1f768474c62ecf4aa3-0ac3bf5e/mvtec_3d_cable_gland_rgb/results.json" |
| results_sha256 | "eb2d66b018f45ee47407004492dbdd9d2b51aeb3eee887dd29b939b922e6359c" |
| save_load_parity | "atol=rtol=1e-5" |
| status | "native_development_feasible" |
| threshold | null |
| warm_p95_pipeline_seconds | 0.15850963999837403 |
| worker_log | "outputs/stage4/38fc0d1f768474c62ecf4aa3-0ac3bf5e/mvtec_3d_cable_gland_rgb_worker.log" |

**components/outputs/stage4/e12ea8b5a6396872a8e26e6f-8f32aeb2/report.json**

| Field | Recorded value |
|---|---|
| backend | "anomalib_p0" |
| manifest_sha256 | "f1fdd9113745565f00827529f475989192465562e881478a3f6d3d31f59b4863" |
| membership_hash | "6d24d51d1858c67b08d14340998310c8a4e419ab7f232270d4f322a7bcd53ca2" |
| run_id | "e12ea8b5a6396872a8e26e6f-8f32aeb2" |
| status | "development_only_uncalibrated" |
| versions | {"Pillow":"12.1.0","anomalib":"2.7.0","numpy":"2.2.4","scipy":"1.15.2","timm":"1.0.30","torch":"2.10.0+cpu","torchvision":"0.25.0+cpu"} |
| weights_sha256 | "80c49dee3da4822c009c5a7fe591e9223c5a2cfcf95a4067ca4dfb5a7b89c612" |

Recipe **ksdd2_surface**

| Field | Recorded value |
|---|---|
| artifact_path | "C:\\Users\\laksh\\OneDrive\\Desktop\\Tech4Bharat\\components\\models\\ksdd2_surface\\padim-p0-e12ea8b5a6396872a8e26e6f-8f32aeb2" |
| available_ram_at_launch_bytes | 5957328896 |
| backend | "anomalib_p0" |
| cold_pipeline_seconds | 0.3807381999940844 |
| development_images | 663 |
| fit_seconds | 27.7748019000137 |
| flagged | null |
| gaussian_shapes | {"inverse_covariance":[10240,100,100],"mean":[100,10240]} |
| init_seconds | 8.048992000010912 |
| input_shape | [256,640] |
| model_bytes | 424902706 |
| normal_fit_images | 128 |
| recipe_id | "ksdd2_surface" |
| resource_measurement | {"elapsed_seconds":284.2809999999881,"peak_sampled_rss_bytes":4378624,"returncode":0,"rss_cap_bytes":3574397337,"sample_interval_seconds":0.05,"status":"completed","time_cap_seconds":1800} |
| results_path | "outputs/stage4/e12ea8b5a6396872a8e26e6f-8f32aeb2/ksdd2_surface/results.json" |
| results_sha256 | "92e9134fbc49d9edc81421cdd1f76e53140ab34bb1b8b2edd5cd46d0bc3a92ef" |
| save_load_parity | "atol=rtol=1e-5" |
| status | "native_development_feasible" |
| threshold | null |
| warm_p95_pipeline_seconds | 0.3769424599930062 |
| worker_log | "outputs/stage4/e12ea8b5a6396872a8e26e6f-8f32aeb2/ksdd2_surface_worker.log" |

Recipe **mvtec_3d_cable_gland_rgb**

| Field | Recorded value |
|---|---|
| artifact_path | "C:\\Users\\laksh\\OneDrive\\Desktop\\Tech4Bharat\\components\\models\\mvtec_3d_cable_gland_rgb\\padim-p0-e12ea8b5a6396872a8e26e6f-8f32aeb2" |
| available_ram_at_launch_bytes | 5357776896 |
| backend | "anomalib_p0" |
| cold_pipeline_seconds | 0.14678860000276472 |
| development_images | 68 |
| fit_seconds | 13.451342299988028 |
| flagged | null |
| gaussian_shapes | {"inverse_covariance":[4096,100,100],"mean":[100,4096]} |
| init_seconds | 8.950188599992543 |
| input_shape | [256,256] |
| model_bytes | 176686693 |
| normal_fit_images | 128 |
| recipe_id | "mvtec_3d_cable_gland_rgb" |
| resource_measurement | {"elapsed_seconds":59.09399999999732,"peak_sampled_rss_bytes":4370432,"returncode":0,"rss_cap_bytes":3214666137,"sample_interval_seconds":0.05,"status":"completed","time_cap_seconds":1800} |
| results_path | "outputs/stage4/e12ea8b5a6396872a8e26e6f-8f32aeb2/mvtec_3d_cable_gland_rgb/results.json" |
| results_sha256 | "0396e57cc5a0f436b79360601bbd0d1f0be8cb08eb07825299d60ebf5f0593bf" |
| save_load_parity | "atol=rtol=1e-5" |
| status | "native_development_feasible" |
| threshold | null |
| warm_p95_pipeline_seconds | 0.16545415000000502 |
| worker_log | "outputs/stage4/e12ea8b5a6396872a8e26e6f-8f32aeb2/mvtec_3d_cable_gland_rgb_worker.log" |

Historical PCB maps: `experiment/results/maps/{reference|padim}_test_*.npy` (360 locally present files). Historical model-state and provider files were enumerated; Stage5 frozen selected states were rehashed. The audit did not newly validate all historical PCB checkpoint/source checksums or model execution.

### 12.11 Phase evidence graph

| Run-relative path | Purpose |
|---|---|
| freeze.json | Source/model/runtime/version/role identities |
| calibration_started.json; evaluate_started.json; stress_started.json | UTC phase reservations |
| calibration_complete.json; evaluation_complete.json; stress_complete.json | Per-phase output/resource hashes; original screens/decision |
| unit_reservations/ | 12 exclusive method/recipe/phase markers |
| requests/ | Exact worker requests |
| calibration/ | Normal rows, thresholds, display scales and resources |
| evaluation/ | Original predictions, aggregate metrics, selected gallery, resources |
| stress/ | Transformed saved predictions/metrics/resources |
| REPORT.md; gallery.html | Readable saved-output report and fixed-scale examples |
| SUPPLEMENT.json | Saved-prediction folder/interval/gallery hashes |

### 12.12 Audit boundary

This report audits available local evidence as of 19 October 2026. It is not independent replication, current external-source authentication, industrial certification or proof of complete historical execution. Existing source/data/model files were not modified; no model experiment was launched. Preserve this report with the exact working-tree snapshot and locally referenced ignored assets.
