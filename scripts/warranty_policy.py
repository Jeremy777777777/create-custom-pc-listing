"""Exact seller-confirmed copy validation; not OEM/legal/publication clearance."""
import json
from pathlib import Path

POLICY = json.loads((Path(__file__).resolve().parents[1] / 'assets/warranty-disclosure-policy.json').read_text(encoding='utf-8'))

def render(manufacturer):
    if not isinstance(manufacturer, str) or not manufacturer.strip():
        raise ValueError('Verified OEM manufacturer name is required')
    if any(c in manufacturer for c in ('[', ']', '【', '】', '\n', '\r')):
        raise ValueError('Unresolved manufacturer placeholder or invalid name')
    return POLICY['paragraph'].replace(POLICY['manufacturerToken'], manufacturer.strip())

def validate_copy(manufacturer, bullets, description, warranty):
    expected = render(manufacturer)
    if not isinstance(bullets, str) or bullets.split('\n\n')[0] != expected:
        raise ValueError('Bullet 1 must equal the fixed Warranty and Disclosure paragraph')
    heading = '**' + POLICY['heading'] + '**' + chr(92) + '\n'
    if not isinstance(description, str) or description.count(heading) != 1 or description.split(heading)[-1] != expected:
        raise ValueError('Description must end with the exact Warranty and Disclosure section')
    if warranty != expected:
        raise ValueError('Warranty Description must equal the same fixed paragraph')
    return {'fixedWording': 'PASS', 'oemApplicabilityOrPublicationReadinessInferred': False}

def validate_workbook_copy(book, manufacturer):
    def value(sheet, field):
        ws = book[sheet]
        matches = [c for c in range(2, ws.max_column + 1) if ws.cell(1, c).value == field]
        if len(matches) != 1:
            raise ValueError(f'Missing/ambiguous warranty copy field: {sheet}/{field}')
        return ws.cell(3, matches[0]).value
    return validate_copy(manufacturer, value('Product Details', 'Bullet Point'),
                         value('Product Details', 'Product Description'),
                         value('Safety&Compliance', 'Warranty Description'))
