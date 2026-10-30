"""Synthetic follow-up regressions; no actual product/review/provider approval."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from unittest.mock import patch
from PIL import Image
sys.path[:0] = [str(Path(__file__).resolve().parents[1]), str(Path(__file__).resolve().parent)]
import business_information_plan as business
import test_business_reference_adaptation as bf
import test_research_export as ef
import test_release_checks as rf
import test_scoped_workflow_v2 as sf
import gallery_engine as g
import image_fact_update as update
import production_guard as guard
import image_policy_sources as policies
import image_review_scope as scope
import drive_delivery as drive
import delivery_context as context
import delivery_privacy as privacy

class BusinessPartial(unittest.TestCase):
    def fixture(self, selected=('PT05.png',)):
        f=bf.BusinessReferenceTests(); f.setUp()
        original=copy.deepcopy(f.plan['images'])
        f.plan['selectedSlots']=list(selected)
        f.plan['images']=[r for r in original if r['file'] in selected]
        return f, original

    def test_single_choice_page_passes_without_seven_other_plans(self):
        f,_=self.fixture();result=f.check()
        self.assertEqual(result['scope'],'SELECTED_SUPPORTING')
        self.assertEqual(result['imageCount'],1)
        self.assertEqual(len(result['unloadedContextSlots']),7)
        self.assertFalse(result['productionApprovalGranted'])
        f.plan['images'][0]['fullConfigurationOverview']=True
        with self.assertRaisesRegex(ValueError,'PT03'):f.check()

    def test_missing_selected_page_and_duplicate_scope_fail(self):
        for selected in ([],['PT05.png','PT05.png'],['MAIN-STRICT.jpg'],[{}]):
            f,_=self.fixture();f.plan['selectedSlots']=selected
            with self.subTest(selected=selected),self.assertRaises(ValueError):f.check()
        f,_=self.fixture();f.plan['images']=[]
        with self.assertRaisesRegex(ValueError,'exactly match'):f.check()

    def test_retained_front_context_prevents_repeated_front(self):
        f,old=self.fixture(('PT03.png',));row=old[0]
        f.plan['retainedContext']=[{**row,'sha256':'a'*64,'evidenceReference':'Synthetic observed prior record'}]
        f.plan['images'][0]['presentation']['storyboard']['framing']='FRONT'
        with self.assertRaisesRegex(ValueError,'front product'):f.check()
        f.plan['images'][0]['presentation']['storyboard']['framing']='THREE_QUARTER'
        result=f.check();self.assertEqual(result['contextSlots'],['PT01.png'])
        f.plan['retainedContext'][0].pop('sha256')
        with self.assertRaisesRegex(ValueError,'Retained context'):f.check()

    def test_nested_accessory_and_screen_customer_copy_cannot_evade_check(self):
        for key in ('customerLabel','screenCopy','presentationCopy'):
            f,_=self.fixture(('PT07.png',));item=f.plan['images'][0]['presentation']
            item['screen']['shown']=False
            item['storyboard'].update(subject='ACCESSORIES',productVisibility='NONE',framing='NONE',productViewId=None)
            item['storyboard']['accessoryTreatment']={'supplyStatus':'NOT_INCLUDED','customerLabel':'Accessories shown are not included.'}
            f.check()
            if key=='customerLabel': item['storyboard']['accessoryTreatment'][key]='STYLE PREVIEW / VL-1223'
            elif key=='screenCopy':item['screen']['customerCopy']='内部说明'
            else:item['customerCopy']='PT03 / VERSION'
            with self.subTest(key=key),self.assertRaises(ValueError):f.check()

    def test_product_free_logo_finalizes_without_fake_silhouette(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);p=root/'TEST-PC';p.mkdir();(p/'unbranded').mkdir()
            Image.new('RGB',(1000,1000),'white').save(p/'unbranded/PT05.png')
            logo=root/'logo.png';im=Image.new('RGBA',(202,102));im.paste('blue',(1,1,201,101));im.save(logo)
            cfg={'x':50,'y':60,'width':80,'height':40,'style':'transparent','anchor':'BRAND_CORNER',
                 'purpose':'Identify the actual manufacturer beside the choices','readingPriority':'SECONDARY',
                 'productVisibility':'NONE','protectedZones':[{'x':300,'y':200,'width':400,'height':500,'label':'PRIMARY_OPTIONS_GUIDE'}]}
            plan={'brand':'OEM','logoRole':'OEM base-product identifier','placementPolicy':'SEMANTIC_OEM_INTEGRATION_V1','placements':{'PT05.png':cfg}}
            g.write(p/'logo-placement.json',plan)
            g.finalize(p,logo,'OEM',root/'contact.png',slots=['PT05.png'])
            self.assertTrue((p/'PT05.png').is_file());self.assertFalse((p/'PT01.png').exists())
            plan.pop('placementPolicy')
            with self.assertRaisesRegex(ValueError,'Product-free'):g.logo_geometry(plan,cfg,im,(1000,1000))

class ImageFactUpdates(unittest.TestCase):
    def fixture(self, root):
        p=root/'TEST-PC';p.mkdir();book,data,workbook,ledger=ef.ResearchExportTests().full_fixture(p);book.close()
        ledger.rename(p/'research-ledger.json')
        cpu=next(f for f in data['facts'] if f['attribute']=='CPU Model Manufacturer')
        cpu.update(status='VERIFIED',final_value='Intel',applies_to_sold_configuration=True,transfer_basis='Synthetic verified image baseline')
        g.write(p/'research-ledger.json',data)
        g.write(p/'style-lock.json',{'status':'APPROVED','recipeVersion':'synthetic'})
        Image.new('RGB',(600,500),'white').save(p/sf.MAIN)
        field='Total USB 3.0 Ports'
        declaration={'fields':[['Product Details',field]],'productPaths':[],'basis':'Synthetic actual-image field scope'}
        request={'mode':'IMAGE_ADJUSTMENT_WORKFLOW','configurationId':'BASE-A','runId':'IMAGE-FACTS',
                 'requestReference':'Synthetic explicit image task','imageFactUpdate':declaration,
                 'selectedSlots':[sf.MAIN],
                 'allowedChanges':['product-facts.json','research-ledger.json','visual-review.json','semantic-review.json','partial-update-qa.json'],
                 'outputs':{sf.MAIN:'IMAGE','product-facts.json':'RESEARCH','research-ledger.json':'RESEARCH'},
                 'styleApproval':{'userReference':'Synthetic approval','styleLockSha256':guard.sha(p/'style-lock.json')}}
        with patch.object(guard,'workflow',return_value='a'*40):contract=guard.capture(p,request)
        fact=next(f for f in data['facts'] if f['attribute']==field)
        fact.update(status='VERIFIED',final_value=4,applies_to_sold_configuration=True,transfer_basis='Synthetic applicable unit')
        fact.setdefault('evidence',{})['research_trace']=rf.trace_for(fact)
        g.write(p/'research-ledger.json',data)
        return p,data,contract,workbook,fact

    def test_real_production_and_drive_pair_delivery_without_workbook(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);p,data,contract,workbook,fact=self.fixture(root);old=workbook.read_bytes()
            sf.selected_reviews(p,[sf.MAIN]);g.accept_partial(p,[sf.MAIN])
            frozen=root/'contract.json';g.write(frozen,contract)
            with patch.object(guard,'workflow',return_value='a'*40):checked=guard.verify(p,frozen,guard.sha(frozen))
            self.assertEqual(checked['checks']['imageFactUpdate']['state'],'SCOPED_IMAGE_FACT_UPDATE_CHECKED')
            self.assertEqual(workbook.read_bytes(),old)
            self.assertIn(workbook.name,checked['checks']['imageFactUpdate']['unchangedWorkbooks'])
            plan=drive.plan(p,'IMAGE-FACTS',list(contract['outputs']))
            policy=g.read(context.ROOT/'assets/delivery-storage.json');stamp=datetime.now(timezone.utc).isoformat()
            nodes=[{'id':policy['projectFolderId'],'name':'Project','parents':[]},
                   {'id':policy['productsFolderId'],'name':'20_PRODUCTS','parents':[policy['projectFolderId']]},
                   {'id':'p','name':'TEST-PC','parents':[policy['productsFolderId']]},
                   {'id':'images','name':'02_IMAGES','parents':['p']},
                   {'id':'research','name':'03_RESEARCH','parents':['p']},
                   {'id':'final','name':'FINAL','parents':['research']}]
            for n in nodes:n.update(mimeType=context.FOLDER,readBackAtUtc=stamp)
            rows=[];screens={};dest={}
            for i,row in enumerate(plan['files']):
                name=row['relativePath'];dest[name]='images' if name==sf.MAIN else 'final'
                if name!=sf.MAIN:screens[name]=privacy.screen_file(p/name,serials_used=False)
                else:screens[name]={'state':'DELIVERY_PRIVACY_SCREEN_PASS','inputSha256':row['sha256'],'manualReviewRequired':False,'serialInventoryDeclared':False}
                rows.append({'relativePath':name,'id':'synthetic-file-'+str(i),'name':name,'parents':[dest[name]],'mimeType':row['mimeType'],
                             'size':row['size'],'downloadedSha256':row['sha256'],'readBackAtUtc':stamp,
                             'webViewLink':'https://drive.google.com/file/d/synthetic-file-'+str(i)+'/view'})
            ctx={'productId':'TEST-PC','serialsUsed':False,'folders':nodes,'fileRoles':contract['outputs'],'privacyChecks':screens}
            self.assertEqual(drive.verify(p,plan,{'files':rows},dest,ctx)['deliveryState'],'DRIVE_DELIVERY_VERIFIED')

    def test_undeclared_field_leaf_and_identity_changes_fail(self):
        for change in ('field','leaf','identity'):
            with self.subTest(change=change),tempfile.TemporaryDirectory() as temp:
                p,data,c,_,_=self.fixture(Path(temp))
                if change=='field':data['facts'][0]['source']='Unrequested source change';g.write(p/'research-ledger.json',data)
                else:
                    facts=g.read(p/'product-facts.json')
                    if change=='leaf':facts['unrequested']='Different'
                    else:facts['identity']['internalId']='OTHER-PC'
                    g.write(p/'product-facts.json',facts)
                with self.assertRaises(ValueError):update.check(p,c['imageFactUpdate'])

    def test_missing_trace_no_pair_or_workbook_bypass_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            p,data,c,_,fact=self.fixture(Path(temp));fact['evidence'].pop('research_trace');g.write(p/'research-ledger.json',data)
            with self.assertRaisesRegex(ValueError,'research_trace'):update.check(p,c['imageFactUpdate'])
            bad=copy.deepcopy(c);bad['outputs'].pop('product-facts.json')
            with self.assertRaisesRegex(ValueError,'pair'):guard.validate_contract(bad)
            bad=copy.deepcopy(c);bad['outputs']['unexpected.xlsx']='RESEARCH'
            with self.assertRaisesRegex(ValueError,'workbooks'):guard.validate_contract(bad)
            bad=copy.deepcopy(c);bad['imageFactUpdate']['scope']['fields']=[['Product Details','Item Name']]
            with self.assertRaisesRegex(ValueError,'technical'):guard.validate_contract(bad)

class RuleSources(unittest.TestCase):
    def fixture(self, root):
        (root/'references').mkdir();(root/'assets').mkdir()
        (root/'references/rule.md').write_text('''# Rules

## MAIN
Original main

## PT
Original supporting
''',encoding='utf-8')
        policy={'imageReview':{'shared':{},'main':{},'supporting':{},'BUSINESS_LAPTOP':{'sourceBindings':{
            'main':[{'path':'references/rule.md','section':'## MAIN','sha256':'0'*64}],
            'supporting':[{'path':'references/rule.md','section':'## PT','sha256':'0'*64}]}}}}
        g.write(root/policies.POLICY,policy);policies.check(root,True)
        return g.read(root/policies.POLICY)

    def test_changed_rule_blocks_production_and_ci_until_explicit_refresh(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);policy=self.fixture(root)
            self.assertEqual(policies.check(root)['state'],'IMAGE_POLICY_SOURCES_CHECKED')
            file=root/'references/rule.md';file.write_text(file.read_text().replace('Original supporting','New supporting'))
            with self.assertRaisesRegex(ValueError,'stale'):policies.check(root)
            with self.assertRaisesRegex(ValueError,'changed'):policies.selected_sources(policy,'BUSINESS_LAPTOP','supporting',root)
            before=policies.selected_sources(policy,'BUSINESS_LAPTOP','main',root)
            policies.check(root,True);new=g.read(root/policies.POLICY)
            self.assertEqual(before,policies.selected_sources(new,'BUSINESS_LAPTOP','main',root))
            self.assertNotEqual(policy['imageReview']['BUSINESS_LAPTOP']['sourceBindings']['supporting'],new['imageReview']['BUSINESS_LAPTOP']['sourceBindings']['supporting'])
            self.assertEqual(policies.selected_sources(policy,'BUSINESS_LAPTOP','supporting',root,historical=True),policy['imageReview']['BUSINESS_LAPTOP']['sourceBindings']['supporting'])

    def test_scoped_projection_excludes_other_kind_source_changes(self):
        root=Path(g.__file__).resolve().parents[1];policy=g.read(root/policies.POLICY)
        style={'scopeVersion':2,'shared':{'designSeries':'BUSINESS_LAPTOP'},'slots':{sf.MAIN:{'status':'APPROVED','approvalReference':'Synthetic main selection'}}}
        before=scope.style_projection('.',sf.MAIN,style,{'__scopedImagePolicy__':json.dumps(policy)})
        policy['imageReview']['BUSINESS_LAPTOP']['sourceBindings']['supporting'][0]['sha256']='b'*64
        after=scope.style_projection('.',sf.MAIN,style,{'__scopedImagePolicy__':json.dumps(policy)})
        self.assertEqual(before,after)
        policy['imageReview']['BUSINESS_LAPTOP']['sourceBindings']['main'][0]['sha256']='c'*64
        self.assertNotEqual(before,scope.style_projection('.',sf.MAIN,style,{'__scopedImagePolicy__':json.dumps(policy)}))

    def test_legacy_sources_missing_sections_and_traversal_are_explicit(self):
        self.assertIsNone(policies.selected_sources({'imageReview':{'shared':{},'main':{},'GAMING':{}}},'GAMING','main','.'))
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);self.fixture(root)
            for row in ({'path':'../outside.md'},{'path':'references/rule.md','section':'## MISSING'}):
                with self.assertRaises(ValueError):policies.source_bytes(root,row)

if __name__=='__main__':unittest.main()
