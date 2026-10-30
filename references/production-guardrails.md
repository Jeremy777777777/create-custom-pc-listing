# Executable production scope — 2026-10-27

For each new product production/revision stage, use `scripts/production_guard.py` before edits and before delivery. It combines actual file-difference checks with existing research/export/gallery validators. It never supplies factual, visual, rights, USER style or marketplace approval.

## Freeze the actual request once

Use a clean committed workflow. Observe existing current Drive bytes and archive requirements first. Stage only the exact product/dependencies; temporary previews, debug logs and run records stay outside its directory. The request JSON contains:

- `runId`, `configurationId`, `requestReference`: actual request and verified target; directory name supplies productId.
- `mode`: FULL_LISTING_WORKFLOW, IMAGE_ONLY_WORKFLOW, IMAGE_ADJUSTMENT_WORKFLOW or explicitly requested CONCEPT_ONLY.
- `allowedChanges`: exact product-relative filenames permitted to be created/modified, including necessary facts, research, recipe and QA sidecars. No wildcard, parent path, alias or deletion. Routine necessary sidecars do not need another approval. Never add unrelated slots or Excel to evade checks.
- `outputs`: exact delivery filenames mapped to RESEARCH, LISTING, IMAGE, QA, SOURCE or CONCEPT. Workbooks must be original top-level XLSX; canonical images cannot be relabelled SOURCE. Image modes cannot regenerate Excel.

Canonical `research-ledger.json` and `product-facts.json` dependencies use RESEARCH, matching their existing `03_RESEARCH/FINAL` destination. A workbook's exact `.research-summary.json` sidecar shares its RESEARCH or LISTING role and folder. Outside the explicit imageFactUpdate branch below, these JSON dependencies require a contracted workbook and never bypass its checks; arbitrary JSON cannot claim a workbook role. Workbook content checks execute on XLSX bytes, while ledger/metadata/summary bindings are checked with the workbook.
- `selectedSlots`: exact requested canonical images, empty for research-only stages. IMAGE_ONLY_WORKFLOW requires all eleven; IMAGE_ADJUSTMENT_WORKFLOW requires the requested subset.
- With image slots, `styleApproval` contains `userReference` to actual USER approval and raw-byte `styleLockSha256` of the approved style-lock.json. A model opinion or test result cannot supply approval.

Run using the dedicated Listing interpreter:

```text
scripts/production_guard.py capture --product <product-cache> --request <request.json> --output <run-directory/production-contract.json>
```

Capture records staged baseline bytes, workflow commit and time. For a newly selected style, retain the observed prior Drive baseline separately, prepare the actual USER-approved shared/per-slot style as a declared stage input, then capture before changing image bytes. Do not present that staged style as the old remote state. A gallery-baseline.json used for remote-only image inventory is immutable within the captured run; changed remote evidence uses a successor observation/run. Retain the exact contract and returned SHA256 independently in the existing run record before edits. This implements existing authorization; it is not another user approval. Missing old receipts use observed-baseline adoption, never invented hashes or a post-edit capture presented as pre-edit.

Research proceeds while style is pending. Capture a research-stage contract without images, deliver Research Review and summary, then capture an image-stage contract after actual style approval. Each stage has its own run ID and observed baseline. Do not include unfinished future outputs in an early-stage contract. A genuine later user scope/style change gets a linked successor contract; never rewrite the original digest to make a failing run pass.

## Scoped image fact updates without Excel

For IMAGE_ONLY_WORKFLOW or IMAGE_ADJUSTMENT_WORKFLOW, add imageFactUpdate to the pre-edit request as {fields: [["Product Details", "exact technical attribute"]], productPaths: ["/exact/scalar/cacheLeaf"], basis: "actual requested image purpose and research scope"}. Deliver both product-facts.json and research-ledger.json as RESEARCH to their existing 03_RESEARCH/FINAL IDs; keep workbook outputs out of this image contract. Existing selected technical fields can be researched or reconciled; copy/offer/FCC work is not smuggled into this branch. Unit fields are declared separately when changed.

Capture freezes the actual prior parsed facts/ledger inside the private run contract. Checks compare all undeclared facts, field selections and product leaves, preserve identity/configuration, validate current ledger structure, hardware/cache coherence, inches and actual research traces for the scoped fields. Declarations cannot be added after capture. The normal output/allowedChanges checks, actual image QA, privacy, source review and Drive history checks still apply. Contract snapshots are private pre-edit provenance, not a second live ledger or files to upload by default.

Excel bytes stay unchanged. The production receipt reports UNCHANGED_NOT_REVALIDATED_AGAINST_UPDATED_FACTS and lists preserved workbooks; previous workbook summaries/approvals do not certify the changed ledger. A later workbook task uses the current ledger and ordinary projection/summary checks. Honest unresolved research never becomes a visible image claim.

## Check outputs and delivery

```text
scripts/production_guard.py check --product <product-cache> --contract <contract.json> --contract-sha256 <independently-retained-sha256> --output <new-run-check.json>
```

Reject unrequested file changes/deletions, missing outputs, changed identity/configuration, mutated style bytes, dirty/different workflow, invalid mode/slot combinations and inputs changing during checking. Research Review allows truthful incomplete evidence but requires matching identity/configuration and a current metadata-bound coverage summary. LISTING Draft outputs check confirmed copy and base configuration while retaining truthful unresolved attribute/candidate rows. Marketplace export remains a separate stricter check; Drive delivery must not demand that all research be resolved. Images run full or selected-slot evidence checks. Candidate information remains outside confirmed workbook Values and customer claims.

The supported `drive_delivery.py plan` and `verify` CLI require `--production-contract` and `--contract-sha256`, reruns production checks, compares run ID and roles, then verifies Drive bytes, exact folder chains and privacy screens. A delivery batch may contain a subset of contracted outputs; the receipt covers only those files. All required batch receipts are needed for completion. The lower-level drive_delivery.verify API retains storage-only semantics for diagnostics/history and cannot grant production clearance. Concepts remain previews and cannot receive normal product-delivery completion.

Perform actual claim-by-claim review of title, bullets, description and image text against verified sold/capability facts and applicable seller policy. Official serial/exact-model research governs technical conflicts; factory facts require sold applicability. Existing validators enforce scope, projection, CPU/RAM/storage consistency, copy structure, warranty and evidence status. They cannot prove every free-text marketing statement, image fidelity, rights or search completeness. Never invent review PASS records or change facts to satisfy checks.

## Trust boundary

Use the committed checker and the digest from the earlier independent run record, not a recomputed digest from an edited contract. A model able to rewrite the checker, contract and independent record can bypass self-hosted checks; these tools detect violations in the supported workflow, not malicious execution outside it. CI protects reusable workflow changes. Storage, production quality and Seller Central authorization remain separate.

No automatic style approval, repeated upload confirmation, automatic publication, recursive historical ingestion or unrelated full-gallery regeneration is introduced.
