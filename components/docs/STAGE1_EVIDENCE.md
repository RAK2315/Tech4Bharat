# Stage 1 verification and self-review

18 October 2026. Base: `b36d144`; branch: `stage-1-safe-acquisition`.
Scope: remaining T01 safe acquisition only. No stage 2 or model work performed.

## Commands actually run

From repository root with `components/.venv-p0/Scripts/python.exe`:

| Command | Result |
|---|---|
| `-m component_inspector.cli acquire --dataset mvtec_ad --category metal_nut` | exit 3, persisted blocked_access with personal form action |
| `-m component_inspector.cli acquire --dataset ksdd2` | initial sandbox network failure, then approved download/extract exit 0 |
| Same KSDD2 command again | sandbox storage read denied; approved retry verified archive/inventory/all raw hashes and membership, exit 0, no second download |
| `-m pytest components/tests/test_sources.py -v -p no:cacheprovider` | **51 passed**, 1.21 s, final source-suite run |
| `-m pytest components/tests -v -p no:cacheprovider` | **53 passed**, 1.64 s, final full component suite |
| `-m component_inspector.cli doctor --json` | exit 0, isolated Python 3.12.14; doctor/acquire supported, model flags false |
| `uv --cache-dir components/.cache/uv pip check --python components/.venv-p0/Scripts/python.exe` | 10 packages checked, compatible |
| Final bounded ZIP-directory preflight on saved KSDD2 archive | accepted, no extraction or image display |
| `git diff --exit-code -- experiment` and the three tracked plan files | no changes |
| `git diff --check -- components` | no whitespace errors; CRLF normalization notices only |
| `git ls-files components/data components/models` | existing .gitkeep placeholders only |

Final full-suite output: [STAGE1_TESTS.txt](STAGE1_TESTS.txt). Ignored detailed
source run, reuse JSON and doctor output are under `components/outputs/stage1/`.
`STAGE1_SOURCES.json` contains only provenance/measurement records, no images.
Preserved plan/historical report hashes were recorded at review time in
`STAGE1_PRESERVED_HASHES.json`; Git comparison also confirms no edits there.

## Test-first evidence

- Initial executable spec: 40 failed (absent module and CLI), before implementation.
  An earlier test-fixture assertion appeared as setup errors; moved to the test
  bodies and reran to obtain actual expected test failures before implementation.
- TAR hidden metadata and forged large ZIP directory: 2 failed / 43 passed before
  hardening; fixed bounded metadata/decompression reads and directory preflight.
- Unexpected raw file: 1 failed / 47 passed before membership verification fix.
- XZ local archive: 1 failed / 48 passed before bounded XZ support.
- Tiny TAR with a 3-byte file limit: 1 failed / 49 passed before separating header
  read bounds from payload size and avoiding tarfile's intermediate stream buffer.
- Forged ZIP entry count: 1 failed / 50 passed before scanning actual directory
  headers before ZipFile allocation.
- Other regression cases exercised already-implemented behavior: CRC failure
  cleanup, blocked CLI, raw tampering, existing-download no-overwrite and retries.
- Full source suite is fictional archives/transport only. No mocked model
  predictions or fabricated human decisions were used.

RED logs are preserved under ignored `components/outputs/stage1/STAGE1*RED.txt`.
Actual KSDD2 acquisition is separate evidence, not inferred from fixture tests.

## Review and rulings

Final review: self-review, because the user prohibited subagents. This has no
independent reviewer. Reviewed source acquisition, error exits, portable path/link
handling, byte/member/metadata bounds, cleanup, idempotence, provenance/licence
records, fixture labelling and raw-data Git exclusions. Fixed the entry-count
allocation finding via observed RED→GREEN and a final green component suite.

Ruling: use the expressly requested checkout and existing environment with a
separate local branch; no worktree or subagent. Cost: no worktree isolation or
independent review. Unrelated modified README/untracked root docs are preserved.

Ruling: MVTec's personal form remains blocked rather than guessing a download URL
or accepting terms. Cost: the two-dataset gate cannot pass without human access.
No scope amendment is inferred from KSDD2 being available.

Ruling: stage 1 validates safe bytes/layout and decodes one training sample; full
label/mask pairing, duplicates, role allocation and count reconciliation stay in
stage 2. Cost: acquired does not yet mean usable for model fitting. The training
file-count discrepancy is explicitly disclosed in DATA_SOURCES.md.

No deferred code-review minors. OS-enforced read-only storage, concurrent hostile
local mutation and public/shared hosting are outside this local CLI's guarantees;
no such guarantees are claimed. Raw write-once policy is enforced by this tool,
with hashes/membership checked on reuse. Source self-hashes do not authenticate a
provider signature. Public-demo/commercial permission remains unestablished.

## Gate and manual actions

**Software gate passes; two-source readiness gate remains blocked.** Obtain MVTec
metal_nut through its official personal flow if acceptable and provide the local
archive path; resume stage 1 import rather than starting stage 2. Check the recorded
KSDD2 hash with Get-FileHash if desired. Review licence/attribution before any public
redistribution. No push, deployment, ML fitting or final-test design inspection.

Sandbox limits: network and new downloaded-file reads required approved escalation;
Git status in the sandbox may warn about the inaccessible ignored raw directory.
No ACLs were changed. The normal approved read verified data successfully.
