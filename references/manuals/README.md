# FCC lookup reading copies

Use [FCC ID lookup manual Word edition](fcc-id-lookup-manual.docx) for human reading and [Chinese source](fcc-id-lookup-manual.zh-CN.md) for searchable plain text. Version: 2026-10-21. Candidate rows follow the explicit user layout decision in ../candidate-review-rows.md.

Execution authority remains [FCC workflow](../fcc-research-workflow.md), [ledger and Excel projection](../research-ledger-projection.md), and [stage snapshots](../workbook-stage-snapshots.md), subject to current explicit user instructions and seller policy. The Word edition summarizes these references; it is not an independent product fact source or a second rulebook.

For current execution also apply the 2026-10-26 [official evidence chain and deep research](../evidence-chain-and-deep-research.md) decision. Matching official research governs ERP/Amazon disagreements, and an unsuccessful serial lookup alone does not complete field research. The 2026-10-21 reading copies retain their version and original hash-bound execution references; they do not incorporate this later project-wide decision and must not be read as overriding it.

`fcc-id-lookup-manual.source.json` binds the original Word bytes, Chinese source and source-reference text hashes. The changed ledger/projection reference now has its exact original source preserved under `source-snapshots/2026-10-21/`, selected by `sourceSnapshotPaths`; the original hash and Word/Chinese bytes are unchanged. This explicitly freezes the 2026-10-21 reading copy and does not claim it reflects current execution. New runs use the active evidence-chain, research-trace and output-Excel references. Source snapshots are historical and excluded from normal execution retrieval.

CI verifies the original source snapshot and document bytes. To publish a newer Word edition, reconcile the Chinese source and regenerate/review the Word pages before creating its new version/binding. Do not refresh hashes to make a stale reading copy appear current. Keep render previews and private serial evidence out of this folder.
