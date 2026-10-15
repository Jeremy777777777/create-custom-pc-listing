"""Cross-stage audit regressions; synthetic metadata/workbooks only."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
import test_research_export as ef
import test_research_handoff as hf
from product_identity import product_id
from product_metadata import listing_view,hardware_projection,check_image_cache
from research_handoff import check_product_location,internal_storage_configuration
from listing_content import capacity_mentions


class OverallAuditTests(unittest.TestCase):
    def test_identifier_aliases_must_agree_and_erp_id_stays_separate(self):
        raw={'productId':'TEST-PC','internalId':'TEST-PC','identity':{'internalId':'TEST-PC','erpProductId':20744}}
        self.assertEqual(product_id(raw),'TEST-PC')
        self.assertIsNone(product_id({'identity':'Legacy display name'}))
        for key,value in (('productId','OTHER'),('internalId','OTHER'),('productId',123),('internalId',' ')):
            altered=copy.deepcopy(raw);altered[key]=value
            with self.subTest(key=key,value=value),self.assertRaises(ValueError):product_id(altered)

    def test_conflicting_product_aliases_fail_export_image_and_directory_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);helper=ef.ResearchExportTests();book,data,path,ledger=helper.full_fixture(root);book.close()
            source=root/'product-facts.json';raw=json.loads(source.read_text());raw['productId']='OTHER-PC'
            source.write_text(json.dumps(raw));before=source.read_bytes()
            functions=(lambda:helper.export_run(ledger,path),lambda:listing_view(raw,data),lambda:hardware_projection(data,raw),
                       lambda:check_product_location(root/'product generated photo/TEST-PC/review.xlsx','TEST-PC',raw))
            for fn in functions:
                with self.assertRaisesRegex(ValueError,'conflicting internal product identifiers'):fn()
            self.assertEqual(source.read_bytes(),before)

    def test_grouped_capacity_numbers_parse_consistently_in_copy_and_cache(self):
        self.assertEqual(list(capacity_mentions('1,000GB SSD')),[(1000.0,'ssd')])
        self.assertEqual(list(capacity_mentions('65,536MB RAM 1,256GB total storage',True)),[(64.0,'ram'),(1256.0,'total_storage')])
        for malformed in ('1,00GB SSD','1,000,00GB SSD','1,5TB HDD'):
            with self.subTest(malformed=malformed),self.assertRaisesRegex(ValueError,'thousands separators'):
                list(capacity_mentions(malformed))
        selected={('Product Details','Hard Disk Size'):{'status':'VERIFIED','final_value':1},
                  ('Product Details','Hard Disk Size Unit'):{'status':'VERIFIED','final_value':'TB'}}
        check_image_cache(selected,{'internalStorage':'1,000GB NVMe SSD'})
        with self.assertRaisesRegex(ValueError,'thousands separators'):check_image_cache(selected,{'internalStorage':'1,00GB SSD'})
        with tempfile.TemporaryDirectory() as tmp:
            helper,data,path,ledger=hf.HandoffTests().fixture(Path(tmp),capacity=1256,components=True)
            data['facts'][-1]['final_value']=1000;data['facts'][-1]['evidence']['storage_medium']='INTERNAL_HDD'
            title=next(f for f in data['facts'] if f['attribute']=='Item Name')
            title['final_value']=title['final_value'].replace(' Win 11 Pro',' + 1,000GB HDD Win 11 Pro')
            hf.HandoffTests().save(data,path,ledger)
            self.assertEqual(helper.export_run(ledger,path)['result'],'EXPORT_EVIDENCE_CHECK_PASS')

    def test_bom_quantity_requires_per_physical_drive_facts(self):
        with tempfile.TemporaryDirectory() as tmp:
            test=hf.HandoffTests();helper,data,path,ledger=test.fixture(Path(tmp),components=True)
            original=copy.deepcopy(data)
            for quantity in (2,'2',0,-1,True,'two',None):
                altered=copy.deepcopy(original);altered['facts'][-1]['evidence']['part_quantity']=quantity
                test.save(altered,path,ledger)
                with self.subTest(quantity=quantity),self.assertRaisesRegex(ValueError,'one physical drive'):
                    helper.export_run(ledger,path)
                with self.assertRaisesRegex(ValueError,'one physical drive'):hardware_projection(altered)
            for quantity in (1,1.0,'1'):
                altered=copy.deepcopy(original);altered['facts'][-1]['evidence']['part_quantity']=quantity
                self.assertEqual(internal_storage_configuration(altered)['totalGB'],512)
            unresolved=copy.deepcopy(original)
            unresolved['facts'][-1].update(status='TBD',final_value=None)
            unresolved['facts'][-1]['evidence']['part_quantity']=None
            self.assertTrue(hardware_projection(unresolved)['storageDependencies'])
            with self.assertRaisesRegex(ValueError,'verified applicable'):internal_storage_configuration(unresolved)
            # A real quantity-two BOM is represented by two explicit drive facts.
            extra=data['facts'][-1];extra['evidence']['part_quantity']=1
            third=copy.deepcopy(extra);third.update(id='third',attribute='Additional internal drive capacity 3')
            data['facts'].append(third)
            total=next(f for f in data['facts'] if f['attribute']=='Memory Storage Capacity')
            total['final_value']=768;total['evidence']['storage_component_fact_ids'].append('third')
            test.save(data,path,ledger)
            self.assertEqual(helper.export_run(ledger,path)['result'],'EXPORT_EVIDENCE_CHECK_PASS')


if __name__=='__main__':unittest.main()
