# VL-1213 — ThinkPad P16v Gen 3 gallery

Input ASIN **B0HC4D4X9M** maps explicitly to ERP product **31213 / VL-1213**. The current physical child PL-1254 identifies Core Ultra 7 265H, RTX PRO 2000 Blackwell, 64GB DDR5, 1TB SSD and Windows 11 Pro. Image-only scope: no workbook recreated.

The user approved the product-specific **B15 / BG15 Architectural Precision** preview on 2026-10-16 with “批准”. The current catalog policy is 2026-10-02 with its later recorded amendments. Original authorized Lenovo hardware pixels are retained; ImageGen created only the original architectural stage, empty workspace and LCD scene. Final text, Windows identity and the original Lenovo logo are deterministic layers.

## Eleven individual images

| Files | Role | Decoded size |
|---|---|---|
| MAIN-STRICT.jpg | Complete actual computer on white, original OEM LCD wallpaper, no added overlays | 1120×950 |
| MAIN-ENHANCED-FRONT-CANDIDATE.png | White exterior, architecture and fixed Windows lockup inside LCD | 1120×950 |
| MAIN-ENHANCED-THREE-QUARTER-CANDIDATE.png | Native original angle with LCD-contained scene and distinct fixed Windows package | 640×540 |
| PT01.png–PT08.png | Purchase reason, workspace, sole base configuration, display/form, task flow, white input detail, battery value, physical port map | 1536×1024 each |

The three MAIN files are alternatives for one marketplace slot. The angle intentionally retains the available original detail without enlargement; it meets the workflow's 500px general minimum but not its 1000px zoom recommendation. Enhanced candidates have **NOT_ASSESSED** Amazon MAIN eligibility. Production QA and repository delivery do not establish marketplace acceptance.

## Evidence and rebuild

- `product-facts.json`: single current image fact record and exact source mapping. No selectable RAM/SSD lists, unverified brightness/gamut, optional SIM/smart-card or wireless-version claim.
- `style-lock.json`: explicit user direction approval and versioned recipe.
- `image-manifest.md`, `visual-review.json`, `semantic-review.json`: actual assistant multimodal inspection notes, current hashes, supplied input binding, slot ownership and limitations. No separate human certification is claimed.
- `logo-placement.json`, `logo-qa.json`, `final-image-qa.json`: measured original-asset placement, byte bindings and local acceptance.
- `production-v1/`: original OEM references, original generated scene layers, prompt set, fixed identity assets, exact recipe, renderer, 28 semantic comparisons, boundary and repeat-build checks. The approved preview is a direction reference only, not an accepted hardware layer.
- Raw unit serials and private source URLs are omitted from public records. As-built keyboard and battery FRUs are retained without identifying the unit.

On the user's Windows setup, from the repository root:

```powershell
& 'C:/Users/jerem/anaconda3/envs/listing-testing/python.exe' 'product generated photo/VL-1213/production-v1/render.py'
& 'C:/Users/jerem/anaconda3/envs/listing-testing/python.exe' scripts/gallery_engine.py finalize --directory 'product generated photo/VL-1213' --asset 'product generated photo/VL-1213/production-v1/references/lenovo-logo-transparent.png' --brand Lenovo --contact '<outside-product-directory>/contact.png' --skip-normalization
```

Rendering resets review readiness and does not manufacture new review approval. Reinspect any changed bytes and bind fresh evidence before `accept`. The tested rebuild used the saved actual inputs and produced identical hashes for all three MAIN files and eight unbranded PT masters; an AI rerun is not a reproducibility claim. Arial/Arial Bold are system font dependencies.

Before repository acceptance, store `logo-qa.json.logoAssetPath` as the portable relative path `production-v1/references/lenovo-logo-transparent.png`. Windows finalization may emit backslashes; normalize this metadata path to forward slashes before `accept` so Linux CI reads the same original asset. The path-only correction does not change any image bytes; final QA must bind the corrected logo-QA record.

Publication/fulfillment follow-up remains separate: current Amazon account/category rules and Windows licensing/activation. Final GitHub verification is performed after push and applicable CI, against the delivered commit and current file hashes.
