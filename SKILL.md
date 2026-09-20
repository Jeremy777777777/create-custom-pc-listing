---
name: create-custom-pc-listing
description: >-
  Research, create, update, or compliance-check an Amazon Custom PC listing
  from a seller ERP product-detail page for a customized laptop or desktop,
  with one Excel workbook as the only final output. Use when the user provides
  an ERP product URL and wants a MegaPC listing, RAM or SSD customization,
  inactive-listing rebuild, Seller Central attribute completion, image planning,
  or listing QA.
---

# Create or Update an Amazon Custom PC Listing Workbook

Use one Excel workbook as the listing's structured record and final deliverable.
Do not generate separate Markdown, text, research, source, image-shot-list, or
checklist files unless the user explicitly requests one.

## Required resources

- Use [assets/listing-workbook-template.xlsx](assets/listing-workbook-template.xlsx)
  when the user does not provide an existing workbook.
- Read [references/compliance-rules.md](references/compliance-rules.md) before
  writing or approving listing claims.
- Read [references/image-spec.md](references/image-spec.md) when planning or
  producing listing images.

The workbook's Amazon Attribute names, order, and Definition cells are the
authoritative schema. Do not add presumed Amazon fields or rewrite definitions.

## Final output contract

The final output is exactly one `.xlsx` workbook. It contains the listing text,
attributes, offer data, safety and compliance data, image plan, verification
status, and evidence sources.

Do not create these former outputs:

- listing overview
- title file
- bullet-points file
- description file
- customization-config file
- image shot-list or image-source log
- compliance-checklist file
- Product Details Markdown or text file
- Safety & Compliance Markdown or text file
- separate verified-specs or research file

Finished image files may exist outside the workbook when the user asks to
create images. Record their paths in the `Images` sheet; they are production
assets, not additional listing-data outputs.

## Workbook modes

### Update an existing workbook

When the user provides an existing workbook, update it directly unless they ask
for a copy. Identify the product by SKU, ASIN, part number, or another stable
identifier. Never overwrite another product's records.

If the workbook already stores multiple products, update the matching product
block or append a new product block using the workbook's existing pattern.
Preserve prior products, formulas, formatting, definitions, data validation,
freeze panes, and source records.

### Create a new workbook

When no workbook is provided, copy the workbook template and create one workbook
for the requested SKU. Name it clearly, for example:

`MegaPC_Lenovo_ThinkCentre_M70q_Gen5_<SKU>.xlsx`

Do not alter the original template asset.

## Workbook data model

The workbook contains these Seller Central sections:

- `Product Details`
- `Images`
- `Variations`
- `Offer`
- `Safety&Compliance`

Each Amazon Attribute is a column. Use the worksheet's auxiliary rows as
follows:

- `Definition`: fixed Amazon definition; do not edit.
- `Value`: final Seller Central value or listing content.
- `Status`: verification state.
- `Source`: evidence supporting the value.

Use only these statuses unless the workbook already defines an equivalent set:

- `VERIFIED`
- `NOT VERIFIED`
- `USER CONFIRMATION REQUIRED`
- `CONFLICT`
- `NOT APPLICABLE`

The `Definition source` line is template provenance. Leave it unchanged. The
`Source` row is product-specific evidence and must be updated for each listing.

For a multi-product workbook, keep the Definition row once and store each
product as a labeled `Value / Status / Source` block. Include a stable SKU or
ASIN in every block label. Never create a second Definition row for each SKU.

## Workflow

### 1. Read the ERP product page

Treat the user-provided ERP product-detail URL as the primary input for the
entire workflow. A typical URL has this form:

`https://<erp-host>/products/<product-id>`

If the user has not supplied the product URL, ask for it before beginning
product research or writing listing content.

Open the exact URL in the user's authenticated browser session and read it in
place. Use the ERP in read-only mode. Do not edit the product, inventory,
pricing, images, notes, serial numbers, or any other ERP data.

If the URL redirects to a login page, asks for authentication, returns an access
error, or does not expose the product record, stop and ask the user to sign in
or provide an accessible export or screenshot. Never request, store, or reuse
the user's ERP password in the skill or workbook.

Extract every relevant field the page actually provides, including when
available:

- ERP product ID from the URL and page
- product name and internal description
- seller SKU or internal product code
- OEM brand and model family
- exact model, machine type, MPN, part number, or MTM
- UPC, EAN, GTIN, or ASIN
- category and laptop/desktop form factor
- CPU, GPU, memory, storage, display, networking, ports, operating system, and
  included accessories
- condition, customization notes, supplier notes, or stocked configuration
- inventory quantity and offer information that is explicitly intended for the
  Amazon listing
- product images, documents, source links, and other attached evidence

Do not ask the user to re-enter information that is already clear on the ERP
page. Do not copy internal-only notes, costs, supplier terms, serial numbers, or
other operational data into customer-facing listing fields. Serial numbers may
help identify the exact unit, but they are never public listing content unless
the user explicitly requests that use.

Treat ERP values as seller-provided operational data, not automatic proof of an
OEM technical claim. Use them to establish product identity and the stocked
configuration, then verify technical specifications under Step 3. If an ERP
value conflicts with a higher-priority source, preserve both values, set the
affected workbook field to `CONFLICT`, and do not choose silently.

Record the exact ERP product URL in the workbook Source cells for values taken
from the page. Carry the extracted ERP facts forward as the starting dataset for
all remaining steps.

### 2. Identify the exact product

Establish as many of these identifiers as are available:

- seller brand
- OEM brand and model family
- exact model or machine type
- OEM part number or MTM
- seller SKU
- UPC, EAN, or ASIN
- laptop or desktop form factor

Family-level specifications are not automatically SKU-level facts. If an exact
SKU cannot be established, mark affected fields `USER CONFIRMATION REQUIRED`
instead of presenting an inferred value as verified.

Default seller brand is MegaPC unless the user specifies another brand. Preserve
the user's existing rule that MegaPC listings use Windows 11 Pro unless the user
explicitly specifies another edition. Treat the OS as a fixed specification,
not a MegaPC customization.

### 3. Research and verify the base product

Use this source priority:

1. Exact-SKU OEM specification, PSREF, service manual, or product documentation
2. Regulatory or certification documentation
3. Authorized distributor or retailer specification
4. Other retailer sources

Prefer the higher-priority source when sources conflict. Record a conflict in
the workbook instead of choosing silently.

Before offering RAM customization, verify that the machine has replaceable
SO-DIMM memory. `LPDDR`, `onboard`, or `soldered` memory is not upgradeable.
When RAM is soldered, offer storage-only customization if the SSD is serviceable.

### 4. Establish the customization

Separate factory specifications from MegaPC changes:

- Factory: CPU, GPU, display, ports, Wi-Fi, camera, chassis, and other OEM facts
- Customization: RAM and storage only

Do not describe CPU, GPU, operating system, Office software, cleanup, or setup
as a customization. Record offered RAM and SSD tiers in the relevant
`Customizations` or Product Details value cells without inventing new Amazon
Attributes.

### 5. Write the listing content into Product Details

Fill the applicable Product Details attributes directly in the workbook.

- `Item Name`: start with the seller brand, include `Custom` or `Customized`,
  and reference the OEM product with `Created Using ...`. Keep it under 200
  characters.
- `Bullet Point`: place the complete ordered bullet set in the cell, separated
  by Excel line breaks. Bullet 1 must disclose the warranty. The closing bullet
  must disclose that the unit was resealed and that only RAM and/or storage was
  modified.
- `Product Description`: enter the ready-to-paste description. When HTML is
  appropriate, use only `<p>`, `<strong>`, and `<br>`.
- Other attributes: enter only values supported by the exact SKU or an explicit
  seller-provided configuration.

Keep title, bullets, description, OS, customization tiers, warranty, and
technical attributes consistent across the workbook.

### 6. Fill Offer

Complete every applicable Offer attribute provided by the workbook. Do not
invent commercial inputs such as SKU, quantity, price, handling time, shipping
template, tax code, or sale dates. Use `USER CONFIRMATION REQUIRED` when seller
input is needed.

Custom PC offers must follow the fulfillment restrictions in
`references/compliance-rules.md`.

### 7. Fill Safety & Compliance

Complete the provided Safety & Compliance attributes using verified evidence
and the compliance reference. Do not guess country of origin, FCC identifiers,
battery energy, regulatory contacts, or certification numbers.

For a customized PC, ensure `Modified Product` reflects the hardware change.
Apply any OEM-sourcing, battery, dangerous-goods, or contact rules from the
compliance reference only when the evidence and product configuration support
them.

### 8. Plan or record images in Images

Use `MAIN` and `PT01` through `PT08` exactly as provided.

For each slot:

- `Value`: production brief, final image filename, or final image path
- `Status`: image readiness or verification status
- `Source`: licensed OEM media source or seller-owned photograph source

Follow the original page image requirements preserved in the sheet and the
rules in `references/image-spec.md`. Do not create a separate shot-list or
sources file.

### 9. Handle Variations

The template currently contains no Variation attributes. Preserve its note and
do not invent variation fields. If Seller Central later exposes fields, update
the workbook schema from the newly captured official definitions before using
them.

### 10. Validate the workbook

Before delivery, check:

- exact product identity is clear
- ERP product ID, seller SKU, and exact product URL are retained where available
- customer-facing fields do not expose internal notes, costs, or serial numbers
- RAM customization is physically feasible
- title begins with the seller brand and uses compliant OEM framing
- warranty disclosure is the first bullet
- closing disclosure identifies the RAM and/or SSD modification
- software is not described as a customization
- OS edition is consistent everywhere
- technical claims agree across listing text and attributes
- image briefs match the verified configuration
- required commercial inputs are present or clearly awaiting the user
- safety and regulatory claims have evidence
- every populated value has an appropriate Status and Source
- no unresolved `CONFLICT` is presented as publish-ready
- Amazon Attribute names and Definitions remain unchanged

Use the workbook's status cells as the validation record. Do not create a
separate checklist file.

### 11. Deliver

Save and return only the completed workbook. Tell the user which fields still
have `NOT VERIFIED`, `USER CONFIRMATION REQUIRED`, or `CONFLICT` status. Do not
claim the listing is ready to publish while a material blocker remains.

## Maintenance boundary

`references/compliance-rules.md` owns policy rules.
`references/image-spec.md` owns image-production rules.
The Excel template owns Amazon Attribute names, field order, and definitions.
Keep each rule in its owning resource instead of duplicating detailed reference
content in this file.
