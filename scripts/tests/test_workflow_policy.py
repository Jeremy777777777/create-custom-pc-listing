"""Guard the user's accepted policy and prevent historical routing regressions."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WARRANTY = ('The original [OEM brand] manufacturer warranty remains valid on factory components. '
            'MegaPC provides a 6-month limited warranty on upgraded RAM and SSD components, '
            'with a 12-month warranty extension available.')

class WorkflowPolicyTests(unittest.TestCase):
    def test_current_policy_and_base_scope(self):
        policy = (ROOT/'references/confirmed-catalog-defaults.md').read_text()
        skill = (ROOT/'SKILL.md').read_text()
        self.assertIn('2026-10-02', policy)
        self.assertIn(WARRANTY, policy)
        self.assertIn(WARRANTY, skill)
        self.assertIn('MegaPC Custom', skill)
        self.assertIn('base sold configuration only', skill)
        self.assertIn('2000×2000', skill)
        self.assertIn('PARTIAL_UPDATE', skill)

    def test_no_discoverable_skill_in_history(self):
        self.assertFalse(list((ROOT/'history').rglob('SKILL.md')))
        for file in list((ROOT/'references').glob('*.md')) + [ROOT/'SKILL.md']:
            content = file.read_text()
            self.assertNotRegex(content, r'\]\([^)]*history/')

    def test_markdown_local_links_resolve(self):
        files = list((ROOT/'references').glob('*.md')) + [ROOT/'SKILL.md', ROOT/'README.md', ROOT/'product generated photo/image-manifest-template.md']
        for file in files:
            for target in re.findall(r'\]\(([^)]+)\)', file.read_text()):
                if '://' in target or target.startswith('#'):
                    continue
                path = target.split('#')[0].replace('%20', ' ')
                self.assertTrue((file.parent/path).exists(), f'{file}: {target}')

    def test_quarantined_outputs_have_no_current_full_pass(self):
        for folder in (ROOT/'product generated photo').glob('VL-*'):
            status_path = folder/'delivery-status.json'
            if not status_path.exists():
                continue
            status = json.loads(status_path.read_text())
            if status.get('galleryState') != 'LEGACY_QUARANTINED':
                continue
            self.assertFalse(status.get('currentQaPass', False))
            self.assertNotEqual(status.get('deliveryState'), 'GITHUB_DELIVERY_VERIFIED')
            self.assertFalse((folder/'final-image-qa.json').exists())
            self.assertFalse((folder/'logo-qa.json').exists())

if __name__ == '__main__':
    unittest.main()
