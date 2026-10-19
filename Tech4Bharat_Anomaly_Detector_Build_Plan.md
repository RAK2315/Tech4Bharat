# Tech4Bharat Component Anomaly Detector Build Plan

> **Execution:** use `executing-plans` task by task; no subagents without explicit
> user authorization. Under standing sequential authorization, complete each
> eligible numbered stage and its automatable checks, then continue when gates
> pass. Personal decisions, access/terms, experimental failure gates and external
> publication restrictions still apply. Editing this plan does not execute it.

**Updated:** 18 October 2026, following the user's cable-gland dataset selection.

**Goal:** evaluate RGB-only cable-gland defect inspection and a separate KSDD2
surface-inspection task, then build a human-review application only for recipes
supported by the experiment. No nut/bolt inspection performance is claimed.

**Architecture:** source inventory -> audited grouped data roles -> separate
reference/PaDiM models -> frozen calibration/evaluation -> local inference ->
human decisions -> batch history and truthful reports -> verified delivery mode.

**Stack:** Python 3.12, CPU PyTorch/PaDiM, Pillow/NumPy, FastAPI/Pydantic, SQLite,
React/TypeScript/Vite. No paid API, GPU requirement, 3D engine or factory hardware.

**Binding detailed contract:** [current execution plan](Tech4Bharat_Codex_Execution_Plan.md)
defines exact T01-T10 interfaces, file responsibilities, numerical rules, API
schemas and checks. [Build playbook](docs/superpowers/plans/2026-10-18-codex-build-playbook.md)
provides stages 0-10 and manual checks. [Scope amendment](components/docs/CABLE_GLAND_SCOPE.md)
records the dataset replacement. Use those current contracts if old review notes
or catalogues differ; do not revive their old rotation-bank or tiled-model designs.

## Current verified starting point

- `components/.venv-p0`: Python 3.12.14 with lightweight setup dependencies.
- `doctor` and bounded `acquire` are implemented. Model/API/UI commands are not.
- Cable gland and KSDD2 are acquired and hashed, not fully audited or split.
- The latest component suite passed 58 tests; no new model accuracy is measured.
- Original MVTec AD metal nut is deferred after access failure, not an active gate.
- Preserve the old PCB experiment and its failed detection results as history.
- Preserve unrelated working-tree edits. Raw data, weights and caches stay ignored.

## 1. Datasets and permitted conclusions

| Role | Dataset and recipe | Current data | Task |
|---|---|---|---|
| D1, primary | MVTec 3D-AD cable_gland; `mvtec_3d_cable_gland_rgb` | 223 training normals, 23 validation normals; test 21 normal +87 anomalous RGB files | Binary visible anomaly and optional attention map on this cable-gland view |
| D2, independent | KSDD2; `ksdd2_surface` | Provider counts: train 2,085 normal +246 anomalous; test 894 normal +110 anomalous | Binary surface anomaly; no invented product/subtype labels |

Counts require the Stage 2 image/mask/group audit. D1 folders are bent, cut, hole
and thread; their initial directory counts are 21, 22, 22 and 22. A folder name
is reporting metadata, not a predicted defect subtype.

D1 source: [MVTec 3D-AD](https://www.mvtec.com/research-teaching/datasets/mvtec-3d-ad).
D2 source: [ViCoS KSDD2](https://www.vicos.si/resources/kolektorsdd2/).
Both specify CC BY-NC-SA 4.0. Retain attribution/licence/changes; no commercial
permission, supplier certification or factory reliability is established.

D1 archive SHA256:
`63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed`.
Its original download URL/date and provider release identity are unverified;
the included readme describes an early review subset. Reconcile the actual
source and notice before experiment freeze/publication. A local hash identifies
bytes and does not authenticate provider identity. See [source ledger](components/docs/DATA_SOURCES.md).

Use D1 RGB PNGs under train/good/rgb, validation/good/rgb and test/*/rgb;
pair test masks from test/*/gt by ID. Keep XYZ TIFFs/camera metadata inert.
This is RGB-only inspection, not an evaluated 3D model. Geometry-only defects
may be invisible in RGB. KSDD2 remains separate, not pooled training data.

## Project-local dataset locations

The dataset is installed locally. From the repository root:

```text
components/data/
  archives/
    cable_gland.tar.xz                # readable-name local archive copy
    63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed.tar
                                     # importer-owned identical archive bytes
    edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8.zip
                                     # KSDD2 archive
  raw/
    mvtec_3d_cable_gland/cable_gland/
      train/good/rgb/                 # D1 training RGB
      validation/good/rgb/            # D1 development-only RGB
      test/<good-or-defect>/rgb/       # D1 locked test RGB
      test/<good-or-defect>/gt/        # test masks
    ksdd2/                            # separate D2 images/masks
  manifests/
    mvtec_3d_cable_gland_source.json
    ksdd2_source.json
    <dataset>_<archive-hash>_inventory.json
```

Do not make a flat image folder or mix modalities/datasets. Source records and
hash inventories own acquisition identity; the recipe YAML selects RGB files.
The readable-name archive is an extra identical local copy, not a new release.
It adds 354,399,396 bytes to storage beyond the importer-owned archive and raw data.
The .tar suffix on the importer copy does not change its XZ-compressed bytes.
Keep all archives/raw data/manifests ignored in Git; tracked provenance summaries
live in components/docs. Preserve original Downloads and importer-owned copies.

Verify/reuse the installed D1 source from repository-root PowerShell:

```powershell
.\components\.venv-p0\Scripts\python.exe -m component_inspector.cli acquire --dataset mvtec_3d_ad --category cable_gland --archive 'C:\Users\laksh\OneDrive\Desktop\Tech4Bharat\components\data\archives\cable_gland.tar.xz'
```

This command checks the archive/inventory/raw hashes and membership on reuse;
it does not redownload, overwrite raw files, fit a model or run final evaluation.
On another computer, obtain the permitted archive and use its actual local path.
Acquisition is complete; the next implementation milestone is Stage 2 auditing,
RGB/mask pairing, duplicate groups and saved fit/development/calibration roles.

## 2. Exact experimental defaults

- Seed 4217. Form physical/duplicate groups before assigning roles; preserve
  official partition separately from experimental role. Unknown IDs stay unknown.
- Split eligible official-training normal groups 60% fit /20% development /
 20% calibration. Deterministic hashed ordering and rounding follow execution
  plan section 4. Independent-image arithmetic: D1 134/45/44; D2 1,251/417/417.
- D1's 23 official validation normals are development-only; if independent this
  gives 68 development normals. Never put them in fit/calibration/final test.
- KSDD2 training anomalies are development-only. D1 has no genuine development
  anomalies; no borrowing final-test defects to select preprocessing/models.
- Quarantine cross-partition contamination and corrupt/missing/mismatched records;
  disclose reasons, altered counts and comparability. Do not remove hard examples.
- Fit at most 128 normal groups per recipe; one canonical image per group.
  Baseline uses 16 deterministic references. No cross-recipe Gaussian/threshold.
- B0: minimum mean squared RGB residual over valid pixels, at most four reference
  comparisons per chunk, sigma-1 smoothing, mean of highest 1% valid pixels score.
  No exhaustive rotation search, registration or per-position tiled bank.
- P0: pinned, verified maintained PaDiM with frozen ResNet18 layer1/2/3 and 100
  channels; target versions and raw-score contract follow execution plan section 5.
  If its bounded compatibility/resource spike fails, only the named 50-channel
  native P1 fallback is allowed. Record backend/weight/channel identities.
- D1 RGB letterbox H256 W256, zero padding, no crop/rotation. D2 H256 W640 with
  one training-inventory-determined clockwise 90-degree orientation if portrait.
  Apply geometry consistently to masks; exclude padding and invert map coordinates.
- Batch 1, CPU, at most four Torch threads, no default augmentation. Fit RSS cap
  min(4 GiB, 60% available RAM at launch); inference RSS cap 4 GiB.
- Freeze both recipes, backend, roles, primary method and code/config identities
  before either final test. Calibration uses held-out normal scores only:
  k=ceil(0.90*(n+1)), one-based kth value, flag strictly greater; fail if k>n.
- Attention display range is calibration-derived and fixed; no probability,
  severity, defect-class or dimensional-tolerance claims. No binary IoU gate.
- Final per-recipe screens: recall >=90%, accepted-normal FPR <=10%, technical
  coverage >=90%, warm p95 <=5 seconds/image. Rejected defects count as misses.
  With unchanged D1 membership: >=79/87 detected and <=2/21 false flags.
  Report denominators/intervals; these are engineering screens, not assurance.
- Preserve the frozen evaluation. A failure produces a report, not repeated
  holdout-driven tuning or a fabricated successful demo.

## 3. Ordered stages, deliverables and checks

Each implementation stage uses meaningful failing tests first, minimal code,
relevant verification and saved evidence. Checkboxes remain pending until verified;
acquisition success does not imply audit, fitting or model readiness.

| Stage | Work and file responsibility | Required evidence / next gate |
|---|---|---|
| 0 | Inspect checkout, existing environment, doctor, ignores and current artifacts | Actual setup/test results; preserve existing environment/data |
| 1 / T01 | Bounded source import in data/acquire.py and source ledger | Archive/inventory hashes, notices, source identity uncertainty, traversal/expansion tests; current imports already completed |
| 2 / T02 | Data adapters, inventory/audit/split manifests, protocol validation | Correct RGB/mask pairing, normal/anomaly counts, official validation development-only, reproducible groups, overlap rejection and quarantine |
| 3 / T03 | Reference model, shared geometry and trusted artifact contracts | Real development predictions, edge-map coordinate checks, resource measurements, save/load parity; no test scoring |
| 4 / T04 | Verified PaDiM integration and bounded fallback | Normalization exactly once, frozen weights/features, same-backend raw parity atol=rtol=1e-5, peak fit/inference memory/time |
| 5 / T05 | Freeze, normal calibration, one final evaluation, failure report | Freeze/access/hash evidence, calibration edge tests, counts/intervals per method and recipe, eligible recipe decision |
| 6 / T06 | Native FastAPI service, SQLite and frontend foundation | Actual calibrated inference; invalid/oversize inputs, wrong artifacts, idempotency, concurrent busy and timeout/late-result tests; frontend build |
| 7 / T07 | One-image review controls and separate decision events | Real image -> native score -> user's actual decision -> saved/reloaded history; loading/error/keyboard checks |
| 8 / T08 | Batch/rework ledger and HTML/CSV export | Six-product fixture sequence, latest-attempt versus ever-reviewed counts, unresolved/draft state, stale acknowledgement, injection escaping |
| 9 / T09 | Frozen manual/assisted timed exercise and feedback draft | User participation, actual times/errors, interrupted/incomplete handling and honest limitations; no fabricated feedback/contact |
| 10 / T10 | Reproduction, backup/restore, missing-artifact handling and delivery package | Full relevant suite, typecheck/build, end-to-end smoke, separate clean/restore fixtures, truthful local-live/replay mode and handoff |

Detailed stage steps and commands: [execution plan sections 8-9](Tech4Bharat_Codex_Execution_Plan.md)
and [playbook](docs/superpowers/plans/2026-10-18-codex-build-playbook.md).
Paths in the table are under components/src/component_inspector except configs,
docs, tests, web and generated artifacts. Do not assume future commands exist.

- [ ] Complete Stage 2 audit and roles, with source uncertainty tracked.
- [ ] Demonstrate both baseline and PaDiM feasibility under resource caps.
- [ ] Reconcile source notice, freeze and evaluate once; issue go/conditional/no-go.
- [ ] Build the application only for eligible recipes. If neither passes, stop
  dependent app work and deliver the experiment/failure report.
- [ ] Obtain the real human review and exercise milestones; automated fixture
  decisions cannot satisfy personal participation or owner acknowledgement.
- [ ] Verify and prepare delivery; publication/push requires separate authorization.

## 4. Application and delivery boundaries

Local service binds 127.0.0.1:8766 with inference concurrency one; busy returns
503. A timeout/disconnect must not release the slot while native work continues.
JPEG/PNG only; actual decode checks, <=10 MiB encoded, <=20 MP decoded and
minimum side 128. Reject invalid/missing/uncalibrated/mismatched artifacts without
fake normal scores. Exact API schemas/status codes follow the execution plan.

Store generated upload names and data outside public assets. Keep immutable model
observations separate from append-only human decisions. Same key/payload retries
are idempotent; changed payload returns 409. Expected IDs count unique products,
not photographs. A new attempt reopens resolution; old acceptance cannot cover it.
Partial/unresolved exports remain drafts; acknowledgement applies to an exact
resolved snapshot and becomes stale when the snapshot changes. Escape HTML/CSV.

No public shared uploads before explicit security/storage/retention verification.
Investigate an actual zero-cost hosting route only against current requirements
and measured model size/RAM/startup/persistence. If unavailable, prepare an
explicit precomputed static replay plus local live demo. No claim of deployed
live inference from replay or local-only tests. Do not buy, publish or push during
preparation; do not contact manufacturers, accept personal terms or sign decisions.

## 5. Resume and completion

Use [STATUS.md](components/docs/STATUS.md) for current evidence, and
[REPRODUCE.md](components/docs/REPRODUCE.md) for implemented commands. Reuse
acquired sources and completed stages; no retraining/evaluation merely to resume.
Continue eligible work without routine stage approval; stop for genuine blockers
or personal milestones with the exact action needed. Usage/access constraints
can interrupt execution; save recoverable evidence rather than promise continuity.

Planning budget remains 42-70 hours including contingency, plus access/participant
waiting. It is unmeasured and must be re-estimated after model feasibility/results.
Completion means verified eligible deliverables and an honest outcome, including
no-go when appropriate. No production, generic-component, hidden-defect, factory
benefit or phone/browser parity claim is supported without separate evidence.

Earlier modelling proposals in this file are superseded by this revision. The
historical PCB experiment and dated technical review remain evidence, not current
implementation requirements or cable-gland performance measurements.
