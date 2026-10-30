# Gaming enhanced MAIN — reusable production prompts

Method: `gaming-enhanced-main-artwork-brand-hierarchy-v1`.
Authority: [approved layout and reference](../references/gaming-enhanced-main-approved-layout.md).
Use this prompt with the actual selected image attached; prose alone is not a substitute for the reference. Replace every bracketed variable from current verified inputs. Never leave placeholders in the generation request or borrow reference-product values. Internal product IDs are metadata only, not prompt copy to render.

## Required inputs and roles

1. **PRODUCT_IDENTITY** — exact current product front photo, or independently sourced actual angle for an angle request. Keep chassis, finish, bezel, camera, hinges, keyboard, touchpad and factory marks.
2. **APPROVED_COMPOSITION** — the selected League of Legends preview, Drive file `1_y2z-KjhPN4lMGirjHjJtyXf5pRKc1iW`, SHA256 `d1ed16ffa9a9878bd09a46b435329a11e632f391112a38f486b573cf63b6ed9a`. Appearance only; its specifications are not source facts for another product.
3. **GAME_ART** — original covered artwork for [GAME_NAME]. Keep original character identity/style; crop/position this art rather than generating a named-game lookalike. Supply an original game mark separately if used.
4. **ORIGINAL_BRANDS** — applicable genuine CPU/GPU/Windows brand assets, with actual model/edition applicability. Original corporate identity plus accurate text is allowed when an exact verified tier badge is unavailable. A missing badge never authorizes inventing a tier or using a competitor's mark.
5. **VERIFIED_COPY** — [CPU_LABEL], [GPU_MODEL], [GPU_VARIANT], [VRAM_LABEL], [REFRESH_HZ], [DISPLAY_LABEL], [RAM_LABEL], [SSD_LABEL], [OS_LABEL]. Retain the full sold configuration in smaller supporting labels without six equal containers. Unknown relevant facts must be resolved or omitted honestly, not guessed from artwork.

## Master visual proposal prompt — send with the inputs

```text
Use case: compositing / product-mockup.
Deliver ONE complete enhanced MAIN visual proposal for [ACTUAL_PRODUCT_NAME].

INPUT ROLES
Image 1 is PRODUCT_IDENTITY: the actual machine only.
Image 2 is APPROVED_COMPOSITION: use its information hierarchy, clear game-character composition, brand placement and product prominence; do not inherit its product or specifications.
Image 3 is GAME_ART: original [GAME_NAME] artwork. Preserve the actual character identity and original art; use it as the screen insert, not merely a loose inspiration.
Remaining supplied images are genuine applicable CPU/GPU/Windows/game marks. Preserve their visible artwork, aspect ratio, colors and lettering; remove irrelevant asset padding only. Final production freezes original marks after the proposal.

PRODUCT AND CANVAS
Show the exact machine from Image 1, complete and large on pure white with a modest neutral contact shadow. Let source aspect ratio set the canvas and natural margins. Maximize useful product presence without clipping, stretching or changing its angle. Preserve actual body color/material, bezel width, hinges, camera, keyboard layout/backlight, touchpad and factory marks. Do not adopt the competitor/reference chassis, RGB keyboard, ports or accessories. No objects beyond the actual permitted product. No text or decoration on white background or chassis.

GAME COMPOSITION
Fill the actual LCD with Image 3's [GAME_NAME] artwork. Make the recognizable character, face, silhouette and action the main visual inside the screen. Choose a crop and placement that work with the informational anchors together. Keep the face and principal silhouette uncovered. Let scene depth and color remain visible; do not turn the artwork into a dark generic wallpaper beneath a grid. Nothing extends beyond the real LCD: no head, hair, hands, weapon, particle, glow, logo or text crosses its boundary. Keep physical bezel and factory marks intact.

PRIMARY INFORMATION — THREE ANCHORS
Upper right: compact genuine CPU identity with accurate readable [CPU_LABEL] beneath/adjacent. No fabricated CPU tier, AI/PRO/Evo/Ultra claim or badge.
Lower right: original GPU brand lockup and [GPU_MODEL] stacked as one strong coherent group. Model text is large and bold, using the applicable brand accent (NVIDIA green only when applicable). Below it, smaller [GPU_VARIANT] and [VRAM_LABEL]. Do not confuse graphics memory with system RAM.
Lower left: large bold italic [REFRESH_HZ]Hz, with smaller [DISPLAY_LABEL] directly beneath. Hz is display refresh, not FPS. Keep this figure distinct and visually balanced against the GPU group.

SECONDARY INFORMATION
Near lower middle, place [RAM_LABEL], [SSD_LABEL] and ONE compact genuine [OS_LABEL] identity with restrained recognizable memory/storage graphics if useful. They are subordinate to the three anchors, comfortably legible and separated from one another. No mandatory retail-package Windows graphic, no duplicate Windows identity. Keep original art visible behind them; no full-width black or semi-transparent specification strip.
An original [GAME_NAME] mark/name may occupy the upper left if it remains subordinate and leaves the character visible. Do not add an invented slogan or game-inclusion claim.

SPACING, MARKS AND TYPE
Use genuine proportional marks, crisp short labels and clean aligned baselines. Keep breathing room from bezel, neighboring labels and the protected face. Use local subtle text stroke/shadow only when needed for contrast. Reposition text or adjust the original-art crop before shrinking labels. CPU group remains compact; GPU model and Hz are the strongest numerical signals; RAM/SSD/OS remain smaller. Adapt the selected reference's relationships to this LCD and view; do not paste its pixel coordinates blindly.

AVOID
No six-box configuration grid, detached parameter cards, mandatory card skins, category-by-category rainbow colors, thick neon card outlines, broad black band, package-sized mandatory Windows block, copied competitor specifications, FPS/benchmark/inclusion claim, invented physical feature, external accessory or generic replacement machine.
No internal page header, page number, internal product ID, preview/version/QA status, watermark, tiny boilerplate footer or footer divider anywhere.

SUCCESS
At thumbnail size: recognizable exact computer, clear game character, strong GPU/Hz and coherent brand hierarchy. At normal viewing size: all actual labels readable and associated, original marks intact, no overlap or clipping. Preserve the approved image's visual impact while using only this product's actual facts.
```

## Refinement prompt — after a proposal is selected

```text
Edit the selected image only in [EXACT_AFFECTED_REGION] to correct [VERIFIED_FACT_OR_ASSET_CHANGE].
Use [GENUINE_ASSET_OR_NATIVE_PRODUCT_SOURCE] as the replacement source and [EXACT_CORRECT_TEXT] for the label.
Preserve product angle, scale, chassis/keys/bezel/factory marks, white exterior, character/art crop, face, light/material, three-anchor hierarchy and every unaffected label. Preserve original brand proportions and actual screen containment. Adjust the local region only; do not flatten the composition into cards or regenerate a different computer/character. No new header/footer/internal ID/status label. Compare against the exact selected bytes before accepting the correction.
```

## Filled example — accepted reference's composition only

Product: HP Victus front, original gray body/keyboard; League of Legends original Jinx art. Upper right: applicable AMD corporate identity plus `Ryzen 7445HS` (no unverified tier numeral). Lower right: original NVIDIA GeForce RTX lockup, large `RTX 4050`, smaller `Laptop GPU · 6GB GDDR6`. Lower left: large `144Hz`, smaller `15.6-inch FHD IPS`. Lower middle: `16GB DDR5`, `512GB NVMe SSD`, one `Windows 11 Pro` identity. Original game identity upper left; clear face/action centrally. These values describe this selected reference, not another machine's facts and not a new independent hardware verification.

## Fit guide and output review

The three anchor positions and relative emphasis are invariants; exact coordinates adapt. A starting guide inside normalized LCD bounds (not the canvas): CPU near upper-right 80–98% width, GPU near lower-right 72–98% width, Hz near lower-left 2–28% width, RAM/SSD/OS in the remaining lower middle. Leave enough distance from the bezel and protect actual face/silhouette. Move groups slightly if the new artwork requires it, preserving hierarchy rather than forcing collisions. An angle uses its own measured screen plane; standalone PCs use their own approved physical safe zone without invented LCD/Hz.

Before sending: resolve variables, verify facts and input roles, check customer copy. After rendering: compare native/400px/200px actual image against selected reference. Check actual hardware, original art and marks, numerical copy, hierarchy, screen containment, no internal labels/footer and no card regression. Save selected bytes, final prompt/inputs and hashes. Preview selection does not alone certify exact physical geometry, final original logos, editable production layers or marketplace acceptance. Production refinement must preserve the selected effect while completing those actual checks.
