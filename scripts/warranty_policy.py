"""Exact seller-confirmed copy validation; not OEM/legal/publication clearance."""
import json
import re
from pathlib import Path

POLICY = json.loads((Path(__file__).resolve().parents[1] / 'assets/warranty-disclosure-policy.json').read_text(encoding='utf-8'))
OWN_POLICY = json.loads((Path(__file__).resolve().parents[1] / 'assets/own-brand-listing-policy.json').read_text(encoding='utf-8'))

def render(manufacturer, listing_mode=None):
    if not isinstance(manufacturer, str) or not manufacturer.strip():
        raise ValueError('Verified OEM manufacturer name is required')
    if any(c in manufacturer for c in ('[', ']', '【', '】', '\n', '\r')):
        raise ValueError('Unresolved manufacturer placeholder or invalid name')
    if listing_mode == 'MEGAPC_OWN_BRAND':
        if manufacturer.strip().casefold() != 'megapc':
            raise ValueError('Own-brand warranty requires MegaPC manufacturer')
        return OWN_POLICY['warrantyParagraph']
    if listing_mode not in (None, 'CUSTOMIZED_OEM'):
        raise ValueError('Unsupported listingMode')
    return POLICY['paragraph'].replace(POLICY['manufacturerToken'], manufacturer.strip())

def validate_copy(manufacturer, bullets, description, warranty, listing_mode=None):
    expected = render(manufacturer, listing_mode)
    if not isinstance(bullets, str) or bullets.split('\n\n')[0] != expected:
        raise ValueError('Bullet 1 must equal the fixed Warranty and Disclosure paragraph')
    # The workbook stores literal HTML, not Excel font styling or Markdown.
    pattern = r'<strong>[^<>]+</strong><br/><br/>(?:\s*<strong>[^<>]+</strong><br/>[^<>]+?(?:<br/><br/>|$))+'
    if not isinstance(description, str) or re.fullmatch(pattern, description, re.DOTALL) is None:
        raise ValueError('Product Description requires strong identity/section headings and br/ separators')
    heading = '<strong>' + POLICY['heading'] + '</strong><br/>'
    if not isinstance(description, str) or description.count(heading) != 1 or description.split(heading)[-1] != expected:
        raise ValueError('Description must end with the exact Warranty and Disclosure section')
    if warranty != expected:
        raise ValueError('Warranty Description must equal the same fixed paragraph')
    return {'fixedWording': 'PASS', 'oemApplicabilityOrPublicationReadinessInferred': False}

def validate_workbook_copy(book, manufacturer, listing_mode=None):
    def value(sheet, field):
        ws = book[sheet]
        matches = [c for c in range(2, ws.max_column + 1) if ws.cell(1, c).value == field]
        if len(matches) != 1:
            raise ValueError(f'Missing/ambiguous warranty copy field: {sheet}/{field}')
        return ws.cell(3, matches[0]).value
    return validate_copy(manufacturer, value('Product Details', 'Bullet Point'),
                         value('Product Details', 'Product Description'),
                         value('Safety&Compliance', 'Warranty Description'), listing_mode)
