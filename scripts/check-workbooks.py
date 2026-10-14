"""Check workbook structure and obvious FCC ID placeholders; never authenticate compliance."""
import argparse
import json
import os
from pathlib import Path
import openpyxl
from warranty_policy import validate_workbook_copy
from research_values import check_fcc_id_value

SHEETS = ['Product Details', 'Offer', 'Safety&Compliance']
RESEARCH_STATUSES = ('VERIFIED', 'INPUT_UNVERIFIED', 'CONFLICT', 'TBD',
                     'SOURCE_UNAVAILABLE', 'NOT_APPLICABLE')
FCC_FIELDS = ('FCC Radio Frequency Emission Compliance',
              'Radio Frequency Emission & Authorization Status', 'FCC ID',
              'SDoC Contact Name', 'SDoC Contact US Mailing Address',
              'SDoC Contact Email Address', 'SDOC Contact US Phone Number')


def check_template_inputs(path):
    """Check required FCC inputs and the shared research status vocabulary."""
    book = openpyxl.load_workbook(path)
    try:
        sheet = book['Safety&Compliance']
        headers = [cell.value for cell in sheet[1]]
        if any(headers.count(field) != 1 for field in FCC_FIELDS):
            raise ValueError('Template requires one of each FCC/SDoC field')
        col = headers.index('FCC ID') + 1
        if sheet.cell(3, col).number_format != '@':
            raise ValueError('Template FCC ID Value must use text formatting')
        for tab in book:
            for column in range(2, tab.max_column + 1):
                cell = tab.cell(4, column)
                if not any(cell.coordinate in validation and validation.type == 'list'
                           and validation.formula1 == '"' + ','.join(RESEARCH_STATUSES) + '"'
                           for validation in tab.data_validations.dataValidation):
                    raise ValueError('Template Status dropdown must match research statuses')
    finally:
        book.close()


def check_field_disposition(status, source):
    if status not in RESEARCH_STATUSES:
        raise ValueError('Status must be one of the six research statuses')
    if not isinstance(source, str) or not source.strip():
        raise ValueError('Source or disposition must contain non-whitespace text')

def template_topology(path):
    book = openpyxl.load_workbook(path, data_only=False)
    try:
        if book.sheetnames != SHEETS:
            raise ValueError('Unexpected template sheets/order')
        result = {}
        for sheet in book:
            if sheet.max_row < 5 or sheet.max_column < 2:
                raise ValueError(f'{sheet.title}: expected five template rows')
            headers = [sheet.cell(1,c).value for c in range(2,sheet.max_column+1)]
            if any(not h for h in headers) or len(set(headers)) != len(headers):
                raise ValueError(f'{sheet.title}: missing or duplicate field names')
            result[sheet.title] = ([tuple(sheet.cell(r,c).value for c in range(1,sheet.max_column+1)) for r in (1,2)],
                                   tuple(sheet.cell(r,1).value for r in range(3,6)))
        return result
    finally:
        book.close()

def check_output(path, topology, manufacturer=None):
    book = openpyxl.load_workbook(path, data_only=False)
    try:
        if book.sheetnames != list(topology):
            raise ValueError(f'{path}: sheets/order changed')
        for sheet in book:
            rows, labels = topology[sheet.title]
            if sheet.max_row < 5 or sheet.max_column != len(rows[0]):
                raise ValueError(f'{path}: {sheet.title} template dimensions changed')
            if [tuple(sheet.cell(r,c).value for c in range(1,sheet.max_column+1)) for r in (1,2)] != rows:
                raise ValueError(f'{path}: {sheet.title} headers/definitions changed')
            if tuple(sheet.cell(r,1).value for r in range(3,6)) != labels:
                raise ValueError(f'{path}: {sheet.title} row labels changed')
            if any(sheet.cell(r,c).value is not None for r in range(6,sheet.max_row+1) for c in range(1,sheet.max_column+1)):
                raise ValueError(f'{path}: {sheet.title} extra data rows added')
            for c in range(2,sheet.max_column+1):
                if not sheet.cell(4,c).value or not sheet.cell(5,c).value:
                    raise ValueError(f'{path}: {sheet.title}/{sheet.cell(1,c).value} lacks Status/Source or disposition')
                check_field_disposition(sheet.cell(4,c).value, sheet.cell(5,c).value)
                if sheet.title == 'Safety&Compliance' and sheet.cell(1,c).value == 'FCC ID':
                    check_fcc_id_value(sheet.cell(3,c).value, sheet.cell(4,c).value)
        if manufacturer is not None:
            validate_workbook_copy(book, manufacturer)
        ledger_path = path.parent/'research-ledger.json'
        if ledger_path.exists():
            ledger = json.loads(ledger_path.read_text(encoding='utf-8-sig'))
            if isinstance(ledger, dict):
                from research_export import verify_workbook
                verify_workbook(book, ledger, mode='draft')
            elif not isinstance(ledger, list):
                raise ValueError('Research ledger must be a legacy array or scoped object')
    finally:
        book.close()

def current_workbooks(root):
    # Immediate canonical product folders only; history/ and nested scratch are excluded.
    return sorted((Path(root)/'product generated photo').glob('*/*.xlsx'))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--directory',default='.');args=ap.parse_args()
    root=Path(args.directory);topology=template_topology(root/'assets/listing-workbook-template.xlsx')
    check_template_inputs(root/'assets/listing-workbook-template.xlsx')
    outputs=current_workbooks(root)
    scoped_checked=0
    legacy_not_assessed=0
    for path in outputs:
        manufacturer=None
        if '_LISTING_' in path.stem.upper():
            facts=json.loads((path.parent/'product-facts.json').read_text(encoding='utf-8-sig'))
            manufacturer=facts.get('identity',{}).get('oemBrand')
            if not manufacturer: raise ValueError(f'{path}: OEM brand required for warranty copy check')
        check_output(path,topology,manufacturer)
        ledger_path=path.parent/'research-ledger.json'
        if ledger_path.exists():
            if isinstance(json.loads(ledger_path.read_text(encoding='utf-8-sig')), dict):
                scoped_checked+=1
            else:
                legacy_not_assessed+=1
    summary={'templateStructure':'PASS','currentOutputsStructureChecked':len(outputs),
             'historicalOutputsExcluded':True,'factOrPublicationReadinessInferred':False,
             'scopedDraftProjectionChecked':scoped_checked,
             'legacyLedgerScopeNotAssessed':legacy_not_assessed}
    (root/'workbook-ci-summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary))
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'],'a',encoding='utf-8') as f:
            f.write(f'### Workbook structure scope\n\nTemplate structure PASS; {len(outputs)} current output workbooks checked. Historical workbooks excluded. No factual, warranty applicability or publication readiness inferred.\n')

if __name__=='__main__':main()
