"""Research/listing/image handoff regressions; never create real product PASS records."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import test_research_export as ef
import test_edge_case_repairs as er
import test_workflow_hardening as gf
import gallery_engine as g
import research_export as r
from product_metadata import listing_view,hardware_projection,exact_cpu_model,check_image_cache
from listing_content import capacity_mentions


class MetadataTests(unittest.TestCase):
    def test_flat_metadata_exports_through_verified_read_only_view(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);helper=ef.ResearchExportTests();book,data,path,ledger=helper.full_fixture(root);book.close()
            flat={'productId':'TEST-PC','identity':'Dell Pro Micro QCM1250','cpu':'Intel Core Ultra 7 265T',
                  'ram':'16GB DDR5','internalStorage':'256GB NVMe SSD'}
            source=root/'product-facts.json';source.write_text(json.dumps(flat));before=source.read_bytes()
            report=helper.export_run(ledger,path)
            self.assertEqual(report['result'],'EXPORT_EVIDENCE_CHECK_PASS')
            self.assertEqual(report['metadataView']['format'],'LEGACY_READ_ONLY_ADAPTER')
            self.assertFalse(report['metadataView']['rawProductFactsRewritten'])
            self.assertEqual(source.read_bytes(),before)
            flat['productId']='OTHER';source.write_text(json.dumps(flat))
            with self.assertRaisesRegex(ValueError,'identity'):helper.export_run(ledger,path)

    def test_real_vl1121_adapter_and_listing_copy_errors_are_actionable(self):
        p=r.ROOT/'product generated photo/VL-1121';raw=json.loads((p/'product-facts.json').read_text(encoding='utf-8-sig'))
        ledger=r.load_ledger(p/'research-ledger.json');original=copy.deepcopy(raw)
        view,report=listing_view(raw,ledger)
        self.assertEqual(raw,original)
        self.assertEqual(view['identity']['internalId'],'VL-1121')
        self.assertEqual(view['selectedBaseConfiguration']['id'],ledger['configurationId'])
        self.assertTrue(view['identity']['oemBrand'])
        self.assertEqual(report['format'],'LEGACY_READ_ONLY_ADAPTER')
        # A research draft remains a draft: it reaches copy checking, not AttributeError.
        with self.assertRaisesRegex(ValueError,'Bullet 1'):
            r.run(r.ROOT/'assets/listing-workbook-template.xlsx',p/'research-ledger.json',
                  p/'VL-1121_RESEARCH_REVIEW.xlsx','draft',stage='LISTING_DRAFT')

    def test_missing_metadata_is_reported_without_guessing(self):
        with tempfile.TemporaryDirectory() as tmp:
            helper=ef.ResearchExportTests();book,data,path,ledger=helper.full_fixture(Path(tmp));book.close()
            manufacturer=next(f for f in data['facts'] if f['attribute']=='Manufacturer')
            manufacturer.update(status='TBD',final_value=None)
            with self.assertRaisesRegex(ValueError,'PRODUCT_METADATA_REQUIRED.*oemBrand'):
                listing_view({'productId':'TEST-PC','identity':'unparsed legacy name','cpu':'Intel Core Ultra 7 265T'},data)


class CopyTests(unittest.TestCase):
    def test_cpu_copy_checks_title_bullets_and_html_without_treating_gpu_as_cpu(self):
        with tempfile.TemporaryDirectory() as tmp:
            helper=ef.ResearchExportTests();book,data,path,ledger=helper.full_fixture(Path(tmp));book.close()
            values={f['attribute']:f['final_value'] for f in data['facts'] if f['sheet']=='Product Details'}
        helper=er.ExportRepairs()
        for field in ('Item Name','Bullet Point','Product Description'):
            # Preserve required warranty/HTML/title framing while changing CPU copy.
            text=values[field]
            if field=='Item Name': text=text.replace(' Win 11 Pro',' Intel Core Ultra 5 235T Win 11 Pro')
            elif field=='Bullet Point': text=text.replace('\n\n','\n\nIntel Core Ultra 5 235T. ',1)
            else: text=text.replace('Synthetic Product','Synthetic Product Intel Core Ultra 5 235T',1)
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'copy CPU'):
                helper.check({field:text})
        for cpu in ('Intel Core Ultra 7 265T','Core Ultra 7 265T','CPU: 265T'):
            title=values['Item Name'].replace(' Win 11 Pro',' '+cpu+' Win 11 Pro')
            self.assertEqual(helper.check({'Item Name':title})['result'],'EXPORT_EVIDENCE_CHECK_PASS')
        title=values['Item Name'].replace(' Win 11 Pro',' NVIDIA RTX 5070 Win 11 Pro')
        self.assertEqual(helper.check({'Item Name':title})['result'],'EXPORT_EVIDENCE_CHECK_PASS')

    def test_cpu_suffix_specs_do_not_become_model_and_ambiguity_is_blocked(self):
        for cpu in ('Intel Core Ultra 7 265T Processor 20 Cores 35W',
                    'Intel Core Ultra 7 265T 24MB Cache 5.3 GHz 20-core'):
            self.assertEqual(exact_cpu_model(cpu),'265T')
            self.assertEqual(er.ExportRepairs().check({}, {'cpu':cpu})['result'],'EXPORT_EVIDENCE_CHECK_PASS')
        with self.assertRaisesRegex(ValueError,'Exact CPU'):
            exact_cpu_model('Intel Core Ultra 7 265T or 235T')

    def test_mixed_reverse_ram_labels_are_consumed_once(self):
        for text in ('RAM: 16GB DDR5 256GB SSD','RAM: 16GB DDR5 SSD: 256GB',
                     'Memory: 16GB DDR5 RAM 256GB NVMe SSD'):
            self.assertEqual(list(capacity_mentions(text)),[(16.0,'ram'),(256.0,'ssd')])
            title='MegaPC Custom Created Using Dell QCM1250 '+text+' Win 11 Pro'
            self.assertEqual(er.ExportRepairs().check({'Item Name':title})['result'],'EXPORT_EVIDENCE_CHECK_PASS')
            with self.assertRaisesRegex(ValueError,'configuration'):
                er.ExportRepairs().check({'Item Name':title.replace('256GB','512GB')})

    def test_specific_cpu_field_cannot_contain_only_family_or_manufacturer(self):
        helper=er.ExportRepairs()
        for model in ('Intel','Core Ultra 7','Ultra 7','7'):
            with self.subTest(model=model),self.assertRaisesRegex(ValueError,'Exact CPU'):
                helper.check({'CPU Model Number':model})
        for model in ('265T','Core Ultra 7 265T','Intel Core Ultra 7 265T'):
            self.assertEqual(helper.check({'CPU Model Number':model})['result'],'EXPORT_EVIDENCE_CHECK_PASS')

    def test_gpu_memory_does_not_capture_next_ssd_capacity(self):
        helper=er.ExportRepairs()
        title='MegaPC Custom Created Using Dell QCM1250 16GB RAM 12GB GDDR7 Memory 256GB NVMe SSD Win 11 Pro'
        changes={'Item Name':title,'Graphics Ram Size':12,'Graphics Ram Size Unit':'GB'}
        self.assertEqual(helper.check(changes)['result'],'EXPORT_EVIDENCE_CHECK_PASS')
        for wrong in (title.replace('256GB','512GB'),title.replace('16GB','32GB'),title.replace('12GB','8GB')):
            with self.subTest(wrong=wrong),self.assertRaisesRegex(ValueError,'configuration|VRAM'):
                helper.check({**changes,'Item Name':wrong})

    def test_memory_categories_reverse_wording_and_clause_boundaries(self):
        for text in ('16GB RAM 12GB GDDR7 Memory 256GB NVMe SSD',
                     'RAM: 16GB; Video Memory: 12GB; SSD: 256GB',
                     '16GB DDR5, 12GB GDDR7 memory, 256GB PCIe Gen4 NVMe SSD'):
            self.assertEqual(list(capacity_mentions(text)),[(16.0,'ram'),(12.0,'vram'),(256.0,'ssd')])
        self.assertEqual(list(capacity_mentions('Cache Memory: 8MB; RAM: 16GB; SSD: 256GB')),
                         [(8/1024,'cache'),(16.0,'ram'),(256.0,'ssd')])
        self.assertEqual(list(capacity_mentions('256GB SSD supports fast loads. Graphics memory is dedicated.')),
                         [(256.0,'ssd')])


class ResearchImageTests(unittest.TestCase):
    def storage_ledger(self):
        ledger=self.ledger();ledger['facts']=[];ledger['fields']=[]
        for fid,attribute,value in (('base','Hard Disk Size',256),('base-unit','Hard Disk Size Unit','GB'),
                                    ('total','Memory Storage Capacity',1280),('total-unit','Memory Storage Capacity Unit','GB'),
                                    ('secondary','Secondary internal drive capacity',1024)):
            fact={'id':fid,'sheet':'Product Details','attribute':attribute,'configurationId':'BASE',
                  'fact_scope':'SOLD_BASE','status':'VERIFIED','final_value':value,
                  'source':'Synthetic exact sold storage source','applies_to_sold_configuration':True,'transfer_basis':'Synthetic assembly'}
            if fid=='secondary':fact['evidence']={'storage_medium':'INTERNAL_HDD','capacity_unit':'GB'}
            if fid=='total':fact['evidence']={'storage_scope':'INTERNAL_TOTAL','storage_component_fact_ids':['base','secondary']}
            ledger['facts'].append(fact)
            if fid!='secondary':ledger['fields'].append({'sheet':fact['sheet'],'attribute':attribute,'selected_fact':fid})
        return ledger

    def test_storage_dependencies_bind_media_count_capacity_units_state_and_source(self):
        original=self.storage_ledger();baseline=hardware_projection(original)
        for key,value in (('storage_medium','INTERNAL_SSD'),('capacity_unit','TB'),('oem_part_number','SYNTHETIC-NEW-PART'),('source','Changed source'),
                          ('final_value',512),('status','TBD'),('transfer_basis','Changed installation basis')):
            altered=copy.deepcopy(original);extra=altered['facts'][-1]
            if key in ('storage_medium','capacity_unit','oem_part_number'):extra['evidence'][key]=value
            else:extra[key]=value
            if key=='status':extra['final_value']=None
            with self.subTest(key=key):self.assertNotEqual(hardware_projection(altered),baseline)
        altered=copy.deepcopy(original);extra=altered['facts'][-1];extra['final_value']=512
        another=copy.deepcopy(extra);another.update(id='third',attribute='Additional internal drive capacity 3')
        altered['facts'].append(another);altered['facts'][2]['evidence']['storage_component_fact_ids'].append('third')
        self.assertNotEqual(hardware_projection(altered),baseline)
        altered=copy.deepcopy(original);altered['facts'][-1]['evidence']['researchLog']='Changed unrelated note'
        alternative=copy.deepcopy(altered['facts'][-1]);alternative.update(id='factory',fact_scope='FACTORY',final_value=2048)
        altered['facts'].append(alternative)
        self.assertEqual(hardware_projection(altered),baseline)
        altered['facts'][2]['evidence']['storage_component_fact_ids'].reverse()
        altered['facts'].reverse();self.assertEqual(hardware_projection(altered),baseline)

    def test_same_total_drive_change_makes_actual_partial_review_stale_without_rewriting(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'TEST';p.mkdir();fixture=gf.GalleryBoundaries()
            try:
                fixture.build(p);original=self.storage_ledger();g.write(p/'research-ledger.json',original)
                fixture.reviews(p,['PT03.png'])
                g.write(p/'delivery-status.json',{'galleryState':'LEGACY_QUARANTINED','currentQaPass':False})
                g.accept(p,slots=['PT03.png']);g.validate_partial(p,['PT03.png'])
                before={n:(p/n).read_bytes() for n in ('visual-review.json','semantic-review.json','partial-update-qa.json','delivery-status.json')}
                for change in ('media','count'):
                    altered=copy.deepcopy(original);extra=altered['facts'][-1]
                    if change=='media':extra['evidence']['storage_medium']='INTERNAL_SSD'
                    else:
                        extra['final_value']=512;third=copy.deepcopy(extra)
                        third.update(id='third',attribute='Additional internal drive capacity 3');altered['facts'].append(third)
                        altered['facts'][2]['evidence']['storage_component_fact_ids'].append('third')
                    g.write(p/'research-ledger.json',altered)
                    with self.subTest(change=change),self.assertRaisesRegex(ValueError,'binding stale'):
                        g.validate_partial(p,['PT03.png'])
                self.assertEqual(before,{n:(p/n).read_bytes() for n in before})
            finally:fixture.doCleanups()

    def test_invalid_storage_dependency_graph_cannot_create_an_image_binding(self):
        for change in ('missing','wrong_config','wrong_role','duplicate'):
            ledger=self.storage_ledger();extra=ledger['facts'][-1];refs=ledger['facts'][2]['evidence']['storage_component_fact_ids']
            if change=='missing':refs[-1]='absent'
            if change=='wrong_config':extra['configurationId']='OTHER'
            if change=='wrong_role':extra['attribute']='RAM Memory Installed'
            if change=='duplicate':refs.append('secondary')
            with self.subTest(change=change),self.assertRaises(ValueError):hardware_projection(ledger)

    def test_equivalent_resolution_dimensions_pass_but_actual_change_does_not(self):
        selected={('Product Details','Resolution'):{'status':'VERIFIED','final_value':'1920 x 1080'}}
        for resolution in ('1920×1080','1920X1080 px','1920 x 1080 pixels'):
            check_image_cache(selected,{'display':{'resolution':resolution}})
        for resolution in ('1080x1920','2560x1440','1920x0','FHD'):
            with self.subTest(resolution=resolution),self.assertRaises(ValueError):
                check_image_cache(selected,{'display':{'resolution':resolution}})

    def ledger(self):
        fact={'id':'wifi','sheet':'Product Details','attribute':'Wireless Communication Standard',
              'configurationId':'BASE','fact_scope':'SOLD_BASE','status':'VERIFIED','final_value':'Wi-Fi 6',
              'source':'Synthetic source','applies_to_sold_configuration':True,'transfer_basis':'Same synthetic sold configuration'}
        return {'schemaVersion':1,'productId':'TEST','configurationId':'BASE','facts':[fact],
                'fields':[{'sheet':fact['sheet'],'attribute':fact['attribute'],'selected_fact':'wifi'}]}

    def test_selected_hardware_binding_changes_but_offer_notes_and_alternatives_do_not(self):
        original=self.ledger();baseline=hardware_projection(original)
        for key,value in [('final_value','Wi-Fi 7'),('status','TBD'),('source','Changed supporting source')]:
            changed=copy.deepcopy(original);changed['facts'][0][key]=value
            if key=='status':changed['facts'][0]['final_value']=None
            self.assertNotEqual(hardware_projection(changed),baseline)
        changed=copy.deepcopy(original)
        changed['facts'][0]['evidence']={'researchLog':'Changed note'}
        alternative=copy.deepcopy(changed['facts'][0]);alternative.update(id='factory-radio',fact_scope='FACTORY')
        changed['facts'].append(alternative)
        offer=copy.deepcopy(changed['facts'][0]);offer.update(id='price',sheet='Offer',attribute='Your Price',final_value=99)
        changed['facts'].append(offer);changed['fields'].append({'sheet':'Offer','attribute':'Your Price','selected_fact':'price'})
        self.assertEqual(hardware_projection(changed),baseline)

    def test_pt08_ledger_only_change_invalidates_new_review_and_detects_stale_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'product generated photo/TEST';p.mkdir(parents=True);fixture=gf.GalleryBoundaries()
            try:
                fixture.build(p);ledger=self.ledger();g.write(p/'research-ledger.json',ledger)
                facts=g.read(p/'product-facts.json');facts['wireless']='Wi-Fi 6';g.write(p/'product-facts.json',facts)
                fixture.reviews(p,['PT08.png'])
                g.write(p/'delivery-status.json',{'galleryState':'LEGACY_QUARANTINED','currentQaPass':False});g.accept(p,slots=['PT08.png'])
                g.validate_partial(p,['PT08.png'])
                ledger['facts'][0]['final_value']='Wi-Fi 7';g.write(p/'research-ledger.json',ledger)
                with self.assertRaisesRegex(ValueError,'cache/research conflict'):g.review_inputs(p)
                facts['wireless']='Wi-Fi 7';g.write(p/'product-facts.json',facts)
                with patch.object(g.subprocess,'check_output',return_value='product generated photo/TEST/research-ledger.json\n'):
                    with self.assertRaisesRegex(ValueError,'binding stale'):g.gate(root,'base','head')
            finally:fixture.doCleanups()

    def test_pre_ledger_review_is_preserved_but_not_counted_as_current_source_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'product generated photo/TEST';p.mkdir(parents=True);fixture=gf.GalleryBoundaries()
            try:
                fixture.build(p);fixture.reviews(p,['PT08.png'])
                g.write(p/'delivery-status.json',{'galleryState':'LEGACY_QUARANTINED','currentQaPass':False});g.accept(p,slots=['PT08.png'])
                g.write(p/'research-ledger.json',self.ledger())
                originals={name:(p/name).read_bytes() for name in ('visual-review.json','semantic-review.json','partial-update-qa.json','delivery-status.json')}
                with patch.object(g.subprocess,'check_output',return_value='product generated photo/TEST/research-ledger.json\n'):
                    summary=g.gate(root,'base','head')
                self.assertEqual(summary['partialUpdatesValidated'],0)
                self.assertEqual(summary['historicalResearchUnboundPartialReviews'],1)
                self.assertEqual(originals,{name:(p/name).read_bytes() for name in originals})
                with self.assertRaisesRegex(ValueError,'binding stale'):g.validate_partial(p,['PT08.png'])
            finally:fixture.doCleanups()


if __name__=='__main__':unittest.main()
