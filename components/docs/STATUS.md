# Setup progress — 18 October 2026

Plan: [Tech4Bharat_Codex_Execution_Plan.md](../../Tech4Bharat_Codex_Execution_Plan.md).

## Initial authorised work (historical)

User requested the virtual environment, initial files and folders only.
This is the setup portion of T01, not authorisation to run the entire plan.

## Rulings

- No Git repository exists in this workspace. Use the separate `components/`
  directory; do not initialise a repository, create a worktree or make commits.
- Reuse the available bundled Python 3.12.14 interpreter through a new environment;
  the system default is Python 3.13 and does not match this plan.
- Use project-local `.cache/uv` because the sandbox's default uv cache is unwritable.
- Install only lightweight setup/dev dependencies now. ML packages, frontend
  dependencies, datasets, models and training remain deferred.
- Preserve the old `experiment/` environment/results and all plan documents.

## Verification

- Created `components/.venv-p0` with Python **3.12.14**, system packages disabled.
- Resolved eight lightweight setup/dev packages into `requirements-setup.lock`
  with distribution hashes; installed the project editable into this environment.
- Installed PyYAML 6.0.3, psutil 7.2.2 and pytest 9.1.1 plus their locked dependencies.
- Wrote diagnostic command tests first: two failed before `cli.py` existed;
  after implementation, `python -m pytest tests -v` passed **2/2**.
- `python -m component_inspector.cli doctor --json` confirms isolated supported
  Python, readable draft configurations, and no installed torch/torchvision/anomalib.
- Dataset acquisition and model readiness remain false; only `doctor` is implemented.
- Dependency setup required escalation because the sandbox blocked uv cache/path
  access. The reviewed escalation succeeded; no action remains blocked.
- All of T01 is **not** complete: acquisition and its safety tests remain future work.

Runtime snapshot: [SETUP_ENVIRONMENT.json](SETUP_ENVIRONMENT.json).

## Subsequent authorisation: local Git repository

The user subsequently requested Git setup for the project. This supersedes the
earlier no-initialisation ruling above: initialise the workspace repository and
commit the existing research and scaffold, excluding local dependencies, datasets,
weights and generated binary artifacts. No remote publication was requested.

## Remaining implementation after initial setup (historical)

Official archive access/licence/source ledger, safe acquisition and extraction tests,
and actual dataset acquisition remain unimplemented. Follow with T02 split auditing
before any model fitting. No performance or readiness result is implied by setup.

## Stage 0 verification — 18 October 2026

- Gate passed for the existing scaffold only. Stage 1 was not executed.
- Branch `main` tracks `origin/main`; HEAD before this verification was `d30447b`.
  Origin is `https://github.com/la-kshita/Tech4Bharat.git`. Remote visibility and
  remote freshness were not checked online; confirm private visibility manually.
- Existing user changes (`README.md` modified and root `docs/` untracked) were
  preserved. No applicable AGENTS.md was found in the workspace or its ancestors.
- Doctor exited 0: Python 3.12.14, isolated/supported, system packages disabled;
  16 logical CPUs, 7,734,337,536 bytes available RAM (~7.20 GiB) and
  659,205,365,760 bytes free disk (~613.93 GiB) at the saved snapshot.
- Node v24.21.0 and npm 11.19.0 are available. Frontend dependencies/build and
  future ML compatibility were not tested. No environment/package changes made.
- Doctor is the only implemented CLI command. All four YAML configurations load;
  backend pins are proposed, protocol is draft, recipe validation is pending.
  Raw archive/data/model directories contain placeholders only; readiness is false.
- Existing tests passed 2/2, including rejection of unsupported `fit` (exit 2).
  The first run emitted a pytest cache permission warning. A second run with
  `-p no:cacheprovider` passed 2/2 without warnings; cache permissions were not changed.
- Optional dependency consistency checks were unavailable: `python -m pip check`
  failed because this uv-created environment has no pip; `uv pip check` failed
  while opening the default cache (os error 183). No dependency consistency pass
  is claimed. These do not prevent the verified doctor/tests from running.
- `git check-ignore -v` confirmed exclusions for environments, raw data, archives,
  models, project/root caches and frontend node_modules. Tracked data/models are
  `.gitkeep` files only.
- Filesystem agrees with the playbook's scaffold scope. The earlier no-Git ruling
  above is historical and superseded; REPRODUCE.md was absent and is now supplied.
- Evidence: [STAGE0_DOCTOR.json](STAGE0_DOCTOR.json),
  [STAGE0_TESTS.txt](STAGE0_TESTS.txt), and commands in [REPRODUCE.md](REPRODUCE.md).
- Next authorised prompt: stage 1 / remaining T01 in the build playbook. Dataset
  source/terms inspection, safe acquisition and tests remain future work.


## Stage 1 / remaining T01 — 18 October 2026

Current authorisation is safe acquisition only. Software is verified; the complete
stage/data gate is **blocked**, because MVTec requires the user's personal form
step. Stage 2 and all model/application stages were not started.

- Working branch: `stage-1-safe-acquisition`, based on stage 0 commit `b36d144`.
  User's modified root README and untracked root docs remain separate.
- Added real `acquire` CLI and local `--archive` import; source registry permits
  only MVTec metal_nut and KSDD2. Blocked access exits 3, failures exit 1, unsupported
  commands exit 2. `doctor` lists acquire but its readiness flags remain scaffold
  defaults, not a dataset-ledger audit.
- Download/extraction use fixed byte/member/expansion bounds, safe portable names,
  regular files only, temporary extraction, one training-only PNG decode, SHA256
  archives/inventories, and no-overwrite/idempotent verification. No downloaded
  script or pickle is executed. No final-test image was viewed/decoded for design.
- MVTec CLI ran and recorded `blocked_access`; zero bytes downloaded. Required
  action: personally use the official form and obtain the metal_nut archive if
  terms are acceptable, then provide its local path. No terms were accepted.
- KSDD2: 853,126,555 downloaded bytes; 852,612,567 extracted bytes in 6,677 files;
  archive + raw logical total 1,705,739,122 bytes (~1.589 GiB). One training image
  decoded at 229×645. Source/inventory/byte hashes and notices are in DATA_SOURCES.md
  and STAGE1_SOURCES.json. Reuse verified all saved hashes and file membership.
- Release layout includes train/test PNGs and five inert .pyb files. Training-file
  count needs reconciliation against provider image counts in stage 2; no label,
  mask-pairing, physical identity or split audit is claimed here.
- Pillow 12.1.0 installed into the reused venv; verified wheel/import/decode on
  Python 3.12.14, updated hashed lightweight lock and editable metadata. No ML
  packages, GPU, paid service or historical environment changes.
- Sandbox blocked initial network attempts; approved escalation enabled Pillow
  install and KSDD2 acquisition. Download-created data also required approved
  access for reuse verification; no ACL changes made. uv discovery initially
  failed in the sandbox, then succeeded with explicit Python and approved access.
- TDD: initial 40 acquisition cases failed for the absent module/CLI. New TAR/ZIP
  metadata, raw-extra-file, XZ and TAR-small-file regressions were each observed
  failing before fixes. Existing-behaviour checks cover CRC cleanup, retries,
  blocked CLI status and original doctor/unsupported-fit contract.
- Final suite: **53 passed** (51 source cases + 2 existing doctor cases).
  Commands/results and self-review are recorded in STAGE1_EVIDENCE.md;
  full test output is STAGE1_TESTS.txt. RED logs remain ignored under
  outputs/stage1/. No new model evidence is claimed by fictional archives.
- `uv --cache-dir components/.cache/uv pip check --python
  components/.venv-p0/Scripts/python.exe` passed (10 installed packages checked).
- Next: resume stage 1 with a legitimately obtained MVTec archive. Do not start
  dependent stage 2 without both sources or an explicit human scope amendment.

Rulings: work in the user-requested checkout with a dedicated local branch and
self-review (no subagents, per user instruction); preserve unrelated working-tree
changes. Cost/limit: no independent reviewer and no separate worktree isolation.
MVTec's personal access flow is a real blocker, not a reason to substitute a mirror.
The earlier source/scaffold statements above are dated historical verification.
