"""Boundary regressions use synthetic fixtures, never actual product QA approvals."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image
import gallery_engine as g
import research_export as r
from workbook_snapshots import check_snapshot_history
import test_research_export as export_fixtures


class ExportBoundaries(unittest.TestCase):
    def fixture(self, root):
        helper=export_fixtures.ResearchExportTests()
        return helper, helper.full_fixture(root)

    def test_identity_and_base_facts_are_bound(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); helper,(book,data,path,ledger)=self.fixture(root); book.close()
            result=helper.export_run(ledger,path)
            facts=root/'product-facts.json'
            self.assertEqual(result['productFactsSha256'],hashlib.sha256(facts.read_bytes()).hexdigest())
            original=json.loads(facts.read_text())
            for section,key,value in [('identity','internalId','OTHER'),('selectedBaseConfiguration','id','OTHER'),('selectedBaseConfiguration','ramGB',64)]:
                changed=copy.deepcopy(original); changed[section][key]=value; facts.write_text(json.dumps(changed))
                with self.subTest(key=key),self.assertRaises(ValueError): helper.export_run(ledger,path)

    def test_source_formulas_rejected_even_when_ledger_matches(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); helper,(book,data,path,ledger)=self.fixture(root)
            formula='=HYPERLINK("https://example.invalid","source")'
            data['facts'][0]['source']=formula; ledger.write_text(json.dumps(data))
            book['Product Details'].cell(5,2).value=formula; book.save(path); book.close()
            with self.assertRaisesRegex(ValueError,'Formula'): helper.export_run(ledger,path)

    def test_export_rejects_missing_core_bad_title_bullets_and_numeric_values(self):
        cases=[('Model Number',None),('Item Name','wrong title'),
               ('Item Name','MegaPC Custom Desktop Created Using Dell QCM1250 64GB RAM 256GB SSD Win 11 Pro'),('Bullet Point','one bullet'),
               ('RAM Memory Installed',True),('RAM Memory Installed',-16),('RAM Memory Installed Size Unit','unknown')]
        for field,value in cases:
            with self.subTest(field=field,value=value),tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp); helper,(book,data,path,ledger)=self.fixture(root)
                fact=next(f for f in data['facts'] if f['attribute']==field and f['sheet']=='Product Details')
                fact.update(final_value=value,status='NOT_APPLICABLE' if value is None else 'VERIFIED')
                col=next(c.column for c in book['Product Details'][1] if c.value==field)
                book['Product Details'].cell(3,col).value=value;book['Product Details'].cell(4,col).value=fact['status']
                book.save(path);book.close();ledger.write_text(json.dumps(data))
                with self.assertRaises(ValueError): helper.export_run(ledger,path)


class GalleryBoundaries(unittest.TestCase):
    def build(self,p,size=(1600,900)):
        for n in g.NAMES: Image.new('RGB',size,'white').save(p/n)
        (p/'unbranded').mkdir()
        for n in g.PT: (p/'unbranded'/n).write_bytes((p/n).read_bytes())
        logo=p.parent/(p.name+'-logo.png')
        mark=Image.new('RGBA',(202,102));mark.paste('blue',(1,1,201,101));mark.save(logo)
        self.addCleanup(lambda:logo.unlink(missing_ok=True))
        cfg={'x':64,'y':64,'width':176,'height':88,'style':'transparent','protectedZones':[{'x':400,'y':300,'width':300,'height':400,'label':'PRODUCT_SILHOUETTE'}]}
        g.write(p/'logo-placement.json',{'brand':'OEM','logoRole':'OEM base-product identifier','placements':{n:cfg for n in g.PT}})
        g.write(p/'product-facts.json',{'identity':{'cpu':'Synthetic'},'selectedBaseConfiguration':{'ramGB':16},'offer':{'price':1}})
        g.write(p/'style-lock.json',{'status':'APPROVED','recipeVersion':'synthetic'})
        g.badges(p,logo,p/'logo-placement.json')
        return logo

    def reviews(self,p,slots=None):
        for file,names in [('visual-review.json',slots or g.NAMES),('semantic-review.json',slots or g.PT)]:
            g.write(p/file,{'schemaVersion':3,'result':'PASS','reviewer':'Synthetic test reviewer','reviewedAtUtc':'2026-10-14T12:00:00Z',
                           'reviewInputsSha256':g.review_inputs(p),'galleryInventorySha256':{n:g.digest(p/n) for n in g.NAMES},
                           'images':[{'file':n,'sha256':g.digest(p/n),'result':'PASS','notes':'Synthetic regression fixture only'} for n in names]})

    def test_full_landscape_pipeline_and_fact_style_invalidation(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);self.build(p);self.reviews(p);g.accept(p);g.validate(p)
            facts=g.read(p/'product-facts.json');facts['offer']['price']=2;g.write(p/'product-facts.json',facts)
            g.validate(p)  # Price is outside image evidence.
            facts['selectedBaseConfiguration']['ramGB']=64;g.write(p/'product-facts.json',facts)
            with self.assertRaisesRegex(ValueError,'binding'):g.validate(p)
            facts['selectedBaseConfiguration']['ramGB']=16;g.write(p/'product-facts.json',facts)
            g.write(p/'style-lock.json',{'status':'REVOKED'})
            with self.assertRaisesRegex(ValueError,'approved style'):g.validate(p)

    def test_partial_landscape_and_vd744_future_update_route(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'product generated photo/VD-744';p.mkdir(parents=True)
            self.build(p);self.reviews(p,['PT02.png'])
            g.write(p/'approved-angle-import.json',{'historical':'not operative'})
            g.write(p/'delivery-status.json',{'galleryState':'LEGACY_QUARANTINED','currentQaPass':False})
            g.accept(p,slots=['PT02.png']);g.validate_partial(p,['PT02.png'])
            with patch.object(g.subprocess,'check_output',return_value='product generated photo/VD-744/PT02.png\n'):
                result=g.gate(root,'base','head')
            self.assertEqual(result['partialUpdatesValidated'],1)

    def test_geometry_rules_identical_and_protection_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);logo=self.build(p);self.reviews(p)
            plan=g.read(p/'logo-placement.json');plan['placements']['PT01.png']['protectedZones']=[];g.write(p/'logo-placement.json',plan)
            qa=g.read(p/'logo-qa.json');qa['placementPlanSha256']=g.digest(p/'logo-placement.json');g.write(p/'logo-qa.json',qa)
            with self.assertRaisesRegex(ValueError,'silhouette'):g.validate(p,require_final=False)
            before={n:g.digest(p/n) for n in g.NAMES}
            with self.assertRaises(ValueError):g.finalize(p,logo,'OEM',p.parent/'sheet.png',slots=['PT01.png'])
            self.assertEqual(before,{n:g.digest(p/n) for n in g.NAMES})

    def test_finalize_missing_contact_does_not_mutate(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);logo=self.build(p);before={n:g.digest(p/n) for n in g.NAMES}
            with self.assertRaisesRegex(ValueError,'Contact'):g.finalize(p,logo,'OEM',None,slots=['PT01.png'])
            self.assertEqual(before,{n:g.digest(p/n) for n in g.NAMES})

    def test_finalize_creates_new_pt_gallery_from_clean_masters(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);logo=self.build(p);sheet=p.parent/(p.name+'-sheet.png')
            self.addCleanup(lambda:sheet.unlink(missing_ok=True))
            before={n:g.digest(p/n) for n in g.MAIN}
            for n in g.PT:(p/n).unlink()
            g.finalize(p,logo,'OEM',sheet)
            self.assertTrue(sheet.exists())
            self.assertEqual(before,{n:g.digest(p/n) for n in g.MAIN})
            self.reviews(p);g.accept(p);g.validate(p)

    def test_review_metadata_rejects_blank_and_invalid_time(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);self.build(p);self.reviews(p)
            original=g.read(p/'visual-review.json')
            for field,value in [('reviewer','  '),('reviewedAtUtc','now'),('reviewedAtUtc','2026-10-14'),('notes','  ')]:
                report=copy.deepcopy(original)
                if field=='notes':report['images'][0]['notes']=value
                else:report[field]=value
                g.write(p/'visual-review.json',report)
                with self.assertRaises(ValueError):g.evidence(p/'visual-review.json',g.NAMES,p)

    def test_completed_without_images_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'product generated photo/TEST';p.mkdir(parents=True)
            g.write(p/'delivery-status.json',{'galleryState':'CURRENT_REVIEWED','currentQaPass':True})
            with self.assertRaisesRegex(ValueError,'no canonical'):g.gate(root)

    def test_frozen_authority_cannot_be_rehashed(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'VL-1326';p.mkdir()
            original=Path(g.__file__).parents[1]/'product generated photo/VL-1326/approved-ai-effect-import.json'
            (p/original.name).write_bytes(original.read_bytes());g.frozen_import(p,original.name)
            record=g.read(p/original.name);record['images']['PT01.png']='0'*64;g.write(p/original.name,record)
            with self.assertRaisesRegex(ValueError,'frozen'):g.frozen_import(p,original.name)


class SnapshotGitBoundaries(unittest.TestCase):
    def test_powershell_wrappers_share_runtime_without_path_fallback(self):
        scripts=Path(g.__file__).parent
        names=['add-brand-badge','add-fixed-image-overlay','finalize-image-gallery','accept-reviewed-gallery',
               'crop-image','new-contact-sheet','normalize-square-image','remove-neutral-logo-background',
               'test-final-image-gallery','test-gallery-commit-gate-selftest','test-wide-wordmark-gate-selftest']
        for name in names:
            text=(scripts/(name+'.ps1')).read_text()
            self.assertIn('Resolve-ListingPython',text)
            self.assertNotIn('Get-Command python',text)
        self.assertIn('HistoricalOnly',(scripts/'test-gaming-main-reference.ps1').read_text())

    def test_review_json_newline_binding_is_portable(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'review.json'
            p.write_bytes(b'{\r\n "result": "PASS"\r\n}\r\n');before=g.digest(p)
            p.write_bytes(p.read_bytes().replace(b'\r\n',b'\n'))
            self.assertEqual(before,g.digest(p))
            p.write_text('{"result":"FAIL"}')
            self.assertNotEqual(before,g.digest(p))

    def test_git_roundtrip_and_append_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            def git(*args):return subprocess.check_output(['git',*args],cwd=root,stderr=subprocess.DEVNULL).decode().strip()
            git('init');git('config','core.autocrlf','true');git('config','user.name','Test');git('config','user.email','test@localhost')
            attrs=Path(g.__file__).parents[1]/'.gitattributes';(root/'.gitattributes').write_bytes(attrs.read_bytes())
            bundle=root/'product generated photo/TEST/workbook-snapshots/v1';bundle.mkdir(parents=True)
            ledger=bundle/'ledger.json';payload=b'{\r\n  "test": true\r\n}\r\n';ledger.write_bytes(payload)
            git('add','.');git('commit','-m','base');base=git('rev-parse','HEAD')
            blob=subprocess.check_output(['git','show','HEAD:product generated photo/TEST/workbook-snapshots/v1/ledger.json'],cwd=root)
            self.assertEqual(blob,payload)
            new=bundle.parent/'v2';new.mkdir();(new/'ledger.json').write_bytes(payload)
            git('add','.');git('commit','-m','new revision');check_snapshot_history(root,base,'HEAD')
            ledger.write_text('changed');git('add','.');git('commit','-m','rewrite old bundle')
            with self.assertRaisesRegex(ValueError,'changed/deleted'):check_snapshot_history(root,base,'HEAD')
            ledger.unlink();git('add','-A');git('commit','-m','delete old bundle')
            with self.assertRaisesRegex(ValueError,'changed/deleted'):check_snapshot_history(root,base,'HEAD')


if __name__=='__main__':unittest.main()
