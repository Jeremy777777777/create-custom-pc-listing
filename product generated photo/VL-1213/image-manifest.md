# VL-1213 current image manifest

## Product, policy and approval

- Internal ID: VL-1213. Input ASIN B0HC4D4X9M explicitly linked by ERP product 31213, listing 115154069; current physical child PL-1254.
- Base used in PT03: Intel Core Ultra 7 265H / NVIDIA RTX PRO 2000 Blackwell Generation 8GB GDDR7 / 64GB DDR5 / 1TB internal SSD / Windows 11 Pro. SSD capacity is decimal nominal, not usable GiB.
- Policy baseline: 2026-10-02 plus active amendments. Scope: IMAGE_ONLY_WORKFLOW, computer only, full 11-image gallery. No workbook stage created.
- Approved B15 / BG15 Architectural Precision, Business/Work audience supported by OEM professional workstation positioning and ERP hardware. Direct user approval “批准” followed the labeled product-specific preview in this chat on 2026-10-16. Approval establishes direction, not automatic QA.
- Palette: graphite, cool gray, navy, restrained icy blue. Geometry and exact source hashes: `production-v1/recipe.json`, `production-v1/sources.json` and `logo-placement.json`.
- Catalog-wide OEM authorization: USER_CONFIRMED_CATALOG_WIDE, holder MegaPC / J-Tech Digital, accurate product merchandising. Original Lenovo logo from https://media.lenovobrandworld.fiestic.com/2022/06/08010946/LenovoLogo_POS-Red-H.png, official Brand World page https://brandworld.lenovo.com/visual-identity/logo/ . Red containing shape, white customized wordmark, proportions and colors preserved. Transparent margin added around the original artwork; no logo redrawn.

## Sources and layers

Official model gallery: https://psref.lenovo.com/Product/ThinkPad/ThinkPad_P16v_Gen_3_Intel . Its seven downloaded PNGs are native 2000×1200. Official Lenovo product page: https://www.lenovo.com/us/en/p/LEN101T0145 . The accurate angle reference is native 584×584 with transparent margins; its final canvas is 640×540 without product enlargement. Native source identities and hashes are in the source ledger; input details are a losslessly rotated/cropped CT2_06 image, physical connectors are CT2_01/02 detail crops. As-built current-unit inspection confirmed US English black backlit numeric keyboards (5N21Q49827 / 5M11T54117) and 90Wh battery (5B11M90137); serial and private lookup URL excluded from public delivery.

Hardware method is ORIGINAL_PHOTO in every final slot. AI-created product drawings from the style board are not used. The original factory silhouette, input, hinges, camera bump, finishes and ThinkPad marks are retained. Permitted changes are edge-connected neutral matte extraction, neutral floor-shadow cleanup outside the physical base, proportional downscaling, lossless crop/rotation, original LCD replacement and deterministic composition. Every visible product view was compared to its source; non-visible details are explicitly marked in the visual notes.

ImageGen created three original scene assets, with exact prompts in `production-v1/generation-prompts.json`. No protected person/game/app imagery, peripherals or paid-software claims. All product pixels originate in official references. Native accepted layers are frozen under `production-v1/layers/`. The Windows package and lockup sources are fixed repository assets; the transparent lockup is a documented deterministic extraction of the same complete white mark and wording, not retyped text. Front uses LOGO_LOCKUP; angle uses PACKAGE once, original aspect ratio and no perspective deformation. All Windows pixels and architectural MAIN content remain within actual LCD polygons; `boundary-check.json` compares final pixels outside LCD with the original source on the same white canvas.

## Ownership and reviews

| Slot | Unique information | Current-byte evidence |
|---|---|---|
| MAIN-STRICT | White/product only | final-image-qa.json / visual-review.json |
| Enhanced front | LCD architecture + Windows lockup | Same plus boundary-check.json |
| Enhanced angle | Actual angle + distinct fixed Windows package | Same plus native-detail limitation |
| PT01 | Professional purchase positioning | visual-review.json / semantic-review.json |
| PT02 | Neutral architectural workspace context | Same; no extra electronic device |
| PT03 | Sole complete base configuration | Same; CPU/GPU/VRAM/RAM/SSD/OS |
| PT04 | 16-inch WUXGA, 16:10, IPS, anti-glare, non-touch | Same; no unverified brightness/gamut |
| PT05 | Model → visualize → refine relationship | Same; original schematic, no app entitlement |
| PT06 | White original US keyboard/TrackPoint/touchpad/numpad | Same; exact original key pixels |
| PT07 | 90Wh + conditional Rapid Charge | Same; no runtime/warranty/spec recap |
| PT08 | Both physical connector regions + Wi-Fi/Bluetooth existence | Same; optional openings excluded |

Actual assistant multimodal inspection covered native outputs and an actual 200px thumbnail sheet. Main headlines, primary hierarchy, product and OEM identity are recognizable at 200px. Detailed port labels, secondary GPU wording and the charging-condition footnote are intended for full-size reading; the review does not pretend every small line remains legible in a 200px image. No separate human certification or Amazon acceptance is claimed.

All 28 PT pairs were reviewed. `production-v1/semantic-pairs.json` records disjoint selected factual ownership when both have nonzero canonical fact sets; narrative-only/zero-denominator pairs use explicit MANUAL_REVIEW with no fabricated overlap percentage. Identity/navigation is excluded; equivalent factual claims retain the same ID.

OEM overlay: original alpha-visible artwork, visible 168×56px on 1536×1024; at 200px, long edge 21.875px and short edge about 7.29px, matching the >2.4 aspect-ratio wordmark branch. Canvas long-edge share 10.94%, measured edge/product/protected-text clearance enforced by the shared geometry function. Final source/master/image hashes are in schema-3 logo QA, not copied from an older gallery.

Local status: actual image inspection and automated structural/geometry acceptance are separate. Actual repeated deterministic render produced 11/11 identical MAIN/unbranded-master hashes. Current final hashes, decoded formats, sizes and review binding are in `final-image-qa.json`. The general size policy is met; enhanced angle does not meet the optional 1000px zoom recommendation. RGB JPEG and opaque RGB/RGBA PNG exports; initial masters exported at 96dpi (PT finalizer omits DPI metadata, requiring publication metadata check).

GitHub delivery is verified separately after local checks, selective push and applicable remote CI; no source serial, environment binaries, credentials or private research output is included. Amazon MAIN eligibility remains NOT_ASSESSED.
