"""Synthetic universal choice-page briefs; no real product research or image QA."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import image_customization_plan as image_plan
import test_customization_policy as fixtures


class ImageCustomizationPlanTests(unittest.TestCase):
    def inputs(self, root, replaceable=True, memory_type='DDR5'):
        ledger, product, _, _ = fixtures.CustomizationTests().fixture(root, replaceable, memory_type)
        return product, ledger, image_plan.digest(json.dumps(product).encode()), image_plan.digest(json.dumps(ledger).encode())

    def test_replaceable_ram_generations_and_all_ssd_tiers(self):
        for memory_type in ('DDR4', 'DDR5'):
            with self.subTest(memory_type=memory_type), tempfile.TemporaryDirectory() as tmp:
                inputs = self.inputs(Path(tmp), True, memory_type)
                plan = image_plan.build(*inputs)
                result = image_plan.check(plan, *inputs)
                self.assertEqual([r['capacity'] for r in plan['ram']['tiers']], ['8GB', '16GB', '32GB', '64GB'])
                self.assertEqual([r['capacity'] for r in plan['ssd']['tiers']], ['512GB', '1TB', '2TB', '4TB'])
                self.assertTrue(all(r['typicalUse'] for group in ('ram', 'ssd') for r in plan[group]['tiers']))
                self.assertIn(memory_type, plan['ram']['label'])
                self.assertEqual(result['ramOptionCount'], 4)
                self.assertEqual(plan['file'], 'PT05.png')
                self.assertFalse(plan['fullConfigurationOverview'])
                self.assertEqual(plan['claimScope'], 'SELLER_OPTIONS_NOT_INSTALLED_CONFIGURATION')

    def test_fixed_lpddr_uses_actual_capacity_without_ram_options(self):
        for memory_type in ('LPDDR4X', 'LPDDR5', 'LPDDR5X'):
            with self.subTest(memory_type=memory_type), tempfile.TemporaryDirectory() as tmp:
                inputs = self.inputs(Path(tmp), False, memory_type)
                plan = image_plan.build(*inputs)
                self.assertEqual(plan['ram']['tiers'], [])
                self.assertEqual(plan['ram']['fixedCapacityGB'], 16)
                self.assertEqual(plan['ram']['label'], '16GB '+memory_type+' RAM (Fixed)')
                self.assertIn('RAM is fixed', plan['selectionNote'])
                self.assertEqual(image_plan.check(plan, *inputs)['ssdOptionCount'], 4)

    def test_existing_smaller_platform_maximum_does_not_remove_64gb_choice(self):
        with tempfile.TemporaryDirectory() as tmp:
            product, ledger, psha, _ = self.inputs(Path(tmp))
            maximum = next(f for f in ledger['facts'] if f['attribute'] == 'RAM Memory Maximum Size')
            maximum.update(status='VERIFIED', final_value=32, fact_scope='PLATFORM_CAPABILITY')
            plan = image_plan.build(product, ledger, psha, image_plan.digest(json.dumps(ledger).encode()))
            self.assertEqual(plan['ram']['tiers'][-1]['capacity'], '64GB')
            self.assertEqual(maximum['final_value'], 32)

    def test_unknown_replaceability_or_type_never_produces_guessed_options(self):
        with tempfile.TemporaryDirectory() as tmp:
            inputs = self.inputs(Path(tmp))
            for changes in ({'status': 'TBD'}, {'status': 'CONFLICT'}, {'replaceable': None}, {'memoryType': 'DDR'}, {'memoryTypeSource': ''}):
                changed = copy.deepcopy(inputs)
                ram = next(f for f in changed[1]['facts'] if f['attribute'] == 'RAM Memory Installed')
                ram['evidence']['customization_ram'].update(changes)
                with self.subTest(changes=changes), self.assertRaises(ValueError):
                    image_plan.build(*changed)

    def test_tier_slot_scope_and_approval_tampering_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            inputs = self.inputs(Path(tmp))
            original = image_plan.build(*inputs)
            for key, value in (('file', 'PT03.png'), ('fullConfigurationOverview', True),
                               ('productionApprovalGranted', True), ('visualQa', 'PASS'),
                               ('claimScope', 'INSTALLED')):
                plan = copy.deepcopy(original)
                plan[key] = value
                with self.subTest(key=key), self.assertRaises(ValueError):
                    image_plan.check(plan, *inputs)
            for group in ('ram', 'ssd'):
                plan = copy.deepcopy(original)
                plan[group]['tiers'][-1]['capacity'] = '128GB' if group == 'ram' else '8TB'
                with self.subTest(group=group), self.assertRaises(ValueError):
                    image_plan.check(plan, *inputs)

    def test_stale_hash_identity_and_type_bindings_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            inputs = self.inputs(Path(tmp))
            plan = image_plan.build(*inputs)
            for index in (2, 3):
                changed = list(inputs)
                changed[index] = '0'*64
                with self.subTest(index=index), self.assertRaises(ValueError):
                    image_plan.check(plan, *changed)
            changed = copy.deepcopy(inputs)
            changed[0]['identity']['internalId'] = 'OTHER-PC'
            with self.assertRaises(ValueError): image_plan.build(*changed)
            changed = copy.deepcopy(inputs)
            next(f for f in changed[1]['facts'] if f['attribute'] == 'RAM Memory Installed')['evidence']['customization_ram']['memoryType'] = 'DDR4'
            with self.assertRaises(ValueError): image_plan.check(plan, *changed)

    def test_own_brand_route_does_not_silently_gain_custom_options(self):
        with tempfile.TemporaryDirectory() as tmp:
            inputs = self.inputs(Path(tmp))
            inputs[0].update(listingMode='MEGAPC_OWN_BRAND', ownBrandAuthority='Synthetic own-brand confirmation')
            inputs[0]['identity']['oemBrand'] = 'MegaPC'
            with self.assertRaisesRegex(ValueError, 'Own-brand'):
                image_plan.build(*inputs)

    def test_real_cli_build_check_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            product, ledger, _, _ = self.inputs(root)
            pfile, lfile = root/'product-facts.json', root/'research-ledger.json'
            pfile.write_text(json.dumps(product), encoding='utf8')
            lfile.write_text(json.dumps(ledger), encoding='utf8')
            plan = root/'customization-image-plan.json'
            script = Path(image_plan.__file__)
            arguments = ['--product-facts', str(pfile), '--ledger', str(lfile), '--plan', str(plan)]
            for command in ('build', 'check'):
                result = subprocess.run([sys.executable, str(script), command, *arguments], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                report = json.loads(result.stdout)
                self.assertFalse(report['productionApprovalGranted'])
                self.assertEqual(report['visualQa'], 'NOT_ASSESSED')
            before = plan.read_bytes()
            result = subprocess.run([sys.executable, str(script), 'build', *arguments], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(plan.read_bytes(), before)
            lfile.write_bytes(lfile.read_bytes()+b'\n')
            result = subprocess.run([sys.executable, str(script), 'check', *arguments], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__': unittest.main()
