"""Recount external transfer outcomes, audit provenance, and export evidence."""
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import shutil

import numpy as np
from PIL import Image, ImageOps
from scipy.special import expit
from scipy.stats import binomtest

from external_transfer import ROOT, REPO, PROJECT, DATASETS, guard, read, write, pixel_hash, source_images
from component_inspector.evaluation.metrics import evaluate
from component_inspector.vision.ksdd2_ensemble import DEFAULT_MANIFEST, sha256


def rate(numerator, denominator):
    if not denominator: return {"numerator": numerator, "denominator": 0, "rate": None, "exact_95": None}
    bounds = binomtest(numerator, denominator).proportion_ci(confidence_level=.95, method="exact")
    return {"numerator": numerator, "denominator": denominator, "rate": numerator / denominator,
            "exact_95": [float(bounds.low), float(bounds.high)]}


def recount(predictions, truth):
    assert len(predictions) == len(truth) == len({row["id"] for row in predictions})
    assert {row["id"] for row in predictions} == set(truth)
    counts = dict.fromkeys(("TP", "FN", "FP", "TN", "rejected_anomalies", "rejected_normals"), 0)
    reasons = Counter()
    for row in predictions:
        label = truth[row["id"]]
        if row["status"] == "scored":
            assert math.isfinite(row["score"]) and type(row["flagged"]) is bool
            counts[("TP" if row["flagged"] else "FN") if label else ("FP" if row["flagged"] else "TN")] += 1
        else:
            assert row["status"] == "rejected" and row["score"] is row["flagged"] is None
            counts["rejected_anomalies" if label else "rejected_normals"] += 1
            if label: counts["FN"] += 1
            reasons[row["reason"]] += 1
    positives = sum(truth.values()); negatives = len(truth) - positives
    assert counts["TP"] + counts["FN"] == positives
    assert counts["FP"] + counts["TN"] + counts["rejected_normals"] == negatives
    scored_normals = negatives - counts["rejected_normals"]
    result = {"counts": counts, "originals": len(truth), "defects": positives, "normals": negatives,
              "recall": rate(counts["TP"], positives), "accepted_normal_fpr": rate(counts["FP"], scored_normals),
              "false_flags_all_normals": rate(counts["FP"], negatives),
              "precision": rate(counts["TP"], counts["TP"] + counts["FP"]),
              "coverage": rate(len(truth) - counts["rejected_anomalies"] - counts["rejected_normals"], len(truth)),
              "defect_coverage": rate(positives - counts["rejected_anomalies"], positives),
              "normal_coverage": rate(scored_normals, negatives), "rejection_reasons": dict(reasons)}
    other = evaluate(predictions, truth)
    assert counts == other["counts"]
    for key in ("recall", "accepted_normal_fpr", "precision", "coverage", "false_flags_all_normals"):
        assert result[key]["rate"] == other[key]["rate"]
    result["ranking_scored_only"] = other["ranking_scored_only"]
    return result


def main():
    protocol = guard(); manifest = read(DEFAULT_MANIFEST); summary = {}; arithmetic = 0; raw_hashes = 0
    old_rows = read(PROJECT / "outputs/recall-round1/manifest.json")["records"]
    assert len(old_rows) == 2331 and all(row["official_split"] == "train" for row in old_rows)
    old_encoded = {row["hashes"]["sha256"] for row in old_rows}; old_decoded = {row["hashes"]["decoded_sha256"] for row in old_rows}
    seen = defaultdict(list); disagreements = []; excluded = []
    for acquisition in (ROOT / "acquisition-complete.json",): assert all(read(acquisition)["sources"].values())
    for path in ROOT.glob("acquisition-*.json"):
        value = read(path)
        if not value.get("selected_archive"): continue
        archive = Path(value["selected_archive"]); expected = value["attempts"][-1]
        assert sha256(archive) == expected["sha256"] and archive.stat().st_size == expected["bytes"]
    for dataset in DATASETS:
        inventory = read(ROOT / f"inventory-{dataset}.json")["rows"]
        inference = read(ROOT / f"inference-{dataset}.json")["rows"]
        original = {str(path): (label, category, mask) for path, label, category, mask in source_images(dataset)}
        assert set(original) == {row["original_path"] for row in inventory}
        for row in inventory:
            source = Path(row["original_path"]); canonical = Path(row["canonical_path"])
            assert sha256(source) == row["original_sha256"] and sha256(canonical) == row["canonical_sha256"]
            with Image.open(source) as image:
                rgb = ImageOps.exif_transpose(image).convert("RGB"); rgb.load()
                assert pixel_hash(rgb) == row["decoded_sha256"] and rgb.size == (row["width"], row["height"])
            with Image.open(canonical) as image: assert pixel_hash(image.convert("RGB")) == row["decoded_sha256"]
            label, category, mask = original[str(source)]
            assert (row["label"], row["category"]) == (label, category)
            if mask:
                assert sha256(mask) == row["mask_sha256"]
                with Image.open(mask) as image:
                    assert image.size == (row["width"], row["height"])
                    pixels = np.asarray(image.convert("L"))
                assert bool(pixels.any()) == row["mask_nonempty"]
                assert float((pixels > 0).mean()) == row["mask_area_fraction"]
                if dataset == "ksdd1": assert bool(pixels.any()) == bool(label)
                elif bool(pixels.any()) != bool(label):
                    disagreements.append({"id": row["id"], "category": category, "label": label, "mask_nonempty": bool(pixels.any())})
            overlap = row["original_sha256"] in old_encoded or row["decoded_sha256"] in old_decoded
            assert row["excluded_ksdd2_train_overlap"] == overlap
            if overlap: excluded.append({"id": row["id"], "reason": "Encoded or decoded KSDD2 TRAIN overlap"})
            seen[row["decoded_sha256"]].append(row["id"]); raw_hashes += 1
        rows = [row for row in inventory if not row["excluded_ksdd2_train_overlap"]]
        truth = {row["id"]: row["label"] for row in rows}
        assert len(rows) == len(inference) and {row["id"] for row in inference} == set(truth)
        output = read(ROOT / f"predictions-{dataset}.json")
        assert output["protocol_identity"] == protocol["identity"] and not output["labels_or_masks_read_for_scoring"]
        predictions = output["rows"]
        for row in predictions:
            if row["status"] != "scored": continue
            assert len(row["member_logits"]) == 3 and all(math.isfinite(v) for v in row["member_logits"])
            independent = float(np.mean(expit(np.asarray(row["member_logits"], dtype=np.float64))))
            assert abs(row["score"] - independent) <= 1e-12
            assert row["flagged"] == (independent > protocol["threshold"]); arithmetic += 1
        metrics = recount(predictions, truth); by_pred = {row["id"]: row for row in predictions}
        categories = {}
        for category in sorted({row["category"] for row in rows}):
            part = {row["id"]: row["label"] for row in rows if row["category"] == category}
            categories[category] = recount([by_pred[i] for i in part], part)
        metrics["categories"] = categories
        small = {row["id"]: row["label"] for row in rows if row["label"] and row.get("mask_area_fraction", 1) <= .005
                 and row.get("mask_nonempty", False)}
        metrics["small_mask_images"] = recount([by_pred[i] for i in small], small) if small else None
        metrics["source_images_before_overlap_exclusion"] = len(inventory)
        metrics["nonbinary_masks"] = sum(not row["mask_is_binary_0_255"] for row in rows if "mask_is_binary_0_255" in row)
        metrics["mask_category_disagreements"] = sum(bool(row["label"]) != row["mask_nonempty"] for row in rows if "mask_nonempty" in row)
        metrics["source_dimensions"] = {"width_range": [min(r["width"] for r in rows), max(r["width"] for r in rows)],
                                         "height_range": [min(r["height"] for r in rows), max(r["height"] for r in rows)]}
        resources = read(ROOT / f"score-{dataset}-resources.json")
        assert resources["status"] == "completed" and resources["peak_sampled_rss_bytes"] <= resources["rss_cap_bytes"]
        summary[dataset] = metrics
        print("VERIFIED", dataset, metrics["counts"], flush=True)
    audit = read(ROOT / "inventory-audit.json")
    assert audit["overlap_exclusions"] == excluded and audit["mask_vs_category_disagreements"] == disagreements
    assert audit["exact_decoded_duplicate_groups"] == [ids for ids in seen.values() if len(ids) > 1]
    guard()
    write(ROOT / "summary.json", {"protocol_identity": protocol["identity"], "model_id": manifest["model_id"],
          "model_identity": manifest["identity"], "threshold": protocol["threshold"], "datasets": summary,
          "training_or_calibration_on_external_data": False, "official_test_accessed": False,
          "interpretation": "Zero-shot domain transfer; new to the fitted supervised heads, not a guarantee of unseen pretrained-backbone exposure or physical independence."})
    write(ROOT / "verification.json", {"protocol_identity": protocol["identity"], "verifier_sha256": sha256(Path(__file__)),
          "original_and_canonical_image_hashes_verified": raw_hashes, "independent_ensemble_scores_and_flags_verified": arithmetic,
          "all_expected_images_accounted_for": True, "inventory_labels_and_mask_hashes_verified": True,
          "ksdd2_training_overlap_exclusions": excluded, "model_and_numerical_hashes_unchanged": True,
          "same_session_audit_not_external_certification": True})
    export = REPO / "docs/research/external-transfer"; export.mkdir(exist_ok=False); files = {}
    for path in sorted(ROOT.glob("*")):
        if path.is_file() and path.suffix in (".json", ".log", ".py"):
            shutil.copyfile(path, export / path.name)
            files[path.name] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    write(export / "export-index.json", {"files": files, "excluded": "Original images and large archives remain local; hashes and source provenance preserved."})
    print("EXTERNAL EVIDENCE EXPORTED", len(files), flush=True)


if __name__ == "__main__": main()
