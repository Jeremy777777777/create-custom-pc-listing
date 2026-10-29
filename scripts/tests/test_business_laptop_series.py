from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import business_laptop_series as b


class BusinessSeriesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)/'repo'
        self.p = Path(self.temp.name)/'VL-TEST'
        self.p.mkdir(); (self.repo/'assets/branding/library').mkdir(parents=True)
        source = Path(__file__).resolve().parents[2]
        (self.repo/b.PROFILE).write_bytes((source/b.PROFILE).read_bytes())
        self.write(self.repo/'assets/branding/library/asset-registry.json', {'assets': []})
        self.write(self.p/'product-facts.json', {'productId':'VL-TEST'})
        self.write(self.p/'style-lock.json', {'status':'PENDING'})
        self.ledger={'productId':'VL-TEST','configurationId':'base','facts':[
            {'id':str(i),'status':'VERIFIED','final_value':i,'fact_scope':'SOLD_BASE'} for i in range(1,9)]}
        self.write(self.p/'research-ledger.json',self.ledger)
        self.info={'productId':'VL-TEST','configurationId':'base','ledgerSha256':b.digest(self.p/'research-ledger.json'),'images':[
            {'file':f'PT{i:02d}.png','buyerQuestion':'Which useful feature?','headline':'Verified proof','primaryTheme':str(i),
             'visualProof':'Native detail','fullConfigurationOverview':i==3,'claims':[{'text':'Verified fact','factIds':[str(i)]}]} for i in range(1,9)]}
        self.write(self.p/'information.json', self.info)
        for n in ['PT03.png','PT04.png','PT06.png']: (self.p/n).write_bytes(('approved '+n).encode())

    @staticmethod
    def write(path,data): path.write_text(json.dumps(data),encoding='utf8')

    def plan(self,preserve=()): return b.build(self.p,'information.json','a'*40,'Actual full-series request',preserve,self.repo)

    def test_new_series_accounts_for_all_eleven_without_granting_approval(self):
        plan=self.plan(); result=b.check(plan,self.p,self.repo)
        self.assertEqual(result['produceCount'],11)
        self.assertEqual(plan['styleApprovalStatus'],'PENDING')
        self.assertFalse(result['productionApprovalGranted'])
        self.assertEqual(result['visualQa'],'NOT_ASSESSED')

    def test_continuation_preserves_three_and_produces_remaining_eight(self):
        result=b.check(self.plan(['PT03.png','PT04.png','PT06.png']),self.p,self.repo)
        self.assertEqual(result['produceCount'],8)
        self.assertEqual(len(result['preservedSlots']),3)

    def test_six_file_pilot_and_duplicate_slot_cannot_claim_complete(self):
        plan=self.plan(); plan['slots']=plan['slots'][:6]
        with self.assertRaises(ValueError): b.check(plan,self.p,self.repo)
        plan=self.plan();plan['slots'][-1]=deepcopy(plan['slots'][0])
        with self.assertRaises(ValueError): b.check(plan,self.p,self.repo)

    def test_modified_approved_image_is_rejected(self):
        plan=self.plan(['PT03.png']);(self.p/'PT03.png').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'preserved bytes'): b.check(plan,self.p,self.repo)

    def test_changed_ledger_information_and_style_require_reconciliation(self):
        for name in ['information.json','style-lock.json','research-ledger.json']:
            original=(self.p/name).read_bytes();plan=self.plan()
            (self.p/name).write_bytes(original+b'\n')
            with self.assertRaises(ValueError): b.check(plan,self.p,self.repo)
            (self.p/name).write_bytes(original)

    def test_profile_change_and_fake_qa_are_rejected(self):
        plan=self.plan();original=(self.repo/b.PROFILE).read_bytes()
        (self.repo/b.PROFILE).write_bytes(original+b'\n')
        with self.assertRaises(ValueError): b.check(plan,self.p,self.repo)
        (self.repo/b.PROFILE).write_bytes(original)
        plan['visualQa']='PASS'
        with self.assertRaises(ValueError): b.check(plan,self.p,self.repo)
        plan=self.plan();plan['styleApprovalStatus']='APPROVED'
        with self.assertRaises(ValueError): b.check(plan,self.p,self.repo)

    def test_wrong_identity_unresolved_fact_and_unentitled_logo_are_rejected(self):
        self.write(self.p/'product-facts.json',{'productId':'OTHER'})
        with self.assertRaises(ValueError): self.plan()
        self.write(self.p/'product-facts.json',{'productId':'VL-TEST'})
        self.ledger['facts'][0]['status']='CONFLICT';self.write(self.p/'research-ledger.json',self.ledger)
        self.info['ledgerSha256']=b.digest(self.p/'research-ledger.json');self.write(self.p/'information.json',self.info)
        with self.assertRaises(ValueError): self.plan()
        self.ledger['facts'][0]['status']='VERIFIED';self.write(self.p/'research-ledger.json',self.ledger)
        self.info['ledgerSha256']=b.digest(self.p/'research-ledger.json')
        self.info['images'][1]['brandAssetIds']=['unverified-word'];self.write(self.p/'information.json',self.info)
        with self.assertRaises(ValueError): self.plan()

    def test_missing_preserved_file_invalid_action_and_escaping_source_fail(self):
        with self.assertRaises(FileNotFoundError): self.plan(['PT08.png'])
        with self.assertRaises(ValueError): self.plan(['PT03.png','PT03.png'])
        plan=self.plan();plan['slots'][0]['action']='SKIP'
        with self.assertRaises(ValueError): b.check(plan,self.p,self.repo)
        with self.assertRaises(ValueError): b.build(self.p,'../information.json','a'*40,'request',repo=self.repo)


if __name__=='__main__': unittest.main()
