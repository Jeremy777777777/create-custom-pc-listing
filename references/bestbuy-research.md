# Mandatory Best Buy research — user decision 2026-11-16

Best Buy is a mandatory, medium-priority source for every product-research run: new full Listings, research-only work, factual revisions and missing-fact research for images. Search it even when OEM/ERP evidence already supplies the requested facts. A purely visual edit that performs no product research does not expand into full research. Workflow-only maintenance and standalone FCC lookup retain their scope. This decision does not retroactively certify or rewrite old products.

## Purpose and authority

Use Best Buy for both **cross-validation** of researched values and **supplemental retrieval** of missing specifications, exact identifiers, original configuration details, manuals and useful official-source leads. Medium priority means a required supporting source, below matching OEM official evidence and target-linked ERP reconciliation; consult it before lower-priority Amazon/other retailer leads. Mandatory frequency does not make its claims primary evidence. Preserve the separate ERP-primary MegaPC own-brand branch.

A Best Buy page cannot override matching official evidence, establish a later MegaPC upgrade or independently promote a technical fact to VERIFIED. Several retailers repeating a claim do not equal independent OEM confirmation. When OEM evidence is missing, retain Best Buy's strongest applicable value as a sourced, qualified candidate and continue official/component/deep research. Formal Value, customer copy and export keep their existing factual gates. A conflicting retailer value does not demote an otherwise resolved official fact; preserve the comparison and resolution.

## Required search on each run

1. Establish the exact target through the existing ERP/official identity route. Search Best Buy using the verified OEM model and full manufacturer part number/SKU, with useful punctuation/spacing variants. Search by a verified UPC/GTIN or Best Buy SKU when available. Never send internal serials, credentials or private ERP records to a retailer.
2. Use Best Buy's public search and/or targeted web queries such as `site:bestbuy.com "<verified manufacturer part number>"`; open promising product pages and their actual Specifications, overview and linked documents. Search snippets are discovery leads, not reviewed specifications. If direct access fails, try accessible public indexed routes, preserving their limitations. Do not bypass login, CAPTCHA or access restrictions.
3. Check exact model/part number, regional variant, CPU/GPU, original RAM/SSD, display, colour and form factor. Record Best Buy SKU, actual seller/marketplace attribution and new/open-box/refurbished condition when shown. A retailer SKU is not the manufacturer part number. Related models are explicitly excluded or labelled family-only leads, never merged into the target.
4. For the facts in scope, compare Best Buy with OEM/ERP findings: original versus installed/sold configuration; capacities; display; ports/wireless; dimensions and weight; battery/power; accessories and other applicable missing attributes. Compare only like units and scopes. Preserve source units; convert physical dimensions into inches under the existing dimension policy. Do not turn a platform option, maximum or package weight into the unit's installed value or net weight.
5. Follow useful new identifiers, official documents and component leads. Record agreements, differences and information that Best Buy adds. A fresh, actual Best Buy search is required for each new research run even when prior stable research is reused. Within one run, reuse one reviewed page/search across fields with explicit applicability rather than repeating identical searches.

## Record the attempt and field comparisons

Use the existing single ledger, not a second fact database or new workbook columns. For affected technical facts, record Best Buy in `evidence.research_trace.routes` as `route: DEEP`, with Best Buy explicitly identified in `query`/`detail`, the actual sanitized search/product URL in `reference`, actual `reviewed_date` and an existing result (`REVIEWED`, `NO_MATCH`, `BLOCKED` or `NOT_STARTED`). Do not invent a new `BESTBUY` route enum. Preserve all other required route categories. Shared searches retain their actual date and reference on each relevant field.

In the existing evidence object, retain excerpts/section references and a comparison identifying the field, OEM/ERP value, Best Buy value, exact identity and FACTORY/CURRENT_UNIT/SOLD_BASE/PLATFORM_CAPABILITY scope, agreement/difference, adopted value or candidate, reason and remaining confirmation. Summarize substantive comparisons and the Best Buy search outcome in the existing Research Review Source/notes and coverage/run summary; expose any supported unresolved candidate under the current candidate-display policy. Supplemental information must be traceable to the actual page, never guessed from an inaccessible page.

Completion review must explicitly check:

- Was a real Best Buy search performed during this run, with identifiers, queries, dates and actual references?
- Were useful matches inspected and in-scope values compared, with supplemental leads followed?
- Are variant mismatches, disagreements and source limitations retained, with proper authority and candidate qualification?
- Does the summary distinguish a reviewed exact match, related-only results, no exact match, access blocked and not yet searched?

Missing the search is unfinished research, not an optional-source omission. `NO_MATCH` means the documented searches found no matching listing, not that Best Buy lacks the product or a hardware feature. A blocked page remains blocked even if a snippet exists. If Best Buy offers no applicable information, record that limit and continue other sources; a genuine no-match or access block permits an honest PARTIAL review delivery and does not erase confirmed OEM facts. Do not claim research complete, successful cross-validation or new VERIFIED facts from an unperformed/blocked search. These are execution/review requirements; existing structural validators cannot authenticate that a website was searched.
