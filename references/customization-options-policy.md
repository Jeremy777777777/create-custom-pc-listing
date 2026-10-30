# Customization in title, bullets and description — user decision 2026-10-29

This current explicit seller decision replaces the former base-only restriction for **CUSTOMIZED_OEM listing copy**. It applies to Item Name, Bullet Point and Product Description. The seller confirmed that the following are its available choices; do not ask again or research platform maximum capacity to reduce these lists. The separate MEGAPC_OWN_BRAND route and image recipes retain their existing scope.

## Required customer copy

- SSD: `512GB / 1TB / 2TB / 4TB SSD Options` in all three copy fields.
- Replaceable RAM: `8GB / 16GB / 32GB / 64GB [verified type] RAM Options` in all three fields, e.g. `8GB / 16GB / 32GB / 64GB DDR5 RAM Options`.
- Fixed RAM: actual capacity and exact researched memory family/generation, e.g. `16GB LPDDR5 RAM (Fixed)` or `32GB LPDDR5X RAM (Fixed)`, in all three fields. Do not offer RAM choices for fixed memory. Never turn DDR5 into LPDDR5 merely because it is soldered.
- Explain customization in a capacity bullet and a Description section: selectable RAM/SSD for replaceable memory; fixed memory plus selectable SSD otherwise. Keep five bullet paragraphs, the exact unchanged warranty first, literal Description HTML, Warranty and Disclosure last, OEM identity and Win 11 Pro. Title stays at most 200 characters; drop secondary features before dropping these options or RAM generation.
- Each choice is an alternative configuration, not several drives/modules simultaneously installed. Do not call the options a measured maximum or imply all options are included. Numeric installed-capacity workbook attributes and selectedBaseConfiguration remain the real base configuration; never insert slash lists into numeric fields or overwrite those facts with the largest option. Other factual/research and publication checks remain separate.

## Research before composing

Use the normal official serial/parts/model evidence chain to determine **actual RAM replaceability** and **exact memory family/generation**, preserving DDR4 vs DDR5 and LPDDR4X vs LPDDR5 vs LPDDR5X, etc. Do not infer replaceability solely from a DDR/LPDDR name. Mixed onboard/socket designs require a product-specific whole-memory determination; do not silently advertise replacement of fixed modules. Keep unknown/conflicting hardware research unresolved rather than selecting a branch by guess.

The standard SSD/RAM capacity choices above are SELLER_POLICY, already confirmed in this conversation. They do not need model maximum-capacity research, candidate ranking or per-tier compatibility approval. A published 32GB platform maximum does **not** remove the seller's 64GB RAM option. Preserve any existing maximum field as its own scoped research fact; do not change it to 64GB or use the advertised option as proof of a hardware maximum. Other unrelated technical fields retain their normal research requirements.

Store the result in the existing selected `RAM Memory Installed` fact under `evidence.customization_ram`, without adding workbook columns or a second ledger:

```json
{
  "status": "VERIFIED",
  "replaceable": true,
  "memoryType": "DDR5",
  "replaceabilitySource": "Actual inspected exact-product service manual URL and section",
  "memoryTypeSource": "Actual inspected matching parts/specification URL and section",
  "reviewedDate": "2026-10-29"
}
```

This is an illustrative shape, not evidence for a product. Preserve actual searches, official part references, scope and review dates alongside the existing research_trace. For unresolved research use an honest status/reason/next_action; do not invent the boolean/type or a VERIFIED result. For fixed memory, verify the actual sold capacity as well. Keep detailed type evidence here even if an Amazon closed selection lacks that precise type; reference-only approximations cannot redefine the real type.

## Executable route and compatibility

`scripts/customization_policy.py` reads this selected evidence, creates deterministic title/bullet/HTML customization fragments, and checks all three saved copy fields. `product_metadata.listing_view` derives its customization view from the selected ledger; an unbound or stale metadata cache is rejected. `research_export.py --write-workbook --stage LISTING_DRAFT` requires completed RAM branch research for customized products before writing. Missing research can still be handed off as an honest PARTIAL RESEARCH_REVIEW. New annotated drafts are checked even without export mode. Do not remove the annotation or use lower-level workbook APIs to evade the new-generation contract.

Use `customization_policy.copy_texts(listing_view(product, ledger)[0])` to compose the original English copy around the researched fragments. Copy facts remain derived from the same ledger. The existing full content validator masks only exact labelled standard option phrases, then continues installed-capacity, storage medium, CPU, VRAM and numeric checks on the remaining claims. Arbitrary unsupported lists or incorrect DDR/LPDDR versions fail.

Read-only legacy workbooks without this annotation remain explicitly historical/base-only; they do not gain current-policy compliance. Do not rewrite existing product deliveries or image galleries during this workflow maintenance. Apply the new policy when generating or explicitly revising customized listing copy. Own-brand products retain their independent copy and sold-capacity rules.

Run the complete repository unit suite plus `scripts/tests/test_customization_policy.py`. The regression fixtures are explicitly synthetic, never claims that a real product was researched. They cover DDR4/DDR5 replacement, LPDDR4X/LPDDR5/LPDDR5X fixed memory, unknown/conflicting evidence, wrong types/lists, seller choices despite a smaller documented maximum, saved workbook generation/readback, legacy compatibility and the separate own-brand route.
