# FCC lookup and workbook mapping

Workflow addition approved by the user on 2026-10-13. Apply during full listing research and when resolving FCC fields; image-only work does not require unrelated FCC research. Recheck current official guidance before a publication decision.

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
| AF | FCC ID | Exact host/installed transmitter identifier, stored as text; candidate values retain INPUT_UNVERIFIED or CONFLICT, with scope and evidence in Source |
| AG | SDoC Contact Name | Matching statement's responsible-party contact |
| AH | SDoC Contact US Mailing Address | Matching statement's US address |
| AI | SDoC Contact Email Address | Supplied email/contact, following this column's Definition |
| AJ | SDOC Contact US Phone Number | Supplied phone/contact, following this column's Definition |

Leave the template's Value/Status/Source cells blank; these instructions are guidance, not product values. The FCC ID Value input has text formatting and an input prompt; the Source input reminds users to include host/module scope and evidence. All future Research and Listing workbooks must cover these fields individually.

Use the six statuses defined in [research-attribute-coverage.md](research-attribute-coverage.md) consistently in the ledger and workbook. `VERIFIED` FCC ID requires an actual identifier, not `TBD`, `FCC`, `Yes`, `No`, `SDoC` or `N/A`. An inaccessible source or unknown installation remains unresolved with its specific reason/next action. `NOT_APPLICABLE` needs evidence for that individual field: a host SDoC may explain no host FCC ID, but does not settle radio-module IDs or make all FCC fields inapplicable. Keep explanations in Source/ledger rather than the ID Value.

## Review before delivery/publication

Check host versus module scope, actual installed configuration, exact ID transcription and evidence links; ensure responsible-party details come from the matched statement. Report unresolved FCC items alongside other compliance gaps. Do not mark applicable FCC compliance READY while these remain unresolved. Structure checks can reject a blank/placeholder VERIFIED ID; they cannot authenticate an FCC grant, installation, SDoC applicability, or Amazon acceptance. Research drafts may be delivered with honest unresolved statuses.

Reference review date: 2026-10-13. Source-access failures during an individual lookup belong in that product's ledger; they are not a permanent condition of this workflow.
