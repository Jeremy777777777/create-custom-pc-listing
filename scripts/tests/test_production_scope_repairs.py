"""Synthetic production-boundary regressions; no real facts or remote actions."""
import contextlib
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from datetime import datetime, timezone

sys.path[:0]=[str(Path(__file__).resolve().parents[1]),str(Path(__file__).resolve().parent)]
import gallery_engine as g
import image_review_scope as scope
import image_fact_update as update
import listing_draft as draft
import production_guard as guard
import drive_delivery as drive
import delivery_context as dc
import delivery_privacy as privacy
import workflow_run as runs
import research_export as export
import test_followup_workflow_fixes as images
import test_listing_draft as drafts
from test_release_checks import trace_for
from reference_fixtures import write_audit

class ScopedFacts(unittest.TestCase):
    def fixture(self, root):
        p,data,c,_,fact=images.ImageFactUpdates().fixture(root)
        return p,data,c,fact

    def test_ports_review_ignores_unshown_unresolved_cpu_but_checks_its_own_dependencies(self):
        with tempfile.TemporaryDirectory() as raw:
            p,data,c,fact=self.fixture(Path(raw))
            cpu=next(f for f in data['facts'] if f['attribute']=='CPU Model Manufacturer')
            cpu.update(status='TBD',final_value=None);g.write(p/'research-ledger.json',data)
            frozen=update.capture(p,c['imageFactUpdate']['scope'])
            g.write(p/'style-lock.json',{'scopeVersion':2,'status':'APPROVED',
                'shared':{'designSeries':'BUSINESS_LAPTOP'},'slots':{'PT08.png':{'status':'APPROVED','approvalReference':'Synthetic actual port selection'}}})
            deps={'scopeVersion':2,'fields':[['Product Details','Total USB 3.0 Ports']],
                  'productPaths':[],'basis':'Synthetic port-only claim'}
            old=scope.binding(p,'PT08.png',deps)
            self.assertEqual(update.check(p,frozen)['state'],'SCOPED_IMAGE_FACT_UPDATE_CHECKED')
            fact['final_value']=5;g.write(p/'research-ledger.json',data)
            self.assertNotEqual(scope.binding(p,'PT08.png',deps),old)
            cpu_deps={**deps,'fields':[['Product Details','CPU Model Manufacturer']]}
            with self.assertRaisesRegex(ValueError,'CPU'):scope.binding(p,'PT08.png',cpu_deps)
            legacy={**deps,'scopeVersion':1}
            with self.assertRaisesRegex(ValueError,'CPU'):scope.binding(p,'PT08.png',legacy)
            fact.update(status='TBD',final_value=None)
            fact['evidence']['research_trace']=trace_for(fact)
            g.write(p/'research-ledger.json',data)
            with self.assertRaisesRegex(ValueError,'Unresolved depicted'):scope.binding(p,'PT08.png',deps)

    def test_scoped_research_can_retain_old_fact_add_factory_evidence_and_select_new_sold_fact(self):
        with tempfile.TemporaryDirectory() as raw:
            p,data,c,fact=self.fixture(Path(raw))
            current=copy.deepcopy(c['imageFactUpdate']['baselineLedger'])
            sold=copy.deepcopy(fact);sold['id']='new-sold-port-evidence'
            factory=copy.deepcopy(fact);factory.update(id='new-factory-port-evidence',fact_scope='FACTORY')
            current['facts'] += [factory,sold]
            next(m for m in current['fields'] if m['attribute']=='Total USB 3.0 Ports')['selected_fact']=sold['id']
            g.write(p/'research-ledger.json',current)
            self.assertEqual(update.check(p,c['imageFactUpdate'])['state'],'SCOPED_IMAGE_FACT_UPDATE_CHECKED')
            oldid=next(f['id'] for f in c['imageFactUpdate']['baselineLedger']['facts'] if f['attribute']=='Total USB 3.0 Ports')
            current['facts']=[f for f in current['facts'] if f['id']!=oldid];g.write(p/'research-ledger.json',current)
            with self.assertRaisesRegex(ValueError,'Preserve prior'):update.check(p,c['imageFactUpdate'])

    def test_missing_and_unknown_metadata_parents_are_allowed_without_hiding_sibling_changes(self):
        for initial in ('absent',None):
            with self.subTest(initial=initial),tempfile.TemporaryDirectory() as raw:
                p,data,_,_=self.fixture(Path(raw));facts=g.read(p/'product-facts.json')
                if initial is None:facts['display']=None;g.write(p/'product-facts.json',facts)
                declared={'fields':[['Product Details','Resolution']],'productPaths':['/display/resolution'],
                          'basis':'Synthetic display detail correction'}
                frozen=update.capture(p,declared)
                resolution=next(f for f in data['facts'] if f['attribute']=='Resolution')
                resolution.update(status='VERIFIED',final_value='1920 x 1080',applies_to_sold_configuration=True,transfer_basis='Synthetic exact panel')
                resolution.setdefault('evidence',{})['research_trace']=trace_for(resolution)
                g.write(p/'research-ledger.json',data);facts['display']={'resolution':'1920 x 1080'};g.write(p/'product-facts.json',facts)
                self.assertEqual(update.check(p,frozen)['state'],'SCOPED_IMAGE_FACT_UPDATE_CHECKED')
                facts['display']['refreshHz']=144;g.write(p/'product-facts.json',facts)
                with self.assertRaisesRegex(ValueError,'outside declared'):update.check(p,frozen)

    def test_known_metadata_scalar_cannot_be_replaced_by_an_object(self):
        with self.assertRaises(ValueError):update.mask_product({'display':'Meaningful existing value'},['/display/resolution'])

    def test_new_serial_lookup_is_bounded_to_declared_fields(self):
        with tempfile.TemporaryDirectory() as raw:
            p,data,c,fact=self.fixture(Path(raw))
            scope_decl={**c['imageFactUpdate']['scope'],'serialResearchUpdate':True}
            frozen=update.capture(p,scope_decl)
            factory=copy.deepcopy(fact);factory.update(id='serial-factory-port',fact_scope='FACTORY')
            factory['evidence']['unit_evidence_alias']='UNIT-AUDIT'
            data['facts'].append(factory)
            data['serial_research'].update(workflow_mode='IMAGE_ADJUSTMENT_WORKFLOW',outcome='COMPLETED',
                sources_attempted=['Synthetic exact-product source'],resolved_fact_ids=[factory['id']],
                reconciliation='Synthetic current sold ports match the linked factory source',
                units=[{'unit_evidence_alias':'UNIT-AUDIT','serial_source_kind':'CURRENT','erp_record_reference':'Synthetic product reference',
                    'target_configuration':'BASE-A','batch_match_basis':'Synthetic same unit','returned_model':'Synthetic exact model',
                    'oem_configuration_source':'https://example.test/product-parts','fact_ids':[factory['id']]}])
            g.write(p/'research-ledger.json',data)
            self.assertEqual(update.check(p,frozen)['state'],'SCOPED_IMAGE_FACT_UPDATE_CHECKED')
            with self.assertRaisesRegex(ValueError,'outside declared'):
                update.check(p,c['imageFactUpdate'])
            foreign=copy.deepcopy(factory);foreign.update(id='foreign-factory-ram',attribute='RAM Memory Installed')
            data['facts'].append(foreign);data['serial_research']['units'][0]['fact_ids'].append(foreign['id'])
            g.write(p/'research-ledger.json',data)
            with self.assertRaisesRegex(ValueError,'outside declared'):update.check(p,frozen)

class DraftStages(unittest.TestCase):
    def fixture(self, root, build=True):
        p=root/'TEST-PC';p.mkdir();data,ledger=drafts.DraftBundleTests().fixture(p)
        result=draft.build(p) if build else None
        return p,data,ledger,result

    def roles(self, result):
        roles={}
        for name in result['files']:
            roles[name]=('RESEARCH' if 'RESEARCH_REVIEW' in name else 'LISTING' if 'LISTING_DRAFT' in name
                         else 'SOURCE' if name==draft.HTML else 'QA')
        roles.update({'research-ledger.json':'RESEARCH','product-facts.json':'RESEARCH','reference-audit.json':'QA'})
        return roles

    def contract(self, root,p,roles):
        request={'mode':'FULL_LISTING_WORKFLOW','configurationId':'BASE-A','runId':'BATCHES',
                 'requestReference':'Synthetic scope, no provider action','allowedChanges':['delivery-status.json'],
                 'outputs':roles,'selectedSlots':[]}
        with patch.object(guard,'workflow',return_value='a'*40):data=guard.capture(p,request)
        path=root/'contract.json';g.write(path,data)
        return path,data

    def deliver_batch(self, root,p,path,roles,names,label):
        plan=drive.plan(p,'BATCHES',names)
        with patch.object(guard,'workflow',return_value='a'*40):
            plan['productionScope']=guard.verify(p,path,guard.sha(path),names)
        policy=g.read(dc.ROOT/'assets/delivery-storage.json');stamp=datetime.now(timezone.utc).isoformat()
        nodes=[{'id':policy['projectFolderId'],'name':'Project','parents':[]},
               {'id':policy['productsFolderId'],'name':'20_PRODUCTS','parents':[policy['projectFolderId']]},
               {'id':'product','name':'TEST-PC','parents':[policy['productsFolderId']]}]
        for key,name,parent in [('research','03_RESEARCH','product'),('final','FINAL','research'),
                                ('listing','01_LISTING','product'),('qa','04_QA','product'),('source','90_SOURCE','product')]:
            nodes.append({'id':key,'name':name,'parents':[parent]})
        for n in nodes:n.update(mimeType=dc.FOLDER,readBackAtUtc=stamp)
        mapping={'RESEARCH':'final','LISTING':'listing','QA':'qa','SOURCE':'source'}
        remote=[];dest={};screens={}
        for i,row in enumerate(plan['files']):
            name=row['relativePath'];dest[name]=mapping[roles[name]]
            screens[name]=privacy.screen_file(p/name,serials_used=False)
            remote.append({'relativePath':name,'id':label+'-'+str(i),'name':name,'parents':[dest[name]],
                'mimeType':row['mimeType'],'size':row['size'],'downloadedSha256':row['sha256'],
                'readBackAtUtc':stamp,'webViewLink':'https://drive.google.com/file/d/'+label+'-'+str(i)+'/view'})
        ctx={'productId':'TEST-PC','serialsUsed':False,'folders':nodes,'fileRoles':{n:roles[n] for n in names},'privacyChecks':screens}
        files={'plan':plan,'readbacks':{'files':remote},'destinations':dest,'context':ctx}
        for key,data in files.items():g.write(root/(label+'-'+key+'.json'),data)
        out=root/(label+'-receipt.json')
        args=['drive_delivery','verify','--product',str(p),'--production-contract',str(path),'--contract-sha256',guard.sha(path),'--output',str(out)]
        for key in files:args += ['--'+key,str(root/(label+'-'+key+'.json'))]
        with patch.object(guard,'workflow',return_value='a'*40),patch.object(sys,'argv',args),contextlib.redirect_stdout(io.StringIO()):drive.main()
        return out

    def test_complete_local_bundle_supports_real_batched_cli_delivery_and_accumulation(self):
        with tempfile.TemporaryDirectory() as raw:
            root=Path(raw);p,_,_,result=self.fixture(root);roles=self.roles(result);path,c=self.contract(root,p,roles)
            first=[n for n in roles if roles[n]=='RESEARCH'];second=[n for n in roles if n not in first]
            a=self.deliver_batch(root,p,path,roles,first,'a')
            b=self.deliver_batch(root,p,path,roles,second,'b')
            self.assertEqual(g.read(b)['deliveryScope'],'BATCH')
            with patch.object(guard,'workflow',return_value='a'*40):
                partial=drive.complete(p,path,guard.sha(path),[a])
                full=drive.complete(p,path,guard.sha(path),[a,b])
            self.assertFalse(partial['allContractedOutputsVerified'])
            self.assertEqual(set(partial['remainingContractedFiles']),set(second))
            self.assertTrue(full['allContractedOutputsVerified'])
            bad=g.read(b);bad['runId']='OTHER';g.write(root/'bad.json',bad)
            with patch.object(guard,'workflow',return_value='a'*40),self.assertRaisesRegex(ValueError,'same-run'):
                drive.complete(p,path,guard.sha(path),[a,root/'bad.json'])
            bad=g.read(b);bad['files'][0]['sha256']='0'*64;g.write(root/'bad.json',bad)
            with patch.object(guard,'workflow',return_value='a'*40),self.assertRaisesRegex(ValueError,'stale'):
                drive.complete(p,path,guard.sha(path),[a,root/'bad.json'])
            badroles={n:r for n,r in roles.items() if n!=draft.HTML}
            with self.assertRaisesRegex(ValueError,'omits'):draft.check_delivery(p,second,roles,contract_outputs=badroles)

    def test_verification_version_can_change_without_rewriting_generation_provenance(self):
        with tempfile.TemporaryDirectory() as raw:
            p,_,ledger,_=self.fixture(Path(raw))
            original=(p/draft.REPORT).read_bytes();record=g.read(p/draft.REPORT)
            with patch.object(draft.subprocess,'check_output',return_value='b'*40+'\n'):
                result=draft.verify(p)
            self.assertEqual(result['generationWorkflowSha'],record['inputs']['workflowSha'])
            self.assertEqual(result['verificationWorkflowSha'],'b'*40)
            self.assertEqual((p/draft.REPORT).read_bytes(),original)
            ledger.write_bytes(ledger.read_bytes()+b'\n')
            with self.assertRaisesRegex(ValueError,'stale'):draft.verify(p)

    def test_actual_single_workbook_revision_uses_frozen_reuse_sources_and_current_copy_checks(self):
        with tempfile.TemporaryDirectory() as raw:
            root=Path(raw);p,data,ledger,_=self.fixture(root,False)
            (p/'inputs').mkdir();previous=p/'inputs/previous-ledger.json';previous.write_bytes(ledger.read_bytes())
            review={'productId':'TEST-PC','configurationId':'BASE-A','previousLedgerSha256':guard.sha(previous),
                    'baselineReference':'Synthetic prior coherent Drive receipt','reviewer':'Synthetic','reviewed_date':'2026-10-30',
                    'impact_review':'Synthetic title wording only; all actual traces retained','fields':[]}
            reuse=p/'inputs/reuse-review.json';g.write(reuse,review)
            book='TEST-PC_LISTING_DRAFT.xlsx';summary='TEST-PC_LISTING_DRAFT.research-summary.json'
            outputs={book:'LISTING',summary:'LISTING','product-facts.json':'RESEARCH','research-ledger.json':'RESEARCH','reference-audit.json':'QA'}
            request={'mode':'FULL_LISTING_WORKFLOW','configurationId':'BASE-A','runId':'REVISION','requestReference':'Synthetic explicit title revision',
                     'allowedChanges':[book,summary,'research-ledger.json','reference-audit.json'],'outputs':outputs,'selectedSlots':[],
                     'listingRevision':{'fields':[['Product Details','Item Name']],'productPaths':[],
                        'previousLedgerPath':'inputs/previous-ledger.json','reuseReviewPath':'inputs/reuse-review.json',
                        'baselineReference':review['baselineReference'],'basis':'Synthetic exact requested title change'}}
            with patch.object(guard,'workflow',return_value='a'*40):contract=guard.capture(p,request)
            contract_path=root/'revision.json';g.write(contract_path,contract)
            title=next(f for f in data['facts'] if f['attribute']=='Item Name')
            title['final_value']=title['final_value'].replace('Desktop,','Business Desktop,')
            g.write(ledger,data);write_audit(ledger)
            args=['research_export','--ledger',str(ledger),'--workbook',str(p/book),'--write-workbook','--stage','LISTING_DRAFT',
                  '--previous-ledger',str(previous),'--research-reuse',str(reuse)]
            with patch.object(sys,'argv',args),contextlib.redirect_stdout(io.StringIO()):export.main()
            with patch.object(guard,'workflow',return_value='a'*40):checked=guard.verify(p,contract_path,guard.sha(contract_path))
            self.assertEqual(checked['checks']['listingDraftBundle']['state'],'SCOPED_LISTING_REVISION_CHECKED')
            self.assertFalse(checked['checks']['listingDraftBundle']['fullBundlePass'])
            self.assertFalse((p/'TEST-PC_RESEARCH_REVIEW.xlsx').exists())
            other=next(f for f in data['facts'] if f['attribute']=='Manufacturer');other['source']='Unrequested source modification';g.write(ledger,data)
            with self.assertRaisesRegex(ValueError,'outside its declared'):
                draft.check_revision(p,contract['listingRevision'],outputs)
            previous.write_bytes(previous.read_bytes()+b'\n')
            with self.assertRaisesRegex(ValueError,'baseline/reuse'):
                draft.check_revision(p,contract['listingRevision'],outputs)

    def test_run_creation_rejects_a_mismatched_checkout_before_creating_records(self):
        with tempfile.TemporaryDirectory() as raw:
            root=Path(raw);p=root/'TEST-PC';p.mkdir()
            g.write(p/'product-facts.json',{'internalId':'TEST-PC'})
            with patch.object(guard,'workflow',return_value='a'*40),self.assertRaisesRegex(ValueError,'pinned'):
                runs.create(root/'run',p,'TASK','RUN','Synthetic actual task','LOCAL','b'*40)
            self.assertFalse((root/'run').exists())

if __name__=='__main__':unittest.main()
