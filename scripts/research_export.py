"""Project scoped evidence into a workbook or check a reviewed export; never publish."""
import argparse
import hashlib
import json
import math
from pathlib import Path

import openpyxl
from jsonschema import Draft202012Validator
from research_values import check_fcc_id_value

ROOT = Path(__file__).resolve().parents[1]
# These existing template fields describe capability rather than installed capacity.
# All unlisted fields require SOLD_BASE evidence. Offer 'maximum price' is not hardware capability.
CAPABILITY_FIELDS = {
    ('Product Details', name) for name in (
        'Ram Memory Maximum Size', 'RAM Memory Maximum Size', 'RAM Memory Maximum Size Unit',
        'Display Maximum Resolution', 'Display Resolution Maximum', 'Display Resolution Maximum Unit',
        'Supported Monitor Maximum Quantity', 'CPU Model Speed Maximum', 'CPU Model Speed Maximum Unit',
        'Maximum Display Brightness')
}


def load_ledger(path):
    data = json.loads(Path(path).read_text(encoding='utf-8-sig'))
    validate_ledger(data)
    return data


def validate_ledger(data):
    schema = json.loads((ROOT/'assets/research-ledger-schema.json').read_text(encoding='utf-8'))
    errors = list(Draft202012Validator(schema).iter_errors(data))
    if errors:
        error = errors[0]
        raise ValueError('Scoped ledger schema: ' + '/'.join(map(str, error.absolute_path))
                         + ' violates ' + str(error.validator))
    facts = {}
    for fact in data['facts']:
        if fact['id'] in facts:
            raise ValueError('Duplicate fact ID: ' + fact['id'])
        if fact['status'] not in ('VERIFIED', 'NOT_APPLICABLE') and fact['final_value'] is not None:
            raise ValueError('Unresolved fact must keep final_value null: ' + fact['id'])
        if fact['status'] == 'NOT_APPLICABLE' and fact['final_value'] is not None:
            raise ValueError('NOT_APPLICABLE must have a null value and source disposition')
        value = fact['final_value']
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError('Research values must be finite: ' + fact['id'])
        if fact['status'] == 'VERIFIED' and (value is None or isinstance(value, str) and not value.strip()):
            raise ValueError('VERIFIED fact requires a value: ' + fact['id'])
        if isinstance(value, str) and value.lstrip().startswith('='):
            raise ValueError('Formula is not a research value: ' + fact['id'])
        facts[fact['id']] = fact
    seen = set()
    for field in data['fields']:
        key = (field['sheet'], field['attribute'])
        if key in seen:
            raise ValueError('Duplicate field mapping: ' + str(key))
        seen.add(key)
        fact = facts.get(field['selected_fact'])
        if fact is None or (fact['sheet'], fact['attribute']) != key:
            raise ValueError('Missing or mismatched selected fact: ' + str(key))
        if fact['configurationId'] != data['configurationId']:
            raise ValueError('Selected fact belongs to another configuration: ' + str(key))
        allowed = {'SOLD_BASE', 'PLATFORM_CAPABILITY'} if key in CAPABILITY_FIELDS else {'SOLD_BASE'}
        if fact['fact_scope'] not in allowed:
            raise ValueError('Selected field requires sold/capability evidence, not factory/current-unit facts: ' + str(key))
        if fact['fact_scope'] == 'SOLD_BASE' and fact['status'] == 'VERIFIED':
            if fact.get('applies_to_sold_configuration') is not True or not fact.get('transfer_basis', '').strip():
                raise ValueError('Verified sold fact needs applicability and transfer_basis: ' + str(key))
        if key == ('Safety&Compliance', 'FCC ID') and fact['status'] == 'VERIFIED':
            check_fcc_id_value(fact['final_value'], 'VERIFIED')
            if fact.get('evidence_scope') not in ('HOST', 'RADIO_MODULE') or fact.get('authorization_route') != 'certification':
                raise ValueError('Verified FCC ID needs matched host/module certification scope')
    return facts


def project(data, field_keys, mode='draft'):
    if mode not in ('draft', 'export'):
        raise ValueError('Unknown projection mode')
    facts = validate_ledger(data)
    expected = list(field_keys)
    mapped = {(f['sheet'], f['attribute']): facts[f['selected_fact']] for f in data['fields']}
    if len(expected) != len(set(expected)) or set(mapped) != set(expected):
        raise ValueError('Ledger field mappings must cover the exact current template')
    projected = {}
    for key in expected:
        fact = mapped[key]
        candidate = fact.get('recommended_candidate')
        if mode == 'export':
            if fact['status'] not in ('VERIFIED', 'NOT_APPLICABLE'):
                raise ValueError('Export blocked by unresolved field: ' + str(key))
            if candidate is not None:
                raise ValueError('Export blocked by recommended candidate: ' + str(key))
        value = fact['final_value']
        source = fact['source']
        if mode == 'draft' and candidate is not None:
            if fact['status'] != 'INPUT_UNVERIFIED' or key != ('Safety&Compliance', 'FCC ID'):
                raise ValueError('Only INPUT_UNVERIFIED FCC research cells may show a recommended candidate')
            value = candidate
            if not isinstance(value, str) or not value.strip() or value.lstrip().startswith('='):
                raise ValueError('FCC candidate must be a nonempty text identifier')
            source = 'MOST_LIKELY_CANDIDATE — NOT CONFIRMED; ' + source
        projected[key] = {'value': value, 'status': fact['status'], 'source': source,
                          'fact_id': fact['id'], 'fact_scope': fact['fact_scope']}
    return projected


def workbook_fields(book):
    return [(sheet.title, cell.value) for sheet in book for cell in list(sheet[1])[1:]]


def same_cell_value(actual, expected):
    """Allow Excel's int/float round trip without conflating Boolean and number."""
    if isinstance(expected, bool) or isinstance(actual, bool):
        return type(actual) is type(expected) and actual == expected
    if isinstance(expected, (int, float)):
        return isinstance(actual, (int, float)) and math.isfinite(actual) and actual == expected
    return type(actual) is type(expected) and actual == expected


def verify_workbook(book, data, mode='draft'):
    result = project(data, workbook_fields(book), mode)
    for sheet in book:
        for column in range(2, sheet.max_column + 1):
            key = (sheet.title, sheet.cell(1, column).value)
            field = result[key]
            if not all(same_cell_value(sheet.cell(row, column).value, field[name])
                       for row, name in ((3, 'value'), (4, 'status'), (5, 'source'))):
                raise ValueError('Workbook differs from scoped ledger projection: ' + str(key))
            if any(sheet.cell(row, column).data_type == 'f' for row in (3,4,5)):
                raise ValueError('Formula cannot be exported: ' + str(key))
    return result


def run(template, ledger, workbook, mode, product_id=None, configuration_id=None, stage=None):
    template, ledger, workbook = map(Path, (template, ledger, workbook))
    canonical_template = ROOT/'assets/listing-workbook-template.xlsx'
    input_hashes = {name: hashlib.sha256(Path(path).read_bytes()).hexdigest()
                    for name, path in (('workbook', workbook), ('ledger', ledger), ('template', template))}
    # Import only at execution time; check-workbooks can use verify_workbook without a cycle.
    import importlib.util
    spec = importlib.util.spec_from_file_location('workbook_checks', ROOT/'scripts/check-workbooks.py')
    checks = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checks)
    if mode == 'export':
        if stage != 'LISTING_DRAFT':
            raise ValueError('Export requires explicit LISTING_DRAFT stage')
        if any(part.casefold() == 'workbook-snapshots' for part in workbook.resolve().parts):
            raise ValueError('Historical workbook snapshots cannot be exported')
        if input_hashes['template'] != hashlib.sha256(canonical_template.read_bytes()).hexdigest():
            raise ValueError('Export requires the current canonical template; alternate/old templates are draft-only')
        checks.check_template_inputs(canonical_template)
    product = None
    metadata_report = None
    manufacturer = None
    data = load_ledger(ledger)
    from research_handoff import check_product_location,coverage_summary,internal_storage_configuration
    check_product_location(workbook,data['productId'])
    listing_stage = stage == 'LISTING_DRAFT' if stage else '_LISTING_' in workbook.stem.upper()
    if mode == 'export' or listing_stage:
        facts_path=workbook.parent/'product-facts.json'
        input_hashes['productFacts']=hashlib.sha256(facts_path.read_bytes()).hexdigest()
        from product_metadata import listing_view
        raw_product = json.loads(facts_path.read_text(encoding='utf-8-sig'))
        product,metadata_report = listing_view(raw_product,data)
        manufacturer = product['identity'].get('oemBrand')
        if not manufacturer:
            raise ValueError('Listing workbook requires OEM brand for existing copy checks')
    checks.check_output(workbook, checks.template_topology(template), manufacturer)
    if mode == 'export' and (not product_id or not configuration_id):
        raise ValueError('Export requires explicit target product ID and configuration ID')
    if product_id is not None and product_id != data['productId']:
        raise ValueError('Ledger belongs to another target product')
    if configuration_id is not None and configuration_id != data['configurationId']:
        raise ValueError('Ledger belongs to another target configuration')
    if mode == 'export':
        if product.get('identity',{}).get('internalId')!=data['productId'] or product.get('selectedBaseConfiguration',{}).get('id')!=data['configurationId']:
            raise ValueError('Product facts identity/configuration differs from export target')
    book = openpyxl.load_workbook(workbook, data_only=False)
    try:
        projected = verify_workbook(book, data, mode)
        if mode == 'export':
            from listing_content import validate_listing
            definitions={(sheet.title,sheet.cell(1,c).value):sheet.cell(2,c).value
                         for sheet in book for c in range(2,sheet.max_column+1)}
            storage=internal_storage_configuration(data)
            validate_listing(projected,product,definitions,storage_total_gb=storage['totalGB'] if storage else None,storage_configuration=storage)
    finally:
        book.close()
    for name, path in (('workbook', workbook), ('ledger', ledger), ('template', template)):
        if hashlib.sha256(Path(path).read_bytes()).hexdigest() != input_hashes[name]:
            raise ValueError('Input changed during validation: ' + name)
    if product is not None and hashlib.sha256(facts_path.read_bytes()).hexdigest()!=input_hashes['productFacts']:
        raise ValueError('Input changed during validation: productFacts')
    return {'productFactsSha256':input_hashes.get('productFacts'), 'result': 'EXPORT_EVIDENCE_CHECK_PASS' if mode == 'export' else 'DRAFT_PROJECTION_PASS',
            'productId': data['productId'], 'configurationId': data['configurationId'],
            'workbookSha256': input_hashes['workbook'],
            'ledgerSha256': input_hashes['ledger'],
            'templateSha256': input_hashes['template'],
            'stage': stage or ('LISTING_DRAFT' if listing_stage else 'RESEARCH_REVIEW'),
            'amazonEligibilityAssessed': False, 'metadataView': metadata_report,
            'coverageSummary':coverage_summary(data,projected),
            'fields': [{'sheet': k[0], 'attribute': k[1], **v} for k,v in projected.items()]}


def main():
    import sys
    # Keep redirected JSON deterministic on Windows as well as Linux.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--template', type=Path, default=ROOT/'assets/listing-workbook-template.xlsx')
    parser.add_argument('--ledger', type=Path, required=True)
    parser.add_argument('--workbook', type=Path, required=True)
    parser.add_argument('--mode', choices=['draft', 'export'], default='draft')
    parser.add_argument('--product-id', help='Required for export: independently selected target')
    parser.add_argument('--configuration-id', help='Required for export: target base configuration')
    parser.add_argument('--stage', choices=['RESEARCH_REVIEW', 'LISTING_DRAFT'],
                        help='Export requires explicit LISTING_DRAFT; filenames cannot grant export eligibility')
    parser.add_argument('--summary-output',type=Path,help='Write a standalone research coverage JSON after successful checking')
    args = parser.parse_args()
    try:
        result = run(args.template, args.ledger, args.workbook, args.mode, args.product_id, args.configuration_id, args.stage)
        if args.summary_output:
            output=args.summary_output
            from research_handoff import check_product_location
            check_product_location(output,result['productId'])
            if not output.name.endswith('.research-summary.json'):
                raise ValueError('Summary output must end with .research-summary.json')
            if output.exists():
                previous=json.loads(output.read_text(encoding='utf-8-sig'))
                if not isinstance(previous,dict) or previous.get('artifactRole')!='RESEARCH_COVERAGE_SUMMARY' or previous.get('productId')!=result['productId']:
                    raise ValueError('Summary output would overwrite an unrelated artifact')
            summary={k:result[k] for k in ('productId','configurationId','stage','workbookSha256','ledgerSha256','templateSha256','productFactsSha256','coverageSummary')}
            summary['artifactRole']='RESEARCH_COVERAGE_SUMMARY'
            summary['workbookFile']=args.workbook.name
            from gallery_engine import write
            write(output,summary)
    except (ValueError, OSError, json.JSONDecodeError) as error:
        parser.exit(1, str(error) + '\n')
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
