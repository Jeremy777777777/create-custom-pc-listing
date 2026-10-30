"""Seller customization copy; hardware research and installed numeric fields stay distinct."""
from datetime import date
import re

VERSION = 'customization-copy-v1'
RAM_OPTIONS = '8GB / 16GB / 32GB / 64GB'
SSD_OPTIONS = '512GB / 1TB / 2TB / 4TB'
TYPE = r'(?:LPDDR[3-6](?:X|T)?|DDR[3-6]L?)'


def research(product, ledger, required=False):
    """Read the selected RAM fact's evidence, never infer replaceability from DDR/LPDDR."""
    from listing_mode import resolve, CUSTOM
    if resolve(product) != CUSTOM:
        return None
    facts = {f['id']: f for f in ledger['facts']}
    ram = next((facts[m['selected_fact']] for m in ledger['fields']
                if (m['sheet'], m['attribute']) == ('Product Details', 'RAM Memory Installed')), None)
    record = ram.get('evidence', {}).get('customization_ram') if ram else None
    if record is None:
        if required:
            raise ValueError('New customized Listing requires researched RAM replaceability and exact memory type')
        return None  # Read-only compatibility, never proof of a current research pass.
    if not isinstance(record, dict):
        raise ValueError('RAM customization research must be an object')
    if record.get('status') != 'VERIFIED':
        if required:
            raise ValueError('RAM customization research is unresolved; preserve a PARTIAL Research Review')
        return {'policyVersion': VERSION, 'state': 'UNRESOLVED'}
    if type(record.get('replaceable')) is not bool or not re.fullmatch(TYPE, str(record.get('memoryType', ''))):
        raise ValueError('RAM customization requires a boolean replaceable and exact DDR/LPDDR generation')
    for key in ('replaceabilitySource', 'memoryTypeSource', 'reviewedDate'):
        if not isinstance(record.get(key), str) or not record[key].strip():
            raise ValueError('RAM customization research requires '+key)
    reviewed = date.fromisoformat(record['reviewedDate'])
    if reviewed.isoformat() != record['reviewedDate'] or reviewed > date.today():
        raise ValueError('RAM customization research date is invalid')
    if ram['status'] != 'VERIFIED' or ram['fact_scope'] != 'SOLD_BASE' or ram.get('applies_to_sold_configuration') is not True:
        raise ValueError('RAM customization must bind verified installed sold RAM')
    for mapping in ledger['fields']:
        if mapping['sheet'] == 'Product Details' and mapping['attribute'] == 'RAM Memory Technology':
            technology = facts[mapping['selected_fact']]
            if technology['status'] == 'VERIFIED' and str(technology['final_value']).casefold() != record['memoryType'].casefold():
                raise ValueError('RAM customization type disagrees with selected RAM Memory Technology')
    return {'policyVersion': VERSION, 'state': 'READY', 'ramFactId': ram['id'],
            'replaceable': record['replaceable'], 'memoryType': record['memoryType'],
            'replaceabilitySource': record['replaceabilitySource'], 'memoryTypeSource': record['memoryTypeSource'],
            'reviewedDate': record['reviewedDate']}


def fragments(product):
    info = product.get('customization')
    if not isinstance(info, dict) or info.get('policyVersion') != VERSION or info.get('state') != 'READY':
        raise ValueError('Current researched RAM customization is required before composing copy')
    if type(info.get('replaceable')) is not bool or not re.fullmatch(TYPE, str(info.get('memoryType', ''))):
        raise ValueError('Invalid researched RAM customization')
    if info['replaceable']:
        ram = RAM_OPTIONS+' '+info['memoryType']+' RAM Options'
    else:
        amount = product['selectedBaseConfiguration']['ramGB']
        if type(amount) not in (int, float) or amount <= 0:
            raise ValueError('Fixed RAM needs actual installed capacity')
        ram = f"{amount:g}GB {info['memoryType']} RAM (Fixed)"
    return {'ram': ram, 'ssd': SSD_OPTIONS+' SSD Options'}


def copy_texts(product):
    """Reusable deterministic fragments for the title, capacity bullet and HTML section."""
    parts = fragments(product)
    if product['customization']['replaceable']:
        explanation = 'Select your memory and SSD configuration when ordering.'
    else:
        explanation = 'Memory is fixed and is not a selectable upgrade; choose your SSD configuration when ordering.'
    body = parts['ram']+'; '+parts['ssd']+'. '+explanation
    return {'titleFragment': parts['ram']+', '+parts['ssd'],
            'bullet': 'Customization Choices — '+body,
            'descriptionSection': '<strong>Memory and Storage Customization</strong><br/>'+body}


def validate_copy(values, product):
    """Require choices in all three copy fields and return text with only those choices masked.

    Remaining installed-capacity/CPU/VRAM checks still inspect every other claim.
    No RAM maximum is consulted to filter the seller-confirmed options.
    """
    parts = fragments(product)
    cleaned = {}
    for field in ('Item Name', 'Bullet Point', 'Product Description'):
        value = values.get(field)
        if not isinstance(value, str):
            raise ValueError('Expected customization listing text: '+field)
        for kind, fragment in parts.items():
            if fragment not in value:
                raise ValueError('Missing exact '+kind+' customization wording: '+field)
        types = re.findall(r'\b'+TYPE+r'\b', value, re.I)
        if any(t.casefold() != product['customization']['memoryType'].casefold() for t in types):
            raise ValueError('Listing RAM type differs from researched generation: '+field)
        # Mask only correctly labelled complete option phrases, not arbitrary capacities.
        value = value.replace(parts['ssd'], 'SSD OPTIONS')
        if product['customization']['replaceable']:
            value = value.replace(parts['ram'], 'RAM OPTIONS')
        if re.search(r'\d+(?:GB|TB)\s*/\s*\d+(?:GB|TB)', value, re.I):
            raise ValueError('Unsupported customization capacity list: '+field)
        cleaned[field] = value
    return cleaned
