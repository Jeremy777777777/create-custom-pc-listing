# Product image specification

Apply [confirmed-catalog-defaults.md](confirmed-catalog-defaults.md) as the single policy authority. All images accurately depict the verified base computer. Use current product-fact records, commercial-use source evidence and the approved style lock; historical gallery files are excluded from ordinary runs; consult only for an explicitly requested historical comparison, never for current QA or approval.

## Deliverables and ownership

### Amazon-based size policy — user decision 2026-10-05

The user removed the fixed 2000×2000 rule for all Listing images. Use the [Amazon US Product image guide](https://sellercentral.amazon.com/help/hub/reference/external/G1881?locale=en_us), checked 2026-10-05:

- Hard pixel requirement: longest side 500–10,000 pixels, inclusive. Square shape and identical dimensions across slots are not required by this general rule.
- Recommendation, not a hard gate: longest side 1,000+ pixels for customer experience and zoom. Record zoom eligibility by size separately from acceptance.
- Use clear, non-pixelated images with no jagged edges. Do not artificially enlarge small images merely to satisfy a number. Preserve native dimensions when usable; normalization/resizing is opt-in and must not upscale or distort the product.
- Amazon supports JPEG, PNG, TIFF and non-animated GIF and recommends JPEG/RGB. Our existing JPG/PNG slot names, opaque backgrounds and sRGB export convention remain workflow conventions, not claims that Amazon bans other supported formats. The guide also specifies at least 72 dpi: inspect export metadata before publication; missing metadata is a review item, not proof of compliance. DPI does not add pixel detail.
- Before publication, check current marketplace/category/account requirements. Use MAIN-specific white background, accurate complete product, product fill and no added marketing overlays requirements; enhanced MAIN candidates are not automatically eligible. All images must accurately depict the sold product and avoid prohibited claims/marks. Apply relevant AI-person metadata disclosure when needed.

`check_image_size` verifies only decoded pixel dimensions. It does not establish clarity, truthful hardware/features, licensing, DPI, or Amazon acceptance. Keep those reviews and existing hash-bound evidence gates. This change does not clear quarantined galleries, overwrite styles, approve generated replacements through the size policy, or retroactively certify older images. It supersedes older fixed-resolution wording; retain historical production receipts as records rather than editing their original claims.

Measure masks, logo bounds and thumbnail readability against each actual canvas. Record per-slot width/height in reports; never infer a 2000px canvas from an old recipe.

All 11 final images meet the Amazon-based size policy below, using sRGB, high-quality JPG/PNG with readable 100% and 200px views. Do not stretch the chassis, invent ports/keys, upscale deficient source detail or crop the product. Original angle photos and AI-faithfully-reproduced product views must match the actual exact model/color and preserve factory marks. Apply [faithful-product-reproduction.md](faithful-product-reproduction.md): visible keyboard/port/geometry differences or unverified details cannot pass, and require correction, sourcing or original-photo fallback. Non-square composition is fit proportionally to canvas; only crops that preserve all product content are allowed.

| File | Required content |
| --- | --- |
| MAIN-STRICT.jpg | Pure white, complete actual computer, no added text/graphics/Windows asset or accessories |
| MAIN-ENHANCED-FRONT-CANDIDATE.png | Accurate front computer, approved screen scene and one audience-specific Windows identity |
| MAIN-ENHANCED-THREE-QUARTER-CANDIDATE.png | Accurate sourced angle with independent fit; one audience-specific Windows identity |
| PT01.png | High-level conversion reason; no Windows asset/full spec grid |
| PT02.png | Relevant original use scene; only computer as device |
| PT03.png | Sole complete base CPU/GPU/RAM/SSD/OS page |
| PT04.png | Display and overall form, not keyboard/touchpad or ports |
| PT05.png | Task relationship, not duplicated specification page |
| PT06.png | White-background keyboard/touchpad/input details, no packout |
| PT07.png | One unused verified value; no seller warranty/service advertising |
| PT08.png | Physical port map and accurate connectivity, no external devices |

Laptop PT08 shows both actual sides where both contain ports, with leaders ending on real connector openings and exact type/count/function labels. Do not use generic icons as a substitute for physical views. For other form factors show relevant front/back surfaces. Missing official reference evidence for the visible angle/details blocks that specific output. AI may faithfully reproduce a supported view under faithful-product-reproduction.md; do not generate plausible unseen hardware.

## Screen and brand controls

Business front defaults to lockup and angle to package; distinct modes may swap for safe fit. Gaming/Student/General use package on both. Use approved fixed assets or documented deterministic lockup crop containing mark plus full Windows 11 Pro text; never generated or retyped approximations. Each asset appears once, full aspect ratio, entirely LCD-contained including its glow/shadow. Background remains continuous with no placeholder rectangle. PT01 and MAIN-STRICT contain none; Business PT03 may use one OS-line lockup.

Enhanced exterior is pure white and neutral contact shadow. Business marketing graphics stay LCD-contained. Gaming only allows the approved HEAD_ONLY/TOP exception from catalog policy; six graphical cards, words, logos and effects stay LCD-contained. Gaming front defaults to SCREEN_ONLY with the current accepted-reference hierarchy and natural aspect-aware margins; old head-breakout/top-clearance ranges apply only to separately approved variations. Angles follow their own measured recipe. Layered production requirements are in [gaming-main-reproducible-workflow.md](gaming-main-reproducible-workflow.md).

Additional OEM logos are required in each PT, outside the computer silhouette; approved transparent asset, original visible geometry/colors, catalog spacing/thumbnail measurements, schema 3 current asset/master/final hashes. Never remove authentic factory chassis marks. Generated logo-free masters preserve existing genuine product marks. No old badge, placeholder or second logo remains beneath the deterministic overlay. Generic neutral-background removal may only flood-fill verified background connected to the edges and must preserve the artwork; prefer genuine transparent originals.

People require seller-owned/licensed/original synthetic sources. No real identity/endorsement, protected game character or copied software UI. Synthetic photoreal people follow applicable `contains-synthetic-performer` metadata rules and manual face/hand/contact QA. Only neutral scene context is allowed, without extra device/accessory depictions.

## Review and status

Use [style-approval-gate.md](style-approval-gate.md), [supporting-gallery-styles.md](supporting-gallery-styles.md) and [final-image-delivery-contract.md](final-image-delivery-contract.md). Save slot fact ownership, semantic metric/manual rationale, 100% and 200px visual checks, LCD masks/protected zones, source licenses and current file hashes. Manual review records must be bound to the actual final hashes; automatic scripts cannot assert visual or license PASS. Any edited output invalidates its corresponding reports. Keep full-gallery QA, delivery verification and Amazon MAIN eligibility separate.

## Current recipe and desktop applicability

Use [production-recipes.md](production-recipes.md) for slot layouts, layer requirements and rebuild procedure. Read the current product style-lock.json first; preserve approved direction while rebuilding missing recipes, without inheriting old QA. Universal LCD/SCREEN_ONLY and lockup/package instructions above apply to integrated-screen computers. Standalone towers/SFF/mini PCs use the catalog policy's DESKTOP_GRAPHIC_SAFE_ZONE exception with package/package, accurate chassis layers and an approved versioned safe-zone recipe; no monitor, invented LCD or head breakout.

## Current Gaming reference — 2026-10-02

For Gaming enhanced MAIN, apply [gaming-approved-main-fit.md](gaming-approved-main-fit.md) before any older generic head-breakout, top-clearance or reference-exclusion instructions. SCREEN_ONLY six-card composition is now the integrated-screen default; HEAD_ONLY is an optional separately approved variation. The exact VL-1221 front supplied and approved by the user is a hash-bound 1237×937 import exception, not a full-gallery PASS or a reusable exception for other files. New generations follow the current Amazon-based size policy in image-spec.md and independently verified product facts.
