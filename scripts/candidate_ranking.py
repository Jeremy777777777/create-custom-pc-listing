"""Keep a reviewed hardware recommendation visible when schema projection withholds it."""
from datetime import date
from html import escape


def text(value):
    return isinstance(value, str) and bool(value.strip())


def assess(fact, required=False):
    review = fact.get('evidence', {}).get('candidate_assessment')
    if review is None:
        if required:
            raise ValueError('Candidate requires a comparative candidate_assessment: ' + fact['attribute'])
        return None
    if not isinstance(review, dict) or review.get('version') != 1:
        raise ValueError('Invalid candidate assessment version')
    if review.get('decision') not in {'RECOMMENDED', 'TIED'}:
        raise ValueError('Candidate assessment needs RECOMMENDED or TIED')
    for name in ('comparison', 'missing_confirmation', 'reviewed_date'):
        if not text(review.get(name)):
            raise ValueError('Candidate comparison requires ' + name)
    reviewed = date.fromisoformat(review['reviewed_date'])
    if reviewed.isoformat() != review['reviewed_date'] or reviewed > date.today():
        raise ValueError('Invalid candidate comparison date')
    options = review.get('options')
    if not isinstance(options, list) or not options:
        raise ValueError('Candidate comparison requires actual supported options')
    ids = []
    for option in options:
        if (not isinstance(option, dict) or option.get('value') is None
                or not all(text(option.get(k)) for k in ('id', 'source', 'support', 'limitations'))
                or option.get('confidence') not in {'HIGH', 'MEDIUM', 'LOW'}):
            raise ValueError('Each candidate needs value, source, support, limitations and qualitative confidence')
        ids.append(option['id'])
    if len(set(ids)) != len(ids):
        raise ValueError('Duplicate candidate option IDs')
    primary = review.get('primary_id')
    if review['decision'] == 'RECOMMENDED':
        if primary not in ids:
            raise ValueError('Recommendation requires a selected supported primary option')
        selected = next(o for o in options if o['id'] == primary)
        if fact.get('value_candidate') is not None and selected['value'] != fact['value_candidate']:
            raise ValueError('Ranked primary must match the recorded hardware candidate')
    elif primary is not None or len(options) < 2:
        raise ValueError('A genuine tie needs alternatives and cannot invent a primary')
    return review


def display(option):
    return str(option['value']) + ((' ' + str(option['unit'])) if option.get('unit') else '')


def recommendation_note(review):
    options = review['options']
    if review['decision'] == 'RECOMMENDED':
        primary = next(o for o in options if o['id'] == review['primary_id'])
        note = 'RECOMMENDED HARDWARE CANDIDATE: ' + display(primary) + ' (' + primary['confidence'] + ' confidence; NOT CONFIRMED). '
    else:
        note = 'TIED HARDWARE CANDIDATES: ' + ' / '.join(display(o) for o in options) + ' (NOT CONFIRMED). '
    note += 'Comparison: ' + review['comparison'] + '; Missing confirmation: ' + review['missing_confirmation']
    note += '; Options: ' + ' | '.join(display(o) + '; source=' + o['source'] + '; support=' + o['support']
                                     + '; limitations=' + o['limitations'] for o in options)
    return note


def apply(data, projected):
    facts = {f['id']: f for f in data['facts']}
    reviews = []
    for key, record in projected.items():
        fact = facts[record['fact_id']]
        review = assess(fact, required=data.get('candidate_coverage_version') == 2
                        and fact.get('value_candidate') is not None)
        if review is None:
            continue
        if fact['status'] in {'VERIFIED', 'NOT_APPLICABLE'}:
            raise ValueError('A candidate comparison cannot turn into a confirmed fact')
        note = recommendation_note(review)
        # Keep the formal/numeric output blank when its Amazon unit is incompatible.
        # Show the original hardware number WITH ITS OWN UNIT in the explanation.
        previous = record.get('value_candidate_source')
        record['value_candidate_source'] = note + (('; AMAZON FIELD PROJECTION: ' + previous) if previous else
            '; Amazon numeric candidate remains withheld where its paired unit/basis is incompatible or unresolved.')
        reviews.append({'sheet': key[0], 'attribute': key[1], 'review': review,
                        'visibleNote': record['value_candidate_source'],
                        'amazonNumericCandidate': record.get('value_candidate')})
    return reviews


def render_html(data, projected):
    """Readable companion, preserving exact units independently of Amazon numeric fields."""
    rows = apply(data, projected)
    body = []
    for row in rows:
        r = row['review']
        primary = next((o for o in r['options'] if o['id'] == r.get('primary_id')), None)
        value = display(primary) if primary else ' / '.join(display(o) for o in r['options'])
        confidence = primary['confidence'] if primary else 'TIED'
        detail = '<br>'.join(escape(display(o) + ': ' + o['support'] + ' Limitations: ' + o['limitations'])
                             + ' <a href="' + escape(o['source'], quote=True) + '">Source</a>' for o in r['options'])
        body.append('<tr><td>' + escape(row['attribute']) + '</td><td><strong>' + escape(value)
                    + '</strong><br>NOT CONFIRMED — ' + confidence + '</td><td>'
                    + escape(r['comparison']) + '<br>Missing confirmation: ' + escape(r['missing_confirmation'])
                    + '</td><td>' + detail + '</td></tr>')
    return ('<!doctype html><html lang="en"><meta charset="utf-8"><title>' + escape(data['productId'])
            + ' field recommendations</title><style>body{font:16px Arial;margin:30px;color:#142639}table{border-collapse:collapse;width:100%}'
            + 'td,th{padding:14px;border:1px solid #ccd5df;text-align:left;vertical-align:top}th{background:#edf3f8}</style>'
            + '<h1>' + escape(data['productId']) + ' — Field Recommendations</h1>'
            + '<p>Research references for review. These recommendations are not confirmed sellable-unit facts or approved Amazon entries.'
            + ' Original hardware units are retained; an incompatible Amazon unit does not authorize conversion or relabelling.</p>'
            + '<table><tr><th>Field</th><th>Recommended reference</th><th>Ranking and missing proof</th><th>Evidence and alternatives</th></tr>'
            + ''.join(body) + '</table></html>')
