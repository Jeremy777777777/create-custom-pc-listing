"""Synthetic adversarial cases; no real product facts or approvals are changed."""
import copy
import io
import contextlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
from unittest.mock import patch
from datetime import datetime, timezone

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import production_guard as guard
import delivery_privacy as privacy
import drive_delivery as drive
import gallery_engine as gallery
import research_export as export
import test_workflow_hardening as gallery_fixtures
import test_research_export as research_fixtures
import test_release_checks as release_fixtures
import test_production_revision as revision_fixtures
import research_audit as audit


class AuditRegressions(unittest.TestCase):
    def test_xlsx_exponent_serial_is_detected_without_echo(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'review.xlsx'
            with zipfile.ZipFile(path,'w') as archive:
                archive.writestr('xl/worksheets/sheet1.xml',
                    '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData><row><c r="A1"><v>1.234567890123e12</v></c></row></sheetData></worksheet>')
            result=privacy.screen_file(path,known_private_values=['1234567890123'],serials_used=True)
            self.assertEqual(result['state'],'PRIVATE_CONTENT_DETECTED')
            self.assertNotIn('1234567890123',json.dumps(result))
            self.assertNotIn('1.234567890123',json.dumps(result))

    def test_readback_in_future_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            p,plan,remote,destinations,context=release_fixtures.ReleaseChecks().delivery(Path(temp))
            remote['files'][0]['readBackAtUtc']='2099-01-01T00:00:00Z'
            with self.assertRaisesRegex(ValueError,'non-future'):
                drive.verify(p,plan,remote,destinations,context)

    def test_research_draft_binds_existing_identity_without_full_fact_requirement(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); book,data,workbook,ledger=research_fixtures.ResearchExportTests().full_fixture(root)
            book.close()
            facts=root/'product-facts.json'
            original=json.loads(facts.read_text())
            result=export.run(export.ROOT/'assets/listing-workbook-template.xlsx',ledger,workbook,'draft',stage='RESEARCH_REVIEW')
            self.assertEqual(result['productFactsSha256'],guard.sha(facts))
            original['selectedBaseConfiguration']['id']='OTHER-CONFIG'
            facts.write_text(json.dumps(original))
            with self.assertRaisesRegex(ValueError,'identity/configuration'):
                export.run(export.ROOT/'assets/listing-workbook-template.xlsx',ledger,workbook,'draft',stage='RESEARCH_REVIEW')
            facts.write_text(json.dumps({'identity':{'internalId':'TEST-PC'},'selectedBaseConfiguration':{'id':'BASE-A'}}))
            export.run(export.ROOT/'assets/listing-workbook-template.xlsx',ledger,workbook,'draft',stage='RESEARCH_REVIEW')

    def test_listing_draft_checks_copy_without_forcing_unresolved_research_to_export(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); book,data,workbook,ledger=research_fixtures.ResearchExportTests().full_fixture(root)
            fact=next(f for f in data['facts'] if f['sheet']=='Safety&Compliance' and f['attribute']=='FCC ID')
            fact.update(status='TBD',final_value=None)
            column=next(c.column for c in book['Safety&Compliance'][1] if c.value=='FCC ID')
            book['Safety&Compliance'].cell(3,column).value=None
            book['Safety&Compliance'].cell(4,column).value='TBD'
            book.save(workbook);ledger.write_text(json.dumps(data))
            export.run(export.ROOT/'assets/listing-workbook-template.xlsx',ledger,workbook,'draft',
                       stage='LISTING_DRAFT',check_copy=True)
            title=next(f for f in data['facts'] if f['attribute']=='Item Name')
            title['final_value']='An invented unsupported title'
            column=next(c.column for c in book['Product Details'][1] if c.value=='Item Name')
            book['Product Details'].cell(3,column).value=title['final_value']
            book.save(workbook);book.close();ledger.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                export.run(export.ROOT/'assets/listing-workbook-template.xlsx',ledger,workbook,'draft',stage='LISTING_DRAFT',check_copy=True)

    def test_full_inventory_tamper_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp); helper=gallery_fixtures.GalleryBoundaries(); self.addCleanup(helper.doCleanups)
            helper.build(p); helper.reviews(p)
            report=gallery.read(p/'semantic-review.json')
            report['galleryInventorySha256']['MAIN.png']='0'*64
            gallery.write(p/'semantic-review.json',report)
            with self.assertRaisesRegex(ValueError,'inventory|gallery bytes'):
                gallery.accept(p)

    def test_healthy_partial_preserves_unchanged_review_and_repeated_updates(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp); helper=gallery_fixtures.GalleryBoundaries(); self.addCleanup(helper.doCleanups)
            helper.build(p); helper.reviews(p)
            gallery.write(p/'delivery-status.json',{'galleryState':'CURRENT_REVIEWED'})
            gallery.accept(p)
            for slots in (['PT08.png'],['PT07.png']):
                helper.reviews(p,slots); gallery.accept(p,slots=slots)
                report=gallery.read(p/'partial-update-qa.json')
                self.assertFalse(report['retainedLegacyGallery'])
                self.assertFalse(report['fullGalleryPass'])
                self.assertEqual(report['retainedReviewState'],'VERIFIED_UNCHANGED')
                self.assertEqual(gallery.read(p/'delivery-status.json')['galleryState'],'SCOPED_REVIEWED')
                gallery.validate_partial(p,slots)
            facts=gallery.read(p/'product-facts.json'); facts['selectedBaseConfiguration']['ramGB']=64
            gallery.write(p/'product-facts.json',facts)
            helper.reviews(p,['PT07.png'])
            with self.assertRaisesRegex(ValueError,'Retained review evidence stale'):
                gallery.validate_partial(p,['PT07.png'])


class ProductionScope(unittest.TestCase):
    def test_real_research_workbook_and_bound_summary_pass_then_tamper_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);p=root/'TEST-PC';p.mkdir()
            book,data,workbook,ledger=research_fixtures.ResearchExportTests().full_fixture(p);book.close()
            ledger.rename(p/'research-ledger.json');ledger=p/'research-ledger.json'
            result=export.run(export.ROOT/'assets/listing-workbook-template.xlsx',ledger,workbook,'draft',stage='RESEARCH_REVIEW')
            raw,reuse=revision_fixtures.reuse_review(data,data)
            result['researchTrace']=audit.validate(data,True,raw,reuse)
            summary=workbook.with_suffix('.research-summary.json');export.write_summary(summary,result,workbook,ledger)
            request={'mode':'FULL_LISTING_WORKFLOW','configurationId':'BASE-A','runId':'RESEARCH-STAGE',
                     'requestReference':'Synthetic research-only stage','allowedChanges':[workbook.name,summary.name],
                     'outputs':{workbook.name:'RESEARCH',summary.name:'RESEARCH'},'selectedSlots':[]}
            # Sidecar is QA; the original workbook is the RESEARCH deliverable.
            request['outputs'][summary.name]='QA'
            with patch.object(guard,'workflow',return_value='a'*40):
                contract=guard.capture(p,request);path=root/'contract.json';gallery.write(path,contract)
                checked=guard.verify(p,path,guard.sha(path))
                self.assertEqual(checked['checks'][workbook.name]['state'],'DRAFT_PROJECTION_PASS')
                plan_path=root/'upload-plan.json'
                args=['drive_delivery','plan','--product',str(p),'--run-id','RESEARCH-STAGE',
                      '--file',workbook.name,'--production-contract',str(path),'--contract-sha256',guard.sha(path),
                      '--output',str(plan_path)]
                with patch.object(sys,'argv',args),contextlib.redirect_stdout(io.StringIO()): drive.main()
                self.assertEqual(json.loads(plan_path.read_text())['productionScope']['contractSha256'],guard.sha(path))
                stale=json.loads(summary.read_text());stale['productFactsSha256']='0'*64
                gallery.write(summary,stale)
                with self.assertRaisesRegex(ValueError,'summary stale'):guard.verify(p,path,guard.sha(path))

    def fixture(self,root):
        p=root/'TEST-PC';p.mkdir()
        gallery.write(p/'product-facts.json',{'identity':{'internalId':'TEST-PC'},'selectedBaseConfiguration':{'id':'BASE-A'}})
        gallery.write(p/'style-lock.json',{'status':'APPROVED'})
        (p/'PT08.png').write_bytes(b'synthetic old image')
        (p/'PT07.png').write_bytes(b'synthetic retained image')
        (p/'retained.xlsx').write_bytes(b'unchanged existing workbook')
        request={'mode':'IMAGE_ADJUSTMENT_WORKFLOW','configurationId':'BASE-A','runId':'TEST-RUN',
                 'requestReference':'Synthetic user request','allowedChanges':['PT08.png'],
                 'outputs':{'PT08.png':'IMAGE'},'selectedSlots':['PT08.png'],
                 'styleApproval':{'userReference':'Synthetic explicit user approval','styleLockSha256':guard.sha(p/'style-lock.json')}}
        with patch.object(guard,'workflow',return_value='a'*40): contract=guard.capture(p,request)
        return p,contract

    def test_scope_rejects_unrequested_mutation_addition_deletion(self):
        for name,action in [('PT07.png','edit'),('extra.txt','edit'),('retained.xlsx','delete')]:
            with self.subTest(name=name),tempfile.TemporaryDirectory() as temp:
                p,c=self.fixture(Path(temp))
                if action=='edit': (p/name).write_bytes(b'outside request')
                else: (p/name).unlink()
                with self.assertRaises(ValueError): guard.check_scope(p,c)

    def test_approved_single_slot_passes_scope_but_cannot_self_certify_image_quality(self):
        with tempfile.TemporaryDirectory() as temp:
            p,c=self.fixture(Path(temp)); (p/'PT08.png').write_bytes(b'not an actual image')
            self.assertEqual(guard.check_scope(p,c)[1],['PT08.png'])
            path=Path(temp)/'contract.json';gallery.write(path,c)
            with patch.object(guard,'workflow',return_value='a'*40),self.assertRaises((ValueError,FileNotFoundError)):
                guard.verify(p,path,guard.sha(path))

    def test_invalid_mode_scope_identity_and_style_are_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            p,c=self.fixture(Path(temp))
            for update in ({'mode':'UNKNOWN'},{'allowedChanges':['../x']},
                           {'allowedChanges':['PT08.png','PT07.png']},{'allowedChanges':['retained.xlsx']},
                           {'mode':'IMAGE_ONLY_WORKFLOW'},{'mode':'CONCEPT_ONLY'},
                           {'outputs':{'retained.xlsx':'SOURCE'}},{'configurationId':'OTHER'},
                           {'styleApproval':{}}):
                with self.subTest(update=update),self.assertRaises(ValueError):
                    guard.check_scope(p,{**c,**update})
            gallery.write(p/'style-lock.json',{'status':'APPROVED','different':'style'})
            with self.assertRaises(ValueError): guard.check_scope(p,c)

    def test_pinned_contract_and_workflow_cannot_change(self):
        with tempfile.TemporaryDirectory() as temp:
            p,c=self.fixture(Path(temp)); path=Path(temp)/'contract.json'; gallery.write(path,c); digest=guard.sha(path)
            with patch.object(guard,'workflow',return_value='b'*40),self.assertRaisesRegex(ValueError,'Workflow revision'):
                guard.verify(p,path,digest)
            c['allowedChanges'].append('PT07.png');gallery.write(path,c)
            with self.assertRaisesRegex(ValueError,'contract changed'): guard.verify(p,path,digest)

    def test_concept_check_cannot_become_publication_or_final_image_pass(self):
        with tempfile.TemporaryDirectory() as temp:
            p,c=self.fixture(Path(temp))
            c.update(mode='CONCEPT_ONLY',selectedSlots=[],outputs={'preview.txt':'CONCEPT'},allowedChanges=['preview.txt'])
            (p/'preview.txt').write_text('synthetic concept')
            path=Path(temp)/'contract.json';gallery.write(path,c)
            with patch.object(guard,'workflow',return_value='a'*40): result=guard.verify(p,path,guard.sha(path))
            self.assertEqual(result['publicationStatus'],'NOT_AUTHORIZED_BY_THIS_CHECK')
            self.assertEqual(result['checks'],{})
            with patch.object(guard,'workflow',return_value='a'*40),self.assertRaisesRegex(ValueError,'exceeds'):
                guard.verify(p,path,guard.sha(path),['PT07.png'])


if __name__=='__main__': unittest.main()
