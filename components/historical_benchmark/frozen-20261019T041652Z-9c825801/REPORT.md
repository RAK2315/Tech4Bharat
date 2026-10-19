# Frozen research evaluation

Decision: **no_go**.

Local noncommercial research on identified supplied archives. Cable-gland early-review notice and unverified provider release identity remain disclosed.

No factory-readiness or human inspection-time saving is established. Quality warnings do not exclude images. Technical rejected defects count as misses.

Primary method was PaDiM before test access. Baseline-only success requires a scope decision. No holdout tuning or repeat evaluation is permitted.

| Recipe / method | TP / FN / FP / TN | Recall | Accepted-normal FPR | Coverage | Warm p95 seconds | Peak tree RSS GiB | Screen |
|---|---|---|---|---|---|---|---|
| mvtec_3d_cable_gland_rgb / reference | 3 / 84 / 1 / 20 | 3.45% | 4.76% | 100.00% | 0.0580 | 0.177 | False |
| mvtec_3d_cable_gland_rgb / padim | 11 / 76 / 1 / 20 | 12.64% | 4.76% | 100.00% | 0.1683 | 0.798 | False |
| ksdd2_surface / reference | 74 / 36 / 75 / 819 | 67.27% | 8.39% | 100.00% | 0.1482 | 0.208 | False |
| ksdd2_surface / padim | 84 / 26 / 77 / 817 | 76.36% | 8.61% | 100.00% | 0.3617 | 1.197 | False |

## Paired stress (same test items; not independent validation)

| Recipe / method / transform | Recall | Accepted-normal FPR | Coverage |
|---|---|---|---|
| mvtec_3d_cable_gland_rgb / reference / blur_radius_2 | 0.00% | 4.76% | 100.00% |
| mvtec_3d_cable_gland_rgb / reference / brightness_0p6 | 2.30% | 0.00% | 100.00% |
| mvtec_3d_cable_gland_rgb / reference / brightness_1p4 | 59.77% | 76.19% | 100.00% |
| mvtec_3d_cable_gland_rgb / padim / blur_radius_2 | 11.49% | 0.00% | 100.00% |
| mvtec_3d_cable_gland_rgb / padim / brightness_0p6 | 11.49% | 0.00% | 100.00% |
| mvtec_3d_cable_gland_rgb / padim / brightness_1p4 | 14.94% | 0.00% | 100.00% |
| ksdd2_surface / reference / blur_radius_2 | 40.00% | 1.90% | 100.00% |
| ksdd2_surface / reference / brightness_0p6 | 100.00% | 100.00% | 100.00% |
| ksdd2_surface / reference / brightness_1p4 | 100.00% | 99.89% | 100.00% |
| ksdd2_surface / padim / blur_radius_2 | 81.82% | 14.09% | 100.00% |
| ksdd2_surface / padim / brightness_0p6 | 70.00% | 4.81% | 100.00% |
| ksdd2_surface / padim / brightness_1p4 | 80.00% | 10.51% | 100.00% |

Full per-method result JSON files contain Wilson 95% intervals, explicit numerators/denominators, precision, scored-subset AUROC/AP, technical rejects, warning diagnostics, cold/init timing and pixel diagnostics.

Pixel metric is macro per-anomalous-image pixel AUROC where defined; it is not pooled dataset pixel AUROC. Empty/constant truth masks have no defined AUROC.

Fit time, model bytes and feasibility resources are in the development summaries locked in freeze.json. Inference resources are conservative owned-process-tree RSS samples, including initialization.

See [failure gallery](gallery.html), freeze.json, calibration_complete.json, evaluation_complete.json and stress_complete.json for identities and hash-linked evidence. Missing gallery categories are explicitly marked.

## Additional saved-prediction analysis

See SUPPLEMENT.json for verified defect-folder recall, appearance-group bootstrap intervals (seed 4217, 1000 replicates), gallery hashes and limitations. Physical independence is unknown.

- Pixel average precision was not collected by the frozen worker and is unavailable.
- Full raw test maps were not archived. Fixed-scale gallery visualizations and macro per-anomalous-image pixel AUROC are available.
- No repeat test inference was performed to recover missing secondary outputs. These require a future independently frozen experiment.
