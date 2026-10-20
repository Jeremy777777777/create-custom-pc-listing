# Product output folders

Final-storage amendment — 2026-10-20: this directory is local working storage and retains historical GitHub product records. Deliver all new images, original Research Review/Listing XLSX and supporting business records to Google Drive under [the current Drive delivery contract](../references/google-drive-delivery.md). Follow the existing Drive README: Listing Draft in `01_LISTING`, Research Review in `03_RESEARCH`, individual images in `02_IMAGES`, reviews/receipts in `04_QA`, and supporting originals in `90_SOURCE`. Preserve missing/draft/partial/QA states. The previous commit/push completion wording below is historical; new product completion requires actual Drive upload and byte verification. GitHub now maintains workflow code, rules, reusable templates and tests.

Use one verified internal-ID folder: `VL-XXXX/`. Upload a real Research Review workbook as soon as available; later base-configuration listing workbooks, final images and current QA share the same folder. Never overwrite the source template.

Read `product-facts.json` and `delivery-status.json` first. `LEGACY_QUARANTINED` images remain recoverable but are not approved examples or completed deliveries. Retired workbook, manifest, QA and delivery records are historical only and must not be loaded in a normal run.

For current production follow `../SKILL.md` and start from `image-manifest-template.md`. A complete current gallery has exactly three MAIN alternatives and PT01–PT08, all 2000×2000 RGB/RGBA with opaque final backgrounds (JPEG must be RGB), plus records. Research-only folders need not contain images. Computer-only imagery has no external equipment or accessories.

Local QA precedes selective commit/push; applicable CI and remote hash verification precede completion. Requested same-slot replacement is authorized after internal QA. Unrelated image bytes must stay unchanged.
