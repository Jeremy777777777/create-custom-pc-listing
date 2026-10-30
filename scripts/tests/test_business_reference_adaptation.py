"""Synthetic design declarations; never source authentication or rendered-image QA."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import business_information_plan as b
import test_business_information_plan as old
import test_business_laptop_series as series_fixture


class BusinessReferenceTests(unittest.TestCase):
    def setUp(self):
        fixture = old.BusinessPlanTests(); fixture.setUp()
        self.plan, self.ledger = fixture.plan, fixture.ledger
        self.ledger['facts'][0]['attribute'] = 'Manufacturer'
        self.ledger['facts'][2]['attribute'] = 'CPU Model'
        self.registry = {'assets': [
            {'id': 'lg-original', 'kind': 'HARDWARE_BRAND', 'match': {'oemBrand': 'LG'}},
            {'id': 'intel-original', 'kind': 'CPU_FAMILY_BADGE', 'match': {'cpuBrand': 'Intel'}}]}
        self.plan['brandContext'] = {'oemBrand': 'LG', 'cpuBrand': 'Intel'}
        self.plan['businessDesignReview'] = {'schemaVersion': 2,
            'referenceUrl': 'https://www.amazon.com/dp/B01N4C1TH4', 'observedDate': '2026-10-29',
            'lessonAndAdaptation': 'SYNTHETIC: distinct native detail, scene and option layouts with purposeful screen art.'}
        for i, row in enumerate(self.plan['images'], 1):
            row['brandAssetIds'] = ['lg-original']
            row['presentation'] = {'layoutFamily': b.LAYOUTS[row['file']],
                'visualSourceIds': ['SYNTHETIC-SOURCE-'+str(i)], 'proofPurpose': 'Explain this page with matching visual detail',
                'screen': {'shown': i in (1, 2, 3, 4, 7), 'contentId': 'screen-'+str(i), 'purpose': 'Page-specific task'},
                'sceneAction': 'Synthetic person prepares a document on the actual laptop',
                'logoAssignments': [{'assetId': 'lg-original', 'role': 'OEM', 'anchor': 'BRAND_CORNER',
                                     'readingPriority': 'SECONDARY', 'relatedFactIds': ['1'], 'purpose': 'Identify the manufacturer'}]}
        shots = [('WHOLE_PRODUCT','FULL','FRONT'), ('USAGE_SCENE','PARTIAL','SCENE'),
                 ('WHOLE_PRODUCT','FULL','THREE_QUARTER'), ('SCREEN_DETAIL','PARTIAL','DETAIL'),
                 ('OPTIONS_GUIDE','NONE','NONE'), ('PRODUCT_DETAIL','PARTIAL','DETAIL'),
                 ('PRODUCT_DETAIL','PARTIAL','DETAIL'), ('PRODUCT_DETAIL','PARTIAL','SIDE')]
        for row, (subject, visibility, framing) in zip(self.plan['images'], shots):
            item = row['presentation']
            item['storyboard'] = {'subject': subject, 'productVisibility': visibility, 'framing': framing,
                'productViewId': item['visualSourceIds'][0] if visibility != 'NONE' else None,
                'productPresenceReason': 'Synthetic: choose a subject to explain this page, not repeat the hero'}
        row = self.plan['images'][2]
        row['brandAssetIds'].append('intel-original')
        row['presentation']['logoAssignments'].append({'assetId': 'intel-original', 'role': 'CPU',
            'anchor': 'PROCESSOR_GROUP', 'readingPriority': 'SECONDARY', 'relatedFactIds': ['3'],
            'purpose': 'Identify the processor described beside this badge'})

    def check(self): return b.check(self.plan, self.ledger, 'actual', self.registry, require_presentation=True)

    def test_complete_distinct_design_and_semantic_logos_pass_without_granting_qa(self):
        result = self.check()
        self.assertEqual(result['presentationReview']['state'], 'BUSINESS_PRESENTATION_DECLARATIONS_CHECKED')
        self.assertFalse(result['productionApprovalGranted'])
        self.assertEqual(result['visualQa'], 'NOT_ASSESSED')

    def test_repeating_one_product_card_layout_is_rejected(self):
        for row in self.plan['images']: row['presentation']['layoutFamily'] = 'PRODUCT_HERO'
        with self.assertRaisesRegex(ValueError, 'distinct'): self.check()

    def test_repeating_one_screen_everywhere_is_rejected_even_with_reuse_reasons(self):
        for row in self.plan['images']:
            row['presentation']['screen'].update(contentId='same-dashboard', reuseReason='Same task again')
        with self.assertRaisesRegex(ValueError, 'one screen'): self.check()

    def test_purposeful_secondary_screen_reuse_requires_a_reason(self):
        screen = self.plan['images'][3]['presentation']['screen']
        screen['contentId'] = 'screen-1'
        with self.assertRaisesRegex(ValueError, 'distinct buyer-purpose'): self.check()
        screen['reuseReason'] = 'The display page zooms the same work document to explain the usable screen area'
        self.check()

    def test_scene_requires_a_real_action_relationship_and_sources(self):
        presentation = self.plan['images'][1]['presentation']
        presentation['sceneAction'] = ''
        with self.assertRaisesRegex(ValueError, 'scene'): self.check()
        presentation['sceneAction'] = 'Preparing a report'
        presentation['visualSourceIds'] = []
        with self.assertRaisesRegex(ValueError, 'visual sources'): self.check()

    def test_component_logo_cannot_float_away_or_become_the_primary_headline(self):
        placement = self.plan['images'][2]['presentation']['logoAssignments'][1]
        original = deepcopy(placement)
        for changes in ({'anchor': 'BRAND_CORNER'}, {'readingPriority': 'PRIMARY'},
                        {'relatedFactIds': ['1']}, {'purpose': ''}):
            placement.clear(); placement.update(original); placement.update(changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError): self.check()

    def test_logo_duplication_and_missing_assignment_are_rejected(self):
        row = self.plan['images'][2]
        row['presentation']['logoAssignments'].append(deepcopy(row['presentation']['logoAssignments'][1]))
        with self.assertRaisesRegex(ValueError, 'one semantic'): self.check()

    def test_cpu_badge_cannot_be_mislabelled_as_oem_identity(self):
        row = self.plan['images'][2]
        row['presentation']['logoAssignments'][1].update(role='OEM', anchor='BRAND_CORNER', relatedFactIds=['1'])
        with self.assertRaisesRegex(ValueError, 'logo kind'): self.check()
        row['presentation']['logoAssignments'] = row['presentation']['logoAssignments'][:1]
        with self.assertRaisesRegex(ValueError, 'one semantic'): self.check()

    def test_choice_page_does_not_become_an_unrelated_component_badge_panel(self):
        row = self.plan['images'][4]
        row['brandAssetIds'].append('intel-original')
        row['claims'].append({'text': 'Synthetic CPU identity', 'factIds': ['3'], 'role': 'SECONDARY', 'reuseReason': 'Test only'})
        row['presentation']['logoAssignments'].append(deepcopy(self.plan['images'][2]['presentation']['logoAssignments'][1]))
        with self.assertRaisesRegex(ValueError, 'PT05'): self.check()

    def test_legacy_read_is_unassessed_but_new_cli_contract_requires_review(self):
        self.plan.pop('businessDesignReview')
        self.assertEqual(b.check(self.plan, self.ledger, 'actual', self.registry)['presentationReview']['state'],
                         'LEGACY_PRESENTATION_NOT_ASSESSED')
        with self.assertRaisesRegex(ValueError, 'reference-adaptation'): self.check()

    def test_new_full_series_build_cannot_omit_presentation_review(self):
        fixture = series_fixture.BusinessSeriesTests(); fixture.setUp()
        self.addCleanup(fixture.temp.cleanup)
        with self.assertRaisesRegex(ValueError, 'reference-adaptation'):
            series_fixture.b.build(fixture.p, 'information.json', 'a'*40, 'Synthetic full series request',
                                   repo=fixture.repo, require_presentation=True)

    def test_missing_storyboard_is_rejected(self):
        self.plan['images'][0]['presentation'].pop('storyboard')
        with self.assertRaisesRegex(ValueError, 'storyboard'): self.check()

    def test_full_front_view_cannot_repeat_under_different_source_ids(self):
        self.plan['images'][2]['presentation']['storyboard']['framing'] = 'FRONT'
        with self.assertRaisesRegex(ValueError, 'front product view'): self.check()

    def test_same_full_product_view_cannot_be_relabelled_as_another_angle(self):
        item = self.plan['images'][2]['presentation']
        item['visualSourceIds'].append('SYNTHETIC-SOURCE-1')
        item['storyboard']['productViewId'] = 'SYNTHETIC-SOURCE-1'
        with self.assertRaisesRegex(ValueError, 'same full-product'): self.check()

    def test_visible_angle_requires_its_actual_declared_source(self):
        self.plan['images'][0]['presentation']['storyboard']['productViewId'] = 'INVENTED-ANGLE'
        with self.assertRaisesRegex(ValueError, 'source-linked'): self.check()

    def test_pt05_is_product_free_and_cannot_have_a_screen(self):
        item = self.plan['images'][4]['presentation']
        item['storyboard'].update(productVisibility='FULL', framing='SIDE', productViewId=item['visualSourceIds'][0])
        with self.assertRaisesRegex(ValueError, 'PT05'): self.check()
        item['storyboard'].update(productVisibility='NONE', framing='NONE', productViewId=None)
        item['screen'].update(shown=True)
        with self.assertRaisesRegex(ValueError, 'product-free'): self.check()

    def test_accessory_page_requires_supply_label_and_verified_package_facts(self):
        item = self.plan['images'][6]['presentation']
        item['screen']['shown'] = False
        item['storyboard'].update(subject='ACCESSORIES', productVisibility='NONE', framing='NONE', productViewId=None)
        with self.assertRaisesRegex(ValueError, 'accessory storyboard'): self.check()
        item['storyboard']['accessoryTreatment'] = {'supplyStatus':'NOT_INCLUDED',
                                                   'customerLabel':'Accessories shown are not included.'}
        self.check()
        item['storyboard']['accessoryTreatment'].update(supplyStatus='INCLUDED', factIds=['1'])
        with self.assertRaisesRegex(ValueError, 'package facts'): self.check()

    def test_version_one_remains_diagnostic_only_for_new_production(self):
        self.plan['businessDesignReview']['schemaVersion'] = 1
        result = b.check(self.plan, self.ledger, 'actual', self.registry)
        self.assertEqual(result['presentationReview']['storyboardReview']['state'], 'LEGACY_STORYBOARD_NOT_ASSESSED')
        with self.assertRaisesRegex(ValueError, 'version 2 storyboard'): self.check()


if __name__ == '__main__': unittest.main()
