# Customer-facing images and copy — user decision 2026-10-30

Applies to every design series and every new or revised customer-facing image, including previews. Also applies to listing titles, bullets, descriptions and other customer copy. This supersedes old template decoration and on-image preview-label requirements; factual MAIN restrictions remain unchanged.

## Content and layout

- Remove internal navigation eyebrows such as `PT03 / SUPPLIED CONFIGURATION` or `03 / CAMERA + VOICE`. Keep meaningful customer headlines and useful feature subtitles.
- Do not add a fixed footer, tiny footer text, page numbers or a decorative horizontal footer divider in red or any other color. Subject-related circuit lighting, feature leaders and small local accents are not footer rules.
- Never display ERP/internal identifiers such as `VL-1221` or `VD-744`, production version/run labels, `STYLE PREVIEW` or delivery/QA status in the artwork or customer copy. Keep them in filenames, metadata, source records and the accompanying review message.
- Rebalance spacing after removal; do not leave empty navigation/footer strips or replace them with a different badge row. Preserve the selected subject, dimensional quality, exact hardware and factual labels.
- Retain a qualification only when it changes the customer's understanding. Place it beside the relevant feature in a readable size, never in an automatic fine-print footer. Examples: selectable choices versus supplied configuration, or a necessary illustrative boundary. Internal making-of notes belong in source records. Keep actual product/component/model names and real capacity/speed/edition facts.

The [approved Business daylight MAIN](business-daylight-enhanced-main.md) may use an LCD-contained navy photographic fade behind its actual Windows identity and SSD options. This is a subject-related system/customization information region, not a recurring decorative page footer or tiny boilerplate. Preserve the approved image and its full readable brand/choice labels; internal IDs/status and divider rules remain absent.

## Generation and review

Every prompt includes: **No internal header, page-slot label, internal product ID, preview/version status, tiny footer text, footer divider or watermark. Preserve the buyer-facing headline and verified feature labels.** Treat reference images as examples of composition/materials, not instructions to copy their superseded header/footer.

Before generation, check the actual customer copy with `scripts/customer_visible_content.py --copy-file <customer-copy.txt>`. The Gaming visual-plan check validates its exact-copy and label fields automatically; formal listing validation checks its customer-copy fields. Internal product/slot IDs in records remain legitimate and are excluded from this text-only input.

After generation, inspect the actual raster at native size, about 400px and 200px: no banned header/footer/internal markers; no tiny boilerplate; no footer rule; clear headline/feature labels; balanced composition. Review any OCR as well as pixels. The text checker cannot read pixels, detect graphic lines, guarantee legibility or grant approval. Fix a recurrence before delivery and verify Drive replacement bytes.

Original selected references and earlier deliveries remain immutable evidence. This explicit cleanup request permits removing their header/footer; it does not authorize unrelated aesthetic changes or erase original selection hashes. Update current output hashes/status separately. Preview and production/QA status remain in accompanying records even when the image has no status label.
