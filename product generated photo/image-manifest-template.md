# VL-<internal-model> Image Manifest

## Product and style lock

- `delivery_mode`: `<FINAL_ASSET_DELIVERY | CONCEPT_ONLY>`
- `workflow_invocation_mode`: `<FULL_LISTING_WORKFLOW | IMAGE_ONLY_WORKFLOW | IMAGE_ADJUSTMENT_WORKFLOW>`
- `delivery_state`: `<BLOCKED_BEFORE_PRODUCTION | IN_PRODUCTION | REWORK_REQUIRED | FINAL_ASSET_QA_PASS>`
- `candidate_semantics`: `COMPLETED_SELECTION_OPTION_NOT_DRAFT`
- `final_image_count`: `11` (`3 MAIN + PT01-PT08`; production records excluded)
- `universal_gallery_dedup_rule`: `<REQUIRED | PASS | FAIL>` (mandatory for every PC audience/style family)
- `universal_physical_port_map_rule`: `<REQUIRED | PASS | FAIL>` (mandatory for every PC audience/style family)
- `physical_port_map_owner_slot`: `<PT08 default | other PT slot with reason>`
- `physical_port_view_coverage`: `<LAPTOP_LEFT_AND_RIGHT | LAPTOP_VERIFIED_SINGLE_SIDE_PARTIAL | DESKTOP_FRONT_AND_REAR | OTHER_VERIFIED>`
- `physical_port_source`: `<authorized exact-model side/rear/front image source>`
- `physical_port_icon_only_failure`: `<false required | true>`
- Internal model: `VL-<internal-model>`
- Exact sold product: `<brand, model, form factor, color>`
- Exact configuration / selectable tiers: `<verified values>`
- `image_style_profile`: `<navy-technical-v1 | feature-led-studio-v1>`
- Profile reason: `<why this profile fits the verified product and licensed assets>`
- `audience_style_family`: `<GAMING | BUSINESS_WORK | STUDENT_STUDY | GENERAL | HYBRID_MANUAL_REVIEW>`
- Audience evidence / confidence / reason: `<verified evidence ledger>`
- `hero_style_id`: `<G01-G16 | B01-B16 | NEUTRAL>`
- `style_approval_status`: `<PROPOSED | APPROVED | REJECTED | BYPASSED_BY_EXPLICIT_USER_REQUEST>`
- `approved_style_id`: `<exact approved hero style ID>`
- `approved_supporting_gallery_pack`: `<matching GG/BG pack>`
- `approval_source`: `<USER_CHAT | EXPLICIT_USER_BYPASS>`
- `approval_timestamp`: `<ISO-8601 timestamp>`
- `screen_background_recipe`: `<palette + required motifs + forbidden motifs>`
- `main_content_boundary`: `<SCREEN_ONLY | approved composition rule>`
- `style_fidelity_review`: `<PASS | REWORK_REQUIRED | NOT_YET_REVIEWED>`
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
- `windows_package_integration_style`: `<SCREEN_GLOW | CANVAS_SIDE_SOFT_SHADOW | NOT_APPLICABLE>`
- `windows_package_background_continuity_review`: `<PASS | BLOCKED>`
- `windows_package_placeholder_visible`: `<false required | true>`
- `frame_break_continuity_review`: `<PASS | BLOCKED | NOT_APPLICABLE>`
- `frame_break_detached_lobes_or_double_border`: `<false required | true | NOT_APPLICABLE>`
- `thumbnail_hierarchy_review`: `<PASS | BLOCKED>`
- `universal_oem_logo_visibility_rule`: `<REQUIRED | PASS | FAIL>`
- `logo_thumbnail_review_size_px`: `200`
- `logo_thumbnail_min_visible_edges_px`: `20 long / 10 short`
- `logo_maximum_long_edge_percent_of_canvas`: `12`
- `logo_minimum_component_separation_px`: `32` (or `2.5%` of canvas short edge, whichever is greater)
- `logo_placeholder_frame_review`: `PASS | FAIL`
- `logo_qa_report`: `<product folder>/logo-qa.json`
- `universal_oem_logo_integration_rule`: `<REQUIRED | PASS | FAIL>`
- `oem_logo_asset_alpha_check`: `<PASS | FAIL | NOT_APPLICABLE_OFFICIAL_REVERSE_ASSET>`
- `oem_logo_preferred_treatment`: `INTEGRATED_TRANSPARENT_MARK`
- `gaming_signature_main`: `<GAMING_WHITE_CATALOG_FRAME_BREAK | NOT_APPLICABLE>`
- `gaming_signature_required_information_review`: `<display + GPU + CPU + RAM/SSD + fixed package: PASS | BLOCKED | NOT_APPLICABLE>`
- `supporting_gallery_pack`: `<GG01-GG16 | BG01-BG16 | NEUTRAL>`
- Gallery story reason: `<why the continuation pack fits verified buyer tasks>`
- Business primary task: `<collaboration | mobility | executive workflow | verified AI workflow | secure hybrid work | other verified task>`
- Benchmark references: `<information coverage only; no wording or assets reused>`
- Benchmark store / ASINs: `<research inputs only; never product evidence>`
- Originality review: `<PASS | BLOCKED>`
- Slot distinctness review: `<PASS | BLOCKED>`
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

Before production, assign every customer-visible claim to one `PRIMARY OWNER` slot. Record the unique information contributed by every PT and its forbidden repeats; after production, populate the OCR/semantic duplicate result. Brand/product identity and navigation labels are excluded from the overlap calculation.

| Slot | Customer question | Planned content | Primary claims owned | Unique contribution | Forbidden repeats | Fact source | Required asset / source | Rights status | Production status | Final path | Duplicate QA |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MAIN-STRICT | What is the exact product? | Product only | Product identity | Clean compliant product view | All overlays |  | Straight-on complete product /  |  | TO SOURCE |  | N/A |
| MAIN-ENHANCED-FRONT-CANDIDATE | Which enhanced front option converts best? | Hero family + fixed Windows package | Front hero message | Completed front choice | Draft/placeholder content |  | Accurate front product + fixed package /  |  | TO PRODUCE |  | N/A |
| MAIN-ENHANCED-THREE-QUARTER-CANDIDATE | Which angled option converts best? | Hero family + fixed Windows package | Angled hero message | Completed angled choice | Invented chassis details |  | Authorized exact-model angle + fixed package /  |  | TO SOURCE |  | N/A |
| PT01 | Why consider this product? | Hero family; no Windows package | High-level purchase reason |  | Full configuration grid |  |  |  | TO PRODUCE |  | PENDING |
| PT02 | How will it be used? | Pack use scene | Use-case narrative |  | Configuration cards |  |  |  | TO PRODUCE |  | PENDING |
| PT03 | What exact configuration is sold? | Single full configuration page | CPU/GPU/RAM/SSD/OS |  | Second display/design recap beyond minimum configuration context |  |  |  | TO PRODUCE |  | PENDING |
| PT04 | What are the display and chassis experiences? | Display + accurate design treatment | Size/resolution/refresh + verified chassis/keyboard facts |  | CPU/RAM/SSD configuration grid |  |  |  | TO PRODUCE |  | PENDING |
| PT05 | How do the components support the task? | Causal pipeline/workflow | Performance relationship, not exact configuration |  | Full CPU/GPU models, RAM/SSD capacities, second specification grid |  |  |  | TO PRODUCE |  | PENDING |
| PT06 | What's included? | Clean white factual layout | Exact in-box items |  | Performance/configuration claims |  |  |  | TO SOURCE |  | PENDING |
| PT07 | What unaddressed value remains? | Dynamic distinct-value module or restrained product scene | One unused verified theme |  | Specification recap, Gaming Essentials, reordered core-spec cards |  |  |  | TO PRODUCE |  | PENDING |
| PT08 | How does it connect? | Exact-model physical port map + supporting wireless/collaboration | Visible physical ports, anchored verified labels, wireless as secondary |  | Icon-only connectivity page; core performance recap |  | Exact-model side/rear/front I/O source |  | TO SOURCE |  | PENDING |

## Cross-gallery duplicate QA

- OCR/extracted claim inventory: `<path or summary>`
- Pairwise semantic overlap review: `<PASS | FAIL; highest pair and percentage>`
- PT03 sole complete-configuration owner: `<PASS | FAIL>`
- PT05 relationship-not-recap review: `<PASS | FAIL>`
- PT07 distinct-value review: `<PASS | FAIL>`
- Every PT adds unique information: `<PASS | FAIL>`
- Overall duplicate gate: `<PASS | FAIL>`

## QA record

- [ ] `MAIN-STRICT` follows the profile-independent Amazon main-image rules and contains no added text, logo overlay, or Windows package.
- [ ] `MAIN-ENHANCED-FRONT-CANDIDATE` uses the accurate front view and fixed Windows 11 Pro package; the package is fully visible, proportionally scaled, and clear of protected content.
- [ ] `MAIN-ENHANCED-THREE-QUARTER-CANDIDATE` uses an authorized exact-model angled view and the same fixed Windows package without inventing chassis details.
- [ ] A screen-placed Windows package sits over a fully continuous background with no placeholder rectangle and uses palette-aware glow/contact shadow without altering the package itself.
- [ ] Gaming frame-break subjects form one continuous screen-connected silhouette; no detached shoulder lobes, triple-bump outline, floating parts, double bezel, neon contour, or sticker edge remains.
- [ ] At least one PT image, normally PT08, shows the exact product's visible physical ports with callout leaders anchored to the correct openings; an icon-only connectivity layout is not accepted.
- [ ] Laptop port coverage includes both port-bearing sides when required, or clearly identifies a verified partial side view; desktop/AIO/mini-PC coverage includes the relevant front and rear I/O. No port geometry or capability was inferred.
- [ ] PT01–PT08 consistently use the selected profile.
- [ ] PT02–PT08 use the continuation pack matching the PT01 Gaming/Business hero family.
- [ ] A `Gallery Content Ownership Matrix` was completed before generation, and each PT has one documented `unique_information_contribution`.
- [ ] OCR and semantic pairwise review passed: no pair exceeds 20% primary-information overlap, PT05 is not a second configuration page, and PT07 is not a specification recap.
- [ ] PT01 contains no Windows package, Windows text tile, or placeholder and uses a different verified information focus from the enhanced MAIN variants.
- [ ] If the enhanced-main package initially caused crowding, the layout was restructured, secondary content reduced, whitespace expanded, or an accurate alternate product angle used; the package was not omitted or replaced with text.
- [ ] `THREE_QUARTER_SIDE_CARD` uses a verified exact-model angled asset and does not invent ports, chassis, keyboard, or included accessories.
- [ ] Title, Description, attributes and image copy agree on model, RAM/SSD, color, features and Win 11 Pro.
- [ ] Every claim is `VERIFIED`; configuration options are clearly distinguished from installed values.
- [ ] Competitor wording, images, icons, layouts and A+ assets were not reused.
- [ ] Every PT01–PT08 image contains the correct verified OEM logo and passed provenance and placement checks; `MAIN-STRICT` has no added overlay and both enhanced MAIN candidates use only approved deterministic brand assets.
- [ ] `logo-qa.json` reports `PASS` for PT01–PT08; every visible OEM mark meets the 200 px thumbnail minimum of 28 px long-edge and 10 px short-edge.
- [ ] Every OEM mark is visually integrated: transparent asset or OEM-approved keyline/reverse treatment, no visible source rectangle or generic white card; any hard badge has a documented `badgeExceptionReason`.
- [ ] 100% and thumbnail reviews passed; no text, product, port, card, border or callout collision.
- [ ] Synthetic-performer metadata was added when required.
- [ ] People/characters passed source, identity/IP, anatomy/contact-point and included-item ambiguity review; PT06 contains none.

Delivery state: `<BLOCKED_BEFORE_PRODUCTION | IN_PRODUCTION | FINAL_ASSET_QA_PASS>`

For `FINAL_ASSET_DELIVERY`, `TO SOURCE`, `TO PRODUCE`, a production brief, an
unbranded master, or a missing deterministic overlay cannot satisfy a requested
slot. `IMAGE_READY_FOR_REVIEW` means the same practical condition as
`FINAL_ASSET_QA_PASS`: the files shown to the user are already complete and the
review decides selection/approval, not whether required content will be added
later.

