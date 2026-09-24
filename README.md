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
assets/
  listing-workbook-template.xlsx              Listing workbook template
  amazon_sellercentral_attributes_definitions.md  Captured field-definition reference
product generated photo/
  README.md                                   Image-delivery folder convention
  VL-<internal-model>/                        Per-product images and manifest
```

## How the Markdown files work together

Start with [`SKILL.md`](SKILL.md). It routes listing work through the compliance
rules, writing guide, Seller Central field reference, and Excel template. After
the relevant listing facts are verified, a separate image task follows
[`references/amazon-product-image-workflow.md`](references/amazon-product-image-workflow.md)
and [`references/image-spec.md`](references/image-spec.md). Finished image files
and their `image-manifest.md` are delivered under
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
