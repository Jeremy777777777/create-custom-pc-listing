# Value / candidate completeness — 2026-10-30

New Research Review and Listing Draft generation must use the supported research_export.py CLI and candidate_coverage_version: 2 in the scoped ledger. Version 1 remains readable as historical coverage, not the current new-generation contract. Historical read-only validation remains compatible; compatibility never grants new delivery readiness. Lower-level writer helpers are not a substitute for the generation CLI audit.

## Comparative recommendations and actual delivery

Do the research and comparison before treating an explanation as closure. For each supported unresolved candidate, record evidence.candidate_assessment (version 1): decision RECOMMENDED or TIED, primary_id (null for a tie), options, comparison, missing_confirmation, reviewed_date. Each option has id, value, optional unit, source, support, limitations and qualitative confidence HIGH/MEDIUM/LOW. A recommendation must identify the supported primary option and match the recorded hardware value_candidate. Explain why it outranks alternatives using exact identity, unit/BOM linkage, official model/configuration and hardware conditions; popularity, arbitrary averages, maximums, or desired output do not rank installed facts. Never invent probabilities. New version-2 generation rejects supported candidates without this comparison.

Before declaring TIED, follow available distinguishing leads such as motherboard/port variant, chassis material, original configuration/parts and linked purchase/SKU records. A genuine tie retains all supported values and the specific unresolved discriminator. RESEARCH_PENDING/BLOCKED with a useful known candidate must retain that candidate; an explanation alone is not a substitute for the strongest defensible recommendation. Source authenticity and whether the search was actually performed remain substantive review.

User priority — 2026-10-30: opening the Draft must immediately show the strongest supported candidate. This takes precedence over earlier instructions to leave the review candidate cell blank for a units/schema mismatch. Fix presentation conflicts in generation and saved-byte verification; a passing structural gate does not excuse an invisible candidate.

Apply scripts/candidate_ranking.py after Amazon projection. A units/schema mismatch may withhold the numeric Amazon projection but never the review display. Row 6 displays the original value AND unit with NOT CONFIRMED / RESEARCH ONLY; its paired review unit displays the research unit and an unresolved-mapping warning, not an incompatible approximate Amazon label. Row 7 retains confidence, comparison, alternatives, sources and missing proof. Keep machine numeric projection and formal Value withheld; do not relabel MT/s as MHz or derive a clock by division. The projection's candidate_display is review text, separate from value_candidate used for Amazon numeric gating.

New workbooks open on Candidate Review, a concise first worksheet with sourced recommendations before pending inputs and evidence links back to the unchanged seven-row template fields. Supported candidates withheld from numeric projection appear first. Saved-byte verification checks the actual opening sheet, displayed values, qualification and links. Deleting or hiding the review, opening another sheet, or erasing the row-6 candidate fails current full-draft delivery. Historical workbooks without this view remain readable as historical inputs, not a new-generation exemption. The HTML companion supplements the workbook; it cannot substitute for opening visibility. Tied alternatives remain tied; reference maxima retain their basis; absence of support never authorizes an invented candidate.

Close the task only after the requested product's actual workbook/ledger/summary were updated, coherently archived, uploaded to its established Drive IDs and read back byte-for-byte. A workflow push, a chat answer, or a generated candidate in memory is not product delivery. Report any undelivered product files separately; do not claim the current Draft was fixed when only reusable rules changed.

Review every actual template field and Definition individually. Keep verified applicable sold facts in Value, with the source and correct units. For an unresolved field, actively seek the strongest defensible candidate through the official/ERP/Amazon/deep-research chain. Use existing value_candidate, value_candidate_source, evidence.candidate_rationale and candidate_missing_confirmation. Keep the formal Value blank. Do not invent confidence percentages or promote a candidate to make the workbook pass.

The actual saved workbook uses row 3 Value, row 4 Status, row 5 Source, row 6 Value Candidate and row 7 Value Candidate Source. A candidate must be visible in rows 6–7, not only in chat or the ledger. Reopen saved bytes and compare them with the projected ledger after Amazon option and paired-unit rules. The coverage sidecar lists every unresolved field and its candidate/disposition; structure PASS is not research completion.

When no defensible single candidate exists, keep numeric candidate cells empty and put a field-specific disposition in row 7 through evidence.candidate_review. Required keys: decision, reason, missing_confirmation, next_action, owner, reviewed_date (YYYY-MM-DD). Decisions are NO_SUPPORT, TIED, SELLER_INPUT_REQUIRED, RESEARCH_PENDING or BLOCKED. TIED additionally requires at least two alternatives containing value and source. NO_SUPPORT requires genuinely exhausted research and a matching research_trace.candidate_decision; blocked/incomplete research is never not-found. These are honest partial dispositions, not a way to skip useful source routes. A generic TBD, a blanket compliance classification or a repeated boilerplate reason does not complete research.

Do not force a candidate for seller price, seller inventory, shipping decisions or unknown private inputs. Record exactly which seller input is missing. A pending/blocked disposition must name the remaining route/access and action. When an OEM maximum or factory part supports a useful reference, state its basis and current-unit limitation in candidate rationale/source; do not silently replace actual net weight with a maximum. Distinguish battery packs, cells and extra supplied spares. Battery chemistry and Amazon form-factor options are different attributes. Pair candidate numbers with correct candidate units; preserve original values/conversions.

Set evidence.candidate_basis to OEM_MAXIMUM, FACTORY_ONLY or FAMILY_CAPABILITY for those reference-only cases. The writer labels them QUALIFIED_REFERENCE, not MOST_LIKELY_CANDIDATE. The rationale/source must state the applicable basis and limitation. Such a reference remains excluded from formal Value and export.

Verified values that have no exact Amazon allowed option stay in the ledger. Use the closest actually observed allowed option in the candidate rows under amazon-selection-contract.md. The allowed choice and hardware applicability both need review; observed schema alone cannot prove the hardware. Do not reuse a different marketplace or conditional context as target confirmation.

New CLI generation rejects a missing contract marker, any unresolved projected field with neither a candidate nor a complete explicit review, and missing visible candidate support. Versioned projections, saved-byte verification, summaries and handoff checks repeat the coverage check. A changed candidate invalidates its summary and requires a new byte-verified delivery. Read the existing research/Drive revision rules before changing an old product; preserve prior coherent bytes and all factual limitations.

The independent FCC task remains outside Listing research. Its validated ERP_INVENTORY neutral handoff retains the current blank FCC layout and is counted as MANAGED_SEPARATELY, never as a researched candidate or an applicable resolved hardware fact. Explicit historical FCC reproduction remains historical; it cannot grant new-generation exemption.

Example review (illustrative schema only, not real research):

    "candidate_review": {
      "decision": "SELLER_INPUT_REQUIRED",
      "reason": "The seller has not supplied the Amazon offer inventory for this SKU.",
      "missing_confirmation": "Current offer inventory; ERP stock is a different quantity.",
      "next_action": "Obtain the seller's offer quantity before formal export.",
      "owner": "Seller account operations",
      "reviewed_date": "2026-10-30"
    }

Report verified values, sourced candidates and unresolved dispositions separately. Do not claim all fields have correct values just because every field has a recorded disposition. Future chat answers must use the same confidence/scope as the current ledger and explicitly state whether a workbook was updated.
