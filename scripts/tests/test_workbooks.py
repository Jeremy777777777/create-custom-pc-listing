import importlib.util
import tempfile
import unittest
from pathlib import Path
import openpyxl

spec=importlib.util.spec_from_file_location('workbooks',Path(__file__).parents[1]/'check-workbooks.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class WorkbookChecks(unittest.TestCase):
    def test_accepts_status_dispositions_but_rejects_structure_and_missing_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'template.xlsx'; book=openpyxl.Workbook();book.remove(book.active)
            for name in module.SHEETS:
                sheet=book.create_sheet(name)
                for r,label in enumerate(['Field / Attribute','Definition','Value','Status','Source'],1):sheet.cell(r,1,label)
                sheet.cell(1,2,'Installed RAM');sheet.cell(2,2,'Installed capacity only')
                sheet.cell(4,2,'TBD');sheet.cell(5,2,'SELLER_INPUT_REQUIRED: installed capacity')
            book.save(path);book.close();topology=module.template_topology(path)
            module.check_output(path,topology)
            book=openpyxl.load_workbook(path);book.worksheets[0].cell(1,2,'Maximum RAM');book.save(path);book.close()
            with self.assertRaisesRegex(ValueError,'headers/definitions'):module.check_output(path,topology)
            book=openpyxl.load_workbook(path);book.worksheets[0].cell(1,2,'Installed RAM');book.worksheets[0].cell(5,2).value=None;book.save(path);book.close()
            with self.assertRaisesRegex(ValueError,'Status/Source'):module.check_output(path,topology)
