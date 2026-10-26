"""Check recorded serial-first research coverage; never authenticate research."""
from datetime import date

ROUTES = {'OEM_SERIAL', 'OEM_MODEL', 'ERP', 'AMAZON', 'DEEP'}
RESULTS = {'REVIEWED', 'NO_MATCH', 'BLOCKED', 'NOT_APPLICABLE', 'NOT_STARTED'}
OUTCOMES = {'CONFIRMED', 'CANDIDATE', 'NOT_FOUND', 'INCOMPLETE', 'BLOCKED', 'CONFLICT', 'NOT_APPLICABLE'}


def text(value):
    return isinstance(value, str) and bool(value.strip())


def validate(data, required=False):
    facts = {f['id']: f for f in data['facts']}
    checked, missing = 0, []
    for mapping in data['fields']:
        fact = facts[mapping['selected_fact']]
        evidence = fact.get('evidence', {})
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
    if required and missing:
        raise ValueError('New research requires research_trace for every selected field; missing count: ' + str(len(missing)))
    return {'state': 'RESEARCH_TRACE_RECORDED' if not missing else 'LEGACY_TRACE_INCOMPLETE',
            'checkedFields': checked, 'missingFields': len(missing),
            'scope': 'RECORDED_COVERAGE_ONLY_NOT_SOURCE_AUTHENTICATION'}
