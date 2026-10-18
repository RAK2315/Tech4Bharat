# Stage 1 source ledger — 18 October 2026

Stage 1 software is implemented. The two-dataset readiness gate remains blocked
by MVTec access. No role allocation, model fitting or evaluation occurred.
Machine-readable source records: [STAGE1_SOURCES.json](STAGE1_SOURCES.json).

| Dataset | Official source and access | Actual local result |
|---|---|---|
| MVTec AD `metal_nut` | [MVTec](https://www.mvtec.com/research-teaching/datasets/mvtec-ad), currently “Fill in the form” | `blocked_access`, CLI exit 3; zero dataset bytes acquired |
| KSDD2 | [ViCoS](https://www.vicos.si/resources/kolektorsdd2/), public [download](https://go.vicos.si/kolektorsdd2) redirects to `https://data.vicos.si/datasets/KSDD/KolektorSDD2.zip` | Acquired, CLI exit 0; hashes verified on reuse |

MVTec action: personally complete the provider's form and any required terms only
if acceptable, obtain the `metal_nut` category archive, then supply its local path
for `acquire --dataset mvtec_ad --category metal_nut --archive PATH`. No form,
account, CAPTCHA or terms acceptance was automated. No mirror was substituted.
No archive checksum/size/release taxonomy is claimed for MVTec before acquisition.
A supplied local archive is explicitly labelled unverified provider identity:
self-computed SHA256 alone does not authenticate the original provider.

KSDD2 retrieval completed **2026-10-18 14:30:15 IST** (09:00:15 UTC).
Provider Last-Modified: 28 September 2023 10:40:04 UTC; this is not a release ID.

- Download: **853,126,555 bytes** (~813.61 MiB).
- SHA256: `edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8`.
- Extraction: **852,612,567 bytes**, **6,677 files**.
- Archive + extracted logical bytes: **1,705,739,122** (~1.589 GiB), excluding
  manifest bytes, caches and filesystem allocation overhead.
- Layout inventory: `train/` 4,664 files; `test/` 2,008 files;
  five root `split_weakly_*.pyb` files. The latter remain inert bytes.
- One training sample decoded via Pillow 12.1.0: `train/10000.png`, RGB PNG,
  **229×645**. No test image was displayed or decoded for model design.
- The provider publishes 2,331 training images and 1,004 test images. The archive
  has 4,664 training files; image/mask pairing, label/count reconciliation and
  quarantine decisions remain stage 2 work. Do not infer audited counts yet.
- No provider-published checksum was verified; this hash identifies acquired bytes.

Ignored local evidence paths (relative to `components/`):

```text
data/archives/edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8.zip
data/raw/ksdd2/
data/manifests/ksdd2_source.json
data/manifests/mvtec_metal_nut_source.json
data/manifests/ksdd2_edcdb486809b24f1d17b785e30c52fafc5999554dd5fe18ddf77b61ceb6f36a8_inventory.json
```

The inventory includes relative path, byte count and SHA256 for every regular file.
Its own SHA256 is `8c6e47dbd3b8e6ac76c695725f84c66a45dc40dd043106de040eb44ec0d20547`.
Raw files are operationally immutable: acquisition does not overwrite them; reuse
verifies hashes and membership. This is not an OS-enforced write-protection claim.

Both source pages specify [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
Retain appropriate credit, the licence link and change notices; NonCommercial and
ShareAlike apply. Public access does not establish commercial permission. This
build is local research; no raw images were committed or published. Before public
hackathon/demo redistribution, review the exact use and content; no commercial
rights or endorsement are claimed. No separate personal terms were accepted.

Attribution:

- MVTec Software GmbH; Paul Bergmann, Michael Fauser, David Sattlegger and
  Carsten Steger, *MVTec AD — A Comprehensive Real-World Dataset for Unsupervised
  Anomaly Detection*, CVPR 2019. Confirm any supplied archive notices on import.
- Kolektor Group (images/annotations); Jakob Bozic, Domen Tabernik and Danijel
  Skocaj, *Mixed supervision for surface-defect detection: from weakly to fully
  supervised learning*, Computers in Industry, 2021, as requested by ViCoS.

The [official layout documentation](https://github.com/vicoslab/mixed-segdec-net-comind2021/blob/master/datasets/README.md)
was inspected as text. Its download/extraction script was not executed: our
bounded extractor replaces unrestricted `extractall` and untrusted pickle loading.
