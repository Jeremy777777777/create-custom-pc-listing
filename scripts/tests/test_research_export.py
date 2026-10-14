"""Guard sold-vs-factory scope and draft-vs-export boundaries using synthetic facts."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import openpyxl
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import research_export as r


class ResearchExportTests(unittest.TestCase):
    def ledger(self, key=('Product Details', 'RAM Memory Size')):
        return {'schemaVersion': 1, 'productId': 'TEST-PC', 'configurationId': 'BASE-A',
                'facts': [{'id': 'sold', 'sheet': key[0], 'attribute': key[1],
                           'configurationId': 'BASE-A', 'fact_scope': 'SOLD_BASE',
                           'status': 'VERIFIED', 'final_value': 32, 'source': 'Synthetic fixture',
                           'applies_to_sold_configuration': True, 'transfer_basis': 'Test assembly record'}],
                'fields': [{'sheet': key[0], 'attribute': key[1], 'selected_fact': 'sold'}]}

    def test_sold_capacity_not_factory_capacity(self):
        data = self.ledger()
        factory = copy.deepcopy(data['facts'][0])
        factory.update(id='factory', fact_scope='FACTORY', final_value=16)
        data['facts'].append(factory)
        key = ('Product Details', 'RAM Memory Size')
        self.assertEqual(r.project(data, [key], 'export')[key]['value'], 32)
        data['fields'][0]['selected_fact'] = 'factory'
        with self.assertRaisesRegex(ValueError, 'not factory'):
            r.project(data, [key], 'export')

    def test_platform_maximum_cannot_fill_installed_capacity(self):
        data = self.ledger()
        data['facts'][0].update(fact_scope='PLATFORM_CAPABILITY', final_value=64)
        with self.assertRaises(ValueError):
            r.project(data, [('Product Details', 'RAM Memory Size')])
        key = ('Product Details', 'RAM Memory Maximum Size')
        data['facts'][0]['attribute'] = data['fields'][0]['attribute'] = key[1]
        self.assertEqual(r.project(data, [key], 'export')[key]['value'], 64)

    def test_fcc_candidate_stays_draft_and_cannot_be_promoted(self):
        key = ('Safety&Compliance', 'FCC ID')
        data = self.ledger(key)
        fact = data['facts'][0]
        fact.update(status='INPUT_UNVERIFIED', final_value=None, recommended_candidate='TEST-ID')
        draft = r.project(data, [key])
        self.assertEqual(draft[key]['value'], 'TEST-ID')
        self.assertIn('NOT CONFIRMED', draft[key]['source'])
        with self.assertRaisesRegex(ValueError, 'unresolved'):
            r.project(data, [key], 'export')
        fact.update(status='VERIFIED', final_value='TEST-ID', evidence_scope='RADIO_MODULE',
                    authorization_route='certification')
        with self.assertRaisesRegex(ValueError, 'candidate'):
            r.project(data, [key], 'export')
        del fact['recommended_candidate']
        self.assertEqual(r.project(data, [key], 'export')[key]['value'], 'TEST-ID')

    def test_verified_fcc_needs_certification_and_scope(self):
        key = ('Safety&Compliance', 'FCC ID')
        data = self.ledger(key)
        data['facts'][0]['final_value'] = 'TEST-ID'
        with self.assertRaisesRegex(ValueError, 'certification'):
            r.project(data, [key], 'export')
        data['facts'][0].update(evidence_scope='HOST', authorization_route='certification', final_value='SDoC')
        with self.assertRaisesRegex(ValueError, 'identifier'):
            r.project(data, [key], 'export')

    def test_no_final_value_for_unresolved_and_no_formula(self):
        for changes in ({'status': 'TBD'}, {'final_value': '=1+1'}, {'final_value': None}, {'final_value': float('nan')}):
            data = self.ledger()
            data['facts'][0].update(changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                r.validate_ledger(data)

    def test_mapping_is_complete_unique_and_configuration_bound(self):
        for change in ('duplicate', 'missing', 'wrong_attribute', 'wrong_config', 'missing_basis'):
            data = self.ledger()
            if change == 'duplicate': data['fields'].append(copy.deepcopy(data['fields'][0]))
            if change == 'missing': data['fields'][0]['selected_fact'] = 'unknown'
            if change == 'wrong_attribute': data['facts'][0]['attribute'] = 'other'
            if change == 'wrong_config': data['facts'][0]['configurationId'] = 'BASE-B'
            if change == 'missing_basis': data['facts'][0].pop('transfer_basis')
            with self.subTest(change=change), self.assertRaises(ValueError):
                r.project(data, [('Product Details', 'RAM Memory Size')])
        with self.assertRaisesRegex(ValueError, 'exact current template'):
            r.project(self.ledger(), [])

    def test_unresolved_draft_allowed_and_na_is_blank(self):
        data = self.ledger()
        key = ('Product Details', 'RAM Memory Size')
        data['facts'][0].update(status='TBD', final_value=None)
        self.assertIsNone(r.project(data, [key])[key]['value'])
        with self.assertRaises(ValueError): r.project(data, [key], 'export')
        data['facts'][0]['status'] = 'NOT_APPLICABLE'
        self.assertIsNone(r.project(data, [key], 'export')[key]['value'])

    def test_schema_rejects_legacy_and_reports_without_dumping_values(self):
        with self.assertRaises(ValueError) as error:
            r.validate_ledger([{'private': 'DO-NOT-PRINT'}])
        self.assertNotIn('DO-NOT-PRINT', str(error.exception))

    def test_cli_checks_workbook_tampering_and_target_identity(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            book = openpyxl.load_workbook(r.ROOT/'assets/listing-workbook-template.xlsx')
            data = {'schemaVersion': 1, 'productId': 'TEST-PC', 'configurationId': 'BASE-A', 'facts': [], 'fields': []}
            for index, key in enumerate(r.workbook_fields(book)):
                fact = self.ledger(key)['facts'][0]
                fact.update(id=str(index), status='NOT_APPLICABLE', final_value=None)
                data['facts'].append(fact)
                data['fields'].append({'sheet': key[0], 'attribute': key[1], 'selected_fact': str(index)})
            for sheet in book:
                for col in range(2, sheet.max_column + 1):
                    sheet.cell(3, col).value = None
                    sheet.cell(4, col).value = 'NOT_APPLICABLE'
                    sheet.cell(5, col).value = 'Synthetic fixture'
            path = root/'review.xlsx'
            book.save(path)
            ledger = root/'ledger.json'
            ledger.write_text(json.dumps(data), encoding='utf-8')
            (root/'research-ledger.json').write_text(json.dumps(data), encoding='utf-8')
            command = [sys.executable, str(r.ROOT/'scripts/research_export.py'), '--ledger', str(ledger),
                       '--workbook', str(path), '--mode', 'export', '--product-id', 'TEST-PC', '--configuration-id', 'BASE-A']
            passed = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(passed.returncode, 0, passed.stderr)
            self.assertFalse(json.loads(passed.stdout)['amazonEligibilityAssessed'])
            wrong = command.copy(); wrong[-1] = 'BASE-B'
            self.assertNotEqual(subprocess.run(wrong, capture_output=True).returncode, 0)
            book['Product Details'].cell(3, 2).value = 'unreviewed edit'
            book.save(path); book.close()
            failed = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn('differs from scoped ledger', failed.stderr)


if __name__ == '__main__':
    unittest.main()
