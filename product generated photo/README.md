# Product-generated photos

Final Amazon gallery images are organized by verified internal model under
`VL-<internal-model>/`. Each canonical product folder contains exactly **11
final image files**: three different completed MAIN choices (`MAIN-STRICT`,
front enhanced, and three-quarter enhanced) plus `PT01`–`PT08`. Manifest and
Logo placement records are additional files and do not count toward 11.

Follow [the dedicated product-image workflow](../references/amazon-product-image-workflow.md)
and [the current image specification](../references/image-spec.md), then select
one per-model visual profile from
[the image style profiles](../references/image-style-profiles.md). Record the
profile and reason in `image-manifest.md`. Each product
folder contains `MAIN-STRICT`, `MAIN-ENHANCED-FRONT-CANDIDATE`,
`MAIN-ENHANCED-THREE-QUARTER-CANDIDATE`, `PT01`–`PT08`, and an
`image-manifest.md` production record. The three MAIN files are alternatives for
one Amazon MAIN slot. Start new models from [`image-manifest-template.md`](image-manifest-template.md).
Image work is separate from the listing workbook.
It is an independently callable child workflow under the complete MegaPC
listing workflow: a user may generate or adjust images for one `VL-XXXX`
without regenerating listing copy or the Excel workbook. Approved review images
must be copied into the canonical `VL-XXXX/` folder; review-suffixed directories
are not final GitHub delivery locations.
