"""Prevent the public Word reading copy from silently drifting from its sources."""
import hashlib
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[2]


class FCCManualCopyTests(unittest.TestCase):
    def test_word_bytes_sources_and_full_reading_text_remain_bound(self):
        folder = ROOT/'references/manuals'
        record = json.loads((folder/'fcc-id-lookup-manual.source.json').read_text(encoding='utf-8'))
        expected = {'references/manuals/fcc-id-lookup-manual.zh-CN.md', 'references/fcc-research-workflow.md',
                    'references/research-ledger-projection.md', 'references/workbook-stage-snapshots.md'}
        self.assertEqual(record['schemaVersion'], 1)
        self.assertEqual(record['artifactRole'], 'FCC_WORKFLOW_READING_COPY')
        self.assertEqual(record['documentPath'], 'references/manuals/fcc-id-lookup-manual.docx')
        self.assertEqual(set(record['sourceTextSha256']), expected)
        for name, sha in record['sourceTextSha256'].items():
            with self.subTest(source=name):
                snapshots = record.get('sourceSnapshotPaths', {})
                self.assertEqual(snapshots, {'references/research-ledger-projection.md':
                    'references/manuals/source-snapshots/2026-10-21/research-ledger-projection.md',
                    'references/fcc-research-workflow.md':
                    'references/manuals/source-snapshots/2026-10-21/fcc-research-workflow.md'})
                self.assertEqual(record.get('bindingScope'), 'ORIGINAL_2026_10_21_READING_COPY_NOT_CURRENT_EXECUTION')
                self.assertEqual(hashlib.sha256((ROOT/snapshots.get(name, name)).read_text(encoding='utf-8').encode('utf-8')).hexdigest(),
                                 sha, 'Reconcile and review the Word reading copy; do not merely refresh hashes')
        word = ROOT/record['documentPath']
        self.assertEqual(hashlib.sha256(word.read_bytes()).hexdigest(), record['documentSha256'])
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        with zipfile.ZipFile(word) as archive:
            xml = ET.fromstring(archive.read('word/document.xml'))
        # Only visible text, excluding empty explicit page-break paragraphs.
        paragraphs = [''.join(t.text or '' for t in p.findall('.//w:t', ns))
                      for p in xml.findall('w:body/w:p', ns)]
        actual = [p for p in paragraphs if p]
        expected_text = [line.lstrip('# ').strip() for line in
                         (folder/'fcc-id-lookup-manual.zh-CN.md').read_text(encoding='utf-8').splitlines()
                         if line.strip() and line != '<!-- PAGE BREAK -->']
        self.assertEqual(actual, expected_text)
        self.assertIn(record['version'].replace('-', '年', 1).replace('-', '月')+'日', actual[1])


if __name__ == '__main__':
    unittest.main()
