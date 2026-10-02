# Final image delivery contract

Apply [confirmed-catalog-defaults.md](confirmed-catalog-defaults.md) and [image-spec.md](image-spec.md). Final delivery means completed individual images with all required copy and deterministic assets, not a contact sheet, concept, ZIP alone or plan to add logos later.

## Production and adjustment

New style follows [style-approval-gate.md](style-approval-gate.md). Existing same-product/same-style local corrections retain approval. A request to modify a named slot authorizes its canonical replacement after internal QA; no redundant upload approval. Do not touch unrelated slots; retain their bytes/hashes. Material style changes need direction approval before production.

Block affected outputs before production if exact model/source rights, angle assets, required verified specs or fixed Windows/OEM identity assets are missing. State specific missing evidence. Never generate hardware to fill the gap. No accessory/packout prerequisite is imposed on computer-only imagery.

## Required evidence

- 11 individual files in current standard at `product generated photo/VL-XXXX/`; shared with the product's Research/Listing workbooks.
- Current image manifest, source/asset records and style lock; deterministic overlay placement including masks/protected zones.
- Schema 3 logo QA with original asset/master/final hashes and actual visible-alpha dimensions/spacing.
- Semantic fact ownership and justified numeric metric or manual review (no fabricated percent).
- Genuine current-hash manual 100%/200px visual, style, product geometry, authentic marks, LCD/HEAD_ONLY boundaries, text and no-peripheral review.
- Final report checks MAIN as well as PT, all sizes/hashes and required reviews. Automatic checks do not imply artistic, license or Amazon acceptance.

If a legacy gallery fails current size/hash/visual review, keep its prior record historical and mark current state REWORK_REQUIRED. Do not mechanically create PASS for modified files or upscale low-resolution old work solely to reach 2000.

## 7. GitHub final delivery

Generation and requested revisions authorize upload unless user requests local-only/concept. Sequence:

1. Finish affected files and local checks; perform actual hash-bound manual reviews.
2. Commit/push the files and current evidence. Remote CI requires this push and cannot be a pre-push gate.
3. Await applicable CI, verify remote commit and every delivered file hash; record `GITHUB_DELIVERY_VERIFIED` with product directory/commit links.
4. Report completed scope and real limitations. An upload failure is not successful delivery. A partial adjustment may be delivered as `CURRENT_REQUESTED_SLOT_QA_PASS` / `PARTIAL_UPDATE` with `partial-update-qa.json` for named slots. A quarantined legacy folder remains whole-gallery REWORK_REQUIRED; no forced rerender of unrelated slots and no full-gallery PASS.

A previous delivery record certifies its recorded commit only. After editing, create evidence for the new commit rather than using the old record. Publication eligibility for MAIN-STRICT/enhanced candidates remains independent.
