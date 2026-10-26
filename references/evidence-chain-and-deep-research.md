# Listing evidence chain and deep research — user decision 2026-10-26

Apply automatically to new Listing generation, revisions and missing-fact research. The user does not need to repeat the procedure. This reference governs source priority, conflict resolution and when research may report a field as not found; read it with the scoped ledger, serial-research and attribute-coverage references. It supersedes older ERP-first technical authority and examples that select an ERP value over conflicting official evidence. It does not retroactively certify or rewrite historical products.

## 1. Identity lookup and evidence priority

**Manufacturer official website research (serial/service-tag lookup plus official exact-product search) > ERP > Amazon search. When product information conflicts, use the matching official website research as the authority. ERP, tracker, Amazon and other secondary sources cannot override it.**

If only an internal computer ID is supplied, use [exact-ID ERP lookup](erp-internal-id-lookup.md) first to establish the target and obtain the available OEM model, SKU, part number and linked serial references. This is identity discovery, not a change to evidence priority. Do not invent numeric ERP IDs, serials or model matches. Reuse exact current product records and earlier verified research as leads, checking their identity, scope and current applicability.

For each applicable product attribute:

1. **Serial-first official research:** the user confirms most products have linked serials. Start with the current target's linked serial/service tag, verify the returned model/SKU, collect its available as-built/BOM details once, and follow exact component/part numbers. Prefer current-unit linkage; historical units require explicit SKU/batch/configuration linkage and cannot establish all current inventory. Then use exact-model/SKU/region official search to fill remaining gaps. Missing serials or unavailable lookup require a recorded exception and continued model research, not repeated requests for a URL.
2. **ERP reconciliation:** inspect the exact detail, Specification and relevant linked configuration, inventory, purchase, assembly or upgrade evidence. Compare it with official findings and preserve both source values and their scopes.
3. **Amazon search:** search verified identifiers, open matching variants and record material differences. Review up to three useful accessible exact/related listings under the existing workflow; do not force unsuitable matches. Similar models and search snippets are discovery leads. Amazon/retailer claims cannot independently establish VERIFIED technical facts.

Seller/account-only fields such as internal SKU, price, inventory meaning and shipping settings still require their actual business sources. Official specifications cannot establish those inputs. Confirmed seller OS/warranty wording remains seller policy, not proof of OEM hardware, licensing or manufacturer warranty eligibility; report factual contradictions rather than inventing evidence or silently changing the policy.

## 2. Resolve conflicts through official research

Match the exact product, variant, region, date and **FACTORY / CURRENT_UNIT / SOLD_BASE / PLATFORM_CAPABILITY** scope before comparing values. A family maximum, selectable option, historical unit or original shipment record does not automatically prove this unit's installed sold configuration.

- If matching official evidence resolves the same attribute and scope, adopt its supported value and retain the rejected ERP/Amazon value, citation and resolution reason in the research evidence. A resolved lower-priority disagreement need not leave the adopted official fact in CONFLICT.
- If ERP reports a later upgrade, retain it as a separately scoped claim. Do not use the upgrade label to bypass official priority. Official factory evidence alone establishes the factory value; it cannot establish either the upgraded sold value or that the factory value remains installed. Until applicability is verified and the discrepancy resolved, the affected sold field stays unresolved and unsupported capacity claims stay out of customer copy/images.
- If official pages disagree, investigate exact SKU/unit linkage, revision and scope using official sources. Do not pick a larger value, majority vote or an arbitrary official page. If no applicable official conclusion is defensible, retain CONFLICT and the required proof.
- If official research is silent or inaccessible, that is not an official negative finding. Continue the evidence chain and deep research, keeping the actual confidence/status; never describe an ERP or Amazon value as official confirmation.

Example: official lookup shows factory 16GB, ERP says 32GB and an Amazon variant says 64GB. Record all three with their scopes. Factory 16GB may be VERIFIED for FACTORY scope; neither 32GB nor 64GB overrides that finding. Do not automatically advertise 16GB as the current unit either. Research the current/sold configuration and keep its value unresolved until supported. A genuinely separate, verified later configuration remains separate from the factory fact, not a silent replacement of it.

For a later modification, require the exact internal ID/configuration or UNIT linkage, dated assembly/replacement record or current physical/system evidence, before/after values, installation evidence and reconciliation with the official factory finding. Store these in `evidence.sold_modification` under the [research trace contract](research-trace-contract.md). A title, generic upgrade claim, unrelated serial or similar Amazon variant cannot confirm installation. Matching official evidence still governs a genuine same-scope conflict. Keep seller OS/warranty assertions labelled seller policy; they do not authenticate OEM coverage or licensing.

## 3. Deep search for unresolved fields

Use [operations preflight](research-operations-preflight.md) for scoped official lookup authorization and consolidated remaining questions. Search available linked configurations/units and exact-model source assets before asking the user to choose capacities or supply photos. Keep image-style approval as the user's separate decision; independent research continues while it is pending.

After the initial chain, automatically continue targeted deep research for unresolved technical fields within the requested scope. Full Listing research covers every applicable template attribute; image-only work researches missing image-required facts without expanding into unrelated compliance work.

Follow applicable routes and promising leads:

- Exact model/SKU/part-number queries, useful identifier variants and regional/language variants; exclude near-matches explicitly.
- Official regional and legacy support sites, specification PDFs, service/maintenance guides, regulatory documents, configuration/BOM and official parts records.
- Exact component manufacturer documentation, preserving component versus whole-system scope; relevant authoritative certification records for regulatory questions.
- Relevant ERP purchase/receipt, configuration and replacement linkages and available current physical/system evidence, reconciled under official priority.
- Archived official documents and credible exact-variant distributor/Amazon sources as qualified supplemental evidence or leads; trace cited claims back to official originals where possible.

Do not stop at an empty ERP cell, missing serial, a generic series page, one failed query, a preset small search count or the first inaccessible portal. Do not ask the user to repeat the workflow or supply a URL that available identifiers can locate. Ask only for specific missing proof/access after independent research, stating what was attempted. Never request passwords or access unrelated private records.

Research may conclude for an attribute when its applicable routes and promising leads have been investigated, further distinct targeted queries yield no new matching evidence, and remaining access or identity limitations are documented. This is exhaustion of relevant research routes, not a claim to have searched the entire internet or a requirement to repeat equivalent queries indefinitely. If time/access prevents completion, report partial research rather than claiming exhaustion.

After applicable searches are exhausted without a confirmed value, actively select the strongest defensible candidate for each unresolved technical field. Record its literal value, source, identity/scope match, why it outranks alternatives and the missing confirmation. Use the existing candidate rows and unresolved status; never copy it into formal Value, customer copy or image claims. If no evidence supports a candidate, or alternatives remain tied, record NO_SUPPORT or TIED and why; do not fabricate precision/probabilities or force a winner. Seller-only inputs do not receive guessed candidates. This fallback applies beyond FCC fields.

## 4. Evidence record and honest missing outcomes

Use the existing single scoped ledger and six workbook Status values. Per-fact `evidence` already accepts research metadata; record field-specific details there and summarize them in Source/reason rather than introducing top-level schema keys, workbook columns or a new Status value. Keep per-field findings separate from the product-level `serial_research` outcome; a successful lookup does not complete all attributes.

New workbook generation follows [research trace contract](research-trace-contract.md). It makes serial-first starts, route dispositions, exhaustion and candidate decisions checkable in the existing evidence object. Historical records without traces remain explicitly unassessed by this new check; do not backfill invented searches.

For each researched field retain: target/configuration and scope; source title/URL or sanitized ERP reference; supporting excerpt/document page; actual access/review date; queries and routes attempted with their access/result; candidate and official adopted values; conflicts and resolution; excluded near-matches; completion/remaining gap; owner and next action where needed. Reuse recorded evidence rather than repeating identical queries across duplicate fields. Keep raw serials and serial-bearing URLs out of public GitHub records and ordinary shared delivery under the existing privacy rules.

| Research outcome | Existing workbook Status and handling |
| --- | --- |
| Applicable value confirmed | VERIFIED only for the supported scope/configuration; cite the evidence |
| Not researched / research incomplete | TBD with that explicit reason; do not say not found |
| No supporting value after completed applicable research | TBD; Source/evidence explicitly says **未找到 / Not found after research**, with search coverage, limitations and remaining proof |
| Access prevents a conclusion | SOURCE_UNAVAILABLE with blocked route and follow-up, even if other accessible routes were searched |
| Identity/current configuration not established | TBD, or INPUT_UNVERIFIED when an evidence-backed candidate exists; state the missing linkage |
| Genuine unresolved conflict, including official-source ambiguity | CONFLICT; preserve alternatives and next proof |
| Field demonstrably not applicable | NOT_APPLICABLE with field-specific evidence; missing information is insufficient |

“未找到” is permitted only after the applicable search is complete and no supporting evidence was found. It never means No, zero, absent hardware or NOT_APPLICABLE. A field may be missing for several reasons; explain them without collapsing blocked, incomplete, unverified or conflicting research into not found. Do not fabricate candidates for seller-only inputs or technical fields with no defensible candidate.

## 5. Carry the chain into the deliverables

Research Review and its coverage summary must explain the official findings, conflict decisions, completed searches and remaining limitations. Listing Draft uses only facts applicable to the base sold configuration; publishable copy and image selling points omit unresolved claims. Keep unresolved Value cells blank and use the existing separate candidate rows where supported. Honest PARTIAL review delivery remains permitted; neither exhausting research nor filling a template grants export or publication eligibility.

Follow [output Excel contract](output-excel-contract.md), [scoped projection](research-ledger-projection.md) and [Drive delivery](google-drive-delivery.md). Deliver original workbooks, final images and sanitized evidence to the established matching product folders, preserve prior coherent versions and verify bytes/parents. Workflow changes belong in GitHub; product business outputs remain in Drive. Automatic structure checks do not prove that sources were actually searched or their claims are true; review the field evidence before reporting research complete.
