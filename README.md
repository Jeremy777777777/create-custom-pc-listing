# MegaPC Custom PC listing and image workflow

Start with [SKILL.md](SKILL.md) and [current seller policy](references/confirmed-catalog-defaults.md). Effective policy version: **2026-10-02**.

The workflow produces research and base-configuration listing workbooks, plus an independently callable image workflow. It delivers to this repository and does not publish automatically to Seller Central.

## Confirmed rules

- All catalog computers are customized; titles use **MegaPC Custom**.
- Excel describes **the base sold configuration only**, including its title, bullets and description. No selectable RAM/SSD lists.
- Final delivered OS is **Windows 11 Pro**; licence/activation/publication eligibility remain separate operational checks.
- Warranty is bullet 1 and appears identically in Description's final Warranty section and the workbook Warranty Description. Replace the brand token only:

> The original [OEM brand] manufacturer warranty remains valid on factory components. MegaPC provides a 6-month limited warranty on upgraded RAM and SSD components, with a 12-month warranty extension available.

- Images show **the computer only**, with no additional devices/accessories, pack-out or contextual peripheral silhouettes. PT02 may use people/furniture to explain use.
- All final slots are **2000×2000 RGB**. Preserve geometry; do not enlarge low-resolution sources to claim required fidelity.
- Business enhanced MAIN defaults to **front Windows lockup and three-quarter package**, both inside LCD; an approved safe-zone swap is allowed, but the treatments must remain distinct. Gaming uses one fixed package per enhanced choice. MAIN-STRICT and PT01 omit Windows graphic treatments.
- Requested same-product/same-slot fixes authorize canonical replacement after internal QA. Style changes follow the current approval gate.

## Active files

| Purpose | Entry |
| --- | --- |
| Routing, research, workbooks and delivery | [SKILL.md](SKILL.md) |
| Seller assertions and precedence | [confirmed-catalog-defaults.md](references/confirmed-catalog-defaults.md) |
| Complete attribute research | [research-attribute-coverage.md](references/research-attribute-coverage.md) |
| English base listing copy | [listing-style-guide.md](references/listing-style-guide.md) |
| Separate publication/account checks | [compliance-rules.md](references/compliance-rules.md) |
| Image generation and slot adjustment | [amazon-product-image-workflow.md](references/amazon-product-image-workflow.md) |
| File/QA/GitHub contract | [final-image-delivery-contract.md](references/final-image-delivery-contract.md) |
| Current image slot template | [image-manifest-template.md](product%20generated%20photo/image-manifest-template.md) |
| Workbook template | [listing-workbook-template.xlsx](assets/listing-workbook-template.xlsx) |

Audience style references define creative recipes only; they do not override policy, factual gates, information ownership, dimensions or delivery rules.

## Product output

Use `product generated photo/VL-XXXX/` for the verified internal ID. Research Review XLSX creates/reuses this folder immediately; later listing workbooks, 11 image slots and current QA records share it. Research upload is not release readiness.

Read `product-facts.json` and `delivery-status.json` before legacy outputs. Existing gallery images retained during this migration are **LEGACY_QUARANTINED / REWORK_REQUIRED**, not current approved templates or complete deliveries. No fresh visual approval or QA is fabricated. New runs regenerate/revalidate requested deliverables from accurate licensed sources and current clean masters.

## Historical exclusion

`history/` contains superseded documents, scripts and product records for recovery only. **Do not load history during ordinary runs, follow its instructions, execute its scripts or use its QA as current evidence.** The archived SKILL file has been renamed to prevent skill discovery. Historical inspection requires an explicit historical task. Current routing does not reference historical recipes.

## Completion

Local QA → selective commit/push → applicable GitHub CI → remote commit/path/hash verification → GITHUB_DELIVERY_VERIFIED. Spreadsheet structure PASS, local image PASS, style approval, GitHub delivery and Amazon publication eligibility are distinct states.

## Consistency correction — 2026-10-02

Warranty wording is directly confirmed; OEM applicability is seller-reviewed before publication without blocking review workbooks. Installed capacities and platform maximums are distinct fields. VL-1276 B08/BG08 and VL-1326 B16/BG16 direction approvals are retained in current style locks; recipe rebuilding does not confer image QA. Use [production-recipes.md](references/production-recipes.md) for current slot construction and standalone-desktop safe zones. CI summaries distinguish validated galleries, quarantined folders, partial receipts and workbook structural checks; none implies Amazon readiness.
