# Universal RAM / SSD choice page — user decision 2026-10-29

The user explicitly extended the confirmed customization scheme from listing copy into universal image design, requesting one page to explain every capacity option and its purpose. For **new full CUSTOMIZED_OEM galleries across all design series/form factors**, PT05 is the default dedicated choice page. This supersedes older PT05 installed-only, generic-task and no-option prescriptions, including Business, Gaming and Mini PC recipes. Keep eleven image files: use the existing PT05, not a twelfth slot. PT03 remains the sole complete installed CPU/GPU/base RAM/base SSD/OS overview; MAIN and other slots keep their current boundaries. The own-brand route is not silently changed by this customization decision.

## Content and factual scope

Use [the same seller options and researched RAM branch](customization-options-policy.md). Research actual replaceability and exact DDR/LPDDR family/generation once in the existing ledger; reuse it in copy and images. Do not infer replaceability from the name, reduce the standard choices by platform maximum, or relabel choices as installed capacity/hardware maximum. Unresolved replaceability/type needs research before this page, not guessed upgrade rows.

For replaceable RAM show the researched type plus all four RAM options and all four SSD options. For fixed RAM show its actual capacity/type, clearly mark it fixed, omit RAM choices and show all four SSD options. Do not suggest LPDDR can be replaced. Retain the authentic keyboard/chassis/ports and the actual selected style.

| Group | Choice | Short illustrative use caption |
| --- | --- | --- |
| Replaceable RAM | 8GB | Everyday browsing and documents |
| Replaceable RAM | 16GB | Daily multitasking and study |
| Replaceable RAM | 32GB | Larger spreadsheets and creative projects |
| Replaceable RAM | 64GB | Memory-intensive projects and workflows |
| SSD | 512GB | Everyday apps and essential files |
| SSD | 1TB | More room for projects and games |
| SSD | 2TB | Larger photo, video and game libraries |
| SSD | 4TB | Extensive project and media collections |

These explain typical capacity use, not measured performance or a promise that every product runs every workload. Do not add FPS/speed boosts, percentages, guaranteed app compatibility, exact file/game counts or unsupported DDR frequency. Larger SSD capacity is more storage room, not automatically a faster drive; greater RAM capacity is working space, not a universal processor/GPU improvement. Keep captions short and choose product-appropriate original examples without inventing benchmarks or software inclusion.

Customer-facing copy is English. Default headline: **Choose Your Memory and Storage**. Show the choices explicitly as **Options**. Selection note for replaceable RAM: “Choose one RAM and one SSD option; only your selected configuration is supplied.” For fixed RAM: “RAM is fixed. Choose one SSD option; only your selected configuration is supplied.” Add “Use examples are illustrative; results depend on the workload and other hardware.” with readable hierarchy. No implied simultaneous multi-drive or multi-module bundle.

## Composition

Use two clearly distinguished RAM / SSD groups with large capacity labels and a short caption per tier. Product presence follows the selected series and the explanatory purpose; it is optional. Business Laptop PT05 is product-free: use distinct capacity/use illustrations and a compact fixed-memory note. Fixed RAM uses a compact locked-memory summary plus four SSD choices. Layout, palette and imagery adapt to the approved Business/Gaming/Mini PC series; a common content contract does not impose one visual style on every product. Keep the page focused on selection, not another CPU/GPU/OS specification poster.

Do not invent DIMM slots, user-accessible memory, component internals, fitted drive brands or motherboard geometry. Original component pictures need actual applicability; a generic explanatory illustration must be identified as such. Do not make another full specification table, repeat every PT03 fact or repeat the option matrix across the whole gallery. The selected installed RAM/SSD may recur as qualified base context with a recorded secondary purpose.

Render final capacities, type, captions and qualifiers as deterministic layers. Inspect final bytes at native resolution, approximately 400px mobile width and 200px thumbnail. At 400px the capacities and tier captions must be legible; at 200px the topic/product and option hierarchy must be apparent. Reflow groups or shorten weak text before shrinking it. Preserve existing image dimensions, product fidelity, original brand assets and MAIN rules.

## Planning, review and delivery

Build a supporting `customization-image-plan.json` from actual current product/ledger files:

```text
python scripts/image_customization_plan.py build --product-facts <product-facts.json> --ledger <research-ledger.json> --plan <new-customization-image-plan.json>
python scripts/image_customization_plan.py check --product-facts <product-facts.json> --ledger <research-ledger.json> --plan <customization-image-plan.json>
```

The helper binds exact input bytes, product/configuration, researched RAM type/replaceability and fixed capacity. It keeps seller-policy option claims separate from installed hardware facts and provides reusable English tier captions. It neither creates an image nor supplies style approval, truth authentication or visual QA. Record the plan path/hash in the series information plan and production recipe; apply the existing source/claim/QA and Drive gates. Store it as supporting SOURCE with the product's production dependencies, not as a canonical image slot or new workbook column. Do not fabricate installed fact IDs for seller option capacities; hardware claims retain real fact IDs and option claims cite the seller policy separately.

For new complete customized series, include the choice page in the product-specific proposal and subsequent approved production. Existing galleries are not bulk-replaced by a policy update. An unrelated single-slot correction preserves PT05; when PT05 or full-gallery redesign is requested, apply this method within the authorized scope and actual style approval. Keep current approval/partial-update rules and QA limitations; the business rule is not approval of a new per-product appearance.

GitHub is updated and validated first. Only then synchronize the exact committed workflow files to the established Drive source paths, preserve prior versions and verify original downloaded bytes. Product image delivery follows its separate Drive path.
