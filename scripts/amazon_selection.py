"""Bind output values to observed Amazon controls without changing hardware facts.

Editable predictive inputs supply suggestions, not a closed vocabulary. A nearby
closed choice is review advice only and must never become an exportable fact.
"""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT/'assets/amazon-selection-catalog.json'
CONTEXT_KEYS = ('marketplaceId', 'locale', 'productType', 'itemTypeKeyword')
PAIRED_BASIS = {
    ('Product Details', 'Color Gamut Name'): ('Color Gamut', 'Color Gamut Value'),
    ('Safety&Compliance', 'Average Battery Life Unit'): ('Battery Life',),
    ('Safety&Compliance', 'Average Standby Battery Life Unit'): ('Average Standby Battery Life',),
    ('Safety&Compliance', 'Battery charge time'): ('Battery Charge Time',),
    ('Safety&Compliance', 'Battery Weight Unit'): ('Battery Weight',),
    ('Safety&Compliance', 'Lithium Battery Energy Content Unit'): ('Lithium Battery Energy Content',),
    ('Safety&Compliance', 'Non-Lithium Battery Energy Content Unit'): ('Non-Lithium Battery Energy Content',),
}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def normalized(value):
    if isinstance(value, bool):
        return 'true' if value else 'false'
    return re.sub(r'\s+', ' ', str(value).strip()).casefold()


def read_catalog(path=CATALOG):
    raw = Path(path).read_bytes()
    catalog = json.loads(raw)
    if catalog.get('schemaVersion') != 1 or not isinstance(catalog.get('contexts'), list):
        raise ValueError('Invalid Amazon selection catalog')
    seen = set()
    for context in catalog['contexts']:
        key = tuple(context.get(k) for k in CONTEXT_KEYS)
        if not all(isinstance(v, str) and v.strip() for v in key) or key in seen:
            raise ValueError('Missing or duplicate Amazon catalog context')
        seen.add(key)
        paths, fields = set(), set()
        for control in context['controls']:
            path = (control['sheet'], control['path'])
            field = (control['sheet'], control['attribute']) if control.get('attribute') else None
            if path in paths or field is not None and field in fields:
                raise ValueError('Ambiguous Amazon control/field mapping')
            paths.add(path)
            if field is not None:
                fields.add(field)
            if control['kind'] not in {'CLOSED', 'ACCOUNT_CLOSED', 'SUGGESTED', 'TEXT', 'NUMBER', 'DATE'}:
                raise ValueError('Unknown Amazon control kind')
            choices = control.get('options', [])
            codes = [x['code'] for x in choices]
            if len(codes) != len(set(codes)):
                raise ValueError('Duplicate Amazon option codes')
            if control['kind'] == 'CLOSED' and (not choices or control.get('complete') is not True):
                raise ValueError('Closed choice requires a complete observed option list')
            if not control.get('evidenceSha256') or not control.get('observedAtUtc'):
                raise ValueError('Amazon control requires observation provenance')
    return catalog, digest(raw)


def match_option(control, value):
    """Exact label/code or explicitly reviewed alias; never fuzzy matching."""
    target = normalized(value)
    matches = [o for o in control.get('options', []) if not o.get('disabled') and
               target in {normalized(o['code']), normalized(o['label'])}]
    if not matches:
        alias = control.get('aliases', {}).get(target)
        matches = [o for o in control.get('options', []) if o['code'] == alias and not o.get('disabled')]
    if len(matches) > 1:
        raise ValueError('Ambiguous Amazon value; explicit option selection required')
    return matches[0] if matches else None


def context_for(catalog, requested):
    matches = [c for c in catalog['contexts'] if
               all(c.get(k) == requested.get(k) for k in CONTEXT_KEYS)]
    if len(matches) != 1:
        raise ValueError('Amazon catalog context is unobserved; do not reuse another product type')
    return matches[0]


def apply(data, projected, catalog, catalog_sha256, mode='draft'):
    """Validate/format schema selections, keeping underlying facts immutable."""
    if mode not in {'draft', 'export'}:
        raise ValueError('Unknown Amazon selection projection mode')
    binding = data.get('amazon_selection')
    if not isinstance(binding, dict) or binding.get('schemaVersion') != 1:
        raise ValueError('New output requires amazon_selection binding')
    if binding.get('catalogSha256') != catalog_sha256:
        raise ValueError('Amazon selection binding is stale for current catalog bytes')
    context = context_for(catalog, binding.get('context', {}))
    controls = {(c['sheet'], c['attribute']): c for c in context['controls'] if c.get('attribute')}
    decisions = binding.get('fields', [])
    by_key = {(d.get('sheet'), d.get('attribute')): d for d in decisions}
    if len(by_key) != len(decisions) or set(by_key) != set(projected):
        raise ValueError('Amazon selection review must cover each template field exactly once')
    output = {k: dict(v) for k, v in projected.items()}
    unknown, approximate = [], []
    for key, record in output.items():
        review = by_key[key]
        control = controls.get(key)
        if control is None:
            if review.get('decision') != 'UNOBSERVED' or not review.get('reason', '').strip():
                raise ValueError('Unobserved Amazon field requires an explicit limitation: ' + str(key))
            if record.get('value') is not None or record.get('value_candidate') is not None:
                unknown.append(key)
                if mode == 'export':
                    raise ValueError('Export blocked by unobserved Amazon control: ' + str(key))
            continue
        if review.get('path') != control['path']:
            raise ValueError('Amazon field review refers to a different control: ' + str(key))
        if control['kind'] == 'ACCOUNT_CLOSED':
            if record.get('value') is not None or record.get('value_candidate') is not None:
                if review.get('decision') != 'UNOBSERVED' or not review.get('reason', '').strip():
                    raise ValueError('Account-specific closed choice requires fresh account review: ' + str(key))
                if mode == 'export':
                    raise ValueError('Export blocked by account-specific Amazon choices: ' + str(key))
                original = record['value'] if record.get('value') is not None else record['value_candidate']
                record.update(value=None, status='INPUT_UNVERIFIED', value_candidate=None,
                              value_candidate_source=None, source=record['source']
                              + '; ACCOUNT-SPECIFIC CLOSED SELECTION NOT VALIDATED: ' + str(original)
                              + '; ' + review['reason'])
                unknown.append(key)
            continue
        if control['kind'] != 'CLOSED':
            if review.get('decision') != 'DIRECT':
                raise ValueError('Editable suggestions cannot be treated as closed choices: ' + str(key))
            continue
        values = {name: record.get(name) for name in ('value', 'value_candidate')}
        missing = []
        mapped = {}
        for name, value in values.items():
            if value is None:
                continue
            # Repeated selections need explicit members: never split model names on commas.
            members = review.get('members', {}).get(name, [value])
            if not isinstance(members, list) or not members or any(v is None for v in members):
                raise ValueError('Invalid explicit repeatable Amazon selections')
            if len(members) > 1 and (not control.get('repeatable') or
                    not isinstance(value, str) or value != '; '.join(str(v) for v in members)):
                raise ValueError('Repeatable members must bind the exact original value')
            options = [match_option(control, v) for v in members]
            if any(o is None for o in options):
                missing.append(name)
            else:
                mapped[name] = '; '.join(o['label'] for o in options)
        if missing:
            if review.get('decision') != 'APPROXIMATE':
                raise ValueError('No suitable Amazon option: closest reference candidate is mandatory: ' + str(key))
            for name in ('reason', 'differences', 'missingConfirmation'):
                if not isinstance(review.get(name), str) or not review[name].strip():
                    raise ValueError('Approximation requires ' + name + ': ' + str(key))
            option = next((o for o in control['options'] if o['code'] == review.get('referenceOptionCode')
                           and not o.get('disabled')), None)
            if option is None:
                raise ValueError('Approximate reference must be an observed allowed option')
            if mode == 'export':
                raise ValueError('Export blocked by approximate Amazon option: ' + str(key))
            original = values['value'] if values['value'] is not None else values['value_candidate']
            previous_candidate_source = record.get('value_candidate_source') if values['value_candidate'] is not None else None
            reference = binding.get('catalogReference')
            if not reference:
                raise ValueError('Approximate reference requires an opened catalogReference URL')
            from workbook_reference_audit import clean_url
            clean_url(reference)
            record.update(value=None, status='INPUT_UNVERIFIED', value_candidate=option['label'],
                source=record['source'] + '; VERIFIED/RESEARCHED VALUE RETAINED IN LEDGER: ' + str(original)
                    + '; AMAZON_SELECTION_UNRESOLVED; ' + review['differences']
                    + (('; ORIGINAL HARDWARE CANDIDATE SUPPORT: ' + previous_candidate_source) if previous_candidate_source else ''),
                value_candidate_source='APPROXIMATE AMAZON OPTION — REFERENCE ONLY; NOT CONFIRMED; '
                    + ((reference + '; ') if reference else '')
                    + 'Catalog evidence SHA256: ' + control['evidenceSha256'] + '; Reason: ' + review['reason']
                    + '; Differences: ' + review['differences'] + '; Missing confirmation: ' + review['missingConfirmation'])
            approximate.append(key)
        else:
            if review.get('decision') != 'DIRECT':
                raise ValueError('Exact compatible option must use DIRECT decision')
            record.update(mapped)
    # A nearby unit/gamut label cannot silently relabel the original number.
    from listing_content import CAPACITY_PAIRS, SPEED_PAIRS
    pairs = dict(PAIRED_BASIS)
    pairs.update({('Product Details', unit): (value,) for value, unit in {**CAPACITY_PAIRS, **SPEED_PAIRS}.items()})
    blocked_pairs = []
    for basis_key in approximate:
        for name in pairs.get(basis_key, ()):
            key = (basis_key[0], name)
            if key not in output:
                continue
            record = output[key]
            if record.get('value') is None and record.get('value_candidate') is None:
                continue
            original = record['value'] if record.get('value') is not None else record['value_candidate']
            record.update(value=None, status='INPUT_UNVERIFIED', value_candidate=None,
                          value_candidate_source=None,
                          source=record['source'] + '; ORIGINAL VALUE RETAINED IN LEDGER: ' + str(original)
                              + '; Paired Amazon basis is approximate: ' + basis_key[1]
                              + '; No numerical conversion or equivalence has been verified.')
            blocked_pairs.append(key)
    return output, {'state': 'AMAZON_SELECTION_PARTIAL' if unknown or approximate else 'AMAZON_SELECTION_CHECK_PASS',
                    'context': binding['context'], 'catalogSha256': catalog_sha256,
                    'unobservedPopulatedFields': [list(k) for k in unknown],
                    'approximateReferenceFields': [list(k) for k in approximate],
                    'pairedBasisUnresolvedFields': [list(k) for k in blocked_pairs],
                    'scope': 'OBSERVED_UI_SCHEMA_ONLY_NOT_PRODUCT_FACT_OR_PUBLICATION_APPROVAL'}


def project_if_bound(data, projected, mode='draft', required=False, catalog_path=CATALOG):
    if 'amazon_selection' not in data:
        if required:
            raise ValueError('New generation/export/delivery requires Amazon selection review')
        return projected, {'state': 'LEGACY_AMAZON_SELECTION_NOT_ASSESSED'}
    catalog, sha = read_catalog(catalog_path)
    return apply(data, projected, catalog, sha, mode)
