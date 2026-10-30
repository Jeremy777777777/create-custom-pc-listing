"""Bounded canonical image-fact updates without generating or approving Excel.

Baseline snapshots belong to the frozen private run contract, not a new live
ledger. Normal Drive privacy, history, research and image review still apply.
"""
import copy
import json
from pathlib import Path

FILES = {'product-facts.json', 'research-ledger.json'}
MODES = {'IMAGE_ONLY_WORKFLOW', 'IMAGE_ADJUSTMENT_WORKFLOW'}


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def declaration(value):
    from product_metadata import NON_IMAGE_FIELDS
    if not isinstance(value, dict) or set(value) != {'fields', 'productPaths', 'basis'}:
        raise ValueError('Image fact scope requires fields, productPaths and actual basis')
    fields, paths = value['fields'], value['productPaths']
    if (not isinstance(fields, list) or not fields
            or any(not isinstance(f, list) or len(f) != 2 or f[0] != 'Product Details'
                   or not isinstance(f[1], str) or not f[1].strip() or f[1] in NON_IMAGE_FIELDS for f in fields)
            or len({tuple(f) for f in fields}) != len(fields)
            or not isinstance(paths, list) or any(not isinstance(p, str) or not p.startswith('/')
                   or p == '/' or any(v in ('', '..') for v in p[1:].split('/')) for p in paths)
            or len(set(paths)) != len(paths)
            or any(b.startswith(a + '/') for a in paths for b in paths if a != b)
            or not isinstance(value['basis'], str) or not value['basis'].strip()):
        raise ValueError('Image fact scope requires unique technical fields and exact product leaf paths')
    return value


def mask_product(data, paths):
    data = copy.deepcopy(data)
    for path in paths:
        parts = [s.replace('~1', '/').replace('~0', '~') for s in path[1:].split('/')]
        item = data
        for part in parts[:-1]:
            if not isinstance(item, dict) or part not in item:
                raise ValueError('Image fact product parent missing')
            item = item[part]
        if not isinstance(item, dict) or isinstance(item.get(parts[-1]), (dict, list)):
            raise ValueError('Image fact product paths must identify exact scalar leaves')
        item.pop(parts[-1], None)
    return data


def project_unchanged(data, fields):
    from product_metadata import selected_facts
    selected = selected_facts(data)
    if any(key not in selected for key in fields):
        raise ValueError('Image fact scope must use existing selected ledger fields')
    ids = {selected[key]['id'] for key in fields}
    result = copy.deepcopy(data)
    result['fields'] = [f for f in result['fields'] if (f['sheet'], f['attribute']) not in fields]
    result['facts'] = [f for f in result['facts'] if f['id'] not in ids]
    return result


def capture(product, scope):
    declaration(scope)
    product = Path(product)
    facts, ledger = (read(product / name) for name in ('product-facts.json', 'research-ledger.json'))
    project_unchanged(ledger, {tuple(f) for f in scope['fields']})
    mask_product(facts, scope['productPaths'])
    return {'schemaVersion': 1, 'scope': copy.deepcopy(scope),
            'baselineProductFacts': facts, 'baselineLedger': ledger}


def check(product, frozen):
    from product_identity import product_id
    from product_metadata import hardware_projection, selected_facts
    from research_audit import validate as trace_check
    from dimension_units import validate_dimensions
    if not isinstance(frozen, dict) or frozen.get('schemaVersion') != 1:
        raise ValueError('Frozen image fact baseline required')
    scope = declaration(frozen['scope'])
    product = Path(product)
    facts, ledger = (read(product / name) for name in ('product-facts.json', 'research-ledger.json'))
    previous, before = frozen['baselineProductFacts'], frozen['baselineLedger']
    if (product_id(facts) != product.name or product_id(previous) != product.name
            or any(ledger.get(k) != before.get(k) for k in ('productId', 'configurationId'))
            or ledger.get('productId') != product.name
            or facts.get('selectedBaseConfiguration', {}).get('id') != previous.get('selectedBaseConfiguration', {}).get('id')):
        raise ValueError('Image fact update cannot change product/configuration identity')
    fields = {tuple(f) for f in scope['fields']}
    if project_unchanged(ledger, fields) != project_unchanged(before, fields):
        raise ValueError('Research changed outside declared image fields')
    if mask_product(facts, scope['productPaths']) != mask_product(previous, scope['productPaths']):
        raise ValueError('Product facts changed outside declared image paths')
    hardware_projection(ledger, facts)
    scoped = {**ledger, 'fields': [f for f in ledger['fields'] if (f['sheet'], f['attribute']) in fields]}
    trace = trace_check(scoped, required=True)
    selected = selected_facts(ledger)
    # Include paired units so an image-only update cannot relabel centimetres.
    validate_dimensions({key: {'value': row['final_value'],
                         **({'value_candidate': row['value_candidate']} if 'value_candidate' in row else {})}
                         for key, row in selected.items()})
    return {'state': 'SCOPED_IMAGE_FACT_UPDATE_CHECKED', 'fields': scope['fields'],
            'productPaths': scope['productPaths'], 'researchTrace': trace,
            'workbookState': 'UNCHANGED_NOT_REVALIDATED_AGAINST_UPDATED_FACTS',
            'unchangedWorkbooks': sorted(p.name for p in product.glob('*.xlsx')),
            'factualAuthentication': 'ACTUAL_SOURCE_REVIEW_REQUIRED', 'publicationStatus': 'NOT_ASSESSED'}
