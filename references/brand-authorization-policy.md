# Catalog Brand Authorization Policy

User amendment 2026-10-29: the user explicitly confirmed authorization for familiar hardware/software marks (including AMD, Intel, Windows and Office) and requested their downloaded original files be stored and reused. Apply [reusable-brand-assets.md](reusable-brand-assets.md); record `USER_CONFIRMED_BRAND_ASSETS_2026_10_29`. This supersedes the older separate-authorization gate below for these catalog hardware/software identities only. Correct component/tier/edition selection and any software inclusion/paid entitlement remain separate factual requirements; do not manufacture them from brand permission. Game/character/stock-media rights remain outside this amendment.

## Seller authorization assertion

MegaPC / J-Tech Digital has explicitly confirmed that it holds the applicable reseller, partner, or written brand-asset permissions for every OEM brand sold in its catalog. For this workflow, record this seller-provided assertion as:

```yaml
oem_brand_authorization_status: USER_CONFIRMED_CATALOG_WIDE
authorization_holder: MegaPC / J-Tech Digital
allowed_context: accurate product merchandising and listing-image production for catalog products sold by the authorization holder
confirmation_source: direct user confirmation in the project workflow
```

## Execution rule

- Do not set `BLOCKED_BEFORE_PRODUCTION` merely because an OEM's public website does not publish the seller's private authorization record.
- Public official OEM product pages, manuals, media galleries, and trademark pages may be researched to obtain accurate model facts and identify official product and Logo assets.
- Use the correct OEM's official, partner-supplied, seller-owned, or otherwise approved original sources. The user confirmed commercial authorization and approved faithful AI reproduction of the official original machine on 2026-10-06; apply [faithful-product-reproduction.md](faithful-product-reproduction.md). Final OEM Logo assets remain approved originals: never redraw, approximate, recolor, stretch, or substitute them.
- Product imagery must still match the exact model, chassis, color, port layout, keyboard layout, and sold configuration. Authorization never permits inventing hardware geometry.
- Record the OEM, asset source URL or seller source, local asset path, and `USER_CONFIRMED_CATALOG_WIDE` status in `image-manifest.md`.
- A workflow may still block when the brand cannot be identified, an asset belongs to a different model/brand, the supplied asset is corrupted or unusable, a specific campaign license is expired or scope-limited, or another third-party right is unresolved.

## Rights that remain separate

This catalog-wide OEM authorization does not automatically cover game IP, entertainment characters, stock-photo people, competitor assets, Office/Copilot entitlements, processor/GPU campaign marks, or other third-party software and media. Those items retain their own evidence and authorization gates.
