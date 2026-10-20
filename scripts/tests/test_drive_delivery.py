import copy
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import drive_delivery as d


class DriveDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.product = Path(self.tmp.name) / 'VL-TEST'
        self.product.mkdir()
        (self.product / 'PT01.png').write_bytes(b'fixture bytes')
        self.plan = d.plan(self.product, 'run-1', ['PT01.png'])
        item = self.plan['files'][0]
        self.readbacks = {'files': [{'relativePath': 'PT01.png', 'id': 'file-1',
            'name': 'PT01.png', 'parents': ['folder-1'], 'mimeType': 'image/png',
            'size': str(item['size']), 'md5Checksum': item['md5'],
            'webViewLink': 'https://drive.google.com/file/d/file-1/view',
            'readBackAtUtc': datetime.now(timezone.utc).isoformat()}]}
        self.destinations = {'PT01.png': 'folder-1'}

    def test_valid_readback_is_storage_only(self):
        receipt = d.verify(self.product, self.plan, self.readbacks, self.destinations)
        self.assertEqual(receipt['deliveryState'], 'DRIVE_DELIVERY_VERIFIED')
        self.assertEqual(receipt['qaStatus'], 'UNCHANGED_BY_STORAGE_VERIFICATION')

    def test_metadata_only_and_wrong_destination_or_checksum_fail(self):
        for key, value in [('md5Checksum', None), ('md5Checksum', '0' * 32),
                           ('parents', ['wrong']), ('size', '0'),
                           ('webViewLink', 'https://drive.google.com/file/d/another/view'),
                           ('readBackAtUtc', '2020-01-01T00:00:00Z')]:
            with self.subTest(key=key, value=value):
                rows = copy.deepcopy(self.readbacks)
                rows['files'][0][key] = value
                with self.assertRaises(ValueError):
                    d.verify(self.product, self.plan, rows, self.destinations)

    def test_changed_bytes_and_incomplete_scope_fail(self):
        with self.assertRaises(ValueError):
            d.verify(self.product, self.plan, {'files': []}, self.destinations)
        (self.product / 'PT01.png').write_bytes(b'new bytes')
        with self.assertRaisesRegex(ValueError, 'changed'):
            d.verify(self.product, self.plan, self.readbacks, self.destinations)

    def test_traversal_and_case_collisions_fail(self):
        for names in [['../PT01.png'], ['PT01.png', 'pt01.png'], ['C:/private.png']]:
            with self.assertRaises(ValueError):
                d.plan(self.product, 'run-1', names)

    def test_drive_readme_excludes_zip_archives(self):
        (self.product / 'backup.zip').write_bytes(b'local backup')
        with self.assertRaisesRegex(ValueError, 'ZIP backups stay local'):
            d.plan(self.product, 'run-1', ['backup.zip'])


if __name__ == '__main__':
    unittest.main()
