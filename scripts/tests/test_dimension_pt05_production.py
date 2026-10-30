"""Synthetic final-entry regressions; never actual product/image approvals."""
import contextlib
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image

sys.path[:0]=[str(Path(__file__).resolve().parents[1]),str(Path(__file__).resolve().parent)]
import gallery_engine as g
import image_review_scope as scope
import image_fact_update as update
import image_customization_plan as choices
import production_guard as guard
import dimension_units as dimensions
import customer_visible_content as customer
import test_batch_and_customization_repairs as custom
import test_followup_workflow_fixes as facts
import test_workflow_hardening as galleries
from test_release_checks import trace_for


def set_fact(data,field,value):
    fact=next(f for f in data['facts'] if f['attribute']==field)
    fact.update(status='VERIFIED',final_value=value)
    fact.setdefault('evidence',{})['research_trace']=trace_for(fact)
    return fact


class ProductionPT05(unittest.TestCase):
    def fixture(self,root):
        p,data,product,deps=custom.CustomizationReview().fixture(root)
        style=g.read(p/'style-lock.json');helper=galleries.GalleryBoundaries()
        self.addCleanup(helper.doCleanups)
        with contextlib.redirect_stdout(io.StringIO()):helper.build(p)
        g.write(p/'product-facts.json',product);g.write(p/'style-lock.json',style)
        return p,data,product,deps

    def contract(self,root,p):
        request={'mode':'IMAGE_ADJUSTMENT_WORKFLOW','runId':'PT05-TEST','configurationId':'BASE-A',
            'requestReference':'Synthetic requested choices page','selectedSlots':['PT05.png'],
            'allowedChanges':['research-ledger.json','visual-review.json','semantic-review.json','partial-update-qa.json'],
            'outputs':{'PT05.png':'IMAGE'},'styleApproval':{'userReference':'Synthetic selection',
                'styleLockSha256':guard.sha(p/'style-lock.json')}}
        cp=root/'contract.json'
        with patch.object(guard,'workflow',return_value='a'*40):g.write(cp,guard.capture(p,request))
        return cp

    def review(self,p,deps,legacy=False):
        report={'schemaVersion':3 if legacy else 4,'result':'PASS','reviewer':'Synthetic fixture',
            'reviewedAtUtc':'2026-10-30T12:00:00Z','galleryInventorySha256':g.gallery_inventory(p),
            'images':[{'file':'PT05.png','sha256':g.digest(p/'PT05.png'),'result':'PASS',
                'notes':'Synthetic image gate test only','dependencies':deps,
                'reviewInputsSha256':scope.binding(p,'PT05.png',deps),
                'customerText':['Choose Your Memory and Storage']}]}
        if legacy:report['reviewInputsSha256']=g.review_inputs(p)
        for name in ('visual-review.json','semantic-review.json'):g.write(p/name,report)
        with contextlib.redirect_stdout(io.StringIO()):g.accept_partial(p,['PT05.png'])

    def verify(self,p,cp):
        with patch.object(guard,'workflow',return_value='a'*40),contextlib.redirect_stdout(io.StringIO()):
            return guard.verify(p,cp,guard.sha(cp))

    def test_final_entry_rejects_missing_conflicting_or_invalid_ram_research(self):
        for changes in (None,{'status':'CONFLICT'},{'status':'TBD'},{'replaceable':None},
                        {'memoryType':'DDR'},{'memoryType':'DDR4'},{'memoryTypeSource':''}):
            with self.subTest(changes=changes),tempfile.TemporaryDirectory() as raw:
                root=Path(raw);p,data,_,deps=self.fixture(root);cp=self.contract(root,p)
                ram=next(f for f in data['facts'] if f['attribute']=='RAM Memory Installed')
                if changes is None:ram['evidence'].pop('customization_ram')
                else:ram['evidence']['customization_ram'].update(changes)
                g.write(p/'research-ledger.json',data)
                self.review(p,deps)  # A freshly supplied hash cannot evade the final research gate.
                with self.assertRaises(ValueError):self.verify(p,cp)

    def test_legacy_review_cannot_bypass_current_pt05_research_gate(self):
        with tempfile.TemporaryDirectory() as raw:
            root=Path(raw);p,data,_,deps=self.fixture(root)
            set_fact(data,'CPU Model Manufacturer','Intel')
            next(f for f in data['facts'] if f['attribute']=='RAM Memory Installed')['evidence'].pop('customization_ram')
            g.write(p/'research-ledger.json',data);cp=self.contract(root,p)
            self.review(p,deps,legacy=True)
            with self.assertRaisesRegex(ValueError,'researched RAM'):self.verify(p,cp)

    def test_fixed_and_replaceable_pages_pass_without_unshown_cpu_or_storage(self):
        for replaceable,memory_type in ((True,'DDR5'),(False,'LPDDR5X')):
            with self.subTest(replaceable=replaceable),tempfile.TemporaryDirectory() as raw:
                root=Path(raw);p,data,product,deps=self.fixture(root)
                ram=next(f for f in data['facts'] if f['attribute']=='RAM Memory Installed')
                ram['evidence']['customization_ram'].update(replaceable=replaceable,memoryType=memory_type)
                set_fact(data,'RAM Memory Technology',memory_type)
                for field in ('CPU Model Manufacturer','Hard Disk Size'):
                    fact=next(f for f in data['facts'] if f['attribute']==field)
                    fact.update(status='TBD',final_value=None);fact.setdefault('evidence',{})['research_trace']=trace_for(fact)
                g.write(p/'research-ledger.json',data);cp=self.contract(root,p);self.review(p,deps)
                result=self.verify(p,cp)['checks']['customizationImage']
                self.assertEqual(result['state'],'CUSTOMIZATION_RESEARCH_CHECK_PASS')
                self.assertEqual(result['replaceable'],replaceable)
                brief=choices.build(product,data,guard.sha(p/'product-facts.json'),guard.sha(p/'research-ledger.json'))
                self.assertEqual(len(brief['ram']['tiers']),4 if replaceable else 0)
                if not replaceable:self.assertEqual(brief['ram']['fixedCapacityGB'],16)


class DimensionDependencies(unittest.TestCase):
    def fixture(self,root):
        p,data,_,_,_=facts.ImageFactUpdates().fixture(root)
        g.write(p/'style-lock.json',{'scopeVersion':2,'status':'APPROVED',
            'shared':{'designSeries':'BUSINESS_LAPTOP'},'slots':{'PT04.png':{'status':'APPROVED','approvalReference':'Synthetic selection'}}})
        Image.new('RGB',(600,500),'white').save(p/'PT04.png')
        return p,data

    def deps(self,key):
        return {'scopeVersion':2,'fields':[list(key)],'productPaths':[],
                'basis':'Synthetic dimension and its explicit unit dependency'}

    def test_all_numeric_pairs_bind_unit_sources_and_reject_metric_or_unknown_units(self):
        for key,unit_name in dimensions.PAIRS.items():
            with self.subTest(field=key),tempfile.TemporaryDirectory() as raw:
                p,data=self.fixture(Path(raw));set_fact(data,key[1],17);unit=set_fact(data,unit_name,'Inches')
                g.write(p/'research-ledger.json',data);deps=self.deps(key);before=scope.binding(p,'PT04.png',deps)
                unit['source']='Synthetic corrected unit source';g.write(p/'research-ledger.json',data)
                self.assertNotEqual(before,scope.binding(p,'PT04.png',deps))
                unit['final_value']='Centimeters';g.write(p/'research-ledger.json',data)
                with self.assertRaisesRegex(ValueError,'Inches'):scope.binding(p,'PT04.png',deps)
                unit.update(status='TBD',final_value=None);unit['evidence']['research_trace']=trace_for(unit);g.write(p/'research-ledger.json',data)
                with self.assertRaisesRegex(ValueError,'Unresolved depicted dimension'):scope.binding(p,'PT04.png',deps)

    def test_unit_only_dependency_binds_and_checks_the_value(self):
        with tempfile.TemporaryDirectory() as raw:
            p,data=self.fixture(Path(raw));value=set_fact(data,'Screen Size',17);set_fact(data,'Display Size Unit','Inches')
            g.write(p/'research-ledger.json',data);deps=self.deps(('Product Details','Display Size Unit'))
            before=scope.binding(p,'PT04.png',deps);value['final_value']=18;g.write(p/'research-ledger.json',data)
            self.assertNotEqual(before,scope.binding(p,'PT04.png',deps))
            value['final_value']=0;g.write(p/'research-ledger.json',data)
            with self.assertRaisesRegex(ValueError,'Positive numeric'):scope.binding(p,'PT04.png',deps)

    def test_port_revision_preserves_unrelated_legacy_metric_dimensions(self):
        with tempfile.TemporaryDirectory() as raw:
            p,data=self.fixture(Path(raw));set_fact(data,'Item Length Horizontal Edge',35);unit=set_fact(data,'Item Length Unit','Centimeters')
            original=copy.deepcopy(unit);g.write(p/'research-ledger.json',data)
            frozen=update.capture(p,{'fields':[['Product Details','Total USB 3.0 Ports']],
                'productPaths':[],'basis':'Synthetic port-only revision'})
            set_fact(data,'Total USB 3.0 Ports',5);g.write(p/'research-ledger.json',data)
            result=update.check(p,frozen)
            self.assertEqual(result['state'],'SCOPED_IMAGE_FACT_UPDATE_CHECKED')
            self.assertEqual(result['untouchedDimensions'],'UNCHANGED_NOT_REVALIDATED')
            self.assertEqual(original,next(f for f in g.read(p/'research-ledger.json')['facts'] if f['attribute']=='Item Length Unit'))

    def test_declared_dimension_is_converted_to_inches_without_rewriting_source(self):
        with tempfile.TemporaryDirectory() as raw:
            p,data=self.fixture(Path(raw));value=set_fact(data,'Item Length Horizontal Edge',35);unit=set_fact(data,'Item Length Unit','Centimeters')
            value['source']='Synthetic original measurement: 35 cm';source=value['source'];g.write(p/'research-ledger.json',data)
            frozen=update.capture(p,{'fields':[['Product Details','Item Length Horizontal Edge'],['Product Details','Item Length Unit']],
                'productPaths':[],'basis':'Synthetic dimension conversion with its paired unit'})
            with self.assertRaisesRegex(ValueError,'Inches'):update.check(p,frozen)
            value['final_value']=dimensions.to_inches(35,'cm');unit['final_value']='Inches';g.write(p/'research-ledger.json',data)
            self.assertEqual(update.check(p,frozen)['state'],'SCOPED_IMAGE_FACT_UPDATE_CHECKED')
            self.assertEqual(value['final_value'],13.7795);self.assertEqual(value['source'],source)

    def test_current_size_review_rejects_metric_caption_even_with_valid_inch_facts(self):
        with tempfile.TemporaryDirectory() as raw:
            p,data=self.fixture(Path(raw));set_fact(data,'Screen Size',17);set_fact(data,'Display Size Unit','Inches');g.write(p/'research-ledger.json',data)
            deps=self.deps(('Product Details','Screen Size'))
            report={'schemaVersion':4,'result':'PASS','reviewer':'Synthetic','reviewedAtUtc':'2026-10-30T12:00:00Z',
                'images':[{'file':'PT04.png','sha256':g.digest(p/'PT04.png'),'result':'PASS','notes':'Synthetic only',
                    'dependencies':deps,'reviewInputsSha256':scope.binding(p,'PT04.png',deps),'customerText':['17cm display']}]}
            with self.assertRaisesRegex(ValueError,'inches'):g.review_record(report,['PT04.png'],p)
            report['images'][0]['customerText']=['17-inch display'];g.review_record(report,['PT04.png'],p)

    def test_customer_entry_rejects_metric_sizes_but_preserves_technical_connector_names(self):
        for text in ('17cm display','10 cm','15-mm','Width: 20 centimeters','0.3m key travel','2 ft'):
            with self.subTest(text=text),self.assertRaisesRegex(ValueError,'inches'):customer.validate_customer_text(text)
        for text in ('17-inch display','3.5mm audio jack','1 x 3.5mm combo audio jack','Intel 3350M','M.2 2280 SSD'):
            with self.subTest(text=text):customer.validate_customer_text(text)

    def test_historical_policy_does_not_rehash_old_dimension_evidence(self):
        with tempfile.TemporaryDirectory() as raw:
            p,data=self.fixture(Path(raw));set_fact(data,'Screen Size',17);unit=set_fact(data,'Display Size Unit','Inches');g.write(p/'research-ledger.json',data)
            policy=g.read(Path(g.__file__).resolve().parents[1]/scope.SCOPED_POLICY);policy['imageReview'].pop('dimensions')
            historical={'__scopedImagePolicy__':json.dumps(policy)};deps=self.deps(('Product Details','Screen Size'))
            before=scope.binding(p,'PT04.png',deps,historical)
            self.assertNotEqual(before,scope.binding(p,'PT04.png',deps))
            unit['source']='Synthetic newer unit evidence';g.write(p/'research-ledger.json',data)
            self.assertEqual(before,scope.binding(p,'PT04.png',deps,historical))


if __name__=='__main__':unittest.main()
