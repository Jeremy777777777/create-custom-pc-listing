"""Separate explicitly requested FCC lookup from listing workbooks.

Private lookup records and raw serials belong in ERP Listing Inventory, never Git.
This module validates recorded results; it does not authenticate FCC evidence.
"""
import argparse
import json
from pathlib import Path

from research_values import check_fcc_id_value

ROOT = Path(__file__).resolve().parents[1]
FCC_KEY = ('Safety&Compliance', 'FCC ID')
EXTERNAL_MODE = 'ERP_INVENTORY'
DISPOSITION = 'MANAGED_SEPARATELY_IN_ERP_LISTING_INVENTORY; FCC_LOOKUP_ONLY task; not assessed in this listing workbook'


def external(data):
    return data.get('fcc_management') == EXTERNAL_MODE


def is_external_field(data, fact):
    return external(data) and (fact.get('sheet'), fact.get('attribute')) == FCC_KEY


def validate_stub(fact):
    """An external handoff is neither FCC confirmation nor not-applicable evidence."""
    if (fact.get('status') != 'TBD' or fact.get('final_value') is not None
            or fact.get('source') != DISPOSITION
            or any(fact.get(k) is not None for k in
                   ('recommended_candidate', 'value_candidate', 'value_candidate_source'))
            or fact.get('evidence_scope') or fact.get('authorization_route')
            or fact.get('evidence')):
        raise ValueError('External FCC field must be a blank TBD handoff without lookup results/candidates/evidence')


def inventory_update(record):
    """Return a private, exact-SKU update plan; never infer a candidate or a serial."""
    if record.get('workflow_mode') != 'FCC_LOOKUP_ONLY' or record.get('explicit_task') is not True:
        raise ValueError('FCC lookup requires a separate explicit FCC_LOOKUP_ONLY task')
    if not isinstance(record.get('internal_id'), str) or not record['internal_id'].strip():
        raise ValueError('Exact internal_id required')
    trace = record.get('search_trace')
    if not isinstance(trace, str) or not trace.strip():
        raise ValueError('Search trace with sources, outcome, date and scope required')
    confirmed = record.get('confirmed_id')
    candidate = record.get('candidate_id')
    outcome = record.get('outcome')
    allowed = {'UNIT_CONFIRMED', 'MODEL_MODULE_MATCH', 'SUPPORTED_OPTION_SELECTED',
               'PENDING', 'FACTORY_NO_WLAN', 'HOST_SDOC'}
    if outcome not in allowed:
        raise ValueError('Unknown manual lookup outcome')
    for value in (confirmed, candidate):
        if value is not None:
            check_fcc_id_value(value, 'VERIFIED')  # Identifier syntax only.
    if confirmed and candidate:
        raise ValueError('Confirmed ID and unconfirmed candidate must remain separate outcomes')
    if confirmed:
        if outcome != 'UNIT_CONFIRMED' or not record.get('confirmation_basis') or not record.get('scope'):
            raise ValueError('Confirmed ID requires exact unit/batch confirmation basis and scope')
    elif outcome == 'UNIT_CONFIRMED':
        raise ValueError('UNIT_CONFIRMED requires a confirmed identifier')
    if candidate:
        if outcome in {'FACTORY_NO_WLAN', 'HOST_SDOC'}:
            raise ValueError('No-radio/SDoC is not a radio-ID candidate')
        for key in ('candidate_basis', 'missing_confirmation', 'scope'):
            if not isinstance(record.get(key), str) or not record[key].strip():
                raise ValueError('Candidate requires ' + key)
        if record.get('candidate_confidence') not in {'HIGH', 'MEDIUM', 'LOW'}:
            raise ValueError('Candidate needs qualitative confidence, not an invented percentage')
    serials = record.get('used_serial_numbers', [])
    if not isinstance(serials, list) or any(not isinstance(s, str) or not s.strip() for s in serials):
        raise ValueError('used_serial_numbers must contain only actual nonempty lookup serials')
    return {
        'internal_id': record['internal_id'],
        'match_by': 'Virtual SKU',
        'updates': {'FCC ID（已确认）': confirmed or '', 'FCC ID 候选': candidate or '',
                    '使用过的 Serial Number': '\n'.join(dict.fromkeys(serials)),
                    'FCC ID 搜索足迹': trace},
        'outcome': outcome, 'scope': record.get('scope', ''),
        'confirmation_basis': record.get('confirmation_basis', ''),
        'candidate_basis': record.get('candidate_basis', ''),
        'missing_confirmation': record.get('missing_confirmation', ''),
        'candidate_confidence': record.get('candidate_confidence', ''),
        'destination': 'ERP Listing Inventory / Listing Tracker',
        'listing_workbook_write': False, 'marketplace_export_authorized': False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', type=Path, required=True, help='Private standalone FCC record')
    parser.add_argument('--output', type=Path, required=True, help='Private update plan; does not perform a Drive write')
    args = parser.parse_args()
    for path in (args.record, args.output):
        if path.resolve().is_relative_to(ROOT):
            raise ValueError('Raw FCC/SN business records must remain outside the workflow repository')
    result = inventory_update(json.loads(args.record.read_text(encoding='utf-8-sig')))
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
