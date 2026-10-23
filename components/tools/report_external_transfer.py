"""Render verified external transfer results without changing inference."""
from pathlib import Path
import json


def read(path): return json.loads(Path(path).read_text(encoding="utf-8"))


def percent(value): return "unavailable" if value is None else f"{100 * value:.2f}%"


def main():
    repo = Path(__file__).resolve().parents[2]
    root = repo / "components/outputs/external-transfer-20261023-v2"
    summary = read(root / "summary.json"); verification = read(root / "verification.json")
    assert summary["protocol_identity"] == verification["protocol_identity"]
    audit = read(root / "inventory-audit.json")
    names = {"magnetic": "Magnetic Tile Defects — real tiles, independent provider",
             "ksdd1": "KolektorSDD1 — real surfaces, same provider as KSDD2",
             "dagm1": "DAGM 2007 Class 1 — synthetic textures only"}
    sources = {"magnetic": "https://github.com/abin24/Magnetic-tile-defect-datasets.",
               "ksdd1": "https://www.vicos.si/resources/kolektorsdd/",
               "dagm1": "https://conferences.mpi-inf.mpg.de/dagm/2007/prizes.html"}
    lines = ["# Frozen ensemble on external datasets", "", "Measured 23 October 2026.", "",
             "**Model used:** the same frozen `ksdd2-ensemble-mvp-v1`: three `longer108` "
             "supervised ResNet18-feature heads (seeds 4220/4221/4222), existing confirmation "
             "fold 0. The numeric cutoff remained **0.33108379983608666**, strict greater-than. "
             "No new models were trained; no external normal calibration, threshold search, "
             "orientation selection or adaptation occurred.", "",
             "These datasets were newly acquired for this project and excluded from the supervised "
             "heads' fitting/calibration. This tests transfer to other products/textures, not new "
             "same-line factory performance. Unknown backbone pretraining exposure and physical "
             "product relationships are not ruled out.", "",
             "## Every registered dataset", "",
             "| Dataset | Defects / normals | Defects caught | Effective recall | False alarms / scored normals | False-alarm rate | Scored / all images |",
             "|---|---:|---:|---:|---:|---:|---:|"]
    for dataset in summary["datasets"]:
        row = summary["datasets"][dataset]; counts = row["counts"]; fpr = row["accepted_normal_fpr"]
        lines.append(f'| [{names[dataset]}]({sources[dataset]}) | {row["defects"]} / {row["normals"]} | '
                     f'{counts["TP"]}/{row["defects"]} | {percent(row["recall"]["rate"])} | '
                     f'{counts["FP"]}/{fpr["denominator"]} | {percent(fpr["rate"])} | '
                     f'{row["coverage"]["numerator"]}/{row["originals"]} |')
    lines += ["", "Recall includes rejected defective images as misses. False-alarm rate uses only "
              "scored normal images; rejected normals are neither true negatives nor successful "
              "inspections. Rates must be read with coverage. Dataset results are never pooled.", "",
              "## Technical rejects and annotation accounting", ""]
    for dataset, row in summary["datasets"].items():
        c = row["counts"]
        lines.append(f'- **{dataset}:** {c["rejected_anomalies"]} defective and {c["rejected_normals"]} normal images rejected; '
                     f'reasons: `{json.dumps(row["rejection_reasons"], sort_keys=True)}`. '
                     f'{row["nonbinary_masks"]} nonbinary masks; {row["mask_category_disagreements"]} mask/category disagreements.')
    lines += ["", "Magnetic Tile truth follows the original folder categories: MT_Free is normal; "
              "Blowhole/Break/Crack/Fray/Uneven are defects. Four MT_Uneven images have empty source "
              "masks; all are retained as defective category labels, with the disagreement disclosed. "
              "Grayscale masks are preserved using nonzero support for descriptive area; it is not "
              "pixel-precise ground truth. KolektorSDD1 truth uses nonempty original fine masks. "
              "DAGM uses the original normal/defect archive identities, with all 1,150 Class 1 images; "
              "it is not a full-DAGM result.", "",
              f'The overlap audit compared encoded and shape-plus-decoded RGB hashes with all 2,331 '
              f'original KSDD2 TRAIN images: **{len(audit["overlap_exclusions"])} overlaps excluded**. '
              f'There were **{len(audit["exact_decoded_duplicate_groups"])} exact decoded duplicate groups** '
              'within/across the external sets, recorded in the raw audit. Unknown near-duplicates, '
              'same-item frames and lot dependence are not eliminated by this check. KSDD1 has '
              'multiple views per product; image counts do not imply that many independent products.', "",
              "## Descriptive small-defect slice", "",
              "Only defective images with a nonempty supplied mask occupying <=0.5% of source pixels "
              "are included below. This is exploratory, with no tuning. Magnetic saliency masks make "
              "this size estimate approximate; four empty-mask positive categories are excluded only "
              "from the size slice and remain in the primary defect counts. No pixel recall is claimed.", "",
              "| Dataset | Small images caught / total | Effective small-image recall |", "|---|---:|---:|"]
    for dataset, row in summary["datasets"].items():
        small = row["small_mask_images"]
        lines.append(f'| {dataset} | ' + (f'{small["counts"]["TP"]}/{small["defects"]} | {percent(small["recall"]["rate"])} |'
                     if small else 'unavailable | unavailable |'))
    lines += ["", "## What this means", "",
              "These fixed-cutoff transfer checks define the model's current scope; they do not "
              "establish that it can inspect every component. Strong defect recall with high normal "
              "false alarms would not meet the target. Poor results must not be repaired by tuning "
              "this cutoff on these evaluation labels and calling the result unseen validation. "
              "A different product/camera may need its own data and separately trained/calibrated "
              "recipe, followed by an independent confirmation batch. The exact KSDD2 MVP model "
              "and all previous results remain unchanged.", "",
              "## Verifiable proof and failures", "",
              f'All {verification["original_and_canonical_image_hashes_verified"]} original image and canonical '
              f'PNG hashes/pixels were checked. A separate SciPy calculation reproduced all '
              f'{verification["independent_ensemble_scores_and_flags_verified"]} scored three-member '
              'averages and flags. Manual rejection-aware counts matched the existing evaluation '
              'implementation. Model, manifest, numerical source and input hashes were unchanged. '
              'No official KSDD2 test image was opened. The independent audit is from this session, '
              'not external certification.', "",
              "The first inventory attempt failed a strict-binary annotation assertion before any "
              "prediction: one KSDD1 fine mask has values 0/85/255. The failed source, diagnosis and "
              "partial first-root inventory are preserved. The second inventory retains nonzero-mask "
              "labels, keeps all originals, discloses grayscale masks and uses a new exclusive "
              "output root; no model, label or threshold was selected from outcomes.", "",
              "Original images were decoded, EXIF-corrected and losslessly stored as RGB PNG for "
              "transport, with exact decoded-pixel equality checks. No image was enlarged to evade "
              "the minimum-side rule. Frozen 90-degree rotation and letterbox geometry were unchanged "
              "even for square textures. Every scoring phase used four CPU threads, one ML worker "
              "at a time, at most 1,800 seconds and min(4 GiB,60% free RAM). Resources and elapsed "
              "times are measured logs, not controlled performance benchmarks.", "",
              "The preregistered rules were published before scoring, followed by the full source/"
              "inventory-hash registration before inference. DAGM is synthetic, KSDD1 shares the "
              "Kolektor/ViCoS provider, and Magnetic Tile is a different material/product. "
              "Descriptive exact binomial intervals are in the raw summary, with dependence limits. "
              "No commercial-use or data-redistribution permission is asserted.", "",
              "Evidence: [protocol](2026-10-23-external-transfer-protocol.md), "
              "[frozen registration](2026-10-23-external-transfer-preregistration.json), "
              "[all counts and intervals](external-transfer/summary.json), "
              "[independent verification](external-transfer/verification.json), "
              "[inventory audit](external-transfer/inventory-audit.json), "
              "[failed inventory attempt](external-transfer/inventory-attempt-1-failure.json), "
              "[failed source](external-transfer/inventory-attempt-1-source.py), "
              "[export hashes](external-transfer/export-index.json).", ""]
    path = repo / "docs/research/2026-10-23-external-transfer-results.md"
    with path.open("x", encoding="utf-8", newline="\n") as stream: stream.write("\n".join(lines))
    print(path)


if __name__ == "__main__": main()
