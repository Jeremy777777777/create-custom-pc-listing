# Per-image review dependencies

For new reviews backed by a scoped research ledger, use `schemaVersion: 4` in both visual-review.json and semantic-review.json. Keep the existing reviewer, UTC review time, result, complete current gallery inventory and per-image byte hash/result/notes requirements. Each image entry additionally contains:

```json
{
  "file": "PT08.png",
  "dependencies": {
    "fields": [["Product Details", "Number of USB 3.0 Ports"]],
    "productPaths": ["/ports"],
    "basis": "Actual inspection: the depicted ports and every caption use these reviewed records."
  },
  "reviewInputsSha256": "computed at actual review time"
}
```

This is an illustrative declaration, not approval or a universal PT08 template. Use only existing selected ledger fields and explicit JSON pointers into the actual product-facts.json. List every fact, physical feature, accessory, badge and claim used by the image, including their relevant dependencies. A pure product photograph can declare its actual chassis/appearance/source references without unrelated specification claims. At least one field or product path and a substantive coverage basis are required. Missing or unknown dependency coverage requires actual inspection before acceptance; never declare an irrelevant field to obtain a valid hash. The script cannot infer complete dependency coverage from pixels.

Compute `image_review_scope.binding(directory, filename, dependencies)` and record its result inside that image entry when reviewing current bytes. Matching visual/semantic entries must use identical declarations and bindings. Common identity/configuration, identity ledger fields, full approved style lock, referenced recipe and applicable policy are included automatically. Selected value units and explicit storage component evidence are included when applicable. The complete scoped ledger and supplied hardware caches must still be internally consistent. Arbitrary research notes and unrelated hardware values are excluded from the per-image digest.

Example: changing RAM maximum does not invalidate an interface-only PT08 whose declared inputs are unchanged. Changing its USB count, chassis identity, style or pixels does. Review affected slots and use the existing partial-update receipt; do not claim whole-gallery PASS when other slots are stale. A factual amendment does not revoke the user's approved style direction; a style-lock change still requires review under that changed style.

Version 3 remains supported with its original global binding. Existing reports retain their status; migration to version 4 requires real dependency inspection and current review, never automatic PASS conversion. Logo QA schema is unchanged. Historical-policy preservation remains limited to unchanged trusted-base bytes, produces historical status only and never grants current approval. Style approval remains exclusively the user's decision.
