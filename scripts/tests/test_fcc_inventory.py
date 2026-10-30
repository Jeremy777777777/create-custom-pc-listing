"""Synthetic coverage for standalone FCC routing and private inventory plans."""
import copy
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import fcc_inventory as f
import research_export as r
from research_audit import validate as audit
import test_research_export as fixtures


class InventoryTests(unittest.TestCase):
    def record(self):
        return dict(workflow_mode='FCC_LOOKUP_ONLY', explicit_task=True,
                    internal_id='TEST-PC', search_trace='Synthetic dated OEM and grant chain; unit scope',
                    outcome='MODEL_MODULE_MATCH', candidate_id='TEST-MODULE-ID',
                    candidate_basis='Synthetic exact module record', missing_confirmation='Current installation',
                    candidate_confidence='MEDIUM', scope='Synthetic unit only',
                    used_serial_numbers=['SYNTHETIC-SN', 'SYNTHETIC-SN'])

    def test_candidate_does_not_become_confirmed(self):
        plan=f.inventory_update(self.record())
        self.assertEqual(plan['updates']['FCC ID（已确认）'], '')
        self.assertEqual(plan['updates']['FCC ID 候选'], 'TEST-MODULE-ID')
        self.assertEqual(plan['updates']['使用过的 Serial Number'], 'SYNTHETIC-SN')
        self.assertFalse(plan['listing_workbook_write'])
        self.assertFalse(plan['marketplace_export_authorized'])

    def test_rejects_implicit_lookup_and_unsupported_promotion(self):
        for mutation in ({'explicit_task':False}, {'workflow_mode':'FULL_LISTING_WORKFLOW'},
                         {'confirmed_id':'TEST-MODULE-ID'}, {'scope':''},
                         {'candidate_confidence':90}, {'outcome':'FACTORY_NO_WLAN'},
                         {'outcome':'HOST_SDOC'}, {'missing_confirmation':''}):
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                f.inventory_update({**self.record(), **mutation})

    def test_scoped_confirmation_and_unresolved_result(self):
        record=self.record()
        record.update(outcome='UNIT_CONFIRMED', candidate_id=None, confirmed_id='TEST-MODULE-ID',
                      confirmation_basis='Synthetic exact unit label and grant')
        self.assertEqual(f.inventory_update(record)['updates']['FCC ID（已确认）'], 'TEST-MODULE-ID')
        record.update(outcome='PENDING', confirmed_id=None)
        self.assertEqual(f.inventory_update(record)['updates']['FCC ID 候选'], '')

    def test_listing_projection_has_no_fcc_result_or_lookup_requirement(self):
        data=fixtures.ResearchExportTests().ledger(f.FCC_KEY)
        data['fcc_management']=f.EXTERNAL_MODE
        data['facts'][0].update(status='TBD',final_value=None,source=f.DISPOSITION)
        self.assertEqual(audit(data,required=True)['missingFields'], 0)
        for mode in ('draft','export'):
            field=r.project(data,[f.FCC_KEY],mode)[f.FCC_KEY]
            self.assertIsNone(field['value'])
            self.assertIsNone(field['value_candidate'])
            self.assertEqual(field['status'],'TBD')
        for mutation in ({'evidence':{'lookup_outcome':'PENDING'}},
                         {'recommended_candidate':'TEST-MODULE-ID'}, {'source':'Invented approval'}):
            changed=copy.deepcopy(data);changed['facts'][0].update(mutation)
            with self.assertRaises(ValueError):r.project(changed,[f.FCC_KEY])

    def test_other_fields_keep_existing_export_checks(self):
        data=fixtures.ResearchExportTests().ledger()
        data['fcc_management']=f.EXTERNAL_MODE
        data['facts'][0].update(status='TBD',final_value=None)
        with self.assertRaisesRegex(ValueError,'unresolved field'):
            r.project(data,[('Product Details','RAM Memory Installed')],'export')

    def test_saved_workbook_contains_only_neutral_fcc_handoff(self):
        from test_fcc_guide_writer import FCCGuideWriterTests
        from reference_fixtures import write_audit
        import openpyxl
        with tempfile.TemporaryDirectory() as scratch:
            root=Path(scratch)
            data,fact,previous,ledger=FCCGuideWriterTests().fixture(root)
            data['fcc_management']=f.EXTERNAL_MODE
            data['candidate_coverage_version']=2
            for key in ('evidence','recommended_candidate','evidence_scope','authorization_route'):
                fact.pop(key,None)
            fact.update(status='TBD',final_value=None,source=f.DISPOSITION)
            ledger.write_text(json.dumps(data),encoding='utf-8');write_audit(ledger)
            output=root/'external.xlsx'
            from test_release_checks import trace_for
            for item in data['facts']:
                if not f.is_external_field(data,item):
                    item.setdefault('evidence',{})['research_trace']=trace_for(item)
            ledger.write_text(json.dumps(data),encoding='utf-8');write_audit(ledger)
            stdout=io.StringIO()
            with patch.object(sys,'argv',['research_export','--ledger',str(ledger),
                              '--workbook',str(output),'--write-workbook']), contextlib.redirect_stdout(stdout):
                r.main()
            result=json.loads(stdout.getvalue())
            self.assertFalse(result['fccPublicationAssessed'])
            book=openpyxl.load_workbook(output)
            sheet=book[f.FCC_KEY[0]]
            column=next(c.column for c in sheet[1] if c.value==f.FCC_KEY[1])
            self.assertEqual([sheet.cell(row,column).value for row in (3,4,5,6,7)],
                             [None,'TBD',f.DISPOSITION,None,None])
            book.close()

    def test_new_cli_does_not_silently_use_legacy_fcc_workflow(self):
        with tempfile.TemporaryDirectory() as scratch:
            root=Path(scratch);ledger=root/'ledger.json';output=root/'out.xlsx'
            ledger.write_text(json.dumps(fixtures.ResearchExportTests().ledger()),encoding='utf-8')
            stderr=io.StringIO()
            with patch.object(sys,'argv',['research_export','--ledger',str(ledger),
                              '--workbook',str(output),'--write-workbook']), contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                r.main()
            self.assertIn('FCC lookup is a separate task',stderr.getvalue())
            self.assertFalse(output.exists())


if __name__=='__main__':unittest.main()
