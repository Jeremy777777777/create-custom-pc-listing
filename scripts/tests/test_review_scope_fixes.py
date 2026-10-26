"""Regression fixtures are synthetic; they do not approve real product evidence."""
import contextlib
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import delivery_privacy as privacy
import gallery_engine as g
import image_review_scope as scope
import research_audit as audit
import research_export as export
import research_handoff as handoff
import test_research_export as fixtures
import test_production_revision as revisions
import test_workflow_hardening as galleries
import test_release_checks as release


class PrivacyNumbers(unittest.TestCase):
    def test_numeric_and_exponent_serials_are_blocked_without_echoing_values(self):
        serial = '123456789012345678901'
        for literal in (serial, serial + '.0', '1.23456789012345678901e20', '"' + serial + '"'):
            with self.subTest(literal=literal), tempfile.TemporaryDirectory() as temp:
                path = Path(temp)/'record.json'
                path.write_text('{"nested":[{"value":' + literal + '}]}')
                result = privacy.screen_file(path, [serial], serials_used=True)
                self.assertEqual(result['state'], 'PRIVATE_CONTENT_DETECTED')
                self.assertNotIn(serial, json.dumps(result))
                out = Path(temp)/'result.json'
                with contextlib.redirect_stdout(io.StringIO()):
                    privacy.main(['check', '--input', str(path), '--private-values-file',
                                  str(self.private_file(Path(temp), serial)), '--output', str(out)])
                self.assertIn('KNOWN_PRIVATE_VALUE', out.read_text())

    def private_file(self, root, serial):
        path = root/'private.json'; path.write_text(json.dumps([serial])); return path

    def test_ordinary_capacity_and_boolean_do_not_match_serial(self):
        self.assertEqual(privacy.findings({'ram': 32, 'ok': True, 'rate': 3.5}, ['1234567890123']), [])


class SummaryContinuity(unittest.TestCase):
    def test_refresh_preserves_reuse_and_false_trace_claim_fails_handoff(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); product = root/'product generated photo/TEST-PC'; product.mkdir(parents=True)
            book, data, workbook, ledger = fixtures.ResearchExportTests().full_fixture(product); book.close()
            canonical = product/'research-ledger.json'; ledger.rename(canonical); ledger = canonical
            (root/'assets').mkdir()
            (root/'assets/listing-workbook-template.xlsx').write_bytes((export.ROOT/'assets/listing-workbook-template.xlsx').read_bytes())
            raw, reuse = revisions.reuse_review(data, data)
            result = export.run(export.ROOT/'assets/listing-workbook-template.xlsx', ledger, workbook, 'draft')
            result['researchTrace'] = audit.validate(data, True, raw, reuse)
            summary = workbook.with_suffix('.research-summary.json')
            export.write_summary(summary, result, workbook, ledger)
            original = json.loads(summary.read_text())['researchTrace']
            args = ['research_export', '--ledger', str(ledger), '--workbook', str(workbook), '--summary-output', str(summary)]
            stdout = io.StringIO()
            with patch.object(sys, 'argv', args), contextlib.redirect_stdout(stdout): export.main()
            self.assertEqual(json.loads(summary.read_text())['researchTrace'], original)
            self.assertEqual(json.loads(stdout.getvalue())['researchTrace'], original)
            self.assertEqual(handoff.check_research_summaries(root), 1)
            document = json.loads(summary.read_text())
            document['researchTrace'].update(state='RESEARCH_TRACE_RECORDED', missingFields=0, checkedFields=len(data['fields']))
            summary.write_text(json.dumps(document)); before = summary.read_bytes()
            with self.assertRaisesRegex(ValueError, 'trace summary'): handoff.check_research_summaries(root)
            with patch.object(sys, 'argv', args), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit): export.main()
            self.assertEqual(before, summary.read_bytes())

    def test_retained_dependency_changes_and_missing_trace_cannot_pass(self):
        helper = revisions.ProductionRevisionTests()
        _, data, raw, reuse = helper.legacy_fixture()
        trace = audit.validate(data, True, raw, reuse)
        audit.validate_summary_trace(data, trace)
        data['facts'][1]['source'] = 'Changed synthetic dependency'
        with self.assertRaisesRegex(ValueError, 'stale'): audit.validate_summary_trace(data, trace)
        with self.assertRaises(ValueError): audit.validate_summary_trace(data, None)

    def test_new_research_can_refresh_a_nonreuse_summary(self):
        with tempfile.TemporaryDirectory() as temp:
            book, data, workbook, ledger = fixtures.ResearchExportTests().full_fixture(Path(temp)); book.close()
            summary = workbook.with_suffix('.research-summary.json')
            args = ['research_export', '--ledger', str(ledger), '--workbook', str(workbook), '--summary-output', str(summary)]
            with patch.object(sys, 'argv', args), contextlib.redirect_stdout(io.StringIO()): export.main()
            fact = data['facts'][0]; fact.setdefault('evidence', {})['research_trace'] = release.trace_for(fact)
            ledger.write_text(json.dumps(data))
            with patch.object(sys, 'argv', args), contextlib.redirect_stdout(io.StringIO()): export.main()
            trace = json.loads(summary.read_text())['researchTrace']
            self.assertEqual(trace['checkedFields'], 1)
            self.assertIsNone(trace['legacyReuse'])


class ScopedImageReviews(unittest.TestCase):
    def fixture(self, root):
        product = root/'TEST-PC'; product.mkdir()
        helper = galleries.GalleryBoundaries(); self.addCleanup(helper.doCleanups); helper.build(product)
        g.write(product/'product-facts.json', {'internalId': 'TEST-PC', 'selectedBaseConfiguration': {'id': 'BASE-A'}})
        data = fixtures.ResearchExportTests().ledger(('Product Details', 'RAM Memory Maximum Size'))
        data['facts'][0]['fact_scope'] = 'PLATFORM_CAPABILITY'
        port = {**copy.deepcopy(data['facts'][0]), 'id': 'ports', 'attribute': 'Number of USB 3.0 Ports', 'final_value': 4, 'fact_scope': 'SOLD_BASE'}
        data['facts'].append(port)
        data['fields'].append({'sheet': port['sheet'], 'attribute': port['attribute'], 'selected_fact': 'ports'})
        g.write(product/'research-ledger.json', data)
        return product, data

    def reviews(self, product):
        for filename, names in [('visual-review.json', g.NAMES), ('semantic-review.json', g.PT)]:
            entries = []
            for name in names:
                field = 'Number of USB 3.0 Ports' if name == 'PT08.png' else 'RAM Memory Maximum Size'
                deps = {'fields': [['Product Details', field]], 'productPaths': [],
                        'basis': 'Synthetic fixture only: covers the single declared claim'}
                entries.append({'file': name, 'sha256': g.digest(product/name), 'result': 'PASS',
                                'notes': 'Synthetic fixture', 'dependencies': deps,
                                'reviewInputsSha256': scope.binding(product, name, deps)})
            g.write(product/filename, {'schemaVersion': 4, 'result': 'PASS', 'reviewer': 'Synthetic fixture',
                                      'reviewedAtUtc': '2026-10-14T12:00:00Z',
                                      'galleryInventorySha256': {n: g.digest(product/n) for n in g.NAMES}, 'images': entries})

    def test_full_acceptance_and_unrelated_ram_change_preserves_ports_partial_review(self):
        with tempfile.TemporaryDirectory() as temp:
            product, data = self.fixture(Path(temp)); self.reviews(product)
            g.accept(product); g.validate(product)
            data['facts'][0]['final_value'] = 64; g.write(product/'research-ledger.json', data)
            with self.assertRaisesRegex(ValueError, 'Per-image'): g.validate(product)
            for file in ('visual-review.json', 'semantic-review.json'):
                report = g.read(product/file); report['images'] = [r for r in report['images'] if r['file'] == 'PT08.png']; g.write(product/file, report)
            g.accept(product, slots=['PT08.png']); g.validate_partial(product, ['PT08.png'])
            data['facts'][1]['final_value'] = 6; g.write(product/'research-ledger.json', data)
            with self.assertRaisesRegex(ValueError, 'Per-image'): g.validate_partial(product, ['PT08.png'])

    def test_common_style_identity_and_image_bytes_still_invalidate(self):
        for change in ('style', 'identity', 'bytes'):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as temp:
                product, data = self.fixture(Path(temp)); self.reviews(product)
                if change == 'style': g.write(product/'style-lock.json', {'status': 'APPROVED', 'recipeVersion': 'changed'})
                if change == 'identity':
                    facts = g.read(product/'product-facts.json'); facts['color'] = 'changed'; g.write(product/'product-facts.json', facts)
                if change == 'bytes': (product/'PT08.png').write_bytes(b'changed synthetic bytes')
                with self.assertRaises(ValueError): g.evidence(product/'visual-review.json', g.NAMES, product)

    def test_missing_dependency_and_disagreeing_reviews_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            product, data = self.fixture(Path(temp)); self.reviews(product)
            with self.assertRaises(ValueError): scope.binding(product, 'PT08.png', {'fields': [], 'productPaths': [], 'basis': 'empty'})
            report = g.read(product/'semantic-review.json'); report['images'][0]['dependencies']['basis'] = 'different declaration'
            g.write(product/'semantic-review.json', report)
            with self.assertRaisesRegex(ValueError, 'disagree'): scope.agree(product)


if __name__ == '__main__': unittest.main()
