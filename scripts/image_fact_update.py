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
    if (not isinstance(value, dict) or not {'fields','productPaths','basis'} <= set(value)
            or not set(value) <= {'fields','productPaths','basis','serialResearchUpdate'}
            or type(value.get('serialResearchUpdate',False)) is not bool):
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
    def remove(node, parts):
        key = parts[0]
        if key not in node:
            return
        value = node[key]
        if len(parts) == 1:
            if isinstance(value, (dict, list)):
                raise ValueError('Image fact product paths must identify exact scalar leaves')
            del node[key]
        elif value is None:
            del node[key]  # An explicitly unknown parent can acquire the declared leaf.
        elif isinstance(value, dict):
            remove(value, parts[1:])
            if not value:
                del node[key]
        else:
            raise ValueError('Image fact product parent must be an object or absent')
    for path in paths:
        parts = [s.replace('~1', '/').replace('~0', '~') for s in path[1:].split('/')]
        remove(data, parts)
    return data


def project_unchanged(data, fields):
    from product_metadata import selected_facts
    selected = selected_facts(data)
    if any(key not in selected for key in fields):
        raise ValueError('Image fact scope must use existing selected ledger fields')
    result = copy.deepcopy(data)
    result['fields'] = [f for f in result['fields'] if (f['sheet'], f['attribute']) not in fields]
    result['facts'] = [f for f in result['facts'] if (f['sheet'], f['attribute']) not in fields]
    return result


def check_research_scope(before, current, fields, serial_update=False):
    """Permit new evidence inside declared fields, preserving other facts/units."""
    old=project_unchanged(before,fields); new=project_unchanged(current,fields)
    if not {f['id'] for f in before['facts']} <= {f['id'] for f in current['facts']}:
        raise ValueError('Preserve prior fact records when adding scoped research evidence')
    if serial_update:
        prior=old.pop('serial_research',{}); actual=new.pop('serial_research',{})
        if prior and not actual:
            raise ValueError('Preserve the recorded serial-research outcome')
        facts={f['id']:f for f in current['facts']}
        permitted={key for key,f in facts.items() if (f['sheet'],f['attribute']) in fields}
        units={u['unit_evidence_alias']:u for u in actual.get('units',[])}
        retained_ids=set()
        for unit in prior.get('units',[]):
            kept=units.get(unit['unit_evidence_alias'])
            if (not kept or any(kept.get(k)!=v for k,v in unit.items() if k!='fact_ids')
                    or not set(unit['fact_ids'])<=set(kept['fact_ids'])):
                raise ValueError('Preserve prior serial-unit evidence in scoped research')
            retained_ids.update(unit['fact_ids'])
        linked={key for u in units.values() for key in u['fact_ids']}
        if not linked <= permitted | retained_ids:
            raise ValueError('New serial evidence links facts outside declared fields')
        if not set(actual.get('resolved_fact_ids',[])) <= permitted | set(prior.get('resolved_fact_ids',[])):
            raise ValueError('Serial resolutions exceed scoped research')
    if old!=new:
        raise ValueError('Research changed outside declared image fields or revision fields')


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
    check_research_scope(before,ledger,fields,scope.get('serialResearchUpdate',False))
    if mask_product(facts, scope['productPaths']) != mask_product(previous, scope['productPaths']):
        raise ValueError('Product facts changed outside declared image paths')
    required = fields | {(m['sheet'], m['attribute']) for m in ledger['fields']
                         if m['sheet'] == 'Product Details' and m['attribute'] in
                         {'Manufacturer', 'Model Name', 'Model Number', 'Color', 'Form Factor'}}
    for sheet, field in list(required):
        required.update((m['sheet'], m['attribute']) for m in ledger['fields']
                        if m['sheet'] == sheet and m['attribute'].startswith(field)
                        and m['attribute'].endswith(' Unit'))
    hardware_projection(ledger, facts, required_fields=required)
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
