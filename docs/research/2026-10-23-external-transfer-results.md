# Frozen ensemble on external datasets

Measured 23 October 2026.

**All three transfer checks failed the practical target.** Normal false alarms
were 99.42%–100% among scored normal images. The frozen model flags almost
everything on these sources, so high recall does not indicate useful detection.
It does not reliably transfer to these other products/textures as-is.

**Model used:** the same frozen `ksdd2-ensemble-mvp-v1`: three `longer108` supervised ResNet18-feature heads (seeds 4220/4221/4222), existing confirmation fold 0. The numeric cutoff remained **0.33108379983608666**, strict greater-than. No new models were trained; no external normal calibration, threshold search, orientation selection or adaptation occurred.

These datasets were newly acquired for this project and excluded from the supervised heads' fitting/calibration. This tests transfer to other products/textures, not new same-line factory performance. Unknown backbone pretraining exposure and physical product relationships are not ruled out.

## Every registered dataset

| Dataset | Defects / normals | Defects caught | Effective recall | False alarms / scored normals | False-alarm rate | Scored / all images |
|---|---:|---:|---:|---:|---:|---:|
| [DAGM 2007 Class 1 — synthetic textures only](https://conferences.mpi-inf.mpg.de/dagm/2007/prizes.html) | 150 / 1000 | 150/150 | 100.00% | 1000/1000 | 100.00% | 1150/1150 |
| [KolektorSDD1 — real surfaces, same provider as KSDD2](https://www.vicos.si/resources/kolektorsdd/) | 52 / 347 | 52/52 | 100.00% | 345/347 | 99.42% | 399/399 |
| [Magnetic Tile Defects — real tiles, independent provider](https://github.com/abin24/Magnetic-tile-defect-datasets.) | 392 / 952 | 338/392 | 86.22% | 884/884 | 100.00% | 1222/1344 |

Recall includes rejected defective images as misses. False-alarm rate uses only scored normal images; rejected normals are neither true negatives nor successful inspections. Rates must be read with coverage. Dataset results are never pooled.

## Technical rejects and annotation accounting

- **dagm1:** 0 defective and 0 normal images rejected; reasons: `{}`. 0 nonbinary masks; 0 mask/category disagreements.
- **ksdd1:** 0 defective and 0 normal images rejected; reasons: `{}`. 1 nonbinary masks; 0 mask/category disagreements.
- **magnetic:** 54 defective and 68 normal images rejected; reasons: `{"Image minimum side below 128 pixels": 122}`. 388 nonbinary masks; 4 mask/category disagreements.

Magnetic Tile truth follows the original folder categories: MT_Free is normal; Blowhole/Break/Crack/Fray/Uneven are defects. Four MT_Uneven images have empty source masks; all are retained as defective category labels, with the disagreement disclosed. Grayscale masks are preserved using nonzero support for descriptive area; it is not pixel-precise ground truth. KolektorSDD1 truth uses nonempty original fine masks. DAGM uses the original normal/defect archive identities, with all 1,150 Class 1 images; it is not a full-DAGM result.

The overlap audit compared encoded and shape-plus-decoded RGB hashes with all 2,331 original KSDD2 TRAIN images: **0 overlaps excluded**. There were **16 exact decoded duplicate groups**, all pairs within KSDD1 with consistent binary labels, recorded in the raw audit. Unknown near-duplicates, same-item frames and lot dependence are not eliminated by this check. KSDD1 has multiple views per product; image counts do not imply that many independent products.

## Descriptive small-defect slice

Only defective images with a nonempty supplied mask occupying <=0.5% of source pixels are included below. This is exploratory, with no tuning. Magnetic saliency masks make this size estimate approximate; four empty-mask positive categories are excluded only from the size slice and remain in the primary defect counts. No pixel recall is claimed.

| Dataset | Small images caught / total | Effective small-image recall |
|---|---:|---:|
| dagm1 | unavailable | unavailable |
| ksdd1 | 24/24 | 100.00% |
| magnetic | 151/178 | 84.83% |

## What this means

These fixed-cutoff transfer checks define the model's current scope; they do not establish that it can inspect every component. Strong defect recall with high normal false alarms would not meet the target. Poor results must not be repaired by tuning this cutoff on these evaluation labels and calling the result unseen validation. A different product/camera may need its own data and separately trained/calibrated recipe, followed by an independent confirmation batch. The exact KSDD2 MVP model and all previous results remain unchanged.

## Verifiable proof and failures

All 2893 original image and canonical PNG hashes/pixels were checked. A separate SciPy calculation reproduced all 2771 scored three-member averages and flags. Manual rejection-aware counts matched the existing evaluation implementation. Model, manifest, numerical source and input hashes were unchanged. No official KSDD2 test image was opened. The independent audit is from this session, not external certification.

The scorer checks inventory files' integrity hashes, including label-bearing
metadata, but does not parse or use their truth labels to compute predictions.
Only the post-inference verifier joins prediction IDs to truth. No mask, label
or defect-size group chooses the model's input geometry or score.

The scoring workers completed in 95.437 seconds (Magnetic Tile), 44.000 seconds
(KSDD1), and 97.172 seconds (DAGM Class 1), peaking at approximately 402 MB
sampled owned-process-tree RSS. The independent audit completed in 32.141
seconds, peaking at 179,400,704 bytes. Its separate
[resources](2026-10-23-external-transfer-audit-resources.json) and
[log](2026-10-23-external-transfer-audit-worker.log) are preserved outside the
export tree.

Eight new rejection-accounting tests passed before scoring. The final full
software run was **160 passed / 4 failed**, rather than a clean pass. All four
failures occur in legacy PaDiM tests when Windows Application Control blocks
the installed `kornia_rs` DLL. A fresh standalone import reproduced that policy
error, while a fresh selected-ensemble load and the registered hash/version
guard passed. No security policy was bypassed, and no model, threshold or
prediction changed. The failed suite, XML, logs and diagnosis are preserved in
[software summary](external-transfer-software/summary.json) and
[diagnosis](external-transfer-software/diagnosis.json). The successful inference
and independent result audit are separate from these blocked legacy checks.

The first inventory attempt failed a strict-binary annotation assertion before any prediction: one KSDD1 fine mask has values 0/85/255. The failed source, diagnosis and partial first-root inventory are preserved. The second inventory retains nonzero-mask labels, keeps all originals, discloses grayscale masks and uses a new exclusive output root; no model, label or threshold was selected from outcomes.

The first staged-publication check also stopped on the existing CRLF dependency
lock, which the older checker's seven-Python-file allowlist did not cover. Its
[failed attempt](2026-10-23-external-transfer-publication-attempt-1.json) is
retained. The unchanged frozen lock and media helper are checked separately
against their exact registered working SHA-256 and canonical Git LF bytes;
explicit checkout attributes preserve their CRLF bytes. Raw failed-test logs
and XML retain their whitespace and hashes. These publication details change
no model, score, label, threshold or numerical source.

Original images were decoded, EXIF-corrected and losslessly stored as RGB PNG for transport, with exact decoded-pixel equality checks. No image was enlarged to evade the minimum-side rule. Frozen 90-degree rotation and letterbox geometry were unchanged even for square textures. Every scoring phase used four CPU threads, one ML worker at a time, at most 1,800 seconds and min(4 GiB,60% free RAM). Resources and elapsed times are measured logs, not controlled performance benchmarks.

The preregistered rules were published before scoring, followed by the full source/inventory-hash registration before inference. DAGM is synthetic, KSDD1 shares the Kolektor/ViCoS provider, and Magnetic Tile is a different material/product. Descriptive exact binomial intervals are in the raw summary, with dependence limits. No commercial-use or data-redistribution permission is asserted.

Evidence: [protocol](2026-10-23-external-transfer-protocol.md), [frozen registration](2026-10-23-external-transfer-preregistration.json), [all counts and intervals](external-transfer/summary.json), [independent verification](external-transfer/verification.json), [inventory audit](external-transfer/inventory-audit.json), [failed inventory attempt](external-transfer/inventory-attempt-1-failure.json), [failed source](external-transfer/inventory-attempt-1-source.py), [export hashes](external-transfer/export-index.json).
