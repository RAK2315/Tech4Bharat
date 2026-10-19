# Stage 2 data audit - 19 October 2026

Both sources were rehashed against their acquisition inventories before decoding.
No test image was displayed or scored. Test decoding was limited to schema/mask/
duplicate integrity. Model fitting/calibration/evaluation have not run.

| Dataset | Usable official membership | Roles (images) | Selected fit / references |
|---|---|---|---|
| Cable gland RGB | train 223 normal; validation 23 normal; test 21 normal +87 anomalous | fit 129; unused fit 5; development 68; calibration 44; test 108 | 128 /16 |
| KSDD2 | train 2,085 normal +246 anomalous; test 894 normal +110 anomalous | fit 128; unused fit 1,123; development 663; calibration 417; test 1,004; quarantine 2 | 128 /16 |

Cable-gland fit role contains 129 images across 128 groups; only the 128 canonical
fit IDs may be consumed. Two same-label near pairs were conservatively grouped
(pHash Hamming 2; thumbnail MAE 1.6202 and 1.8906 on 0-255 scale), both within
original training. Their precise IDs and group decisions are in the JSON summary.
There is no cross-official-partition contamination in this audit. No supplied
physical item IDs were established: all 3,691 enumerated candidate records remain
physically unidentified. Hash/grouping checks are not physical-independence proof.

The KSDD2 archive includes train/10301 (copy).png and train/10301_GT (copy).png.
Neither has a valid image/mask pair under the documented source schema; both are
quarantined as missing_mask. They are not extra normal training examples. The
remaining 3,335 images reconcile to the provider counts. No .pyb was executed.

Cable-gland class_ids.json declares 0=good, 255=bent, 254=cut, 253=hole,
252=thread. Masks are validated against that mapping and interpreted as binary
nonzero anomaly regions; values other than 255 are not discarded. KSDD2 mask
labels are determined from verified binary masks, not filename guesses.

The KSDD2 training inventory is portrait, resolving its one recipe-wide rotation
to 90 degrees clockwise; cable gland rotation is 0. Official cable-gland
validation stays development-only. Role guards reject fit/calibration access to
final test, anomalies in normal fitting, unused fit IDs and cross-role groups.

A few development-only spot checks were viewed: cable-gland train/good/rgb/002.png
and KSDD2 train/10021.png with 10021_GT.png. The latter's upper-left annotation
plausibly matches the visible surface irregularity. This is a spot-check, not an
independent label validation or any measured model performance.

Machine-readable evidence: [summary](STAGE2_AUDIT_SUMMARY.json). Full immutable
per-recipe manifests, inventory hashes, role IDs and effective configurations are
at the ignored content-addressed path listed there. Exact cable-gland download
URL/early-review notice reconciliation remains a requirement before freeze.
