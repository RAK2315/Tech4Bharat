# VisA PCB data acquisition — 19 October 2026

## Scope and user constraint

The user requested downloading VisA PCB data and explicitly instructed: **do not
implement a CNN for it ourselves**. This task acquires and verifies data only.
It does not authorize model implementation, fitting, training, threshold selection
or final-test evaluation. Any future modelling should respect that constraint and
use an established implementation if separately requested.

Status: **complete — official archive downloaded, PCB1–PCB4 extracted and verified; no model implemented or trained**.

## Official source

- Repository: https://github.com/amazon-science/spot-diff
- Source archive: https://amazon-visual-anomaly.s3.us-west-2.amazonaws.com/VisA_20220922.tar
- Release filename: `VisA_20220922.tar`.
- HTTP Content-Length checked: **1,929,840,640 bytes**.
- Dataset license: **CC BY 4.0**; retain attribution and the supplied license.
- Attribution: Yang Zou, Jongheon Jeong, Latha Pemula, Dongqing Zhang and Onkar
  Dabeer, *SPot-the-Difference Self-Supervised Pre-training for Anomaly Detection
  and Segmentation*, ECCV 2022.

The full official archive contains 12 categories. Only `pcb1`, `pcb2`, `pcb3`
and `pcb4` are to be extracted; the source archive is retained. Original images,
multiclass mask bytes and category annotation CSVs are preserved without resizing,
binarizing masks or reorganizing into a new training protocol.

## Official one-class split metadata

Verified from `split_csv/1cls.csv` at upstream commit
`2a692ab575001cbde74d402d897a7286086c6199`. Local extraction reconciled exactly to these upstream CSV counts.

| Category | Train normal | Test normal | Test anomalous | Total images |
|---|---:|---:|---:|---:|
| PCB1 | 904 | 100 | 100 | 1,104 |
| PCB2 | 901 | 100 | 100 | 1,101 |
| PCB3 | 905 | 101 | 100 | 1,106 |
| PCB4 | 904 | 101 | 100 | 1,105 |
| Total | 3,614 | 402 | 400 | 4,416 |

These official roles are metadata, not a new project development/calibration/test
protocol. No model should use test images for fitting or tuning. The previous
PCB1 mirror experiment already observed a PCB1 holdout; downloading official
bytes does not make corresponding images or physical products untouched again.
Physical-product independence has not been established.

## Verified local paths (relative to repository root)

- Source archive: `components/data/archives/VisA_20220922.tar`.
- Selected raw data: `components/data/raw/visa_pcb_official_20220922/`.
- Metadata: `components/data/manifests/visa_pcb_official_20220922/`.
- Metadata includes `source.json`, per-file `inventory.json`, upstream `1cls.csv`,
  filtered `pcb_1cls.csv`, upstream README, dataset license, NOTICE and an inert
  text copy of `id2class.py`.

Data and generated metadata remain ignored by Git. Preserve them with the local
archive and this acquisition note if recreating the research environment later.
No changes to the earlier frozen cable/KSDD2 run are part of this acquisition.

## Verification

Completed: all **4,820 extracted files** rehashed against inventory with zero mismatches;
**4,416 RGB images, 400 anomaly masks and 4 category CSVs**. Exact image/mask
membership reconciled to the pinned official one-class CSV. All image headers
and mask dimensions validated without displaying images or scoring them.

Archive SHA256: `2eb8690c803ab37de0324772964100169ec8ba1fa3f7e94291c9ca673f40f362`.
Extracted bytes: **960,432,308**. Archive plus extracted PCB bytes: **2,890,272,948**,
excluding small manifests/documentation. Redundant download ranges/partial copy
were removed after final archive and extraction verification.

Machine-readable source, hashes, dimensions and split counts are in
`components/data/manifests/visa_pcb_official_20220922/source.json`; per-file hashes
are in `inventory.json`. The S3 multipart ETag is an object identity, not a provider-published
SHA256 checksum. Local archive hashing must not be described as independent
provider checksum authentication.
