"""An older research stage stays immutable without blocking current projection."""
import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import research_export as r
from workbook_snapshots import check_snapshot, check_snapshots


class SnapshotTests(unittest.TestCase):
    def bundle(self, root):
        directory = root/'product generated photo/TEST-PC/workbook-snapshots/review-v1'
        directory.mkdir(parents=True)
        files = {}
        for role, name in [('workbook','old-review.xlsx'), ('ledger','research-ledger.json'), ('template','template.xlsx')]:
            (directory/name).write_bytes(('Synthetic old ' + role).encode())
            files[role] = {'path':name, 'sha256':hashlib.sha256((directory/name).read_bytes()).hexdigest()}
        receipt = {'schemaVersion':1, 'artifactRole':'HISTORICAL_SNAPSHOT', 'exportEligible':False,
                   'productId':'TEST-PC', 'configurationId':'BASE-A', 'stage':'RESEARCH_REVIEW', 'files':files}
        (directory/'snapshot.json').write_text(json.dumps(receipt), encoding='utf-8')
        return directory, receipt

    def checks(self):
        spec = importlib.util.spec_from_file_location('checks', r.ROOT/'scripts/check-workbooks.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        return module

    def test_current_discovery_excludes_bound_snapshots_and_detects_tampering(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            directory, receipt = self.bundle(root)
            current = directory.parents[1]/'current.xlsx'
            current.write_bytes(b'Current file discovery fixture')
            self.assertEqual(self.checks().current_workbooks(root), [current])
            self.assertEqual(check_snapshots(root), 1)
            self.assertFalse(check_snapshot(directory)['exportEligible'])
            (directory/'old-review.xlsx').write_bytes(b'Changed old bytes')
            with self.assertRaisesRegex(ValueError, 'bytes changed'):
                check_snapshots(root)

    def test_missing_receipt_paths_and_export_flags_fail_closed(self):
        with tempfile.TemporaryDirectory() as scratch:
            directory, receipt = self.bundle(Path(scratch))
            for field, value in [('exportEligible', True), ('artifactRole', 'CURRENT'), ('stage', 'READY')]:
                broken = dict(receipt); broken[field] = value
                (directory/'snapshot.json').write_text(json.dumps(broken), encoding='utf-8')
                with self.subTest(field=field), self.assertRaises(ValueError): check_snapshot(directory)
            receipt['files']['ledger']['path'] = '../outside.json'
            (directory/'snapshot.json').write_text(json.dumps(receipt), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'local filenames'): check_snapshot(directory)
            (directory/'snapshot.json').unlink()
            with self.assertRaises(OSError): check_snapshots(Path(scratch))

    def test_optional_historical_summary_is_bound_and_remains_immutable(self):
        with tempfile.TemporaryDirectory() as scratch:
            directory, receipt = self.bundle(Path(scratch))
            summary = {'artifactRole': 'RESEARCH_COVERAGE_SUMMARY', 'productId': 'TEST-PC',
                       'configurationId': 'BASE-A', 'stage': 'RESEARCH_REVIEW', 'workbookFile': 'old-review.xlsx'}
            summary.update({role+'Sha256': receipt['files'][role]['sha256'] for role in ('workbook','ledger','template')})
            path = directory/'old-review.research-summary.json'
            path.write_text(json.dumps(summary), encoding='utf-8')
            receipt['files']['summary'] = {'path': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
            (directory/'snapshot.json').write_text(json.dumps(receipt), encoding='utf-8')
            self.assertFalse(check_snapshot(directory)['exportEligible'])
            summary['configurationId'] = 'OTHER'
            path.write_text(json.dumps(summary), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'bytes changed'): check_snapshot(directory)
            receipt['files']['summary']['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
            (directory/'snapshot.json').write_text(json.dumps(receipt), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'does not bind'): check_snapshot(directory)

    def test_archived_real_workbook_is_independent_of_latest_ledger_and_never_exportable(self):
        # Use the real template and scoped fixtures, not a fabricated manifest PASS.
        from test_research_export import ResearchExportTests
        helper = ResearchExportTests()
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            current_root = root/'product generated photo/TEST-PC'; current_root.mkdir(parents=True)
            book, data, path, ledger = helper.full_fixture(current_root)
            directory = current_root/'workbook-snapshots/review-v1'; directory.mkdir(parents=True)
            old = directory/path.name; path.rename(old)
            (directory/'research-ledger.json').write_bytes(ledger.read_bytes())
            template = directory/'template.xlsx'; template.write_bytes((r.ROOT/'assets/listing-workbook-template.xlsx').read_bytes())
            receipt = {'schemaVersion':1, 'artifactRole':'HISTORICAL_SNAPSHOT', 'exportEligible':False,
                       'productId':'TEST-PC', 'configurationId':'BASE-A', 'stage':'RESEARCH_REVIEW', 'files':{}}
            for role, file in [('workbook',old), ('ledger',directory/'research-ledger.json'), ('template',template)]:
                receipt['files'][role] = {'path':file.name, 'sha256':hashlib.sha256(file.read_bytes()).hexdigest()}
            (directory/'snapshot.json').write_text(json.dumps(receipt), encoding='utf-8')
            fact = next(f for f in data['facts'] if f['attribute']=='RAM Memory Installed')
            fact.update(status='VERIFIED', final_value=32)
            column = next(c.column for c in book['Product Details'][1] if c.value=='RAM Memory Installed')
            book['Product Details'].cell(3,column).value=32; book['Product Details'].cell(4,column).value='VERIFIED'
            book.save(path); book.close()
            (current_root/'research-ledger.json').write_text(json.dumps(data), encoding='utf-8')
            self.checks().check_output(path, self.checks().template_topology(r.ROOT/'assets/listing-workbook-template.xlsx'))
            self.assertEqual(check_snapshots(root), 1)
            self.assertEqual(self.checks().current_workbooks(root), [path])
            with self.assertRaisesRegex(ValueError, 'Historical workbook'):
                r.run(template, directory/'research-ledger.json', old, 'export', 'TEST-PC', 'BASE-A', 'LISTING_DRAFT')
            # A stale stage left at top level still fails instead of being silently ignored.
            stale = current_root/'stale.xlsx'; stale.write_bytes(old.read_bytes())
            with self.assertRaisesRegex(ValueError, 'differs'):
                self.checks().check_output(stale, self.checks().template_topology(r.ROOT/'assets/listing-workbook-template.xlsx'))


if __name__ == '__main__':
    unittest.main()
