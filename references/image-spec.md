# Product Image Spec

This reference governs the Amazon product-image gallery for customized PCs.
Use it through the [dedicated image workflow](amazon-product-image-workflow.md),
after the relevant listing facts have been verified in the main workflow.
It covers only the nine-image product gallery. Image production is a separate
task from the listing workbook and must not add,
remove, rename, or populate workbook sheets unless the user explicitly asks.
The selectable visual systems are defined in
[image-style-profiles.md](image-style-profiles.md). A profile changes PT-image
styling and information hierarchy; it never changes the requirements below.
For centered screen features and Windows 11 Pro package-style treatments, also
read [conversion-hero-styles.md](conversion-hero-styles.md) and
[hero-composition-variants.md](hero-composition-variants.md). The latter is an
independent PT01 composition layer: every Gaming G/C and Business B family may
use either the approved front-facing or three-quarter variant when the exact
product-view evidence supports it.
For a product verified as Gaming, additionally read
[gaming-hero-styles.md](gaming-hero-styles.md). Its 3D characters, vehicles,
environments, and effects are PT01 add-ons or separately gated enhanced-main
candidates; they are never permitted on the default strict `MAIN`. Also read
[gaming-core-badge-styles.md](gaming-core-badge-styles.md) for the six approved
Windows 11 Pro and core-configuration compositions. One four-cell
`CORE_SPEC_CLUSTER` counts as one feature card; all values must match the
selected verified SKU.
For a product verified as Business/Work, also read
[business-work-hero-styles.md](business-work-hero-styles.md). Its B01–B06
layouts may display Office or Copilot only after the exact SKU entitlement and
approved brand assets pass the documented gates.
For PT02–PT08 audience-specific scenes and narrative continuity, also read
[supporting-gallery-styles.md](supporting-gallery-styles.md). The selected
Gaming or Business continuation pack must match the PT01 hero family.

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

A Windows 11 Pro package, card, badge, feature label, or screen callout is not
permitted in the default strict `MAIN`. An enhanced-main concept may be kept as
an internal candidate. When the seller confirms that its current account or
category permits this treatment, record that confirmation and date in the
manifest and produce the candidate for review; do not replace `MAIN.jpg` or
mark the candidate Amazon-ready until auditable account/category evidence and
human approval are recorded.

## Supporting gallery — fixed internal order

| Slot | Variant | Role | Background | Required content |
|---|---|---|---|---|
| **1** | `MAIN` | Hero | Pure white | Centered straight-on complete product; included accessories only; no overlay |
| **2** | `PT01` | Conversion Hero / display | Selected profile + audience family + `FRONT_SCREEN_CARD` or `THREE_QUARTER_SIDE_CARD` | Product remains primary; use one hero attribute, verified supporting cards, and one subordinate Windows 11 Pro card in the variant's protected zone. Gaming 3D mode permits no more than two feature cards. |
| **3** | `PT02` | Use cases | Selected profile + matching continuation pack | Product in one verified use story; 1–3 licensed or original synthetic people/characters only when they clarify the use case; apply metadata and IP review |
| **4** | `PT03` | Full specifications / configuration | Selected profile + matching continuation pack | Audience-appropriate loadout/work grid with verified CPU, display, RAM/SSD tiers and OS; no people |
| **5** | `PT04` | Design and form factor | Selected profile + matching continuation pack | Accurate product angles and verified design facts; narrative effects remain peripheral and may not invent internals or geometry |
| **6** | `PT05` | Performance / platform | Selected profile + matching continuation pack | Gaming pipeline or Business workflow grounded in verified hardware; at most one secondary person; no invented FPS, benchmark, battery or AI claims |
| **7** | `PT06` | What's included | White | Show only the exact unit, power equipment, and accessories included with the SKU |
| **8** | `PT07` | Specification recap | White or light + continuation accents | 4–6 verified facts in the selected family; no people |
| **9** | `PT08` | Connectivity | White/light + continuation ecosystem | Verified rear/side ports and connectivity remain primary; contextual peripherals may not imply inclusion |

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

Supporting PT images may contain concise factual specification text. For this
customized laptop and desktop workflow, `PT01`–`PT08` must use one OEM logo
matching the verified manufacturer of the physical computer. The logo identifies the base product;
it must not imply that the OEM performed, approved, or warrants the seller's
customization. Use official or otherwise approved source artwork and apply it
through deterministic post-production. Never ask a generative model to redraw
lettering or trademarks, and never substitute a seller logo for the product's
OEM logo. Do not add store contact information, warranty advertisements, or
sales claims. A genuine trademark already printed on the photographed chassis
does not need to be removed.

The default Windows treatment is an original text-only OS Proof Tile. Where the
seller has confirmed permission for package-style treatment, PT01 or an
enhanced-main candidate may use a style from `conversion-hero-styles.md`.
Official Windows logo or package artwork requires current commercial-use
rights and the official source asset; an AI approximation is review-only. A
package-style visual must communicate a preinstalled OS and must not imply that
physical retail media is included. Record the OS evidence, visual style,
placement, asset source, rights status, and product center offset.

## Internal visual style

- Select exactly one `image_style_profile` from
  [image-style-profiles.md](image-style-profiles.md) for each product. The
  existing `navy-technical-v1` remains the default; the new
  `feature-led-studio-v1` is an additional option, not a replacement.
- Record the selected profile and reason in `image-manifest.md`; use it
  consistently across PT01–PT08. `MAIN` is profile-independent.
- Use bold, legible sans-serif headings and short factual feature cards.
- Keep one consistent, non-promotional on-screen wallpaper across product views.
- For `Centered Performance + Screen Package`, measure the computer separately
  from all overlays. Keep its horizontal center within 2% of the canvas center,
  use approximately 78%–86% of canvas width, and anchor the Windows visual
  inside the screen's lower-right corner. Never shift the product left to create
  a separate OS column.
- A verified Gaming product must add one G01–G06 treatment from
  `gaming-hero-styles.md`. Keep the screen environment, rear subject,
  frame-break subject, depth effects, and contact light as separate layers.
  Default to original genre imagery; do not use unlicensed game characters,
  logos, screenshots, maps, HUD, skins, signature props, vehicles, or trade
  dress. Keep at least 25% of the screen quiet and use no more than two feature
  cards when this add-on is active.
- A verified Business/Work product must select one B01–B06 treatment from
  `business-work-hero-styles.md`. Office and Copilot claims, icons, logos, and
  package visuals require exact-SKU entitlement evidence; unresolved elements
  are removed rather than inferred. `Lifetime Office` requires seller-approved
  wording and auditable evidence for that SKU.
- PT02–PT08 must use the matching GG01–GG06 or BG01–BG06 pack from
  `supporting-gallery-styles.md`. Keep typography, card geometry, colors,
  lighting, and story world consistent; do not treat each slot as a random
  campaign. PT02 is the primary people scene, PT05 permits at most one
  secondary person when needed, and PT06 never permits people or scene props.
- Every person/character must record asset mode, source, role, count, identity
  and IP review, and synthetic-performer metadata status. People, characters,
  and contextual peripherals cannot cover the product or imply inclusion.
- A Gaming frame-break subject may cross no more than two screen edges and its
  out-of-screen area must remain at or below 12% of the computer's visual
  bounding box. It must stay visually connected to the screen and cannot cover
  the webcam, bezel geometry, hinge, keyboard, touchpad, OEM mark, Windows tile,
  or verified specification text.
- Do not let internal styling override Amazon requirements or accurate product
  representation.
- Keep the OEM logo subordinate to the content. Select its location separately
  for every PT image; there is no universal corner. Its visible mark, keyline,
  badge, and protected clear space must not cover or touch the product, title,
  body copy, feature cards, footers, ports, callout leaders, borders, or
  decorative lines.
- Measure clearance from the final rendered outer edge, including a white
  keyline or badge background. `logo-placement.json` must declare a
  `minimumClearancePx` of at least 16 pixels for the production canvas and a
  `protectedZones` array for every PT image. Keep the rendered logo at least
  that distance from the canvas edge and every recorded protected zone; use a
  larger value when the OEM identity standard requires it. A placement that
  merely avoids pixel overlap but visually touches a card border or decorative
  line is a blocking defect.
- Follow the OEM's approved logo treatment. Circular marks may use the OEM's
  specified white keyline on dark photography; wordmarks may require a neutral
  badge. Preserve source colors, proportions, registration marks, and
  legibility. Do not stretch a circular logo into a rectangle.
- Keep an unbranded master and a per-image `logo-placement.json`. Generate a
  separate review set from those masters, inspect every image at 100%, and
  also inspect a gallery-size thumbnail before approval. The composition script
  must reject insufficient canvas clearance or intersection with a declared
  protected zone. Replace final files only after human approval. If no safe
  placement exists, redesign or regenerate that PT composition and keep the slot
  `BLOCKED` until the correct OEM logo can be placed safely. Do not omit the logo
  and mark the PT image complete.

## Brand and configuration safeguards

- The overlay brand must match the verified physical OEM exactly. A mismatch is
  a blocking defect.
- Every final PT01–PT08 file must contain that verified OEM logo. Missing logo,
  unlicensed logo artwork, or an unsafe placement is a blocking defect. `MAIN`
  remains exempt from added overlays and may show only the OEM mark physically
  present on the genuine product.
- Do not visually present the OEM as the listing seller or imply OEM approval of
  the customization.
- Do not place `Customized by MegaPC`, seller warranty claims, merchant contact
  information, or other seller-specific copy on gallery images. Do not combine
  OEM and seller logos unless a separately approved co-branding rule explicitly
  requires it.
- Document customization and warranty in the listing title, bullet points, and
  product description rather than as gallery advertising.
- Display RAM and SSD tiers only when physically supported and actually offered.
- Show `Win 11 Pro` consistently in the relevant PT images after verifying the
  exact sold configuration, license/activation, and fulfillment process. It is
  a fixed preinstalled specification, never a buyer-selectable customization.
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

