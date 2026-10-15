"""Workbook extension handling matches Windows and case-sensitive CI without renaming files."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from zipfile import BadZipFile
import test_research_export as ef
import research_export as r
from workbook_paths import files_with_suffix,resolve_workbook_path
from research_handoff import check_research_summaries

spec=importlib.util.spec_from_file_location('case_checks',r.ROOT/'scripts/check-workbooks.py')
checks=importlib.util.module_from_spec(spec);spec.loader.exec_module(checks)


class WorkbookCaseTests(unittest.TestCase):
    def test_discovery_is_independent_of_linux_glob_case_and_excludes_nested_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'product generated photo/TEST';p.mkdir(parents=True)
            expected=[]
            for name in ('a.xlsx','b.XLSX','c.XlSx'):
                path=p/name;path.touch();expected.append(path)
            (p/'directory.xlsx').mkdir();(p/'workbook-snapshots/old').mkdir(parents=True)
            (p/'workbook-snapshots/old/old.XLSX').touch()
            original=Path.glob
            with patch.object(Path,'glob',lambda path,pattern,**kwargs:original(path,pattern,case_sensitive=True)):
                self.assertEqual(checks.current_workbooks(root),expected)
            self.assertEqual(resolve_workbook_path(p/'B.xlsx'),p/'b.XLSX')

    def test_invalid_uppercase_workbook_is_checked_not_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'product generated photo/TEST';p.mkdir(parents=True)
            (root/'assets').mkdir();shutil.copyfile(r.ROOT/'assets/listing-workbook-template.xlsx',root/'assets/listing-workbook-template.xlsx')
            (p/'broken.XLSX').write_bytes(b'Invalid synthetic workbook')
            original=Path.glob
            with (patch.object(Path,'glob',lambda path,pattern,**kwargs:original(path,pattern,case_sensitive=True)),
                  patch.object(sys,'argv',['check-workbooks.py','--directory',str(root)])):
                with self.assertRaises(BadZipFile):checks.main()

    def test_uppercase_workbook_cli_and_summary_use_actual_name_and_remain_bound(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'product generated photo/TEST-PC';p.mkdir(parents=True)
            (root/'assets').mkdir();shutil.copyfile(r.ROOT/'assets/listing-workbook-template.xlsx',root/'assets/listing-workbook-template.xlsx')
            helper=ef.ResearchExportTests();book,data,path,ledger=helper.full_fixture(p,name='REVIEW.XLSX');book.close()
            ledger=ledger.rename(p/'research-ledger.json');before=path.read_bytes()
            output=p/'TEST-PC.RESEARCH-SUMMARY.JSON'
            subprocess.run([sys.executable,str(r.ROOT/'scripts/research_export.py'),'--ledger',str(ledger),'--workbook',str(p/'review.xlsx'),
                            '--summary-output',str(output)],check=True,capture_output=True)
            summary=json.loads(output.read_text());self.assertEqual(summary['workbookFile'],'REVIEW.XLSX')
            self.assertEqual(summary['workbookSha256'],hashlib.sha256(before).hexdigest())
            self.assertEqual(path.read_bytes(),before);self.assertEqual(check_research_summaries(root),1)
            summary['workbookFile']='review.xlsx';output.write_text(json.dumps(summary))
            self.assertEqual(check_research_summaries(root),1)
            del summary['workbookFile'];output.write_text(json.dumps(summary))
            self.assertEqual(check_research_summaries(root),1)
            summary['ledgerSha256']='0'*64;output.write_text(json.dumps(summary))
            with self.assertRaisesRegex(ValueError,'stale'):check_research_summaries(root)

    def test_case_collision_is_rejected_before_choosing_an_arbitrary_file(self):
        class SyntheticPath:
            def __init__(self,name):self.name=name
            def is_file(self):return True
            def __lt__(self,other):return self.name<other.name
        # Two names cannot coexist on ordinary Windows, so simulate Linux entries.
        with patch.object(Path,'is_dir',return_value=True),patch.object(Path,'iterdir',return_value=iter([SyntheticPath('same.xlsx'),SyntheticPath('SAME.XLSX')])):
            with self.assertRaisesRegex(ValueError,'differ only by case'):files_with_suffix(Path('synthetic'),'.xlsx')


if __name__=='__main__':unittest.main()
