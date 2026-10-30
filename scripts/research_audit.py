"""Check recorded serial-first research coverage; never authenticate research."""
from datetime import date
import hashlib
import json
import re

ROUTES = {'OEM_SERIAL', 'OEM_MODEL', 'ERP', 'AMAZON', 'DEEP'}
RESULTS = {'REVIEWED', 'NO_MATCH', 'BLOCKED', 'NOT_APPLICABLE', 'NOT_STARTED'}
OUTCOMES = {'CONFIRMED', 'CANDIDATE', 'NOT_FOUND', 'INCOMPLETE', 'BLOCKED', 'CONFLICT', 'NOT_APPLICABLE'}


def text(value):
    return isinstance(value, str) and bool(value.strip())


def retained_input_hash(data, fact_id, dependencies):
    facts = {f['id']: f for f in data['facts']}
    ids = sorted(set([fact_id, *dependencies]))
    if any(key not in facts for key in ids):
        raise ValueError('Retained research dependency is missing')
    inputs = {'facts': [facts[key] for key in ids],
              'fields': sorted((m for m in data['fields'] if m['selected_fact'] in ids),
                               key=lambda m: (m['sheet'], m['attribute']))}
    return hashlib.sha256(json.dumps(inputs, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()


def validate_summary_trace(data, recorded):
    """Check current coverage and retained inputs; do not authenticate old sources."""
    current = validate(data)
    if not isinstance(recorded, dict) or any(recorded.get(key) != current[key]
            for key in ('state', 'checkedFields', 'missingFields', 'scope')):
        raise ValueError('Research trace summary disagrees with current ledger coverage')
    reuse = recorded.get('legacyReuse')
    if reuse is not None:
        missing = {f['id'] for f in data['facts'] if not f.get('evidence', {}).get('research_trace')}
        missing &= {m['selected_fact'] for m in data['fields']}
        if (not isinstance(reuse, dict) or not isinstance(reuse.get('retainedFactIds'), list)
                or set(reuse['retainedFactIds']) != missing or len(reuse['retainedFactIds']) != len(missing)
                or not text(reuse.get('baselineReference'))
                or any(not re.fullmatch('[0-9a-f]{64}', str(reuse.get(k, '')))
                       for k in ('previousLedgerSha256', 'reviewSha256'))):
            raise ValueError('Invalid retained research summary binding')
        bindings = reuse.get('retainedInputs')
        if bindings is not None:
            if not isinstance(bindings, dict) or set(bindings) != missing:
                raise ValueError('Retained input coverage differs from missing traces')
            for key, binding in bindings.items():
                if (not isinstance(binding, dict) or not isinstance(binding.get('dependencyFactIds'), list)
                        or not all(text(d) for d in binding['dependencyFactIds'])
                        or binding.get('sha256') != retained_input_hash(data, key, binding['dependencyFactIds'])):
                    raise ValueError('Retained research fact/dependency binding is stale')
    return recorded


def legacy_reuse(data, missing, previous_bytes, review):
    """Bind unchanged legacy facts to observed old bytes and an explicit impact review."""
    if not isinstance(review, dict) or not isinstance(previous_bytes, bytes):
        raise ValueError('Legacy reuse requires previous ledger bytes and a reuse review')
    digest = hashlib.sha256(previous_bytes).hexdigest()
    if review.get('previousLedgerSha256') != digest:
        raise ValueError('Legacy reuse baseline hash mismatch')
    previous = json.loads(previous_bytes.decode('utf-8-sig'))
    if not isinstance(previous, dict):
        raise ValueError('Legacy reuse requires a scoped previous ledger')
    # Old records may lack traces, but their scope and schema must still be valid.
    from research_export import validate_ledger
    validate_ledger(previous)
    for key in ('productId', 'configurationId'):
        if not text(data.get(key)) or previous.get(key) != data[key] or review.get(key) != data[key]:
            raise ValueError('Legacy reuse identity/configuration mismatch')
    if not all(text(review.get(key)) for key in ('baselineReference', 'reviewer', 'reviewed_date', 'impact_review')):
        raise ValueError('Legacy reuse needs observed baseline and applicability/impact review')
    reviewed = date.fromisoformat(review['reviewed_date'])
    if reviewed.isoformat() != review['reviewed_date'] or reviewed > date.today():
        raise ValueError('Invalid legacy reuse review date')
    entries = review.get('fields')
    if not isinstance(entries, list) or not all(isinstance(row, dict) and text(row.get('factId')) for row in entries):
        raise ValueError('Legacy reuse requires explicit retained fact entries')
    ids = [row['factId'] for row in entries]
    if len(set(ids)) != len(ids) or set(ids) != set(missing):
        raise ValueError('Legacy reuse must cover exactly the missing selected traces')
    old = {fact['id']: fact for fact in previous['facts']}
    current = {fact['id']: fact for fact in data['facts']}
    for row in entries:
        fact_id = row['factId']
        dependencies = row.get('dependencyFactIds')
        if (not text(row.get('basis')) or not isinstance(dependencies, list)
                or not all(text(key) for key in dependencies) or len(set(dependencies)) != len(dependencies)):
            raise ValueError('Legacy reuse needs applicability basis and explicit dependency facts')
        # Compare whole records, not just values: sources, scopes, candidates and
        # status must survive unchanged. Review cannot exempt changed dependencies.
        for key in [fact_id, *dependencies]:
            if key not in old or key not in current or old[key] != current[key]:
                raise ValueError('Legacy fact/dependency changed; refresh affected research traces')
        mappings = lambda ledger: [m for m in ledger['fields'] if m['selected_fact'] == fact_id]
        if mappings(previous) != mappings(data):
            raise ValueError('Legacy selected field mapping changed')
    return {'previousLedgerSha256': digest, 'baselineReference': review['baselineReference'],
            'reviewSha256': hashlib.sha256(json.dumps(review, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest(),
            'retainedFactIds': ids,
            'retainedInputs': {row['factId']: {
                'dependencyFactIds': row['dependencyFactIds'],
                'sha256': retained_input_hash(data, row['factId'], row['dependencyFactIds'])} for row in entries}}


def validate(data, required=False, previous_bytes=None, reuse=None):
    from fcc_inventory import is_external_field, validate_stub
    facts = {f['id']: f for f in data['facts']}
    checked, missing = 0, []
    for mapping in data['fields']:
        fact = facts[mapping['selected_fact']]
        evidence = fact.get('evidence', {})
        if is_external_field(data, fact):
            validate_stub(fact)
            checked += 1
            continue
        trace = evidence.get('research_trace')
        if trace is None:
            missing.append(fact['id'])
            continue
        if not isinstance(trace, dict) or trace.get('version') != 1:
            raise ValueError('Research trace version required')
        kind = trace.get('field_class')
        if kind not in {'TECHNICAL', 'SELLER_INPUT', 'SELLER_POLICY', 'DERIVED_COPY'}:
            raise ValueError('Research trace field classification required')
        if not text(trace.get('reason')):
            raise ValueError('Research trace requires a field-specific reason')
        # Classification is reviewed against the field Definition, not guessed by sheet.
        if kind != 'TECHNICAL':
            if not text(trace.get('basis')):
                raise ValueError('Nontechnical research disposition requires its source/basis')
            checked += 1
            continue
        outcome = trace.get('outcome')
        if outcome not in OUTCOMES:
            raise ValueError('Research trace outcome required')
        if trace.get('start') not in {'SERIAL_LOOKUP', 'NO_LINKED_SERIAL', 'REUSE_VERIFIED'}:
            raise ValueError('Serial-first start or documented exception required')
        if trace['start'] != 'SERIAL_LOOKUP' and not text(trace.get('start_basis')):
            raise ValueError('Missing serial/reused evidence needs its basis')
        routes = trace.get('routes')
        if not isinstance(routes, list):
            raise ValueError('Research routes must be recorded')
        names = set()
        for row in routes:
            if not isinstance(row, dict) or row.get('route') not in ROUTES or row.get('result') not in RESULTS:
                raise ValueError('Unknown research route/result')
            if not all(text(row.get(k)) for k in ('query', 'reference', 'detail', 'reviewed_date')):
                raise ValueError('Route needs query, sanitized reference, result detail and review date')
            reviewed = date.fromisoformat(row['reviewed_date'])
            if reviewed.isoformat() != row['reviewed_date'] or reviewed > date.today():
                raise ValueError('Invalid research review date')
            names.add(row['route'])
        if trace['start'] == 'SERIAL_LOOKUP' and routes and routes[0]['route'] != 'OEM_SERIAL':
            raise ValueError('Serial lookup must lead recorded research routes')
        if outcome == 'CONFIRMED' and (fact['status'] != 'VERIFIED' or not any(r['result'] == 'REVIEWED' for r in routes)):
            raise ValueError('Confirmed outcome needs a verified fact and reviewed evidence')
        if fact['status'] == 'VERIFIED' and outcome != 'CONFIRMED':
            raise ValueError('Verified fact cannot hide incomplete research')
        candidate = fact.get('value_candidate', fact.get('recommended_candidate'))
        exhausted = trace.get('exhausted') is True
        decision = trace.get('candidate_decision')
        if exhausted:
            if names != ROUTES or any(r['result'] == 'NOT_STARTED' for r in routes):
                raise ValueError('Exhaustion requires all applicable route dispositions')
            if not text(trace.get('stop_reason')):
                raise ValueError('Exhaustion needs a stop reason')
            if fact['status'] not in {'VERIFIED', 'NOT_APPLICABLE'}:
                if decision not in {'SELECTED', 'NO_SUPPORT', 'TIED'} or not text(trace.get('candidate_reason')):
                    raise ValueError('Unresolved exhausted research requires a best-candidate decision')
                if (decision == 'SELECTED') != (candidate is not None):
                    raise ValueError('Candidate decision and candidate value disagree')
                if candidate is not None and not all(text(evidence.get(k)) for k in ('candidate_rationale', 'candidate_missing_confirmation')):
                    raise ValueError('Best candidate needs rationale and missing confirmation')
        if outcome == 'NOT_FOUND':
            if not exhausted or decision != 'NO_SUPPORT' or candidate is not None or fact['status'] != 'TBD':
                raise ValueError('Not found requires exhausted no-support research, never a candidate')
            if any(r['result'] == 'BLOCKED' for r in routes):
                raise ValueError('Blocked access cannot be presented as not found')
        if outcome == 'CANDIDATE' and (candidate is None or fact['status'] in {'VERIFIED', 'NOT_APPLICABLE'}):
            raise ValueError('Candidate outcome must remain unverified')
        if outcome == 'NOT_APPLICABLE' and fact['status'] != 'NOT_APPLICABLE':
            raise ValueError('Not-applicable outcome/status mismatch')
        if outcome == 'BLOCKED' and fact['status'] not in {'SOURCE_UNAVAILABLE', 'INPUT_UNVERIFIED', 'CONFLICT'}:
            raise ValueError('Blocked outcome must keep an honest unresolved status')
        if outcome == 'CONFLICT' and fact['status'] != 'CONFLICT':
            raise ValueError('Conflicting outcome/status mismatch')
        modification = evidence.get('sold_modification')
        if modification is not None:
            if not isinstance(modification, dict) or not all(text(modification.get(k)) for k in ('record_reference', 'reviewed_date', 'unit_linkage', 'before', 'after', 'installation_evidence', 'reconciliation')):
                raise ValueError('Sold modification requires linked dated installation evidence and reconciliation')
            date.fromisoformat(modification['reviewed_date'])
        checked += 1
    reuse_result = None
    if reuse is not None or previous_bytes is not None:
        reuse_result = legacy_reuse(data, missing, previous_bytes, reuse)
    if required and missing and reuse_result is None:
        raise ValueError('New research requires research_trace for every selected field; missing count: ' + str(len(missing)))
    return {'state': 'RESEARCH_TRACE_RECORDED' if not missing else 'LEGACY_TRACE_INCOMPLETE',
            'checkedFields': checked, 'missingFields': len(missing),
            'legacyReuse': reuse_result,
            'scope': 'RECORDED_COVERAGE_ONLY_NOT_SOURCE_AUTHENTICATION'}
