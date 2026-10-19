"""Serial lookup outcome, evidence linkage, delivery and legacy regressions."""
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import test_research_export as fixtures
import research_export as r
from serial_research import validate_serial_research, serial_research_summary, check_serial_research_delivery


class SerialResearchTests(unittest.TestCase):
    def data(self):
        data = fixtures.ResearchExportTests().ledger()
        data['serial_research'] = {
            'workflow_mode': 'FULL_LISTING_WORKFLOW', 'outcome': 'SERIAL_NOT_FOUND',
            'reason': 'Synthetic linked current and historical ERP records contain no serial',
            'reviewed_date': '2026-10-14', 'sources_attempted': ['Synthetic target inventory/receipt lookup'],
            'units': [], 'resolved_fact_ids': [], 'factory_sold_differences': [],
            'unresolved_fields': ['Factory RAM'], 'reconciliation': '',
            'next_action': 'Obtain a linked receipt or unit label', 'owner': 'Synthetic researcher'}
        return data

    def completed(self):
        data = self.data()
        factory = copy.deepcopy(data['facts'][0])
        factory.update(id='factory', fact_scope='FACTORY', final_value=16,
                       evidence={'unit_evidence_alias': 'UNIT-A'})
        data['facts'].append(factory)
        data['serial_research'].update(
            outcome='COMPLETED', units=[{
                'unit_evidence_alias': 'UNIT-A', 'serial_source_kind': 'HISTORICAL',
                'erp_record_reference': 'Synthetic receipt reference', 'target_configuration': 'BASE-A',
                'batch_match_basis': 'Synthetic exact SKU/batch link', 'returned_model': 'Synthetic model',
                'oem_configuration_source': 'https://example.com/support/model/parts', 'fact_ids': ['factory']}],
            resolved_fact_ids=['factory'], factory_sold_differences=['Factory 16GB; sold 32GB per assembly record'],
            unresolved_fields=[], reconciliation='Historical unit factory RAM differs from independently documented sold assembly.')
        return data

    def test_failure_is_deliverable_but_missing_attempts_or_followup_is_rejected(self):
        data = self.data()
        self.assertEqual(validate_serial_research(data, required=True, full_research=True)['outcome'], 'SERIAL_NOT_FOUND')
        for key in ('sources_attempted', 'owner', 'next_action', 'reviewed_date'):
            changed = copy.deepcopy(data)
            changed['serial_research'][key] = [] if key == 'sources_attempted' else ''
            with self.subTest(key=key), self.assertRaises(ValueError):
                r.validate_ledger(changed)
        for outcome in ('ERP_TARGET_NOT_FOUND', 'ERP_UNAVAILABLE', 'OEM_UNAVAILABLE', 'OEM_NO_BOM'):
            data['serial_research']['outcome'] = outcome
            self.assertEqual(validate_serial_research(data, required=True)['outcome'], outcome)

    def test_legacy_is_explicitly_unassessed_not_completed(self):
        data = fixtures.ResearchExportTests().ledger()
        self.assertEqual(serial_research_summary(data)['outcome'], 'NOT_ASSESSED_LEGACY')
        with self.assertRaisesRegex(ValueError, 'serial_research required'):
            validate_serial_research(data, required=True)
        data = self.data(); data['serial_research']['outcome'] = 'NOT_ASSESSED_LEGACY'
        with self.assertRaisesRegex(ValueError, 'Legacy'):
            validate_serial_research(data, required=True)

    def test_full_research_cannot_claim_image_exemption(self):
        data = self.data(); record = data['serial_research']
        record.update(outcome='NOT_REQUIRED', workflow_mode='IMAGE_ADJUSTMENT_WORKFLOW',
                      reason='Existing verified facts sufficient for local image adjustment', sources_attempted=[], unresolved_fields=[])
        validate_serial_research(data, required=True)
        with self.assertRaisesRegex(ValueError, 'FULL_LISTING_WORKFLOW'):
            validate_serial_research(data, required=True, full_research=True)
        record['workflow_mode'] = 'FULL_LISTING_WORKFLOW'
        with self.assertRaisesRegex(ValueError, 'NOT_REQUIRED'):
            validate_serial_research(data)

    def test_completed_chain_preserves_historical_factory_scope_and_sold_value(self):
        data = self.completed(); r.validate_ledger(data)
        self.assertEqual(r.project(data, [('Product Details', 'RAM Memory Installed')], 'export')[('Product Details', 'RAM Memory Installed')]['value'], 32)
        summary = serial_research_summary(data)
        self.assertEqual(summary['units'][0]['serial_source_kind'], 'HISTORICAL')
        self.assertEqual(summary['resolvedAttributes'][0]['attribute'], 'RAM Memory Installed')
        self.assertEqual(summary['evidenceKinds'], ['HISTORICAL'])
        self.assertFalse(summary['factualReadinessAssessed'])
        for alteration in ('missing_fact', 'sold_fact', 'wrong_alias', 'wrong_configuration', 'unverified_fact', 'no_reconciliation'):
            changed = copy.deepcopy(data); record = changed['serial_research']; unit = record['units'][0]
            if alteration == 'missing_fact': unit['fact_ids'] = ['missing']
            if alteration == 'sold_fact': unit['fact_ids'] = ['sold']
            if alteration == 'wrong_alias': changed['facts'][-1]['evidence']['unit_evidence_alias'] = 'UNIT-B'
            if alteration == 'wrong_configuration': unit['target_configuration'] = 'OTHER'
            if alteration == 'unverified_fact': changed['facts'][-1].update(status='TBD', final_value=None)
            if alteration == 'no_reconciliation': record['reconciliation'] = ''
            with self.subTest(alteration=alteration), self.assertRaises(ValueError):
                r.validate_ledger(changed)

    def test_failure_cannot_claim_resolved_facts_and_sources_are_sanitized(self):
        data = self.completed()
        for url in ('http://example.com/parts', 'https://example.com/parts?serial=PRIVATE',
                    'https://example.com/servicetag/PRIVATE/parts', 'https://example.com/parts#PRIVATE'):
            data['serial_research']['units'][0]['oem_configuration_source'] = url
            with self.subTest(url=url), self.assertRaises(ValueError) as error:
                r.validate_ledger(data)
            self.assertNotIn('PRIVATE', str(error.exception))
        data = self.completed(); data['serial_research']['outcome'] = 'OEM_NO_BOM'
        with self.assertRaisesRegex(ValueError, 'cannot claim'):
            r.validate_ledger(data)

    def test_new_writer_and_export_reject_missing_record_without_creating_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); helper = fixtures.ResearchExportTests()
            book, data, path, ledger = helper.full_fixture(root); book.close()
            del data['serial_research']; ledger.write_text(json.dumps(data))
            output = root/'new.xlsx'
            with self.assertRaisesRegex(ValueError, 'serial_research required'):
                r.write_workbook(r.ROOT/'assets/listing-workbook-template.xlsx', ledger, output)
            self.assertFalse(output.exists())
            with self.assertRaisesRegex(ValueError, 'serial_research required'):
                helper.export_run(ledger, path)
            self.assertEqual(r.run(r.ROOT/'assets/listing-workbook-template.xlsx', ledger, path, 'draft')['coverageSummary']['serialResearch']['outcome'], 'NOT_ASSESSED_LEGACY')

    def test_legacy_summary_remains_readable_but_new_summary_cannot_hide_missing_record(self):
        import shutil
        from research_handoff import check_research_summaries
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); product = root/'product generated photo/TEST-PC'; product.mkdir(parents=True)
            (root/'assets').mkdir()
            shutil.copyfile(r.ROOT/'assets/listing-workbook-template.xlsx', root/'assets/listing-workbook-template.xlsx')
            book, data, path, ledger = fixtures.ResearchExportTests().full_fixture(product); book.close()
            ledger = ledger.rename(product/'research-ledger.json')
            del data['serial_research']; ledger.write_text(json.dumps(data))
            result = r.run(r.ROOT/'assets/listing-workbook-template.xlsx', ledger, path, 'draft')
            output = product/'old.research-summary.json'
            with self.assertRaisesRegex(ValueError, 'serial_research'):
                r.write_summary(output, result, path)
            self.assertFalse(output.exists())
            old = {key:result[key] for key in ('productId','configurationId','stage','workbookSha256','ledgerSha256','templateSha256','productFactsSha256','coverageSummary')}
            old = copy.deepcopy(old); del old['coverageSummary']['serialResearch']
            old.update(artifactRole='RESEARCH_COVERAGE_SUMMARY', workbookFile=path.name)
            output.write_text(json.dumps(old)); self.assertEqual(check_research_summaries(root), 1)
            data['serial_research'] = self.data()['serial_research']; ledger.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, 'stale'):
                check_research_summaries(root)

    def test_git_delivery_requires_new_records_and_reads_target_revision(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            def git(*args):
                return subprocess.run(['git', *args], cwd=root, capture_output=True, check=True).stdout.decode().strip()
            git('init'); git('config', 'user.name', 'Synthetic'); git('config', 'user.email', 'test@example.com')
            product = root/'product generated photo/TEST-PC'; product.mkdir(parents=True)
            ledger = product/'research-ledger.json'
            old = fixtures.ResearchExportTests().ledger(); ledger.write_text(json.dumps(old))
            git('add', '.'); git('commit', '-m', 'legacy'); base = git('rev-parse', 'HEAD')
            self.assertEqual(check_serial_research_delivery(root)['legacyNotAssessed'], ['TEST-PC'])
            old['facts'][0]['source'] = 'Changed research'; ledger.write_text(json.dumps(old))
            with self.assertRaisesRegex(ValueError, 'serial_research required'):
                check_serial_research_delivery(root)
            ledger.write_text(json.dumps(self.data())); git('add', '.'); git('commit', '-m', 'record attempt')
            head = git('rev-parse', 'HEAD')
            ledger.write_text(json.dumps(old))  # Worktree must not override explicit HEAD-side validation.
            self.assertEqual(check_serial_research_delivery(root, base, head)['recordedOutcomes']['TEST-PC'], 'SERIAL_NOT_FOUND')
            ledger.write_text(json.dumps(self.data()))
            ledger.unlink()
            with self.assertRaisesRegex(ValueError, 'requires a scoped ledger'):
                (product/'new.xlsx').write_bytes(b'synthetic')
                check_serial_research_delivery(root)


if __name__ == '__main__':
    unittest.main()
