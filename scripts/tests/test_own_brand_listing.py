"""Own-brand authorization, copy, warranty and existing configuration gates stay distinct."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from listing_mode import resolve, CUSTOM, OWN_BRAND
from listing_content import validate_listing
from warranty_policy import render, validate_copy
import research_export as r
import test_research_export as fixtures
spec = importlib.util.spec_from_file_location('own_workbook_checks', r.ROOT/'scripts/check-workbooks.py')
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)


class OwnBrandTests(unittest.TestCase):
    def fixture(self, root):
        book, data, path, ledger = fixtures.ResearchExportTests().full_fixture(root)
        product = json.loads((root/'product-facts.json').read_text())
        product.update(listingMode=OWN_BRAND, ownBrandAuthority='Synthetic explicit seller own-manufacture decision')
        product['identity'].update(oemBrand='MegaPC', oemModel='TEST-MINI')
        warranty = render('MegaPC', OWN_BRAND)
        changes = {
            'Manufacturer':'MegaPC', 'Model Number':'TEST-MINI', 'Model Name':'TEST-MINI',
            'Item Name':'MegaPC TEST-MINI Mini PC, Intel Core Ultra 7 265T, 16GB RAM, 256GB SSD, Win 11 Pro',
            'Bullet Point':warranty+'\n\nSynthetic verified product benefit'*4,
            'Product Description':'<strong>MegaPC TEST-MINI</strong><br/><br/><strong>Warranty and Disclosure</strong><br/>'+warranty,
            'Warranty Description':warranty,
        }
        for fact in data['facts']:
            if fact['attribute'] in changes: fact['final_value'] = changes[fact['attribute']]
        return book, data, product

    def test_explicit_authority_and_manufacturer_are_required(self):
        self.assertEqual(resolve({}), CUSTOM)
        for product in ({'listingMode':'typo'},
                        {'listingMode':OWN_BRAND,'identity':{'oemBrand':'Dell'},'ownBrandAuthority':'Synthetic'},
                        {'listingMode':OWN_BRAND,'identity':{'oemBrand':'MegaPC'}}):
            with self.assertRaises(ValueError): resolve(product)

    def test_own_brand_content_passes_without_relaxing_sold_capacity_checks(self):
        with tempfile.TemporaryDirectory() as scratch:
            book, data, product = self.fixture(Path(scratch))
            projected = r.project(data, r.workbook_fields(book))
            self.assertEqual(validate_listing(projected, product)['content'], 'PASS')
            changed = copy.deepcopy(projected)
            changed[('Product Details','Item Name')]['value'] = changed[('Product Details','Item Name')]['value'].replace('16GB RAM','64GB RAM')
            with self.assertRaisesRegex(ValueError,'another RAM/SSD'): validate_listing(changed, product)
            for text in ('MegaPC Custom TEST-MINI', 'Created Using TEST-MINI', 'Our upgraded RAM', 'The seal was opened'):
                changed = copy.deepcopy(projected)
                changed[('Product Details','Bullet Point')]['value'] += ' '+text
                with self.assertRaisesRegex(ValueError,'Own-brand copy'): validate_listing(changed, product)
            book.close()

    def test_warranty_branch_cannot_leak_into_customized_products(self):
        own = render('MegaPC', OWN_BRAND)
        description = '<strong>MegaPC Mini PC</strong><br/><br/><strong>Warranty and Disclosure</strong><br/>'+own
        self.assertEqual(validate_copy('MegaPC', own+'\n\nBenefits', description, own, OWN_BRAND)['fixedWording'],'PASS')
        self.assertIn('1-year limited warranty on the RAM and SSD', own)
        self.assertNotIn('seal', own)
        self.assertIn('upgraded RAM', render('Dell'))
        with self.assertRaises(ValueError): render('Dell', OWN_BRAND)
        with self.assertRaises(ValueError): validate_copy('Dell', own, description, own)

    def test_real_workbook_checker_resolves_mode_from_product_metadata(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            book, data, product = self.fixture(root)
            projection = r.project(data, r.workbook_fields(book))
            for ws in book:
                for col in range(2, ws.max_column+1):
                    rec = projection[(ws.title, ws.cell(1,col).value)]
                    for row, key in ((3,'value'),(4,'status'),(5,'source')): ws.cell(row,col).value = rec[key]
            path = root/'TEST_LISTING_DRAFT.xlsx'
            book.save(path)
            book.close()
            (root/'product-facts.json').write_text(json.dumps(product))
            checks.check_output(path, checks.template_topology(r.ROOT/'assets/listing-workbook-template.xlsx'),'MegaPC')
            product.pop('listingMode')
            (root/'product-facts.json').write_text(json.dumps(product))
            with self.assertRaisesRegex(ValueError,'fixed Warranty'): checks.check_output(path,checks.template_topology(r.ROOT/'assets/listing-workbook-template.xlsx'),'MegaPC')


if __name__ == '__main__': unittest.main()
