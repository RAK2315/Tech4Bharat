"""Registered fixed-model inference on new external datasets, with no tuning."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import io
import json
from pathlib import Path
import sys
import time

import numpy as np
from PIL import Image, ImageOps
import psutil

from component_inspector.vision.ksdd2_ensemble import (
    DEFAULT_BUNDLE, DEFAULT_MANIFEST, Ensemble, PROJECT, read_manifest, sha256, verify_bundle,
)
from component_inspector.vision.media import MediaError, decode_media
from component_inspector.vision.resources import run_bounded

ROOT = PROJECT / "outputs/external-transfer-20261023"
REPO = PROJECT.parent
DATASETS = ("magnetic", "ksdd1", "dagm1")


def read(path): return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, data):
    with Path(path).open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(data, stream, indent=2, sort_keys=True, allow_nan=False); stream.write("\n")


def digest(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def pixel_hash(image):
    return hashlib.sha256(json.dumps((image.height, image.width, 3)).encode() + image.tobytes()).hexdigest()


def mask_info(path, size, *, require_binary):
    with Image.open(path) as image:
        assert image.size == size
        pixels = np.asarray(image.convert("L"))
        values = np.unique(pixels)
        binary = set(values).issubset({0, 255})
        if require_binary: assert binary, "Nonbinary fine mask"
    return {"mask_path": str(path), "mask_sha256": sha256(path),
            "mask_nonempty": bool(pixels.any()), "mask_area_fraction": float((pixels > 0).mean()),
            "mask_is_binary_0_255": binary, "mask_unique_value_count": len(values)}


def source_images(dataset):
    if dataset == "magnetic":
        base = ROOT / "raw/magnetic"
        categories = {"MT_Blowhole", "MT_Break", "MT_Crack", "MT_Fray", "MT_Free", "MT_Uneven"}
        rows = []
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in (".jpg", ".jpeg", ".bmp"):
                continue
            found = categories.intersection(path.parts)
            if not found: continue
            assert len(found) == 1 and path.parent.name == "Imgs"
            category = found.pop(); mask = path.with_suffix(".png")
            assert mask.is_file(), "Missing paired magnetic mask"
            rows.append((path, int(category != "MT_Free"), category, mask))
        assert len(rows) == 1344 and sum(r[1] for r in rows) == 392
        return rows
    if dataset == "ksdd1":
        base = ROOT / "raw/ksdd1"
        rows = []
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in (".bmp", ".png", ".jpg"):
                continue
            if path.stem.endswith("_label"): continue
            mask = path.with_name(path.stem + "_label.bmp")
            assert mask.is_file(), "Missing KSDD1 fine mask: " + str(path)
            with Image.open(mask) as im: label = int(np.asarray(im.convert("L")).any())
            rows.append((path, label, "defect" if label else "normal", mask))
        assert len(rows) == 399 and sum(r[1] for r in rows) == 52
        return rows
    assert dataset == "dagm1"
    rows = []
    for suffix, label in (("normal", 0), ("defect", 1)):
        base = ROOT / f"raw/dagm1-{suffix}"
        paths = sorted(p for p in base.rglob("*") if p.is_file() and p.suffix.lower() in (".png", ".bmp"))
        assert len(paths) == (150 if label else 1000)
        rows.extend((path, label, suffix, None) for path in paths)
    return rows


def inventory():
    acquisition = read(ROOT / "acquisition-complete.json")
    assert all(acquisition["sources"].values()), "Preserve unavailable source; do not silently change datasets"
    manifest = read_manifest(); verify_bundle(DEFAULT_BUNDLE, manifest)
    training = read(PROJECT / "outputs/recall-round1/manifest.json")
    assert len(training["records"]) == 2331 and all(r["official_split"] == "train" for r in training["records"])
    original_encoded = {r["hashes"]["sha256"] for r in training["records"]}
    original_decoded = {r["hashes"]["decoded_sha256"] for r in training["records"]}
    (ROOT / "canonical").mkdir(exist_ok=False)
    all_rows = []; seen = defaultdict(list); inputs = {d: [] for d in DATASETS}; exclusions = []
    for dataset in DATASETS:
        directory = ROOT / "canonical" / dataset; directory.mkdir()
        rows = []
        for path, label, category, mask in source_images(dataset):
            relative = path.relative_to(ROOT / "raw").as_posix()
            identity = dataset + ":" + hashlib.sha256(relative.encode()).hexdigest()
            with Image.open(path) as image:
                assert image.width * image.height <= 20_000_000 and getattr(image, "n_frames", 1) == 1
                original_format = image.format
                rgb = ImageOps.exif_transpose(image).convert("RGB"); rgb.load()
                decoded = pixel_hash(rgb)
                canonical = directory / (identity.split(":")[1] + ".png")
                rgb.save(canonical, format="PNG")
                with Image.open(canonical) as check: assert pixel_hash(check.convert("RGB")) == decoded
                row = {"id": identity, "dataset": dataset, "label": label, "category": category,
                       "source_relative": relative, "original_path": str(path), "original_sha256": sha256(path),
                       "decoded_sha256": decoded, "original_format": original_format, "width": rgb.width, "height": rgb.height,
                       "canonical_path": str(canonical), "canonical_sha256": sha256(canonical)}
                if mask: row.update(mask_info(mask, rgb.size, require_binary=dataset == "ksdd1"))
            overlap = row["original_sha256"] in original_encoded or decoded in original_decoded
            row["excluded_ksdd2_train_overlap"] = overlap
            rows.append(row); seen[decoded].append(identity)
            if overlap: exclusions.append({"id": identity, "reason": "Encoded or decoded KSDD2 TRAIN overlap"})
            else: inputs[dataset].append({"id": identity, "image_path": str(canonical), "sha256": row["canonical_sha256"]})
        write(ROOT / f"inventory-{dataset}.json", {"rows": rows})
        write(ROOT / f"inference-{dataset}.json", {"rows": inputs[dataset]})
        all_rows.extend(rows)
        print("INVENTORIED", dataset, len(rows), Counter(r["label"] for r in rows), flush=True)
    duplicate_groups = [ids for ids in seen.values() if len(ids) > 1]
    anomalies = [{"id": r["id"], "category": r["category"], "label": r["label"], "mask_nonempty": r["mask_nonempty"]}
                 for r in all_rows if "mask_nonempty" in r and bool(r["label"]) != r["mask_nonempty"]]
    write(ROOT / "inventory-audit.json", {"ksdd2_train_records_compared": 2331, "official_test_images_accessed": False,
           "overlap_exclusions": exclusions, "exact_decoded_duplicate_groups": duplicate_groups,
           "mask_vs_category_disagreements": anomalies, "all_canonical_pixels_equal_original_rgb": True,
           "note": "Category truth retained for magnetic; empty defect mask does not relabel or remove an image."})
    import component_inspector.vision.ksdd2_ensemble as adapter
    source_files = [Path(__file__), PROJECT / "tools/acquire_external_transfer.py",
                    PROJECT / "tools/verify_external_transfer.py", PROJECT / "tests/test_external_transfer_audit.py",
                    Path(adapter.__file__), PROJECT / "src/component_inspector/vision/geometry.py",
                    PROJECT / "src/component_inspector/vision/media.py", PROJECT / "src/component_inspector/vision/resources.py",
                    PROJECT / "requirements-recall.lock", DEFAULT_MANIFEST, REPO / "docs/research/2026-10-23-external-transfer-protocol.md"]
    frozen_files = [*ROOT.glob("acquisition*.json"), *ROOT.glob("inventory*.json"), *ROOT.glob("inference*.json")]
    protocol = {"created_utc": datetime.now(timezone.utc).isoformat(), "model_identity": manifest["identity"],
                "model_id": manifest["model_id"], "threshold": manifest["calibration"]["threshold"], "datasets": list(DATASETS),
                "source_sha256": {str(p.resolve()): sha256(p) for p in source_files},
                "input_sha256": {str(p.resolve()): sha256(p) for p in frozen_files},
                "bundle_sha256": {str((DEFAULT_BUNDLE / name).resolve()): entry["sha256"] for name, entry in manifest["files"].items()},
                "numerical_versions": manifest["numerical_versions"], "new_training_or_calibration": False,
                "official_test_access": False, "source_model_selection_changed": False}
    protocol["identity"] = digest(protocol); write(ROOT / "protocol.json", protocol)
    write(REPO / "docs/research/2026-10-23-external-transfer-preregistration.json", protocol)
    print("FROZEN EXTERNAL TRANSFER", protocol["identity"], flush=True)


def guard():
    protocol = read(ROOT / "protocol.json"); other = dict(protocol); identity = other.pop("identity")
    assert digest(other) == identity
    for collection in ("source_sha256", "input_sha256", "bundle_sha256"):
        for name, expected in protocol[collection].items(): assert sha256(Path(name)) == expected, name
    assert {name: version(name) for name in protocol["numerical_versions"]} == protocol["numerical_versions"]
    return protocol


def score(dataset):
    protocol = guard()
    # No label/mask file is opened here. Inventory hash checks do not decode truth.
    entries = read(ROOT / f"inference-{dataset}.json")["rows"]
    model = Ensemble(); rows = []
    for n, entry in enumerate(entries):
        path = Path(entry["image_path"]); assert sha256(path) == entry["sha256"]
        tick = time.perf_counter()
        try:
            decoded = decode_media(path.read_bytes())
            result = model.predict_image(decoded.image, with_attention=False)
            assert result["model_identity"] == protocol["model_identity"] and result["threshold"] == protocol["threshold"]
            warnings = list(decoded.warnings)
            if not (184 <= decoded.image.width <= 242 and 602 <= decoded.image.height <= 660):
                warnings.append("outside_ksdd2_capture_dimensions")
            row = {"id": entry["id"], "status": "scored", "score": result["score"], "flagged": result["flagged"],
                   "member_logits": result["member_logits"], "warnings": warnings}
        except MediaError as exc:
            row = {"id": entry["id"], "status": "rejected", "score": None, "flagged": None,
                   "reason": str(exc), "status_code": exc.status_code}
        row["elapsed_seconds"] = time.perf_counter() - tick; rows.append(row)
        if n % 100 == 0 or n + 1 == len(entries): print("EXTERNAL SCORE", dataset, n + 1, "/", len(entries), flush=True)
    guard()
    write(ROOT / f"predictions-{dataset}.json", {"protocol_identity": protocol["identity"], "rows": rows,
          "labels_or_masks_read_for_scoring": False, "official_test_accessed": False})


def run():
    protocol = guard()
    for dataset in protocol["datasets"]:
        cap = min(4 * 1024**3, int(.6 * psutil.virtual_memory().available))
        result = run_bounded([sys.executable, str(Path(__file__).resolve()), "score", "--dataset", dataset],
                             ROOT / f"score-{dataset}-worker.log", max_rss_bytes=cap, max_seconds=1800)
        write(ROOT / f"score-{dataset}-resources.json", result); print(dataset, result, flush=True)
        if result["status"] != "completed": raise RuntimeError("Preserve failed external inference phase")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=["inventory", "score", "run"])
    parser.add_argument("--dataset", choices=DATASETS)
    args = parser.parse_args()
    if args.phase == "inventory": inventory()
    elif args.phase == "score":
        assert args.dataset; score(args.dataset)
    else: run()


if __name__ == "__main__":
    if sys.platform == "win32":
        import ctypes
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.SetThreadExecutionState.argtypes = [ctypes.c_uint]
        kernel.SetThreadExecutionState.restype = ctypes.c_uint
        if not kernel.SetThreadExecutionState(0x80000001): raise ctypes.WinError(ctypes.get_last_error())
        try: main()
        finally: kernel.SetThreadExecutionState(0x80000000)
    else: main()
