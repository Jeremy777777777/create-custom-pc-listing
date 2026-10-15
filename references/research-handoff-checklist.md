# Research handoff checks — 2026-10-15

This implements the existing research, base-configuration and delivery stages without changing workbook sheets/rows/fields, directory names or image slots. Use this checklist before declaring a stage complete; automation and factual/manual review remain separate.

| Handoff | Required evidence/check | Automation boundary |
| --- | --- | --- |
| ERP → target | Exact internal product ID, selected sold configuration and unit/batch linkage; Quantity meaning confirmed before using inventory | Directory/ledger identity is checked; ERP interpretation still needs source review |
| Serial/OEM → sold research | Preserve FACTORY/CURRENT_UNIT evidence; transfer only with sold applicability and a specific basis; sanitize serial-bearing records | Scoped ledger checks states/scope/basis, not whether the OEM interpretation is true |
| Research → workbook | Exact template projection; each field has a status/source; summary counts and unresolved follow-ups | `research_export.py` returns `coverageSummary`; a standalone summary uses the command below |
| Storage → listing | Installed base drive, total internal storage and other flash are distinguished; normalize units before comparison | Unexplained different `Memory Storage Capacity` and `Hard Disk Size` fail export; explicit component totals follow the contract below |
| Workbook → product directory | Canonical `product generated photo/<productId>/` must match ledger and independently recorded product identity | Draft/current-workbook and export checks reject a different folder; scratch/debug files outside this tree remain supported |
| Listing → export | Fresh four-input hashes, explicit target IDs and LISTING_DRAFT, verified applicable fields, current copy/unit checks | Export receipt is evidence checking only; actual account/category/schema/licensing/compliance checks remain separate |
| Facts → images | Current approved style, actual image claims and selected hardware; new supplied reviews bind current inputs | Image integrity/geometry/bindings do not establish visual fidelity, rights or Amazon eligibility |
| Local → GitHub | Commit/push, applicable CI, remote commit/file hashes | CI success alone does not certify factual completeness or publication readiness |

## Coverage delivery

Run in the selected `listing-testing` environment. Use actual filenames and target IDs:

```bash
python scripts/research_export.py --ledger 'product generated photo/PRODUCT-ID/research-ledger.json' --workbook 'product generated photo/PRODUCT-ID/PRODUCT-ID_RESEARCH_REVIEW.xlsx' --mode draft --stage RESEARCH_REVIEW --summary-output 'product generated photo/PRODUCT-ID/PRODUCT-ID.research-summary.json'
```

Every successful draft/export receipt includes per-sheet total/six-status counts, unresolved fields and their reasons, actions and owners. Detailed follow-ups come from the selected fact's `evidence.reason`, `evidence.next_action`, and `evidence.owner`; missing action/owner is explicitly listed under `missingFollowUpMetadata`, never guessed or marked complete. Source/disposition supplies the reason when no separate reason exists. Unresolved research remains deliverable; this summary does not grant READY_FOR_SELLER_REVIEW. Review critical facts and existing completeness gates separately.

`--summary-output` writes a separate JSON with artifact role, product/configuration/stage, input hashes and coverage. It must end with `.research-summary.json` and cannot overwrite a file of another role or product. Supply it for Research Review delivery and refresh it after ledger/workbook changes. Core `run()`/CI remain read-only and do not rewrite product summaries automatically. Public summaries follow the same serial/source sanitization policy as public ledgers. Legacy array ledgers still need scope reconciliation before this scoped summary/export path.

Current workbook CI checks every delivered top-level `.research-summary.json`: product/directory/configuration, declared stage, referenced workbook and current ledger/template/product-facts hashes, plus recomputed coverage counts/follow-ups. A stale or edited summary fails with an explicit regeneration message; CI never refreshes the old conclusions. New summaries record `workbookFile` as a local filename. Earlier summaries without it remain readable only when their workbook hash identifies exactly one current workbook. Summary output itself must also belong to the correct product directory when written under the canonical tree. Existing products without a summary are not silently backfilled or newly certified; the standalone file is required by the new Research Review delivery procedure above.

## Storage field relationships

`Hard Disk Size` remains the installed drive capacity checked against `selectedBaseConfiguration.ssdGB`. By default, a populated `Memory Storage Capacity` must agree after GB/TB conversion. A different total is not an optional upgrade tier and cannot be justified by an external disk, cloud space or factory alternative. `Flash Memory Installed Size` is not automatically treated as an SSD alias: its precise medium/Definition needs field-specific review.

For a genuinely different total internal capacity, put `storage_scope: "INTERNAL_TOTAL"` and `storage_component_fact_ids: [...]` inside the selected Memory Storage Capacity fact's `evidence`. Include the selected Hard Disk Size fact ID exactly once, plus distinct additional physical-drive fact IDs in the same ledger. Each additional drive must be a VERIFIED SOLD_BASE Product Details fact for this configuration with applicability, transfer basis and source; its evidence records `capacity_unit` (GB/TB) and `storage_medium` (INTERNAL_SSD/INTERNAL_HDD). Its numeric final_value is its installed capacity. Each physical drive appears once; IDs represent components, not duplicate descriptions or selectable alternatives. The base drive uses its selected unit fact. Export sums the components and checks the total. Evidence still requires actual source/physical-drive review; IDs alone do not prove installation.

Additional drives use dedicated, unmapped ledger attributes named `Secondary internal drive capacity` or `Additional internal drive capacity`, optionally followed by an identifying suffix (for example `Additional internal drive capacity 2`). These supporting facts add no workbook columns. Existing template fields, including RAM, VRAM, cache and aggregate capacity fields, cannot be referenced as additional physical drives even if someone adds an SSD/HDD medium tag to them.

Copy validation uses that same verified per-drive configuration. Explicit SSD/NVMe and HDD claims must match a recorded drive of that medium; generic storage claims must match a recorded drive or the internal total. Explicit `total storage`, `total internal storage` and `combined storage` claims must match the total. For example, a verified 256GB base SSD plus 1TB internal HDD permits `256GB SSD + 1TB HDD` and `1.25TB total internal storage`; it cannot authorize `1TB SSD`, `2TB HDD` or `1.25TB SSD`. Multiple drives of the same medium are accepted individually, while combined capacity must be clearly identified as total storage. Free-form claims, physical-drive count and unrecognized wording still require factual review; the parser does not authenticate installation evidence.

This permits, for example, a verified 256GB base drive plus a verified second 256GB internal drive with a 512GB internal total. It does not change the established base-drive fields or allow the total to be mislabeled as one SSD in copy. Do not guess a component list to pass validation. Drafts retain the disagreement with an honest unresolved status until evidence is reconciled.
