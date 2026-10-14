# Workflow validation boundaries — 2026-10-14

This reference refines existing stages; it does not change worksheet names, five-row layout, field definitions, product directories or eleven image slots. Research drafts still permit unresolved facts. Formal export requires complete applicable evidence and content. No tool automatically publishes to Seller Central.

## Export

`research_export.py --mode export --stage LISTING_DRAFT` requires the independently selected product/configuration IDs to match both the scoped ledger and `product-facts.json` (`identity.internalId`, `selectedBaseConfiguration.id`). Its receipt includes `productFactsSha256`, workbook, ledger and current template hashes. Adapters must compare all four current inputs and target IDs immediately before export. A changed input requires a fresh check.

The export content gate requires verified OEM identity, CPU model, installed RAM/storage with units and sold OS. It checks title policy/length, five bullet paragraphs, the existing exact warranty/HTML checks, positive numeric capacity/speed fields and units, integer counts, RAM aliases, installed RAM versus verified maximum and sold capacities versus selected base. Manufacturer/model and CPU model number must agree with product identity. The maximum is a capability, not the installed capacity. Display-specific fields may remain evidenced NOT_APPLICABLE for standalone desktops. Ambiguous grouping fields require Definition/source review rather than invented equivalence. These checks cannot prove source authenticity or detect every misleading claim in prose.

Value, Status and Source cells must be literal values, never Excel formulas. Draft checking still verifies exact ledger projection without imposing export completeness. Do not fill unknown specifications or rewrite a real product to satisfy a test.

## Images and supplied review

Composition, full validation and partial validation share `logo_geometry`: alpha-visible aspect ratio, transparent asset, product-silhouette protected zones, clearance, official wordmark requirements and the same canvas-long-edge visibility limit.

Every new visual/semantic review must include `reviewInputsSha256`, obtained with `gallery_engine.review_inputs(product_directory)` when reviewing the actual current images. Record that value in the review **at review time**, not by automatically refreshing an old PASS. It binds product hardware facts, approved style lock, referenced recipe and the active catalog/image/fidelity/delivery policy text. The top-level offer/inventory/researchLog/updatedAtUtc/delivery keys are excluded because they do not change depicted hardware. Hardware changes conservatively invalidate supplied reviews; rerun only the requested affected image scope and review it with the current inputs. The helper returns a binding, never a visual or semantic decision.

Reviewer and per-image notes must contain non-whitespace text; reviewedAtUtc must be an ISO timestamp with UTC offset, for example `2026-10-14T12:00:00Z`. Hashes do not replace actual inspection. Existing historical reviews without input bindings remain preserved as historical evidence. They cannot authorize a new changed-slot delivery until reviewed against current facts/style/policy. No migration automatically manufactures a review or rewrites old product records.

Gallery JSON hash bindings use UTF-8 LF-normalized content, so Git's Windows/Linux newline conversion cannot invalidate an otherwise identical review or plan. New JSON writes and normal JSON checkouts use LF. Image hashes always cover raw bytes. Workbook snapshots deliberately override JSON text conversion and bind their original raw bytes. This normalization never permits a changed JSON value to reuse a review.

An approved import authorizes frozen bytes only. The VL-1221 archived exact-asset receipt and VL-1326 import receipt are pinned in `assets/frozen-import-records.json`; changing both image hashes and receipt does not create new authorization. This registry is maintained workflow authority, not an output file to regenerate when an import fails. VD-744 and VL-1276 retain their existing fixed authorization checks. Updating an approval requires new direct user evidence and an explicit reviewed workflow change.

For VD-744's next ordinary update, preserve `approved-angle-import.json` unchanged as historical authorization. Move the current delivery state to LEGACY_QUARANTINED, currentQaPass:false, deliveryScope:PARTIAL_UPDATE and provide current selected-slot review/partial receipt; retained slots remain quarantined. Alternatively, review the complete gallery and use normal full acceptance, which sets CURRENT_REVIEWED. The frozen import branch applies only while its specific import state is active. Prior authorization does not supply QA for new bytes. A declared completed/current gallery with zero images is an error, not a research-only folder.

Finalization stages normalization, compositing and the complete contact sheet before replacing selected outputs. The contact output is mandatory and must be outside the canonical product directory. It preserves unselected slots and rejects invalid plans/assets before delivering changes. Disk/OS failures still require verifying hashes and rerunning from clean masters.

## Historical workbook storage

Snapshot bundles are append-only. `.gitattributes` disables text conversion for their entire path, preserving original ledger/template/workbook bytes across Windows/GitHub checkouts. CI and the revision-scoped local runner compare all existing snapshot Git blobs against the trusted base revision. Modifications, deletions, renames and added files inside an old bundle fail even if its receipt is rehashed. Add a new revision directory instead. Current bundle schema/hash checks remain mandatory. A run without base/head checks present bundle integrity only; it cannot prove historical immutability. Git history here supplies preservation evidence, never product facts or operative policy.

## Local tools

All image PowerShell wrappers use `scripts/listing-python.ps1`: LISTING_PYTHON, an active listing-testing environment, or the user's Anaconda listing-testing interpreter. It verifies Python 3.12 and the environment identity and never falls back to WindowsApps/PATH. The test runner also supports explicit -PythonPath. Isolated GitHub CI uses its configured Python 3.12 runtime.

The old HEAD_ONLY reference checker requires explicit -HistoricalOnly and cannot establish current production approval. Current production follows the active SCREEN_ONLY/default and explicitly approved variation rules.
