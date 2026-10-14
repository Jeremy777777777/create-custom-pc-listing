"""Shared structural FCC identifier checks; not FCC authentication."""


def check_fcc_id_value(value, status):
    if str(status).strip().upper() != 'VERIFIED':
        return
    placeholders = {'', 'TBD', 'N/A', 'NA', 'NONE', 'YES', 'NO', 'FCC',
                    'FCC ID', 'SDOC', 'NOT APPLICABLE', 'NOT_APPLICABLE',
                    'UNKNOWN', 'PENDING', 'NOT FOUND', 'SOURCE_UNAVAILABLE'}
    if (not isinstance(value, str) or value.strip().upper() in placeholders
            or value.lstrip().startswith('=')):
        raise ValueError('VERIFIED FCC ID requires an actual text identifier, not a blank/placeholder')
