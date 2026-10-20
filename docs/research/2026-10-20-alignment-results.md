# Training/scoring alignment after the recall study

20 October 2026. **Running: no unmeasured outcome is an accuracy claim.** This follow-up addresses a reproducible training instability found while checking the remaining recall strategies.

## Why another experiment was necessary

The [remaining-strategy study](2026-10-20-round2-results.md) reached 80/82 detected defects and 22/417 normal false alarms (97.56% recall / 5.28% FPR) with focal training, localized scoring and hard-normal refinement. A full repeated training run with seed 4218 also caught 80/82, but seed 4219 collapsed to 3/82 with 42/417 false alarms. Two good runs did not establish a reliable training recipe.

The failed checkpoint reproduces all 916 stored calibration/evaluation scores exactly. Across the three seeds, channel normalization tensors are identical, feature-cache paths match and model weights are finite. The failed seed's learned image-classifier coefficient on the maximum local defect logit is -1.148, while successful seeds learn positive coefficients. This permits the image-classification objective to encourage decreasing the strongest local score on a defective image, even though the inference rule interprets larger localized scores as more defective. Background-logit shortcuts can fit training labels while conflicting with localized inference.

Ranked diagnosis: (1) learned-classifier/scoring conflict; (2) normalization or artifact mismatch; (3) insufficient localization learning. Targeted probes exclude the normalization mismatch and show the sign conflict; the corrective experiments test its practical effect. The original bad result remains in the evidence and is not discarded as an inconvenient seed.

## Correction and fixed experiment

The image loss now directly uses **BCE of the same top-0.1%-mean segmentation logit used at inference**. Weighted focal pixel supervision remains gamma 2, positive weight 8. The unused learned classifier is frozen and contributes neither to training nor inference. This removes its ability to reverse the meaning of the localization score.

Everything else follows the recorded recipe: frozen ResNet18 layers 2/3; 384-channel 32x80 cached features with a float16 roundtrip; 128 original normals plus 164 labeled defects; 60 base epochs with AdamW learning rate 0.001; training-only mining of 128 additional normals from 1,123 eligible originals; 12 refinement epochs at learning rate 0.0002. Batch size is 4, weight decay 0.0001 and gradient clipping 5. Normalization uses only the original fitting images. No lighting augmentation is added.

Seeds **4217, 4218 and 4219** were recorded before fitting. Seed 4217 remains canonical; both repeats are always reported and cannot silently replace it. Each trained model gets its own normal-only rank cutoff at alpha 0.10 using the same 417 reserved normals. Evaluation remains the same 82 defects and 417 normals, all from the provider's training split. No official test image enters this study. These outcomes are continued selection on already observed development data, not independent confirmation.

## Regression checks before full training

A test at the actual objective seam first failed under the old learned-classifier loss: flipping an unused classifier's sign changed the loss and segmentation gradients. It passed after using the aligned objective. Additional tests verify that positive-image loss pushes the selected valid peak upward, padding receives no score gradient, and differentiable training pooling exactly matches the existing inference pooling. The full suite passed **116 tests** with 45 pinned-backend deprecation warnings in 28.72 seconds.

The corrected full three-seed training experiment, original-image parity and split/metric audits must finish before declaring the practical failure resolved. A software property test alone is not a recall result.

## Reproduce

Recreate the [round 1 data, feature cache and pinned environment](2026-10-19-round1-results.md#reproduction-commands), then run from the repository root in PowerShell:

```powershell
components/.venv-p0/Scripts/python.exe components/tools/run_recall_alignment.py --root components/outputs/recall-alignment --parent components/outputs/recall-round1
components/.venv-p0/Scripts/python.exe components/tools/verify_recall_alignment.py --root components/outputs/recall-alignment
components/.venv-p0/Scripts/python.exe components/tools/benchmark_recall_round2.py --root components/outputs/recall-alignment --weights .cache/recall-downloads/model.safetensors --method aligned
components/.venv-p0/Scripts/python.exe components/tools/summarize_recall_round2.py --root components/outputs/recall-alignment --output-directory docs/research/alignment-replication
```

Use a new empty run directory for a changed experiment. Each worker runs alone with four CPU threads, at most min(4 GiB, 60% available RAM), and a 1,800-second phase cap. All completed and failed attempts remain recorded. Raw datasets, feature arrays and trained tensors are local ignored artifacts; source code, configurations, exact score rows and compact evidence are tracked.
