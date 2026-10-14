# Scoped ledger, workbook projection and export evidence check — 2026-10-14

Apply [serial-number-product-research.md](serial-number-product-research.md), [research-attribute-coverage.md](research-attribute-coverage.md) and the FCC-specific reference. Research drafts may contain honest unresolved fields; export evidence checks are a separate stage, not a prerequisite for doing research or delivering a draft.

## Canonical structure for new research

Use [research-ledger-schema.json](../assets/research-ledger-schema.json) for new `research-ledger.json` files. The root has `schemaVersion:1`, `productId`, `configurationId`, `facts` and `fields`. This is the single product research ledger; record each scoped fact separately within it, not in competing ledgers. Keep detailed sanitized part/source/unit metadata inside each fact's `evidence` object.

- `facts` have unique IDs, exact `sheet`/`attribute`, `configurationId`, `fact_scope`, `status`, `final_value` and a nonblank `source`/disposition. FACTORY and CURRENT_UNIT facts remain supporting evidence. Create a separate SOLD_BASE fact with `applies_to_sold_configuration:true` and a specific `transfer_basis` only after the actual unit/configuration and changes are resolved. Do not merely relabel a factory fact. Keep original facts and their evidence.
- `fields` map each actual template field exactly once to `selected_fact`. They must cover the current three worksheets' attributes exactly, without duplicate or invented fields. The selected fact must match the attribute and target configuration. No new workbook columns are introduced.
- Installed fields and all unlisted fields require SOLD_BASE scope. The explicit capability allowlist in scripts/research_export.py additionally allows PLATFORM_CAPABILITY for existing RAM maximum, maximum display-resolution/brightness, maximum CPU speed and maximum supported monitor fields (and their existing unit fields). Offer maximum price/order quantity are seller facts, not hardware capabilities. Capability evidence must still match the target configuration. Review the allowlist against Definition when template fields change; never silently treat an installed field as a maximum.
- Unresolved states have `final_value:null`. NOT_APPLICABLE also has a null value and a field-specific source/disposition. VERIFIED requires a value; every VERIFIED SOLD_BASE selection requires applicability and transfer basis. The six existing statuses remain unchanged.
- A research-only recommended FCC ID uses INPUT_UNVERIFIED, `recommended_candidate`, and null `final_value`. Draft projection displays the candidate in AF with an automatic `MOST_LIKELY_CANDIDATE — NOT CONFIRMED` Source prefix. Alternatives and ranking stay in evidence. Other unresolved fields project blank values with their status/disposition. Customer-facing listing copy uses verified facts only.
- A VERIFIED FCC ID needs the exact text identifier, HOST/RADIO_MODULE `evidence_scope` and `authorization_route:certification`, plus the SOLD_BASE applicability/basis. An SDoC is recorded in the separate authorization/contact fields, not placed in FCC ID. A recommended candidate cannot be exported, even if someone changes its status to VERIFIED. Removing the candidate flag without obtaining evidence is not verification.

Example: retain a FACTORY RAM fact of 16GB and a SOLD_BASE RAM fact of 32GB backed by the seller's assembly record. Map the installed RAM field to the 32GB fact. Keep the 64GB maximum as a separate PLATFORM_CAPABILITY fact and map only the applicable maximum field to it. If sold RAM remains unknown, select a SOLD_BASE TBD fact, not the VERIFIED factory fact.

## Draft projection and CI

`scripts/research_export.py` provides `project(...)` for generation and `verify_workbook(...)` for checking exact Value/Status/Source projection. Use these helpers when constructing new workbooks; preserve the existing template topology and copy/warranty checks. All workbook Value/Status/Source cells must match their selected ledger facts, including the candidate warning. Formula cells are rejected.

Run in the dedicated listing-testing environment from the repository root:

```bash
python scripts/research_export.py --ledger 'product generated photo/PRODUCT-ID/research-ledger.json' --workbook 'product generated photo/PRODUCT-ID/RESEARCH_REVIEW.xlsx' --mode draft
```

The existing check-workbooks.py automatically checks draft projection when a product folder's research-ledger.json is a scoped object. CI exercises this through the normal workbook check. Legacy array ledgers retain structural-only draft validation; they cannot pass this new export check. Do not automatically migrate them or infer missing applicability/transfer evidence. Reconcile them manually when that product is next researched or exported. Current top-level workbooks must have reconciled selected values. Preserve an earlier stage that must stay unchanged using [hash-bound historical stage snapshots](workbook-stage-snapshots.md), rather than validating it against the latest ledger or rewriting its history. Snapshot CI checks preservation; snapshots are excluded from current projection and blocked from export.

## Mandatory pre-export evidence check

Apply [workflow validation boundaries](workflow-validation-boundaries.md): formal export additionally binds product-facts identity/configuration and productFactsSha256, checks core sold PC completeness/copy/numeric-unit consistency, and rejects formulas in Value, Status and Source. A marketplace adapter must match all four current input hashes. Drafts retain honest unresolved fields.

Before any marketplace upload, API export or saved Seller Central update from a workbook, run:

```bash
python scripts/research_export.py --ledger 'product generated photo/PRODUCT-ID/research-ledger.json' --workbook 'product generated photo/PRODUCT-ID/LISTING_DRAFT.xlsx' --mode export --stage LISTING_DRAFT --product-id PRODUCT-ID --configuration-id BASE-CONFIGURATION-ID
```

Use the actual filename and declare LISTING_DRAFT explicitly for export. A filename cannot grant export eligibility: export always requires product-facts.json with verified identity.oemBrand and runs the mandatory listing-copy/warranty checks, even for a renamed or research-named file. RESEARCH_REVIEW is draft-only; use --stage RESEARCH_REVIEW for its draft check when needed. Historical snapshots cannot be exported. Select the target IDs independently and compare them to the ledger; do not use a related historical unit's configuration. All selected fields must be VERIFIED or evidenced NOT_APPLICABLE. Unknown/TBD/conflicting/unavailable fields, recommended candidates, factory/current-unit values mapped as sold, wrong configuration, missing field mappings, formulas, or workbook edits that disagree with the ledger fail with nonzero exit status. Value/Status/Source matching is type-aware: bool and number, or text and number, never match; Excel numeric 1 and 1.0 may match.

Export binds to the repository's current canonical template, including its required FCC/status inputs. --template may identify a byte-identical copy; an old or altered template is draft/debug-only and cannot produce an export pass. The receipt binds templateSha256, workbookSha256, ledgerSha256 and productFactsSha256; input changes during validation fail. Re-run after any of those inputs changes. Output is a local JSON evidence-check result with input hashes and projected fields; it is not an Amazon upload file and sends nothing to Seller Central. Any future marketplace adapter must require a fresh successful result matching all four actual input hashes, LISTING_DRAFT stage and target IDs, plus the existing factual/channel review.

`EXPORT_EVIDENCE_CHECK_PASS` means recorded scopes, states, mapping and workbook values passed these checks. It does not authenticate the manufacturer's documents, confirm actual installation, verify licensing, satisfy marketplace-specific schema/mandatory fields, or establish Amazon eligibility. Existing copy, seller review, account/category, compliance and publication checks remain required. Unsaved UI trials remain drafts and must visibly distinguish any candidate from confirmed information.

Serial-bearing URLs, labels and alias mappings remain private under the serial research policy. Public evidence uses sanitized references; passing schema validation is not privacy review.
