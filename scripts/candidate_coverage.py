"""Account for blank draft values without inventing facts or candidate numbers."""
from collections import Counter
from datetime import date

DECISIONS = {'NO_SUPPORT', 'TIED', 'SELLER_INPUT_REQUIRED', 'RESEARCH_PENDING', 'BLOCKED'}


def text(value):
    return isinstance(value, str) and bool(value.strip()) and value.strip().upper() not in {'TBD', 'UNKNOWN', 'N/A'}


def require_current(data):
    if data.get('candidate_coverage_version') != 1:
        raise ValueError('New workbook generation requires candidate_coverage_version: 1 and per-field candidate review')


def review_projection(data, projected, required=False):
    """Check exact projected coverage; expose gap explanations, never fabricate research."""
    strict = required or data.get('candidate_coverage_version') == 1
    facts = {f['id']: f for f in data['facts']}
    counts = Counter()
    unresolved = []
    for key, record in projected.items():
        if record['status'] in {'VERIFIED', 'NOT_APPLICABLE'}:
            counts[record['status']] += 1
            continue
        fact = facts[record['fact_id']]
        from fcc_inventory import is_external_field, validate_stub
        if is_external_field(data, fact):
            validate_stub(fact)
            counts['MANAGED_SEPARATELY'] += 1
            continue
        evidence = fact.get('evidence', {})
        candidate = record.get('value_candidate')
        if candidate is not None:
            if strict and not text(record.get('value_candidate_source')):
                raise ValueError('Candidate needs visible source and qualification: ' + str(key))
            decision = 'SELECTED'
        else:
            review = evidence.get('candidate_review')
            if review is None and not strict:
                counts['UNREVIEWED_LEGACY'] += 1
                continue
            if not isinstance(review, dict) or review.get('decision') not in DECISIONS:
                raise ValueError('Blank Value and candidate require an explicit candidate_review: ' + str(key))
            for name in ('reason', 'missing_confirmation', 'next_action', 'owner', 'reviewed_date'):
                if not text(review.get(name)):
                    raise ValueError('Candidate review requires ' + name + ': ' + str(key))
            reviewed = date.fromisoformat(review['reviewed_date'])
            if reviewed.isoformat() != review['reviewed_date'] or reviewed > date.today():
                raise ValueError('Invalid candidate review date: ' + str(key))
            decision = review['decision']
            trace = evidence.get('research_trace', {})
            if decision == 'NO_SUPPORT' and (trace.get('exhausted') is not True or
                    trace.get('candidate_decision') != 'NO_SUPPORT'):
                raise ValueError('NO_SUPPORT requires exhausted no-support research: ' + str(key))
            if decision == 'TIED' and (not isinstance(review.get('alternatives'), list) or
                    len(review['alternatives']) < 2 or not all(
                    isinstance(a, dict) and a.get('value') is not None and text(a.get('source'))
                    for a in review['alternatives'])):
                raise ValueError('TIED requires sourced alternatives: ' + str(key))
            explanation = ('NO CONFIRMED CANDIDATE — ' + decision + '; ' + review['reason']
                           + '; Missing confirmation: ' + review['missing_confirmation']
                           + '; Next action: ' + review['next_action'] + '; Owner: ' + review['owner'])
            if decision == 'TIED':
                explanation += '; Alternatives: ' + '; '.join(
                    str(a['value']) + ' [' + a['source'] + ']' for a in review['alternatives'])
            record['value_candidate_source'] = explanation
        counts[decision] += 1
        unresolved.append({'sheet': key[0], 'attribute': key[1], 'decision': decision,
                           'candidate': candidate, 'explanation': record.get('value_candidate_source')})
    return {'version': 1, 'state': 'PARTIAL' if unresolved else 'ALL_VALUES_RESOLVED',
            'counts': dict(counts), 'unresolvedFields': unresolved,
            'scope': 'RECORDED_DISPOSITIONS_ONLY_NOT_FACT_AUTHENTICATION'}
