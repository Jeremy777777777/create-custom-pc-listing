# MegaPC own-brand Mini PC listings — user decision 2026-10-28

This route supersedes catalog-wide customized/OEM wording for the user's own manufactured MegaPC products only. Existing customized third-party OEM products retain their current route. Do not classify a product as own-brand from its chassis resemblance or from a MegaPC seller name alone.

## Authority and identity

The user confirmed manufacturer, seller and intended chassis branding are MegaPC, then clarified: the supplied assets are original material, appearance/interfaces are shared, exact details follow ERP, missing details come from those supplied materials, Excel uses the ERP VD identifier, and these are not customized listings.

For these products, exact matching ERP detail/Specification and linked sellable configuration are the primary configuration record. Use the original supplied material to fill absent physical/interface/structural fields. Record both sources and the user's shared-appearance confirmation. Do not transplant a source asset's older CPU, graphics, RAM/SSD, wireless or OS claim over ERP. Component-manufacturer research cross-checks technical identities and terminology; a processor capability does not establish a fitted port, radio, memory speed or whole-system capability. Retain real conflicts for reconciliation, never quietly relabel numbers or units.

Different original source variants may conflict with one another. Keep their identity and scope: for example AMR5's illustrated HDMI/DisplayPort arrangement differs from AM08's dual-HDMI layout, and AM08 Pro's marketing HDMI version conflicts with its spreadsheets. Shared appearance authority enables reuse of matching physical features, not choosing an arbitrary disputed protocol. When ERP is silent and supplied records conflict, keep that detail unresolved/candidate and use only their supported common wording, such as connector count without an unverified version.

Bind each requested VD product separately to its observed ERP detail, actual linked sellable configuration and source date. A shared model name or appearance does not merge processor variants. Do not infer inventory meaning, raw serial delivery, extra variants or installed module identities from those observations. Product-specific facts remain in the authorized Drive product records, not this reusable workflow reference.

Use the exact ERP identifier for filenames and canonical product directories, e.g. `VD-740_LISTING_DRAFT.xlsx` and `VD-740_RESEARCH_REVIEW.xlsx`. AM08/AM08 Pro/AMR5 are source labels, not substitute output IDs. Reuse/verify the matching existing Drive product folder; permitted missing internal-ID folder creation follows the existing bounded authorization.

## Explicit execution route

Set `product-facts.json` root `listingMode` to `MEGAPC_OWN_BRAND` and `ownBrandAuthority` to the actual user decision/date. `identity.oemBrand` remains the existing schema's manufacturer key and must be `MegaPC`; it does not imply a separate third-party OEM. `identity.oemModel` holds the ERP model. Missing mode retains `CUSTOMIZED_OEM` for compatibility. Unknown modes or own-brand mode with a different manufacturer/missing authority fail validation.

Use original English product copy, for example `MegaPC AR9-69 Mini PC, AMD Ryzen 7 7840HS, 32GB DDR5 RAM, 1TB SSD, Win 11 Pro`. Keep the existing 200-character limit, five complete bullet paragraphs, literal Description HTML, verified base-configuration consistency and field-by-field evidence/candidate rows. Do not use Custom, Customized, Created Using, upgrade stories or seal-opening claims. Manufacturer/brand/seller are MegaPC. Store factual assembly information in research only where applicable, without inventing alterations.

## Retained warranty scope

The user replied “沿用” to retaining existing warranty, then expressly ruled out customized listings. The own-brand wording in [own-brand-listing-policy.json](../assets/own-brand-listing-policy.json) therefore retains the existing one-year RAM/SSD limited coverage and MegaPC manufacturer's remaining-component coverage, while removing inapplicable upgraded/third-party/seal assertions. It does not invent a one-year whole-system term. Remaining-component coverage terms stay a manual publication check. Use that same paragraph in bullet 1, the final `Warranty and Disclosure` HTML section and Warranty Description. The existing third-party customized paragraph remains unchanged for its route.

## Images and release

Use the independent M/MG Mini PC design series and product-specific previews. The user confirmed actual MegaPC branding; preserve geometry, materials and connectors when adapting authorized supplied assets. Other brand marks in source references are provenance, not the intended final sales branding. Brand treatments require the actual approved MegaPC artwork and fidelity review, not an invented logo. Existing accessory treatment, inches, safe zones, style approval, image QA, privacy, original-XLSX Drive delivery and GitHub workflow backup rules remain applicable. Do not publish to Seller Central automatically or call a partial draft complete.
