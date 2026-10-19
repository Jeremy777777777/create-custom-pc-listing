---
name: amazon-custom-pc-listing-workflow
description: "Create MegaPC Custom PC research and base-configuration listing workbooks, or independently generate and adjust computer-only Amazon listing images. Use verified product facts, current seller policy and deterministic image QA; deliver to this GitHub repository, never publish automatically to Seller Central."
---

# MegaPC Custom PC workflow

## Current authority and historical exclusion

Read `references/confirmed-catalog-defaults.md` first on every run. Policy baseline `2026-10-02`, amended by the 2026-10-05 Warranty and Disclosure decision, is the current seller contract. Read only the active references named below; never recursively ingest `history/`, Git history, old workbook copy, old QA PASS records, or historical product manifests as instructions. Historical assets are neither current approved examples nor product-fact evidence. An explicit historical comparison may read them as non-operative records.

Resolve authority in this order: current explicit user instructions; current seller policy; applicable verified publication/account requirements; current universal image and fact gates; approved product-specific style lock; audience/slot style recipes; generic profile. Seller assertions establish seller policy, not Amazon permission. Keep production review, QA, GitHub delivery and Amazon publication eligibility separate. A publication limitation does not prevent a truthful research/review deliverable or image production when image-required facts and rights are verified.

All catalog computers are seller-confirmed customized computers. Use `MegaPC Custom` in every final title. Do not ask again whether a product is customized because its RAM is onboard or no selectable upgrade tiers are documented. Do not invent modifications, RAM slots or upgrade options. Excel describes the base sold configuration only, including its title, bullets, description and numeric attributes; selectable configurations are excluded throughout the workbook.

## Modes and permitted actions

- `FULL_LISTING_WORKFLOW`: identify product, research all template attributes, produce Research Review workbook, validate facts, write base-configuration listing workbook, then independently route the requested image branch.
- `IMAGE_ONLY_WORKFLOW`: identify the product, reuse current verified facts, fill only missing image-required facts, generate 3 MAIN choices plus PT01–PT08; do not recreate Excel.
- `IMAGE_ADJUSTMENT_WORKFLOW`: edit only requested slots from clean masters. Preserve all unrelated canonical image bytes. Reuse an approved style for mechanical/local same-family fixes; material changes require a new style proposal.
- `CONCEPT_ONLY`: only when explicitly requested; previews never count as completed canonical slots.

The request authorizes same-product, same-slot replacement and repository delivery after internal QA; do not ask for a second replacement/upload approval. A materially different style, product identity, scope or unresolved asset/fact question still needs the appropriate clarification. Never publish to Seller Central automatically.

## 1. Identify and map the target

### Python / Jupyter execution preference

For every Listing mode (text/workbooks, images and workflow updates), apply the user's [Python/Jupyter testing preference](references/python-jupyter-testing.md) before programmable work. Prefer the dedicated Anaconda `listing-testing` Python 3.12 environment and **Python (Listing Testing)** kernel; verify the interpreter and run checks relevant to the changed content. Jupyter debugging and direct scripts share this environment; no always-open server is needed. Missing environment/access is reported rather than silently switching runtimes. This tooling preference does not replace factual/manual image QA, style approval or delivery gates.

Read `references/input-source-cross-validation.md`.

Optional sources:
- MyStore ERP: https://erp-git-feat-part-serial-numbers-overhaul-jtechdigital.vercel.app/products?s=categoryId,status,id
- Listing Status Tracker: https://docs.google.com/spreadsheets/d/11qeinso-6eRYgSVLQlRdteOZL8vsZE9IBfZcVMBXEkE/edit?gid=621896540#gid=621896540

Use `MYSTORE_ONLY`, `CHECKLIST_ONLY` or `MYSTORE_AND_CHECKLIST`. Locate the exact requested product, not the whole catalog. Preserve original records, source URLs, timestamps, product IDs, tracker sheet/row, name, internal VL/VA identifier and quantity. Match by verified identity and configuration; do not merge fuzzy matches or expand an unconfirmed range. A missing source may be replaced by independent authoritative evidence.

Confirm the canonical internal ID before writing `product generated photo/<internal-id>/` (for example VL-1221 or VD-744). Preserve the verified prefix; do not invent a VL alias or substitute an ERP number, ASIN or OEM model. Confirm Quantity's business meaning before using it as Amazon available inventory. Read an existing folder's current `product-facts.json` and `delivery-status.json` before looking at any previous output. `LEGACY_QUARANTINED` means historical images must be revalidated, not reused as approved styles or uploaded as current finished output.

## 2. Research and field validation

Read `references/research-attribute-coverage.md`, `references/confirmed-catalog-defaults.md`, and the current `assets/listing-workbook-template.xlsx`. Enumerate every actual attribute and Definition in Product Details, Offer and Safety&Compliance; column A is the Field / Attribute row-label column, not a product field. Keep one fact ledger; image work must not create a competing set of facts.

For new research, use [scoped ledger and projection](references/research-ledger-projection.md) and assets/research-ledger-schema.json. Keep factory/current/sold/capability facts separately within that one ledger and map template fields explicitly. Use scripts/research_export.py --write-workbook to generate a new staged Excel and coverage summary from the ledger, and its export mode for mandatory pre-export evidence checking. Follow the updated guide's brand routes and FCC outcome/color contract in [FCC research](references/fcc-research-workflow.md). Legacy array ledgers remain research drafts until their scopes are reconciled. Do not promote a candidate or factory-installed value into a confirmed sold value just to pass checks.

Research exact OEM SKU/model/region/colour, installed CPU/GPU/RAM/internal SSD, display, wireless, physical ports, input, camera/audio/security, dimensions/weight, power/battery, pack-out and regulatory attributes. Distinguish installed values from capabilities and maximums. Use exact ERP/assembly records for sold configuration, exact OEM evidence for physical facts, and component sources only for the component. Retailer/Amazon pages discover omissions and differences; they do not independently verify specifications or asset rights.

Apply [ERP serial-based PC research](references/serial-number-product-research.md) across product attributes: proactively find current or historical serials linked to the target, query the official OEM as-built configuration/parts, resolve exact hardware parts and reconcile each finding with seller upgrades and the base sold configuration. Record factory/current/sold/platform scope per field; historical units and factory pack-out do not automatically establish current inventory or included accessories. Use existing verified facts for scoped image work and keep raw serials/private evidence out of public delivery.

Record the product-level `serial_research` outcome under that guide before new workbook generation, changed research delivery or marketplace export checking. A failed lookup is a valid research outcome with attempted sources, reason and follow-up owner/action; it does not verify unresolved hardware. Untouched legacy records remain unassessed, never implicitly completed. Image-only work may record a justified `NOT_REQUIRED`; full research cannot use that exemption.

For full listing research and FCC-field corrections, apply [FCC lookup and workbook mapping](references/fcc-research-workflow.md). First seek current or historical serials linked to the target in ERP, resolve the OEM factory hardware part and exact radio module, then match its official FCC ID. Where confirmation is incomplete, deliver a ranked evidence-linked most-likely candidate with INPUT_UNVERIFIED, rationale and the missing verification; ties/no defensible candidate remain explicit. Keep serials/private unit evidence out of public GitHub records and candidates out of marketplace export. Image-only edits do not require unrelated compliance research.

The [Chinese Word FCC manual](references/manuals/fcc-id-lookup-manual.docx) and [searchable Chinese source](references/manuals/fcc-id-lookup-manual.zh-CN.md) are reading copies of these active references. Follow [reading-copy maintenance](references/manuals/README.md); they do not override current execution rules or authorize new external actions.

Review up to three accessible high-quality exact/related Amazon listings for coverage and original information organisation. Do not force three unsuitable results or copy text/images. Save searches, date, URLs and differences.

Each field records candidates, final value, applicability, source/date, exact configuration, status and disposition. States: `VERIFIED`, `INPUT_UNVERIFIED`, `CONFLICT`, `TBD`, `SOURCE_UNAVAILABLE`, `NOT_APPLICABLE`. Preserve genuine unresolved conflicts. Seller/account/logistics-only fields use `TBD` with `SELLER_INPUT_REQUIRED` and a specific required input. Every field needs a status and source or disposition, even when Value is blank. Evidence-linked FCC candidates are permitted in research under the linked procedure; they are not verified final facts. No unsupported guesses, silent blanks, missing-as-zero, or series options treated as installed.

Apply current confirmed policy resolutions before classifying conflicts: OEM Home versus seller-delivered Pro is an explained difference, not an OS conflict; VL-1276's internal SSD is 512GB and RAM is fixed 16GB onboard. Licence/activation and publication evidence remain separate review items. Do not re-ask settled seller assertions. Model-specific hardware assertions never transfer to another ID.

## 3. Produce Research Review and listing workbooks

As soon as the mapped internal ID and a real Research Review workbook exist, upload it to the product folder; do not wait for imagery or publication readiness. Never overwrite the source template. Use explicit stage filenames and true review statuses.

All top-level product workbooks are current and must match the current ledger. Preserve superseded stages with their original ledger/template and immutable hashes under [workbook stage snapshots](references/workbook-stage-snapshots.md); CI checks their preserved bytes rather than latest-field projection. Historical snapshots never become export-eligible. Export requires explicit LISTING_DRAFT stage, the current canonical template and OEM identity/copy checks regardless of filename.

Read `references/listing-style-guide.md` and `references/compliance-rules.md`. Write original English copy only from verified base facts and the confirmed seller policy:
- Title starts `MegaPC Custom`, references the OEM model using `Created Using`, describes only installed base RAM/SSD and relevant verified features, and ends `Win 11 Pro`. Maximum 200 characters; no optional capacity lists.
- Default to five bullets, with the complete mandatory warranty paragraph as bullet 1. Store five paragraphs in the single Bullet Point cell, separated by exactly one blank line. Publish-time export splits paragraphs; do not add template columns.
- Replace `[OEM brand]` in the mandatory paragraph with the verified manufacturer. Preserve every other word: `MegaPC provides a 1-year limited warranty on the upgraded RAM and SSD components. The original [OEM brand] manufacturer warranty remains valid on all remaining factory components, so you are covered on both the base machine and our upgrades. The original seal has been opened solely for upgrading purposes.` Use it identically in bullet 1, final Description Warranty and Disclosure paragraph and Warranty Description. No alternate duration, optional extension, paraphrase, omitted seal sentence or product-specific wording is allowed.
- Product Description uses literal HTML in the Excel Value cell: `<strong>Identity</strong><br/><br/>`, then `<strong>Section Heading</strong><br/>Body`, with `<br/><br/>` between sections. Use this format for all future Listing Excel outputs; do not substitute Markdown, backslashes, Excel-only rich-text styling or `</br>`. See the 2026-10-07 catalog format decision. Warranty and Disclosure is last. Describe installed base memory/storage; do not include selectable tiers. Other hardware remains factory configured; final OS follows seller policy rather than a blanket “software remains original” statement.

Map by worksheet name plus exact row-1 field name: row 2 Definition, row 3 Value, row 4 Status, row 5 Source. Preserve all sheets, headers and template rows. Units pair with numbers. Title→Item Name; paragraphs→Bullet Point; description→Product Description; base CPU/RAM/SSD/OS→existing semantic fields; verified seller SKU/available quantity→Offer; warranty→Safety&Compliance Warranty Description. Keep detailed evidence and QA outside the workbook. Use assets/warranty-disclosure-policy.json and scripts/warranty_policy.py to render/validate the fixed paragraph. Listing-stage workbook checks require the current product identity.oemBrand; unknown manufacturer prevents final substitution, not a fallback to different warranty wording.

Export coverage counts and unresolved critical/seller items. `WORKBOOK_STRUCTURE_PASS` means structure, not fact/compliance clearance. Draft listing copy can be present with an honest review disposition; do not write TBD/internal warnings into customer copy. `READY_FOR_SELLER_REVIEW` requires applicable completeness and compliance gates; no automatic Amazon publication. Research and listing workbooks share the same product folder.

## 4. Image preflight, proposal and production

Read these current references:
- `references/amazon-product-image-workflow.md`
- `references/final-image-delivery-contract.md`
- `references/image-spec.md`
- `references/style-approval-gate.md`
- `references/brand-authorization-policy.md`
- `references/image-style-profiles.md`
- `references/conversion-hero-styles.md`
- `references/hero-composition-variants.md`
- `references/supporting-gallery-styles.md`

Gaming additionally reads `gaming-hero-styles.md`, `gaming-core-badge-styles.md`, `gaming-main-reproducible-workflow.md`. Business reads `business-work-hero-styles.md`, and B07–B17 also reads `business-laptop-gallery-styles.md`. Business Laptop B17/BG17 reads [business-graphite-design-system.md](references/business-graphite-design-system.md) and its two approved visual references before planning. It adapts exact-product features, screen content and measured layouts, not Yoga-specific copy. B17 is optional: the user retained existing selection and per-product preview/approval in the [2026-10-05 decision record](references/business-graphite-policy-decisions.md).

First verify every required exact-model angle, physical port image, fact and asset right. Search authorized OEM sources autonomously; retailer discovery never grants commercial rights. The user-confirmed OEM authorization covers the approved official-image references and their faithful AI reproduction under [faithful-product-reproduction.md](references/faithful-product-reproduction.md); other IP stays separately gated. Block production if required material is missing; never fabricate chassis, ports or a completed gallery.

Use computer-only imagery: no external accessories/devices, contextual peripheral silhouettes, retail pack-out, or seller warranty advertising. A human and furniture may establish the PT02 use case without additional equipment. Fixed software labels in the LCD are graphic assets, not included retail boxes. Preserve authentic chassis marks; added OEM logos go outside the product only in PT negative space. Select audience from OEM positioning and hardware/workload evidence; catalog-wide Pro alone does not classify every computer as Business.

Approve one product-specific G/C/A/GG or B/BG style and recipe before full production unless the current user explicitly bypasses proposal approval. Existing same-product approval survives policy refresh and local fixes; changing hero world, palette, layout family, pack or purchase narrative requires reapproval. Keep style consistency rather than identical wallpaper.

Deliver RGB/RGBA files meeting the Amazon-based size policy in `references/image-spec.md` with opaque final backgrounds (JPEG must be RGB): MAIN-STRICT.jpg, MAIN-ENHANCED-FRONT-CANDIDATE.png, MAIN-ENHANCED-THREE-QUARTER-CANDIDATE.png, PT01.png–PT08.png. Three MAIN files are alternatives for one Amazon slot. MAIN-STRICT is pure white/product only. Enhanced outside background is white, all marketing content inside LCD; Gaming permits approved continuous head/helmet only across TOP, never shoulders/hands/effects. Gaming fixed package appears once on each enhanced choice; Business defaults to front lockup and three-quarter package; the approved recipe may swap their placement, but the two choices must use distinct treatments. PT01 has no Windows treatment; PT03 owns base full configuration and OS; PT04 display/form; PT06 input detail; PT08 actual physical ports. PT07 adds an unused verified value, never seller warranty promotion or spec recap.

Use exact licensed original product layers or AI layers that pass the official-original fidelity gate in [faithful-product-reproduction.md](references/faithful-product-reproduction.md), with clean masters, deterministic brands/text and current scripts. AI must faithfully reproduce the actual machine; never invent hardware or redraw final logos. Reject mismatched or unverified visible details and use the original photo when faithful reproduction cannot be verified. Flat approved PNGs are references, not complete layered production packs. Keep masters and recipes reproducible outside canonical delivery. Start new manifests from `product generated photo/image-manifest-template.md`.

## 5. QA, updates and GitHub delivery

Apply [workflow validation boundaries](references/workflow-validation-boundaries.md) for export identity/content checks, review-input binding, import lifecycle, snapshot preservation and local tool selection. These refine the existing stages without changing the workbook or gallery structure.

Apply [follow-up workflow checks](references/workflow-edge-case-checks.md) for explicit field types/units, CPU/RAM/copy consistency, non-image change and deletion routing, and output rollback. Historical records remain historical; these implementation checks do not replace actual review or change approved product appearance.

Apply [product fact projection](references/product-fact-projection.md) when moving research into Listing or using a scoped ledger for images. Use verified read-only metadata views, bind selected hardware research in new image reviews, and report pre-ledger reviews separately without inventing a new PASS.

Use the [research handoff checklist](references/research-handoff-checklist.md) to close each stage: canonical directory identity, storage scope/unit reconciliation, coverage summary and unresolved follow-up ownership. Deliver a current `.research-summary.json` alongside new scoped Research Review workbooks; neither the summary nor CI replaces factual/publication review.

Apply [capacity measurement basis](references/capacity-measurement-basis.md): nominal SSD/HDD GB/TB are decimal (1TB = 1000GB), with separate memory-size conventions. Do not substitute system/usable GiB measurements for installed nominal drive capacity; reconcile their source/basis first.

Follow `references/final-image-delivery-contract.md` for script commands, report schemas and current-byte binding. Automation checks decoded image dimensions/format, exact slot set, geometry, hashes and supplied review evidence; manual reviews verify product appearance, rights, style, spelling, ports, semantic ownership and 100%/200px readability. Never invent manual PASS, unmeasured overlap percentages, or fresh QA for quarantined historical bytes.

Same-slot updates use that slot's clean master and preserve all unrelated bytes. Any changed image invalidates its hash-bound reports and delivery record. An update may reuse unchanged review evidence only if the underlying bytes and relevant facts/policy remain unchanged. Finalization is not permission to rewrite unrelated slots. When the existing gallery is quarantined, complete and QA only the requested slots using the partial-update contract; retain overall REWORK_REQUIRED and state deliveryScope PARTIAL_UPDATE. Hash-bound partial-update-qa.json proves only changed slots and cross-gallery content review; it cannot confer full-gallery PASS. CI may accept that scoped update without pretending unchanged legacy slots passed the current standard.

Sequence: local tests and current QA for the delivered scope → selective commit/push → applicable remote CI → remote commit/path/file-hash verification → `GITHUB_DELIVERY_VERIFIED` for the explicitly reported delivery scope. A partial update never claims full-gallery verification. Remote CI is not a precondition for its own triggering push. CI failure means delivery blocked, never Amazon-ready. Explicit local-only/no-upload/concept instructions skip remote delivery only.

A canonical folder must have exactly 11 current image slots when completed; XLSX and JSON/Markdown records are additional deliverables. During Research it may contain only a workbook/fact record. Quarantined historical galleries are retained for recovery but cannot satisfy completion. Do not execute scripts in history. Git preserves previous versions.

## Final report

Report the verified internal ID, source mapping, base configuration, workbook stage, critical unresolved items, current policy version, gallery state, requested/changed slots, local and applicable remote QA, GitHub folder/workbook/commit links and remote hash verification. State any production/delivery/publication blockers separately. Do not present a ZIP, local PASS or historical report as GitHub completion.

## Current recipe and desktop applicability

Use [production-recipes.md](references/production-recipes.md) for slot layouts, layer requirements and rebuild procedure. Read the current product style-lock.json first; preserve approved direction while rebuilding missing recipes, without inheriting old QA. Universal LCD/SCREEN_ONLY and lockup/package instructions above apply to integrated-screen computers. Standalone towers/SFF/mini PCs use the catalog policy's DESKTOP_GRAPHIC_SAFE_ZONE exception with package/package, accurate chassis layers and an approved versioned safe-zone recipe; no monitor, invented LCD or head breakout.

## Current Gaming reference — 2026-10-02

For Gaming enhanced MAIN, apply [gaming-approved-main-fit.md](references/gaming-approved-main-fit.md) before any older generic head-breakout, top-clearance or reference-exclusion instructions. SCREEN_ONLY six-card composition is now the integrated-screen default; HEAD_ONLY is an optional separately approved variation. The exact VL-1221 front supplied and approved by the user is a hash-bound 1237×937 import exception, not a full-gallery PASS or a reusable exception for other files. New generations follow the current Amazon-based size policy in image-spec.md and independently verified product facts.
