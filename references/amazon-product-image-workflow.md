# Image production workflow

Pending review: [AI product reconstruction proposal — 2026-10-06](ai-product-reconstruction-proposal.md). The user has requested reference-guided AI product creation and a decision on conflicting old rules. This proposal does not activate a replacement; continue current production rules until the user decides.

1. Read [confirmed-catalog-defaults.md](confirmed-catalog-defaults.md), current product-fact record and [image-spec.md](image-spec.md). Identify exact base SKU, internal VL ID, verified assets and current statuses. Historical generated files are excluded from ordinary runs; consult only for an explicitly requested historical comparison.
2. Source accurate high-resolution exact-model front/angle/port/input views. OEM official → authorized exact-model retailer → seller photos. Record URL/date/dimensions/SHA-256/model-color match and commercial-use basis. Exhaust independent search before asking for missing views; never invent product geometry.
3. Classify audience from actual positioning/capabilities; select G/C/A→GG, B→BG or neutral profile. Optional Business Laptop B17/BG17 uses [business-graphite-design-system.md](business-graphite-design-system.md) and its approved appearance references; adapt hero, source views and task-specific screens from actual facts. Build fact ownership for PT01–PT08, using fixed slots in catalog policy. Existing selection defaults and per-product preview approval remain intact.
4. Create/reuse a valid style lock under [style-approval-gate.md](style-approval-gate.md). Legacy examples cannot grant a new product approval. Keep the palette/family consistent while task-specific screen content changes.
5. Build computer-only composition and clean masters with preserved authentic factory marks; no generated final logos/specifications. Reserve natural PT logo space and LCD zones. Gaming uses frozen actual layers/masks and six graphical cards; a flat reference does not constitute production pack.
6. Deterministically compose approved OEM/Windows assets and proofread base copy. Retain exact asset proportions, LCD clipping of effects and protected component spacing. Use portable `python scripts/gallery_engine.py --help`; PowerShell entry points may delegate to the same pipeline. Do not normalize unrelated files during targeted edits.
7. Run geometry/file/size/hash checks plus actual 100%/200px human review, semantic ownership review and current-hash evidence. Review includes all MAIN and PT, authentic marks, no extra devices/accessories, hardware accuracy, text, style and screen boundaries. Automated file checks cannot manufacture manual PASS.
8. Replace requested same slots after successful internal QA; refresh affected evidence. Follow [final-image-delivery-contract.md](final-image-delivery-contract.md): local QA → commit/push → CI → remote-hash verification → delivery. Keep untouched file bytes stable and preserve historical evidence distinctly.

## Portable pipeline and manual evidence

```bash
python scripts/gallery_engine.py --help
python scripts/gallery_engine.py finalize --directory 'product generated photo/VL-XXXX' --asset assets/branding/OEM-logo.png --brand OEM --contact /tmp/gallery-contact.png
python scripts/gallery_engine.py accept --directory 'product generated photo/VL-XXXX' --brand OEM
```

Use actual approved asset paths. `finalize` prepares composition and AWAITING_VISUAL_REVIEW evidence; it does not fabricate visual PASS. Between prepare and accept, genuinely inspect current files and write schema3 `visual-review.json` (all11 filenames) and `semantic-review.json` (PT01–PT08). Each has `schemaVersion:3`, `result:PASS`, actual `reviewer`, `reviewedAtUtc`, and `images` entries containing `file`, current `sha256`, `result:PASS`, and nonempty actual-inspection `notes`. Semantic records explain ownership/repetition; any numeric fact-overlap worksheet belongs in the manifest and is not asserted as an automatic script result. `accept` validates those current-hash records before writing final QA. Unsupported logo background/style exceptions remain blocked; obtain a valid transparent original rather than forcing a sticker.

For targeted work pass `--slots PT02.png` (actual requested filenames) to both `finalize` and `accept`, and keep unaffected files unchanged. For example, after genuinely inspecting the prepared PT02 output:

```bash
python scripts/gallery_engine.py accept --directory 'product generated photo/VL-XXXX' --brand OEM --slots PT02.png
```

The all11/all8 review sets above apply to full-gallery acceptance only. For partial acceptance, both schema3 review files contain `images` entries for exactly the selected filenames, with the same real reviewer/time, current hashes, PASS and actual-inspection notes. Additionally, `semantic-review.json.galleryInventorySha256` must map every one of the 11 gallery filenames to its current SHA256; selected-slot semantic notes must evaluate ownership/repetition against that retained gallery. This mapping binds retained bytes without approving their visual quality. Selected PT slots also require current logo evidence and placement records. A quarantined legacy gallery can receive a genuine selected-slot review and `partial-update-qa.json`: record `CURRENT_REQUESTED_SLOT_QA_PASS` / `PARTIAL_UPDATE` for the named scope while whole-gallery state stays REWORK_REQUIRED. Do not require recreating11 files to deliver an authorized local correction, and never label it FULL_GALLERY_QA_PASS. Preserve local original/master hash evidence; when those masters are not uploaded, remote verification explicitly reports recorded-only rather than falsely claiming they were remotely checked.

## Current recipe and desktop applicability

Use [production-recipes.md](production-recipes.md) for slot layouts, layer requirements and rebuild procedure. Read the current product style-lock.json first; preserve approved direction while rebuilding missing recipes, without inheriting old QA. Universal LCD/SCREEN_ONLY and lockup/package instructions above apply to integrated-screen computers. Standalone towers/SFF/mini PCs use the catalog policy's DESKTOP_GRAPHIC_SAFE_ZONE exception with package/package, accurate chassis layers and an approved versioned safe-zone recipe; no monitor, invented LCD or head breakout.

## Current Gaming reference — 2026-10-02

For Gaming enhanced MAIN, apply [gaming-approved-main-fit.md](gaming-approved-main-fit.md) before any older generic head-breakout, top-clearance or reference-exclusion instructions. SCREEN_ONLY six-card composition is now the integrated-screen default; HEAD_ONLY is an optional separately approved variation. The exact VL-1221 front supplied and approved by the user is a hash-bound 1237×937 import exception, not a full-gallery PASS or a reusable exception for other files. New generations follow the current Amazon-based size policy in image-spec.md and independently verified product facts.
