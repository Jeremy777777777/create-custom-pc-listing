# MegaPC listing writing guide

Apply [confirmed-catalog-defaults.md](confirmed-catalog-defaults.md) first. This guide controls expression, not product facts. Write original English from the verified base configuration; competitor pages are market references only.

## Title

`MegaPC Custom [Product Type], Created Using [OEM Model], [Display/GPU/Form Differentiator], [CPU], [Installed RAM], [Installed SSD], [Verified Relevant Features], Win 11 Pro`

Use the actual base values, never selectable tiers. Select only useful verified features, such as Backlit Keyboard, FP Reader, Touchscreen or an accurate wireless standard. No feature is a required bundle. Target ≤200 characters; remove redundant adjectives/secondary features before identity or core capacity facts. Gaming/Business positioning must match actual evidence.

## Five bullets

Bullet 1 is the exact mandatory warranty text from catalog policy; no heading or rewritten wording is inserted into it. Remaining bullets use `Benefit Heading — verified fact + practical buyer value` with short headings and 1–2 sentences.

| Order | Purpose |
| --- | --- |
| 1 | Exact OEM/MegaPC warranty disclosure |
| 2 | Strongest verified purchase reason |
| 3 | Supporting CPU/GPU/platform performance; no invented benchmarks |
| 4 | Base RAM/SSD, actual customization and useful capacity |
| 5 | Verified display/input/connection experience and fixed OS as appropriate |

Avoid repeating the same full specification list. Combine adjacent topics as needed, but warranty stays first. In the workbook's single Bullet Point cell store exactly five paragraphs separated by one blank line (`\n\n` in code, actual newline characters in Excel). Publication adapters split on blank lines into the five channel bullet fields.

## Description

Store the following HTML structure as literal text in the workbook's existing Product Description Value cell, following the user's 2026-10-07 decision. Bold the opening identity and every section heading with `<strong>`. Use one `<br/>` between a section heading and its body, and two `<br/><br/>` after the identity and between sections. Actual newlines in the example only make the source readable; the tags control displayed breaks. A single-line HTML string is preferred for reproducible output. Do not use Markdown bold, heading backslashes, `</br>` or Excel-only font styling as the saved description format.

```html
<strong>MegaPC Custom [Product Type] — Created Using [OEM Model]</strong><br/><br/>
<strong>[Primary Benefit]</strong><br/>[Verified specification and its practical value.]<br/><br/>
<strong>[Processor / Graphics]</strong><br/>[Verified base hardware and appropriate tasks.]<br/><br/>
<strong>[Memory & Storage]</strong><br/>[Installed base RAM/SSD and actual MegaPC modifications; no selectable tiers.]<br/><br/>
<strong>[Experience & Connectivity]</strong><br/>[Relevant verified computer capabilities.]<br/><br/>
<strong>Windows 11 Pro</strong><br/>[Fixed seller OS; no implied Office or paid Copilot entitlement.]<br/><br/>
<strong>Warranty and Disclosure</strong><br/>[Insert the complete mandatory warranty text without rewriting it.]
```

Escape special characters in copy when needed (`&amp;`, `&lt;`, `&gt;`); preserve visible facts and punctuation. Do not wrap or rewrite the fixed warranty paragraph, add text after it or add trailing break tags. Validate balanced strong tags, break separators and the exact final warranty paragraph using scripts/warranty_policy.py. The workbook stores HTML text; Excel itself need not render it as formatted text. Amazon publication rendering is a separate check, not a promised outcome of the stored format.

Sections may be combined/omitted when irrelevant; Warranty and Disclosure is last. Do not present OS upgrades as buyer-selectable software customization or state that all software remains factory configured. Other hardware stays factory configured, with actual RAM/storage changes described accurately. No unsupported FPS, battery/runtime, compatibility, thermal or security guarantees. Exact facts must agree across title, bullets, description, attributes and images. Run [compliance-rules.md](compliance-rules.md) before marking publication ready.

Warranty and Disclosure wording is directly confirmed by the user on 2026-10-05. Use the fixed paragraph unchanged in all three locations, with only the manufacturer substituted; no style/model exception. Run scripts/warranty_policy.py validation through check-workbooks.py for Listing workbooks. OEM applicability and actual seal-opening/customization consistency remain seller manual publication checks, not blockers to draft generation.
