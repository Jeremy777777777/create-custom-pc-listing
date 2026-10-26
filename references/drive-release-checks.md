# Product release checks — 2026-10-26

[Drive delivery](google-drive-delivery.md) owns storage layout and authorization. These checks make its boundaries reproducible. They use supplied connector observations; none authenticates a remote account, uploads files, grants style/QA approval or locks Drive. Continue the existing run record instead of creating a second product status system.

## Before replacing current files

Resolve the exact product/current IDs and load the last verified Drive receipt and original ledger, style lock and affected dependencies. Record their actual hashes. Existing Git history checks cover retained Git fixtures only; a new Drive product needs this Drive baseline. A missing baseline is HISTORY_CONTINUITY_UNVERIFIED, not an inferred clean history. Preserve current bytes in the established archive and reconcile the baseline before overwriting them. First delivery requires a completed accessible destination search proving no previous product delivery; a failed search is not first delivery.

Use one writer per product in the current coordinated work. Immediately before writes, read back the targeted current file IDs, parents and checksums again. `delivery_context.py revision --baseline <baseline.json> --observed <fresh.json>` compares exact inventories. Both inputs contain `productId`, actual UTC `readBackAtUtc` and `files` rows with `relativePath`, `id`, `sha256`, `parentFolderId`. Include the current delivery marker in this comparison. A changed/moved/missing file or new competing revision stops overwrite for reconciliation. This check is not a remote transaction/lock: use provider conditional writes when actually supported; otherwise serialize writers and verify immediately after writes. Never claim race-free execution from offline comparison alone.

For ledger changes, run `delivery_context.py history --previous <downloaded-previous-ledger> --current <new-ledger> --previous-sha256 <hash-from-verified-previous-receipt>`. It rejects a scoped-ledger downgrade or product/configuration substitution. Keep complete old coherent bundles, conflicts, approvals and source evidence archived; the helper does not prove archive preservation or authenticate the baseline. A legitimate configuration change needs a separately identified/reconciled configuration, not relabelling the previous one. Unrelated product history is outside this check.

Prepare all files and archive old coherent bytes before replacing current files. Reuse stable IDs. If a write is uncertain, read back before retrying. If any dependent file fails, mark DELIVERY_INCOMPLETE and record changed/unchanged IDs and repair actions; do not update the completion marker or delete the only local copy. Publish the run's completion marker/current summary last, after all listed bytes and roles pass. Consumers use that manifest to detect a mixed/incomplete current view; stable file IDs do not provide atomic multi-file replacement.

## Privacy of actual deliverables

Run `delivery_privacy.py check-file --input <file> --serials-used yes|no [--private-values-file <private-list.json>] [--visual-review <inspection.json>]` on each planned file. If raw serials/service tags were used in the run, the actual known-value list is mandatory, stays private and is deleted only after verified delivery. Do not declare no merely to bypass this requirement.

The helper screens JSON/text and every XLSX XML/relationship part, including hidden cells, comments, hyperlinks and document properties. Images have metadata screening plus actual visual privacy inspection; XLSX embedded media/objects and unsupported formats also require inspection. The separate inspection contains the exact `sha256`, `result: NO_PRIVATE_CONTENT`, actual `reviewer`, `reviewedAtUtc` and substantive `notes`. It must describe actual inspection, never a generated PASS. Unknown sensitive content still needs review. A no-pattern result cannot establish licensing, hardware fidelity or complete privacy clearance. Keep original evidence private and create a sanitized derivative when needed; never alter facts to satisfy screening.

## Product directory and receipt

The `drive_delivery.py verify` CLI now requires `--context <context.json>` in addition to plan/readbacks/destinations. The context contains:

- `productId`, `serialsUsed` boolean and `folders`: current connector folder observations with `id`, `name`, `mimeType`, `parents`, `readBackAtUtc` and optional `trashed`. Read them after plan creation. Include pinned project/products roots, one exact internal-ID folder and the relevant section/FINAL children.
- `fileRoles`: each exact planned relative path maps to RESEARCH, LISTING, IMAGE, QA or SOURCE. Research uses `03_RESEARCH/FINAL`, listing `01_LISTING`, canonical images `02_IMAGES`, reviews `04_QA`, supporting production assets `90_SOURCE`. Workbook stage/role is grounded in the existing workbook checks, never guessed from a filename alone. Canonical names get an additional role check.
- `privacyChecks`: each planned path maps to its actual-byte `check-file` result. All hashes and serial-use declarations must match. Shareable readbacks remain separately projected with `share-readbacks`.

The verifier checks the pinned project/products chain, exact product and role folders, current privacy screens, and original byte/metadata comparison. Missing context on the lower-level Python API produces only DRIVE_BYTES_MATCHED_CONTEXT_UNCHECKED, never DRIVE_DELIVERY_VERIFIED. Connector authenticity, actual previous-version preservation, completed prewrite/history checks and real review remain required operating evidence in the run record.

## One completion report

Use separate existing run-record fields for: research outcome/unresolved counts; Research Review and Listing Draft stage; USER style approval and preview/recipe reference; current scoped image QA; exact delivered-file inventory/receipt; workflow SHA and backup scope; publication NOT_EXECUTED or actual separately authorized state. A directory called FINAL, eleven filenames, candidate-filled cells, a test pass or a GitHub push cannot substitute for these states. Keep screenshots/previews outside the eleven canonical current slots.

Evidence reuse is bounded by current identity, configuration, bytes, parents and applicable policy. Changes invalidate only dependent facts/outputs/reviews; they do not revoke an unchanged user-approved style direction or force unrelated product research.
