"""Regressions for the eight follow-up findings; synthetic outputs only."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image
import test_research_export as ef
import test_workflow_hardening as gf
import gallery_engine as g
from listing_content import base_spec_fragments


class ExportRepairs(unittest.TestCase):
    def check(self,changes,identity=None):
        changes=dict(changes)
        if 'Resolution' in changes:
            # Positive panel scenarios now include explicit native-panel evidence.
            changes.setdefault('Native Resolution',changes['Resolution'])
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);helper=ef.ResearchExportTests();book,data,path,ledger=helper.full_fixture(root)
            for field,value in changes.items():
                sheet,attribute=field if isinstance(field,tuple) else ('Product Details',field)
                fact=next(f for f in data['facts'] if f['attribute']==attribute and f['sheet']==sheet)
                fact.update(status='VERIFIED',final_value=value)
                if attribute in {'Resolution','Native Resolution','Display Refresh Rate in Hertz'}:
                    fact.setdefault('evidence',{})['display_scope']='INTERNAL_PANEL'
                column=next(c.column for c in book[sheet][1] if c.value==attribute)
                book[sheet].cell(3,column).value=value
                book[sheet].cell(4,column).value='VERIFIED'
            book.save(path);book.close();ledger.write_text(json.dumps(data),encoding='utf-8')
            if identity:
                facts=json.loads((root/'product-facts.json').read_text());facts['identity'].update(identity)
                (root/'product-facts.json').write_text(json.dumps(facts),encoding='utf-8')
            return helper.export_run(ledger,path)

    def test_resolution_and_contract_are_text_fractional_refresh_is_valid(self):
        for resolution in ('1920 x 1080','1920×1080','1920x1080 pixels'):
            self.assertEqual(self.check({'Resolution':resolution,'Government Contract Name and Number':'NASA SEWP V, SYNTHETIC-CONTRACT',
                'Display Refresh Rate in Hertz':59.94})['result'],'EXPORT_EVIDENCE_CHECK_PASS')
        for bad in ('1920 x 0',True,'unknown',1920):
            with self.subTest(bad=bad),self.assertRaisesRegex(ValueError,'Resolution'):self.check({'Resolution':bad})
        with self.assertRaisesRegex(ValueError,'count'):self.check({'Total USB Ports':2.5})

    def test_frequency_units_are_field_specific(self):
        for field,unit in [('CPU Base Speed','CPU Base Speed Unit'),('CPU Model Speed Maximum','CPU Model Speed Maximum Unit'),('Memory Clock Speed','Memory Clock Speed Unit'),('Memory Speed','Memory Speed Unit')]:
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'unit'):self.check({field:1,unit:'MT/s'})
        self.assertEqual(self.check({'CPU Base Speed':1500,'CPU Base Speed Unit':'MHz','Memory Clock Speed':2.8,'Memory Clock Speed Unit':'GHz'})['result'],'EXPORT_EVIDENCE_CHECK_PASS')

    def test_explicit_numeric_rules_preserve_non_pc_sheet_checks(self):
        for field in ('Item Weight','Voltage',('Offer','Item Package Width'),('Safety&Compliance','Battery Weight')):
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'numeric'):self.check({field:True})

    def test_both_maximum_ram_aliases_must_agree_and_cover_installed(self):
        for value in (8,32,'32GB',True):
            with self.subTest(value=value),self.assertRaises(ValueError):self.check({'Ram Memory Maximum Size':value,'RAM Memory Maximum Size':64,'RAM Memory Maximum Size Unit':'GB'})
        for value in (64,'64GB','65536 MB'):
            self.assertEqual(self.check({'Ram Memory Maximum Size':value,'RAM Memory Maximum Size':64,'RAM Memory Maximum Size Unit':'GB'})['result'],'EXPORT_EVIDENCE_CHECK_PASS')
        with self.assertRaisesRegex(ValueError,'maximum'):self.check({'Ram Memory Maximum Size':'8GB'})

    def test_cpu_family_manufacturer_model_and_explicit_verified_alias(self):
        for field,value in [('CPU Model','AMD Ryzen 7'),('CPU Model Manufacturer','AMD'),('CPU Model Number','265')]:
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'CPU'):self.check({field:value})
        self.assertEqual(self.check({'CPU Model':'Intel(R) Core(TM) Ultra 7','CPU Model Manufacturer':'Intel'})['result'],'EXPORT_EVIDENCE_CHECK_PASS')
        self.assertEqual(self.check({'CPU Model':'Core Ultra 7 Series 2'},{'cpuFieldAliases':{'CPU Model':['Core Ultra 7 Series 2']}})['result'],'EXPORT_EVIDENCE_CHECK_PASS')

    def test_copy_capacities_match_base_in_common_forms_and_orders(self):
        template='MegaPC Custom Desktop Created Using Dell QCM1250 {} Win 11 Pro'
        for bad in ('64GB DDR5 Memory 1TB NVMe SSD','RAM: 64GB SSD: 1TB','64GB DDR5 1TB PCIe Gen4 NVMe SSD','16GB RAM 1TB M.2 2280 NVMe SSD'):
            with self.subTest(bad=bad),self.assertRaisesRegex(ValueError,'another RAM/SSD'):self.check({'Item Name':template.format(bad)})
        for good in ('16GB DDR5 Memory 256GB NVMe SSD','RAM: 16GB SSD: 256GB','16GB DDR5 256GB PCIe Gen4 NVMe SSD','16GB RAM 256GB M.2 2280 NVMe SSD'):
            self.assertEqual(self.check({'Item Name':template.format(good)})['result'],'EXPORT_EVIDENCE_CHECK_PASS')
        self.assertEqual(base_spec_fragments({'selectedBaseConfiguration':{'ramGB':16,'ssdGB':256}}),{'ram':'16GB RAM','ssd':'256GB SSD'})


class GalleryRepairs(unittest.TestCase):
    def test_deletion_cannot_become_research_including_removed_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'product generated photo/TEST';p.mkdir(parents=True)
            g.write(p/'delivery-status.json',{'galleryState':'LEGACY_QUARANTINED','currentQaPass':False})
            with self.assertRaisesRegex(ValueError,'no canonical images'):g.gate(root)
            for exists in (True,False):
                if not exists:shutil.rmtree(p)
                with patch.object(g.subprocess,'check_output',return_value='product generated photo/TEST/PT01.png\n'):
                    with self.assertRaisesRegex(ValueError,'deleted or renamed'):g.gate(root,'base','head')

    def test_real_git_rename_is_seen_as_canonical_deletion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'product generated photo/TEST';p.mkdir(parents=True)
            def git(*args):return subprocess.check_output(['git',*args],cwd=root,stderr=subprocess.DEVNULL).decode().strip()
            git('init');git('config','user.name','Synthetic');git('config','user.email','synthetic@localhost')
            (p/'PT01.png').write_bytes(b'synthetic bytes');git('add','.');git('commit','-m','base');base=git('rev-parse','HEAD')
            (p/'PT01.png').rename(p/'renamed.png');git('add','-A');git('commit','-m','rename')
            with self.assertRaisesRegex(ValueError,'deleted or renamed'):g.gate(root,base,'HEAD')

    def test_facts_style_and_review_only_changes_check_partial_qa(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'product generated photo/TEST';p.mkdir(parents=True)
            fixture=gf.GalleryBoundaries()
            try:
                fixture.build(p);fixture.reviews(p,['PT02.png'])
                g.write(p/'delivery-status.json',{'galleryState':'LEGACY_QUARANTINED','currentQaPass':False})
                g.accept(p,slots=['PT02.png'])
                originals={name:(p/name).read_bytes() for name in ('product-facts.json','style-lock.json','visual-review.json')}
                # Non-image commerce metadata does not invalidate image QA.
                facts=g.read(p/'product-facts.json');facts['offer']['price']=2;g.write(p/'product-facts.json',facts)
                with patch.object(g.subprocess,'check_output',return_value='product generated photo/TEST/product-facts.json\n'):
                    self.assertEqual(g.gate(root,'base','head')['partialUpdatesValidated'],1)
                for filename in originals:
                    for name,data in originals.items():(p/name).write_bytes(data)
                    record=g.read(p/filename)
                    if filename=='product-facts.json':record['selectedBaseConfiguration']['ramGB']=64
                    elif filename=='style-lock.json':record['status']='REVOKED'
                    else:record.pop('reviewInputsSha256')
                    g.write(p/filename,record)
                    with patch.object(g.subprocess,'check_output',return_value='product generated photo/TEST/'+filename+'\n'):
                        with self.assertRaises(ValueError):g.gate(root,'base','head')
            finally:fixture.doCleanups()

    def test_legacy_partial_reviews_are_reported_as_historical(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'product generated photo/TEST';p.mkdir(parents=True)
            (p/'PT01.png').write_bytes(b'legacy unchanged bytes')
            g.write(p/'delivery-status.json',{'galleryState':'LEGACY_QUARANTINED','deliveryScope':'PARTIAL_UPDATE','currentQaPass':False})
            g.write(p/'partial-update-qa.json',{'fullGalleryPass':False})
            result=g.gate(root)
            self.assertEqual(result['historicalPartialReviewsNotCurrent'],1)
            self.assertEqual(result['partialUpdatesValidated'],0)
            # Recording remote delivery does not manufacture a new visual review.
            with patch.object(g.subprocess,'check_output',return_value='product generated photo/TEST/delivery-status.json\n'):
                self.assertEqual(g.gate(root,'base','head')['historicalPartialReviewsNotCurrent'],1)
            with patch.object(g.subprocess,'check_output',return_value='product generated photo/TEST/product-facts.json\n'):
                with self.assertRaises((ValueError,FileNotFoundError)):g.gate(root,'base','head')

    def test_finalize_rolls_back_output_and_metadata_on_each_commit_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'gallery';p.mkdir();fixture=gf.GalleryBoundaries()
            try:
                logo=fixture.build(p);sheet=root/'contact.png';sheet.write_bytes(b'original contact')
                for name in ['PT01.png','PT02.png']:Image.new('RGB',(1600,900),'red').save(p/'unbranded'/name)
                watched=[p/n for n in g.NAMES]+[p/'unbranded'/n for n in g.PT]+[p/'logo-qa.json',sheet]
                before={path:path.read_bytes() for path in watched}
                original=os.replace
                for failure_target in (p/'PT02.png',p/'logo-qa.json',sheet):
                    def fail_once(src,dst,target=failure_target):
                        if Path(dst)==target:raise PermissionError('Synthetic destination lock')
                        return original(src,dst)
                    with patch.object(g.os,'replace',side_effect=fail_once):
                        with self.assertRaises(PermissionError):g.finalize(p,logo,'OEM',sheet,slots=['PT01.png','PT02.png'])
                    self.assertEqual(before,{path:path.read_bytes() for path in watched})
                    self.assertFalse(list(p.rglob('.listing-write-*')))
            finally:fixture.doCleanups()

    def test_transaction_removes_new_outputs_and_retains_backup_if_restore_locked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'source';source.write_bytes(b'new');first=root/'first';second=root/'second';second.write_bytes(b'old second')
            original=os.replace
            def fail_second(src,dst):
                if Path(dst)==second:raise PermissionError('Synthetic second lock')
                return original(src,dst)
            with patch.object(g.os,'replace',side_effect=fail_second):
                with self.assertRaises(PermissionError):g.commit_outputs([(source,first),(source,second)])
            self.assertFalse(first.exists());self.assertEqual(second.read_bytes(),b'old second')
            first.write_bytes(b'old first');calls=[]
            def fail_restore(src,dst):
                calls.append(Path(dst))
                if Path(dst)==second or calls.count(first)>1:raise PermissionError('Synthetic restore lock')
                return original(src,dst)
            with patch.object(g.os,'replace',side_effect=fail_restore):
                with self.assertRaisesRegex(OSError,'retained recovery backups'):g.commit_outputs([(source,first),(source,second)])
            self.assertIn(b'old first',[p.read_bytes() for p in root.glob('.listing-write-*')])


if __name__=='__main__':unittest.main()
