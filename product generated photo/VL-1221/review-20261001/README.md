# VL-1221 requested rework — review delivery

Status: `REVIEW_READY`, not canonical replacement or a full-gallery QA pass.

This review contains the two latest requested assets: the front enhanced MAIN and PT08. The eleven existing canonical image files in the parent directory are unchanged.

## Front enhanced MAIN

- Preserves the approved front composition, product scale and whitespace; the robot's head alone crosses the LCD top edge.
- Display, RAM and SSD use graphical cards with short specifications; CPU, GPU and Windows use deterministic composition of original assets after removing their generated approximations.
- AMD and NVIDIA source padding is trimmed without removing visible artwork; the resulting complete visible asset is uniformly scaled. The Windows package is used whole and uniformly scaled.
- AMD source: https://www.amd.com/content/dam/amd/en/images/logos/products/2462924-amd-ryzen-7-badge.png
- NVIDIA source: https://iprsoftwaremedia.com/219/files/202512/202512022046/geforcertx-logo-wht.png?download=true
- Windows source: repository `assets/branding/windows-11-pro-package.png`.
- Remaining limitation: product/scenery/card master is an edited generated composition, not a newly obtained OEM product photograph. This file does not assert that Amazon has approved an enhanced MAIN.

## PT08

- Preserves the user-approved white-background, two-side chassis composition with independent blue/orange icon callouts and a wireless footer.
- The HP mark is the original repository `assets/branding/hp-logo-blue.png`, deterministically placed at x38/y1090 with a 128px square bound on a 1254px canvas. The adjacent divider is shortened for clearance.
- Physical depiction source: the user's supplied approved reference `codex-clipboard-73486348-16c6-48e9-9e18-30e99ebd1802.png`, subsequently edited by ImageGen. It is **not represented as verified OEM photography**. User confirmation of asset authorization is retained separately from factual/photo provenance.
- Interface labels are checked against the previously retrieved HP 15-fb3xxx maintenance guide and the 15-fb3093dx product information. The reference image is not itself a specification source.
- HP guide: https://kaas.hpcloud.hp.com/pdf-public/pdf_11551834_en-US-1.pdf

## Scope and remaining canonical issues

The parent gallery's legacy PT06 still depicts an adapter and the parent directory lacks the current full-gallery logo QA record. These issues are not silently marked PASS by this two-image review. Canonical replacement requires the full applicable delivery checks and resolution of product-photo provenance. This review directory does not add extra top-level canonical images.

## Prompt set and production method

Built-in ImageGen edit mode: preserve approved composition and head-only breakout; replace text-dominated card interiors with graphical assets; clear CPU/GPU/Windows generated marks for original-asset composition; remove the leftover white inner Windows outline. PT08: preserve the supplied dual-side layout, chassis appearance, short labels and independent physical-port callouts; remove the generated HP mark and shorten the adjacent footer divider. Original AMD/NVIDIA/Windows/HP assets are then placed using `finalize-requested.ps1` in the local production folder.

Visual review: the requested two files have readable specifications, screen-contained cards, no shoulder/hand breakout, matching dark PT08 appearance, separate interface leaders and an original HP overlay. SHA-256 and dimensions are recorded in `review-assets.json`; this scoped review must not be called `FINAL_ASSET_QA_PASS` for the complete gallery.
