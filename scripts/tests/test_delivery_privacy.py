import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import delivery_privacy as privacy


class DeliveryPrivacyTests(unittest.TestCase):
    def fixture(self):
        return {'files': [{'relativePath': 'PT01.png', 'id': 'file-1', 'name': 'PT01.png',
            'parents': ['folder-1'], 'mimeType': 'image/png', 'size': '123',
            'downloadedSha256': 'a' * 64, 'readBackAtUtc': '2026-10-26T12:00:00Z',
            'webViewLink': 'https://drive.google.com/file/d/file-1/view?usp=drivesdk'}]}

    def test_derivative_excludes_private_fields_without_mutating_source_or_claiming_verification(self):
        data = self.fixture()
        data['files'][0].update(download_url='https://example.test/raw?sig=PRIVATE',
                                rawSerial='TEST-PRIVATE-1234', qaStatus='PASS')
        data['privateBrowserSession'] = {'cookie': 'PRIVATE'}
        before = copy.deepcopy(data)
        self.assertTrue(privacy.findings(data))
        result = privacy.share_readbacks(data)
        self.assertEqual(data, before)
        self.assertEqual(result['files'][0]['downloadedSha256'], 'a' * 64)
        self.assertEqual(result['files'][0]['parents'], ['folder-1'])
        self.assertEqual(result['files'][0]['webViewLink'], 'https://drive.google.com/file/d/file-1/view')
        self.assertEqual(result['verificationStatus'], 'SUPPLIED_METADATA_NOT_AUTHENTICATED')
        self.assertEqual(result['excludedFieldCount'], 4)
        self.assertFalse(privacy.findings(result))
        self.assertNotIn('PRIVATE', json.dumps(result))
        self.assertNotIn('qaStatus', result['files'][0])

    def test_identifiers_in_prose_encoded_urls_and_object_keys_never_echo_in_findings(self):
        secret = 'SYNTHETIC-UNIT-123'
        data = {secret: [{'note': 'unit synthetic-unit-123',
                         'source': 'https://example.test/?q=SYNTHETIC%252DUNIT%252D123'}]}
        found = privacy.findings(data, [secret])
        self.assertGreaterEqual(sum(f['code'] == 'KNOWN_PRIVATE_VALUE' for f in found), 3)
        self.assertNotIn(secret, json.dumps(found))
        self.assertTrue(all(set(f) == {'location', 'code'} for f in found))

    def test_sensitive_url_key_path_local_path_and_credentials_are_detected(self):
        for value in ('https://example.test/?SerialNumber=TEST',
                      'https://example.test/?X-Amz-Signature=TEST',
                      'https://example.test/service-tag/TEST',
                      'https://user:password@example.test/model',
                      'C:/Users/private/source.json', '/home/private/source.json'):
            with self.subTest(value=value):
                self.assertTrue(privacy.findings({'source': value}))
        for key in ('raw_serial', 'serviceTag', 'refresh_token', 'client_secret'):
            with self.subTest(key=key):
                self.assertTrue(privacy.findings({key: 'TEST'}))
        self.assertFalse(privacy.findings({'serial_research': {'unit_evidence_alias': 'UNIT-A'},
                                         'source': 'https://pcsupport.lenovo.com/model'}))

    def test_projection_refuses_wrong_host_file_identity_credentials_and_unrecognized_rows(self):
        for url in ('https://drive.google.com.evil.test/file/d/file-1/view',
                    'https://drive.google.com/file/d/wrong/view',
                    'http://drive.google.com/file/d/file-1/view',
                    'https://user:private@drive.google.com/file/d/file-1/view',
                    'https://drive.google.com:8443/file/d/file-1/view'):
            data = self.fixture()
            data['files'][0]['webViewLink'] = url
            with self.subTest(url=url), self.assertRaises(ValueError):
                privacy.share_readbacks(data)
        with self.assertRaises(ValueError):
            privacy.share_readbacks({'files': []})
        data = self.fixture()
        data['files'][0]['name'] = 'SYNTHETIC-PRIVATE-123.png'
        with self.assertRaises(ValueError):
            privacy.share_readbacks(data, ['SYNTHETIC-PRIVATE-123'])

    def test_original_xlsx_provider_view_preserves_file_identity(self):
        data = self.fixture()
        item = data['files'][0]
        item.update(mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    webViewLink='https://docs.google.com/spreadsheets/d/file-1/edit?rtpof=true')
        result = privacy.share_readbacks(data)
        self.assertEqual(result['files'][0]['webViewLink'], 'https://docs.google.com/spreadsheets/d/file-1/edit')
        self.assertEqual(result['files'][0]['id'], 'file-1')

    def test_cli_binds_actual_input_bytes_and_does_not_echo_private_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, secrets = root/'input.json', root/'private-values.json'
            source.write_text(json.dumps({'note': 'SYNTHETIC-PRIVATE-123'}), encoding='utf-8')
            secrets.write_text(json.dumps(['SYNTHETIC-PRIVATE-123']), encoding='utf-8')
            before = source.read_bytes()
            capture = io.StringIO()
            with contextlib.redirect_stdout(capture):
                status = privacy.main(['check', '--input', str(source), '--private-values-file', str(secrets)])
            report = json.loads(capture.getvalue())
            self.assertEqual(status, 1)
            self.assertEqual(report['inputSha256'], hashlib.sha256(before).hexdigest())
            self.assertNotIn('SYNTHETIC-PRIVATE-123', capture.getvalue())
            self.assertEqual(source.read_bytes(), before)
            self.assertTrue(report['manualReviewRequired'])

    def test_cli_refuses_overwrite_and_canonical_record_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, output = root/'input.json', root/'shareable.json'
            source.write_text(json.dumps(self.fixture()), encoding='utf-8')
            args = ['share-readbacks', '--input', str(source), '--output', str(output)]
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(privacy.main(args), 0)
                before = output.read_bytes()
                self.assertEqual(privacy.main(args), 2)
                self.assertEqual(privacy.main(args[:-1] + [str(root/'research-ledger.json')]), 2)
            self.assertEqual(output.read_bytes(), before)
            self.assertFalse((root/'research-ledger.json').exists())


if __name__ == '__main__':
    unittest.main()
