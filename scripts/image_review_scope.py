"""Per-image evidence bindings; declarations require actual visual/semantic review."""
import hashlib
import json
from pathlib import Path

IDENTITY_KEYS = ('internalId', 'productId', 'identity', 'brand', 'manufacturer', 'model',
                 'modelNumber', 'modelName', 'sku', 'partNumber', 'color', 'formFactor', 'chassis')
IDENTITY_FIELDS = {'Manufacturer', 'Model Number', 'Model Name', 'Color', 'Form Factor'}
FACT_KEYS = ('id', 'status', 'final_value', 'fact_scope', 'configurationId', 'source',
             'applies_to_sold_configuration', 'transfer_basis')


def pointer(data, path):
    if not isinstance(path, str) or not path.startswith('/') or path == '/':
        raise ValueError('Product dependency requires an explicit JSON pointer')
    value = data
    for part in path[1:].split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        try:
            value = value[int(part)] if isinstance(value, list) and part.isdigit() else value[part]
        except (KeyError, IndexError, TypeError):
            raise ValueError('Product dependency path missing') from None
    return value


def binding(directory, slot, dependencies, policy_text=None):
    import gallery_engine as g
    from product_identity import product_id
    from product_metadata import selected_facts, hardware_projection
    from research_history import check_product_research_history
    from capacity_units import STORAGE_FIELDS
    p = Path(directory)
    if slot not in g.NAMES or not isinstance(dependencies, dict):
        raise ValueError('Per-image dependency declaration required')
    fields, paths = dependencies.get('fields'), dependencies.get('productPaths')
    if (not isinstance(fields, list) or not all(isinstance(key, list) and len(key) == 2
            and all(isinstance(v, str) and v.strip() for v in key) for key in fields)
            or not isinstance(paths, list) or not all(isinstance(v, str) for v in paths)
            or not fields and not paths or len({tuple(k) for k in fields}) != len(fields)
            or len(set(paths)) != len(paths) or not isinstance(dependencies.get('basis'), str)
            or not dependencies['basis'].strip()):
        raise ValueError('Explicit unique fields/product paths and actual coverage basis required')
    check_product_research_history(p)
    facts, style, ledger = (g.read(p/name) for name in ('product-facts.json', 'style-lock.json', 'research-ledger.json'))
    if (product_id(facts) != p.name or not isinstance(ledger, dict) or ledger.get('productId') != p.name
            or style.get('style_approval_status', style.get('status')) != 'APPROVED'):
        raise ValueError('Scoped image review requires matching product/ledger and approved style')
    selected = selected_facts(ledger)
    hardware = hardware_projection(ledger, facts)  # Retain cache/ledger coherence checks.
    requested = {tuple(key) for key in fields}
    if any(key not in selected for key in requested):
        raise ValueError('Image dependency is not a selected ledger field')
    required = requested | {key for key in selected if key[0] == 'Product Details' and key[1] in IDENTITY_FIELDS}
    # Unit facts are cheap to include and affect the meaning of any named value.
    for sheet, field in list(required):
        for key in selected:
            if key[0] == sheet and key[1].startswith(field) and key[1].endswith(' Unit'):
                required.add(key)
    projection = [{'sheet': sheet, 'attribute': field,
                   **{k: selected[(sheet, field)][k] for k in FACT_KEYS if k in selected[(sheet, field)]},
                   'capacityBasis': selected[(sheet, field)].get('evidence', {}).get('capacity_basis')}
                  for sheet, field in sorted(required)]
    identity = {key: facts[key] for key in IDENTITY_KEYS if key in facts}
    identity['configurationId'] = ledger['configurationId']
    payload = {'slot': slot, 'dependencies': dependencies, 'identity': identity, 'styleLock': style,
               'selectedFacts': projection, 'productValues': {path: pointer(facts, path) for path in sorted(paths)}}
    if any(field in STORAGE_FIELDS for _, field in required):
        payload['storageDependencies'] = hardware.get('storageDependencies')
        payload['storageCapacityBasis'] = hardware.get('storageCapacityBasis')
    recipe = style.get('recipePath')
    root = Path(g.__file__).resolve().parents[1]
    if recipe:
        payload['recipe'] = g.read(root/recipe if str(recipe).startswith('assets/') else p/recipe)
    for name in g.POLICY_INPUTS:
        payload[name] = (policy_text[name] if policy_text is not None else
                         (root/'references'/name).read_text(encoding='utf-8-sig')).replace('\r\n', '\n')
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def agree(directory):
    import gallery_engine as g
    visual, semantic = (g.read(Path(directory)/name) for name in ('visual-review.json', 'semantic-review.json'))
    if visual.get('schemaVersion') == 4 or semantic.get('schemaVersion') == 4:
        if visual.get('schemaVersion') != 4 or semantic.get('schemaVersion') != 4:
            raise ValueError('Visual and semantic reviews must use the same scoped review version')
        entries = {row['file']: row for row in visual['images']}
        for row in semantic['images']:
            other = entries.get(row['file'])
            if other is None or any(other.get(key) != row.get(key) for key in ('dependencies', 'reviewInputsSha256')):
                raise ValueError('Visual/semantic image dependency declarations disagree')
