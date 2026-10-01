# MegaPC Amazon Custom PC Workflow

This repository contains one end-to-end workflow with two coordinated outputs:

1. a verified Amazon listing workbook for human Seller Central review
2. an independently callable image child workflow that delivers exactly 11 final images per `VL-XXXX`: three alternative MAIN files and PT01–PT08

Nothing in this repository authorizes automatic publishing to Seller Central.

Catalog-wide seller defaults and autonomous research follow
[`references/confirmed-catalog-defaults.md`](references/confirmed-catalog-defaults.md):
Windows 11 Pro; 6-month warranty + 12-month extended warranty; computer-only
gallery imagery; internal SSD and installed RAM cross-validation; independently
source exact-model high-resolution angles from OEM, Best Buy and Amazon.
Previously approved product styles remain approved during the same task.

## Repository map

```text
SKILL.md                                      Main workflow and task router
references/
  input-source-cross-validation.md           MyStore/Checking List input and conflict rules
  compliance-rules.md                        Listing and customization gates
  listing-style-guide.md                     Title, bullets, and description style
  amazon-product-image-workflow.md            Separate image-production workflow
  image-spec.md                               Three MAIN variants and PT01-PT08 requirements
  final-image-delivery-contract.md             No-draft final-asset delivery and Gaming signature MAIN
  image-style-profiles.md                     Selectable per-model PT visual styles
  conversion-hero-styles.md                   Centered hero and Windows 11 Pro treatments
  hero-composition-variants.md                Front-facing and three-quarter enhanced-MAIN composition layer
  gaming-hero-styles.md                       Six original 3D gaming hero add-ons
  gaming-core-badge-styles.md                 Six Gaming core-config compositions + enhanced-MAIN Windows rules
  business-work-hero-styles.md                 Business/Work hero routing and entitlement gates
  business-laptop-gallery-styles.md            B07–B16 end-to-end Business laptop galleries
  supporting-gallery-styles.md                 Gaming/Business PT02-PT08 continuation packs
assets/
  listing-workbook-template.xlsx              Listing workbook template
  amazon_sellercentral_attributes_definitions.md  Captured field-definition reference
product generated photo/
  README.md                                   Image-delivery folder convention
  image-manifest-template.md                  New-model style and slot template
  VL-<internal-model>/                        Per-product images and manifest
```

## How the Markdown files work together

Start with [`SKILL.md`](SKILL.md). It routes listing work through the compliance
rules, writing guide, Seller Central field reference, and Excel template. After
the relevant listing facts are verified, a separate image task follows
[`references/final-image-delivery-contract.md`](references/final-image-delivery-contract.md),
[`references/amazon-product-image-workflow.md`](references/amazon-product-image-workflow.md)
and [`references/image-spec.md`](references/image-spec.md). Image production
selects one per-model profile from
[`references/image-style-profiles.md`](references/image-style-profiles.md); the
existing navy style remains available and the feature-led studio style is an
additional option. Enhanced-main candidates and PT01 also follow
[`references/conversion-hero-styles.md`](references/conversion-hero-styles.md),
including the preferred `Centered Performance + Screen Package` base preset.
Verified gaming models then select one of sixteen original 3D genre treatments
from [`references/gaming-hero-styles.md`](references/gaming-hero-styles.md).
The selected treatment is required across both completed enhanced-MAIN choices
and `PT01`; both enhanced choices use the approved white-catalog 3D frame-break
signature when C07 is selected, while the default strict Amazon `MAIN` never uses it. Only a continuous 3D subject may cross the LCD boundary; effects and six verified specification cards remain inside. Cards may occupy approved corners or staggered zones, not a fixed row. Authentic factory OEM marks on the exact computer are preserved. Each Gaming hero also selects one of
seven core-configuration compositions and one of sixteen matching asset-card skins from
[`references/gaming-core-badge-styles.md`](references/gaming-core-badge-styles.md).
Business/Work models instead select one of sixteen productivity treatments from
[`references/business-work-hero-styles.md`](references/business-work-hero-styles.md)
after the workflow verifies the exact Office/Copilot entitlement. The workflow
records the audience evidence, confidence, and routing reason so Gaming,
Business/Work, Student/Study, and General products do not silently share the
wrong visual language.
Business laptops may additionally select one of ten complete B07–B16/BG07–BG16
systems from
[`references/business-laptop-gallery-styles.md`](references/business-laptop-gallery-styles.md),
which emphasize collaboration tools, mobility, executive workflows, verified AI
tools, or secure hybrid work across all three MAIN variants and PT01–PT08.
Production creates both enhanced compositions from
[`references/hero-composition-variants.md`](references/hero-composition-variants.md).
The front and three-quarter variants map to every Gaming G/C family and every
Business B family; the angled variant requires a verified, licensed exact-model product view. PT01 may
reuse that angle, but it must omit the Windows package and use a different focus.
The selected hero family then continues through PT02–PT08 using the matching
Gaming or Business story pack in
[`references/supporting-gallery-styles.md`](references/supporting-gallery-styles.md),
including controlled use of licensed or original synthetic people where a real
use case benefits from them.
Business `MAIN-ENHANCED-FRONT-CANDIDATE` and
`MAIN-ENHANCED-THREE-QUARTER-CANDIDATE` use different fixed Windows forms:
one approved logo lockup and one package. Both remain wholly inside the LCD.
Other audience families follow their own fixed-package rules.
`MAIN-STRICT` and PT01 never use a Windows asset.
All branded assets require recorded commercial-use rights.
Finished image files and their `image-manifest.md` are delivered under
[`product generated photo/`](product%20generated%20photo/); they are not written
back into the listing workbook.
The image branch may be invoked by itself for generation or adjustment when the
user does not need the listing copy and workbook rebuilt.

```text
MyStore product and/or Checking List row
  -> source mapping and field-level cross-validation
  -> research and fact validation
  -> listing copy and workbook
  -> compliance and human review
  -> separate image plan and production
  -> image QA
  -> mandatory GitHub upload under product generated photo/VL-XXXX/
  -> remote file/hash and applicable CI verification
  -> GitHub folder delivery and human review
```


Final image generation includes GitHub delivery by default. Upload all 11 finished images and QA records to `product generated photo/VL-XXXX/` using the verified internal ID, then verify the remote files and applicable CI. Local images, a ZIP, or workflow-only commits are not completed gallery delivery. Only an explicit local-only/no-upload/concept request skips this step. Report completion with the GitHub folder and commit links after `GITHUB_DELIVERY_VERIFIED`; see [the delivery contract](references/final-image-delivery-contract.md#7-默认-github-最终交付强制).
