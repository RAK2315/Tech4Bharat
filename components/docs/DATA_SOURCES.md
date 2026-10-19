# Current sources - cable gland and KSDD2

Active scope: [RGB-only cable gland + KSDD2](CABLE_GLAND_SCOPE.md).
Both sources are acquired, not audited/split. Original metal-nut access is
**deferred**, not a blocker for the replacement recipe. Its record below is
historical and retained for provenance. The cable-gland local-import details
appear at the end of this ledger; provider identity remains unverified.
Current experimental roles are defined in the scope amendment and execution
plan, superseding the older next-action paragraphs below.

---

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


## Cable-gland acquisition - 18 October 2026

User-supplied archive: `C:\Users\laksh\Downloads\cable_gland.tar.xz`.
Official source: https://www.mvtec.com/research-teaching/datasets/mvtec-3d-ad .
Status: acquired, not audited or split; separate identity `mvtec_3d_ad/cable_gland`.
Local import completed 2026-10-18T16:36:48.457546+00:00 (22:06:48 IST).
Original download time, exact download URL and provider release ID are unknown.

Archive bytes: 354399396. SHA256:
`63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed`.
Content-addressed copy under components:
`data/archives/63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed.tar`.
The existing importer stores TAR-family archives with a .tar suffix; the bytes
remain XZ-compressed and unchanged. Actual format is detected from content.
Raw root: `data/raw/mvtec_3d_cable_gland/cable_gland/`.
Inventory: 820 regular files, 759081950 extracted bytes; inventory SHA256:
`7e3f5e22b18edc9c3e9894a402973dbbf05345a8deea30b32e0c9879d707032c`.
Layout counts: 223 training RGB images, 23 validation RGB images, 108 test RGB
images (21 good; 22 cut; 22 hole; 21 bent; 22 thread). This is not a full audit.
Only train/good/rgb/000.png was decoded: RGB PNG, 400 x 400. No test image viewed.
XYZ files remain inert source data. Proposed modelling uses RGB only, not 3D.

Included notices: MVTec copyright 2021, CC BY-NC-SA 4.0. Retain attribution,
licence and changes; no commercial permission claimed or personal terms accepted.
Attribution: Bergmann, Sattlegger, Steger, The MVTec 3D-AD Dataset (VISAPP 2022).
The included readme describes an early review subset. The exact provider download
URL and release/notice reconciliation remain pending before experiment freeze.
No provider checksum verified: self-computed SHA256 identifies acquired bytes,
not provider identity. Import mode: local_archive_unverified_provider_identity.

Importer tests were written first: two new behavior tests failed before support
existed. After adding the separate source/category, CLI and training-RGB selector,
all 58 component tests passed (3.81 s). Command from components:
`.\.venv-p0\Scripts\python.exe -m pytest tests -q --basetemp=.cache/cable-green-1 --tb=short`.
KSDD2 and the historical blocked metal-nut record are preserved. The original
metal-nut protocol is not silently reinterpreted as cable gland. Next: document
replacement RGB-only recipe, data roles and validation handling before Stage 2.
No training, final evaluation, model readiness or complete Stage 2 claim.


Project-local archive copy - 18 October 2026: copied the supplied download to
components/data/archives/cable_gland.tar.xz (354399396 bytes); SHA256 matches
63728f5ab3b37feaa03a796eefd44e572afe74e49b28e8fc3b19ec98838aeaed.
Existing importer-owned archive/raw files and Downloads original were preserved.
Acquire reuse exited 0 after verifying archive/inventory and all 820 raw file
hashes and membership. The extra named copy adds 354399396 storage bytes.
Build/reproduction commands now use the project-local archive; recipe raw paths
remain unchanged. No training or test-image decoding occurred.


## Download-origin recovery - 19 October 2026

The original Downloads archive's Windows Zone.Identifier supplies the exact HostUrl:
https://www.mydrive.ch/shares/45892/8836f2fd7407ec1c54dc165a5b8a2e91/download/428792309-1643274318/cable_gland.tar.xz
No ReferrerUrl was present. This is local browser metadata, not a provider checksum.
The archive's readme/CC-BY-NC-SA-4.0 licence are retained. Its early-review wording
is disclosed alongside matching published category counts (223/23/21/87); no current
provider release identity is claimed. Local research may identify these exact bytes,
while publication remains subject to notice/contents review. No personal form/terms
was submitted or accepted by Codex. See CABLE_GLAND_SOURCE_RECONCILIATION.json.
