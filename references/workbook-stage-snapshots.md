# Current workbooks and historical stage snapshots — 2026-10-14

Apply [research-ledger-projection.md](research-ledger-projection.md). Early Research Review delivery remains allowed. A later listing may use newly verified facts without rewriting the earlier research result to pretend it was already known.

## Artifact roles

- Every immediate `product generated photo/<internal-id>/*.xlsx` is **current**, regardless of its date or filename. It must use the current canonical template and, for scoped ledgers, match the current ledger projection. Multiple current files are allowed only when their projected facts/statuses/sources are reconciled. Do not silently exclude an inconvenient current workbook by renaming it.
- A superseded stage is an immutable **HISTORICAL_SNAPSHOT** under `product generated photo/<internal-id>/workbook-snapshots/<revision>/`. It preserves the workbook, the exact ledger used at that stage, the original template, and snapshot.json with SHA256 for all three. It is not current approval or a source of newly verified product facts.
- Snapshot CI verifies preserved bytes and role metadata, without applying the latest ledger/template/copy policy to those historical bytes. A snapshot is never export-eligible, even if its original values happened to be VERIFIED. The export command rejects workbooks in workbook-snapshots. To produce a current listing, reconcile the facts into the current ledger and create/review a current workbook.

## Transition to a new stage

1. Before replacing the current ledger or advancing a workbook whose projection will differ, identify any earlier workbook that should remain a frozen record rather than an updated current review. Preserve its corresponding original ledger and template at the same time. If those original inputs are missing, report the gap and recover the genuine files; do not bind an old workbook to a newly invented or updated ledger.
2. Create a new, non-existing revision directory and move only the superseded workbook into it; include copies of its original ledger and original template. Retain raw serial evidence privately and check public artifacts for sensitive data before committing. Do not change the historical workbook's cells or upgrade its status. Use a different revision for a distinct snapshot; do not overwrite a prior bundle.
3. Write the receipt below with actual IDs, stage, local filenames and hashes computed from the preserved bytes. The three paths must be distinct simple filenames within the bundle; no parent paths or undeclared extra files/subdirectories are allowed.
4. Run scripts/check-workbooks.py through the normal test helper. Snapshot hash/metadata checks must pass. Create/update the current workbook and current ledger at product top level; current projection checks must pass independently. Commit the coherent transition together. Missing receipts or changed snapshot bytes fail CI.

Receipt format (replace illustrative values and hash placeholders with actual evidence):

```json
{
  "schemaVersion": 1,
  "artifactRole": "HISTORICAL_SNAPSHOT",
  "exportEligible": false,
  "productId": "PRODUCT-ID",
  "configurationId": "BASE-CONFIGURATION-ID",
  "stage": "RESEARCH_REVIEW",
  "files": {
    "workbook": {"path": "RESEARCH_REVIEW.xlsx", "sha256": "<64 lowercase hex characters>"},
    "ledger": {"path": "research-ledger.json", "sha256": "<64 lowercase hex characters>"},
    "template": {"path": "template.xlsx", "sha256": "<64 lowercase hex characters>"}
  }
}
```

Stages are RESEARCH_REVIEW or LISTING_DRAFT. The receipt's productId must match its product directory. `SNAPSHOT_HASHES_VERIFIED` certifies preservation only, not the original facts, original QA, rights or marketplace acceptance. Legacy array ledgers may be preserved as the actual original input; they are not automatically migrated or made export-ready. Existing outputs are not automatically archived by a workflow/code update.

Historical snapshot access is permitted specifically to preserve/verify those records or for an explicit historical comparison. It does not authorize inheriting archived instructions, style approvals, PASS claims or stale facts. Only current reconciled facts drive new listing copy/images.

The updated FCC guide additionally permits the Excel writer's explicit `--previous-workbook` color comparison: a matching same-product/configuration snapshot must pass receipt/hash and workbook-role checks. Reuse only the fill of an unchanged previously VERIFIED FCC ID; all current values/statuses/sources come from the current ledger. This exception does not execute archived content, promote historical evidence or allow snapshot export.
# Preservation refinement — 2026-10-14

Apply [workflow validation boundaries](workflow-validation-boundaries.md): snapshot paths disable Git text conversion and revision-scoped CI compares existing bundle blobs to the trusted base. Receipt rehashing cannot authorize a rewrite; add a new revision bundle. Runs without base/head verify current bundle integrity only.
