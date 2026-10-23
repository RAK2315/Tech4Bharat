# Frozen-model external transfer check

Registered 23 October 2026 before external image prediction. This is a
zero-shot cross-dataset evaluation, not training or application development.

## Fixed model and question

Evaluate only the already selected `ksdd2-ensemble-mvp-v1`: existing
confirmation fold 0, seeds 4220/4221/4222, `longer108`, model identity
`8ddcac9907af4c033cbc9ff208f452ce572ea6b251da373cf267c2a3df95f355`.
The cutoff stays **0.33108379983608666**, strict greater-than. No fitting,
calibration, orientation search, threshold scan, best-member choice or new
ensemble weights. Use the existing `vision/ksdd2_ensemble.py` unchanged.

Question: how does the exact selected model perform on other datasets without
adaptation? Do not present another domain's results as new same-line factory
confirmation, or mix separate datasets into one favorable average.

## Source selection fixed before scoring

1. **Magnetic Tile Defects**, entire six-category authors' release at commit
   `cc4eb530b57b9cb7225bf76023873043ffd50655`, from
   [the authors](https://github.com/abin24/Magnetic-tile-defect-datasets.).
   `MT_Free` is normal; Blowhole/Break/Crack/Fray/Uneven are defective.
   Use original image files, not masks or overview collages. Category labels
   define binary truth; retain and disclose empty-mask/category disagreements.
   The authors welcome research use with citation; no additional commercial
   rights or redistribution permission are inferred.
   Annotation-format inspection before any prediction found that some original
   magnetic masks contain grayscale saliency values rather than strict binary
   labels. Preserve them: nonzero defines mask presence/area for descriptive
   inventory only; image-level category truth remains authoritative. Report
   nonbinary-mask counts. Do not optimize a mask threshold or relabel categories.
2. **KolektorSDD1**, entire 399-image fine-annotation release linked by
   [ViCoS](https://www.vicos.si/resources/kolektorsdd/), public
   `https://data.vicos.si/datasets/KSDD/KolektorSDD.zip`.
   Nonempty paired fine mask means defective; empty mask means normal.
   This is separate from KSDD2 but from the same research/industrial provider;
   physical-product independence is not established. CC BY-NC-SA 4.0.
3. **DAGM 2007 Class 1 only**, all images in original `Class1.zip` (normal)
   and `Class1_def.zip` (defective), linked by the
   [competition](https://conferences.mpi-inf.mpg.de/dagm/2007/prizes.html).
   This first-numbered class was selected for bounded compute before scoring,
   not for performance. It is synthetic texture/defect data, not real factory
   images or evaluation of all ten DAGM classes. No commercial rights claimed.

If a source cannot be acquired or verified, retain the failure and report it
as unavailable. Do not replace it based on model outcomes. No authentication,
terms acceptance, paid acquisition or public redistribution of images.

## Inventory, exclusions and label separation

Record original archives' URLs, final locations, sizes and SHA-256, image IDs,
encoded/decoded hashes and dimensions. Validate paired masks where provided;
never infer a missing mask as a normal label. Lock the complete inventory and
source labels before any inference. Exclude only byte-identical or
shape-and-RGB-identical overlap with the original 2,331-image KSDD2 TRAIN pool,
recording every exclusion. Do not read official KSDD2 test images. Report exact
duplicates within/between new sources without silently selecting a subset;
no crops/augmentations are counted as independent images.

For transport compatibility, decode each source with EXIF correction and
convert to RGB PNG losslessly, recording the exact pixel hash before and
after. This handles original BMP without changing image geometry or
intensity. Do not enlarge images to bypass the model's 128-pixel minimum side.
Apply existing media limits and frozen 90-degree rotation/letterboxing to all
datasets, even if different views might help. Keep technical rejects with null
score/flag and their reasons; no hidden normal prediction on failure.

The scoring worker receives only original ID, canonical image path and hash;
no masks or labels. Predictions are immutable and joined to locked truth only
after inference. Store all member logits and the combined score; score each
image once, with one fixed cutoff. No diagnostic threshold sweep follows.

## Metrics and verification

Per dataset report TP/FN/FP/TN, defects/normals, effective recall (technical
defect rejects count as misses), false alarms among scored normals, normal and
defect coverage, precision and descriptive binomial intervals. Report failed
media separately; rejected normals are not true negatives. Retain category
slices and mask-defined small-defect counts where valid; they are descriptive,
not selection criteria. Do not pool datasets or interpret pixel masks as a
pixel-accuracy claim.

Independently recompute the sigmoid/three-member average, strict cutoff flags,
counts and label joins from saved outputs. Require all declared originals to
be accounted for. Model files, manifest and numerical source hashes must match
before and after; source-record images must match inventory hashes. Audit
encoded/decoded KSDD2 TRAIN overlap before inference. Descriptive intervals
assume independent images; unknown same-product/lot correlations and repeated
source frames mean those intervals are not factory guarantees.

Four CPU threads, one owned ML worker at a time, 1,800 seconds and
min(4 GiB, 60% available RAM) per dataset phase. Preserve all failures, resource
logs, source inventories and predictions in a new output directory. Keep
original studies and the open ML handoff unchanged except an additive result
link after reporting. New exposed data cannot later be called untouched.

## Inventory repair before any inference

The first inventory attempt stopped on a strict-binary-mask assertion. The
source fine mask `kos20/Part4_label.bmp` has values 0, 85 and 255, while 388
Magnetic Tile masks are grayscale. Nonempty-mask image labels and nonzero-area
accounting were already the declared rules, so retain these originals and
report their annotation formats; no defect is dropped or relabeled. Preserve
the failed source, diagnosis and partial inventory under the first output root.
Complete the inventory in the new `external-transfer-20261023-v2` root using
the exact same acquired archives. Frozen numerical/model code and thresholds
are unchanged. Register all final source/input hashes before first prediction.
