# MegaPC Custom PC listing and image workflow

FCC research is an independently requested `FCC_LOOKUP_ONLY` task. Follow [standalone FCC / ERP inventory](references/fcc-research-workflow.md). Do not research or store FCC identifiers, candidates, raw serials or lookup evidence in new Listing Research / Draft workbooks. Other product-attribute and serial-first research remains required.

Start with [the current execution router](references/current-workflow.md). It selects research/copy, Business/Gaming/Mini PC images, single-image review and scoped delivery. Current GitHub → Drive synchronization is manual through connected tools; new runs use scripts/workflow_run.py for CONNECTOR, LOCAL, BROWSER or MIXED execution.

The workflow produces research and base-configuration listing workbooks, plus an independently callable image workflow. All final product images, Excel and supporting business records are delivered to [Google Drive](https://drive.google.com/drive/folders/1Knp8RUWyw5N1MownbfJSSo-m6NgrqrQq). GitHub maintains workflow code, rules, reusable templates and tests. It does not publish automatically to Seller Central. Read [Google Drive delivery](references/google-drive-delivery.md) before product work; existing repository outputs are historical and are not a synchronized current Drive mirror.

## Confirmed rules

- All catalog computers are customized; titles use **MegaPC Custom**.
- Numeric Excel attributes describe the base sold configuration only. Customized titles, bullets and descriptions show [SSD and RAM customization choices](references/customization-options-policy.md): SSD 512GB / 1TB / 2TB / 4TB; replaceable RAM 8GB / 16GB / 32GB / 64GB with exact researched type; fixed RAM actual capacity/type. Do not filter seller choices by hardware maximum.
- Final delivered OS is **Windows 11 Pro**; licence/activation/publication eligibility remain separate operational checks.
- Warranty is bullet 1 and appears identically in Description's final Warranty and Disclosure section and the workbook Warranty Description. Replace the brand token only:

> MegaPC provides a 1-year limited warranty on the upgraded RAM and SSD components. The original [OEM brand] manufacturer warranty remains valid on all remaining factory components, so you are covered on both the base machine and our upgrades. The original seal has been opened solely for upgrading purposes.

- Images show **the computer only**, with no additional devices/accessories, pack-out or contextual peripheral silhouettes. PT02 may use people/furniture to explain use.
- Final slots follow the [Amazon-based size policy](references/image-spec.md), not a fixed square resolution. Preserve geometry; do not enlarge low-resolution sources to claim required fidelity.
- Business enhanced MAIN defaults to **front Windows lockup and three-quarter package**, both inside LCD; an approved safe-zone swap is allowed, but the treatments must remain distinct. Gaming integrated-display enhanced choices use one compact genuine Windows edition identity; no mandatory package-sized block. MAIN-STRICT and PT01 omit Windows graphic treatments.
- Requested same-product/same-slot fixes authorize canonical replacement after internal QA. Style changes follow the current approval gate.

## Active files

Workflow changes follow [GitHub → Drive synchronization](references/github-drive-sync.md): every push creates a commit backup; validated current main updates Drive's current workflow pointer. Each product generation records the workflow SHA and checks its actual Drive sync receipt. Initial activation requires the documented GitHub Actions Secrets; missing authorization is reported as blocked.

| Purpose | Entry |
| --- | --- |
| Routing, research, workbooks and delivery | [SKILL.md](SKILL.md) |
| Default full output Excel: complete copy, seven rows, technical research, candidates and current Drive delivery | [output-excel-contract.md](references/output-excel-contract.md) |
| Seller assertions and precedence | [confirmed-catalog-defaults.md](references/confirmed-catalog-defaults.md) |
| Complete attribute research | [research-attribute-coverage.md](references/research-attribute-coverage.md) |
| Official source priority, conflict decisions, deep search and honest missing-field outcomes | [evidence-chain-and-deep-research.md](references/evidence-chain-and-deep-research.md) |
| Scoped access, Drive parent checks, residual questions and upload-record privacy | [research-operations-preflight.md](references/research-operations-preflight.md) / [operations policy](assets/listing-operations-policy.json) / [privacy helper](scripts/delivery_privacy.py) |
| Scoped facts, template projection and mandatory pre-export evidence checks | [research-ledger-projection.md](references/research-ledger-projection.md) / [JSON schema](assets/research-ledger-schema.json) |
| Current stage files versus immutable historical workbook bundles | [workbook-stage-snapshots.md](references/workbook-stage-snapshots.md) |
| PC information: ERP current/historical serial → OEM as-built parts → sold-configuration reconciliation | [serial-number-product-research.md](references/serial-number-product-research.md) |
| FCC: updated guide's brand routes, actual driver-package inspection, scoped candidates and Excel progress colors | [fcc-research-workflow.md](references/fcc-research-workflow.md) |
| FCC workflow Chinese Word reading copy and version binding | [Word manual](references/manuals/fcc-id-lookup-manual.docx) / [reading-copy maintenance](references/manuals/README.md) |
| English base listing copy | [listing-style-guide.md](references/listing-style-guide.md) |
| Separate publication/account checks | [compliance-rules.md](references/compliance-rules.md) |
| Image generation and slot adjustment | [amazon-product-image-workflow.md](references/amazon-product-image-workflow.md) |
| File/QA/GitHub contract | [final-image-delivery-contract.md](references/final-image-delivery-contract.md) |
| Current image slot template | [image-manifest-template.md](product%20generated%20photo/image-manifest-template.md) |
| Mini PC / Gaming original-media information design | [Complete source-to-replacement workflow](references/mini-gaming-real-source-workflow.md), [planning template](assets/mini-gaming-information-plan-template.json), [style routing policy](assets/mini-gaming-style-policy.json) |
| Reference-driven Business Laptop B17/BG17 | [Graphite Business design system](references/business-graphite-design-system.md) |
| Business defaults/approval decisions (existing rules retained) | [Policy decisions](references/business-graphite-policy-decisions.md) |
| Workbook template | [listing-workbook-template.xlsx](assets/listing-workbook-template.xlsx) |
| Preferred Python/Jupyter environment for text and images | [Testing preference](references/python-jupyter-testing.md) / [setup and reusable tests](local-testing/README.md) |

Audience style references define creative recipes only; they do not override policy, factual gates, information ownership, dimensions or delivery rules.

## Product output

Use `product generated photo/<internal-id>/`, preserving the verified ID and prefix (for example VL-1221 or VD-744). Research Review XLSX creates/reuses this folder immediately; later listing workbooks, 11 image slots and current QA records share it. Research upload is not release readiness.

Read `product-facts.json` and `delivery-status.json` before legacy outputs. Existing gallery images retained during this migration are **LEGACY_QUARANTINED / REWORK_REQUIRED**, not current approved templates or complete deliveries. No fresh visual approval or QA is fabricated. New runs regenerate/revalidate requested deliverables from accurate licensed sources and current clean masters.

## Historical exclusion

`history/` contains superseded documents, scripts and product records for recovery only. **Do not load history during ordinary runs, follow its instructions, execute its scripts or use its QA as current evidence.** The archived SKILL file has been renamed to prevent skill discovery. Historical inspection requires an explicit historical task. Current routing does not reference historical recipes.

## Completion

Product delivery: local QA → upload individual images/original XLSX and evidence to Drive → read back file IDs/parents/MIME/size/checksums → save receipt/current links → DRIVE_DELIVERY_VERIFIED for the stated scope. GitHub CI applies independently to workflow-code changes and retained fixtures. Spreadsheet structure PASS, local image PASS, style approval, Drive delivery and Amazon publication eligibility are distinct states. Never commit new product business files as the final delivery.

## Consistency correction — 2026-10-02

Warranty wording is directly confirmed; OEM applicability is seller-reviewed before publication without blocking review workbooks. Installed capacities and platform maximums are distinct fields. VL-1276 B08/BG08 and VL-1326 B16/BG16 direction approvals are retained in current style locks; recipe rebuilding does not confer image QA. Use [production-recipes.md](references/production-recipes.md) for current slot construction and standalone-desktop safe zones. CI summaries distinguish validated galleries, quarantined folders, partial receipts and workbook structural checks; none implies Amazon readiness.

Current Gaming visual baseline: [gaming-approved-main-fit.md](references/gaming-approved-main-fit.md). VL-1221 enhanced front is the exact user-supplied, user-confirmed Amazon-accepted image; its native-size exception is scoped to that file and hash. Remaining gallery QA and remote upload are separate.
