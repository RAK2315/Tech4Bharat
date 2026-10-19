# Component Inspection Assistant — Copy-Paste Build Playbook

> **Current scope and continuation:** D1 is RGB-only MVTec 3D-AD cable gland;
> D2 remains KSDD2. Read [scope amendment](../../../components/docs/CABLE_GLAND_SCOPE.md)
> before any stage. Under standing sequential authorization, stage-boundary
> instructions to wait or paste another prompt do not require routine approval.
> Finish each stage and its checks, then continue if its prerequisites pass.
> Scientific failure gates, required human participation, personal access/terms,
> publication and push restrictions still apply. Recovery/publication prompts are
> conditional instructions, not additional stages to execute automatically.


> **For agentic workers:** use the installed `executing-plans` skill to implement one requested stage at a time. Do not delegate unless the human explicitly requests it. Follow the existing execution plan, write meaningful failing tests before new behaviour, and mark work complete only after running verification. This document supplies prompts; creating it does not start implementation.

**Goal:** build and evaluate a narrow component inspection assistant, then build a human-review application only if the experiment supports it.

**Architecture:** immutable dataset inventory → reference and PaDiM models → frozen calibration/evaluation → native local API → review and batch ledger → reports and tested delivery mode.

**Tech stack:** Python 3.12, CPU PyTorch, PaDiM/ResNet18, FastAPI, SQLite, React/TypeScript/Vite. No paid APIs or GPU requirement.

**Spec:** [current execution plan](../../../Tech4Bharat_Codex_Execution_Plan.md), especially sections 3–9. This playbook translates its T01–T10 tasks into user prompts and checks; it does not replace its numerical/model/data contracts. If they conflict, report the conflict before changing the experiment.

## 1. How you should use this file

- Open the existing `Tech4Bharat` folder in Codex. Keep the same project selected.
- Paste the starter prompt below, then paste **one numbered stage prompt at a time**.
- Wait for the stage report, perform its manual checks, then decide whether to paste the next prompt. Do not paste the entire document as one implementation request.
- You may use the same chat. In a new chat, paste the starter prompt again and name the next stage.
- Text blocks labelled **Copy into Codex** are prompts. PowerShell blocks are optional commands for you to run, not Codex prompts.
- Paths in commands assume your workspace is `C:\Users\laksh\OneDrive\Desktop\Tech4Bharat`. Change only that path if you move the project.
- The later commands and screens are **to be implemented**, not capabilities that already exist.
- Ask Codex to demonstrate evidence if a result is unclear. A screenshot or a green test summary alone cannot prove the experiment is valid.

### Current starting point, recorded 18 October 2026

- Local Git repository and private GitHub remote exist; initial commit is `d30447b`.
- `components/.venv-p0` uses Python 3.12.14; lightweight setup dependencies and the editable package exist.
- `doctor` and safe `acquire` are implemented; the latest component suite passed 58 tests before this documentation update.
- Cable-gland and KSDD2 acquisition completed. Audit/splits, models, evaluation, API and UI remain unimplemented. Metal-nut access is a historical deferred blocker; exact cable-gland download provenance remains pending.
- `experiment/` contains older PCB work. Do not treat it as results for cable glands or KSDD2.
- Existing setup must be inspected and reused rather than deleted/recreated.

## 2. Starter prompt — paste at the start of a build chat

**Copy into Codex:**

```text
Work in C:\Users\laksh\OneDrive\Desktop\Tech4Bharat.
Read applicable AGENTS.md instructions, Tech4Bharat_Codex_Execution_Plan.md,
Tech4Bharat_Anomaly_Detector_Build_Plan_Reviewed.md,
components/README.md, components/docs/STATUS.md, and
docs/superpowers/plans/2026-10-18-codex-build-playbook.md.

Use the installed executing-plans skill and relevant domain/testing skills.
Under standing sequential authorization, execute remaining eligible numbered stages
and their automatable checks without routine stage approval. Otherwise execute
only the stage requested. Do not restart completed work or
delegate to subagents. Inspect existing files and Git status before changing them.
Preserve experiment/, historical results and older plans. Keep changes within
components/ except supporting documentation and necessary repository ignores.

Use free local CPU compute and permitted free dependencies. Ask before paid usage.
Do not assume factory access, a GPU, phone testing or expert/manufacturer contacts.
Do not accept account terms, invent feedback, submit the hackathon entry or sign
batch records for me. Verify exact dependency APIs/compatibility when implementing.

For each new behaviour: write a meaningful failing test, confirm it fails for
the expected reason, implement, then run appropriate checks. Never substitute
mock predictions for model evidence. Label fixtures, transformed images and replay.
Implement planned commands before running them; unsupported commands must fail.

Keep fit, development, calibration and untouched test roles separate. Never tune
on final-test failures. Follow the fixed protocol and stop conditions in the spec.
Update components/docs/STATUS.md and REPRODUCE.md with commands, evidence paths,
failures and next stage. Commit only this stage's reviewed files after checks;
do not include datasets/weights/caches/uploads or other unrelated changes.
Do not push or deploy as part of a stage unless its prompt explicitly requests it.

At stage end report: what ran; test counts; actual outputs and limitations; files
changed; local commit; manual checks I should do; and whether the next gate passed.
If blocked, explain the exact blocker and complete independent work. Do not fake
completion or start a dependent stage. Under sequential authorization continue
when gates pass; otherwise wait for the next requested stage.
```

## Global constraints and fixed choices

- D1: **MVTec 3D-AD `cable_gland`, RGB only**. Expected folders bent/cut/hole/thread; verify labels and masks. No XYZ-based inference or 3D performance claim. See components/docs/CABLE_GLAND_SCOPE.md.
- D2: **KolektorSDD2**, a separate surface recipe with binary anomaly labels, not a second nut type.
- Never merge their fitting data, Gaussian statistics or thresholds. VisA PCB1 is historical, not training data for this build.
- B0: 16 deterministic normal RGB references; minimum mean RGB residual reference; sigma-1 smoothed map; highest-1%-pixel mean score.
- P0: frozen ResNet18 PaDiM, layer1/2/3, 100 channels, normal-only fit, at most 128 fit groups per recipe. This is fitting normal statistics, not supervised neural-network training.
- Target environment: Anomalib 2.7.0, torch 2.10.0, torchvision 0.25.0 CPU; these are proposed pins whose compatibility must be tested.
- P1 only if P0 fails its four-hour compatibility timebox: separate environment, native compact 50-channel PaDiM with torch 2.6.0+cpu / torchvision 0.21.0+cpu. Verify availability; no silent architecture search.
- Seed 4217; official-training normal groups 60% fit / 20% development / 20% calibration. D1 official validation RGB images are development-only. Preserve official partitions and test membership subject to disclosed contamination quarantine.
- Normal-only calibration: k = ceil(0.90 × (n+1)), one-based kth score, flag strictly greater than threshold. Fail if k > n.
- Default no augmentation. Separate brightness/blur stress tests happen after original evaluation; do not mix results.
- Provisional screens: recall ≥90%, accepted-normal FPR ≤10%, scoring coverage ≥90%, warm native p95 ≤5 s/image, inference RSS ≤4 GiB. Rejected defects count as misses. These are engineering targets, not industrial requirements.
- CPU batch 1, at most four Torch threads; fit RSS cap min(4 GiB, 60% of available RAM at launch).
- Images: JPEG/PNG only, no animated/multipage images, ≤10 MiB, ≤20 MP decoded, shortest side ≥128. Bad inputs produce errors, not normal results.
- Model output is an anomaly flag/attention map, not a defect subtype, probability, root cause, certification or approval.
- Local service defaults to 127.0.0.1:8766; preserve historical port 8765. SQLite and files remain outside public assets.

## Review focus — failures the checks must catch

1. Dataset leakage or final-test tuning: owned by stages 2 and 5; overlapping grouped fixtures must fail and frozen hashes must remain unchanged.
2. A plausible-looking but misaligned heatmap: owned by stages 3 and 4; non-square fixtures and save/load tests must verify coordinates and raw output parity.
3. Bad inputs or busy inference reported as normal: owned by stage 6; error/null-output and concurrency tests must prove the contract.
4. Duplicate/reworked products inflating coverage or retaining stale acceptance: owned by stage 8; the six-product sequence below must reconcile.
5. Public replay presented as live inference or local labels presented as real identities: owned by stages 7 and 10; inspect labels and disable unsupported uploads.

## 3. Stage 0 — verify the existing starting point

**Copy into Codex:**

```text
Execute stage 0 of the build playbook: verify existing setup only.
Inspect Git branch/remote/status, Python isolation, free RAM/disk, Node/npm,
components configuration and the actual CLI. Run doctor --json and the existing
components tests using components/.venv-p0/Scripts/python.exe.
Check ignored paths for environments, raw data, models and caches. Do not print
credentials. Do not rebuild the venv or install ML packages. Update setup status
only if needed; report any mismatch between this playbook and the filesystem.
Provide the next exact prompt to use, but do not execute stage 1.
```

**Manual checks:**

- [ ] Run the following from PowerShell. The interpreter should report Python 3.12, the diagnostic should describe the actual environment, and pytest must exit successfully. The initial setup had two tests; future additions can increase that count.

```powershell
Set-Location 'C:\Users\laksh\OneDrive\Desktop\Tech4Bharat'
.\components\.venv-p0\Scripts\python.exe --version
.\components\.venv-p0\Scripts\python.exe -m component_inspector.cli doctor --json
.\components\.venv-p0\Scripts\python.exe -m pytest components/tests -v
git status --short --branch
git remote -v
```

- [ ] Check GitHub still identifies the repository as private.
- [ ] Confirm Codex does not claim that models or datasets are ready from setup alone.

**Gate:** continue only if the scaffold works or Codex has repaired a concrete setup failure and rerun checks.

## 4. Stage 1 — obtain datasets safely (remaining T01)

**Files:** `data/acquire.py`, `tests/test_sources.py`, `docs/DATA_SOURCES.md`, CLI wiring. All implementation paths below are under `components/src/component_inspector/` unless otherwise stated.

**Copy into Codex:**

```text
Implement stage 1 / remaining T01: safe acquisition of MVTec 3D-AD cable_gland (RGB modelling) and
KolektorSDD2 from official sources. Reuse the existing scaffold.
Inspect current download access, release structure, attribution and licence terms.
Official starting pages: https://www.mvtec.com/research-teaching/datasets/mvtec-3d-ad
and https://www.vicos.si/resources/kolektorsdd2/ . Implement acquire with dataset,
category where applicable and --archive PATH for a legitimately obtained archive.
Record original URL, retrieval date, actual bytes, SHA256, terms and extraction
inventory. Download only needed material where the provider supports it.
Use temporary bounded extraction and reject traversal, symlink/hardlink escape,
unsafe absolute paths and excessive expansion/member counts. Test these with tiny
fictional archives before extracting real data; never change the old experiment.
Record required human access actions if blocked; do not bypass access or silently
substitute a mirror. Keep raw data immutable and excluded from Git. Inspect current
licence restrictions before demo redistribution; public access is not commercial
permission. Run tests/test_sources.py and existing tests. Do not fit models or
inspect final-test imagery for model design. Report measured download/disk totals.
```

**Manual checks:**

- [ ] Open `components/docs/DATA_SOURCES.md`; it should contain actual source URLs, dates, hashes, terms and successful/blocked status for each dataset.
- [ ] Compare one archive's SHA256 with the ledger using the exact archive path Codex supplies:

```powershell
Get-FileHash -Algorithm SHA256 'PASTE_THE_ACTUAL_ARCHIVE_PATH_HERE'
```

- [ ] Ask Codex to show the traversal/archive-bomb test names and their actual results. Do not create a malicious archive yourself.
- [ ] Run `git ls-files components/data components/models`; only intended placeholders/documentation should appear, not raw images or weights.

**Gate:** usable permitted data, or an explicit blocker. If one dataset is inaccessible, do not silently claim the two-dataset protocol is complete; resolve access or record a human-approved scope amendment before dependent work.

## 5. Stage 2 — audit data and lock image roles (T02)

D1 uses RGB-only cable gland. Keep official validation development-only, audit
RGB/mask ID pairing and exclude XYZ/camera metadata from model inputs. Preserve
source-notice uncertainty until reconciled before freeze. See the scope amendment.

**Files:** `contracts.py`, `data/{adapters,audit,split}.py`, `tests/test_splits.py`, manifests and audit reports.

**Copy into Codex:**

```text
Implement stage 2 / T02 using the acquired archives. Follow section 4 and the
contracts in section 7 of the execution plan. Preserve official split and separate
experimental role. Verify image/mask pairing, actual taxonomy and dimensions.
Quarantine corrupt/missing/mismatched records with reasons; never turn a defective
image without a mask into a normal sample. Audit byte/decoded hashes and near-
duplicate candidates before deterministic group allocation. Record physical-item
identity uncertainty rather than claiming hashing proves physical independence.
Split normal training groups 60/20/20 using seed 4217. Select at most 128 normal
fit groups and 16 baseline references, with exact used/unused IDs. KSDD2 training
anomalies are development only. Preserve official tests for stage 5 and disclose
quarantined cross-split duplicates. Implement prepare and access controls so fit
and develop cannot consume calibration/test records. Write deliberate leakage,
missing-mask and determinism tests, run them and existing tests. Save machine-
readable manifests plus a short readable audit summary. Show training/development
samples only; do not expose test galleries yet. Stop before model implementation.
```

**Manual checks:**

- [ ] Open the readable audit: actual image counts, normal/anomalous counts, role counts, quarantine counts and unknown physical IDs must be visible.
- [ ] Run `prepare --config configs/protocol.yaml` twice using the exact working-directory command Codex supplies. Membership hashes should match; timestamps may differ.
- [ ] Ask Codex to demonstrate, with a fictional fixture, that putting one group in fit and calibration is rejected.
- [ ] View a few **development** image/mask pairs. Check labels and boundaries plausibly match. This is a spot-check, not an independent annotation audit.
- [ ] There must be separate D1 and D2 manifests, with no test IDs selected as references.

**Gate:** audited reproducible roles and demonstrated overlap rejection. Unknown physical IDs remain a disclosed limitation.

## 6. Stage 3 — implement the reference baseline (T03)

**Files:** `vision/{geometry,reference}.py`, `tests/{test_geometry,test_reference}.py`.

**Copy into Codex:**

```text
Implement stage 3 / T03: shared geometry and real B0 reference inference only.
Follow section 5 exactly: RGB float32 [0,1], aspect-preserving letterbox, valid ROI,
D1 H256 W256; D2 H256 W640 with training-inventory-determined fixed orientation.
Use bilinear images and nearest-neighbour masks, inverse-map to original shape.
Choose 16 deterministic fit references, compare at most four at once, select the
minimum mean squared RGB residual reference, smooth sigma 1 and score the highest
1% valid pixels. Preserve colour; no brightness centring, registration or rotation
bank. Inference functions must not accept labels/masks. Implement fit/develop CLI
contracts for method reference. Run actual inference on development images only,
separately per dataset. Test known non-square coordinate markers, mask mapping,
padding exclusion, deterministic references, finite scores and chunk equivalence.
Save development maps/raw scores, actual timing and memory. Uncalibrated flags must
remain null. Do not claim defect recall or inspect final tests. Stop before PaDiM.
```

**Manual checks:**

- [ ] Open a development original and its restored map: dimensions and orientation should match; the nut should not be cropped away.
- [ ] Ask Codex to show the known-marker geometry fixture before/after restoration; a marked corner must return to the same corner.
- [ ] Repeat inference on the same development image; results should be repeatable within the documented tolerance.
- [ ] Confirm there is no pass/fail threshold or claimed measured defect recall yet.

**Gate:** working native baseline for each recipe, correct mapping and bounded resource evidence. An attractive overlay alone is not a pass.

## 7. Stage 4 — implement and test native PaDiM (T04)

**Files:** `vision/{padim_adapter,artifact_store}.py`, `tests/test_padim.py`, selected environment lock and resource report.

**Copy into Codex:**

```text
Implement stage 4 / T04: actual CPU PaDiM, not a mock or a YOLO substitution.
Inspect current primary sources and exact pinned package implementation before
installing. Attempt P0 in .venv-p0: Anomalib 2.7.0, CPU torch 2.10.0/torchvision
0.25.0, frozen ResNet18 layer1/2/3 and 100 retained channels. Record exact weight
source/hash and normalisation once. Use the low-level adapter, not library Engine
defaults that could validate or choose thresholds on official tests.
Follow the four-hour P0 compatibility timebox and one separate P1 fallback in the
execution plan. Log failed commands and the selected backend. Do not compile torch,
install CUDA/[full], alter experiment/.venv or switch algorithms silently.
Fit D1 first, then a separate D2 model on selected normal fit images only. Measure
actual fit/init/inference resources, enforce min(4 GiB,60% launch available RAM)
fit RSS, batch 1 and at most four threads. Score max raw map over valid ROI and
restore maps to original coordinates. Test frozen parameters, normalisation,
stored channel selection, recipe mismatch and trusted save/load raw output parity
at atol=rtol=1e-5 on the same backend. Select one backend for both recipes before
freeze; rerun both development fits if fallback changes it. Lock actual resolved
dependencies and implement native padim fit/develop commands. Use development data
only. Report model bytes, timings, RSS, numerical failures and passing/failing tests.
If both implementations fail, stop with a feasibility report; do not build the app.
```

**Manual checks:**

- [ ] Ask Codex to show one model's fit manifest, weight hash, saved model size and measured resource log. It must be fitted from normal data, with separate artifacts per recipe.
- [ ] Run the same development image, restart the process and run it again with the saved artifact. Compare raw scores using the parity evidence, not rounded UI numbers.
- [ ] Ask Codex to demonstrate a wrong-recipe artifact being rejected with a fixture.
- [ ] Watch Task Manager during a development run to spot gross memory issues. Task Manager is only a rough check; retain measured process RSS logs.
- [ ] Confirm all predictions came from actual inference and no final test results were used.

**Gate:** repeatable native model within caps. These checks prove software feasibility, not inspection accuracy.

## 8. Stage 5 — freeze, calibrate and evaluate once (T05)

**Files:** `evaluation/{calibrate,metrics,runner,reports,stress}.py`, metric/calibration tests, immutable run outputs.

**Copy into Codex:**

```text
Implement and execute stage 5 / T05 only after native feasibility passed.
First test metrics/calibration on fictional hand-computable values, including
ties, null denominators and too-few calibration normals. Then freeze both recipes,
backend, primary method, preprocessing, roles, dependencies and code/artifact
hashes before any final-test scoring. Implement freeze/calibrate/evaluate/stress/
report CLI commands and reject unfrozen or mismatched bundles.
Calibrate B0 and primary separately for each recipe on its normal calibration
records only. Use k=ceil(.90*(n+1)), kth score, strict score>threshold; k>n fails.
Freeze display scaling from calibration, not test images. Do not use adaptive F1
callbacks or inspect test results to change preprocessing/model selection.
Evaluate the untouched official D1 and D2 test memberships with the already-frozen
protocol. Report each method/recipe separately: TP FN FP TN, technical rejections,
defect misses including rejected defects, recall, accepted-normal FPR plus false
flags/all normals, observed-prevalence precision, coverage, ranking/pixel metrics
where meaningful, intervals, actual cold/warm p95 latency, fit/init/inference RSS
and model bytes. Keep technical rejection/abstention distinct from blur/exposure
warnings; do not imply warnings are a validated retake rule. Human review time is
still unmeasured. Handle missing metrics honestly, not as zero or 100%.
Only afterward run paired brightness x0.6/x1.4 and blur-radius-2 stress copies,
unchanged thresholds and separate tables. Produce a failure gallery with misses,
false alarms, a correct flag and a normal item; say explicitly if a category has
no example. Label maps anomaly intensity, not probability/severity.
Apply the provisional per-recipe screens from the spec. If both recipes fail,
stop application work and deliver the failure report. If only baseline passes,
disclose post-test selection and require a scope decision before a baseline demo.
Do not tune and rerun the same holdout until it passes. Report which exact recipe
and method, if any, can proceed. No factory-readiness claim.
```

**Manual checks:**

- [ ] Before the real evaluation, ask for the fictional metric check: TP=9, FN=1, FP=2, TN=18, no rejections → recall 90%, FPR 10%, precision 9/11 ≈81.82%, coverage 100%.
- [ ] Calibration check: normals 1…19 give k=18 and threshold 18. A score of 18 is not flagged; 19 is flagged. Eight calibration scores must fail because k=9 exceeds n=8.
- [ ] Read counts as well as percentages. For unchanged imported D1 membership of 87 anomalies/21 normals, 90% recall requires ≥79 detected anomalies and ≤10% FPR allows ≤2 normal false flags. Audited counts may differ and must be disclosed.
- [ ] Verify the run has freeze/calibration hashes recorded before final predictions. Ask for the access log and relevant tests; timestamps alone do not prove absence of leakage.
- [ ] Now view the failure gallery. Ask why each error is possible, but **do not ask to tune this frozen experiment against those examples**.
- [ ] Verify stress-test results are separate and no inspection-time saving is claimed.

**Gate:** use the reported go/conditional/no-go decision. A failed model is a valid experiment outcome, not permission to fabricate a successful demo.

## 9. Stage 6 — local inference service (T06, only after stage 5 gate)

**Files:** `application/{api,store}.py`, `tests/test_api.py`, frontend package/lock.

**Copy into Codex:**

```text
Implement stage 6 / T06 for only the method/recipes eligible after stage 5.
Build the local FastAPI/Pydantic service, SQLite store and minimal React/TypeScript/
Vite foundation using verified locked dependencies. Implement the execution plan's
section 9 API schemas. Default 127.0.0.1:8766. Registry exposes calibrated eligible
bundles only; reject unknown/mismatched/missing artifacts. Bound encoded/decoded
image sizes, validate actual decoding, strip metadata from display copies, use
generated file names and keep original uploads/weights outside public assets.
POST /api/inspect performs real native inference with concurrency one; busy returns
503. Client disconnect/timeout must not release the inference slot while native
work is still running. Same idempotency key/payload returns the same inspection;
changed payload returns 409. Failures have null score/flag, never fake normal.
Test corrupt/oversize/unsupported images, recipe/hash mismatch, duplicates, busy
requests and late results. Record API latency separately from model timing.
Implement serve, run API tests plus existing tests and frontend typecheck/build.
Provide exact startup/shutdown commands and local API docs URL. No public hosting.
```

**Manual checks:**

- [ ] Start the service using Codex's exact command. Open `http://127.0.0.1:8766/docs`.
- [ ] Run a valid development image through the API; compare its score/model ID with native CLI output using the same artifact.
- [ ] Try a text file renamed `.png`, a GIF and a file above the encoded limit. Expect clear rejection (422 decode, 415 format, 413 size as applicable), never a normal score.
- [ ] Use the provided two-request harness; one request should receive 503 **when the calls actually overlap**. Fast sequential calls need not produce 503.
- [ ] Use the fixture harness for same-key retry and changed payload: same result/no new record, then 409.
- [ ] Missing/wrong model must block inference. Have Codex demonstrate with an isolated registry fixture; do not delete the real artifact.

**Gate:** actual model-backed API with tested failure handling. A successful HTTP response alone is insufficient.

## 10. Stage 7 — first real human review (T07)

**Files:** `web/src/{App,Review}.tsx`, ledger decision persistence and tests.

**Copy into Codex:**

```text
Implement stage 7 / T07: one real end-to-end inspection and human decision.
Use the existing API and a development image. Build accessible upload/recipe/
product-ID controls, original image, toggleable aligned attention overlay, raw
score/threshold/model identity, warnings and explicit error/uncalibrated states.
Use 'not flagged', not 'AI approved'; intensity is not probability/severity.
Offer acceptable/defective/uncertain/rework and an optional note. Model results
remain immutable; decisions append separate events. UI must not convert a model
flag into an automatic human disposition. Local reviewer labels are demo identities.
Test loading/error/retry states, keyboard access and saved/reloaded decisions.
Run API/ledger tests, frontend typecheck/build and relevant automated UI checks.
Start the working local app and give me the exact URL and development image path.
Then wait for me to actually review and choose a decision; never click or invent
my decision. Mark that human milestone pending until I do it. No batch polish yet.
```

**Manual checks (your participation is required):**

- [ ] Upload the named development image and confirm both original and model result appear.
- [ ] Toggle the overlay; inspect orientation and position. The original must remain accessible.
- [ ] Choose your own decision and note. Refresh and restart the app; the decision should persist.
- [ ] Changing your decision should append history, not silently overwrite the model observation.
- [ ] Navigate with Tab/Enter; controls must have visible focus and usable labels.
- [ ] An error must not leave a previous item's score visible as the new item's result.

**Gate:** actual image → native prediction → your decision → saved/reloaded record. Automated fictional decisions do not satisfy the participant milestone.

## 11. Stage 8 — batches, rework and reports (T08)

**Files:** `application/{ledger,export}.py`, `web/src/{Batch,Report}.tsx`, ledger/export/API tests.

**Copy into Codex:**

```text
Implement stage 8 / T08: truthful batch accounting and HTML/CSV export.
Follow section 9 endpoints and T08 definitions. Expected IDs are unique products,
not photos. Count current_scored/current_reviewed from each product's latest
attempt, and ever_scored/ever_reviewed separately. Display uninspected, unresolved,
acceptable, defective, uncertain and rework clearly without overlapping totals.
A new rework attempt reopens resolution; old acceptance cannot cover it. Record
same-key retries idempotently, block cross-product reuse of the same image, and
invalidate an acknowledgement when its underlying snapshot changes. Cap expected
IDs at 1000 and reject duplicates. Do not treat an acknowledged defective item as
shipping acceptance. Only resolved latest decisions can support final owner
acknowledgement; uncertain/rework remain unresolved. Partial exports stay drafts.
Test the exact six-product fictional sequence in this playbook. Generate reports
from a transaction-consistent snapshot with coverage, observations, model/calibration
identity, human decisions, attribution and limitations. Escape HTML and spreadsheet
formula injection. Keep fixture decisions explicitly fictional and benchmark images
distinct from real factory records. Prepare a sample report, not an invented signed
factory batch. Run tests, typecheck/build and reconcile API/UI/export counts.
```

### Manual six-product sequence — use a separate FICTIONAL batch

Ask Codex for distinct permitted development images and a resettable fixture workspace. This sequence checks software only. Do not use it as evidence of inspection accuracy.

| Action | Expected current scored | Expected current reviewed | Expected uninspected | Expected resolved |
|---|---:|---:|---:|---:|
| Create P001…P006, no uploads | 0 | 0 | 6 | 0 |
| Inspect P001, human acceptable | 1 | 1 | 5 | 1 |
| Retry identical P001 request/key | 1 | 1 | 5 | 1 |
| Attempt same image under P002: reject reuse | 1 | 1 | 5 | 1 |
| P002 distinct image, human defective | 2 | 2 | 4 | 2 |
| P003 distinct image, human rework | 3 | 3 | 3 | 2 |
| P003 new capture/attempt, no decision yet | 3 | 2 | 3 | 2 |
| P003 latest attempt, human uncertain | 3 | 3 | 3 | 2 |
| P003 latest attempt, human acceptable | 3 | 3 | 3 | 3 |

- [ ] P003's old rework/uncertain decisions remain in history. New attempts do not create a seventh product.
- [ ] At the new P003 attempt, `ever_reviewed` stays 3 even though `current_reviewed` drops to 2.
- [ ] Export now: report is draft, 3/6 scored and 3/6 reviewed; P004–P006 remain uninspected.
- [ ] Attempt final acknowledgement now: blocked because three expected products are unresolved/uninspected.
- [ ] Resolve P004–P006 using distinct images and your own fixture decisions. If a latest decision is uncertain/rework, acknowledgement remains blocked.
- [ ] Only if you choose, acknowledge this explicitly fictional resolved snapshot yourself. It must not be labelled a shipment certificate or verified identity.
- [ ] Add a new P001 attempt: prior acknowledgement becomes stale, current reviewed falls to 5, current scored remains 6 and unresolved becomes 1. Fresh export is draft until re-resolved/re-acknowledged.
- [ ] Put `<script>alert(1)</script>` in a fictional note: it displays as text and executes nothing. Put `=1+1` in a note and inspect the CSV as text: the export must neutralise formula execution. Ask for automated coverage of other formula prefixes too.
- [ ] UI, API and report must agree for the same snapshot. Later events must not silently rewrite an already exported snapshot.

**Gate:** reproducible counts, intact history and honest report status. Do not use batch size as the denominator for model accuracy without known labels.

## 12. Stage 9 — timed review exercise and feedback draft (T09)

**Files:** `outputs/human_exercise/`, analysis and feedback documents.

**Copy into Codex:**

```text
Prepare stage 9 / T09 using a frozen eligible method and explicitly benchmark images.
Create 24 distinct items: 12 manual, 12 assisted, balanced normal/anomalous per arm;
stratify verified defect type/size where feasible. No repeated image or known group
across arms. Record whether these are already-used benchmark test items; do not
present this as a new untouched model validation. Randomise arm order with a saved
seed, freeze assignment/analysis before my responses and hide answer keys until
completion. Show no correctness feedback mid-exercise. Record actual per-item and
total time, decision, uncertainty, hints used, pauses/abandonment and missing data.
Test the recorder and incomplete-session handling using fictional records, then
give me the exercise URL and plain instructions. Do not complete it for me.
After I participate, analyse errors and times jointly, disclose one-person/order/
matching/synthetic-prevalence limitations and exclude unmeasured capture time.
No factory inspection-time saving claim. If I have not participated, mark results
pending. Draft manufacturer/buyer feedback questions on usefulness, extra workload,
existing alternatives and required evidence. Do not contact anyone or invent answers.
```

**Manual checks:**

- [ ] Use an isolated fixture rehearsal first to verify timer persistence and interruption handling; do not preview actual exercise images or answers.
- [ ] Complete the real exercise once, without opening the answer key or receiving correctness hints.
- [ ] Record interruptions honestly; missing/abandoned trials must not silently become fast correct responses.
- [ ] Compare exported timestamps and decisions to your experience. Both correctness counts and timing should be reported, not speed alone.
- [ ] Read the feedback draft: ask what users do today, what this adds, what they distrust and what would make them reject it. No fabricated testimonials.

**Gate:** actual pilot findings or clearly pending exercise. A one-person benchmark pilot cannot validate factory effectiveness.

## 13. Stage 10 — package, verify delivery and prepare handoff (T10)

**Files:** startup scripts, `docs/{REPRODUCE,MODEL_CARDS,DEPLOYMENT}.md`, demo outputs and final README updates.

**Copy into Codex:**

```text
Execute stage 10 / T10: package and verify the smallest supported application.
Provide tested PowerShell startup/shutdown and clean-environment reproduction
instructions, selected dependency locks, model/data provenance, resource needs,
known failures and measured scope. Do not overwrite my environment to test a clean
setup; use a separate permitted temporary environment. Test missing artifacts,
restart persistence, report download and expected errors. Document database backup/
restore and create a fixture-only reset, never deleting my real records by default.
Run the full relevant Python suite, frontend typecheck/build and one automated
end-to-end upload→inference→decision→report smoke test. Distinguish mock UI fixtures
from real inference checks. Reconcile all status documents with actual results.

Investigate a concrete zero-cost public live option against current primary docs
and actual model RAM/size/startup/latency/persistence requirements. Do not purchase
anything or assume free credits. Before enabling shared public uploads, define and
test authentication/authorisation, upload limits, rate limiting, retention and
storage isolation. Do not expose the localhost demo to the internet as-is.
If safe free live hosting is unavailable, package a static replay with precomputed
benchmark observations, declared fictional IDs, no arbitrary live-upload claims
and explicit non-shared/non-durable browser-local decisions. Keep local live startup.
Check licence/attribution and exact publication contents; keep raw data, private
records, credentials and model files out of frontend assets unless redistribution
is explicitly justified. Present the prepared delivery mode, files and deployment
command for review. Do not publish or push during this preparation stage.
Provide a final go/conditional/no-go, remaining human actions and a short demo script.
```

**Manual checks:**

- [ ] Follow the startup instructions yourself after closing the prior app. They must work without Codex making hidden repairs.
- [ ] Upload a permitted development image, wait for actual inference, decide, refresh, restart and export. The saved record must survive.
- [ ] Restore a backup into a **separate fixture workspace** and compare counts. Never test restore over your only copy.
- [ ] A missing artifact produces a clear error; no successful fake prediction is substituted.
- [ ] Open any proposed replay: it must say replay/precomputed, reject unsupported live uploads, and disclose browser-local storage limitations.
- [ ] Confirm exact hosted content and licence notes before requesting publication. Private GitHub does not make a deployed website private.
- [ ] For a genuinely hosted live route, test cold start, repeated requests, restart persistence and unauthorised access; local test success does not prove hosting success.

### Optional publication prompt — only after reviewing the prepared package

```text
Publish only the reviewed delivery mode and files recorded in
components/docs/DEPLOYMENT.md, using its verified zero-cost configuration.
If the mode, visibility, included data, account terms or costs differ, stop and
explain before proceeding. I will complete account/terms prompts myself.
Do not expose private records or enable unreviewed shared uploads. Verify the
deployed URL in a fresh browser session, confirm its live/replay label and run the
applicable smoke checks. Report actual hosting limits and deployment evidence.
```

### Optional GitHub sync prompt — local commits do not automatically push

```text
Inspect the current changes and origin. Confirm the destination is the existing
private Tech4Bharat repository and no raw data, model weights, uploads, secrets or
caches are tracked. Run the relevant verification for unverified changes, commit
only the intended source/documentation and push the current reviewed branch.
Verify the remote commit matches and report remaining uncommitted files.
Do not change repository visibility or force-push.
```

## 14. Common recovery prompts

**When a command or test fails:**

```text
Use systematic-debugging to investigate this exact failure: [paste error and
command, with secrets removed]. Reproduce it, identify the cause, add a meaningful
regression test where appropriate, make the smallest correction and rerun checks.
Do not delete data/environments, disable the failing test, weaken a gate or change
the experiment to hide the problem. Explain whether any frozen result is invalid.
```

**When returning after a break:**

```text
Read the starter instructions in the build playbook and components/docs/STATUS.md.
Inspect actual files, Git changes and saved evidence. Reconcile status with reality;
do not rerun final evaluation or retrain merely to resume. Tell me the last verified
stage and blockers. Execute stage [NUMBER] only if its prerequisites are met.
```

**When accuracy fails:**

```text
Do not tune against this test set. Preserve the frozen run and report errors/counts,
limits and the cheapest new independent experiment. Distinguish a correctness bug
from a modelling failure. If correcting a bug affects evaluation, invalidate and
label affected results. Do not call a reused holdout untouched or build an inspector
claim the evidence does not support.
```

## 15. What you do versus what Codex does

| Work | Codex | You |
|---|---|---|
| Dependencies, code, tests, data auditing, native runs | Implement, execute and record evidence | Spot-check using this guide |
| Required account/access/terms action | Explain exact blocker and prepare permitted steps | Complete personal prompts |
| Model correctness and evaluation | Test/report, including failures | Inspect evidence; do not tune holdout examples |
| Human inspection decisions | Provide UI and preserve history | Make the actual decisions |
| Timed pilot | Prepare, record, analyse | Participate honestly |
| Owner acknowledgement | Prepare snapshot, enforce state rules | Personally acknowledge if appropriate |
| Manufacturer feedback | Draft exercise | Obtain voluntary feedback later if possible |
| Publication/submission | Prepare and verify authorised output | Review mode/content and handle personal submission |

## 16. Final acceptance checklist

- [ ] Datasets and models have provenance; no cross-role/group leakage silently ignored.
- [ ] Both methods have measured results per dataset, including failures and counts.
- [ ] Final thresholds and code/config identities were frozen before evaluation.
- [ ] Actual native inference works with trusted saved artifacts and correct geometry.
- [ ] The exposed recipe/method matches the evidence gate; unsupported recipes are hidden or explicitly research-only.
- [ ] Your actual review persists; duplicates/rework/coverage/report counts reconcile.
- [ ] Draft/acknowledged and fictional/real distinctions are visible.
- [ ] Human timing is measured or clearly unmeasured; no invented contacts/feedback.
- [ ] Delivery is truthfully labelled local live, hosted live or static replay.
- [ ] Reproduction commands, limits, tests and failure examples are documented.

**Planning estimate:** the existing execution plan allocates 42–70 hours including contingency, plus participant/access delays. This is an unmeasured planning budget, not a promise. Re-estimate after stages 4–5; do not spend the app budget if the experiment fails.

**Skills used to prepare this document:** `writing-plans` for staged instructions and verification; `brainstorming` for checking scope against the already-established design. No product code, model fitting, acquisition or deployment is performed by this document.
