# Product Image Spec

This reference governs the Amazon product-image gallery for customized PCs.
Use it through the [dedicated image workflow](amazon-product-image-workflow.md),
after the relevant listing facts have been verified in the main workflow.
It covers only the nine-image product gallery. Image production is a separate
task from the listing workbook and must not add,
remove, rename, or populate workbook sheets unless the user explicitly asks.

Amazon's current requirements override this internal production standard:

- Product image guide: https://sellercentral.amazon.com/help/hub/reference/G1881
- Technical image file requirements:
  https://sellercentral.amazon.com/help/hub/reference/G9FUUH87RBNXGKB7
- Reviewed against the US Seller Central guide on 2026-09-20.

## Scope and internal gallery standard

The standard gallery contains `MAIN` plus `PT01` through `PT08`. Amazon supports
more PT variants, but these nine slots are the current MegaPC production
standard. Their order is an internal workflow convention, not a promise that
Amazon will display images in that order.

Amazon may select, arrange, or modify submitted images, including images
contributed by multiple selling partners. Uploading an image does not guarantee
that it will appear. A selected image can take up to 24 hours to display.

Amazon requires at least one compliant main image and recommends at least six
additional images plus one product video. The nine-slot gallery satisfies the
image-count recommendation. A video is recommended but is not a required
workbook output.

## Technical file requirements

Apply these checks before marking an image `VERIFIED`:

- Supported formats: JPEG, TIFF, PNG, or non-animated GIF. Prefer JPEG for final
  Amazon uploads; PNG remains appropriate for production masters when needed.
- Longest side: minimum 500 pixels and maximum 10,000 pixels.
- Use at least 1,000 pixels on the longest side to enable zoom. Internal targets
  are 2,000 × 2,000 pixels for `MAIN` and 1,500–2,000 pixels square for PT images.
- Do not artificially enlarge a small source image to meet the minimum.
- Resolution: at least 72 dpi.
- Prefer RGB color mode.
- Images must be clear, professionally finished, non-pixelated, and free of
  jagged edges.

### File naming and variant codes

For bulk upload, name files with exactly three components separated by periods:

`ProductIdentifier.VARIANT.extension`

Examples:

- `B0XXXXXXXX.MAIN.jpg`
- `B0XXXXXXXX.PT01.jpg`
- `012345678905.PT08.jpg`

Do not insert spaces, dashes, or extra filename components. The product
identifier may be an ASIN, UPC, EAN, GTIN, ISBN, or JAN. Use:

- `MAIN` for the primary image
- `PT01`–`PT08` for this workflow's supporting gallery images
- `PS01`–`PS06` only for warning or safety images intended for Amazon's Safety
  and Product Resources section, not as ordinary gallery slots

## Use and record real image files lawfully

Final delivery must point to actual image files, not only describe them. Record
each file path, readiness, and provenance in the product folder's
`image-manifest.md`. Use only assets that the seller has the right to use
commercially:

1. Official OEM images obtained through an authorized reseller media library
2. Seller-owned photography of the stocked unit
3. Original infographics composed from verified product facts and licensed
   assets

Do not download, crop, recolor, trace, composite, or lightly edit third-party
editorial, review, retailer, or competitor images for a commercial listing.
Online reference images may help identify a needed angle, but they are not
licensed production assets.

If no licensed source or image-production capability is available, do not
fabricate a file or a final path. Keep the slot in `image-manifest.md`, record
the expected licensed source, and set its status to `TO SOURCE` or `TO PRODUCE`.

## Amazon competitor research boundary

Relevant Amazon listings may be reviewed to understand expected image coverage,
benefit order, common infographic topics, and overall visual quality. A target
listing is a benchmark for completeness, not a production template.

- Record competitor and OEM Amazon URLs only as research references. They are
  not asset provenance.
- Do not reproduce another seller's wording, composition, distinctive layout,
  screenshots, ratings, review excerpts, badges, or comparison graphics.
- Use original composition and copy within the fixed internal slot roles below.
- Final product photography still requires an authorized OEM source or
  seller-owned photography. Infographics must use verified facts.

## AI-generated people disclosure

If an image contains a photorealistic person who was generated entirely by AI,
add the keyword `contains-synthetic-performer` to the image file's `dc:subject`
XMP field with an IPTC-compatible metadata editor before uploading it to Amazon.
Record that metadata check in the image's Source or production note.

Do not add this tag when the image:

- contains only real people, even if AI tools altered the image
- contains no people
- contains only non-photorealistic people
- contains characters from movies, video games, or other expressive works

This rule is especially relevant when producing the use-case scenes in `PT02`.

## MAIN image requirements

`MAIN` appears first on the detail page and in search results. It must:

- accurately represent the real product's scale, quantity, color, and included
  components in a realistic, professional-quality image
- show the complete product within the frame without cropping any part
- show the product only once; do not combine front and back views
- show one selling unit and only accessories actually included with it
- fill approximately 85% of the image area
- use a pure white background with RGB values `255, 255, 255`
- contain no added text, graphics, borders, badges, watermarks, or logo overlays
- exclude props and accessories that are not included
- exclude packaging unless the packaging is an important product feature
- never be a placeholder or temporary image

The internal `MAIN` composition is a centered, straight-on 0° view with no
rotation, tilt, yaw, or three-quarter angle. Use a neutral, non-promotional
screen image and keep the chassis square to the camera. Show the included
keyboard and mouse for a desktop or all-in-one only when the exact SKU includes
them. Show a laptop alone unless external accessories are included.

A trademark physically present on the genuine product may remain visible as
part of an accurate photograph. Do not add or enlarge an OEM, seller, or other
logo as a separate graphic.

## Supporting gallery — fixed internal order

| Slot | Variant | Role | Background | Required content |
|---|---|---|---|---|
| **1** | `MAIN` | Hero | Pure white | Centered straight-on complete product; included accessories only; no overlay |
| **2** | `PT01` | Display | Dark navy, orange accents | Product three-quarter view plus verified display, webcam, and audio facts |
| **3** | `PT02` | Use cases | Dark navy | Product plus business, remote work, reception, or study scenes; apply the AI-person metadata rule when required |
| **4** | `PT03` | Full specifications | Dark navy, orange accents | CPU, display, offered RAM tiers, offered SSD tiers, OS, connectivity, and collaboration facts |
| **5** | `PT04` | Design and form factor | Dark navy, blue accents | Side/profile views and verified chassis, footprint, stand, and included-accessory facts |
| **6** | `PT05` | Performance | Dark navy, blue accents | CPU, offered RAM tiers, offered SSD tiers, and preinstalled OS; do not present software as a customization |
| **7** | `PT06` | What's included | White | Show only the exact unit, power equipment, and accessories included with the SKU |
| **8** | `PT07` | Specification recap | White or light | CPU, offered RAM tiers, offered SSD tiers, and preinstalled OS |
| **9** | `PT08` | Connectivity | White | Verified rear/side ports and connectivity; do not show unavailable ports |

Reserve three-quarter views and multiple angles for PT images. Every displayed
RAM or SSD option must be genuinely offered for the listing. Use a brief factual
footer such as `Configuration varies by selected option` when several selectable
configurations exist.

## Requirements for every gallery image

Every image must:

- accurately represent the product being sold and match the listing title,
  selected configuration, quantity, color, and included accessories
- use only verified technical claims and correctly licensed assets
- remain readable, unclipped, and free of pixelation or jagged edges
- avoid customer reviews, star ratings, testimonials, and review excerpts
- avoid prices, coupons, free-shipping claims, time-limited promotions, and
  seller- or store-specific information
- avoid Amazon names, logos, trademarks, and confusingly similar designs,
  including Amazon, Prime, Alexa, and the Amazon Smile
- avoid Amazon badges and similar graphics, including Amazon's Choice,
  Premium Choice, Best Seller, Top Seller, and Works with Alexa
- avoid nudity or sexually suggestive photographs, illustrations, and scenes

Supporting PT images may contain concise factual specification text. Do not add
seller logos, OEM logo overlays, watermarks, merchant names, store contact
information, warranty advertisements, or sales claims. A genuine trademark
already printed on the photographed chassis does not need to be removed.

## Internal visual style

- Use dark navy (`#0A1A3A`) and white/light themes with restrained orange
  (`#F1511B`) and blue (`#1F8FFF`) accents.
- Use bold, legible sans-serif headings and short factual feature cards.
- Keep one consistent, non-promotional on-screen wallpaper across product views.
- Do not let internal styling override Amazon requirements or accurate product
  representation.
- Do not use logos as decorative elements. The visual system comes from color,
  typography, layout, and the genuine product photography.

## Brand and configuration safeguards

- Do not visually present the OEM as the listing seller or imply OEM approval of
  the customization.
- Do not place `Customized by MegaPC`, seller warranty claims, merchant contact
  information, or other seller-specific copy on gallery images.
- Document customization and warranty in the listing title, bullet points, and
  product description rather than as gallery advertising.
- Display RAM and SSD tiers only when physically supported and actually offered.
- Windows or other software may be shown only as a preinstalled specification,
  never as a hardware customization.
- Show Touch, AI-ready, webcam, cellular, or other features only when verified
  for the exact SKU.
- Show a port or accessory only when it is present or included with the exact
  shipped configuration.

## Separate image-task output format

Deliver each product under `product generated photo/VL-<internal-model>/` with
`MAIN` and `PT01`–`PT08` image files plus one `image-manifest.md`. The manifest
is the production record and must include, for every slot:

- final repository-relative file path, or a production brief when not ready
- status: `VERIFIED`, `TO SOURCE`, `TO PRODUCE`, or `BLOCKED`
- licensed asset provenance and the verified product facts used in the image
- any required AI-person metadata note

Use the internal filenames `MAIN.jpg` and `PT01.jpg`–`PT08.jpg` in the GitHub
product folder (or the matching real extension). Before Amazon bulk upload,
export or rename copies to `ProductIdentifier.VARIANT.extension` as described
above. Do not put production records in the listing workbook, and do not claim
an Amazon-ready file path for an image that does not exist.
