# MegaPC Amazon Custom PC Workflow

This repository contains one end-to-end workflow with two coordinated outputs:

1. a verified Amazon listing workbook for human Seller Central review
2. a separate nine-image gallery package for human image review

Nothing in this repository authorizes automatic publishing to Seller Central.

## Repository map

```text
SKILL.md                                      Main workflow and task router
references/
  input-source-cross-validation.md           MyStore/Checking List input and conflict rules
  compliance-rules.md                        Listing and customization gates
  listing-style-guide.md                     Title, bullets, and description style
  amazon-product-image-workflow.md            Separate image-production workflow
  image-spec.md                               MAIN and PT01-PT08 requirements
  image-style-profiles.md                     Selectable per-model PT visual styles
  conversion-hero-styles.md                   Centered hero and Windows 11 Pro treatments
  gaming-hero-styles.md                       Six original 3D gaming hero add-ons
  gaming-core-badge-styles.md                 Six Gaming core-config + Windows compositions
  business-work-hero-styles.md                 Six Business/Work Office and Copilot treatments
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
[`references/amazon-product-image-workflow.md`](references/amazon-product-image-workflow.md)
and [`references/image-spec.md`](references/image-spec.md). Image production
selects one per-model profile from
[`references/image-style-profiles.md`](references/image-style-profiles.md); the
existing navy style remains available and the feature-led studio style is an
additional option. PT01 and approved enhanced-main candidates also follow
[`references/conversion-hero-styles.md`](references/conversion-hero-styles.md),
including the preferred `Centered Performance + Screen Package` base preset.
Verified gaming models then select one of six original 3D genre treatments
from [`references/gaming-hero-styles.md`](references/gaming-hero-styles.md).
These treatments are for `PT01` or a separately gated enhanced-main candidate,
never the default strict Amazon `MAIN`. Each Gaming hero also selects one of
six Windows 11 Pro and core-configuration compositions from
[`references/gaming-core-badge-styles.md`](references/gaming-core-badge-styles.md).
Business/Work models instead select one of six productivity treatments from
[`references/business-work-hero-styles.md`](references/business-work-hero-styles.md)
after the workflow verifies the exact Office/Copilot entitlement. The workflow
records the audience evidence, confidence, and routing reason so Gaming,
Business/Work, Student/Study, and General products do not silently share the
wrong visual language.
Text-only OS treatments are the default; official lockup/package assets require
recorded commercial-use rights.
Finished image files and their `image-manifest.md` are delivered under
[`product generated photo/`](product%20generated%20photo/); they are not written
back into the listing workbook.

```text
MyStore product and/or Checking List row
  -> source mapping and field-level cross-validation
  -> research and fact validation
  -> listing copy and workbook
  -> compliance and human review
  -> separate image plan and production
  -> image QA and human review
```
