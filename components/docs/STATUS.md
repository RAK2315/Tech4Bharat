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
