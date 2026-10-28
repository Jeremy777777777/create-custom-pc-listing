"""Reject unsupported clock candidates; never convert a transfer rate to clock.

Only selected facts in selection-bound current ledgers are inspected. Historical
facts/evidence are retained without becoming current claims. This structural
check cannot authenticate a supplied manufacturer quotation or measurement.
"""
import math
import re

PAIRS = (('Memory Speed', 'Memory Speed Unit'),
         ('Memory Clock Speed', 'Memory Clock Speed Unit'))
TRANSFER = re.compile(r'(?<![a-z])(?:MT\s*/\s*s|megatransfers?\s*(?:/|per)\s*second)\b', re.I)
INFERENCE = re.compile(r'half[ -]?(?:rate|clock)|divid\w*|÷\s*2|/\s*2\b|'
                       r'DDR.{0,100}(?:correspond|conversion|suggest)|'
                       r'(?:infer|deriv)\w*.{0,80}clock', re.I)


def validate(data):
    if 'amazon_selection' not in data:
        return
    facts = {f['id']: f for f in data['facts']}
    selected = {(m['sheet'], m['attribute']): facts[m['selected_fact']]
                for m in data['fields']}
    transfer_candidates = []
    for value_name, unit_name in PAIRS:
        f = selected.get(('Product Details', value_name), {})
        u = selected.get(('Product Details', unit_name), {})
        value = f.get('value_candidate')
        unit = u.get('value_candidate', u.get('final_value'))
        if value is None:
            continue
        if (unit == 'MT/s' and isinstance(value, str)
                and re.fullmatch(r'[0-9]+(?:\.[0-9]+)?(?: or [0-9]+(?:\.[0-9]+)?)+', value)
                and str((f.get('evidence') or {}).get('candidate_rationale', '')).startswith('TIED_VARIANT_DEPENDENT:')
                and all(float(n) > 0 for n in value.split(' or '))):
            transfer_candidates.extend(float(n) for n in value.split(' or '))
            continue
        if (isinstance(value, bool) or not isinstance(value, (int, float))
                or not math.isfinite(value) or value <= 0):
            raise ValueError(value_name + ': candidate requires a positive finite rate')
        if unit not in ('MT/s', 'MHz', 'GHz'):
            raise ValueError(value_name + ': candidate requires its explicit rate basis/unit')
        if unit == 'MT/s':
            transfer_candidates.append(value)
    for value_name, unit_name in PAIRS:
        f = selected.get(('Product Details', value_name), {})
        u = selected.get(('Product Details', unit_name), {})
        value = f.get('value_candidate')
        unit = u.get('value_candidate', u.get('final_value'))
        if value is None or unit not in ('MHz', 'GHz'):
            continue
        evidence = f.get('evidence') or {}
        active = ' '.join(str(x or '') for x in (
            f.get('source'), f.get('value_candidate_source'),
            evidence.get('candidate_rationale')))
        half_of_transfer = any(math.isclose(value * (1000 if unit == 'GHz' else 1) * 2,
                                            rate, rel_tol=1e-9) for rate in transfer_candidates)
        if not (TRANSFER.search(active) or INFERENCE.search(active) or half_of_transfer):
            continue
        basis = evidence.get('memory_clock_basis') or {}
        # An independently quoted or measured clock can coincide numerically with
        # half a transfer rate. A formula or an inferred candidate is not evidence.
        if (basis.get('kind') not in ('OEM_STATED_CLOCK', 'MEASURED_CURRENT_CLOCK')
                or basis.get('value') != value or basis.get('unit') != unit
                or not isinstance(basis.get('source'), str) or not basis['source'].strip()
                or not isinstance(basis.get('excerpt'), str) or not basis['excerpt'].strip()
                or basis['source'] not in str(f.get('value_candidate_source', ''))):
            raise ValueError(value_name + ': unsupported transfer-to-clock candidate; retain '
                             'the source MT/s reference, withhold paired clock number, or '
                             'supply independent quoted/measured memory_clock_basis evidence')
