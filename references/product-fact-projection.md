# Research facts, metadata views and image review — 2026-10-14

This refines [scoped research projection](research-ledger-projection.md) and [workflow checks](workflow-edge-case-checks.md). It preserves the template, field names, product directories and eleven image slots. No research value or existing review is silently promoted to VERIFIED/PASS.

## Research → Listing

`product_metadata.listing_view` supplies a read-only structured view. A legacy `identity` display string is never parsed to guess manufacturer/model. The adapter takes only VERIFIED selected ledger fields for the missing OEM brand/model, CPU and installed capacity/unit values. Existing explicit values must agree. The product's independent internalId/productId must match the ledger; a missing configuration ID may be associated with that matched product's selected ledger configuration. Record the source fact IDs and adapter format in the evidence-check receipt.

`research_export.py` and `check-workbooks.py` use this view for Listing checks. Original product-facts bytes stay unchanged and their raw hash remains in the receipt, alongside the ledger/workbook/template hashes. Metadata deficiencies return `PRODUCT_METADATA_REQUIRED` with the missing fields, rather than an AttributeError. A successfully adapted research workbook still needs actual listing copy and all existing export gates; adaptation cannot create customer copy or verify unresolved specifications.

For new full research, prefer the structured identity and selectedBaseConfiguration form. Legacy image-only records may remain as preserved caches; new Listing work uses the verified selected ledger view. Do not maintain a second independently edited set of current specifications.

## Research → images

New `gallery_engine.review_inputs` bindings include a deterministic scoped-ledger hardware projection when one exists. It binds the target product/configuration, selected fact IDs, scopes, states, final values, source and sold-applicability basis. Offer and Safety&Compliance fields, customer copy/keywords, unselected factory alternatives and research notes are excluded from this hardware projection. Hardware changes conservatively invalidate the supplied review; no new style proposal is implied.

Known cache fields (identity, CPU, installed RAM/storage/VRAM, OS, display and wireless) are checked against their corresponding selected verified facts before a new binding is produced. Contradictions and unresolved corresponding facts require reconciliation. Not every free-form cache phrase can be interpreted automatically: the actual image's claims and authoritative selected facts still need factual review. Unknown/missing cache fields are not fabricated. Legacy array ledgers remain draft evidence, not a new scoped source.

The model-number check distinguishes the exact CPU anchor from manufacturer/family. Generic `Intel` or `Core Ultra 7` cannot fill `CPU Model Number` for a 265T. Formatting/trademark normalization and specifically evidenced aliases remain supported; unsupported model naming needs explicit metadata/evidence rather than a guessed SKU.

Capacity text is associated once, within a clause and adjacent label group. RAM/DDR, GDDR/VRAM, cache and SSD/NVMe have distinct roles; a graphics-memory label cannot capture the next SSD capacity. Verified numeric VRAM, when present, is checked separately. Cache levels and unparsed free-form claims still require field-specific review.

Reverse capacity wording consumes same-role suffix labels too: `RAM: 16GB DDR5 256GB SSD` must retain 256GB as storage. CPU extraction excludes appended wattage, frequency, cache capacity and core/thread counts; multiple remaining model candidates require explicit reconciliation rather than selecting the last token. Recognized CPU identities in title, bullets and HTML description must agree with the supplied canonical identity or its explicit model-number aliases. Recognition covers common Intel Core/Ultra, Ryzen, Apple and exact Snapdragon model forms; unrecognized/free-form claims still need factual review, and a passing copy check does not authenticate the CPU. Resolution cache comparisons normalize supported width-by-height spellings (`x`, `×`, optional px/pixels) while rejecting actual dimension changes and unsupported labels such as `FHD`.

## Preserve old reviews honestly

Existing image reviews may predate their scoped ledger. Preserve their original bytes and approval, but do not claim they reviewed that later ledger. During CI, unchanged canonical images may receive cached-fact/image-integrity preservation checks using the exact original binding. Such full/partial records are counted separately as `historicalResearchUnboundGalleries` / `historicalResearchUnboundPartialReviews`, never as current source-bound full/partial PASS.

Strict validation and acceptance for new work require the new binding and actual review. Changed canonical image slots cannot take the historical-preservation route. New ledger-bound records become stale when their selected hardware changes; changing both cache and ledger still requires a new actual review. The workflow update itself does not refresh old PASS records or rewrite real product files.

This permits immediate research-draft delivery while clearly identifying older image evidence that needs reconciliation for the next image update. CI success, historical preservation, current scoped image QA, remote delivery and Amazon publication remain separate results.
