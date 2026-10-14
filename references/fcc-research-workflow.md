# FCC lookup and workbook mapping

Workflow addition approved by the user on 2026-10-13; ERP serial-first lookup and ranked candidate fallback approved on 2026-10-14. Apply during full listing research and when resolving FCC fields; image-only work does not require unrelated FCC research. Recheck current official guidance before a publication decision.

## Standard path: ERP serial → OEM configuration → part → FCC ID

Perform this path proactively before asking the user for a serial number or label. This is an evidence-gathering procedure, not an assumption that every OEM exposes configuration data or that every unit has the same radio.

1. **Find a linked unit in ERP.** Open the exact requested product and its linked child configurations, current inventory/serial records, and relevant historical purchase/receipt/sales records. Read only the minimum records necessary to identify the relevant unit or hardware batch. Prefer a current unit tied to the target sold configuration; next use a historical unit tied to the same OEM SKU/batch; then a related unit as a discovery lead only. Record whether the serial is CURRENT, HISTORICAL or USER_SUPPLIED and how it links to the ERP/internal product and target configuration. A multi-configuration parent, similar name or same CPU alone is not a unit match. Deduplicate repeated serials; do not guess missing serials or scan unrelated inventory. Historical ERP transaction records are permitted evidence here; archived workflow instructions/assets remain excluded under SKILL.md.
2. **Query the OEM with the serial/service tag.** Use the official manufacturer support portal and verify the returned commercial model against ERP. Open Original Configuration / As Built / Parts / BOM (or the manufacturer's equivalent). Record the exact wireless part number, module model, form factor/revision and applicable region; distinguish the actual hardware row from a driver/software bundle. For Dell, use the device's support page → Quick links → Product Specifications → Original Configuration, then expand the wireless-card hardware row. UI labels may change; follow visible controls. A driver-download list or general model specification with optional radios is not factory installation evidence. If a direct URL/search fails, try the official site's visible lookup UI; record login/access/no-data failures and continue independent official-module/host research.
3. **Resolve the part to an exact module.** Follow the OEM part record, module label, official parts/service documentation and component manufacturer's documentation. Preserve suffixes: a family such as AX211 alone may cover several module packages and FCC IDs. A form-factor/part inference must be identified as an inference, with the missing link stated. An OEM BOM verifies factory installation only: check available ERP repair/customization/replacement records for radio changes and whether the target unit/batch still matches. RAM/SSD customization alone does not prove or disprove a radio change. Do not transfer one serial's radio to an entire parent product or other stock batches.
4. **Match and validate the FCC identifier.** Follow the official label/module-document and FCC EAS checks below. Keep the chain explicit: target ERP record → unit/batch link → OEM serial result → hardware part → exact module/version → FCC ID. Record host SDoC separately; a service tag, regulatory type or part number is not an FCC ID.
5. **Return a usable result even when incomplete.** Give either a confirmed identifier with its unit/batch scope, a clearly labeled most-likely candidate with the missing verification, an unresolved tie, or no defensible candidate. Include the host authorization evidence independently. Do not stop at “send a label” before attempting available ERP/OEM research. Request only the smallest remaining evidence after explaining what was established.

Keep raw serials, unredacted labels, private ERP screenshots and serial-bearing OEM URLs in the private working evidence only. Public GitHub records use a local evidence alias such as UNIT-A, a non-sensitive product/configuration reference and sanitized source links without serial query/path parameters. Do not publish the alias-to-serial mapping. Public module IDs and official non-unit regulatory documents may be cited normally.

## Confirmation and most-likely candidate fallback

Use the existing six field statuses; confidence/ranking is additional metadata, not a seventh status.

| Evidence outcome | Workbook/ledger treatment | User-facing result |
| --- | --- | --- |
| Exact target unit/batch, exact module and official ID mapping established; no unresolved material installation contradiction | VERIFIED with evidence scope and installation basis | Confirmed ID, applicability and whether evidence is factory configuration or current inspection |
| Factory BOM/part known but module suffix inferred, current-unit continuity unconfirmed, or only a matched historical unit available | INPUT_UNVERIFIED; candidate separate from verified final_value | Most likely candidate, conditional on the stated missing link |
| Material sources disagree or equally supported IDs remain | CONFLICT, preserve alternatives | Explain the conflict/tie; no arbitrary winner |
| No evidence-linked ID can be proposed | TBD, or SOURCE_UNAVAILABLE when access is the blocker | No defensible candidate; attempted paths and next evidence |

Rank evidence-linked candidates in this order: target-unit OEM hardware BOM/label; same-SKU/batch historical OEM BOM; exact part-to-module official documentation; exact-model official optional-module documentation; third-party discovery leads. Evaluate the complete chain, not a single strong link: an official grant alone cannot outrank missing installation evidence. A retailer/mirror-only ID remains a discovery lead, never a VERIFIED ID. An optional-module list alone cannot establish a uniquely preferred installed module. Do not invent an ID or choose the most popular option to satisfy the fallback.

If one candidate is better supported, explicitly recommend it as **MOST_LIKELY_CANDIDATE — NOT CONFIRMED**, even when full verification is unavailable. Use qualitative confidence HIGH / MEDIUM / LOW with a concrete rationale, not invented percentages. For each plausible alternative record why it ranks lower and what would distinguish it. When evidence does not distinguish candidates, report a tie. If none has a defensible link, report that rather than fabricating a recommendation.

Candidate delivery format:

```text
Result: MOST_LIKELY_CANDIDATE — NOT CONFIRMED
Recommended FCC ID: <exact evidence-linked identifier>
Scope: RADIO_MODULE / <module and version>
Installation basis: <current/historical factory BOM or other evidence>
Confidence and reason: <HIGH/MEDIUM/LOW; strongest link and remaining gap>
Alternatives: <other supported IDs and ranking reasons, or none established>
To confirm: <specific label, exact suffix, replacement record or batch check>
Export: blocked pending verification; research draft only
```

Research ledger additions for this chain: `unit_evidence_alias`, `serial_source_kind`, `erp_record_reference`, `target_configuration`, `batch_match_basis`, `oem_configuration_source`, `oem_part_number`, `module_model`, `module_variant`, `installation_basis`, `replacement_check`, `candidate_values`, `recommended_candidate`, `candidate_confidence`, `ranking_reason`, `missing_links`, `confirmation_action`, `final_value`, `status`, `evidence_scope`, `authorization_route`, `sources_attempted`, and `reviewed_date`. Source entries include document title/page/date and access result; sanitize public URLs. These are ledger metadata, not new workbook columns. For unresolved candidates keep `final_value` unset; a research draft AF Value may show the single recommended candidate with INPUT_UNVERIFIED and an explicit candidate warning in Source. Keep alternatives in the ledger/Source, not concatenated in the ID cell. Clear any prior final value that new evidence has invalidated and record the conflict rather than silently replacing it.

Before Seller Central or other marketplace export, independently verify that only VERIFIED identifiers applicable to the sold configuration are exported. Never auto-promote a candidate because it was placed in AF, approved as a research recommendation, or passed structure tests. Candidate research is a valid deliverable and does not block other independently verified research work; it remains an explicit FCC publication gap.

## Find evidence for the exact sold computer

1. Record the ERP/internal ID, OEM model/SKU, regulatory model/type and region. Where a radio is installed, identify its exact Wi-Fi/Bluetooth/WWAN module from assembly records, OEM configuration, module/host labels or electronic regulatory labels. If installation is unknown, record that gap and research the host in parallel. A list of optional radios is not installation evidence. Do not expose serial numbers or private labels in public GitHub records.
2. Search the OEM support/compliance portal for the exact commercial AND regulatory model: `site:<OEM-domain> "<model>" FCC`, `"<regulatory model>" "Supplier's Declaration of Conformity"`, and `"<model>" regulatory information`. Open the actual US compliance statement, regulatory guide or label; an EU CE declaration is not US FCC evidence. Save URL, document title/date, page and the model identifiers establishing the match.
3. Transcribe `FCC ID` / `Contains FCC ID` exactly from the verified label or official module documentation. Preserve hyphens and distinguish the host from each installed transmitter. Do not substitute a Dell/HP regulatory model, service tag, FRN, IC/ISED number or FCC logo for an FCC ID. Never choose one of several optional module IDs just because it supports the advertised Wi-Fi standard.
4. Look up the candidate in the [FCC Equipment Authorization System](https://apps.fcc.gov/oetcf/eas/reports/GenericSearch.cfm), reached from the [FCC ID search page](https://www.fcc.gov/general/fcc-id-search-page). Enter the grantee and product portions as identified by the official record; preserve the product-code hyphen. Review the grant/applicant, equipment description/model, authorization date and relevant label, manual and integration exhibits. The applicant may be the radio-module maker, not the computer OEM. A matching grant establishes the module record, not proof it is installed in this computer or that the host is compliant.
5. For an SDoC route, retrieve the matching US compliance information statement and its responsible party. Research the name, US address and supplied telephone/Internet contact from that document. Do not manufacture the contact from a generic support page or substitute the seller automatically. A certified module and a host SDoC can coexist; record both with their scopes.
6. If the official system is unavailable (403, timeout, unavailable exhibit), record the query, date, failure and any independent OEM evidence. Do not claim a database lookup succeeded. Third-party FCC mirrors and retailers may locate candidates, but do not independently establish a verified grant or exact-unit match. Keep unresolved evidence pending and identify the required label/configuration/document and owner.

## Authorization route and evidence scope

Under [47 CFR 15.101](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-15/subpart-B/section-15.101), Class B personal computers may use SDoC or certification. Therefore no database result or no visible FCC ID does not mean the computer is exempt or noncompliant. [47 CFR 2.1077](https://www.ecfr.gov/current/title-47/section-2.1077) identifies the compliance-statement information for SDoC, including the product and US responsible party. An OEM statement or module grant is not a blanket conclusion for every customized assembly; check the marketed configuration and applicable integration conditions separately.

Extend the existing research ledger entries, rather than creating competing product facts. Add `evidence_scope` (`HOST`, `RADIO_MODULE`, or `UNRESOLVED`) separately from `authorization_route` (SDoC, certification, or unresolved). Record exact OEM/regulatory/module model, candidate FCC ID(s), installation evidence when relevant, grant or SDoC URL/document/page/date, searches attempted, reviewed date, status, reason and next action. A verified module grant with unconfirmed installation stays a candidate, not a VERIFIED sold-product FCC ID. Keep multiple installed transmitter IDs separate in the ledger; check the marketplace field's supported format before exporting them.

## Existing template fields

The canonical template already includes these columns in `Safety&Compliance`; preserve their names, definitions, and the five-row `Field / Attribute`, `Definition`, `Value`, `Status`, `Source` layout. Do not add a second generic FCC column or overwrite published product workbooks to simulate completed research.

| Column | Header | Fill from |
| --- | --- | --- |
| AD | FCC Radio Frequency Emission Compliance | Matched US FCC compliance evidence, with scope in Source |
| AE | Radio Frequency Emission & Authorization Status | Evidenced authorization route; match current marketplace permitted values at export |
| AF | FCC ID | Exact host/installed transmitter identifier, stored as text; a research-only recommended candidate uses INPUT_UNVERIFIED and an explicit warning in Source; unresolved conflicts keep alternatives in ledger/Source and no single asserted ID |
| AG | SDoC Contact Name | Matching statement's responsible-party contact |
| AH | SDoC Contact US Mailing Address | Matching statement's US address |
| AI | SDoC Contact Email Address | Supplied email/contact, following this column's Definition |
| AJ | SDOC Contact US Phone Number | Supplied phone/contact, following this column's Definition |

Leave the template's Value/Status/Source cells blank; these instructions are guidance, not product values. The FCC ID Value input has text formatting and an input prompt; the Source input reminds users to include host/module scope and evidence. All future Research and Listing workbooks must cover these fields individually.

Use the six statuses defined in [research-attribute-coverage.md](research-attribute-coverage.md) consistently in the ledger and workbook. `VERIFIED` FCC ID requires an actual identifier, not `TBD`, `FCC`, `Yes`, `No`, `SDoC` or `N/A`. An inaccessible source or unknown installation remains unresolved with its specific reason/next action. `NOT_APPLICABLE` needs evidence for that individual field: a host SDoC may explain no host FCC ID, but does not settle radio-module IDs or make all FCC fields inapplicable. Keep explanations in Source/ledger rather than the ID Value.

## Review before delivery/publication

Check host versus module scope, actual installed configuration, exact ID transcription and evidence links; ensure responsible-party details come from the matched statement. Report unresolved FCC items alongside other compliance gaps. Do not mark applicable FCC compliance READY while these remain unresolved. Structure checks can reject a blank/placeholder VERIFIED ID; they cannot authenticate an FCC grant, installation, SDoC applicability, or Amazon acceptance. Research drafts may be delivered with honest unresolved statuses.

Procedure update date: 2026-10-14; regulatory references last reviewed 2026-10-13 (no new legal review claimed). Source-access failures during an individual lookup belong in that product's ledger; they are not a permanent condition of this workflow.
