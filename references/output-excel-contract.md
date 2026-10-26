# Default output Excel contract — user decision 2026-10-21

This is the standing result contract for future full research/listing Excel deliveries. The accepted result is a populated listing workbook with field-by-field research and separate evidence-backed candidate rows. A research-only workbook, blank template or coverage report cannot substitute for that result. Apply this reference together with the current seller policy, copy guide, scoped ledger, candidate-row and Drive delivery rules. It records the reusable format and review method, not the specifications or completeness counts of any previous product.

Apply the 2026-10-26 [official evidence chain and deep research](evidence-chain-and-deep-research.md) automatically: official serial lookup plus exact-product search > ERP > Amazon, with matching official research governing conflicts. A reported later configuration cannot silently override official evidence; preserve scope and unresolved sold applicability. Carry the queries, sources, conflict decisions and research completion basis into the ledger/Research Review and use only applicable verified facts in Listing Draft and image copy.

## Workbook and copy

- Use the current canonical `assets/listing-workbook-template.xlsx`. Preserve Product Details, Offer and Safety&Compliance, their exact field names and Definitions, all 294 current attributes, formatting, status menus and units. A future reviewed template change must enumerate its actual fields; do not silently discard fields to fit the old count.
- Each sheet has seven rows: **Field / Attribute**, **Definition**, **Value**, **Status**, **Source**, **Value Candidate**, **Value Candidate Source**. Map by worksheet plus exact field name, not column position or a similar name. Freeze and wrapping must keep long copy and evidence readable; retain the canonical layout rather than redesigning each run.
- Deliver an English Item Name, five complete bullet paragraphs in the single Bullet Point cell, and a Product Description containing literal HTML. Apply the current title, base sold configuration and fixed warranty/disclosure rules in SKILL.md and listing-style-guide.md. Candidate claims, TBD and internal research warnings never enter customer copy.
- A full Excel request produces a current **LISTING_DRAFT** as well as the separately identified **RESEARCH_REVIEW** and its summary. Early research handoff remains permitted and useful, but is explicitly partial and never reported as completed full Excel delivery. If evidence prevents honest copy, identify the exact blocked fields rather than inventing claims or silently omitting the copy.

## Every attribute gets a disposition

Use [operations preflight](research-operations-preflight.md) to exhaust independent technical research before one consolidated missing-fact request. Preserve an instruction to defer seller-only price/SKU/GTIN/quantity fields; keep their honest TBD disposition without stopping unrelated technical research or a permitted PARTIAL draft. This does not waive final export requirements, style approval, actual QA or publication review.

Classify by the field's Definition and evidence requirements, not simply by its worksheet or whether its Source contains an ERP URL:

1. **Seller/account/operational inputs:** preserve supplied values and confirmed seller policy. Research completion does not invent price, inventory meaning, shipping settings, licensing eligibility or legal declarations. Missing inputs stay TBD with SELLER_INPUT_REQUIRED, the specific input and responsible party. Do not fabricate candidates for these inputs. The user's instruction to leave this class alone does not erase already confirmed policy or block later explicit seller input.
2. **Technical facts needing exact configuration/unit confirmation:** search exact OEM SKU/region documentation, ERP-linked current/historical units and OEM as-built parts; reconcile factory evidence with the sold base configuration. Record conflicts and applicability limits. An inaccessible page is a failed attempt, not evidence that the value is absent or zero.
3. **Technical attributes recoverable from authoritative documentation:** research exact OEM specifications/manuals, component-manufacturer documentation and relevant regulatory sources. Follow links, alternate official versions and part-level evidence where useful. Component evidence establishes the component only. Do not stop at an empty ERP field or a generic series page.

For classes 2/3, perform the initial evidence chain and then targeted deep research across the applicable routes in research-attribute-coverage.md and serial-number-product-research.md. Record queries, URLs/document sections, access date, findings, failed access, excluded near-matches and official conflict decisions. Only use “Not found after research” after the relevant routes and promising leads are complete and further distinct targeted queries yield no new evidence. Keep incomplete, blocked, identity/configuration-unverified and conflicting outcomes separate using the existing Status/reason fields. Exhaustion documents the remaining proof needed; it does not guarantee every cell can be filled or require equivalent searches indefinitely.

For each field choose one outcome:

| Evidence outcome | Value / Status | Candidate rows and explanation |
| --- | --- | --- |
| Exact field/configuration is confirmed | Confirmed value and VERIFIED, with source | Both candidate cells blank |
| Matching official evidence resolves an ERP/Amazon disagreement in the same scope | Official supported value and VERIFIED if applicable to the selected configuration | Retain rejected values and the official decision in the evidence; factory-only evidence does not verify sold applicability |
| One best defensible possibility remains unconfirmed | Value blank; honest unresolved status | One literal candidate and citation; explain why ranked first and what would confirm it |
| Genuine conflicting evidence or tied alternatives | Value blank; CONFLICT or applicable unresolved status | Do not force a winner; retain alternatives, conflict and next proof in Source/evidence |
| No supporting value/candidate after completed applicable deep research | Value blank; TBD | Both candidate cells blank; Source/evidence says Not found after research and records coverage, limitations, owner and next action |
| Research incomplete, access blocked or identity/configuration unverified | Value blank; TBD, SOURCE_UNAVAILABLE or evidence-backed INPUT_UNVERIFIED as appropriate | State the actual limitation and follow-up; never label it not found merely because a page failed |
| Proven not applicable | NOT_APPLICABLE with basis | Both candidate cells blank; silence in a spec sheet is insufficient |

Use the candidate properties and paired-row validation in candidate-review-rows.md. Candidate sources must support the proposed field/configuration, not merely name a broad website. Never promote a candidate to Value to reduce unresolved counts. Preserve final_value null until independently reconciled and verified. Include unresolved totals **including fields with candidates**, with reasons and next actions, in the accompanying summary.

## Repeated factual pitfalls to check

- CPU base speed is distinct from maximum/boost speed; missing published base frequency stays unresolved. Keep exact CPU suffix conflicts visible.
- Memory data rate in MT/s is not the physical clock in MHz/GHz. Label any justified inference and its conditions as a candidate rather than silently changing units.
- Integrated/shared graphics does not establish a fixed installed VRAM capacity. Native panel resolution is distinct from maximum external/display-engine resolution.
- Distinguish installed, optional, maximum, starting and measured values: RAM/SSD, weight, battery, accessories and ports must match their Definitions and scopes.
- Preserve L1/L2/L3 versus total cache; USB connector versus protocol counts; battery Wh/cells versus pack count, runtime, health and shipping declarations. Do not infer one from another merely to fill a column.
- Exclude near-match regional SKUs, optional configurations and unrelated unit records. Source specificity and sold applicability are required even when a value looks plausible.

## Acceptance and current delivery

Before delivery, validate current ledger-to-template projection, candidate/source pairs and rationale/missing-proof, copy presence/format/warranty, identity, configuration scopes and numeric units. Review the actual workbook's long copy and evidence for readability. Structure tests cannot authenticate product facts, visual quality, licences or Amazon eligibility. Do not add an export gate that forces unresolved research into false certainty; honest drafts may remain PARTIAL.

Keep a single current `03_RESEARCH/FINAL` per product, reuse its known IDs and preserve superseded coherent bytes in the existing archive. Keep one current Listing Draft under `01_LISTING` and link it from the current research entry/summary. Independent run records remain under `30_RUNS`; do not create dated sibling FINAL deliveries. Upload original individual XLSX and selected evidence, read back actual IDs, parents, MIME, size and available byte checksums, then update current links and scoped delivery receipts. GitHub receives reusable workflow changes only.

Every generation records the exact workflow SHA, separate workflow-backup status, actual product-delivery status and unresolved follow-ups. Follow github-drive-sync.md for workflow backup; copying an Excel to Drive is not proof that the workflow was backed up. The Drive baseline README remains unchanged.
