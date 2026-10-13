"""Check template topology only; never infer factual, seller or publication readiness."""
import argparse
import json
import os
from pathlib import Path
import openpyxl
from warranty_policy import validate_workbook_copy

SHEETS = ['Product Details', 'Offer', 'Safety&Compliance']
FCC_FIELDS = ('FCC Radio Frequency Emission Compliance',
              'Radio Frequency Emission & Authorization Status', 'FCC ID',
              'SDoC Contact Name', 'SDoC Contact US Mailing Address',
              'SDoC Contact Email Address', 'SDOC Contact US Phone Number')


def check_fcc_template(path):
    """Confirm FCC inputs exist; this never authenticates a product or grant."""
    book = openpyxl.load_workbook(path)
    try:
        sheet = book['Safety&Compliance']
        headers = [cell.value for cell in sheet[1]]
        if any(headers.count(field) != 1 for field in FCC_FIELDS):
            raise ValueError('Template requires one of each FCC/SDoC field')
        col = headers.index('FCC ID') + 1
        if sheet.cell(3, col).number_format != '@':
            raise ValueError('Template FCC ID Value must use text formatting')
        for row in (3, 5):
            cell = sheet.cell(row, col)
            if not any(cell.coordinate in validation and validation.showInputMessage
                       and validation.prompt for validation in sheet.data_validations.dataValidation):
                raise ValueError('Template FCC ID needs Value/Source evidence prompts')
    finally:
        book.close()


def check_fcc_id_value(value, status):
    if str(status).strip().upper() != 'VERIFIED':
        return
    placeholders = {'', 'TBD', 'N/A', 'NA', 'NONE', 'YES', 'NO', 'FCC',
                    'FCC ID', 'SDOC', 'NOT APPLICABLE', 'NOT_APPLICABLE'}
    if not isinstance(value, str) or value.strip().upper() in placeholders:
        raise ValueError('VERIFIED FCC ID requires an actual text identifier, not a blank/placeholder')

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
                if sheet.title == 'Safety&Compliance' and sheet.cell(1,c).value == 'FCC ID':
                    check_fcc_id_value(sheet.cell(3,c).value, sheet.cell(4,c).value)
        if manufacturer is not None:
            validate_workbook_copy(book, manufacturer)
    finally:
        book.close()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--directory',default='.');args=ap.parse_args()
    root=Path(args.directory);topology=template_topology(root/'assets/listing-workbook-template.xlsx')
    check_fcc_template(root/'assets/listing-workbook-template.xlsx')
    outputs=sorted((root/'product generated photo').glob('VL-*/*.xlsx'))
    for path in outputs:
        manufacturer=None
        if '_LISTING_' in path.stem.upper():
            facts=json.loads((path.parent/'product-facts.json').read_text(encoding='utf-8-sig'))
            manufacturer=facts.get('identity',{}).get('oemBrand')
            if not manufacturer: raise ValueError(f'{path}: OEM brand required for warranty copy check')
        check_output(path,topology,manufacturer)
    summary={'templateStructure':'PASS','currentOutputsStructureChecked':len(outputs),
             'historicalOutputsExcluded':True,'factOrPublicationReadinessInferred':False}
    (root/'workbook-ci-summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary))
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'],'a',encoding='utf-8') as f:
            f.write(f'### Workbook structure scope\n\nTemplate structure PASS; {len(outputs)} current output workbooks checked. Historical workbooks excluded. No factual, warranty applicability or publication readiness inferred.\n')

if __name__=='__main__':main()
