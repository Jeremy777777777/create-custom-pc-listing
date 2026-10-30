import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gaming_visual_plan import check, PROFILE


class GamingVisualPlanTests(unittest.TestCase):
    def setUp(self):
        self.registry = {'methodProfile': PROFILE, 'references': [{'driveFileId': 'selected-reference', 'sha256': 'a' * 64}]}
        self.plan = {'designSeries': 'GAMING', 'family': 'G22', 'methodProfile': PROFILE,
                     'productId': 'TEST', 'configurationId': 'actual-config', 'selectedSlots': ['PT04.png'],
                     'images': [{'file': 'PT04.png', 'primaryTheme': 'Display explanation',
                                 'visualProof': 'DISPLAY_DETAIL', 'visualExplanation': {
                                     'subject': 'Actual display', 'buyerUnderstanding': 'Understand the display specifications',
                                     'mainVisual': 'Actual screen with detail enlargement', 'composition': 'Display leads, labels adjacent',
                                     'actualProductSourceIds': ['official-front'], 'exactCopy': ['Verified display label'],
                                     'avoid': ['Detached number cards'], 'selectedCompositionInvariants': ['Display focal scale'],
                                     'referenceImageIds': ['selected-reference'],
                                     'referenceImageSha256': {'selected-reference': 'a' * 64},
                                     'labelToVisualMap': [{'label': 'Verified display label', 'visual': 'Display detail'}]}}]}

    def test_complete_plan_does_not_grant_visual_or_user_approval(self):
        result = check(self.plan, self.registry)
        self.assertEqual(result['visualQuality'], 'REQUIRES_ACTUAL_IMAGE_REVIEW')
        self.assertEqual(result['userApproval'], 'NOT_GRANTED_BY_THIS_CHECK')

    def test_wrong_reference_version_is_rejected(self):
        self.plan['images'][0]['visualExplanation']['referenceImageSha256']['selected-reference'] = 'b' * 64
        with self.assertRaisesRegex(ValueError, 'ID/hash'):
            check(self.plan, self.registry)

    def test_every_selected_page_needs_explanation(self):
        self.plan['selectedSlots'].append('PT05.png')
        with self.assertRaisesRegex(ValueError, 'PT05'):
            check(self.plan, self.registry)

    def test_minipc_and_main_cannot_inherit_gaming_pt_check(self):
        for changes in ({'designSeries': 'MINI_PC'}, {'selectedSlots': ['MAIN-STRICT.jpg']}):
            plan = copy.deepcopy(self.plan)
            plan.update(changes)
            with self.assertRaises(ValueError):
                check(plan, self.registry)

    def test_flat_product_hero_seed_and_empty_mapping_are_rejected(self):
        self.plan['images'][0]['visualProof'] = 'PRODUCT_HERO'
        with self.assertRaisesRegex(ValueError, 'product-hero seed'):
            check(self.plan, self.registry)
        self.plan['images'][0]['visualProof'] = 'DISPLAY_DETAIL'
        self.plan['images'][0]['visualExplanation']['labelToVisualMap'] = []
        with self.assertRaisesRegex(ValueError, 'mapping'):
            check(self.plan, self.registry)


if __name__ == '__main__':
    unittest.main()
