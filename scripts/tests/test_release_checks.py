"""Synthetic research, directory, privacy and previous-version boundary checks."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import research_audit as audit
import delivery_context as context
import delivery_privacy as privacy
import drive_delivery as drive
import github_drive_sync as sync


def trace_for(fact):
    status = fact['status']
    return {'version': 1, 'field_class': 'TECHNICAL', 'reason': 'Synthetic field evidence',
            'start': 'NO_LINKED_SERIAL', 'start_basis': 'Synthetic ERP search has no serial',
            'outcome': {'VERIFIED': 'CONFIRMED', 'NOT_APPLICABLE': 'NOT_APPLICABLE',
                        'INPUT_UNVERIFIED': 'CANDIDATE', 'CONFLICT': 'CONFLICT',
                        'SOURCE_UNAVAILABLE': 'BLOCKED', 'TBD': 'INCOMPLETE'}[status],
            'exhausted': False, 'routes': [{'route': 'OEM_MODEL', 'result': 'REVIEWED',
                'query': 'Synthetic exact model', 'reference': 'https://example.test/model',
                'detail': 'Synthetic document', 'reviewed_date': '2026-10-20'}]}


class ReleaseChecks(unittest.TestCase):
    def ledger(self):
        fact = {'id': 'ram', 'status': 'TBD', 'final_value': None, 'evidence': {}}
        fact['evidence']['research_trace'] = trace_for(fact)
        return {'facts': [fact], 'fields': [{'selected_fact': 'ram'}]}

    def test_new_research_missing_trace_and_fake_exhaustion_fail(self):
        data = self.ledger()
        self.assertEqual(audit.validate(data, True)['checkedFields'], 1)
        data['facts'][0]['evidence'] = {}
        self.assertEqual(audit.validate(data)['state'], 'LEGACY_TRACE_INCOMPLETE')
        with self.assertRaisesRegex(ValueError, 'missing count'): audit.validate(data, True)
        data = self.ledger()
        data['facts'][0]['evidence']['research_trace'].update(exhausted=True, outcome='NOT_FOUND')
        with self.assertRaisesRegex(ValueError, 'route dispositions'): audit.validate(data, True)

    def test_exhausted_candidate_and_blocked_not_found(self):
        data = self.ledger(); fact = data['facts'][0]; evidence = fact['evidence']
        trace = evidence['research_trace']
        trace.update(exhausted=True, outcome='NOT_FOUND', stop_reason='All distinct relevant routes checked',
                     candidate_decision='NO_SUPPORT', candidate_reason='No matching evidence')
        trace['routes'] = [{**trace['routes'][0], 'route': route, 'result': 'NO_MATCH'} for route in sorted(audit.ROUTES)]
        audit.validate(data, True)
        trace['routes'][0]['result'] = 'BLOCKED'
        with self.assertRaisesRegex(ValueError, 'Blocked access'): audit.validate(data, True)
        fact.update(status='INPUT_UNVERIFIED', value_candidate=32, value_candidate_source='Synthetic matched parts record')
        evidence.update(candidate_rationale='Exact part match strongest', candidate_missing_confirmation='Current installation')
        trace.update(outcome='CANDIDATE', candidate_decision='SELECTED', candidate_reason='Part match')
        audit.validate(data, True)
        fact['status'] = 'VERIFIED'
        with self.assertRaises(ValueError): audit.validate(data, True)

    def test_no_confirmed_fact_with_incomplete_trace_or_unsupported_modification(self):
        data = self.ledger(); fact = data['facts'][0]
        fact['status'] = 'VERIFIED'
        with self.assertRaisesRegex(ValueError, 'incomplete'): audit.validate(data, True)
        fact['evidence']['research_trace'] = trace_for(fact)
        fact['evidence']['sold_modification'] = {'after': '32 GB'}
        with self.assertRaisesRegex(ValueError, 'installation evidence'): audit.validate(data, True)

    def delivery(self, root):
        product = root/'VL-99999'; product.mkdir()
        (product/'VL-99999_RESEARCH_REVIEW.xlsx').write_bytes(b'synthetic inventory fixture')
        plan = drive.plan(product, 'TEST-RUN', ['VL-99999_RESEARCH_REVIEW.xlsx'])
        row = plan['files'][0]; name = row['relativePath']; stamp = datetime.now(timezone.utc).isoformat()
        policy = json.loads((context.ROOT/'assets/delivery-storage.json').read_text())
        ids = [policy['projectFolderId'], policy['productsFolderId'], 'p', 'research', 'final']
        names = ['Project', '20_PRODUCTS', 'VL-99999', '03_RESEARCH', 'FINAL']
        nodes = [{'id': id_, 'name': n, 'mimeType': context.FOLDER, 'parents': [] if i == 0 else [ids[i-1]], 'readBackAtUtc': stamp} for i,(id_,n) in enumerate(zip(ids,names))]
        ctx = {'productId': 'VL-99999', 'serialsUsed': False, 'folders': nodes,
               'fileRoles': {name:'RESEARCH'}, 'privacyChecks':{name:{'state':'DELIVERY_PRIVACY_SCREEN_PASS','inputSha256':row['sha256'],'manualReviewRequired':False,'serialInventoryDeclared':False}}}
        remote = {'files':[{'relativePath': name,'id':'file','name':name,'parents':['final'],
                    'mimeType':row['mimeType'],'size':row['size'],'sha256Checksum':row['sha256'],
                    'webViewLink':'https://drive.google.com/file/d/file/view','readBackAtUtc':stamp}]}
        return product, plan, remote, {name:'final'}, ctx

    def test_correct_chain_and_privacy_required_for_complete_receipt(self):
        with tempfile.TemporaryDirectory() as temp:
            product, plan, remote, destinations, ctx = self.delivery(Path(temp))
            self.assertEqual(drive.verify(product,plan,remote,destinations)['deliveryState'], 'DRIVE_BYTES_MATCHED_CONTEXT_UNCHECKED')
            self.assertEqual(drive.verify(product,plan,remote,destinations,ctx)['deliveryState'], 'DRIVE_DELIVERY_VERIFIED')
            for change in ('wrong-product', 'wrong-parent', 'role', 'privacy', 'serial'):
                bad = copy.deepcopy(ctx); name = plan['files'][0]['relativePath']
                if change == 'wrong-product': bad['folders'][2]['name'] = 'VL-OTHER'
                if change == 'wrong-parent': bad['folders'][3]['parents'] = ['unrelated']
                if change == 'role': bad['fileRoles'][name] = 'LISTING'
                if change == 'privacy': bad['privacyChecks'][name]['inputSha256'] = '0'*64
                if change == 'serial': bad['serialsUsed'] = True
                with self.subTest(change=change), self.assertRaises(ValueError): drive.verify(product,plan,remote,destinations,bad)

    def test_revision_changes_and_scoped_drive_downgrade_rejected(self):
        record = {'productId':'VL-TEST','readBackAtUtc':datetime.now(timezone.utc).isoformat(),
                  'files':[{'relativePath':'research-ledger.json','id':'x','sha256':'a'*64,'parentFolderId':'f'}]}
        context.check_revision(record, copy.deepcopy(record))
        bad = copy.deepcopy(record); bad['files'][0]['sha256'] = 'b'*64
        with self.assertRaisesRegex(ValueError,'CURRENT_REVISION_CHANGED'): context.check_revision(record,bad)
        previous = b'{"productId":"VL-TEST","configurationId":"BASE","facts":[],"fields":[]}'
        context.check_history(previous,previous,hashlib.sha256(previous).hexdigest())
        with self.assertRaisesRegex(ValueError,'downgraded'): context.check_history(previous,b'[]',hashlib.sha256(previous).hexdigest())
        with self.assertRaisesRegex(ValueError,'baseline'): context.check_history(previous,previous,'0'*64)

    def test_privacy_xlsx_hidden_cells_comments_links_and_serial_inventory(self):
        import openpyxl
        from openpyxl.comments import Comment
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)/'test.xlsx'; book = openpyxl.Workbook(); hidden = book.create_sheet('hidden'); hidden.sheet_state='hidden'
            hidden['A1']='SYNTHETIC-PRIVATE-123'; hidden['B1'].comment=Comment('SYNTHETIC-PRIVATE-123','test')
            hidden['C1'].hyperlink='https://example.test/?serial=SYNTHETIC-PRIVATE-123'
            book.save(p); book.close()
            with self.assertRaisesRegex(ValueError,'inventory'): privacy.screen_file(p, serials_used=True)
            result=privacy.screen_file(p,['SYNTHETIC-PRIVATE-123'],True)
            self.assertEqual(result['state'],'PRIVATE_CONTENT_DETECTED')
            self.assertNotIn('SYNTHETIC-PRIVATE-123',json.dumps(result))

    def test_image_privacy_needs_actual_current_byte_inspection(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'test.png'; Image.new('RGB',(4,4),'white').save(p)
            result=privacy.screen_file(p,serials_used=False)
            self.assertEqual(result['state'],'MANUAL_REVIEW_REQUIRED')
            review={'sha256':result['inputSha256'],'result':'NO_PRIVATE_CONTENT','reviewer':'Synthetic test','notes':'Synthetic plain white image','reviewedAtUtc':datetime.now(timezone.utc).isoformat()}
            self.assertEqual(privacy.screen_file(p,serials_used=False,visual_review=review)['state'],'DELIVERY_PRIVACY_SCREEN_PASS')
            review['sha256']='0'*64
            with self.assertRaises(ValueError): privacy.screen_file(p,serials_used=False,visual_review=review)

    def test_missing_runner_auth_fails_before_planning_without_secret_output(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); config=root/'config.json'; config.write_text('{}'); output=root/'result.json'
            argv=['sync','--source',str(root),'--config',str(config),'--commit','a'*40,'--repository','example/repo','--branch','main','--output',str(output)]
            with patch.object(sys,'argv',argv), patch.dict(sync.os.environ,{},clear=True), patch.object(sync,'make_plan') as planner:
                self.assertEqual(sync.main(),1)
                planner.assert_not_called()
            self.assertEqual(json.loads(output.read_text())['state'],'BLOCKED_MISSING_DRIVE_AUTH')


if __name__ == '__main__': unittest.main()
