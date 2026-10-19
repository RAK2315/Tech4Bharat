# Current cable-gland / KSDD2 reproduction commands

Run from the repository root. Reuse the existing Python 3.12 environment.
The following imports/verifies real sources; it does not fit a model:

```powershell
.\components\.venv-p0\Scripts\python.exe -m component_inspector.cli acquire --dataset mvtec_3d_ad --category cable_gland --archive 'C:\Users\laksh\OneDrive\Desktop\Tech4Bharat\components\data\archives\cable_gland.tar.xz'
.\components\.venv-p0\Scripts\python.exe -m component_inspector.cli acquire --dataset ksdd2
.\components\.venv-p0\Scripts\python.exe -m component_inspector.cli doctor --json
.\components\.venv-p0\Scripts\python.exe -m pytest components/tests -q --basetemp=components/.cache/scope-check-20261018
```

Use a fresh workspace-local --basetemp directory for a later test run. Pytest
clears an existing explicit basetemp; never point it at real data or records.
Cable-gland source identity is separate from mvtec_ad/metal_nut. The latter
remains supported for historical compatibility but is not an active recipe.
Both current imports must return acquired (exit 0); missing MVTec local archives
return blocked_access (exit 3). General failures return exit 1.
See [current scope](CABLE_GLAND_SCOPE.md) for validation roles, RGB-only paths,
archive notice uncertainty and the planned next data audit. No fit/calibrate/
evaluate/serve implementation is claimed. Sections below are dated historical
evidence and old commands; their metal-nut blocker no longer governs this build.

---

# Existing scaffold verification

Verified 18 October 2026 from the repository root in PowerShell. Reuse the existing
environment; these commands require no installation or ML packages.

```powershell
Set-Location 'C:\Users\laksh\OneDrive\Desktop\Tech4Bharat'
.\components\.venv-p0\Scripts\python.exe -m component_inspector.cli doctor --json
.\components\.venv-p0\Scripts\python.exe -m pytest components/tests -v
.\components\.venv-p0\Scripts\python.exe -m pytest components/tests -v -p no:cacheprovider
node --version
npm --version
git status --short --branch
git branch --show-current
git check-ignore -v components/.venv-p0/probe components/data/raw/probe components/data/archives/probe components/models/probe components/.cache/probe .cache/probe components/web/node_modules/probe
git ls-files components/data components/models
```

Doctor exited 0, supported isolated Python 3.12.14. Both test runs passed 2/2.
The default test run warned that its pytest cache could not be created; the
cache-disabled run passed without warnings. This bypasses cache writes only.
Evidence: [doctor snapshot](STAGE0_DOCTOR.json) and
[cache-disabled test output](STAGE0_TESTS.txt). Resource readings fluctuate.

Optional `python -m pip check` failed (pip is absent); `uv pip check --python
components/.venv-p0/Scripts/python.exe` failed opening its default cache
(os error 183). No install or cache repair was performed, and dependency
consistency is unverified beyond successful imports and the two existing tests.

No model/data inference or acquisition was run. Backend targets remain unvalidated,
and no frontend build exists yet. Verify repository visibility in GitHub manually;
local remote configuration cannot establish private visibility.

Next: request stage 1 / remaining T01 using the exact prompt in
[the build playbook](../../docs/superpowers/plans/2026-10-18-codex-build-playbook.md).
Do not run planned acquisition, fitting or service commands until implemented.

## Stage 1 — safe acquisition

Run from the repository root. All real archives/raw data/manifests remain ignored.
No model packages are needed. See DATA_SOURCES.md for the current access blocker,
measured bytes, licence/attribution and the full archive SHA256.

```powershell
.\components\.venv-p0\Scripts\python.exe -m component_inspector.cli acquire --dataset mvtec_ad --category metal_nut
.\components\.venv-p0\Scripts\python.exe -m component_inspector.cli acquire --dataset ksdd2
.\components\.venv-p0\Scripts\python.exe -m pytest components/tests/test_sources.py -v -p no:cacheprovider
.\components\.venv-p0\Scripts\python.exe -m pytest components/tests -v -p no:cacheprovider
uv --cache-dir components/.cache/uv pip check --python components/.venv-p0/Scripts/python.exe
```

MVTec currently returns a JSON `blocked_access` record and exit **3**. This is
expected, not a successful download. KSDD2 acquisition returns exit **0**; subsequent
runs verify saved archive/inventory/raw hashes without downloading again. General
failures return JSON on stderr and exit **1**; unsupported commands still exit **2**.

After personally obtaining the category archive through the official flow, use
its real local path (the placeholder below is not a runnable acquisition):

```powershell
.\components\.venv-p0\Scripts\python.exe -m component_inspector.cli acquire --dataset mvtec_ad --category metal_nut --archive 'C:\PATH\TO\metal_nut.tar.xz'
```

Local ZIP, TAR, TAR.GZ and TAR.XZ are supported. `--archive` copies and hashes bytes
without changing the supplied archive; its provider identity and original retrieval
date are unverified. Do not use it to substitute an unrecorded mirror. Only
`mvtec_ad --category metal_nut` and `ksdd2` without a category are supported.
`--root PATH` selects an isolated project root for fictional software fixtures;
never use fictional fixture sources as real dataset/model evidence.

Safety bounds: 2 GiB archive/download, 6 GiB declared/actual extracted payload,
64 MiB per file, 20,000 visible members, 200× expansion. ZIP directory metadata is
bounded before parsing; ZIP64/multidisk/encrypted entries are rejected. TAR metadata
reads are bounded to at most 1 MiB, stream expansion includes metadata/headers,
and XZ dictionary memory is capped at 128 MiB. Links, devices, FIFOs, sparse TAR,
traversal/absolute/Windows drive/ADS/device names and path collisions are rejected.
Only regular file bytes are manually written, with per-file hashes and ZIP CRC
verification. One training PNG is decoded after extraction; full image/mask audit
is deferred to stage 2. Limits may reject other layouts; do not silently relax them.

Extraction uses a private temporary tree; raw output is published only after the
training sample check. Existing destinations are never replaced. Acquisition has
an exclusive per-dataset lock. On interruption, inspect the ignored `.acquire-*`
scratch directory and `.acquire-DATASET.lock`; do not automatically delete a lock
or existing raw/source records. Orphan archive/inventory files may remain after a
storage/publication failure and need inspection. Do not use cleanup commands on
real data. Mutation/concurrent edits by other local programs are not prevented by
an OS-level immutable filesystem; this CLI is a local single-user tool.

In this Codex sandbox the initial network calls were blocked. Approved escalation
allowed the official KSDD2 download; reading its new files for reuse verification
also required escalation. No ACLs were changed. PyPI installation of Pillow also
required approved network access. The existing venv was reused, and its editable
metadata refreshed; no ML package was installed. `uv pip check` now passes using
the explicit project-local cache (the stage 0 default-cache failure is historical).

The updated lock was generated offline from available package metadata:

```powershell
uv --cache-dir components/.cache/uv pip compile components/pyproject.toml --python components/.venv-p0/Scripts/python.exe --extra dev --generate-hashes --output-file components/requirements-setup.lock --offline
uv --cache-dir components/.cache/uv pip install --python components/.venv-p0/Scripts/python.exe --offline --no-deps -e components
```

Fresh environments require permitted network access for the hashed lock install
and build dependencies, as described in components/README.md. No clean environment
rebuild is claimed for this stage. Doctor still reports conservative scaffold
readiness flags; actual acquisition state lives in the per-dataset source records.

Stage 2 must wait for usable MVTec data or an explicitly approved scope amendment.
Do not fit models or reinterpret final-test data to work around this blocker.


## Sequential-resume checkpoint - 18 October 2026

All remaining stages are now authorised sequentially, but MVTec access remains a
genuine blocker. Fresh component suite: 53 passed. MVTec acquire: blocked_access,
exit 3. Obtain the archive personally through the official form and supply its
local path; import it with the stage 1 --archive command above. Then continue
stage 2 onward without routine approval, subject to each evidence gate and human
participation requirements. No scope amendment or permission to accept personal
terms is implied by sequential execution.

## Stage 5 commands and immutable run

Use `components/.venv-p0/Scripts/python.exe -m component_inspector.cli`.
The current frozen run is `components/runs/frozen-20261019T041652Z-9c825801`.
Commands accept `--run` followed by that directory:

- `calibrate`: normal-only calibration of both methods, D1 then D2.
- `evaluate`: original held-out memberships, only after hash-verified calibration.
- `stress`: brightness 0.6/1.4 and blur radius 2, only after all original tests.
- `report`: regenerate readable report/gallery from completed hash-verified phases.

Calibration, evaluation and stress reserve one-time phase and per-method markers.
Do not remove markers or rerun a held-out phase. On failure inspect retained logs;
a software failure is not permission to tune/repeat the holdout. Report regeneration
is read-only with respect to models and predictions. Future app/CLI/docs additions
are outside the frozen numerical-runtime graph; modifying frozen runtime, model,
source, role or configuration files invalidates this run.

Exact freeze identity and phase hashes are in `freeze.json` and each
`*_complete.json`. Large source/model/run artifacts remain ignored by Git.
