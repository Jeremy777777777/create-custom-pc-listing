import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from customer_visible_content import validate_customer_text
from test_gaming_visual_plan import GamingVisualPlanTests
from gaming_visual_plan import check


class CustomerVisibleContentTests(unittest.TestCase):
    def test_internal_markers_cannot_leak_into_copy(self):
        for text in ('HP Victus / VL-1221', 'vd\u2011744', 'STYLE PREVIEW',
                     'PT03 / SUPPLIED CONFIGURATION', '03 / CAMERA + VOICE'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                validate_customer_text(text)

    def test_real_models_specs_and_customer_headlines_remain_valid(self):
        validate_customer_text('HP Victus 15-fb3093dx | Ryzen 7 7445HS | RTX 4050 | 16GB DDR5')
        validate_customer_text('THE POWER BEHIND YOUR PLAY.\nWindows 11 Pro\nIllustrative component view')

    def test_plan_checks_customer_labels_but_keeps_internal_identity(self):
        fixture = GamingVisualPlanTests()
        fixture.setUp()
        fixture.plan['productId'] = 'VL-1221'
        check(fixture.plan, fixture.registry)
        visual = fixture.plan['images'][0]['visualExplanation']
        visual['exactCopy'] = ['VL-1221']
        with self.assertRaisesRegex(ValueError, 'internal product ID'):
            check(fixture.plan, fixture.registry)
        visual['exactCopy'] = ['Display']
        visual['labelToVisualMap'][0]['label'] = 'PT04 / DISPLAY'
        with self.assertRaisesRegex(ValueError, 'page slot'):
            check(fixture.plan, fixture.registry)


if __name__ == '__main__':
    unittest.main()
