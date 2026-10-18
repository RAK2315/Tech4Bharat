# Setup progress — 18 October 2026

Plan: [Tech4Bharat_Codex_Execution_Plan.md](../../Tech4Bharat_Codex_Execution_Plan.md).

## Current authorised work

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

## Remaining implementation

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
