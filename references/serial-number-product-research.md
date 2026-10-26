# PC research through ERP serials and OEM factory configurations

User-approved research method — 2026-10-14. This supplements all PC attribute research, not only FCC lookup. Apply during FULL_LISTING_WORKFLOW and when missing product facts need research. In image-only work, use it only for missing image-required facts; do not expand a targeted edit into unrelated research.

2026-10-26 update: [official evidence chain and deep research](evidence-chain-and-deep-research.md) governs source priority and completion. Official serial lookup plus exact-product website search > ERP > Amazon; matching official research governs conflicts. The initial ERP lookup below discovers identity/serials only. A failed serial outcome is not completion of every attribute's research, and missing serials do not excuse skipping official product search or targeted deep research.

## Standard procedure

Apply [operations preflight and official lookup authorization](research-operations-preflight.md) before submitting a linked unit identifier. The user-approved scope covers the current product's serial/service tag sent only to its matching listed manufacturer's official lookup, for the documented research purposes. Record target linkage, observed official destination and authorization source without exposing the raw serial in ordinary delivery. CAPTCHA/login and actual approval rejections retain their tool-specific requirements.

1. **Map the target.** Identify the exact ERP/internal product, OEM SKU, base sold configuration, region and relevant child record under [input-source-cross-validation.md](input-source-cross-validation.md). If ERP is accessible, proactively check its linked current inventory and historical procurement/receipt/sales serial records before asking the user for more information. Prefer a current unit tied to the target configuration, followed by a historical unit tied to the same SKU/batch. User-provided serials may enter the same process. Deduplicate serials and read only relevant records. A parent product, same CPU or similar name alone is not a configuration match. Historical ERP business records are permitted evidence; archived workflow instructions, old generated workbooks and historical image manifests remain excluded as fact sources.
2. **Look up the serial on the official OEM site.** Use Service Tag / Serial Number / Warranty Lookup / Parts Lookup and verify the returned model and SKU. Open Original Configuration / As Built / Parts / BOM or an equivalent hardware inventory. Dell example: support page → Quick links → Product Specifications → Original Configuration → expand relevant hardware rows. Use the manufacturer's visible controls; do not invent internal API endpoints. Record access failures, absent BOM data and lookup date. A model landing page, generic option list or recommended driver list is not unit-specific installation evidence.
3. **Collect the available factory details once.** Extract relevant parts and descriptions for CPU/GPU, RAM capacity/count/type/speed, SSD capacity/model/interface/form factor, wireless module, display/panel, keyboard/layout/backlight, camera/microphone, battery, power adapter, optional I/O modules, original OS and factory pack-out. Record exact part numbers, quantities, units and the manufacturer's wording before normalization. Expand ambiguous hardware rows instead of treating a software bundle or abbreviated label as a hardware fact. Not every OEM exposes every field; an absent row does not prove absence of a feature.
4. **Resolve parts with official documentation.** Use OEM part documentation, exact-model service/specification guides and the component manufacturer's documentation to interpret the exact part/revision. Keep unit-installed facts separate from platform capabilities and supported maximums. For example, a 5600-rated memory part does not alone establish the actual operating speed; a CPU's maximum memory speed does not establish installed RAM speed. A panel part needs an exact match before importing resolution, refresh rate or touch capability. Platform port totals need the actual optional-I/O configuration. Record any inferred suffix or unresolved part mapping as unverified.
5. **Reconcile factory, current and sold configurations.** Compare the OEM result against linked ERP assembly/upgrade/repair/replacement and fulfillment records, current system/label evidence if available, and the confirmed base sold configuration. Preserve factory RAM/SSD separately from seller-installed values. Factory OS does not override the confirmed Windows 11 Pro policy. Original keyboard/mouse/adapter pack-out does not prove the seller includes those items now; manufacturer warranty lookup is dated OEM coverage evidence, not a new seller warranty promise. Do not use warranty start/shipping dates as Model Year or infer a software licence/entitlement from a preinstalled application. Explain resolved differences and retain genuine conflicts.
6. **Map findings into the existing attribute ledger.** Reuse the one product fact ledger and current template fields; do not create a competing BOM-derived fact set or new workbook columns. Each supported attribute gets its own source, scope and status. An exact factory fact can be VERIFIED for FACTORY scope while the corresponding SOLD_BASE value remains TBD/INPUT_UNVERIFIED. Only transfer it to SOLD_BASE when the unit/configuration linkage and any relevant modifications are resolved. A related historical serial is a discovery lead, not proof for all current units. If linked current units differ, split evidence by child configuration/batch; never majority-vote or fill the parent with one unit's values.
7. **Close remaining gaps with targeted deep research.** Separately perform official exact-model/SKU search, reconcile ERP and search Amazon under the evidence chain, then follow applicable official regional/legacy support, manuals, exact parts/component documents, regulatory records and useful supplemental leads for unresolved fields. Missing serials, login requirements or unavailable OEM lookup do not stop independent research. Record field-specific queries, sources, outcomes and remaining proof. Only say not found after documented completion of the applicable routes; blocked, incomplete, unverified and conflicting findings remain distinct. Ask only for the smallest unresolved input after independent research. Apply [fcc-research-workflow.md](fcc-research-workflow.md) specifically for radio authorization and its ranked-candidate fallback; official priority also governs FCC conflicts.

## Field-level evidence and status

During an unsuccessful OEM lookup, preserve ERP/seller source discrepancies in the relevant fact's `evidence.source_discrepancies`; `serial_research.factory_sold_differences` is reserved for an actual completed OEM comparison. This prevents misclassifying source disagreements at entry. It does not authorize removing genuine differences, conflicts or facts to pass a validator; preserve the original evidence when a correction requires review.

New ledgers implement these scopes through [research-ledger-projection.md](research-ledger-projection.md) and its JSON schema. Keep FACTORY and SOLD_BASE as separate fact records in the same ledger; the template selects the applicable sold record, not whichever scope happens to be VERIFIED. Detailed unit/part/source metadata below lives under each fact's `evidence`; final value, scope, status and applicability use the schema's explicit fields.

Extend ledger entries with `unit_evidence_alias`, `serial_source_kind` (CURRENT / HISTORICAL / USER_SUPPLIED), `erp_record_reference`, `target_configuration`, `batch_match_basis`, `oem_configuration_source`, `oem_part_number`, `part_description`, `part_quantity`, `fact_scope` (FACTORY / CURRENT_UNIT / SOLD_BASE / PLATFORM_CAPABILITY), `factory_value`, `current_or_sold_value`, `modification_evidence`, `transfer_basis`, `sources_attempted`, `reviewed_date`, `status`, `reason` and `next_action` as relevant. Preserve raw and normalized values, source document/page/date and access outcome. These are evidence metadata, not additional workbook headers or status vocabulary.

- VERIFIED requires evidence supporting the precise field and stated scope; a verified FACTORY value is not automatically a verified SOLD_BASE value.
- INPUT_UNVERIFIED holds an evidence-linked candidate with its missing confirmation. Keep candidates out of final customer copy/marketplace export until verified. The FCC-specific recommended-candidate format remains in the FCC reference; this general procedure does not require guessing other missing attributes.
- CONFLICT preserves incompatible evidence until explained. Matching official research resolves lower-priority disagreements; retain the rejected value and decision. Conflicting official sources or unresolved scope remain open. Do not prefer the larger capacity or newer-looking serial automatically.
- TBD and SOURCE_UNAVAILABLE specify the missing information or blocked source and next step. NOT_APPLICABLE needs field-specific evidence, never merely a missing BOM row.

Example: OEM lookup establishes factory 16GB RAM and a particular SSD part, while ERP reports a sold 32GB/1TB upgrade. Keep the official factory fact and separately scoped upgrade claim with their sources. ERP cannot override the official factory result; neither the factory value nor the reported upgrade automatically proves the current sold configuration. Research and resolve sold applicability before using installed-capacity claims. RAM speed, SSD interface, available slots and pack-out need evidence for the actual configuration rather than inheritance from factory or Amazon variants.

## Recorded outcome and delivery gate — 2026-10-19

Keep one product-level `serial_research` object in the scoped ledger, alongside `facts` and `fields` (schemaVersion remains 1 for read compatibility). Per-field evidence still holds the actual hardware findings. New workbook generation and export checks require the record and `workflow_mode: FULL_LISTING_WORKFLOW`. Local/CI workbook checks require a record for new/changed top-level ledgers, workbooks and `.research-summary.json` files. Unrelated image changes do not require retroactive research. An unchanged legacy ledger without this object remains readable and is reported as `NOT_ASSESSED_LEGACY`; neither this update nor CI rewrites it or certifies a previous lookup. When updating a legacy array ledger, reconcile it into a scoped ledger before delivering new research.

Use these outcomes:

| Outcome | Meaning |
| --- | --- |
| `COMPLETED` | A linked unit's official factory/current configuration was obtained and at least one fact verified in its stated scope; unresolved attributes may remain explicit |
| `ERP_TARGET_NOT_FOUND` | ERP was searched but the target product could not be mapped |
| `SERIAL_NOT_FOUND` | Relevant accessible current/historical records yielded no linked serial |
| `ERP_UNAVAILABLE` | ERP access prevented the serial search |
| `OEM_UNAVAILABLE` | A linked serial was available privately but official lookup was inaccessible |
| `OEM_NO_BOM` | Official lookup did not expose a usable unit hardware configuration |
| `NOT_REQUIRED` | Image-only/adjustment scope reuses sufficient verified facts; explain why no new lookup is needed |
| `NOT_ASSESSED_LEGACY` | Historical execution has not been assessed; read-only compatibility, not valid for new research delivery/export |

Every assessed record has `workflow_mode`, `outcome`, a specific `reason`, ISO `reviewed_date`, sanitized `sources_attempted`, `units`, `resolved_fact_ids`, `factory_sold_differences`, `unresolved_fields` and `reconciliation`. Incomplete outcomes or remaining unresolved attributes require `next_action` and `owner`. A date is the actual review date, not a default inserted by a generator. A full research run cannot use `NOT_REQUIRED` or change its declared mode to bypass the check. Query failures remain deliverable Research Review outcomes; applicable unresolved facts still block export under the ordinary field gates. Successful serial lookup alone never means all attributes or current inventory are verified.

Example of an honest unsuccessful attempt (illustrative values only; do not copy as evidence):

```json
"serial_research": {
  "workflow_mode": "FULL_LISTING_WORKFLOW",
  "outcome": "SERIAL_NOT_FOUND",
  "reviewed_date": "2026-10-19",
  "reason": "Target mapped, but the relevant current and historical ERP records exposed no linked serial.",
  "sources_attempted": ["Sanitized target product and relevant receipt/inventory references"],
  "units": [],
  "resolved_fact_ids": [],
  "factory_sold_differences": [],
  "unresolved_fields": ["Unit-specific factory configuration"],
  "reconciliation": "",
  "next_action": "Locate the linked receipt or obtain a unit label privately.",
  "owner": "Assigned researcher"
}
```

For `COMPLETED`, each `units` entry records `unit_evidence_alias` (for example UNIT-A), `serial_source_kind` (CURRENT/HISTORICAL/USER_SUPPLIED), non-sensitive `erp_record_reference`, matching `target_configuration`, `batch_match_basis`, `returned_model`, sanitized HTTPS `oem_configuration_source`, and nonempty `fact_ids`. For a user-supplied unit with no ERP link, explicitly state that in `erp_record_reference` and explain the user-confirmed target linkage; do not invent an ERP reference. Each linked fact must exist in the same ledger/configuration with FACTORY or CURRENT_UNIT scope and the same `evidence.unit_evidence_alias`. `resolved_fact_ids` references VERIFIED linked facts, not sold facts inferred from the BOM. Keep unresolved findings among the linked facts with honest statuses. Explain the original/current/sold comparison in `reconciliation`; list differences separately, with an empty differences array only when the reconciliation explains no relevant difference. Retain sold applicability and transfer-basis requirements in the existing fact schema.

The generated `coverageSummary.serialResearch` includes the recorded outcome, unit/source scope, resolved fact references, differences and unresolved follow-up. Local/CI `workbook-ci-summary.json` lists recorded outcomes and untouched legacy products separately. Existing summaries without serial research remain readable only while their ledger is unchanged and has no new record. A changed record invalidates the summary's ledger hash and recomputed coverage. These checks assess record consistency, not whether the manufacturer was actually queried, the returned model is authentic, or the raw serial was fully redacted. Review all public strings and source URLs manually; automated screening only catches common serial-bearing URL patterns.

## Private evidence and public delivery

Retain raw serials, complete serial-bearing OEM URLs, private ERP screenshots and alias mappings only in private working evidence. Public GitHub ledgers/workbook Source cells use an alias such as UNIT-A, a non-sensitive product/configuration reference and sanitized source links without serial path/query parameters. Do not upload an unredacted OEM export simply to document research. Preserve traceability privately and cite public exact-model/part documents where available.

The research summary states whether serial lookup was attempted, current/historical evidence scope, attributes resolved, original-versus-sold differences and unresolved fields. Automated workbook checks verify structure, not the truth of BOM interpretation or whether a component remains installed. No existing product output is retroactively rewritten by this workflow update.
