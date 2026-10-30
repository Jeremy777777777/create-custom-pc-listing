"""Per-image evidence bindings; declarations require actual visual/semantic review."""
import hashlib
import json
from pathlib import Path

IDENTITY_KEYS = ('internalId', 'productId', 'identity', 'brand', 'manufacturer', 'model',
                 'modelNumber', 'modelName', 'sku', 'partNumber', 'color', 'formFactor', 'chassis')
IDENTITY_FIELDS = {'Manufacturer', 'Model Number', 'Model Name', 'Color', 'Form Factor'}
FACT_KEYS = ('id', 'status', 'final_value', 'fact_scope', 'configurationId', 'source',
             'applies_to_sold_configuration', 'transfer_basis')
SCOPED_POLICY = 'assets/workflow-execution-policy.json'


def style_projection(directory, slot, style, policy_text=None, customization=False, dimensions=False):
    """V2 binds shared design plus this slot; delivery settings and other slots are irrelevant."""
    import gallery_engine as g
    if style.get('scopeVersion') != 2 or not isinstance(style.get('shared'), dict) or not style['shared']:
        raise ValueError('V2 review requires explicit shared and per-slot style')
    item = style.get('slots', {}).get(slot)
    if (not isinstance(item, dict) or item.get('status') != 'APPROVED'
            or not isinstance(item.get('approvalReference'), str) or not item['approvalReference'].strip()):
        raise ValueError('Selected slot requires its actual USER approval reference')
    series = style['shared'].get('designSeries')
    if series not in {'BUSINESS_LAPTOP', 'GAMING', 'MINI_PC'}:
        raise ValueError('Shared style needs the actual designSeries')
    root = Path(g.__file__).resolve().parents[1]
    if policy_text is None:
        policy = g.read(root/SCOPED_POLICY)
    else:
        raw = policy_text.get('__scopedImagePolicy__')
        if not isinstance(raw, str):
            raise ValueError('Historical v2 review requires the exact committed scoped image policy')
        policy = json.loads(raw)
    rules = policy['imageReview']
    kind = 'main' if slot in g.MAIN else 'supporting'
    relevant = {key: dict(rules[key]) for key in ('shared', kind, series)}
    extra_keys = ()
    if customization and 'customization' in rules:
        if rules['customization'].get('version') != 1:
            raise ValueError('Unknown customization image binding version')
        relevant['customization'] = dict(rules['customization'])
        extra_keys = ('customization',)
    if dimensions and 'dimensions' in rules:
        if rules['dimensions'].get('version') != 1:
            raise ValueError('Unknown dimension image binding version')
        relevant['dimensions'] = dict(rules['dimensions'])
        extra_keys += ('dimensions',)
    for rule in relevant.values():
        if isinstance(rule.get('sourceBindings'), dict):
            rule['sourceBindings'] = rule['sourceBindings'].get(kind, [])
    result = {'styleLock': {'shared': style['shared'], 'slot': item},
              'imagePolicy': relevant}
    from image_policy_sources import selected_sources
    sources = selected_sources(policy, series, kind, root, historical=policy_text is not None,
                               extra_keys=extra_keys)
    if sources is not None:
        result['imagePolicySources'] = sources
    recipe = item.get('recipePath')
    if recipe:
        from pathlib import PurePosixPath
        part = PurePosixPath(recipe)
        if part.is_absolute() or '..' in part.parts or '\\' in recipe or ':' in recipe:
            raise ValueError('Selected recipe must use a safe relative path')
        result['recipe'] = g.read(root/recipe if recipe.startswith('assets/') else Path(directory)/recipe)
    return result


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
    version = dependencies.get('scopeVersion', 1)
    if version not in (1, 2):
        raise ValueError('Unknown image dependency scope version')
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
    requested = {tuple(key) for key in fields}
    if any(key not in selected for key in requested):
        raise ValueError('Image dependency is not a selected ledger field')
    if version == 2 and any(selected[key]['status'] not in {'VERIFIED','NOT_APPLICABLE'} for key in requested):
        raise ValueError('Unresolved depicted image field: '+', '.join(field for sheet,field in sorted(requested)
                         if selected[(sheet,field)]['status'] not in {'VERIFIED','NOT_APPLICABLE'}))
    required = requested | {key for key in selected if key[0] == 'Product Details' and key[1] in IDENTITY_FIELDS}
    from dimension_units import dimension_dependencies, PAIRS, TEXT_FIELDS, validate_dimensions
    dimension_fields = set(PAIRS) | {(key[0],unit) for key,unit in PAIRS.items()} | TEXT_FIELDS
    has_dimensions = bool(requested & dimension_fields)
    # Historical policy retains its exact old payload. Current reviews use the
    # explicit mapping, not a naming-prefix guess, for dimension dependencies.
    current_dimensions = version == 2 and (policy_text is None or 'dimensions' in
        json.loads(policy_text.get('__scopedImagePolicy__','{}')).get('imageReview',{}))
    if current_dimensions:
        expanded = dimension_dependencies(requested)
        if not expanded <= set(selected):
            raise ValueError('Dimension dependency requires its exact value/unit pair')
        if any(selected[key]['status'] not in {'VERIFIED','NOT_APPLICABLE'} for key in expanded & dimension_fields):
            raise ValueError('Unresolved depicted dimension or paired unit')
        required.update(expanded)
        validate_dimensions({key:{'value':selected[key]['final_value']} for key in expanded})
    # Unit facts are cheap to include and affect the meaning of any named value.
    for sheet, field in list(required):
        for key in selected:
            if key[0] == sheet and key[1].startswith(field) and key[1].endswith(' Unit'):
                required.add(key)
    hardware = hardware_projection(ledger, facts, required_fields=required if version == 2 else None)
    projection = [{'sheet': sheet, 'attribute': field,
                   **{k: selected[(sheet, field)][k] for k in FACT_KEYS if k in selected[(sheet, field)]},
                   'capacityBasis': selected[(sheet, field)].get('evidence', {}).get('capacity_basis')}
                  for sheet, field in sorted(required)]
    identity = {key: facts[key] for key in IDENTITY_KEYS if key in facts}
    identity['configurationId'] = ledger['configurationId']
    payload = {'slot': slot, 'dependencies': dependencies, 'identity': identity,
               'selectedFacts': projection, 'productValues': {path: pointer(facts, path) for path in sorted(paths)}}
    if any(field in STORAGE_FIELDS for _, field in required):
        payload['storageDependencies'] = hardware.get('storageDependencies')
        payload['storageCapacityBasis'] = hardware.get('storageCapacityBasis')
    if version == 2:
        ram_fields = {'RAM Memory Installed', 'RAM Memory Installed Size Unit', 'RAM Memory Technology'}
        from listing_mode import resolve, CUSTOM
        customization = (resolve(facts) == CUSTOM and
                         (slot == 'PT05.png' or any(sheet == 'Product Details' and field in ram_fields
                                                  for sheet, field in required)))
        style_data = style_projection(directory, slot, style, policy_text,
                                      customization=customization, dimensions=has_dimensions)
        payload.update(style_data)
        if 'customization' in style_data['imagePolicy']:
            # Bind researched replaceability/type and its sources, not only the
            # installed GB value. Missing evidence remains explicit, never READY.
            payload['customizationFacts'] = [
                {'sheet': sheet, 'attribute': field,
                 **{k: row[k] for k in FACT_KEYS if k in row},
                 'customizationRam': row.get('evidence', {}).get('customization_ram')}
                for (sheet, field), row in sorted(selected.items())
                if sheet == 'Product Details' and field in ram_fields]
        return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
    payload['styleLock'] = style
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
            if row.get('dependencies', {}).get('scopeVersion') == 2 and other.get('customerText') != row.get('customerText'):
                raise ValueError('Visual/semantic rendered-copy declarations disagree')
