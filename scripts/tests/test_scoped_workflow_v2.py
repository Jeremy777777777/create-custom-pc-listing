"""Synthetic regressions for real workflow boundaries; no product approval is granted."""
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gallery_engine as g
import image_review_scope as scope
import production_guard as guard
import workflow_run as runs
import customer_visible_content as customer
import test_business_reference_adaptation as business_fixture
import test_gaming_visual_plan as gaming_fixture
import test_review_scope_fixes as review_fixture
import gaming_visual_plan as gaming

STAMP = '2026-10-14T12:00:00Z'
MAIN = g.MAIN[1]


def simple_product(root):
    p = root/'TEST-PC'
    p.mkdir()
    g.write(p/'product-facts.json', {'internalId':'TEST-PC','selectedBaseConfiguration':{'id':'BASE-A'}})
    g.write(p/'style-lock.json', {'status':'APPROVED','recipeVersion':'synthetic'})
    Image.new('RGB',(600,500),'white').save(p/MAIN)
    return p


def selected_reviews(p, slots):
    inventory = g.gallery_inventory(p, slots)
    for file in ('visual-review.json','semantic-review.json'):
        g.write(p/file, {'schemaVersion':3,'result':'PASS','reviewer':'Synthetic fixture only',
                        'reviewedAtUtc':STAMP,'reviewInputsSha256':g.review_inputs(p),
                        'galleryInventorySha256':inventory,
                        'images':[{'file':n,'sha256':g.digest(p/n),'result':'PASS',
                                   'notes':'Synthetic review; not actual product evidence'} for n in slots]})


class PartialInventory(unittest.TestCase):
    def test_one_main_can_deliver_without_ten_unrequested_images(self):
        with tempfile.TemporaryDirectory() as temp:
            p=simple_product(Path(temp)); selected_reviews(p,[MAIN])
            g.accept_partial(p,[MAIN]); g.validate_partial(p,[MAIN])
            report=g.read(p/'partial-update-qa.json')
            self.assertEqual(report['galleryInventorySha256'],{MAIN:g.digest(p/MAIN)})
            self.assertEqual(len(report['galleryCoverage']['unavailableInThisRun']),10)
            self.assertFalse(report['fullGalleryPass'])
            with self.assertRaises(FileNotFoundError): g.validate(p)

    def test_evidenced_remote_baseline_avoids_downloading_other_images(self):
        with tempfile.TemporaryDirectory() as temp:
            p=simple_product(Path(temp))
            remote={'sha256':'b'*64,'driveFileId':'synthetic-file','parentFolderId':'synthetic-parent',
                    'observedAtUtc':STAMP,'evidenceReference':'https://example.invalid/synthetic-receipt'}
            g.write(p/'gallery-baseline.json',{'schemaVersion':1,'productId':p.name,'images':{'PT08.png':remote}})
            selected_reviews(p,[MAIN]); g.accept_partial(p,[MAIN]); g.validate_partial(p,[MAIN])
            report=g.read(p/'partial-update-qa.json')
            self.assertEqual(report['galleryCoverage']['knownRemoteOnly'],['PT08.png'])
            self.assertEqual(report['retainedReviewStates']['PT08.png'],'REMOTE_BYTES_RECORDED_REVIEW_NOT_LOADED')
            remote.pop('evidenceReference')
            g.write(p/'gallery-baseline.json',{'schemaVersion':1,'productId':p.name,'images':{'PT08.png':remote}})
            with self.assertRaisesRegex(ValueError,'evidence'): g.gallery_inventory(p,[MAIN])

    def test_retained_tamper_and_wrong_inventory_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            p=simple_product(Path(temp))
            Image.new('RGB',(600,500),'white').save(p/'PT08.png')
            g.write(p/'gallery-baseline.json',{'schemaVersion':1,'productId':p.name,
                    'images':{'PT08.png':{'sha256':g.digest(p/'PT08.png')}}})
            selected_reviews(p,[MAIN]);g.accept_partial(p,[MAIN])
            Image.new('RGB',(600,500),'red').save(p/'PT08.png')
            with self.assertRaisesRegex(ValueError,'retained image'):g.validate_partial(p,[MAIN])

    def test_frozen_baseline_cannot_change_even_if_listed_as_allowed(self):
        with tempfile.TemporaryDirectory() as temp:
            p=simple_product(Path(temp))
            g.write(p/'gallery-baseline.json',{'schemaVersion':1,'productId':p.name,'images':{}})
            request={'mode':'IMAGE_ADJUSTMENT_WORKFLOW','runId':'R1','configurationId':'BASE-A',
                     'requestReference':'Synthetic explicit one-main request','allowedChanges':[MAIN,'gallery-baseline.json'],
                     'outputs':{MAIN:'IMAGE'},'selectedSlots':[MAIN],
                     'styleApproval':{'userReference':'Synthetic approval','styleLockSha256':guard.sha(p/'style-lock.json')}}
            with patch.object(guard,'workflow',return_value='a'*40):contract=guard.capture(p,request)
            g.write(p/'gallery-baseline.json',{'schemaVersion':1,'productId':p.name,'images':{},'changed':True})
            with self.assertRaisesRegex(ValueError,'Frozen gallery baseline'):guard.check_scope(p,contract)

    def test_finalize_and_contact_sheet_work_with_only_requested_main(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);p=simple_product(root);before=g.digest(p/MAIN)
            g.finalize(p,None,None,root/'contact.png',slots=[MAIN])
            self.assertEqual(g.digest(p/MAIN),before)
            self.assertTrue((root/'contact.png').is_file())
            self.assertFalse((p/'PT01.png').exists())


class ScopedReviewInputs(unittest.TestCase):
    def setup_product(self, root):
        helper=review_fixture.ScopedImageReviews()
        self.addCleanup(helper.doCleanups)
        p,data=helper.fixture(root)
        style={'scopeVersion':2,'status':'APPROVED',
               'shared':{'designSeries':'BUSINESS_LAPTOP','palette':['navy','pale gray']},
               'slots':{n:{'status':'APPROVED','approvalReference':'Synthetic selection for '+n,
                           'recipePath':'source/'+n+'.json'} for n in g.NAMES}}
        (p/'source').mkdir()
        for n in g.NAMES:g.write(p/'source'/(n+'.json'),{'slot':n,'version':1})
        g.write(p/'style-lock.json',style)
        deps={'scopeVersion':2,'fields':[['Product Details','Number of USB 3.0 Ports']],
              'productPaths':[],'basis':'Synthetic per-image fact and style coverage'}
        return p,style,deps

    def test_other_slot_style_recipe_and_policy_do_not_expire_ports_review(self):
        with tempfile.TemporaryDirectory() as temp:
            p,style,deps=self.setup_product(Path(temp));before=scope.binding(p,'PT08.png',deps)
            style['slots'][MAIN]['approvalReference']='Different synthetic main approval'
            g.write(p/'style-lock.json',style);g.write(p/'source'/(MAIN+'.json'),{'changed':True})
            self.assertEqual(before,scope.binding(p,'PT08.png',deps))
            policy=g.read(Path(g.__file__).resolve().parents[1]/scope.SCOPED_POLICY)
            policy['sync']['defaultMode']='UNRELATED_CHANGE'
            policy['imageReview']['GAMING']['version']=99
            self.assertEqual(before,scope.binding(p,'PT08.png',deps,{'__scopedImagePolicy__':json.dumps(policy)}))

    def test_own_slot_shared_style_fact_and_applicable_policy_invalidate(self):
        for change in ('own','shared','fact','policy'):
            with self.subTest(change=change),tempfile.TemporaryDirectory() as temp:
                p,style,deps=self.setup_product(Path(temp));before=scope.binding(p,'PT08.png',deps);historical=None
                if change=='own':g.write(p/'source/PT08.png.json',{'version':2})
                if change=='shared':
                    style['shared']['palette']=['red'];g.write(p/'style-lock.json',style)
                if change=='fact':
                    ledger=g.read(p/'research-ledger.json');ledger['facts'][1]['final_value']=7;g.write(p/'research-ledger.json',ledger)
                if change=='policy':
                    policy=g.read(Path(g.__file__).resolve().parents[1]/scope.SCOPED_POLICY)
                    policy['imageReview']['supporting']['version']=2
                    historical={'__scopedImagePolicy__':json.dumps(policy)}
                self.assertNotEqual(before,scope.binding(p,'PT08.png',deps,historical))

    def test_one_failed_retained_record_does_not_discard_other_valid_records(self):
        with tempfile.TemporaryDirectory() as temp:
            p,style,deps=self.setup_product(Path(temp));retained={}
            for name in ('PT07.png','PT08.png'):
                row={'file':name,'sha256':g.digest(p/name),'result':'PASS','notes':'Synthetic fixture',
                     'customerText':['A verified customer-facing feature'],'dependencies':deps,
                     'reviewInputsSha256':scope.binding(p,name,deps)}
                report={'schemaVersion':4,'result':'PASS','reviewer':'Synthetic','reviewedAtUtc':STAMP,'images':[row]}
                retained[name]={kind:copy.deepcopy(report) for kind in ('visual-review.json','semantic-review.json')}
            g.write(p/'partial-update-qa.json',{'retainedReviewEvidence':retained})
            style['slots']['PT07.png']['approvalReference']='Changed synthetic selection';g.write(p/'style-lock.json',style)
            valid=g.retained_reviews(p,[MAIN])
            self.assertIn('PT08.png',valid)
            self.assertNotIn('PT07.png',valid)
            row={'file':MAIN,'sha256':g.digest(p/MAIN),'result':'PASS','notes':'Synthetic main review',
                 'customerText':['A verified main feature'],'dependencies':deps,
                 'reviewInputsSha256':scope.binding(p,MAIN,deps)}
            for file in ('visual-review.json','semantic-review.json'):
                g.write(p/file,{'schemaVersion':4,'result':'PASS','reviewer':'Synthetic','reviewedAtUtc':STAMP,
                                'images':[copy.deepcopy(row)],'galleryInventorySha256':g.gallery_inventory(p,[MAIN])})
            g.accept_partial(p,[MAIN])
            self.assertEqual(g.read(p/'partial-update-qa.json')['retainedReviewState'],'PARTIALLY_VERIFIED')
            g.validate_partial(p,[MAIN])

    def test_v2_does_not_accept_missing_copy_or_unapproved_slot(self):
        with tempfile.TemporaryDirectory() as temp:
            p,style,deps=self.setup_product(Path(temp))
            row={'file':'PT08.png','sha256':g.digest(p/'PT08.png'),'result':'PASS','notes':'Synthetic',
                 'dependencies':deps,'reviewInputsSha256':scope.binding(p,'PT08.png',deps)}
            report={'schemaVersion':4,'result':'PASS','reviewer':'Synthetic','reviewedAtUtc':STAMP,'images':[row]}
            with self.assertRaisesRegex(ValueError,'customerText'):g.review_record(report,['PT08.png'],p)
            row['customerText']=['STYLE PREVIEW']
            with self.assertRaisesRegex(ValueError,'production status'):g.review_record(report,['PT08.png'],p)
            style['slots']['PT08.png']['status']='PENDING';g.write(p/'style-lock.json',style)
            with self.assertRaisesRegex(ValueError,'approval'):scope.binding(p,'PT08.png',deps)


class SemanticBrandAndCopy(unittest.TestCase):
    def logo(self):
        logo=Image.new('RGBA',(202,102));logo.paste('blue',(1,1,201,101));return logo

    def placement(self):
        return {'x':50,'y':60,'width':80,'height':40,'style':'transparent','anchor':'PRODUCT_IDENTITY',
                'purpose':'Identify the actual laptop beside its customer-facing product name',
                'readingPriority':'SECONDARY','protectedZones':[{'x':300,'y':220,'width':400,'height':500,'label':'PRIMARY_FEATURE_VISUAL'}]}

    def test_original_logo_can_integrate_at_subordinate_size_without_fake_product_zone(self):
        plan={'logoRole':'OEM base-product identifier','placementPolicy':'SEMANTIC_OEM_INTEGRATION_V1'}
        self.assertGreater(g.logo_geometry(plan,self.placement(),self.logo(),(1000,1000)),0)
        with self.assertRaises(ValueError):g.logo_geometry({'logoRole':'OEM base-product identifier'},self.placement(),self.logo(),(1000,1000))

    def test_integrated_logo_still_rejects_distortion_overlap_and_missing_purpose(self):
        for mutation in ({'height':80},{'x':300,'y':220},{'purpose':''},{'readingPriority':'PRIMARY'}):
            cfg=self.placement();cfg.update(mutation)
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):
                g.logo_geometry({'logoRole':'OEM base-product identifier','placementPolicy':'SEMANTIC_OEM_INTEGRATION_V1'},cfg,self.logo(),(1000,1000))

    def test_business_and_gaming_customer_copy_share_the_same_checker(self):
        fixture=business_fixture.BusinessReferenceTests();fixture.setUp()
        for value in ('PT01 / CONFIGURATION','STYLE PREVIEW','VA-215','测试标题'):
            original=fixture.plan['images'][0]['headline']
            fixture.plan['images'][0]['headline']=value
            with self.subTest(value=value),self.assertRaises(ValueError):fixture.check()
            fixture.plan['images'][0]['headline']=original
        fixture.plan['productId']=fixture.ledger['productId']
        fixture.check()
        customer.validate_image_plan_copy({'productId':'VL-1223','images':[{'headline':'LG gram 17','claims':[{'text':'32GB LPDDR5X'}]}]})

    def test_new_gaming_cli_contract_requires_original_oem_placement(self):
        fixture=gaming_fixture.GamingVisualPlanTests();fixture.setUp()
        with self.assertRaisesRegex(ValueError,'OEM semantic'):gaming.check(fixture.plan,fixture.registry,require_oem=True)
        visual=fixture.plan['images'][0]['visualExplanation']
        visual['oemLogoPlacement']={'assetPath':'assets/original-oem.png','assetSha256':'a'*64,
                                   'anchor':'FEATURE_HEADER','purpose':'Identify the laptop',
                                   'readingPriority':'SECONDARY','protectedElements':['headline','primary visual']}
        result=gaming.check(fixture.plan,fixture.registry,require_oem=True)
        self.assertEqual(result['oemPlacement'],'ORIGINAL_SEMANTIC_PLACEMENT_CHECKED')
        visual['oemLogoPlacement']['assetPath']='../outside.png'
        with self.assertRaisesRegex(ValueError,'safe relative'):gaming.check(fixture.plan,fixture.registry,require_oem=True)


class ConnectorRun(unittest.TestCase):
    def setup_run(self, root, mode='CONNECTOR'):
        p=simple_product(root);run=root/'run'
        with patch.object(guard,'workflow',return_value='a'*40):
            runs.create(run,p,'TASK-TEST','RUN-TEST','Synthetic user instruction',mode,'a'*40)
        evidence=root/'tool-evidence.json'
        g.write(evidence,{'source':mode,'outcome':'SUCCEEDED','notes':'Synthetic connector receipt only','id':'synthetic-file'})
        return p,run,evidence

    def test_connector_execution_has_no_browser_result_requirement(self):
        with tempfile.TemporaryDirectory() as temp:
            p,run,evidence=self.setup_run(Path(temp))
            self.assertEqual(runs.record_evidence(run,evidence)['execution']['state'],'COMPLETED')
            self.assertFalse((run/'browser-result.json').exists())
            self.assertEqual(runs.validate(run,p)['deliveryState'],'NOT_PREPARED')

    def test_evidence_tamper_source_mismatch_and_missing_execution_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            p,run,evidence=self.setup_run(Path(temp));data=g.read(evidence);data['source']='BROWSER';g.write(evidence,data)
            with self.assertRaisesRegex(ValueError,'source differs'):runs.record_evidence(run,evidence)
            data['source']='CONNECTOR';g.write(evidence,data);saved=runs.record_evidence(run,evidence)
            (run/saved['execution']['evidence'][0]['path']).write_text('{}',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'changed'):runs.validate(run)

    def test_run_paths_reject_traversal_and_real_links(self):
        with tempfile.TemporaryDirectory() as temp:
            p,run,evidence=self.setup_run(Path(temp))
            for value in ('../outside.json','/absolute.json','C:/private.json','evidence/../outside.json'):
                with self.subTest(value=value),self.assertRaises(ValueError):runs.safe_file(run,value)
            link=run/'link'
            try:link.symlink_to(Path(temp),target_is_directory=True)
            except OSError:return
            with self.assertRaisesRegex(ValueError,'link'):runs.safe_file(run,'link/file.json')

    def test_recorded_partial_execution_cannot_be_promoted_by_editing_its_manifest(self):
        with tempfile.TemporaryDirectory() as temp:
            p,run,evidence=self.setup_run(Path(temp))
            data=g.read(evidence);data['outcome']='PARTIAL';g.write(evidence,data)
            recorded=runs.record_evidence(run,evidence)
            self.assertEqual(recorded['execution']['state'],'PARTIAL')
            recorded['execution']['state']='COMPLETED';g.write(run/'run-manifest.json',recorded)
            with self.assertRaisesRegex(ValueError,'recorded outcomes'):runs.validate(run)
            recorded['execution']['state']='PARTIAL';recorded['publicationState']='PUBLISHED'
            g.write(run/'run-manifest.json',recorded)
            with self.assertRaisesRegex(ValueError,'publication'):runs.validate(run)

    def test_complete_single_main_run_stages_real_production_checked_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);p,run,evidence=self.setup_run(root);selected_reviews(p,[MAIN]);g.accept_partial(p,[MAIN])
            request={'mode':'IMAGE_ADJUSTMENT_WORKFLOW','runId':'RUN-TEST','configurationId':'BASE-A',
                     'requestReference':'Synthetic user selected one main','allowedChanges':[MAIN],
                     'outputs':{MAIN:'IMAGE'},'selectedSlots':[MAIN],
                     'styleApproval':{'userReference':'Synthetic explicit approval','styleLockSha256':guard.sha(p/'style-lock.json')}}
            contract=root/'contract.json'
            with patch.object(guard,'workflow',return_value='a'*40):
                g.write(contract,guard.capture(p,request))
                runs.record_evidence(run,evidence)
                plan=runs.stage(run,p,contract,guard.sha(contract),[MAIN])
            self.assertEqual(len(plan['files']),1)
            self.assertEqual(plan['productionScope']['state'],'PRODUCTION_SCOPE_CHECK_PASS')
            self.assertEqual(runs.validate(run)['deliveryState'],'STAGED_NOT_UPLOADED')
            self.assertEqual(runs.validate(run)['publicationState'],'NOT_PERFORMED')
            with self.assertRaisesRegex(ValueError,'immutable'):runs.record_evidence(run,evidence)
            (run/'delivery-plan.json').write_text('{}',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'plan changed'):runs.validate(run)


if __name__=='__main__':unittest.main()
