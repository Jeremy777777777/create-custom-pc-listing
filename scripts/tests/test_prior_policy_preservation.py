"""Historical integrity can survive policy updates without granting new QA."""
import tempfile, unittest, subprocess, sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).parents[1]))
import gallery_engine as g

class PreservationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.p=self.root/'product generated photo/TEST';self.p.mkdir(parents=True)
        self.git('init','-q');self.git('config','user.name','Fixture');self.git('config','user.email','fixture@example.invalid')
        g.write(self.p/'product-facts.json',{'internalId':'TEST','cpu':'Fixture CPU'})
        g.write(self.p/'style-lock.json',{'status':'APPROVED','recipePath':'assets/recipe.json'})
        (self.root/'assets').mkdir();g.write(self.root/'assets/recipe.json',{'version':'fixture-v1'})
        # review_inputs resolves recipePath against its repository, so the unit
        # fixture mocks only binding calculation, not Git byte proof.
        self.policy={n:'old policy '+n for n in g.POLICY_INPUTS}
        (self.root/'references').mkdir()
        for n,t in self.policy.items():(self.root/'references'/n).write_text(t,encoding='utf-8')
        for n in ('visual-review.json','semantic-review.json'):g.write(self.p/n,{'reviewInputsSha256':'trusted-old-binding'})
        (self.p/'PT01.png').write_bytes(b'fixture-image-bytes')
        self.git('add','.');self.git('commit','-qm','trusted fixture')
        self.base=self.git('rev-parse','HEAD').strip()
    def git(self,*args):return subprocess.check_output(['git',*args],cwd=self.root,text=True,stderr=subprocess.STDOUT)
    def preserve(self):
        with patch.object(g,'review_inputs',return_value='trusted-old-binding') as binding,patch.object(g,'validate') as validate:
            result=g.preserve_prior_policy_gallery(self.root,self.p,self.base)
            binding.assert_called_once_with(self.p,policy_text=self.policy)
            validate.assert_called_once_with(self.p,trusted_policy_binding='trusted-old-binding',preserve_unbound_research=False)
            return result
    def test_unchanged_bytes_are_historical_not_current_and_not_mutated(self):
        before={p.name:p.read_bytes() for p in self.p.iterdir()}
        (self.root/'references/image-spec.md').write_text('new desktop rule',encoding='utf-8')
        result=self.preserve();self.assertIs(result['currentPolicyQa'],False)
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.p.iterdir()})
    def test_changed_image_cannot_preserve_even_if_committed(self):
        (self.p/'PT01.png').write_bytes(b'changed');self.git('add','.');self.git('commit','-qm','change')
        with self.assertRaisesRegex(ValueError,'Changed product bytes'):self.preserve()
    def test_changed_facts_and_review_cannot_preserve(self):
        for n in ('product-facts.json','visual-review.json'):
            with self.subTest(file=n):
                p=self.p/n;before=p.read_bytes();p.write_bytes(b'{}')
                with self.assertRaisesRegex(ValueError,'Changed product bytes'):self.preserve()
                p.write_bytes(before)
    def test_changed_recipe_cannot_preserve(self):
        g.write(self.root/'assets/recipe.json',{'version':'changed'})
        with self.assertRaisesRegex(ValueError,'Changed recipe'):self.preserve()
    def test_added_or_deleted_file_cannot_preserve(self):
        p=self.p/'unexpected.png';p.write_bytes(b'new')
        with self.assertRaisesRegex(ValueError,'inventory'):self.preserve()
        p.unlink();(self.p/'PT01.png').unlink()
        with self.assertRaisesRegex(ValueError,'inventory'):self.preserve()
    def test_missing_trusted_base_and_new_gallery_cannot_preserve(self):
        with self.assertRaisesRegex(ValueError,'Trusted base'):g.preserve_prior_policy_gallery(self.root,self.p,None)
        new=self.root/'product generated photo/NEW';new.mkdir()
        with self.assertRaisesRegex(ValueError,'New gallery'):g.preserve_prior_policy_gallery(self.root,new,self.base)
    def test_stale_binding_not_explained_by_base_is_rejected(self):
        with patch.object(g,'review_inputs',return_value='different-binding'),patch.object(g,'validate') as validate:
            with self.assertRaisesRegex(ValueError,'does not match trusted-base'):g.preserve_prior_policy_gallery(self.root,self.p,self.base)
            validate.assert_not_called()
    def test_later_push_can_find_matching_committed_ancestor_policy(self):
        original=self.base
        (self.root/'references/image-spec.md').write_text('new desktop rule',encoding='utf-8')
        self.git('add','.');self.git('commit','-qm','policy amendment');self.base=self.git('rev-parse','HEAD').strip()
        def binding(directory,include_research=True,policy_text=None):
            return 'trusted-old-binding' if policy_text==self.policy else 'new-policy-binding'
        with patch.object(g,'review_inputs',side_effect=binding),patch.object(g,'validate') as validate:
            result=g.preserve_prior_policy_gallery(self.root,self.p,self.base)
            self.assertEqual(result['policyCommit'],original);self.assertFalse(result['currentPolicyQa'])
            validate.assert_called_once_with(self.p,trusted_policy_binding='trusted-old-binding',preserve_unbound_research=False)

if __name__=='__main__':unittest.main()
