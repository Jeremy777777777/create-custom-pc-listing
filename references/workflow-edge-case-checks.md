# Follow-up workflow checks — 2026-10-14

These implementation refinements preserve the three sheets, five rows, existing fields and eleven image slots. They supplement [workflow validation boundaries](workflow-validation-boundaries.md) without changing the product appearance or seller policy. They do not refresh product approvals or manufacture human review.

## Export semantics

Type checks use explicit current-template fields, not phrases inside Definition. `Resolution` accepts positive width × height text; fractional display refresh rates are permitted. Government contract names/numbers remain text. Declared count fields require nonnegative integers. Applicable capacities and speeds still need positive numeric values and paired units.

Unit rules belong to each field: installed RAM uses GB/MB, disk size GB/TB, Memory Speed MHz, and CPU/memory clock frequencies MHz/GHz. MT/s is a transfer rate and cannot fill a frequency field by relabeling its unit. Research the actual requested quantity; never assume a conversion to pass export.

Both existing maximum RAM fields refer to the same supported maximum. `RAM Memory Maximum Size` remains numeric with its existing unit field. `Ram Memory Maximum Size` may use the same verified unit or explicit capacity text such as `64GB`. They must agree after normalization and cover installed RAM. No field is renamed or added.

CPU Model, CPU Model Number and CPU Model Manufacturer must agree with verified `product-facts.identity.cpu`. Normalization handles spaces, punctuation and trademark symbols; it does not equate different CPU families. A genuine OEM/channel naming alias may be recorded under `identity.cpuFieldAliases` as field-name → list of verified equivalent names, with supporting research evidence. Never create an alias to excuse a contradiction.

Use `listing_content.base_spec_fragments(product)` to obtain base RAM/SSD fragments when composing new copy. Formal export checks common forward/reversed RAM, Memory, DDR/LPDDR, SSD and NVMe/PCIe/M.2 capacity wording against that base. Cache/graphics memory must not be treated as system RAM. Free-form claims still require human factual review; matching a pattern cannot prove that every sentence is accurate.

## Gallery change routing

Revision checks use `git diff --no-renames` and reject deleted/renamed canonical slots, including when the entire old product directory disappears. Existing quarantined/current/import galleries cannot become research-only simply by removing all images. Genuine new research folders remain permitted.

A scoped product's bound partial receipt is checked even when only facts, style, recipe or review metadata change. A commerce-only change excluded by the existing review-input contract may pass without image regeneration. Changes that affect depicted facts/style require renewed actual review. Historical partial records without input bindings remain preserved and are explicitly counted as `historicalPartialReviewsNotCurrent`; they never count as current partial or full PASS. Changes to their product inputs/review records require current evidence before delivery. Shared code checks may report untouched historical records without rewriting them.

Recording remote delivery status alone does not refresh or require a new visual approval. Untouched historical reviews remain explicitly historical in the CI summary.

## Finalization writes

Finalization prepares all selected images, clean masters, logo QA and contact sheet before writing. It then creates same-directory replacement files and original-byte backups for every destination. A write/replace failure rolls back already committed destinations and removes newly created outputs. Unselected files remain unchanged.

If the operating system also prevents rollback, the command fails with the retained recovery-backup locations; preserve those files and restore the affected destinations after resolving the lock/permissions. Never claim success after partial recovery. This handles ordinary write errors; process termination/power loss still requires checking current bytes and retained backups before retrying. It is not a simultaneous multi-file filesystem transaction.

Tests use synthetic fixtures, real Git deletion/rename scenarios and injected write/rollback failures. They do not assess actual product appearance, asset rights or Amazon publication eligibility.
