"""Commercial names and model numbers have independent evidence roles."""
import copy
import unittest
from product_metadata import check_metadata_consistency

class ModelIdentityRoleTests(unittest.TestCase):
    def selected(self):
        return {('Product Details','Model Name'):{'status':'VERIFIED','final_value':'ThinkPad X1 2-in-1 Gen 10'},
                ('Product Details','Model Number'):{'status':'INPUT_UNVERIFIED','final_value':None,'value_candidate':'21Q0CTO1WW'}}

    def test_verified_name_does_not_promote_or_require_number_candidate(self):
        selected=self.selected();before=copy.deepcopy(selected)
        check_metadata_consistency(selected,{'identity':{'oemModel':'ThinkPad X1 2-in-1 Gen 10'}},True)
        self.assertEqual(selected,before)

    def test_wrong_generation_is_still_rejected(self):
        for strict in (False,True):
            with self.subTest(strict=strict),self.assertRaisesRegex(ValueError,'Model Name / Model Number'):
                check_metadata_consistency(self.selected(),{'identity':{'oemModel':'ThinkPad X1 2-in-1 Gen 9'}},strict)

    def test_candidate_number_never_satisfies_image_identity(self):
        with self.assertRaisesRegex(ValueError,'unresolved'):
            check_metadata_consistency(self.selected(),{'identity':{'oemModel':'21Q0CTO1WW'}},True)

    def test_explicit_number_must_be_verified_even_with_verified_name(self):
        with self.assertRaisesRegex(ValueError,'Model Number'):
            check_metadata_consistency(self.selected(),{'identity':{'oemModel':'ThinkPad X1 2-in-1 Gen 10','oemModelNumber':'21Q0CTO1WW'}},True)

    def test_legacy_number_identity_keeps_exact_matching(self):
        selected={('Product Details','Model Number'):{'status':'VERIFIED','final_value':'QCM1250'}}
        check_metadata_consistency(selected,{'identity':{'oemModel':'QCM1250'}},True)
        with self.assertRaisesRegex(ValueError,'Model Name / Model Number'):
            check_metadata_consistency(selected,{'identity':{'oemModel':'QCM1255'}},True)

    def test_unresolved_name_cannot_be_accepted_from_an_unrelated_number(self):
        selected=self.selected();selected[('Product Details','Model Name')].update(status='TBD',final_value=None)
        selected[('Product Details','Model Number')].update(status='VERIFIED',final_value='21Q0CTO1WW')
        with self.assertRaisesRegex(ValueError,'Model Name / Model Number'):
            check_metadata_consistency(selected,{'identity':{'oemModel':'ThinkPad X1 2-in-1 Gen 10'}},True)

if __name__=='__main__':unittest.main()
