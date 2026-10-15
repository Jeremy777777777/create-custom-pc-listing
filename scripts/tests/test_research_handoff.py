"""Product-directory, storage-scope and coverage-delivery regressions using scratch data."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import test_research_export as ef
from research_handoff import check_product_location,coverage_summary,internal_storage_total
import research_export as r

spec=importlib.util.spec_from_file_location('checks_handoff',r.ROOT/'scripts/check-workbooks.py')
checks=importlib.util.module_from_spec(spec);spec.loader.exec_module(checks)


class HandoffTests(unittest.TestCase):
    def test_canonical_directory_matches_ledger_and_facts_without_restricting_scratch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'product generated photo/WRONG';p.mkdir(parents=True)
            helper=ef.ResearchExportTests();book,data,path,ledger=helper.full_fixture(p);book.close()
            ledger.rename(p/'research-ledger.json')
            for fn in (lambda:checks.check_output(path,checks.template_topology(r.ROOT/'assets/listing-workbook-template.xlsx')),
                       lambda:helper.export_run(p/'research-ledger.json',path)):
                with self.assertRaisesRegex(ValueError,'product directory'):fn()
            p=p.rename(p.with_name('TEST-PC'));path=p/path.name
            self.assertEqual(helper.export_run(p/'research-ledger.json',path)['result'],'EXPORT_EVIDENCE_CHECK_PASS')
            facts=json.loads((p/'product-facts.json').read_text());facts['identity']['internalId']='OTHER'
            (p/'product-facts.json').write_text(json.dumps(facts))
            with self.assertRaisesRegex(ValueError,'identity differs'):
                checks.check_output(path,checks.template_topology(r.ROOT/'assets/listing-workbook-template.xlsx'))
            check_product_location(root/'scratch/review.xlsx','TEST-PC')

    def fixture(self,root,capacity=512,components=False,unit='GB'):
        helper=ef.ResearchExportTests();book,data,path,ledger=helper.full_fixture(root)
        for field,value in [('Memory Storage Capacity',capacity),('Memory Storage Capacity Unit',unit)]:
            fact=next(f for f in data['facts'] if f['attribute']==field and f['sheet']=='Product Details')
            fact.update(status='VERIFIED',final_value=value)
        if components:
            base=next(f for f in data['facts'] if f['attribute']=='Hard Disk Size')
            extra=copy.deepcopy(base);extra.update(id='secondary',attribute='Secondary internal drive capacity',final_value=256,
                evidence={'capacity_unit':'GB','storage_medium':'INTERNAL_SSD'})
            data['facts'].append(extra)
            total=next(f for f in data['facts'] if f['attribute']=='Memory Storage Capacity')
            total['evidence']={'storage_scope':'INTERNAL_TOTAL','storage_component_fact_ids':[base['id'],'secondary']}
        projected=r.project(data,r.workbook_fields(book))
        for sheet in book:
            for col in range(2,sheet.max_column+1):
                record=projected[(sheet.title,sheet.cell(1,col).value)]
                for row,key in ((3,'value'),(4,'status'),(5,'source')):sheet.cell(row,col).value=record[key]
        book.save(path);book.close();ledger.write_text(json.dumps(data))
        return helper,data,path,ledger

    def test_storage_alias_unit_conversion_and_mismatch(self):
        for capacity,unit,valid in ((256,'GB',True),(.25,'TB',True),(512,'GB',False)):
            with tempfile.TemporaryDirectory() as tmp:
                helper,data,path,ledger=self.fixture(Path(tmp),capacity,unit=unit)
                if valid:self.assertEqual(helper.export_run(ledger,path)['result'],'EXPORT_EVIDENCE_CHECK_PASS')
                else:
                    with self.assertRaisesRegex(ValueError,'storage capacity fields disagree'):helper.export_run(ledger,path)

    def test_explicit_internal_component_total_and_bad_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            helper,data,path,ledger=self.fixture(Path(tmp),components=True)
            self.assertEqual(helper.export_run(ledger,path)['result'],'EXPORT_EVIDENCE_CHECK_PASS')
            original=copy.deepcopy(data)
            for change in ('external','factory','wrong_config','duplicate','missing_base','wrong_total'):
                altered=copy.deepcopy(original);extra=altered['facts'][-1]
                total=next(f for f in altered['facts'] if f['attribute']=='Memory Storage Capacity')
                if change=='external':extra['evidence']['storage_medium']='EXTERNAL_USB'
                if change=='factory':extra['fact_scope']='FACTORY'
                if change=='wrong_config':extra['configurationId']='OTHER'
                if change=='duplicate':total['evidence']['storage_component_fact_ids'].append('secondary')
                if change=='missing_base':total['evidence']['storage_component_fact_ids']=['secondary']
                if change=='wrong_total':extra['final_value']=128
                if change=='wrong_total':
                    self.assertEqual(internal_storage_total(altered),384)
                    # A changed component basis cannot validate the unchanged 512GB workbook.
                    ledger.write_text(json.dumps(altered))
                    with self.assertRaisesRegex(ValueError,'storage capacity fields disagree'):helper.export_run(ledger,path)
                else:
                    with self.subTest(change=change),self.assertRaises(ValueError):internal_storage_total(altered)

    def test_coverage_counts_followups_and_cli_sidecar(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);helper=ef.ResearchExportTests();book,data,path,ledger=helper.full_fixture(root,copy_present=False)
            fact=data['facts'][0];fact.update(status='TBD',final_value=None,source='SELLER_INPUT_REQUIRED: target SKU',
                evidence={'reason':'Need seller SKU','next_action':'Confirm in ERP','owner':'Seller'})
            key=(fact['sheet'],fact['attribute']);col=next(c.column for c in book[key[0]][1] if c.value==key[1])
            book[key[0]].cell(4,col).value='TBD';book[key[0]].cell(5,col).value=fact['source']
            book.save(path);book.close();ledger.write_text(json.dumps(data))
            report=r.run(r.ROOT/'assets/listing-workbook-template.xlsx',ledger,path,'draft')
            summary=report['coverageSummary']
            self.assertEqual(sum(s['total'] for s in summary['sheets'].values()),len(data['fields']))
            self.assertEqual(summary['unresolvedFields'][0]['owner'],'Seller')
            self.assertEqual(summary['missingFollowUpMetadata'],[])
            del fact['evidence']['owner']
            missing=coverage_summary(data,r.project(data,[(f['sheet'],f['attribute']) for f in data['fields']]))
            self.assertEqual(missing['missingFollowUpMetadata'][0]['missing'],['owner'])
            output=root/'review.research-summary.json'
            cmd=[sys.executable,str(r.ROOT/'scripts/research_export.py'),'--ledger',str(ledger),'--workbook',str(path),'--summary-output',str(output)]
            subprocess.run(cmd,check=True,capture_output=True)
            saved=json.loads(output.read_text());self.assertEqual(saved['artifactRole'],'RESEARCH_COVERAGE_SUMMARY')
            self.assertEqual(saved['ledgerSha256'],report['ledgerSha256'])
            output.write_text('{"artifactRole":"OTHER"}');before=output.read_bytes()
            result=subprocess.run(cmd,capture_output=True)
            self.assertNotEqual(result.returncode,0);self.assertEqual(output.read_bytes(),before)


if __name__=='__main__':unittest.main()
