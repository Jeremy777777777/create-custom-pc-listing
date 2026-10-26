"""Exercise source delivery and bounded legacy revisions with synthetic artifacts."""
import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import delivery_context as context
import drive_delivery as drive
import research_audit as audit
import research_export as export
import test_release_checks as release_fixtures
import test_research_export as export_fixtures


def reuse_review(previous, current):
    raw = json.dumps(previous).encode('utf-8')
    missing = {f['id'] for f in current['facts'] if not f.get('evidence', {}).get('research_trace')}
    review = {'productId': current['productId'], 'configurationId': current['configurationId'],
              'previousLedgerSha256': hashlib.sha256(raw).hexdigest(),
              'baselineReference': 'Synthetic observed legacy baseline and archive readbacks',
              'reviewer': 'Synthetic reviewer', 'reviewed_date': '2026-10-26',
              'impact_review': 'Synthetic only changed field has no effect on retained facts',
              'fields': [{'factId': key, 'dependencyFactIds': [],
                          'basis': 'Synthetic source, scope and applicability reviewed unchanged'} for key in sorted(missing)]}
    return raw, review


class ProductionRevisionTests(unittest.TestCase):
    def source_fixture(self, root, name):
        product, _, _, _, ctx = release_fixtures.ReleaseChecks().delivery(root)
        source = product/name
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_bytes(b'synthetic source bytes, no actual product')
        plan = drive.plan(product, 'SYNTHETIC-SOURCE', [name])
        stamp = datetime.now(timezone.utc).isoformat()
        for node in ctx['folders']:
            node['readBackAtUtc'] = stamp
        parent = 'p'
        for i, segment in enumerate(['90_SOURCE', *Path(name).parts[:-1]]):
            folder_id = 'source-' + str(i)
            ctx['folders'].append({'id': folder_id, 'name': segment, 'parents': [parent],
                                  'mimeType': context.FOLDER, 'readBackAtUtc': stamp})
            parent = folder_id
        row = plan['files'][0]
        ctx['fileRoles'] = {name: 'SOURCE'}
        ctx['privacyChecks'] = {name: {'state': 'DELIVERY_PRIVACY_SCREEN_PASS',
            'inputSha256': row['sha256'], 'manualReviewRequired': False, 'serialInventoryDeclared': False}}
        remote = {'files': [{'relativePath': name, 'id': 'source-file', 'name': source.name,
                  'parents': [parent], 'mimeType': row['mimeType'], 'size': row['size'],
                  'sha256Checksum': row['sha256'], 'webViewLink': 'https://drive.google.com/file/d/source-file/view',
                  'readBackAtUtc': stamp}]}
        return product, plan, remote, {name: parent}, ctx

    def test_source_masters_nested_dependencies_and_same_name_records_deliver(self):
        for name in ('master.png', 'unbranded/PT01.png', 'production/run-a/layers/mask.png',
                     'prior/research-ledger.json', 'prior/VL-99999_RESEARCH_REVIEW.xlsx'):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temp:
                args = self.source_fixture(Path(temp), name)
                result = drive.verify(*args)
                self.assertEqual(result['deliveryState'], 'DRIVE_DELIVERY_VERIFIED')

    def test_source_cannot_escape_or_flatten_its_observed_relative_chain(self):
        for mutation in ('flatten', 'other-product', 'ambiguous', 'stale', 'shortcut'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temp:
                product, plan, remote, destinations, ctx = self.source_fixture(Path(temp), 'unbranded/PT01.png')
                leaf = ctx['folders'][-1]
                if mutation == 'flatten': destinations['unbranded/PT01.png'] = 'source-0'
                if mutation == 'other-product': leaf['parents'] = ['another-product']
                if mutation == 'ambiguous': ctx['folders'].append({**leaf, 'id': 'duplicate'})
                if mutation == 'stale': leaf['readBackAtUtc'] = '2020-01-01T00:00:00Z'
                if mutation == 'shortcut': leaf['mimeType'] = 'application/vnd.google-apps.shortcut'
                with self.assertRaises(ValueError): context.validate(plan, destinations, ctx)

    def test_root_canonical_images_cannot_be_relabelled_source(self):
        with tempfile.TemporaryDirectory() as temp:
            product, plan, remote, destinations, ctx = self.source_fixture(Path(temp), 'PT01.png')
            with self.assertRaisesRegex(ValueError, 'Canonical file role'):
                drive.verify(product, plan, remote, destinations, ctx)
            ctx['folders'].append({**ctx['folders'][-1], 'id': 'images', 'name': '02_IMAGES'})
            ctx['fileRoles']['PT01.png'] = 'IMAGE'
            destinations['PT01.png'] = 'images'; remote['files'][0]['parents'] = ['images']
            self.assertEqual(drive.verify(product, plan, remote, destinations, ctx)['deliveryState'], 'DRIVE_DELIVERY_VERIFIED')

    def legacy_fixture(self):
        previous = export_fixtures.ResearchExportTests().ledger()
        previous['facts'].append({**copy.deepcopy(previous['facts'][0]), 'id': 'dependency'})
        current = copy.deepcopy(previous)
        raw, review = reuse_review(previous, current)
        review['fields'] = [row for row in review['fields'] if row['factId'] == 'sold']
        review['fields'][0]['dependencyFactIds'] = ['dependency']
        return previous, current, raw, review

    def test_unchanged_legacy_fact_preserves_missing_trace_state(self):
        previous, current, raw, review = self.legacy_fixture()
        result = audit.validate(current, True, raw, review)
        self.assertEqual(result['state'], 'LEGACY_TRACE_INCOMPLETE')
        self.assertEqual(result['legacyReuse']['retainedFactIds'], ['sold'])
        self.assertEqual(current, previous)
        with self.assertRaisesRegex(ValueError, 'missing count'): audit.validate(current, True)

    def test_changed_facts_dependencies_identity_and_bad_baselines_cannot_reuse(self):
        for mutation in ('value', 'status', 'source', 'scope', 'dependency', 'mapping', 'hash', 'identity', 'extra', 'review'):
            with self.subTest(mutation=mutation):
                previous, current, raw, review = self.legacy_fixture()
                fact = current['facts'][0]
                if mutation == 'value': fact['final_value'] = 64
                if mutation == 'status': fact['status'] = 'TBD'
                if mutation == 'source': fact['source'] = 'New source'
                if mutation == 'scope': fact['fact_scope'] = 'FACTORY'
                if mutation == 'dependency': current['facts'][1]['final_value'] = 64
                if mutation == 'mapping': current['fields'][0]['attribute'] = 'Different field'
                if mutation == 'hash': review['previousLedgerSha256'] = '0'*64
                if mutation == 'identity': current['configurationId'] = 'OTHER'
                if mutation == 'extra': review['fields'].append(copy.deepcopy(review['fields'][0]))
                if mutation == 'review': review['impact_review'] = ''
                with self.assertRaises(ValueError): audit.validate(current, True, raw, review)

    def test_cli_partial_revision_writes_real_workbook_and_honest_reuse_summary(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            book, previous, old_workbook, ledger = export_fixtures.ResearchExportTests().full_fixture(root)
            book.close()
            old_bytes = old_workbook.read_bytes()
            current = copy.deepcopy(previous)
            changed = next(f for f in current['facts'] if f['attribute'] == 'Model Name')
            changed['source'] = 'Synthetic newly reviewed exact-model source'
            changed.setdefault('evidence', {})['research_trace'] = release_fixtures.trace_for(changed)
            raw, review = reuse_review(previous, current)
            prior = root/'previous-ledger.json'; prior.write_bytes(raw)
            reviewed = root/'reuse-review.json'; reviewed.write_text(json.dumps(review), encoding='utf-8')
            ledger.write_text(json.dumps(current), encoding='utf-8')
            out = root/'updated.xlsx'
            args = ['research_export', '--write-workbook', '--ledger', str(ledger), '--workbook', str(out),
                    '--previous-ledger', str(prior), '--research-reuse', str(reviewed)]
            with patch.object(sys, 'argv', args), contextlib.redirect_stdout(io.StringIO()): export.main()
            self.assertTrue(out.is_file())
            self.assertEqual(old_workbook.read_bytes(), old_bytes)
            summary = json.loads(out.with_suffix('.research-summary.json').read_text(encoding='utf-8'))
            self.assertEqual(summary['researchTrace']['state'], 'LEGACY_TRACE_INCOMPLETE')
            self.assertEqual(summary['researchTrace']['checkedFields'], 1)
            self.assertEqual(summary['researchTrace']['missingFields'], len(previous['fields'])-1)
            self.assertEqual(summary['researchTrace']['legacyReuse']['previousLedgerSha256'], hashlib.sha256(raw).hexdigest())
            self.assertEqual(summary['workbookSha256'], hashlib.sha256(out.read_bytes()).hexdigest())
            # The same revision without a bound baseline still cannot skip the audit.
            blocked = root/'blocked.xlsx'
            args = ['research_export', '--write-workbook', '--ledger', str(ledger), '--workbook', str(blocked)]
            with patch.object(sys, 'argv', args), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit): export.main()
            self.assertFalse(blocked.exists())


if __name__ == '__main__': unittest.main()
