# Inspection Workbench: MVP, simulation and validation brief

**Team discussion draft · 17 October 2026 · Proposed scope, not a completed product**

## 1. Decision in one minute

- **What we can build:** a small, interactive inspection workbench with a simulated production line, product-level review, truthful coverage counts, alerts and a draft batch report.
- **What remains conditional:** an image-based assistant that usefully flags visible defects in one product category from one prescribed view. Our current tested detector configuration is inadequate.
- **What we should not promise:** a validated factory digital twin, automatic discovery of real damage causes, autonomous quality approval, reduced inspection time or acceptance by large buyers.
- **Current verdict:** conditional go for a bounded simulation demonstrator; no-go for deploying the tested detector as a reliable inspector. An operational inspection MVP needs another validation gate.
- **Candidate USP:** “See what was inspected, what the model flagged, what the person decided and what remains unknown—then test inspection policies in a clearly labelled simulation.” This is a positioning hypothesis, not validated demand or a claim of uniqueness.

## 2. Problem and target users

Problem statement 4.2 describes small component, packaging and textile units where visual inspection is manual, defects can reach buyers, and records are thin. The proposed first user is a line worker or supervisor; the owner approves batch records. A buyer's quality team is a possible report reader, not a confirmed customer.

The statement's “10–15% of defects missed” figure is supplied challenge context. We have not independently established that rate for our chosen product or target manufacturers. It is not a measured baseline for this project.

**Problem statement:** a small manufacturer needs a practical way to organise narrow visual inspections and record their coverage and outcomes without treating unchecked products as acceptable.

**Value proposition:** combine human inspection, optional measured AI assistance and traceable batch records; use simulation to explore workload and missed-defect trade-offs before making operational claims.

**Demand uncertainty:** we have no manufacturer or buyer interviews, representative factory images, rejection records or evidence that this workflow beats a spreadsheet plus existing inspection software. Public benchmark success would not establish commercial usefulness.

## 3. Constraints and hackathon fit

| Item | Current baseline |
|---|---|
| Implementation capacity | One Codex-assisted builder; this document can support teammate discussion, but extra capacity is not assumed |
| Frontend preference | TypeScript |
| Budget | Free tools/services; ask before any paid usage |
| Hardware | No new hardware; laptop CPU execution has been tested; GPU not required for the proposed simulation |
| Data and contacts | Public data only; no factory access, representative phone captures or manufacturer/buyer contacts assumed |
| Intended outcome | Eventually a deployed, extendable MVP; current work is a local experiment and this proposal |
| Dates retained from earlier research | Registration 10 November, idea 15 November, prototype 15 December, finale 27 December 2026 |
| Rules uncertainty | Earlier sources conflicted on team size/student eligibility; resolve directly before relying on eligibility |

The deadline dates above are retained conversation findings, **not freshly verified in this document**. The [HackCulture challenge page](https://hackculture.io/hackathons/tech4bharat-gavs-hackathon) could not be fetched during this document update. Reconfirm dates, eligibility, submission format, simulation disclosure and the exact judging rubric with the organiser. Do not invent judging weights.

The strongest connection to problem 4.2 is actual inspection assistance and honest quality records. A visually attractive factory simulation alone has weaker fit with the manual-inspection problem. AI performance must be measured; animation is not AI evidence.

## 4. What we already tested

The disposable experiment used actual native CPU inference on VisA PCB1 images. It compared simple reference-image matching with a compact PaDiM configuration using ResNet18 features. These are **our custom experimental results**, not official VisA leaderboard results or a reproduction of the authors' exact configuration.

| Untouched test result | Reference matching | Compact PaDiM |
|---|---:|---:|
| Defective items flagged | 15 / 80 | 45 / 80 |
| Defect recall | 18.75% | 56.25% |
| Defects missed | 65 / 80 | 35 / 80 |
| Normal items falsely flagged | 1 / 100 | 15 / 100 |
| False-positive rate | 1% | 15% |
| Precision at test prevalence | 15 / 16 = 93.75% | 45 / 60 = 75% |
| Model-assessed coverage | 180 / 180 | 180 / 180 |
| Native processing median / p95 | 138 / 156 ms | 85 / 97 ms |

- Test defect prevalence was 80/180 = 44.44%; it is not a factory prevalence estimate.
- Both methods failed the frozen provisional screen: recall at least 90%, normal-item FPR at most 10%, coverage at least 90%, and warm p95 processing at most five seconds. These were engineering targets, not validated industrial requirements.
- Reference/training: 100 normal images. Calibration: 100 normal and 20 defective images. Final test: 100 normal and 80 defective images. Thresholds were selected on calibration only.
- Exact/conservative near-duplicate checks found no pairs, but physical-board identifiers were unavailable. Physical-instance leakage cannot be ruled out.
- Synthetic brightening increased PaDiM false flags to 27/100 normal images. Transformed-image stress results are separate from untouched real-image results; they do not reproduce all physical glare or lighting effects.
- No retakes or abstentions occurred. That does not prove the simple image-quality gate was effective.
- Actual laptop browser inference matched decisions on ten selected fixtures; browser median/p95 was approximately 331/442 ms. This was a small parity check, not a full browser accuracy evaluation or phone test.
- The exported model is approximately 43.1 MB. Localhost download timing does not establish internet download performance.
- Human review time, capture workload and inspection-time savings remain unmeasured. The prepared user exercise is still pending.

**Implication:** compute speed is promising; detection usefulness is the blocker. A factory map cannot repair missed defects. Do not let unflagged images bypass human inspection on this evidence.

See [full experiment report](experiment/artifacts/EXPERIMENT_REPORT.md), [reproduction instructions](experiment/README.md), [failure gallery](experiment/artifacts/failure_gallery.html) and [prepared human exercise](experiment/artifacts/review_exercise.html).

## 5. What typical approaches look like—and our intended difference

These are plausible hackathon patterns, **not evidence about what every other team will build**.

| Common approach | Likely weakness | Our proposed difference |
|---|---|---|
| Upload photo → AI says good/bad | Hides misses, false alarms and unsupported conditions | Show measured limitations, human decision and unresolved status |
| Attractive 3D factory with red machines | Can imply live data or causal knowledge without evidence | Small 2D line; explicit simulated/replayed/observed provenance |
| Heatmap presented as an explanation | Anomaly location does not explain manufacturing cause | Describe it as an attention aid; no causal or severity claim |
| Dashboard showing a defect percentage | May omit uninspected products and denominator | Separate batch size, inspected count, model coverage and human outcomes |
| Generated “quality certificate” | May overstate inspection or buyer acceptance | Draft record with actual coverage, limitations and owner approval state |
| All products, all defects, phone-ready | Scope and generalisation are untested | One product/view and limited visible defects; expand only after testing |

**Existing solutions already cover substantial parts of this space.** [Cognex VisionPro Deep Learning](https://www.cognex.com/en/products/machine-vision-software/visionpro-deep-learning) is an established industrial inspection product; [Anomalib](https://anomalib.readthedocs.io/) provides open-source anomaly-detection tooling. We should reuse established techniques where suitable. These sources do not establish that our target users find those alternatives unaffordable or unusable.

Human review, reports and dashboards are individually copyable features. Our defensibility, if it emerges, would come from a validated product-specific capture recipe, useful review workflow, representative failure data and adoption—not a novel model or a factory animation. We have not established that moat yet.

## 6. Exact proposed demonstrator

**Working name:** Inspection Workbench. This is a team proposal, not an approved brand.

### One complete journey

1. Open a demo batch with a prominent **SIMULATED LINE** label and a declared product count.
2. Start a seeded simulation: products move through processing, inspection and rework stations. Station times and defect generation are declared assumptions.
3. Click the inspection station to view product IDs and statuses: uninspected, awaiting review, acceptable, defective, uncertain or rework pending.
4. Open a benchmark photograph. Show an optional model flag and attention map labelled **experimental benchmark inference**. Any assignment of that photograph to a simulated product is explicitly fictional.
5. A person records acceptable/defective/uncertain, visible defect category if known, and a note. A model flag never becomes a human decision automatically.
6. Re-upload a photo or rework a product: preserve history and prevent duplicate counting.
7. Trigger an alert using the human-confirmed inspected subset. Show numerator, denominator, time window and minimum sample count. Separate model-flag alerts from confirmed-defect alerts.
8. Open a draft batch report showing coverage, flags, decisions, unresolved items and limitations. An owner role can acknowledge the record; demo role acknowledgement is not a verified electronic signature.
9. Compare inspection policies under identical simulated arrivals and defect events. Report simulated missed defects, reviews, queues and completion time across repeated seeds.

### Must-have features

- One batch, one product recipe and a small clickable 2D line.
- Seeded, reproducible simulation with editable assumptions and clear provenance labels.
- Product IDs, image hashes, duplicate handling and append-only decision/rework history.
- Human review, uncertain status and accurate inspected/uninspected accounting.
- Alerts with clear denominators; no “zero defects” conclusion from no inspections.
- Exportable HTML/CSV report, printable to PDF, with owner approval state.
- Accessible nontechnical interface and a clear demo reset.
- Optional current detector only as a disclosed research component; stronger inspection claims require a new validation pass.

### Explicit exclusions

- Full 3D reconstruction, physics-based scratch formation, live machines, sensors and real-time factory tracking.
- Automatic real-world root-cause discovery or automatic machine-control recommendations.
- Autonomous batch acceptance or claims of buyer certification.
- All-product detection, hidden/internal defects, untested phone compatibility and measured time-saving claims.
- New paid APIs, expert labels fabricated by an LLM, or synthetic records presented as actual inspections.

## 7. Simulation: what it can and cannot establish

- **Discrete-event simulation:** models arrivals, station capacity, queues, inspection and rework. Appropriate for this scope.
- **Historical replay:** displays recorded observations in order. It does not predict the outcome of changing a machine setting.
- **Causal benchmark experiment:** tests methods against a known benchmark graph or generating mechanism. Its validity is limited to those assumptions.
- **Physics simulation:** predicts physical interactions from geometry, materials and calibrated contact/process models. We lack the necessary factory-specific inputs and validation; exclude it.

Use Python [SimPy](https://simpy.readthedocs.io/en/latest/) for the process model. Compare policies using the same underlying product events and repeated random seeds. Keep simulator truth inaccessible to the worker-facing inspection decision; otherwise the demo becomes an oracle that simply reveals injected labels.

The simulator may know which fictional items are defective for evaluation. A real inspection system does not know this without evidence. Displaying an injected defective item is not successful AI detection.

## 8. Research datasets and their roles

**Current team direction: start with components only.** Use [COMPONENT_DATASETS.md](COMPONENT_DATASETS.md) for the active shortlist; textile, packaging and process-monitoring alternatives below remain historical options rather than current build commitments. Select one component type and prescribed view before implementation.

For the expanded 29-family catalogue, including purpose, project relevance, links, access and licensing limitations, see [DATASET_CATALOGUE.md](DATASET_CATALOGUE.md).

“Research-grade” here means documented research provenance and a reproducible evaluation opportunity. It does not mean representative of Indian MSMEs or certified industrial ground truth.

| Dataset/tool | Appropriate use | Key limitation and access |
|---|---|---|
| [VisA / SPot-the-Difference](https://github.com/amazon-science/spot-diff), ECCV 2022 | Visual anomaly detection; PCB1 is already locally tested | No linked process history or damage causes. Data CC BY 4.0; code has separate terms. Our mirror's binary masks prevent subtype recall |
| [causalAssembly](https://github.com/boschresearch/causalAssembly), CLeaR 2024 | Manufacturing causal-method benchmark; semisynthetic generation and interventions | Not an image dataset or proof of real factory causality. R needed for fitting distributional random forests; Windows rpy2 issues documented. Code AGPL-3.0; check data distribution terms separately |
| [PerfCam](https://github.com/AstraZeneca/PerfCam-Dataset), 2025 research proof of concept | Production-event replay and investigation of a digital-twinning dataset | Reconstruction colour frames removed; only depth images remain in that part. Large assets not downloaded/tested here. Repository Apache-2.0 except specified YOLO weights under AGPL |
| [SECOM](https://archive.ics.uci.edu/dataset/179/secom), UCI 2008 | Small tabular quality-risk experiment: 1,567 examples, 104 failures, measurements and timestamps | Missing values, class imbalance, no defect photos or intervention ground truth. Roughly 1.9 MB download; CC BY 4.0 |

**Use first:** existing VisA assets for the inspection experiment and explicit synthetic events for the line. No external process dataset is necessary to test software accounting.

**Optional later:** causalAssembly if causal-method evaluation becomes an explicit research objective; PerfCam after checking assets and reproducibility; SECOM for a separate tabular-risk experiment. Do not add all three merely to claim more datasets.

**Never join unrelated datasets as if they describe the same physical products.** A VisA image attached to a SECOM record would be a fictional illustration, not multimodal factory evidence.

### 8.1 VisA — primary visual-inspection benchmark

- **Research provenance:** Zou et al., *SPot-the-Difference Self-Supervised Pre-training for Anomaly Detection and Segmentation*, ECCV 2022. [Original research repository, paper and download instructions](https://github.com/amazon-science/spot-diff).
- **What it provides:** normal/anomalous product photographs and anomaly annotations. Our experiment uses PCB1, one visible face of a board; original defect labels include Bent, Melt, Scratch and Missing.
- **What we can test:** reference matching versus an established anomaly detector, calibration-only thresholds, defect recall, false alarms, image processing latency and human review using benchmark images.
- **Access and current status:** public download instructions in the original repository. The local experiment used the [BrachioLab/visa mirror](https://huggingface.co/datasets/BrachioLab/visa), pinned to revision `d185c42584b49f1df81fe12bde627559ed88d483`. Mirror bytes have not been independently compared with the original archive. Existing local download was approximately 297 MB for the experiment assets; that is not the size of the entire original dataset.
- **Licensing:** original dataset CC BY 4.0; original project code Apache 2.0. Preserve attribution and check separate model-weight terms.
- **Hardware:** our configured native CPU inference has actually run; no GPU or paid API was required. This does not establish the requirements of every method trained on VisA.
- **Critical limitation:** the mirror masks used locally are binary. They do not support per-defect-type recall without verified subtype annotations. There are no linked factory process records or physical-board IDs; no causal analysis or guaranteed physical-instance split is possible from those assets alone.
- **Decision:** use first, but preserve the existing failed holdout as historical evidence. New tuning needs a new untouched holdout rather than recycling it as independent validation.

### 8.2 causalAssembly — causal-method research, not visual inspection

- **Research provenance:** Göbler et al., *causalAssembly: Generating Realistic Production Data for Benchmarking Causal Discovery*, CLeaR 2024. [Original paper](https://proceedings.mlr.press/v236/gobler24a.html) · [Bosch Research code, data and examples](https://github.com/boschresearch/causalAssembly).
- **What it provides:** a manufacturing benchmark framework, production-line graph/data access, and semisynthetic data generation. Supports hard and soft interventions within its model.
- **What we can test:** whether a method recovers benchmark relationships; how interventions change simulated outcomes under the specified generating assumptions.
- **Access:** repository examples expose `ProductionLineGraph.get_data()` and `get_ground_truth()`. Installation instructions use `pip install causalAssembly`; this package and its data have not been installed/downloaded for our project.
- **Licensing:** repository code AGPL-3.0. Confirm the applicable data terms and obligations before redistribution or integration into a hosted application.
- **Implementation risk:** fitting distributional random forests requires R; the authors warn that `rpy2` may cause Windows issues. Run a small dependency/data-loading spike before adopting it. A plain seeded process simulator remains the fallback.
- **Critical limitation:** benchmark ground truth concerns the benchmark model. It cannot establish which machine causes defects in a real factory, and it does not supply defect photographs linked to those process variables.
- **Decision:** optional research branch; exclude from the critical path of the inspection-workflow demonstrator.

### 8.3 PerfCam — production-line digital-twinning research assets

- **Research provenance:** KTH/AstraZeneca, *PerfCam: Digital Twinning for Production Lines Using 3D Gaussian Splatting and Vision Models*, 2025 research proof of concept. [Paper/preprint](https://arxiv.org/abs/2504.18165) · [Official dataset and experiment links](https://github.com/AstraZeneca/PerfCam-Dataset) · [Implementation](https://github.com/AstraZeneca/PerfCam).
- **What it provides:** assets and documentation associated with reconstruction, object/event detection and a production-line experiment. The release is not a generic, ready-to-use factory simulator.
- **What we can test:** whether released events and assets can support a reproducible historical replay or line-status visualisation.
- **Access:** use the official repository's experiment/event and dataset links. Large files use Git LFS. We have inspected documentation, not downloaded and verified the full assets or reproduced the pipeline.
- **Licensing:** repository files Apache-2.0 except specified YOLO weight files under AGPL; retain asset-level notices.
- **Critical restriction:** colour frames were removed from the reconstruction portion for compliance reasons; only depth images remain there. Do not assume the complete colour reconstruction procedure can be reproduced from released data.
- **Hardware:** recorded data can be explored without buying capture hardware; full 3D reconstruction/runtime feasibility on our laptop is untested and outside the proposed MVP.
- **Decision:** secondary lead for replay research. Do not make the public demo depend on complete 3D reproduction or treat its tracking results as defect-classification evidence.

### 8.4 SECOM — lightweight manufacturing quality-risk benchmark

- **Research provenance:** McCann and Johnston, UCI Machine Learning Repository, 2008. [Official dataset, schema, files and licence](https://archive.ics.uci.edu/dataset/179/secom) · [Dataset DOI](https://doi.org/10.24432/C54305).
- **What it provides:** 1,567 semiconductor production examples, including 104 failures, process measurements, pass/fail labels and test timestamps. UCI lists 591 features; confirm the raw schema before implementation rather than hard-coding that count.
- **What we can test:** a CPU tabular quality-risk baseline, missing-value handling, class-imbalance evaluation and timestamped record replay.
- **Access:** official archive approximately 1.9 MB; raw measurement file approximately 5.1 MB. No paid inference service is required. Not downloaded or evaluated in this project.
- **Licensing:** CC BY 4.0 with attribution.
- **Implementation precautions:** partition before fitting imputers/scalers or selecting features; never leak test labels into preprocessing. Check timestamp ordering and the proposed deployment task before choosing a temporal or random split. Report failure recall and false alarms rather than accuracy alone.
- **Critical limitation:** no visual defect images, verified station-routing model or intervention ground truth. Predictive feature importance is not a real-world causal diagnosis.
- **Decision:** suitable for a separate small quality-risk experiment, not a replacement for validating the image-based assistant.

### 8.5 Dataset adoption checklist

Before using any new release in the demo:

1. Confirm the official release, version, licence, attribution and redistribution terms.
2. Download a small sample first; check real files rather than metadata or Git LFS pointers alone.
3. Record checksums, schema, labels, missingness, known physical-item identifiers and capture conditions.
4. Define reference/training, calibration and untouched test partitions before tuning; group physical items and near duplicates wherever possible.
5. State whether observations are real, replayed, semisynthetic or fully synthetic; keep transformed stress tests separate from real-image results.
6. Save reproducible evaluation settings and failures. Do not infer factory performance from unrelated research benchmarks.

**Selection summary:** VisA for the existing visual experiment; explicit synthetic events for software/workflow simulation; causalAssembly only for a scoped causal-benchmark experiment; PerfCam only after asset verification; SECOM only for a distinct tabular-risk task. No single verified dataset in this shortlist supplies linked images, process measurements, physical product identity and validated real damage causes for our target users.

## 9. Architecture and deployment

Recommended implementation choices, pending product build approval:

- **Frontend:** React + TypeScript with a simple 2D SVG/HTML station view. Easier to review and maintain than a 3D engine for this task.
- **Simulation:** Python + SimPy; save run seed, parameters, policy and output events. Prefer precomputed runs for a dependable public demo if continuous hosting is unavailable.
- **Inspection research:** existing native Python environment. Browser ONNX inference remains optional because full test-set parity, image gates and phone behaviour are unverified.
- **Storage:** local SQLite for a single-machine prototype; portable JSON/CSV exports. A public multi-user service needs authenticated server-side storage and access controls.
- **Reporting:** deterministic HTML/CSV generated from event history; user prints HTML to PDF. No LLM needed to invent explanations.
- **Deployment:** a static frontend with disclosed precomputed simulation runs is the simplest free-hosting candidate. It must not claim live server inference. Free-host terms, storage, model-file limits and quotas must be verified at deployment time; no permanent free hosting assumed.

Alternatives: an all-TypeScript seeded simulator avoids a Python service but requires carefully implementing event scheduling; a local Python service keeps native inference and simulation together but is harder to make continuously available for free.

For a public demo, use public benchmark data only. Real factory uploads would require explicit permission, retention/deletion controls, authenticated access and secure handling. Do not expose the local experiment server publicly. Hashes and an append-only log help traceability but do not alone make records tamper-proof.

## 10. Problems we may encounter and responses

| Risk | Response / cheapest test | Remaining limitation |
|---|---|---|
| Too little representative data | One product/view; preserve held-out sets; collect actual target captures only with permission | Public data cannot validate field transfer |
| Current model misses defects | Inspect failures; timebox alignment/crop or resolution changes; evaluate on a new holdout | No promised accuracy improvement; stop AI branch if it fails |
| Lighting, glare or blur | Prescribed distance/view/background and controlled capture guidance; test real variation; abstain when unsuitable | Software cannot reconstruct a defect hidden by glare |
| Non-expert labels disagree | Plain defect examples, uncertain option, second review of disputed cases | No expert access currently; do not invent consensus |
| Too many false alarms | Calibration-only threshold selection; measure workload at plausible prevalence | High benchmark precision may collapse at low prevalence |
| Tiny defects vanish at resize | Inspect crop/resolution alternatives within a frozen follow-up protocol | More detail can increase memory and runtime |
| Product changes | Version recipes and reference sets; require revalidation | No automatic transfer claim |
| Duplicate photos/rework inflate counts | Separate product, photo and review IDs; preserve attempts/history | Exact hashes do not detect every altered duplicate |
| Simulator manufactures its conclusion | Publish assumptions; repeat seeds; keep truth separate; sensitivity analysis | Valid only within the specified model |
| Cause claims from correlations | Report associations; evaluate interventions only within causal benchmark | Real causality still requires domain evidence |
| Model download/hosting fails | Native local demo or labelled precomputed inference; inspect hosting limits | Precomputed output is not live inference |
| Browser/phone fails | Native CPU fallback; test actual phones before promising support | Laptop parity does not establish phone readiness |
| Owner/report workflow is misleading | Draft status, unresolved counts, explicit acknowledgement; preserve overrides | No buyer acceptance or verified signature claim |
| No user demand | Short feedback exercise against spreadsheet/current workflow | No interviews completed; feature interest is not adoption |
| Scope consumes the deadline | Cut 3D, live integration, generic product support and causal branch first | Simulation-only entry may be weaker for Applied AI judging |

## 11. Validation gates and delivery plan

These are **planning timeboxes, not measured delivery estimates**. Extra teammates are not assumed. A reliable full inspection-MVP estimate is unavailable while the detector prerequisite fails.

| Stage | Timebox | Deliverable / decision |
|---|---|---|
| Reconfirm rules and select scope | Half a working day | Eligibility/deadline check; one product and supported visible-defect definition |
| Complete prepared human review exercise | One short participant session plus analysis | Actual review timings/errors; disclose order bias, artificial prevalence and absent capture time |
| Narrow detector follow-up | 1–2 working days maximum | One justified change, calibration-only tuning and a new untouched holdout; continue or stop |
| Simulation and accounting spike | 1–2 working days | Reproducible policy comparison; duplicate/rework/uninspected invariants |
| Integrate interface and report | 2–3 working days | One complete review journey and truthful export |
| Packaging and deployment check | One working day | Reproducible demo, limits, reset and fallback |

The demonstrator allocation is approximately 4–6 working days after scope selection, excluding the optional detector follow-up and unpredictable hosting/setup issues. This is a proposed effort budget, not evidence-backed certainty or a promise. Re-estimate after the simulation spike.

**Inspection gate:** pre-register recall, false-positive, coverage/abstention and latency targets; use the existing 90% / 10% / 90% / five-second screens only as provisional starting points. Agree defect severity and miss tolerance before interpreting them. Measure counts and uncertainty, not percentages alone.

**Human gate:** measure manual versus assisted error and review time. The existing 24-image exercise is a convenience pilot with manual-first order and unmatched item difficulty. It can expose problems; it cannot establish factory efficacy. A stronger follow-up should counterbalance order and include capture/retake effort.

**Simulation gate:** same seed/configuration reproduces results; counts reconcile; duplicates do not create new products; rework retains history; sampled inspection is never labelled full coverage. Compare policies over repeated seeds and report variability.

**User gate:** obtain permission-based feedback from a manufacturer or buyer when contacts become available. Ask them to review the sample report, explain their current alternative, identify missing evidence and estimate added steps. Do not claim validation until feedback exists.

## 12. Three-minute demo

1. State the boundary: “This is a simulated line and benchmark inspection research; it is not connected to a factory.”
2. Run a small seeded batch; click the inspection station and show pending/uninspected products.
3. Review one flagged and one unflagged image; demonstrate that unflagged does not mean approved.
4. Enter an uncertain decision and a rework event; upload a duplicate and show unchanged unique-product counts.
5. Trigger a defect-rate alert with an explicit inspected denominator.
6. Export a draft report showing incomplete coverage and pending owner acknowledgement.
7. Compare two inspection policies, then show detector misses and measured limitations. Close with the next validation gate, not a production-readiness claim.

## 13. What would change the verdict?

- **Upgrade to a narrow inspection MVP:** new untouched images meet provisional performance targets, a human pilot shows acceptable workload/error trade-offs, and the capture recipe is practical.
- **Upgrade to a useful factory tool:** representative target-unit trials show value compared with current practice, users can maintain records, and data/privacy/deployment requirements are met.
- **Keep simulation only:** policy experiments and accounting work, but detector usefulness remains unproven. Pitch as research/workflow evaluation; acknowledge weaker direct fit with defect reduction.
- **Stop or change problem:** model misses remain unacceptable, capture/review adds too much work, users already have an adequate alternative, or eligibility cannot be met.
- **Strongest evidence against building now:** the actual detector experiment failed; no real-user benefit or demand is established. Attractive simulation does not outweigh those findings.

## 14. Evidence, assets and open questions

- **Measured local evidence:** [experiment report](experiment/artifacts/EXPERIMENT_REPORT.md), [frozen protocol](experiment/PROTOCOL.md), [reproduction guide](experiment/README.md), [failure gallery](experiment/artifacts/failure_gallery.html).
- **Prepared, not validated:** [sample batch report](experiment/artifacts/sample_batch_report.html), [human exercise](experiment/artifacts/review_exercise.html), [manufacturer/buyer feedback exercise](experiment/feedback.md). Sample ledger/human decisions are fictional; no owner or buyer endorsement exists.
- **Technical references:** [PaDiM paper](https://arxiv.org/abs/2011.08785), [ONNX Runtime Web](https://onnxruntime.ai/docs/get-started/with-javascript/web.html), [SimPy](https://simpy.readthedocs.io/en/latest/), plus dataset and competitor links above.
- **Source freshness:** dataset/repository facts were checked in the preceding research on 17 October 2026. Hackathon page inaccessible on this update; exact rules need reconfirmation. PerfCam/causalAssembly/SECOM were researched, not downloaded or run in this project.
- **Search coverage:** official dataset repositories, original research pages, UCI, simulation documentation and existing inspection tooling. This brief synthesises that work; it is not a new systematic market review or an exhaustive competitor census.
- **Unresolved:** actual target product/defect severity, factory prevalence, physical-instance leakage, expert labels, phone performance, user workload, buyer evidence requirements, hosting limits and team eligibility.

**Team decision requested:** choose whether to pursue the bounded simulation demonstrator while completing the inspection validation gates. Do not interpret this brief as approval to claim a reliable factory inspector or a validated digital twin.
