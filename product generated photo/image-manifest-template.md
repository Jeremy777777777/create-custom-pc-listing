# VL-<internal-model> Image Manifest

## Product and style lock

- Internal model: `VL-<internal-model>`
- Exact sold product: `<brand, model, form factor, color>`
- Exact configuration / selectable tiers: `<verified values>`
- `image_style_profile`: `<navy-technical-v1 | feature-led-studio-v1>`
- Profile reason: `<why this profile fits the verified product and licensed assets>`
- `audience_style_family`: `<GAMING | BUSINESS_WORK | STUDENT_STUDY | GENERAL | HYBRID_MANUAL_REVIEW>`
- Audience evidence / confidence / reason: `<verified evidence ledger>`
- `hero_style_id`: `<G01-G06 | B01-B06 | NEUTRAL>`
- `enhanced_front_main_composition_variant`: `FRONT_SCREEN_CARD`
- `enhanced_three_quarter_main_composition_variant`: `THREE_QUARTER_SIDE_CARD`
- `pt01_composition_variant`: `<FRONT_SCREEN_CARD | THREE_QUARTER_SIDE_CARD>`
- `enhanced_front_product_view_source`: `<path/source and commercial-use basis>`
- `enhanced_front_exact_model_visual_match`: `<PASS | BLOCKED>`
- `enhanced_three_quarter_product_view_angle`: `<THREE_QUARTER_LEFT | THREE_QUARTER_RIGHT>`
- `enhanced_three_quarter_product_view_source`: `<path/source and commercial-use basis; exact-model angled source required>`
- `enhanced_three_quarter_exact_model_visual_match`: `<PASS | TO_SOURCE | BLOCKED>`
- `enhanced_front_main_windows_package_asset`: `assets/branding/windows-11-pro-package.png`
- `enhanced_three_quarter_main_windows_package_asset`: `assets/branding/windows-11-pro-package.png`
- `strict_main_windows_asset_mode`: `NONE`
- `pt01_windows_asset_mode`: `NONE`
- `enhanced_front_windows_package_placement`: `<SCREEN_SAFE_ZONE | CANVAS_SIDE_SAFE_ZONE>`
- `enhanced_three_quarter_windows_package_placement`: `<SCREEN_SAFE_ZONE | CANVAS_SIDE_SAFE_ZONE>`
- `enhanced_front_windows_package_size_pct`: `<relative to screen or canvas; preserve aspect ratio>`
- `enhanced_three_quarter_windows_package_size_pct`: `<relative to screen or canvas; preserve aspect ratio>`
- `product_to_card_gap_pct`: `<required for THREE_QUARTER_SIDE_CARD>`
- `outer_clear_space_review`: `<PASS | BLOCKED>`
- `windows_package_non_overlap_review`: `<PASS | BLOCKED>`
- `thumbnail_hierarchy_review`: `<PASS | BLOCKED>`
- `supporting_gallery_pack`: `<GG01-GG06 | BG01-BG06 | NEUTRAL>`
- Gallery story reason: `<why the continuation pack fits verified buyer tasks>`
- Benchmark references: `<information coverage only; no wording or assets reused>`
- Final canvas / format: `<dimensions, encoding, RGB>`

## High-intent feature gate

These are candidate fields, not a required bundle. Add, remove, or replace rows
for the exact model; only `VERIFIED` features may reach the title or images.

| Feature | Final value | Status | Evidence | Allowed in title/images? |
| --- | --- | --- | --- | --- |
| Webcam |  |  |  |  |
| Backlit Keyboard |  |  |  |  |
| FP Reader |  |  |  |  |
| Wi-Fi |  |  |  |  |
| Windows 11 Pro |  |  | License/activation and fulfillment evidence required |  |

Delete or mark `BLOCKED` for any claim that is not `VERIFIED`. Do not treat a benchmark listing as product evidence.

## Asset and brand treatment

- Licensed product-photo source: `<source and commercial-use basis>`
- OEM logo asset and permission basis: `<required for PT01–PT08: path/source>`
- `MAIN-STRICT` overlay: `None`
- Unbranded master location: `<path>`
- Deterministic logo plan: `<required logo-placement.json path>`
- Fixed Windows package asset: `assets/branding/windows-11-pro-package.png` (required for both enhanced MAIN candidates; deterministic composition only; prohibited in `MAIN-STRICT` and PT01)

## People and scene asset ledger

Add one row for every slot containing a person or character. `PT02` is the
primary people scene; `PT05` permits at most one secondary person when needed;
`PT06` must always be `NONE`.

| Slot | Asset mode | Role / count | Source / license | Identity/IP review | Synthetic metadata | Included-item ambiguity review |
| --- | --- | --- | --- | --- | --- | --- |
| PT02 | `NONE / SELLER_OWNED / LICENSED_STOCK / ORIGINAL_SYNTHETIC` |  |  |  |  |  |
| PT05 | `NONE / SELLER_OWNED / LICENSED_STOCK / ORIGINAL_SYNTHETIC` |  |  |  |  |  |
| PT06 | `NONE` | None | N/A | PASS | NOT_REQUIRED | PASS |

## Slot plan and record

| Slot | Role | Continuation treatment | Verified copy / facts | Required asset or angle | Fact source | Asset source | Status | Final path |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MAIN-STRICT | White-background default hero | None | No overlay copy | Straight-on complete product |  |  | TO SOURCE |  |
| MAIN-ENHANCED-FRONT-CANDIDATE | Front enhanced hero candidate | Hero family + fixed Windows package | Verified hero content | Accurate front product view |  |  | TO PRODUCE |  |
| MAIN-ENHANCED-THREE-QUARTER-CANDIDATE | Three-quarter enhanced hero candidate | Hero family + fixed Windows package | Verified hero content | Authorized exact-model three-quarter product view |  |  | TO SOURCE |  |
| PT01 | Display / feature overview | Hero family; no Windows package | Distinct verified focus from all MAIN variants |  |  |  | TO PRODUCE |  |
| PT02 | Use cases | Pack use scene |  |  |  |  | TO PRODUCE |  |
| PT03 | Full specifications / configuration | Pack loadout/work grid |  |  |  |  | TO PRODUCE |  |
| PT04 | Design and form factor | Pack design treatment |  |  |  |  | TO PRODUCE |  |
| PT05 | Performance / platform | Pack pipeline/workflow |  |  |  |  | TO PRODUCE |  |
| PT06 | What's included | Clean white factual layout |  |  |  |  | TO SOURCE |  |
| PT07 | Specification recap | Pack recap cards |  |  |  |  | TO PRODUCE |  |
| PT08 | Connectivity / collaboration | Pack ecosystem |  |  |  |  | TO SOURCE |  |

## QA record

- [ ] `MAIN-STRICT` follows the profile-independent Amazon main-image rules and contains no added text, logo overlay, or Windows package.
- [ ] `MAIN-ENHANCED-FRONT-CANDIDATE` uses the accurate front view and fixed Windows 11 Pro package; the package is fully visible, proportionally scaled, and clear of protected content.
- [ ] `MAIN-ENHANCED-THREE-QUARTER-CANDIDATE` uses an authorized exact-model angled view and the same fixed Windows package without inventing chassis details.
- [ ] PT01–PT08 consistently use the selected profile.
- [ ] PT02–PT08 use the continuation pack matching the PT01 Gaming/Business hero family.
- [ ] PT01 contains no Windows package, Windows text tile, or placeholder and uses a different verified information focus from the enhanced MAIN variants.
- [ ] If the enhanced-main package initially caused crowding, the layout was restructured, secondary content reduced, whitespace expanded, or an accurate alternate product angle used; the package was not omitted or replaced with text.
- [ ] `THREE_QUARTER_SIDE_CARD` uses a verified exact-model angled asset and does not invent ports, chassis, keyboard, or included accessories.
- [ ] Title, Description, attributes and image copy agree on model, RAM/SSD, color, features and Win 11 Pro.
- [ ] Every claim is `VERIFIED`; configuration options are clearly distinguished from installed values.
- [ ] Competitor wording, images, icons, layouts and A+ assets were not reused.
- [ ] Every PT01–PT08 image contains the correct verified OEM logo and passed provenance and placement checks; `MAIN-STRICT` has no added overlay and both enhanced MAIN candidates use only approved deterministic brand assets.
- [ ] 100% and thumbnail reviews passed; no text, product, port, card, border or callout collision.
- [ ] Synthetic-performer metadata was added when required.
- [ ] People/characters passed source, identity/IP, anatomy/contact-point and included-item ambiguity review; PT06 contains none.

Delivery state: `<BLOCKED | IN PRODUCTION | IMAGE_READY_FOR_REVIEW>`

