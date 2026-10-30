"""Synthetic regressions for customization review and real batched entry points."""
import contextlib
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from PIL import Image
sys.path[:0] = [str(Path(__file__).resolve().parents[1]), str(Path(__file__).resolve().parent)]
import gallery_engine as g
import image_review_scope as scope
import image_customization_plan as choices
import production_guard as guard
import workflow_run as runs
import drive_delivery as drive
import delivery_context as dc
import delivery_privacy as privacy
import test_customization_policy as fixtures


class CustomizationReview(unittest.TestCase):
    def fixture(self, root):
        p = root/'TEST-PC'; p.mkdir()
        data, product, _, _ = fixtures.CustomizationTests().fixture(p)
        g.write(p/'product-facts.json', product); g.write(p/'research-ledger.json', data)
        g.write(p/'style-lock.json', {'scopeVersion':2, 'status':'APPROVED',
            'shared':{'designSeries':'BUSINESS_LAPTOP'},
            'slots':{n:{'status':'APPROVED','approvalReference':'Synthetic reviewed selection'}
                     for n in ('PT05.png','PT08.png')}})
        Image.new('RGB',(600,500),'white').save(p/'PT05.png')
        deps = {'scopeVersion':2, 'fields':[['Product Details','RAM Memory Installed'],
            ['Product Details','RAM Memory Technology']], 'productPaths':[],
            'basis':'Synthetic RAM options and exact memory generation'}
        return p, data, product, deps

    def test_changed_ram_branch_invalidates_actual_saved_review(self):
        with tempfile.TemporaryDirectory() as raw:
            p, data, product, deps = self.fixture(Path(raw))
            before = scope.binding(p,'PT05.png',deps)
            report = {'schemaVersion':4,'result':'PASS','reviewer':'Synthetic fixture only',
                'reviewedAtUtc':'2026-10-30T12:00:00Z','images':[{'file':'PT05.png',
                'sha256':g.digest(p/'PT05.png'),'result':'PASS','notes':'Synthetic review only',
                'customerText':['Choose Your Memory and Storage'],'dependencies':deps,'reviewInputsSha256':before}]}
            g.review_record(report,['PT05.png'],p)
            ram = next(f for f in data['facts'] if f['attribute']=='RAM Memory Installed')
            ram['evidence']['customization_ram']['replaceable'] = False
            g.write(p/'research-ledger.json',data)
            self.assertNotEqual(before,scope.binding(p,'PT05.png',deps))
            with self.assertRaisesRegex(ValueError,'binding stale'):
                g.review_record(report,['PT05.png'],p)
            plan=choices.build(product,data,guard.sha(p/'product-facts.json'),guard.sha(p/'research-ledger.json'))
            self.assertEqual(plan['ram']['tiers'],[])
            self.assertEqual(plan['ram']['label'],'16GB DDR5 RAM (Fixed)')

    def test_type_source_status_and_evidence_removal_change_dependent_binding(self):
        with tempfile.TemporaryDirectory() as raw:
            p, data, _, deps = self.fixture(Path(raw)); original=copy.deepcopy(data)
            before=scope.binding(p,'PT05.png',deps)
            for changes in ({'memoryTypeSource':'https://example.test/another-source'},
                            {'replaceabilitySource':'https://example.test/another-manual'},
                            {'status':'CONFLICT'}, {'memoryType':'DDR4'}, None):
                current=copy.deepcopy(original)
                ram=next(f for f in current['facts'] if f['attribute']=='RAM Memory Installed')
                if changes is None:ram['evidence'].pop('customization_ram')
                else:ram['evidence']['customization_ram'].update(changes)
                g.write(p/'research-ledger.json',current)
                with self.subTest(changes=changes):self.assertNotEqual(before,scope.binding(p,'PT05.png',deps))

    def test_pt05_automatically_binds_branch_but_unrelated_ports_do_not(self):
        with tempfile.TemporaryDirectory() as raw:
            p, data, _, _=self.fixture(Path(raw))
            deps={'scopeVersion':2,'fields':[['Product Details','Manufacturer']],
                  'productPaths':[],'basis':'Synthetic product identity, no explicit RAM declaration'}
            old={n:scope.binding(p,n,deps) for n in ('PT05.png','PT08.png')}
            next(f for f in data['facts'] if f['attribute']=='RAM Memory Installed')['evidence']['customization_ram']['replaceable']=False
            g.write(p/'research-ledger.json',data)
            self.assertNotEqual(old['PT05.png'],scope.binding(p,'PT05.png',deps))
            self.assertEqual(old['PT08.png'],scope.binding(p,'PT08.png',deps))

    def test_historical_policy_retains_old_binding_shape_without_current_pass(self):
        with tempfile.TemporaryDirectory() as raw:
            p,data,_,deps=self.fixture(Path(raw))
            old_policy=g.read(Path(g.__file__).resolve().parents[1]/scope.SCOPED_POLICY)
            old_policy['imageReview'].pop('customization')
            policy={'__scopedImagePolicy__':json.dumps(old_policy)}
            old=scope.binding(p,'PT05.png',deps,policy)
            self.assertNotEqual(old,scope.binding(p,'PT05.png',deps))
            next(f for f in data['facts'] if f['attribute']=='RAM Memory Installed')['evidence']['customization_ram']['replaceable']=False
            g.write(p/'research-ledger.json',data)
            self.assertEqual(old,scope.binding(p,'PT05.png',deps,policy))


class DeliveryBatches(unittest.TestCase):
    def fixture(self, root):
        p=root/'TEST-PC';p.mkdir()
        g.write(p/'product-facts.json',{'internalId':'TEST-PC','selectedBaseConfiguration':{'id':'BASE-A'}})
        for n in ('a.json','b.json'):g.write(p/n,{'synthetic':n})
        request={'mode':'FULL_LISTING_WORKFLOW','configurationId':'BASE-A','runId':'BATCHES',
            'requestReference':'Synthetic actual scope','allowedChanges':['a.json','b.json'],
            'outputs':{'a.json':'QA','b.json':'QA'},'selectedSlots':[]}
        with patch.object(guard,'workflow',return_value='a'*40):
            cp=root/'contract.json';g.write(cp,guard.capture(p,request))
            run=root/'run';runs.create(run,p,'TASK','BATCHES','Synthetic actual request','LOCAL','a'*40)
        evidence=root/'evidence.json';g.write(evidence,{'source':'LOCAL','outcome':'SUCCEEDED','notes':'Synthetic fixture execution; no remote action'})
        runs.record_evidence(run,evidence)
        return p,cp,run,request

    def stage(self,run,p,cp,files,batch_id=None):
        with patch.object(guard,'workflow',return_value='a'*40):
            return runs.stage(run,p,cp,guard.sha(cp),files,batch_id)

    def receipt(self,root,p,cp,name,label,file_id):
        plan=drive.plan(p,'BATCHES',[name]);stamp=datetime.now(timezone.utc).isoformat()
        policy=g.read(dc.ROOT/'assets/delivery-storage.json')
        nodes=[{'id':policy['projectFolderId'],'name':'Project','parents':[]},
            {'id':policy['productsFolderId'],'name':'20_PRODUCTS','parents':[policy['projectFolderId']]},
            {'id':'p','name':'TEST-PC','parents':[policy['productsFolderId']]},
            {'id':'qa','name':'04_QA','parents':['p']}]
        for n in nodes:n.update(mimeType=dc.FOLDER,readBackAtUtc=stamp)
        row=plan['files'][0]
        observed={'files':[{'relativePath':name,'id':file_id,'name':name,'parents':['qa'],
            'mimeType':row['mimeType'],'size':row['size'],'downloadedSha256':row['sha256'],
            'readBackAtUtc':stamp,'webViewLink':'https://drive.google.com/file/d/'+file_id+'/view'}]}
        ctx={'productId':'TEST-PC','serialsUsed':False,'folders':nodes,'fileRoles':{name:'QA'},
             'privacyChecks':{name:privacy.screen_file(p/name,serials_used=False)}}
        records={'plan':plan,'readbacks':observed,'destinations':{name:'qa'},'context':ctx}
        output=root/(label+'-receipt.json')
        argv=['drive_delivery','verify','--product',str(p),'--production-contract',str(cp),
              '--contract-sha256',guard.sha(cp),'--output',str(output)]
        for flag,data in records.items():
            path=root/(label+'-'+flag+'.json');g.write(path,data);argv+=['--'+flag,str(path)]
        with patch.object(guard,'workflow',return_value='a'*40),patch.object(sys,'argv',argv),contextlib.redirect_stdout(io.StringIO()):drive.main()
        return output

    def test_same_run_cli_stages_two_immutable_plans(self):
        with tempfile.TemporaryDirectory() as raw:
            root=Path(raw);p,cp,run,_=self.fixture(root)
            first=self.stage(run,p,cp,['a.json']);before=(run/'delivery-plan.json').read_bytes()
            argv=['workflow_run','stage','--run',str(run),'--product',str(p),'--production-contract',str(cp),
                  '--contract-sha256',guard.sha(cp),'--file','b.json','--batch-id','remaining']
            output=io.StringIO()
            with patch.object(guard,'workflow',return_value='a'*40),patch.object(sys,'argv',argv),contextlib.redirect_stdout(output):runs.main()
            result=json.loads(output.getvalue())
            self.assertEqual(result['planRelativePath'],'delivery-plans/remaining.json')
            manifest=runs.validate(run,p)
            self.assertEqual(len(manifest['deliveryBatches']),2)
            self.assertEqual((run/'delivery-plan.json').read_bytes(),before)
            self.assertEqual(first['batchId'],'batch-001')
            self.assertEqual(manifest['deliveryState'],'STAGED_NOT_UPLOADED')
            (run/'delivery-plans/remaining.json').write_text('{}',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'plan changed'):runs.validate(run,p)

    def test_legacy_manifest_appends_without_rewriting_old_plan(self):
        with tempfile.TemporaryDirectory() as raw:
            p,cp,run,_=self.fixture(Path(raw));self.stage(run,p,cp,['a.json'])
            before=(run/'delivery-plan.json').read_bytes();data=g.read(run/'run-manifest.json')
            data.pop('deliveryBatches');data.pop('deliveryContractSha256');g.write(run/'run-manifest.json',data)
            plan=self.stage(run,p,cp,['b.json'])
            self.assertEqual(plan['batchId'],'batch-002')
            self.assertEqual((run/'delivery-plan.json').read_bytes(),before)
            self.assertEqual(len(runs.validate(run,p)['deliveryBatches']),2)

    def test_duplicate_batch_and_changed_contract_fail_without_altering_manifest(self):
        with tempfile.TemporaryDirectory() as raw:
            root=Path(raw);p,cp,run,request=self.fixture(root);self.stage(run,p,cp,['a.json'],'first')
            original=(run/'run-manifest.json').read_bytes()
            for label in ('first','FIRST','../outside'):
                with self.subTest(label=label),self.assertRaises(ValueError):self.stage(run,p,cp,['b.json'],label)
            other=root/'other-contract.json';changed={**g.read(cp),'requestReference':'Synthetic changed scope'};g.write(other,changed)
            with self.assertRaisesRegex(ValueError,'same frozen contract'):self.stage(run,p,other,['b.json'])
            self.assertEqual((run/'run-manifest.json').read_bytes(),original)

    def test_cross_batch_id_collision_fails_after_real_cli_batch_checks(self):
        with tempfile.TemporaryDirectory() as raw:
            root=Path(raw);p,cp,_,_=self.fixture(root)
            a=self.receipt(root,p,cp,'a.json','a','shared-id')
            b=self.receipt(root,p,cp,'b.json','b','shared-id')
            with patch.object(guard,'workflow',return_value='a'*40),self.assertRaisesRegex(ValueError,'ID reused'):
                drive.complete(p,cp,guard.sha(cp),[a,b])

    def test_distinct_ids_complete_and_same_file_rechecks_are_idempotent(self):
        with tempfile.TemporaryDirectory() as raw:
            root=Path(raw);p,cp,_,_=self.fixture(root)
            a=self.receipt(root,p,cp,'a.json','a','file-a')
            b=self.receipt(root,p,cp,'b.json','b','file-b')
            with patch.object(guard,'workflow',return_value='a'*40):
                partial=drive.complete(p,cp,guard.sha(cp),[a,a])
                complete=drive.complete(p,cp,guard.sha(cp),[a,b,a])
            self.assertEqual(partial['deliveryState'],'DRIVE_DELIVERY_PARTIAL')
            self.assertEqual(partial['remainingContractedFiles'],['b.json'])
            self.assertTrue(complete['allContractedOutputsVerified'])
            self.assertEqual(len(complete['files']),2)


if __name__=='__main__':unittest.main()
