# Current dataset scope - 18 October 2026

The user selected cable gland and requested updates to the previously prepared
files. This amendment replaces the original metal-nut D1 with **RGB-only MVTec
3D-AD cable_gland**. D2 remains KSDD2. It takes precedence over older metal-nut
requirements in historical plans, source evidence and dated status entries.
The updated execution plan remains the active ordered technical contract.

## Data and recipe contract

- D1 dataset/category: `mvtec_3d_ad/cable_gland`.
- Active recipe: `mvtec_3d_cable_gland_rgb`.
- Raw root: `components/data/raw/mvtec_3d_cable_gland/cable_gland/`.
- Use only `train/good/rgb/*.png`, `validation/good/rgb/*.png`,
  `test/*/rgb/*.png`; pair test masks from `test/*/gt/*.png` by ID.
- Preserve XYZ TIFFs, calibration and notices as inert source evidence. Do not
  pass them to models or treat camera calibration as model threshold calibration.
- Expected initial RGB counts: 223 training normals, 23 validation normals,
  21 test normals and 87 test anomalies (bent 21; cut/hole/thread 22 each).
  These counts need decoding/label/mask/group audit before benchmark reporting.
- Train normals alone supply the seeded 60/20/20 fit/development/calibration
  split. Independent-image arithmetic is 134/45/44; actual grouped counts govern.
  At most 128 fit groups and 16 baseline references, as before.
- Official validation normals are development-only (68 development normals if
  independent). Never use them for fitting, threshold calibration or final test.
- Keep original partition and experimental role separately. Audit duplicates
  across train/validation/test and quarantine contamination with reasons.
- D1 has no development anomalies. Do not borrow test defects for tuning.
- RGB aspect-preserving letterbox H256 W256, zero RGB padding, no rotation,
  cropping, registration or augmentation. Original-coordinate map checks remain.
- Model fitting, thresholds, display scales and results stay separate from KSDD2.
  No 3D, nut/bolt, material-strength or factory-effectiveness claims are supported.

## Gates retained

The original CPU/resource caps, reference baseline and PaDiM comparison, seed,
normal-only calibration, data-role separation and one frozen final evaluation
remain unchanged. Both active recipes/configurations must freeze before either
test is scored. Existing 90% recall and 10% FPR screens remain: with unchanged
D1 test counts this requires at least 79/87 anomalies flagged and at most 2/21
normal false flags. Report counts, uncertainty and quarantined cases.
A failed model gate is a valid outcome; it does not authorize holdout tuning.
Human decisions and timed participation remain personal milestones.

## Source uncertainty and current implementation

Safe import succeeded; archive SHA256 is
`63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed`.
The acquisition mode is local_archive_unverified_provider_identity. The exact
provider download URL and original retrieval date are unknown. The included
readme calls the archive an early review subset. Record the actual download
source and reconcile that notice before experiment freeze or publication.
Do not remove or silently rewrite that uncertainty. No personal terms accepted.
See DATA_SOURCES.md and STAGE1_SOURCES.json for hashes and retained notices.

Both active datasets are acquired, not audited or split. The original MVTec AD
metal-nut source remains a deferred blocked record; it no longer blocks work on
the replacement recipe. Model/API/UI commands are still unimplemented.
No new final accuracy, model readiness or completed Stage 2 is claimed.
