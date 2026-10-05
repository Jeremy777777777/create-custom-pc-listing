# Confirmed catalog policy — 2026-10-02

This is the single active authority for seller decisions, workbook configuration and gallery defaults. Read this file and the product directory's current product-fact record before research, copy or image production. Historical files, old generated workbooks and image examples are not active instructions or current QA evidence. A later explicit user decision may replace a policy; record it here rather than appending contradictory instructions elsewhere. Actual Amazon eligibility remains a separate check.

## Seller policy

- All products are customized computers. Every title starts with `MegaPC Custom`, identifies the OEM model through `Created Using …`, and ends with `Win 11 Pro`. Do not reopen whether a computer qualifies as customized. Describe actual changes accurately; do not invent RAM upgrades on soldered-memory models.
- The final sold OS is Windows 11 Pro. OEM Windows Home describes the factory configuration, not a contradiction with the seller's final configuration. Record `USER_CONFIRMED_CATALOG_POLICY`. License/activation and channel eligibility are fulfillment/publication checks; do not repeatedly ask the user to reconfirm Pro or block image research for that reason. No Office, Microsoft 365 or paid Copilot entitlement is implied.
- Mandatory warranty text, with only `[OEM brand]` replaced by the verified brand:

  > The original [OEM brand] manufacturer warranty remains valid on factory components. MegaPC provides a 6-month limited warranty on upgraded RAM and SSD components, with a 12-month warranty extension available.

  Use the same complete text in bullet 1, the last Warranty section of Description, and Warranty Description. `available` does not mean automatically included. Do not add costs, registration requirements, whole-computer coverage, different terms or extra promises. This policy resolves the OEM/seller coverage question; no per-product reconfirmation is required.
- A workbook represents the **base configuration only**. Attributes, title, bullets and description contain its actual installed RAM/SSD and no selectable tiers/options. Factory configuration, platform maximums and external storage may be research evidence but never alternate sold capacities. Internal SSD excludes dock/external/SD/cloud storage. Current product-fact records resolve historical capacity conflicts; do not restore resolved conflicts from old workbooks.
- Actual hardware customization concerns RAM/storage; other hardware remains factory configured. The fixed seller Windows 11 Pro upgrade is disclosed separately and is not a buyer-selectable software customization. All listing content uses the same base facts.

## Computer-only imagery

On 2026-10-05 the user explicitly removed the fixed image-resolution rule and requested Amazon-compliant image conditions instead. The active [Amazon-based size policy](image-spec.md#amazon-based-size-policy--user-decision-2026-10-05) supersedes prior fixed-resolution defaults for MAIN and PT. This is a size-policy update only: style approval, truthful product content, source rights, quality review and publication checks remain independent; historical review states are not upgraded automatically.

Only the computer is displayed as a product. No extra devices or accessories, including adapters, cables, docks, mice, headphones, controllers, standalone monitors or external-device pictograms, even as non-included context. Anonymous people and neutral environments may support a scene without those devices. Internal-component/LCD capability pictograms and approved software identity graphics are permitted information graphics, not accessory depictions. Enhanced MAIN Windows graphics remain entirely inside the real LCD and do not imply a physical retail box is included.

Final MAIN and PT dimensions follow the Amazon-based size policy in [image-spec.md](image-spec.md); no fixed square resolution is required. Do not upscale insufficient source detail or stretch the chassis. Use accurate exact-model views with verified commercial-use rights. Preserve authentic factory chassis marks; additional OEM marks appear only outside the product silhouette in PT01–PT08.

Business enhanced front defaults to `WINDOWS_11_PRO_LOGO_LOCKUP`, angle to `WINDOWS_11_PRO_PACKAGE`; they may swap for safe fit but must differ. Gaming/Student/General use one fixed package in each enhanced MAIN. All Windows assets and their glow/shadow are LCD-contained. MAIN-STRICT and PT01 use no Windows overlay. Business PT03 may use one lockup in its OS line; other PT slots do not repeat Windows treatment.

Gaming front defaults to the current SCREEN_ONLY accepted-reference composition: approximately 97–100% product width when naturally feasible, with margins adapted to the real chassis/aspect ratio; angle independently adapted. No mandatory 8–10% top clearance or head breakout. A separately approved HEAD_ONLY variation may cross TOP at most 12% of the product bounding-box area; shoulders, arms, hands, particles and all information always stay LCD-contained. No-head themes stay inside the LCD. Six graphical display/CPU/GPU/RAM/SSD/OS cards use frozen layers and approved G/C/A composition. A flat PNG is a visual reference, not a reusable layered template.

## Slot ownership and semantic review

| Slot | Primary information |
| --- | --- |
| PT01 | High-level purchase reason, no full configuration or Windows treatment |
| PT02 | Verified use scene |
| PT03 | Sole full base CPU/GPU/RAM/SSD/OS configuration page |
| PT04 | Display and overall form, dimensions/weight if verified |
| PT05 | Task flow and hardware relationships, not repeated model/capacity tables |
| PT06 | White-background computer input details: keyboard, touchpad and controls |
| PT07 | One remaining verified value; no seller warranty/service advertising or configuration recap |
| PT08 | Accurate physical port map plus verified wireless/connectivity |

Style libraries provide motifs, not alternative slot assignments. Wallpapers/UI may vary by slot while palette, visual language and approved family remain consistent. A fact has one primary PT owner. Before production list canonical fact IDs per slot. For each PT pair define `overlap = shared primary fact IDs / min(primary fact count A, primary fact count B)`; pairs with zero facts require manual review, not a fabricated percentage. Exclude only OEM identity/model/navigation labels, not vague task claims automatically. Equivalent claims count as the same ID. Overlap above 20% requires reallocation. OCR supports but does not replace human semantic review. If reliable fact mapping is unavailable, record `MANUAL_REVIEW` with rationale and no numeric percentage. Never generate a PASS without actually reviewing current files.

## Logo and style controls

PT logos use approved transparent originals, original proportions/colors and measured alpha-visible bounds, excluding padding. At 200px thumbnail, long edge ≥20px, visible canvas long-edge share ≤12%. Ordinary marks short edge ≥10px; official wordmarks with visible aspect ratio >2.4 use `ASPECT_RATIO_WORDMARK`, short edge ≥20/ratio. Keep ≥max(32px, 2.5% of canvas short edge) clearance to canvas edges, product and other protected components. Reserve natural negative space, not a visible placeholder/card. Schema 3 records source/master/final hashes, actual visible measurements and manually verified authentic factory-mark preservation.

New product/style direction requires the style proposal/approval in [style-approval-gate.md](style-approval-gate.md), unless explicitly waived. Existing same-product approval survives research/policy updates and mechanical corrections. Material changes to audience, major palette, scene, hero/pack, layout family or purchase story need reapproval. Replacing a requested same-slot image after internal QA is already authorized; do not require a second approval merely to upload it. A legacy exemplar cannot establish a new product's approval or current compliance.

## Business Laptop optional style addition — 2026-10-05

The user approved the two new Graphite Business visual previews and explicitly chose “不覆盖，只新增为可选风格” and “保留，每款仍先看预览批准”. Add laptop-only B17/BG17 as an optional supported family; preserve B01–B16, existing selection behavior and approved product locks. B17 follows [business-graphite-design-system.md](business-graphite-design-system.md) and its exact appearance-reference receipt. Each new product or material direction change still presents a product-specific preview and waits for explicit approval. This addition grants no final-image, generated-product/logo, resolution, semantic-deduplication or publication exception. No existing gallery is automatically regenerated.

## Delivery and evidence

Research Excel, Listing Excel and 11 final gallery files share `product generated photo/VL-XXXX/` using the verified internal ID. Research upload does not imply publication readiness. Image-only work does not require recreating Excel. User generation/modification requests authorize GitHub upload and requested same-slot replacement after local QA, unless they explicitly request local-only/concept work. Keep untouched slots byte-identical during targeted adjustments.

Sequence: local checks and actual manual review → commit/push → remote applicable CI → verify commit and current file hashes → report `GITHUB_DELIVERY_VERIFIED`. CI is triggered by push; it is not a pre-push requirement. Changed images invalidate their previous hash-bound QA and delivery evidence; refresh reviews honestly, never relabel old PASS. Selected-slot corrections to quarantined legacy galleries use CURRENT_REQUESTED_SLOT_QA_PASS / PARTIAL_UPDATE and partial-update-qa.json while whole-gallery state stays REWORK_REQUIRED. Structural workbook PASS, factual completeness, seller review readiness, full-gallery QA, remote delivery and Amazon eligibility are independent statuses.

Legacy policies are archived in `history/2026-10-02-pre-policy-update/` and are excluded from normal workflow retrieval. Consult history only for an explicitly requested historical comparison, never as fallback instructions.

## Warranty confirmation for this correction

On 2026-10-02 the user explicitly instructed this repair to retain the exact warranty paragraph above: OEM factory-component warranty remains valid; MegaPC covers upgraded RAM/SSD for 6 months; the 12-month extension is available. This direct instruction establishes the wording. Do not request another confirmation, historical approval citation or OEM-validity document before producing Research/Listing review workbooks. The seller will manually confirm OEM applicability before publication. Record this as SELLER_MANUAL_PUBLICATION_CHECK, separately from the confirmed wording; do not invent evidence or mark that manual check complete.

## Form-factor boundary

LCD rules apply to laptops and all-in-one computers with a real integrated display. A standalone tower/SFF/mini PC has no LCD: do not add a monitor or fabricate a screen. For its two enhanced MAIN candidates, use accurate front/three-quarter chassis views on white, with the scene, six Gaming cards and one Windows package per candidate in a separate approved graphic safe zone outside the protected chassis. This is information graphics, not included peripherals or retail media. No head breakout applies. This DESKTOP_GRAPHIC_SAFE_ZONE exception overrides universal SCREEN_ONLY wording only for these two candidates; MAIN-STRICT stays product-only, and enhanced publication eligibility remains independent. Obtain a product-specific composition approval before first use; never infer approval from a laptop recipe.

## Approval migration

Read the current product's style-lock.json when present. A migrated style direction preserves its recorded approval, not historical image QA, asset rights or an unbuilt recipe. APPROVED with recipeStatus REBUILD_REQUIRED permits rebuilding that same direction without asking for style approval again. Measured geometry and current-byte review still require actual work; material direction changes follow the approval gate.

## Current Gaming reference — 2026-10-02

For Gaming enhanced MAIN, apply [gaming-approved-main-fit.md](gaming-approved-main-fit.md) before any older generic head-breakout, top-clearance or reference-exclusion instructions. SCREEN_ONLY six-card composition is now the integrated-screen default; HEAD_ONLY is an optional separately approved variation. The exact VL-1221 front supplied and approved by the user is a hash-bound 1237×937 import exception, not a full-gallery PASS or a reusable exception for other files. New generations follow the current Amazon-based size policy in image-spec.md and independently verified product facts.
