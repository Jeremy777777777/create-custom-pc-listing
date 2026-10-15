"""Drive labels use decimal units; memory conventions and system-space evidence stay separate."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
import test_research_export as ef
import test_research_handoff as hf
from capacity_units import capacity_units,scaled_capacity
from product_metadata import listing_view,check_image_cache,hardware_projection
from listing_content import capacity_mentions
from research_handoff import internal_storage_configuration


class CapacityBasisTests(unittest.TestCase):
    def test_decimal_drive_units_do_not_change_memory_or_cache_conventions(self):
        self.assertEqual(capacity_units('Hard Disk Size')['tb'],1000)
        self.assertEqual(capacity_units('Memory Storage Capacity')['tb'],1000)
        self.assertEqual(capacity_units('RAM Memory Installed')['tb'],1024)
        self.assertEqual(list(capacity_mentions('16GB RAM 1TB SSD 8MB Cache')),
                         [(16.0,'ram'),(1000.0,'ssd'),(8/1024,'cache')])
        self.assertEqual(scaled_capacity(1.001,1000),1001)
        self.assertEqual(list(capacity_mentions('1.256TB total storage',True)),[(1256.0,'total_storage')])
        self.assertEqual(list(capacity_mentions('16GiB RAM')),[(16.0,'ram')])
        for text in ('1TiB SSD','931GiB storage'):
            with self.subTest(text=text),self.assertRaisesRegex(ValueError,'Binary/system storage'):
                list(capacity_mentions(text))

    def test_adapter_cache_and_export_agree_on_1tb_1000gb(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);helper=ef.ResearchExportTests();book,data,path,ledger=helper.full_fixture(root);book.close()
            fields={f['attribute']:f for f in data['facts'] if f['sheet']=='Product Details'}
            fields['Hard Disk Size']['final_value']=1;fields['Hard Disk Size Unit']['final_value']='TB'
            fields['Item Name']['final_value']=fields['Item Name']['final_value'].replace('256GB SSD','1TB SSD')
            fields['Memory Storage Capacity'].update(status='VERIFIED',final_value=1000)
            fields['Memory Storage Capacity Unit'].update(status='VERIFIED',final_value='GB')
            raw=json.loads((root/'product-facts.json').read_text());raw['selectedBaseConfiguration']['ssdGB']=1000
            (root/'product-facts.json').write_text(json.dumps(raw));hf.HandoffTests().save(data,path,ledger)
            self.assertEqual(listing_view(raw,data)[0]['selectedBaseConfiguration']['ssdGB'],1000)
            self.assertEqual(helper.export_run(ledger,path)['result'],'EXPORT_EVIDENCE_CHECK_PASS')
            selected={('Product Details','Hard Disk Size'):fields['Hard Disk Size'],('Product Details','Hard Disk Size Unit'):fields['Hard Disk Size Unit']}
            check_image_cache(selected,{'internalStorage':'1TB NVMe SSD'})
            check_image_cache(selected,{'selectedBaseConfiguration':{'ssdGB':1000}})
            with self.assertRaisesRegex(ValueError,'capacity conflict'):
                check_image_cache(selected,{'selectedBaseConfiguration':{'ssdGB':1024}})
            with self.assertRaisesRegex(ValueError,'binary/system capacity'):
                check_image_cache(selected,{'internalStorage':'931GiB SSD'})

    def test_decimal_multi_drive_total_accepts1256_and_rejects1280(self):
        for total,valid in ((1256,True),(1280,False)):
            with tempfile.TemporaryDirectory() as tmp:
                test=hf.HandoffTests();helper,data,path,ledger=test.fixture(Path(tmp),capacity=total,components=True)
                extra=data['facts'][-1];extra['final_value']=1
                extra['evidence'].update(capacity_unit='TB',storage_medium='INTERNAL_HDD',capacity_basis='DECIMAL_MARKETING')
                test.save(data,path,ledger)
                self.assertEqual(internal_storage_configuration(data)['totalGB'],1256)
                if valid:self.assertEqual(helper.export_run(ledger,path)['result'],'EXPORT_EVIDENCE_CHECK_PASS')
                else:
                    with self.assertRaisesRegex(ValueError,'storage capacity fields disagree'):helper.export_run(ledger,path)

    def test_known_system_measurement_cannot_replace_nominal_storage(self):
        with tempfile.TemporaryDirectory() as tmp:
            test=hf.HandoffTests();helper,data,path,ledger=test.fixture(Path(tmp),components=True)
            original=copy.deepcopy(data)
            for field in ('Hard Disk Size','Memory Storage Capacity','Secondary internal drive capacity'):
                for basis in ('BINARY_SYSTEM','FORMATTED_USABLE'):
                    altered=copy.deepcopy(original)
                    fact=next(f for f in altered['facts'] if f['attribute']==field)
                    fact.setdefault('evidence',{})['capacity_basis']=basis
                    test.save(altered,path,ledger)
                    with self.subTest(field=field,basis=basis),self.assertRaisesRegex(ValueError,'decimal nominal capacity'):
                        helper.export_run(ledger,path)
            data=copy.deepcopy(original)
            field=next(f for f in data['facts'] if f['attribute']=='Hard Disk Size')
            field.setdefault('evidence',{})['capacity_basis']='DECIMAL_MARKETING'
            # Declared basis participates in image inputs without changing stored product bytes.
            self.assertNotEqual(hardware_projection(data),hardware_projection(original))


if __name__=='__main__':unittest.main()
