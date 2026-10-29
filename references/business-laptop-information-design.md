# Business Laptop information design — user decision 2026-10-29

Read [universal image production](universal-image-production.md) first. That shared layer owns the production mechanics and reusable assets; this document owns Business Laptop content architecture. The user's subsequent approval of the six VL-1223/VL-1271 previews authorizes their scoped current-slot replacement, with the actual approval and image hashes recorded in product evidence. It does not approve other products automatically.

Apply to Business Laptop planning, generation and revision, across B/BG families. The user reviewed Amazon ASIN [B01N4C1TH4](https://www.amazon.com/dp/B01N4C1TH4) and requested fuller, more useful information design after comparing VL-1223 and VL-1271. The page observed on 2026-10-29 showed ThinkPad L16, despite the supplied URL slug mentioning E16. It is an organization reference, never hardware evidence for our products.

This decision supersedes older Business Laptop instructions that prescribe only 2–3 callouts, rigid single-fact pages, a mandatory generic three-step PT05, or numerical rejection solely because a useful secondary fact recurs. Preserve factual verification, one complete configuration page, base sold capacities, actual product fidelity, Windows placement, style approval and Drive delivery. Other design series retain their existing rules.

## Plan content before rendering

Read the current product facts, research ledger, delivery state and style lock. Create a product-specific `business-information-plan.json` outside canonical image slots. Record product/configuration IDs, source workflow commit, ledger SHA256, design family, preview/approval state, and each planned slot's:

- Buyer question, specific headline and primary theme.
- Evidence-backed claims with canonical fact IDs, scope, source and final English copy. Include source qualifiers such as Typical, fixed/on-package memory, nominal capacity and maximum clock where applicable.
- Visual proof: exact whole-product angle, native detail crop, port map, coherent scene or explanatory diagram; keep the source path/hash.
- Reading order: headline, product/detail, principal values, concise use explanation. Each module adds a reason to understand or choose the machine.
- Exact registry asset IDs and the facts that make each brand/edition applicable.
- Secondary fact reuse and its purpose; explain why it aids the new theme instead of repeating a page.

Do not let an empty required field become a generic slogan. Source the missing useful detail, reallocate related facts, or explain the actual limitation. Do not add unsupported claims to fill a layout.

## Reading hierarchy and visual density

Use a compact buyer-benefit headline, prominent accurate hardware and grouped proof. Technical pages commonly support 3–6 meaningful proof units, with a number/type, a short use explanation, and a matching detail or icon where useful. This is a planning target, not a quota or a reason to shrink text. A large title and repeated full laptop with one isolated number is usually insufficient.

Vary compositions: product plus grouped modules, front display, keyboard/camera detail, true side views and one purposeful office scene. Reuse palette, typography, line weights and brand treatment rather than one title/product/footer grid. Keep working documents coherent and unbranded unless applicable software identity is confirmed. Avoid meaningless charts or decorative performance bars.

Inspect the actual image at full resolution, approximately 400px mobile width and 200px thumbnail. At 200px the topic and product should be evident; at 400px principal values and module labels should read. Subordinate detail can require zoom. Reflow or remove weak content before reducing text below readable size. Do not claim measured density/coverage percentages without actually measuring and explaining their meaning.

## Supporting gallery architecture

The eleven-file delivery contract remains: three MAIN alternatives and PT01–PT08. Preserve untouched MAIN bytes during a supporting-image revision.

| Slot | Buyer question and useful content |
| --- | --- |
| PT01 | Why consider this computer? One strong purchase theme with a few compatible verified proof points. No full configuration table or Windows overlay. |
| PT02 | How does it fit my work? One credible use scene, coherent screen task and a few useful contextual annotations. Avoid a second generic office image with the same message. |
| PT03 | What performance/configuration am I buying? The sole complete installed CPU/GPU/RAM/internal SSD/OS overview, concise benefit explanations, correct processor brand asset and one fixed OS asset. No unsupported benchmark or capacity choices. |
| PT04 | What is the screen experience? Group exact size, native resolution, panel, ratio, touch, refresh, brightness/gamut and surface only as verified for the sold panel. Keep paired units/gamut names correct and qualifiers visible. |
| PT05 | What do memory and storage mean for my work? Explain the installed capacities and applicable fixed/upgrade limits, with original work examples. Secondary reuse of PT03 RAM/SSD is allowed because this page adds explanation. An evidenced convertible/form relationship may instead own this page. Do not default to Plan/Review/Deliver filler. |
| PT06 | What will I use every day? White-background keyboard/touchpad/control details with close labels and concise uses. Related verified camera/privacy/input features can be grouped when the evidence supports the theme. Never invent backlighting or keys. |
| PT07 | What other important buyer question remains? A coherent mobility/battery or collaboration/privacy theme with related evidence; combine thin facts rather than giving a single battery number a whole page. No invented runtime, security certification or seller warranty advertising. |
| PT08 | What can I connect? Actual left/right connector map with clear endpoint labels, supported functions/speeds and verified wireless footer. Do not substitute detached port icons for the real machine. |

Fact ownership means a primary explanation has a home. A concise overview and a later deeper explanation may share a fact. Review the complete claims: recycled headline/page narrative is weak even with different fact IDs; useful explanatory reuse is acceptable without manufacturing a low overlap score. Preserve one full configuration overview and document every secondary recurrence.

## Reference lessons and boundaries

The reference's overview combines processor explanation with a compact parameter strip; screen details form a coherent cluster; input claims point to actual locations; storage/memory pages explain choices. Adopt these relationships with original layouts/copy and our own verified hardware. Do not copy its artwork, CPU comparison bars, optional capacities, certification claims or implied app bundle. Its pure scene page shows that density may vary across a gallery.

For VL-1223, retain the approved pale-gray/navy B05 family. Fixed 32GB LPDDR5X and 1TB internal SSD remain the configuration; LPDDR5X speed conflict stays omitted. For VL-1271, retain graphite/navy B17; base 16GB/512GB, actual US non-backlit keyboard, camera shutter and genuine ports remain model-specific. These are examples, not transferable catalog facts.

## Production and acceptance

Use [reusable brand assets](reusable-brand-assets.md) before image generation. Create original scenes or redesign previews with the image tool; final product layers must pass actual model fidelity, and final text/logos use deterministic original assets. Keep preview status visible outside the customer artwork. Store prompts and layer/asset/claim bindings with the production recipe.

A change to layout family or purchase narrative requires actual-product previews and explicit USER approval under [style-approval-gate.md](style-approval-gate.md), even when the palette is retained. Continue workflow and asset work while approval is pending. Preview files are not canonical finals or a full-gallery PASS.

Check the declared plan before rendering: `python scripts/business_information_plan.py --plan <business-information-plan.json> --ledger <research-ledger.json> --repo .`. The plan binds the current ledger hash, all eight PT slots, claim fact IDs, PRIMARY/SECONDARY roles with reuse reasons, source/detail description and compatible registry IDs. Use the checker module's field names when creating the plan; no separate workbook columns are added. This check supplements actual copy review and existing production/gallery checks; it never grants style or image acceptance.

Before acceptance, review factual applicability, text accuracy, meaningful per-page contribution, detail fidelity, mobile reading, original-logo integrity and complete dependencies. A plan validator checks declarations only; it cannot establish visual quality or truth of free-text claims. Keep current image QA and Drive checks separate.
