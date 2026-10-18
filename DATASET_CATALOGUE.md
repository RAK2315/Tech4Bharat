    # Dataset catalogue for Inspection Workbench

**Research date: 17 October 2026 · Comprehensive project-scoped catalogue · 29 dataset/benchmark families**

## Read this first

**Current scope: components only.** Start with [the components-only shortlist](COMPONENT_DATASETS.md). This full catalogue is retained for reference; textile, raw-material and process-monitoring entries are not the first build's data plan.

This catalogue covers visual defect inspection, textile/metal/PCB alternatives, multi-view/3D inspection, production-quality prediction and factory simulation/replay. It expands the shortlist in [the team brief](TEAM_PROJECT_BRIEF.md).

It is an extensive, bounded scoping catalogue, not a guarantee that every industrial dataset worldwide has been found. A listed dataset is a candidate, not necessarily accessible, licensed for our eventual product, or representative of Indian small manufacturers. Research provenance is not industrial certification.

**Status:** only the selected VisA PCB1 assets have been downloaded and evaluated in our project. Other entries were assessed from sources; no new downloads or model runs were performed to prepare this document. A working source page is not proof that all linked archives can currently be downloaded.

**Priorities are our judgments:**

- **A — first-stage candidate:** directly supports the narrow visual experiment or required workflow test.
- **B — conditional alternative:** useful if we deliberately choose its product/task and clear access/licensing.
- **C — later research:** relevant to a separate extension; keep off the MVP critical path.
- **D — peripheral:** explains an adjacent capability, not a defect-inspection solution.

**Source status:** “primary checked” means an author/provider page or research publication was inspected. “partial” means the release, terms or schema still needs verification. All licences below are source descriptions, not a blanket clearance for commercial deployment; dataset, model weights and code can have different terms.

## 1. Recommended selection

| Need | Candidate | Reason | Boundary |
|---|---|---|---|
| Continue the existing image experiment | VisA PCB1 | Existing reproducible data/model setup and failure evidence | The tested detectors failed; use a new holdout for new tuning |
| Switch to one simpler industrial surface task | KSDD2 or one BTAD/MPDD category | Narrow products and defect annotations | Choose one; check capture conditions, normal data and licence |
| Test reference comparison | DeepPCB | Aligned reference/test pairs | Scanner/preprocessing and artificial defects limit field relevance |
| Test real captured lighting shifts | MVTec AD 2 | Explicit lighting changes | Non-commercial terms and partially private test labels |
| Explore textiles instead of components | AITEX AFID | Fabric images, codes and masks | Small dataset; licence and archive contents need checking |
| Simulate queues, inspection and rework | Our own seeded synthetic events | Direct control over required accounting cases | Fictional software test data; not evidence about factories |
| Test causal algorithms under known assumptions | causalAssembly | Benchmark graph and interventions | No validated target-factory causes |
| Investigate line replay | PerfCam; Future Factories as a lead | Production events or synchronized process data | Access/schema checks before adoption; not generic damage truth |

**Do not download everything.** Select one visual product category and a separate explicit synthetic event stream. Do not concatenate unrelated benchmarks and call them one factory dataset.

## 2. Visual anomaly detection and components

### 01. VisA — Visual Anomaly Dataset

- **Links:** [original repository, paper and downloads](https://github.com/amazon-science/spot-diff) · [official archive](https://amazon-visual-anomaly.s3.us-west-2.amazonaws.com/VisA_20220922.tar).
- **Data/purpose:** 10,821 images over 12 objects, including four PCB categories, with normal/anomalous labels and anomaly annotations; visual anomaly detection/localisation.
- **Project relevance: A.** Supports comparison of reference matching and established anomaly detection, threshold calibration, false alarms and review exercises.
- **Limits:** no linked machine histories or damage causes. Our local binary-mask mirror does not support subtype recall; physical-board identifiers are unavailable. The current compact PaDiM caught 45/80 test defects and falsely flagged 15/100 normal items; this is failed configuration evidence, not a dataset-wide verdict.
- **Access/licence/status:** primary checked; original data CC BY 4.0. Selected mirror assets already tested; provenance and custom split documented in [experiment README](experiment/README.md).

### 02. MVTec AD

- **Link:** [official dataset, paper and download page](https://www.mvtec.com/research-teaching/datasets/mvtec-ad).
- **Data/purpose:** more than 5,000 images across 15 object/texture categories; normal-only training and annotated anomalies for testing.
- **Project relevance: B.** A standard alternative for one product such as a metal nut, screw or bottle, or a texture category. Useful for defect localisation comparisons.
- **Limits:** controlled benchmark captures do not validate a phone workflow. Do not choose a category only because it produces attractive accuracy.
- **Access/licence/status:** primary checked; CC BY-NC-SA 4.0. Research/non-commercial restrictions apply; no commercial-product permission inferred.

### 03. MVTec AD 2

- **Link:** [official release, paper, utilities and evaluation server](https://www.mvtec.com/research-teaching/datasets/mvtec-ad-2).
- **Data/purpose:** over 8,000 high-resolution images in eight challenging scenarios, including reflective/transparent objects, small defects and illumination shifts. Initial paper 2025; current provider page cites an IJCV 2026 publication.
- **Project relevance: B.** Best shortlisted benchmark for testing actual captured lighting changes rather than only digitally brightened copies.
- **Limits:** private test labels require the official evaluation server; public labels support local initial evaluation. High resolution may increase runtime. Different objects still do not establish target-product robustness.
- **Access/licence/status:** primary checked; download form; CC BY-NC-SA 4.0. Download and evaluation access not exercised.

### 04. MVTec LOCO AD

- **Link:** [official release and evaluation code](https://www.mvtec.com/research-teaching/datasets/mvtec-loco-ad).
- **Data/purpose:** 3,644 images across five categories, with structural anomalies and logical anomalies such as missing required objects or invalid placement.
- **Project relevance: B.** Relevant if the chosen problem is packaging/assembly completeness rather than only scratches.
- **Limits:** counting/arrangement reasoning is a separate task from surface anomaly detection; a model suitable for one may fail at the other.
- **Access/licence/status:** primary checked; CC BY-NC-SA 4.0. Do not confuse logical anomalies with root-cause explanations.

### 05. KolektorSDD / KSDD

- **Link:** [ViCoS original release, annotations and folds](https://www.vicos.si/resources/kolektorsdd/).
- **Data/purpose:** 399 controlled industrial images: 52 visibly defective and 347 negative images, with fine or box annotation options.
- **Project relevance: B.** Small, focused surface-defect experiment with limited positive examples.
- **Limits:** very few defects and multiple views of items. Use physical-item grouping where available; a non-defect-visible view of a faulty item is not necessarily a healthy physical product. Preserve the distinction between image and product labels.
- **Access/licence/status:** primary checked; CC BY-NC-SA 4.0. Authors provide folds; inspect grouping before adapting splits.

### 06. KolektorSDD2 / KSDD2

- **Link:** [ViCoS original dataset and paper](https://www.vicos.si/resources/kolektorsdd2/).
- **Data/purpose:** 356 defective and 2,979 normal images; surface scratches, spots and imperfections. Released with 2021 research.
- **Project relevance: A/B.** A strong candidate if we deliberately change the experiment to one surface-inspection recipe.
- **Limits:** controlled industrial capture, not uncontrolled phone photos; no linked process causes. Audit labels and retain a separate calibration subset without contaminating the test set.
- **Access/licence/status:** primary checked; download link available; CC BY-NC-SA 4.0, commercial use requires contacting the provider. Full archive not tested.

### 07. BTAD — BeanTech Anomaly Detection

- **Link:** [authors' VT-ADL repository and dataset download](https://github.com/pankajmishra000/VT-ADL).
- **Data/purpose:** RGB images of three industrial products with pixel-level ground truth, introduced with VT-ADL in 2021.
- **Project relevance: B.** Small product-specific anomaly-detection alternative; useful for comparing model behaviour across a single declared capture setup.
- **Limits:** images were cropped and log-transformed for privacy. Their appearance is not an untreated phone-image distribution; product semantics may be less useful for a worker demonstration.
- **Access/licence/status:** primary checked; dataset source specifies CC-BY-SA (follow the linked exact terms); repository code MIT is separate. Archive not downloaded.

### 08. MPDD — Metal Parts Defect Detection

- **Link:** [authors' dataset repository, paper and download](https://github.com/stepanje/MPDD).
- **Data/purpose:** over 1,000 metal-part images with pixel-precise defects; anomaly-free training and a normal/anomalous evaluation subset. Research published in 2021.
- **Project relevance: B.** Directly relevant to component-manufacturing inspection and evaluating metal-part surface anomalies.
- **Limits:** reflective appearance and position variation can complicate reference methods; actual difficulty on our selected category must be measured. It is not a process-history dataset.
- **Access/licence/status:** primary checked; SharePoint download linked. Repository has a licence file, but exact dataset redistribution/commercial terms were not assessed here; verify before adoption.

### 09. NEU surface defects — NEU-CLS / NEU-DET / related segmentation releases

- **Link:** [original researcher's dataset page](https://faculty.neu.edu.cn/songkc/en/zdylm/263270/list/index.htm).
- **Data/purpose:** steel-surface defect classification/detection; the provider distinguishes image-only classification data from detection data with annotations and also links segmentation resources.
- **Project relevance: B.** Useful if we choose steel surface inspection and need explicit defect categories or boxes.
- **Limits:** task variants are not independent factories or interchangeable annotations. Verify normal-image availability: defective-class recognition alone cannot measure normal-item false-positive rate.
- **Access/licence/status:** primary checked; provider links cloud downloads. Exact reuse terms and raw contents not verified. Do not inherit a mirror's licence without checking the original.

### 10. Magnetic Tile Defects

- **Link:** [authors' repository for “Saliency of magnetic tile surface defects”](https://github.com/abin24/Magnetic-tile-defect-datasets.).
- **Data/purpose:** magnetic-tile surface images and pixel-level annotations, with folders for blowholes, breakage, cracks, fraying, unevenness and defect-free examples.
- **Project relevance: B.** A focused manufactured-component alternative for localisation and normal-versus-defective evaluation.
- **Limits:** tile texture/lighting and defect taxonomy are product-specific; no machine histories. Check actual file counts, group structure and label coverage before designing the experiment.
- **Access/licence/status:** primary checked; authors welcome research use and request citation. Explicit commercial/redistribution permission was not established; treat that as unresolved.

### 11. DeepPCB

- **Link:** [original repository and annotations](https://github.com/tangsanli5201/DeepPCB).
- **Data/purpose:** 1,500 aligned reference/test pairs, bounding boxes for open, short, mousebite, spur, pin hole and spurious copper.
- **Project relevance: B.** Particularly suitable for a reference-image difference baseline and localisation when a template exists.
- **Limits:** linear-scan CCD captures, registration and binarisation simplify the task; authors manually added artificial defects. This is bare-board pattern inspection, not evidence of assembled-board phone performance. Group crops by source board where identifiers permit.
- **Access/licence/status:** primary checked; README says dataset research use only even though repository metadata shows MIT. Respect dataset-specific restrictions; do not assume MIT clears the images.

### 12. Severstal Steel Defect Detection

- **Link:** [original Kaggle competition data](https://www.kaggle.com/competitions/severstal-steel-defect-detection/data).
- **Data/purpose:** steel-surface image segmentation challenge; a possible alternative when selecting a continuous sheet-surface task.
- **Project relevance: B, pending access.** Could evaluate defect masks and patch-wise processing on a specific surface domain.
- **Limits:** production-line scan appearance is different from a phone capture. The current tool retrieved no readable data-page body, so exact current counts, schema, licence and normal-image composition are not established by this catalogue.
- **Access/licence/status:** partial; Kaggle account/rules/download workflow must be checked. Do not adopt a third-party mirror's terms as the competition licence.

## 3. Textile datasets and synthetic texture controls

### 13. AITEX AFID — A Public Fabric Image Database

- **Link:** [official AITEX dataset, paper and archives](https://www.aitex.es/afid/).
- **Data/purpose:** provider describes 245 images of seven fabrics, normal/defective images and masks; defects include yarn/pick problems, knots, creases and contamination. Paper 2019.
- **Project relevance: B.** Strong domain alignment if the team chooses one textile and one visible defect family.
- **Limits:** small source-image count; cropping creates correlated patches, not independent cloth samples. Keep all patches from one source in one partition. Other reports list differing archive counts; verify the downloaded snapshot rather than silently resolving the discrepancy.
- **Access/licence/status:** primary checked; archive links present; dataset-specific commercial/redistribution permission not established on inspected page. Do not assume website availability means unrestricted reuse.

### 14. TILDA Textile Texture Database

- **Link:** [original Freiburg release](https://lmb.informatik.uni-freiburg.de/resources/datasets/tilda.en.html).
- **Data/purpose:** 1996 textile texture benchmark; eight textile kinds, normal/error classes, 3,200 grayscale TIF images and descriptive files.
- **Project relevance: B/C.** Useful as a classical textile baseline and for testing how texture changes affect error detection.
- **Limits:** repeated relocation/rotation of textile samples creates potential physical-sample leakage. Legacy capture and labels are not a modern factory phone benchmark; verify segmentation availability rather than assuming masks.
- **Access/licence/status:** primary checked; provider links download; original page lists approximately 1.2 GB. Exact reuse licence and current archive availability not verified.

### 15. ZJU-Leaper

- **Links:** [authors' API/baseline repository](https://github.com/nico-zck/ZJU-Leaper-Dataset) · [original paper](https://ieeexplore.ieee.org/document/9346038/).
- **Data/purpose:** fabric-inspection benchmark with progressive settings from normal-only data toward labelled defects; intended to reflect gradual data collection and deployment.
- **Project relevance: B, access unresolved.** Especially relevant to the challenge's small-data and non-expert-labelling constraints.
- **Limits:** third-party descriptions disagree on counts/subsets. Do not copy a mirror's taxonomy or assume download readiness; the inspected repository still lists download/API documentation tasks. No download or label-schema validation performed.
- **Access/licence/status:** primary paper/repository checked; exact accessible release and dataset licence unresolved. Keep off critical path until a small sample can be retrieved and verified.

### 16. DAGM 2007 Industrial Optical Inspection

- **Link:** [original competition, data description and downloads](https://conferences.mpi-inf.mpg.de/dagm/2007/prizes.html).
- **Data/purpose:** artificially generated texture backgrounds and defects, with weak elliptical labels; industrial optical-inspection algorithm benchmark.
- **Project relevance: C.** Useful for controlled synthetic debugging and demonstrating the difference between weak labels and precise masks.
- **Limits:** explicitly synthetic; cannot count as real-product accuracy evidence or realistic physical lighting. Ellipses are not pixel-perfect defect boundaries. Keep results separate from VisA/KSDD2.
- **Access/licence/status:** primary checked; legacy archive links shown; contemporary redistribution/commercial permission and link health not verified.

## 4. Multi-view and 3D research — outside the first MVP

### 17. Real-IAD

- **Links:** [authors' project](https://realiad4ad.github.io/Real-IAD/) · [author-hosted access page](https://huggingface.co/datasets/Real-IAD/Real-IAD).
- **Data/purpose:** CVPR 2024 multi-view industrial anomaly benchmark, approximately 150,000 images of 30 objects.
- **Project relevance: C.** Can investigate whether defects need multiple views and how to group all views of a physical item for evaluation.
- **Limits:** roughly 53 GB at 1024 resolution and 507 GB raw according to authors. Selecting one prescribed view changes the task and must be reported. Industrial collection does not imply target-MSME representativeness.
- **Access/licence/status:** primary checked; authors describe automatically approved access requests; dataset card specifies research-only CC BY-NC-SA 4.0. Access not requested here.

### 18. MVTec 3D-AD

- **Link:** [official dataset and paper](https://www.mvtec.com/research-teaching/datasets/mvtec-3d-ad).
- **Data/purpose:** over 4,000 industrial 3D scans in ten categories, defect-free training/validation and annotated defect tests; publication 2022.
- **Project relevance: C.** Can test geometry-sensitive defects with existing recorded scans, without purchasing a sensor for offline research.
- **Limits:** an ordinary RGB photograph does not supply equivalent depth. Results cannot support our hardware-free capture workflow or a whole-factory twin; local processing feasibility is untested.
- **Access/licence/status:** primary checked; download form; CC BY-NC-SA 4.0.

### 19. Real3D-AD

- **Links:** [official NeurIPS 2023 project](https://github.com/M-3LAB/Real3D-AD) · [original paper](https://arxiv.org/abs/2309.13226).
- **Data/purpose:** 3D point-cloud anomaly benchmark over twelve object categories; normal templates and annotated test point clouds.
- **Project relevance: C.** Optional geometry/reference-comparison research where a defect changes shape.
- **Limits:** specialised scanning, large point sets and few reference templates make it a different task. It does not reconstruct a factory or identify machine causes. No local performance assumptions.
- **Access/licence/status:** primary project/paper identified; archive retrieval and exact release licence not inspected. Treat licensing as unresolved rather than copying a secondary catalogue's claim.

### 20. Real-IAD D³

- **Links:** [CVPR 2025 paper](https://openaccess.thecvf.com/content/CVPR2025/papers/Zhu_Real-IAD_D3_A_Real-World_2DPseudo-3D3D_Dataset_for_Industrial_Anomaly_Detection_CVPR_2025_paper.pdf) · [authors' release card](https://huggingface.co/datasets/Real-IAD/Real-IAD_D3).
- **Data/purpose:** RGB, pseudo-3D and high-precision 3D industrial anomaly research across twenty categories.
- **Project relevance: C.** Tests whether geometry adds information that RGB misses; useful only for a deliberate later multimodal research branch.
- **Limits:** these modalities are not available from our prescribed single photograph. Additional data and model complexity; access approval may require an institutional email/affiliation.
- **Access/licence/status:** primary paper/card checked; research only, CC BY-NC-SA 4.0. Do not assume access within hackathon time; no request made.

## 5. Production quality, causal benchmarks and factory replay

### 21. SECOM

- **Link:** [official UCI release](https://archive.ics.uci.edu/dataset/179/secom).
- **Data/purpose:** 1,567 semiconductor production examples, 104 failures, process measurements and test timestamps; donated 2008.
- **Project relevance: C.** Small CPU-friendly candidate for a separate tabular quality-risk experiment or historical pass/fail replay.
- **Limits:** missingness, imbalance, no defect photos or verified physical line graph. UCI lists 591 features; inspect raw schema. Predictive feature importance is not causality.
- **Access/licence/status:** primary checked; approximately 1.9 MB download, CC BY 4.0. Not run locally.

### 22. Bosch Production Line Performance

- **Link:** [original Kaggle competition data](https://www.kaggle.com/competitions/bosch-production-line-performance/data).
- **Data/purpose:** manufacturing process measurements and failure prediction competition; candidate for production-quality risk analysis.
- **Project relevance: C, pending access.** Could examine measurement/date information for quality-risk research after schema validation.
- **Limits:** anonymisation limits actionable physical interpretation; dates are not automatically station service times or a complete routing/queue history. No defect-image linkage or intervention ground truth established.
- **Access/licence/status:** partial; current page body not readable through the research tool. Verify account requirements, competition rules, file sizes and raw schema before adopting. Do not claim unrestricted product use.

### 23. causalAssembly

- **Links:** [Bosch Research tool/data](https://github.com/boschresearch/causalAssembly) · [CLeaR 2024 paper](https://proceedings.mlr.press/v236/gobler24a.html).
- **Data/purpose:** benchmark production-line data/graph and a framework for generating semisynthetic data with hard/soft interventions.
- **Project relevance: C.** The closest shortlisted resource for evaluating causal-method behaviour under known benchmark assumptions; optional simulated intervention demonstrations.
- **Limits:** a benchmark graph is not the causal graph of a target small factory. No linked defect photographs. Fitting distributional random forests requires R and authors flag Windows rpy2 problems.
- **Access/licence/status:** primary checked in preceding research; package/data not run here. Code AGPL-3.0; confirm data terms separately. Plain seeded simulation is our fallback.

### 24. PerfCam

- **Links:** [official dataset and events](https://github.com/AstraZeneca/PerfCam-Dataset) · [2025 paper](https://arxiv.org/abs/2504.18165) · [implementation](https://github.com/AstraZeneca/PerfCam).
- **Data/purpose:** production-line digital-twinning proof-of-concept assets for reconstruction, tracking and experimental events.
- **Project relevance: C.** Candidate for historical line replay or investigating clickable station/event displays.
- **Limits:** reconstruction colour frames removed for compliance; only depth remains in that portion. Full released asset completeness and pipeline reproduction are untested. Product tracking is not defect inspection or cause validation.
- **Access/licence/status:** primary checked in preceding research; Git LFS for large files. Repository Apache-2.0 except specified YOLO weights under AGPL. Not downloaded.

### 25. Future Factories V2 — analog and synchronized multimodal datasets

- **Links:** [authors' 2025 paper](https://arxiv.org/abs/2502.05020) · [related Testbed-as-a-Service releases](https://github.com/m-r-mccormick/Testbed-as-a-Service/releases).
- **Data/purpose:** paper describes an eight-hour manufacturing-lab run and two datasets: analog time series and synchronized system data/images.
- **Project relevance: C, release mapping unresolved.** A promising lead for genuinely synchronized process/image research, unlike arbitrarily joining unrelated image and sensor benchmarks.
- **Limits:** do not assume images have visible-defect masks, per-product identity or causal ground truth. The related release must be matched to the exact V2 data/version; download size, licence and schema need verification.
- **Access/licence/status:** primary paper and related release page checked; actual V2 files and reuse terms not established. Not a hackathon-critical dependency.

### 26. AI4I 2020 Predictive Maintenance

- **Link:** [official UCI dataset and generating details](https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset).
- **Data/purpose:** 10,000 synthetic records with process variables and generated machine-failure modes.
- **Project relevance: C.** Lightweight illustration of synthetic alerts or risk-model evaluation when explicitly framed as maintenance research.
- **Limits:** machine failure is not a visible defective product. Generated relationships are assumptions, not discovered real causes. Exclude failure-mode targets from predictors when evaluating overall failure to avoid direct label leakage.
- **Access/licence/status:** primary checked; approximately 510 KB CSV, CC BY 4.0. Always label synthetic. Not run locally.

### 27. Condition Monitoring of Hydraulic Systems

- **Link:** [official UCI release](https://archive.ics.uci.edu/dataset/447/condition+monitoring+of+hydraulic+systems).
- **Data/purpose:** 2,205 experimental hydraulic test-rig cycles with sensor time series and component-condition labels.
- **Project relevance: C.** Optional demonstration of measured condition changes and time-series replay without owning the rig.
- **Limits:** test-rig equipment condition, not product-surface quality or a general factory model. Cycles may share experimental conditions; random splitting without grouping can overstate generalisation.
- **Access/licence/status:** primary checked; approximately 73.1 MB archive, CC BY 4.0. CPU feature extraction is a candidate, not a measured project result.

## 6. Adjacent vision datasets — counting/pose, not defects

### 28. MVTec Screws

- **Link:** [official dataset](https://www.mvtec.com/research-teaching/datasets/mvtec-screws).
- **Data/purpose:** oriented bounding-box detection; provider describes 384 images of thirteen screw/nut types on a wooden background.
- **Project relevance: D.** Could support a later item-finding/counting interface or orientation experiments.
- **Limits:** **not a screw-defect benchmark** and not the same as MVTec AD's screw category. Object identity/location does not tell us if the product is acceptable.
- **Access/licence/status:** primary provider page/catalogue checked; inspect exact release terms before use. Excluded from the first defect MVP.

### 29. MVTec ITODD

- **Link:** [official industrial 3D object detection/pose dataset](https://www.mvtec.com/company/research/datasets/mvtec-itodd).
- **Data/purpose:** industrial object detection and 3D pose estimation using multiple sensors.
- **Project relevance: D.** A later reference for locating parts in industrial scenes or bin-picking visualisation.
- **Limits:** no established defect ground truth or factory process history; extra pose/3D complexity does not solve our narrow inspection problem.
- **Access/licence/status:** primary checked; CC BY-NC-SA 4.0. Recorded assets do not establish phone capture compatibility; excluded from MVP.

## 7. Additional leads, not cleared dataset selections

These are separately listed to preserve discovery coverage without implying verified accessibility or adding them to the 29-family count:

| Lead | Purpose/relevance | Why not a cleared candidate yet |
|---|---|---|
| [LUSITANOv2 original publication](https://www.mdpi.com/2079-9292/15/19/4403) | Recent fabric-defect research from active textile production; potentially more relevant capture context than generic texture benchmarks | Publication surfaced during search; release files, licence, split grouping and full claims not assessed |
| [MVTec dataset directory](https://www.mvtec.com/research-teaching/datasets) | Discovery of related tracking, segmentation and pose datasets | Directory is not an additional dataset; most adjacent tasks do not supply defect labels |
| [Anomalib](https://github.com/open-edge-platform/anomalib) | Dataset loaders and reproducible anomaly-model experiments | Software library, not a dataset or independent validation source; each loader retains original data terms |

Generically named Kaggle/Roboflow mirrors, image collections without clear provenance, private industrial datasets and unrelated maintenance/medical/driving benchmarks are not enumerated as equivalent alternatives. New relevant releases may exist; absence here is not evidence they do not exist.

## 8. Our synthetic workflow fixture — required, not research evidence

Alongside the public image data, create a tiny seeded event fixture with product ID, batch ID, station, timestamp, image ID/hash, source, model version/flag, human decision and rework history. Include duplicates, missing photos, uninspected items, retakes, uncertain reviews and blocked approval.

- **Purpose:** test counts, UI, policy simulation and reports.
- **Relevance: A.** Necessary for the workbench even if every detector is removed.
- **Status:** the existing experiment already contains a small explicitly fictional accounting sequence; expanding it is proposed work.
- **Boundary:** injected defect truth evaluates simulator policies. It must not be exposed as if an image model discovered the defect. It is not factory demand, throughput or inspection-accuracy evidence.
- **No artificial linkage:** mapping benchmark images to fictional product IDs is an illustration; never call it a real linked image/process dataset.

## 9. Adoption and evaluation checklist

1. Select one product, prescribed view and visible defect definition. Define the decision a worker must make.
2. Retrieve a small sample from the original release; verify that links return actual files, not access pages or large-file pointers.
3. Record release/revision, source URLs, download date, checksums, attribution and dataset-specific licence. Keep code/weight licences separate.
4. Audit normal/defective counts, label meaning, ambiguous cases, physical-item identifiers and capture conditions. Compare archived counts with provider descriptions; disclose differences.
5. Split physical products, source boards, cloth rolls/source images and multi-view groups before generating crops or augmentations. Record any grouping uncertainty.
6. Separate reference/training, calibration and untouched test sets. Fit preprocessing on training only; select thresholds on calibration only.
7. Report recall/misses, normal false-positive rate, precision at observed prevalence, abstentions, retakes, coverage and latency with counts. Do not substitute AUROC for an operating-point assessment.
8. Keep untouched real-image results separate from artificial defects, synthetic generation and transformed lighting/blur tests.
9. Test captured lighting changes if available. Digital brightening cannot establish resilience to glare, shadows or hidden defects.
10. Measure human capture/review effort separately. Images alone do not establish workload savings, buyer acceptance or a lower consignment rejection rate.
11. Keep new tuning separate from the old final holdout. The current VisA failures remain valid historical results; rerunning does not create new independent evidence.
12. Before a public demo, review redistribution/display rights and free hosting limits. No paid API, affiliation access or commercial permission is assumed.

## 10. Search log and coverage limits

Searches used official provider pages, author repositories, arXiv, original CVPR/CLeaR/IEEE research pages, UCI and original competition pages. Secondary search hits were discovery leads, not substitutes for missing original licences. Preprints and conference/journal versions of the same resource were treated as one dataset family; mirrors were not counted as new datasets.

| Date | Query/source route | Result or unresolved issue |
|---|---|---|
| 17 Oct 2026 and preceding same-chat research | `VisA spot-diff dataset`; official Amazon repository/archive | Existing visual baseline; distinguish original annotations from binary mirror masks |
| 17 Oct 2026 | `MVTec AD 2 license download`; MVTec AD/LOCO/3D provider pages | Lighting and task alternatives; non-commercial restrictions |
| 17 Oct 2026 | `KolektorSDD2 official`; `DeepPCB official` | Focused surface and reference-pair candidates; controlled capture/artificial defects |
| 17 Oct 2026 | `industrial defect datasets official NEU DET severstal magnetic tile` | Additional metal/steel candidates; original Kaggle content inaccessible |
| 17 Oct 2026 | `fabric defect dataset official AITEX AFID ZJU leaper`; Freiburg TILDA | Textile coverage; small datasets, legacy capture, ambiguous access/licensing |
| 17 Oct 2026 | MPDD/BTAD author repositories; DAGM competition | Product alternatives and explicitly synthetic controls |
| 17 Oct 2026 | `Real IAD official dataset license`; `Real3D AD official`; `Real-IAD D3` | Multi-view/3D coverage; large downloads and approval constraints |
| 17 Oct 2026 and preceding same-chat research | SECOM, Bosch, causalAssembly, PerfCam primary pages | Risk/causal/replay candidates with different ground truth; no target-factory validation |
| 17 Oct 2026 | `FutureFactories dataset official multimodal manufacturing V2` | Promising synchronized data; exact release mapping unresolved |
| 17 Oct 2026 | UCI AI4I/hydraulic releases; MVTec Screws/ITODD | Explicitly separate maintenance/pose from product defects |

This was a single-reviewer scoping search, not a PRISMA systematic review. Ranked search results do not establish global exhaustiveness. Archives, full papers and legal terms were not all inspected end to end. No fabricated screening counts, download success, accuracy measurements or access approvals are reported.

## 11. Final selection rule

**For the present build:** one visual category + explicit synthetic workflow events. Choose a second visual benchmark only to answer a defined question such as lighting robustness. Keep causal, maintenance and 3D datasets off the critical path.

None of the verified candidates currently establishes a linked dataset of target-MSME product photographs, actual process history, physical product identity, valid interventions and buyer acceptance. Future Factories is a synchronized-data lead, not evidence that this full gap is solved. A dataset catalogue does not overturn the failed detector gate or validate demand.

## Method acknowledgement

Prepared using the installed literature-review skill for source tracking, scope and evidence limitations. Method resource: Kassis, T., Agarwal, V., He, Y., Patel, D., and Brueckner, A. M. (2026), [Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents](https://doi.org/10.48550/arXiv.2609.00065). This is a workflow reference, not a dataset or evidence supporting product performance.
