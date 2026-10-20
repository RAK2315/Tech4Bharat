# Remaining recall strategies: round 2

Started 20 October 2026 after the user authorized the remaining strategies and improvement of the strongest candidate. Status: running; no pending entry is an accuracy claim.

The retained parent is round 1 supervised KSDD2: 77/82 detected defects, 27/417 normal false alarms (93.90% recall / 6.47% FPR). The same training/evaluation membership is retained for direct comparison. Those development outcomes are already observed and now guide model selection. New results are **observed-development comparisons**, not independent confirmation.

## Fixed initial experiments

- **R04:** finer 64x160 feature grid from layers 1–3 with a fixed random 448-to-96 channel projection to keep CPU cost comparable. The RGB input remains approximately native resolution; this tests finer latent detail, not invented information from image upscaling. No claim about RGB cable gland is made.
- **R05:** same supervised architecture/IDs/60 epochs, replacing weighted pixel BCE with weighted focal loss (gamma 2). Image loss and optimizer stay fixed.
- **R06:** same saved segmentation maps, compare maximum, top 0.1% mean and maximum local 3x3 average. Each score rule gets its own normal-only threshold.
- **R07:** diagnose normal peak locations. KSDD2 is a texture surface; object-background masking and pose alignment are deferred unless task evidence justifies them. Padding is already excluded and edge defects must not be removed.
- **R08:** one actual image brightness/contrast variant (0.8–1.2) per training original, randomly used with probability 0.5. Masks and geometry stay paired. Compare original images plus fixed paired brightness/blur stress without threshold changes.
- **R09:** nested 50 of the original 100 PaDiM channels, same 128 fitting IDs/covariance formula/regularization. No defective image enters Gaussian fitting.
- **R10:** pair the strongest eligible supervised head with compact PatchCore using two fixed fusion rules. Split the 417 calibration normals into disjoint normalization and threshold subsets; never assume two separate 10%-FPR detectors produce a 10%-FPR ensemble.

At most one compound focal-plus-lighting training variant and one training-only hard-negative refinement may follow, if relevant. Check the best learned configuration with two additional initialization seeds; these are stability checks on observed development data, not new independent items. The round 1 results, model states, phase markers and original archived benchmark remain unchanged.

Each phase runs alone with at most 4 CPU threads, RSS <=min(4 GiB, 60% available RAM) and an 1,800-second pilot limit. Resource-stopped attempts and unsupported/deferred strategies are retained. Cutoffs remain alpha-0.10 normal calibration; evaluation labels will not be used to lower them to hit a desired headline.

Measured outcomes and decisions will be appended after workers finish. Protocol: `components/configs/recall_round2.json`. Local artifacts: `components/outputs/recall-round2/`.
