"""Unit conversion and new-output enforcement, with synthetic data only."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import dimension_units as d
import research_export as export
import test_fcc_guide_writer as fixture
from reference_fixtures import write_audit


class DimensionUnitsTests(unittest.TestCase):
    def test_exact_conversions_ranges_and_tuple_order(self):
        for value,unit in [(254,'mm'),(25.4,'cm'),(.254,'m'),(10,'inch'),(10,'INCHES')]:
            self.assertEqual(d.to_inches(value,unit),10)
        self.assertEqual(d.to_inches(1,'ft'),12)
        self.assertEqual(d.convert_length_text('17.9–18.9 mm'),'0.7047–0.7441 inches')
        self.assertEqual(d.convert_length_text('254 x 127 x 25.4 mm'),'10 x 5 x 1 inches')
        for value,unit in [(0,'mm'),(-1,'cm'),(True,'mm'),(float('nan'),'mm'),(1,'unknown'),(1,'kg'),(.0000001,'mm')]:
            with self.subTest(value=value,unit=unit),self.assertRaises(ValueError):d.to_inches(value,unit)
        with self.assertRaises(ValueError):d.convert_length_text('254 x127')

    def test_all_numeric_pairs_and_candidates_require_inch_units(self):
        for (sheet,field),unitfield in d.PAIRS.items():
            good={(sheet,field):{'value':10},(sheet,unitfield):{'value':'Inches'}}
            self.assertEqual(d.validate_dimensions(good)['state'],'INCH_DIMENSIONS_CHECK_PASS')
            for unit in ['Millimeters','Centimeters','Feet',None]:
                bad=copy.deepcopy(good);bad[(sheet,unitfield)]['value']=unit
                with self.subTest(field=field,unit=unit),self.assertRaises(ValueError):d.validate_dimensions(bad)
            candidate={(sheet,field):{'value':None,'value_candidate':'0.7–0.74'},(sheet,unitfield):{'value':None,'value_candidate':'Inches'}}
            d.validate_dimensions(candidate)
            candidate[(sheet,unitfield)]['value_candidate']='Millimeters'
            with self.assertRaises(ValueError):d.validate_dimensions(candidate)

    def test_composite_and_bezel_strings_need_explicit_inches(self):
        for key in d.TEXT_FIELDS:
            d.validate_dimensions({key:{'value':'10 x 5 x 1 inches'}})
            for value in ['254 x127 x25.4 mm','10 x5 x1',2,True,'0 inches']:
                with self.subTest(key=key,value=value),self.assertRaises(ValueError):d.validate_dimensions({key:{'value':value}})
        d.validate_dimensions({})  # Unknown dimensions never become an invented number.

    def test_customer_size_copy_and_technical_designations(self):
        for text in ['Dimensions:254 x127 x25.4 mm','Height:18 mm','Width is 25 cm','Depth 1 foot']:
            with self.subTest(text=text),self.assertRaises(ValueError):d.validate_dimension_copy(text)
        for text in ['Dimensions:10 x5 x1 inches','M.2 2280 SSD;3.5mm audio;1920 x1200 pixels','Weight:1.59kg;60Hz']:
            d.validate_dimension_copy(text)

    def test_real_writer_rejects_metric_and_accepts_converted_ledger(self):
        with tempfile.TemporaryDirectory() as scratch:
            root=Path(scratch);data,_,old,ledger=fixture.FCCGuideWriterTests().fixture(root)
            length=next(f for f in data['facts'] if f['attribute']=='Item Length Horizontal Edge')
            unit=next(f for f in data['facts'] if f['attribute']=='Item Length Unit')
            length.update(status='VERIFIED',final_value=254)
            unit.update(status='VERIFIED',final_value='Millimeters')
            ledger.write_text(json.dumps(data));write_audit(ledger)
            before=old.read_bytes()
            with self.assertRaisesRegex(ValueError,'Inches'):export.write_workbook(export.ROOT/'assets/listing-workbook-template.xlsx',ledger,root/'blocked.xlsx')
            self.assertFalse((root/'blocked.xlsx').exists());self.assertEqual(old.read_bytes(),before)
            length['evidence']={'original_value':254,'original_unit':'mm','conversion':'254 /25.4'}
            length['final_value']=d.to_inches(254,'mm');unit['final_value']='Inches'
            ledger.write_text(json.dumps(data));write_audit(ledger)
            out=root/'new.xlsx';export.write_workbook(export.ROOT/'assets/listing-workbook-template.xlsx',ledger,out)
            import openpyxl
            book=openpyxl.load_workbook(out);sheet=book['Product Details']
            col=next(c.column for c in sheet[1] if c.value=='Item Length Horizontal Edge')
            self.assertEqual(sheet.cell(3,col).value,10);book.close()


if __name__=='__main__':unittest.main()
