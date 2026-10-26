# Serial-first research trace and candidate decision — 2026-10-26

The [evidence chain](evidence-chain-and-deep-research.md) owns research authority and stopping decisions. This contract records their execution inside each selected fact's existing `evidence.research_trace`; it creates no second ledger or workbook columns. New full-workbook CLI generation requires one trace per selected field. Existing read-only checks retain legacy compatibility and validate any traces supplied. The Python projection/writer APIs remain lower-level helpers; they do not replace the CLI's new-run audit.

Each trace has `version:1`, `field_class` and a field-specific `reason`. Classify by the actual Definition: `TECHNICAL`, `SELLER_INPUT`, `SELLER_POLICY` or `DERIVED_COPY`. Nontechnical fields require `basis` identifying the actual seller source, missing input, policy or verified source-fact IDs. Do not misclassify a technical fact to avoid research. Classification and sources still require substantive review.

Technical traces additionally contain:

- `start`: `SERIAL_LOOKUP`, `NO_LINKED_SERIAL` or `REUSE_VERIFIED`. The latter two require `start_basis`, describing the completed serial search or exact still-applicable previous evidence. An inaccessible serial portal remains a serial-first attempt, with BLOCKED route result.
- `outcome`: `CONFIRMED`, `CANDIDATE`, `NOT_FOUND`, `INCOMPLETE`, `BLOCKED`, `CONFLICT` or `NOT_APPLICABLE`; this describes research, not a new workbook Status.
- `routes`: chronological entries with `route` (`OEM_SERIAL`, `OEM_MODEL`, `ERP`, `AMAZON`, `DEEP`), actual `query`, sanitized `reference`, `reviewed_date` (YYYY-MM-DD), `result` (`REVIEWED`, `NO_MATCH`, `BLOCKED`, `NOT_APPLICABLE`, `NOT_STARTED`) and explanatory `detail`. Shared document/query references may be reused across fields; each field retains its applicability and result. Do not repeat searches merely to create rows.
- `exhausted`: true only after all applicable routes and promising leads have dispositions. All five route categories must be represented, with an explicit reason for inapplicability. No NOT_STARTED entry is allowed when exhausted. Keep access blocks explicit; blocked research cannot become NOT_FOUND.
- Exhausted traces require `stop_reason`. Unresolved exhausted traces also require `candidate_decision` (`SELECTED`, `NO_SUPPORT`, `TIED`) and `candidate_reason`. SELECTED requires the existing `value_candidate` + `value_candidate_source` pair (or the FCC-specific `recommended_candidate`) and `evidence.candidate_rationale` + `candidate_missing_confirmation`. A tied result has no forced single candidate; alternatives remain in evidence. NOT_FOUND requires TBD, NO_SUPPORT, no candidate and no blocked route.

An early truthful PARTIAL workbook may use INCOMPLETE with an empty routes list and the actual reason/next action. It cannot label a fact VERIFIED or research exhausted. A serial lookup that confirmed one part does not complete other fields. Never generate synthetic traces for real products.

For a changed sold configuration, `evidence.sold_modification` contains `record_reference`, `reviewed_date`, `unit_linkage`, `before`, `after`, `installation_evidence` and `reconciliation`. These must describe actual target-linked assembly/detection evidence; a nonblank string is not authentication. Preserve FACTORY evidence separately and follow the official-priority reconciliation rule.

`scripts/research_audit.py` checks trace structure and outcome consistency. The `research_export.py --write-workbook` CLI runs it before creating a new file. A valid record does not prove its queries were performed or its sources are authentic. Review citations and target linkage separately. Historical ledgers and snapshots are not automatically rewritten or recertified.

Reuse stable research when exact model/region, configuration, relevant components and source applicability are unchanged. Recheck after changes to those inputs, newly conflicting evidence or a source revision. Refresh inventory/price/current warranty observations when used; a new chat alone does not invalidate stable hardware research. Preserve the earlier evidence and actual dates.
