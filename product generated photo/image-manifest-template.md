# VL-<internal-ID> image manifest

Use [current catalog policy](../references/confirmed-catalog-defaults.md). This template records current production evidence; do not fill PASS by copying a prior product. Final dimensions follow [image-spec.md](../references/image-spec.md); current product-fact record wins over historical workbooks/images.

## Product and approved style

```yaml
policy_version: 2026-10-02
internal_product_id: VL-XXXX
configuration_scope: BASE_ONLY
product_fact_record: <current path + SHA-256>
oem_brand: <verified>
exact_model_color: <verified>
final_os: Windows 11 Pro
retail_media_included: false
image_size: [ACTUAL_WIDTH, ACTUAL_HEIGHT] # decoded output dimensions, per slot if mixed
audience_style_family: <GAMING|BUSINESS_WORK|STUDENT_STUDY|GENERAL>
image_style_profile: <profile>
hero_style_id: <Gxx|Bxx|neutral ID>
supporting_gallery_pack: <GGxx|BGxx|NEUTRAL>
gaming_core_layout_id: <Cxx|NOT_APPLICABLE>
gaming_asset_card_style_id: <Axx|NOT_APPLICABLE>
style_approval_status: <APPROVED|PROPOSED>
approval_source_timestamp: <actual approval reference>
recipe_path_hash: <versioned recipe and hash>
form_factor: <LAPTOP|AIO|STANDALONE_DESKTOP>
main_content_boundary: <SCREEN_ONLY|HEAD_ONLY_FRAME_BREAK|DESKTOP_GRAPHIC_SAFE_ZONE>
enhanced_main_outer_background: PURE_WHITE
gaming_breakout_edge: <TOP|NOT_APPLICABLE>
gaming_breakout_parts: <HEAD_ONLY|NONE>
gaming_product_width_pct: <actual measured fit; current reference approximately97-100, no clipping>
gaming_top_clearance_pct: <actual aspect-aware margins; no mandatory8-10 in SCREEN_ONLY>
layered_production_pack: <actual files or NOT_READY; flat PNG is not sufficient>
current_gaming_reference: assets/gaming-main-reference/vl1221-amazon-approved-20261002/approved.png
user_approved_exact_import_exception: <receipt path or NOT_APPLICABLE>
enhanced_front_windows_asset_mode: <integrated-screen Business LOGO_LOCKUP; otherwise PACKAGE>
enhanced_three_quarter_windows_asset_mode: PACKAGE
windows_asset_placement: <SCREEN_SAFE_ZONE|DESKTOP_GRAPHIC_SAFE_ZONE>
windows_package_asset: assets/branding/windows-11-pro-package.png
windows_lockup_source_recipe_rights: <fixed asset or deterministic complete mark+text derivative>
logo_qa_schema_version: 3
logo_visibility_mode: <STANDARD|ASPECT_RATIO_WORDMARK>
logo_minimum_component_separation_px: ACTUAL_GAP # max(32, ceil(min(width,height)*0.025))
logo_maximum_visible_long_edge_percent: 12
thumbnail_size_px: 200
logo_minimum_visible_long_edge_at_thumbnail_px: 20
logo_minimum_visible_short_edge_at_thumbnail_px: <10 or20/visibleAspectRatio>
```

## Source and layering ledger

| Asset | Source URL/date | Exact model/color | Original dimensions/hash | Commercial-use evidence | Layer/mask path/hash |
| --- | --- | --- | --- | --- | --- |
| Front computer | | | | | |
| Angle/port/input photos | | | | | |
| OEM/CPU/GPU/Windows marks | | | | | |
| Original scene/subject/card skins | | | | | |

Record synthetic/licensed-person source and required metadata, LCD/product/head masks and each graphical card's usable/icon/text bounds, z-order and effect bounds. No additional devices/accessories appear.

## Slot plan and current final evidence

| Slot | Unique primary information | Exact source/asset | Canonical fact IDs | Final SHA-256 | 100%/200px manual review |
| --- | --- | --- | --- | --- | --- |
| MAIN-STRICT | White-background computer only | | N/A | | |
| MAIN-ENHANCED-FRONT-CANDIDATE | Approved front hero and Windows identity | | | | |
| MAIN-ENHANCED-THREE-QUARTER-CANDIDATE | Accurate angle hero and Windows identity | | | | |
| PT01 | Distinct high-level reason; no Windows overlay | | | | |
| PT02 | Use scene, computer only | | | | |
| PT03 | Full base CPU/GPU/RAM/SSD/OS | | | | |
| PT04 | Display/overall form | | | | |
| PT05 | Hardware/task relationships | | | | |
| PT06 | Keyboard/touchpad/input on white | | | | |
| PT07 | Remaining verified value, no seller warranty advertising | | | | |
| PT08 | Real physical port map and connectivity | | | | |

## Semantic and final QA

| PT pair | Shared primary fact IDs | Smaller fact count | Metric or MANUAL_REVIEW rationale | Result |
| --- | --- | --- | --- | --- |
| <all28 pairs> | | | | |

Numeric overlap uses shared/min counts, fails above20%; zero-count/unreliable mapping uses honest manual review, no invented percentage. Equivalent claims share fact IDs; exclude only identity/navigation. Keep slot unique contributions explicit.

- Actual source/rights and exact hardware reviewed; authentic factory marks preserved.
- All11 current files, sizes, hashes and required manual reviews verified, including MAIN.
- Logo alpha-visible bounds/spacing, protected silhouettes and current source/master/final hashes checked in schema3.
- Integrated-screen Windows assets/glow/shadow remain LCD-contained, one per enhanced MAIN; Business modes differ. Standalone desktop uses approved protected-chassis graphic safe zones and package/package, never a fabricated monitor/LCD.
- Integrated-screen Gaming only HEAD_ONLY/TOP, all six card contents/effects in LCD; desktop has no head breakout. Frozen layered production pack actually exists.
- No extra products/accessories, old placeholders, duplicated overlays or unverified claims.
- Material style approval and actual current-hash fidelity review recorded.

Statuses: `WORKBOOK_STRUCTURE`, `FACT_COMPLETENESS`, `STYLE_FIDELITY`, `FULL_GALLERY_QA`, `AMAZON_MAIN_ELIGIBILITY`, `GITHUB_DELIVERY` remain separate. Changed files invalidate prior reviews. Record local checks → pushed commit → applicable CI → remote file-hash verification; requested same-slot replacement needs no redundant approval.
