# Gaming PT visual explanation — user-approved VL-1221 direction

## Scope and precedence

The user selected the generated VL-1221 PT03, then explicitly accepted PT01, PT05 and PT07. The initial delivery replaced PT01/PT05/PT07. On 2026-10-30 the user additionally approved the redesigned PT03, requested its cleaned replacement, and applied [customer-facing content](customer-facing-image-content.md) across all images and future copy. Preserve original selection evidence in [the registry](../assets/gaming-visual-reference-registry.json), but do not copy its superseded headers/footers.

Apply this reference before older G22 PT composition rules. Keep G22/A22/GG22 identifiers for compatibility and use `methodProfile: gaming-visual-explanation-v2`. This changes Gaming PT01–PT08; it does not migrate Mini PC/Business recipes, alter any MAIN rule, approve other products or turn style acceptance into factual/marketplace QA. G01–G21/GG01–GG21 remain explicit opt-in alternatives, never automatic fallbacks for this direction.

## Core standard

Every page follows [customer-facing content](customer-facing-image-content.md): no internal page eyebrow, fixed footer/divider, internal product ID or preview/version label. Keep meaningful main headlines, verified component labels and readable necessary qualifications beside the feature. Production status belongs outside the artwork.

**Turn the page's selling point into a visual explanation. Choose the subject and explanatory image before arranging text. Use pictures and words together to explain the feature, component, relationship or use.**

Treat the accurate computer as a product anchor, not an obligatory largest object. Component illustrations, task windows, optical details, controls and use scenes may lead according to the page. Keep a clear focal hierarchy, dimension, material, perspective and lighting. Place factual labels next to their corresponding visuals. Do not satisfy a hardware topic with a generic laptop view and detached parameter cards.

Use the selected references' graphite/deep-burgundy environment, metallic materials, dimensional technical imagery, local crimson light/circuit accents and readable white headings. Match their depth and visual explanation, not identical coordinates or a circuit board on every page. Keep secondary copy calm; expressive artwork may occupy the rest of the canvas. Cards remain optional aids, never the default solution. A light detail background is optional, not mandatory.

## Page-specific standards

| Page | Visual subject and explanation | Text and factual boundaries | Reject |
| --- | --- | --- | --- |
| PT01 — buying reason | For VL-1221, combine a mobile GPU illustration, dedicated-memory representation, actual laptop and original gaming scene. Give hardware and its use linked focal roles. Other products choose their strongest verified reason. | Name the actual GPU/graphics-memory capacity beside the corresponding visuals. Distinguish graphics memory from system RAM. | Laptop plus two large text cards; desktop GPU board standing in for a laptop GPU; implied measured game results. |
| PT02 — gaming worlds | Compose named original game art/logos with varied scale, depth and one dominant visual or a coherent portfolio. Use an actual product anchor only where it strengthens composition. | Keep identities/readable names; retain covered source/authorization scope. Game depiction alone is genre context, not FPS, inclusion or playability proof. | Mandatory equal six-tile grid; tiny cover collage; AI imitation of named game artwork. |
| PT03 — supplied configuration | Let dimensional CPU/GPU technical illustrations lead. Use recognizable RAM/SSD component illustrations and a smaller actual-product anchor. Present the full configuration through related imagery. | Include actual CPU, GPU, installed RAM, internal SSD and OS. Put each specification next to its subject; useful CPU metrics may support the main illustration. | Flat chip outline as the complete technical visual; five large configuration text cards; inherited reference specifications. |
| PT04 — display/form | Use actual display/form views, meaningful screen content, detail enlargements and supported view/refresh/size illustrations. Let the image explain the chosen feature. | Match actual resolution, refresh rate, finish and brightness where verified; physical dimensions use inches. Depict refresh sequences only as explanatory illustrations, not captured comparative tests. | Front laptop photo plus a column of unrelated numbers; invented screen quality or comparison. |
| PT05 — RAM/SSD choices | Combine dimensional memory/storage illustrations with layered original task windows and organized files/media. Arrange capacity choices and short uses around the explanation. Product scale follows the topic. | Apply universal choice content and researched fixed/replaceable RAM branch. Label choices as options; distinguish base configuration. More capacity is working/storage room, not a benchmark. | Rear laptop photo as a substitute for explaining memory/storage; a second full CPU/GPU/OS table; capacity speed bars. |
| PT06 — controls/input | Lead with faithful keyboard/touchpad/control closeups and selective operation context. Show evidenced backlighting visibly when it is the selling point. | Match actual keys, layout, controls and supported functions. Use actual detail photos or reference-bound faithful reproduction. | Mandatory white background; word-only backlight claim; invented key/dial/gesture capability. |
| PT07 — remaining feature | VL-1221 uses clearly conceptual optics and dual microphones with a video-call scene. Other products may use cooling/access/maintenance only when applicable. | Link labels to the right visual. Camera temporal image-noise reduction is not microphone noise cancellation. Separate technical concept from actual internal structure. | Generic gaming screen beside camera text; fake exploded actual hardware; unsupported privacy shutter, fan arrangement or cooling measurements. |
| PT08 — connections | Keep true opposing port views as the foundation. Use short accurate leaders, clear grouping and concise use explanations; contextual technical art stays secondary. | Verify each opening, count, side and function. Use original physical views; never replace a port map with a device-network diagram. | Generic connector icons instead of real ports; obstructed openings; invented USB-C functions. |

PT01, PT03, PT05 and PT07 have user-selected examples. PT02/PT04/PT06/PT08 are proposed continuations of the principle, not already approved rendered pictures. New-product previews remain product-specific.

## Generate, refine and preserve

1. Read actual product facts, selected slots, latest approval and reference registry. Retrieve the original selected images by their stable Drive IDs and verify SHA256. Do not rely on a signed URL, filename, chat memory or a descriptive style name alone.
2. For every selected page, write its buyer question, visual subject, explanatory relationship, composition, label-to-visual mapping, exact copy, actual-product source, generation/reference inputs, and what it must avoid. Use the `visualExplanation` block in the Gaming information plan. Apply the template gamingOverrides and set designSeries GAMING, family G22 and methodProfile gaming-visual-explanation-v2. Run `python scripts/gaming_visual_plan.py --plan <plan.json> --repo <checkout>` before new generation. This checks actual selected-page plan/reference completeness, not aesthetics or image QA. If the plan is just a laptop plus facts, redesign before generation.
3. Supply the closest approved image as a **style/composition reference**, current actual hardware as a **product-identity reference**, and current facts as the **only source of specifications**. Explicitly separate these roles in the prompt. Use the image-generation tool for requested generated visuals.
4. Allow generated full-page proposals, technical backgrounds, dimensional component concepts, abstract original task interfaces and anonymous synthetic use scenes. Whole-page proposals are a valid route to the desired composition. Preserve the selected result as approval evidence before refinements.
5. For new production, isolate/freeze accurate hardware, generated scene/component artwork, final text and genuine brand assets. Refine only inaccurate details/labels/logos using local image edits or compositing; preserve selected framing, product angle/scale, lighting, depth, feature imagery and information hierarchy. Never turn a selected rich image into flat boxes merely to make text/logo placement easier. Record any necessary material visual change and obtain judgment only when it changes the approved direction.
6. Preserve original manufacturer marks. Use genuine original assets for final added marks. For new selected Gaming PT pages, integrate one original subordinate OEM identity in a meaningful brand area, product-identity line or feature header. Plan its purpose, original asset/hash and protected visual/text regions under [the current OEM integration policy](current-workflow.md). Placement is not forced into an external corner; preserve actual manufacturer marks. Hardware brand/factual correctness remains mandatory.
7. For actual named games use covered original art/logos and readable names. For a generic gaming, task or call concept, original generated artwork is allowed without presenting it as a named game/software or an included entitlement. Layered task windows may extend beyond the LCD on **PT images** as explanatory artwork; MAIN containment remains separate and unchanged.
8. Component, optical, circuit and task visuals must be recognizable as concepts, not claimed photos of the actual motherboard, fitted component brand, real optical assembly or actual test captures. Label where needed. Do not invent FPS, comparisons, noise-cancellation or performance improvements. Distinguish source fact, illustration and measured result.

## Acceptance and exact-byte adoption

Inspect native resolution, about 400px width and 200px thumbnail. Record substantive findings, not an automatic PASS:

- Is the page topic apparent before reading small text?
- Does its main picture explain a feature, relationship or use, rather than merely decorate the page?
- Can the reader associate each major claim with its component/detail/scene?
- Does it match the selected reference's depth, hierarchy and material quality while serving this page's different purpose?
- Are copy, actual hardware, marks and illustrative boundaries accurate and readable?
- Has it fallen back to repeated generic laptop views and large parameter cards?

Compare the corrected image against the exact selected image; record differences. Factual/technical corrections do not authorize aesthetic regression. Automated structure/storage checks cannot decide these visual questions.

When the user selects an existing image, freeze its appearance/source hash. The current OEM integration decision authorizes a carefully placed genuine OEM mark while preserving the selected scene, subject, depth and hierarchy. Where all facts and genuine marks are already correct, retain the exact approved bytes. Record the selected and final hashes plus any specific correction. Apply normal scoped actual-image QA and byte-verified delivery; incomplete source or production review remains explicitly incomplete rather than receiving fabricated PASS. Earlier exact-byte adoption records retain their own historical scope; they are not a substitute for this current integrated-brand production path.

## Retired defaults and unchanged boundaries

Replace old Gaming PT instructions requiring a dominant full laptop on every page, quiet card-based layouts, uniform module materials, PT03 ordered text modules, PT05 alternate rear view, white PT06, rigid external-corner OEM badges, or original-media-only creativity. Those are no longer defaults. Existing explanatory data, appropriate original game sources, universal PT05 options, exact facts, real interfaces, MAIN limits, mobile review, scoped approvals and verified Drive delivery remain. Older approvals and history stay as records, not competing current appearance constraints.

Read the current entry points and this page on each new Gaming PT run. Read the slot standard and supply the actual selected reference image before generation. Keep references as immutable individual images in the established Drive source tree; GitHub carries the rules, reusable plan and reference metadata, not product-output binaries.
