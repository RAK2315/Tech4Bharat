# Components-only dataset shortlist

**Scope update: 17 October 2026 · Components are the first product domain**

Extracted and prioritised from [the full dataset catalogue](DATASET_CATALOGUE.md). This document narrows data selection; it does not claim that a new detector or application has been built.

## 1. What “components only” means here

- **Electronic assemblies:** populated PCBs, where visible damage or missing parts may be inspected.
- **Mechanical/electrical parts:** metal parts, fasteners, magnetic tiles and similar discrete manufactured components.
- **Bare PCBs:** a separate reference-comparison task, because conductive-pattern defects and scanner captures differ from populated-board photographs.
- **Exclude from the first build:** textiles, food, general packaging, sheet-steel inspection, machine maintenance, automatic cause discovery and 3D reconstruction.

One component type, one prescribed view and a defined set of visible defects remain the first experiment's scope. “Components” is a domain choice, not permission to promise detection for every component.

## 2. First choices

| Priority | Dataset / selected subset | Purpose | Why it is relevant | Important condition |
|---|---|---|---|---|
| 1 — continue existing work | **VisA PCB1** | Visual anomalies on an assembled electronic board | Existing local references, calibration, inference, reports and failure examples | Current detector failed; improvements require a new untouched holdout |
| 2 — mechanical-part alternative | **MPDD: one part category** | Detect/localise defects on metal parts | Direct fit for component manufacturing | Inspect sample images, exact category and data terms before choosing |
| 3 — focused surface alternative | **KSDD2** | Industrial surface imperfections | Narrow inspection task with normal and defective examples | Controlled acquisition and non-commercial licence; verify product context |
| 4 — familiar component benchmark | **MVTec AD: metal_nut, screw or transistor** | Normal-only training and anomaly localisation | Recognisable discrete components for a narrow demo | Pick one category; non-commercial restrictions apply |

**Recommendation:** keep PCB1 as the immediate diagnostic experiment because it is already available. Do not choose it as the final product until a revised configuration passes validation. If the team wants mechanical parts instead of electronics, inspect MPDD samples first, with KSDD2 or a single MVTec component category as alternatives. No model improvement is assumed from switching datasets.

## 3. Directly relevant component datasets

### 1. VisA — PCB1, PCB2, PCB3 and PCB4 only

- **Link:** [official research repository and download](https://github.com/amazon-science/spot-diff).
- **Purpose:** visual anomaly detection and localisation on populated circuit boards.
- **Relevance:** highest continuity with our existing electronic-component experiment. Use PCB1 alone initially; other PCB categories are separate later tasks, not automatic extra training examples for PCB1.
- **Supported claims:** benchmark defect flagging and review performance under the selected images/capture conditions.
- **Limits:** no process causes, phone validation or guaranteed physical-board identity. Original labels are not automatically predicted defect classes; our local masks are binary.
- **Licence/status:** data CC BY 4.0. PCB1 subset already tested; other subsets not evaluated here.
- **Existing evidence:** compact PaDiM flagged 45/80 defects, missed 35/80 and falsely flagged 15/100 normal items. Reference matching flagged 15/80 defects. Both failed the provisional screen. See [full experiment report](experiment/artifacts/EXPERIMENT_REPORT.md).

### 2. MPDD — Metal Parts Defect Detection

- **Link:** [authors' repository, paper and dataset download](https://github.com/stepanje/MPDD).
- **Purpose:** visual defect detection/localisation on industrial metal parts; over 1,000 images with pixel-level masks.
- **Relevance:** a direct candidate for a mechanical-component inspection assistant.
- **Use:** select one documented part category, inspect defect visibility, then compare reference matching and an established anomaly method.
- **Limits:** position and reflective appearance can challenge spatial comparison. Actual ease and CPU performance are unmeasured; no linked machine-cause evidence.
- **Licence/status:** original source checked; archive not downloaded. Verify exact dataset reuse terms from the licence and release before adopting.

### 3. KolektorSDD2 / KSDD2

- **Link:** [official ViCoS dataset and paper](https://www.vicos.si/resources/kolektorsdd2/).
- **Purpose:** industrial surface-defect detection, including scratches, spots and imperfections; 356 defective and 2,979 normal images.
- **Relevance:** focused alternative for inspection of a visible component surface.
- **Use:** binary flagging/localisation with a clearly described surface/view; retain normal items to measure false alarms.
- **Limits:** controlled industrial capture is not representative phone capture. Confirm the actual item/surface context before using product-specific wording in the demo.
- **Licence/status:** CC BY-NC-SA 4.0; commercial use requires contacting the provider. Source checked, archive not tested locally.

### 4. KolektorSDD / KSDD — original release

- **Link:** [official release, masks and folds](https://www.vicos.si/resources/kolektorsdd/).
- **Purpose:** defect detection on production-item surfaces; 399 images, including 52 visibly defective images.
- **Relevance:** compact small-data experiment for component surfaces.
- **Use:** study reference scarcity and localised defect review.
- **Limits:** few defects and multiple views of items. Preserve physical-item grouping; an image without a visible defect is not proof that the whole item is defect-free. Do not treat it as the same release as KSDD2.
- **Licence/status:** CC BY-NC-SA 4.0; source checked, not run here.

### 5. MVTec AD — selected component categories

- **Link:** [official dataset and evaluation references](https://www.mvtec.com/research-teaching/datasets/mvtec-ad).
- **Select:** `metal_nut`, `screw` or `transistor`; `cable` may be considered if that is the actual chosen product.
- **Purpose:** anomaly detection/localisation from normal training examples and annotated tests.
- **Relevance:** recognisable components with a bounded product-specific inspection task.
- **Use:** evaluate one category at a time; define which defect types/views our workflow supports.
- **Limits:** laboratory conditions, limited product variety and benchmark annotations do not establish tolerance compliance or field reliability. The `screw` category is distinct from the MVTec Screws object-detection dataset.
- **Licence/status:** CC BY-NC-SA 4.0; source checked, no local evaluation.

### 6. Magnetic Tile Defect Dataset

- **Link:** [authors' dataset repository](https://github.com/abin24/Magnetic-tile-defect-datasets.).
- **Purpose:** surface-defect localisation on magnetic tiles, with categories/folders covering cracks, breakage, blowholes and other imperfections plus defect-free examples.
- **Relevance:** a specific manufactured component suitable for a product-focused demonstration.
- **Use:** inspect image/mask quality and choose a limited visible defect definition before splitting.
- **Limits:** product texture and lighting may not transfer to other components. No linked process histories or true physical cause labels.
- **Licence/status:** authors welcome research use and request citation; unrestricted commercial/redistribution permission was not established. Resolve before adoption; not downloaded here.

### 7. DeepPCB — bare-board alternative

- **Link:** [original dataset and annotations](https://github.com/tangsanli5201/DeepPCB).
- **Purpose:** reference/test comparison with bounding boxes for six conductive-pattern defects; 1,500 aligned image pairs.
- **Relevance:** especially useful for a classical reference-matching baseline when the product is a bare PCB.
- **Use:** demonstrate differences such as open/short circuits in the visible pattern; do not imply electrical testing has occurred.
- **Limits:** scan images are aligned/preprocessed, and authors added artificial defects. Not equivalent to populated-board or phone inspection. Keep crops from the same source board grouped where identifiers permit.
- **Licence/status:** README restricts dataset to research despite MIT repository metadata; dataset restrictions must be respected. Not run here.

## 4. Conditional component candidates — inspect subsets before adoption

| Dataset and link | Purpose and component relevance | Why conditional |
|---|---|---|
| [Real-IAD](https://realiad4ad.github.io/Real-IAD/) | Multi-view anomalies across manufactured objects; useful for a component category after verifying its schema and item IDs | Large release; approximately 53 GB downsampled / 507 GB raw. Research-only CC BY-NC-SA 4.0 and access workflow. Select a component subset and one view; no need to ingest all objects |
| [BTAD](https://github.com/pankajmishra000/VT-ADL) | Industrial anomaly images for three products with masks; possible component/surface alternative | Confirm product identity and worker relevance from samples. Privacy preprocessing changes appearance. Dataset CC-BY-SA; follow exact linked terms; not the code's MIT licence |
| [MVTec AD 2](https://www.mvtec.com/research-teaching/datasets/mvtec-ad-2) | `Wall Plugs` is a component-relevant candidate; useful for difficult visibility/lighting research | Overlap and bulk objects depart from one-item/one-view scope. Non-commercial terms; partly private labels. `Sheet Metal` concerns material surfaces and is excluded from this component-only first build |

These are alternatives, not extra datasets to combine indiscriminately. Preserve physical-item and multi-view groups across partitions.

## 5. Later component research, outside the first build

| Dataset and link | Potential purpose | Why defer |
|---|---|---|
| [MVTec 3D-AD](https://www.mvtec.com/research-teaching/datasets/mvtec-3d-ad) | Geometry-aware defect research if a relevant category is selected | Requires depth/3D inputs absent from the single-image workflow; non-commercial terms |
| [Real3D-AD](https://github.com/M-3LAB/Real3D-AD) | Point-cloud shape anomaly/reference comparison | Object/category fit, licence and processing must be checked; not a phone or factory-twin solution |
| [Real-IAD D³](https://huggingface.co/datasets/Real-IAD/Real-IAD_D3) | Component inspection combining RGB, pseudo-3D and 3D | Research-only/access constraints and unavailable target capture modalities |
| [MVTec Screws](https://www.mvtec.com/research-teaching/datasets/mvtec-screws) | Find/count/orient screws and nuts | Object detection, not defect labels; cannot train or validate acceptable/defective decisions by itself |
| [MVTec ITODD](https://www.mvtec.com/company/research/datasets/mvtec-itodd) | Industrial part pose/localisation research | No established defect labels; 3D pose is outside scope; non-commercial terms |

## 6. Removed from the active selection

- **AITEX AFID, TILDA and ZJU-Leaper:** textiles, excluded by the components-only direction.
- **NEU surface datasets and Severstal:** raw steel surface inspection, excluded from the discrete-component first build. Reconsider only if the actual target changes to sheet material.
- **MVTec LOCO AD:** potentially useful for later assembly completeness, but not selected without a matching component task/subset.
- **SECOM, Bosch Production Line, AI4I and hydraulic monitoring:** process quality or machine condition, not training data for visible defects on our chosen component.
- **causalAssembly, PerfCam and Future Factories:** separate causal/replay research; not linked component-defect truth for this MVP.
- **DAGM:** synthetic texture data, unnecessary for the first component experiment.

The full catalogue remains available as research history. Exclusion here means out of current scope, not that a dataset has no value.

## 7. Next selection and validation steps

1. Choose **electronics (PCB1)** or **one mechanical part**, not both for the first recipe. Until that decision changes, PCB1 is the existing diagnostic baseline only.
2. For a new candidate, inspect a small sample of normal/defective images, labels and licence before a large download.
3. Specify visible defects, view, distance/scale assumptions and unsupported cases; no automatic subtype claims from binary anomaly labels.
4. Group physical items/source boards/views before splitting. Separate training/reference, calibration and untouched test images; disclose missing identifiers.
5. Set provisional recall, false-alarm, coverage/abstention and latency targets before inference. Calibrate thresholds only on calibration data.
6. Report misses and false flags with counts. Keep synthetic defects and transformed lighting tests separate from untouched captured images.
7. Complete human review testing before claiming time savings. Continue human inspection of unflagged products until skipping them has evidence.
8. Use explicit fictional events for line/rework/accounting tests; do not claim the benchmark's components came from our simulated line.

**Decision boundary:** choosing components makes the build narrower. It does not resolve the failed detector gate, prove small-manufacturer demand or create permission to deploy research-only datasets commercially.

## Source and evidence status

This is a filtered synthesis of the sources checked for [DATASET_CATALOGUE.md](DATASET_CATALOGUE.md) on 17 October 2026 and the local experiment report. No new dataset download, accuracy run, phone test or user feedback was performed for this scope update. Exact subset contents and permissions still require the checks stated above.
