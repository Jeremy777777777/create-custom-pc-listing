import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import brand_assets as b


class BrandAssetsTests(unittest.TestCase):
    def test_tier_and_missing_context_do_not_match(self):
        a = {"match": {"cpuBrand": "Intel", "cpuFamily": "Core Ultra", "cpuTier": "7"}}
        self.assertTrue(b.eligible(a, {"cpuBrand": "Intel", "cpuFamily": "Core Ultra", "cpuTier": "7"}))
        self.assertFalse(b.eligible(a, {"cpuBrand": "Intel", "cpuFamily": "Core", "cpuTier": "7"}))
        self.assertFalse(b.eligible(a, {"cpuBrand": "Intel"}))

    def test_office_permission_does_not_supply_entitlement(self):
        a = {"match": {"software": "Word", "entitlementRequired": True}}
        self.assertFalse(b.eligible(a, {"brandAuthorization": True}))
        self.assertTrue(b.eligible(a, {"verifiedSoftwareEntitlements": ["Word"]}))
        self.assertFalse(b.eligible(a, {"verifiedSoftwareEntitlements": ["Excel"]}))

    def test_pro_edition_does_not_match_home(self):
        a = {"match": {"osEdition": "Windows 11 Pro"}}
        self.assertFalse(b.eligible(a, {"osEdition": "Windows 11 Home"}))
        self.assertTrue(b.eligible(a, {"osEdition": "Windows 11 Pro"}))

    def test_corrupted_master_and_escaping_path_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "master.svg"
            p.write_bytes(b"original")
            a = {"id": "a", "path": "master.svg", "sha256": hashlib.sha256(b"original").hexdigest(),
                 "byteLength": 8, "sourcePage": "https://example.com/media", "url": "https://example.com/master.svg",
                 "authorization": "USER_CONFIRMED", "identity": "test"}
            self.assertEqual(b.verify(td, {"assets": [a]}), 1)
            p.write_bytes(b"modified")
            with self.assertRaises(ValueError):
                b.verify(td, {"assets": [a]})
            a["path"] = "../outside.svg"
            with self.assertRaises(ValueError):
                b.verify(td, {"assets": [a]})

    def test_signed_source_not_shareable(self):
        with tempfile.TemporaryDirectory() as td:
            (Path(td) / "a").write_bytes(b"a")
            a = {"id": "a", "path": "a", "sha256": hashlib.sha256(b"a").hexdigest(), "byteLength": 1,
                 "sourcePage": "https://example.com", "url": "https://example.com/a?sig=private",
                 "authorization": "USER_CONFIRMED", "identity": "test"}
            with self.assertRaises(ValueError):
                b.verify(td, {"assets": [a]})


if __name__ == "__main__":
    unittest.main()
