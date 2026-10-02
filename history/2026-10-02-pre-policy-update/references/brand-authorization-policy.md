# Catalog Brand Authorization Policy

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
- Use only the correct OEM's official, partner-supplied, seller-owned, or otherwise approved original asset. Never redraw, approximate, recolor, stretch, or substitute an OEM Logo.
- Product imagery must still match the exact model, chassis, color, port layout, keyboard layout, and sold configuration. Authorization never permits inventing hardware geometry.
- Record the OEM, asset source URL or seller source, local asset path, and `USER_CONFIRMED_CATALOG_WIDE` status in `image-manifest.md`.
- A workflow may still block when the brand cannot be identified, an asset belongs to a different model/brand, the supplied asset is corrupted or unusable, a specific campaign license is expired or scope-limited, or another third-party right is unresolved.

## Rights that remain separate

This catalog-wide OEM authorization does not automatically cover game IP, entertainment characters, stock-photo people, competitor assets, Office/Copilot entitlements, processor/GPU campaign marks, or other third-party software and media. Those items retain their own evidence and authorization gates.
