from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import business_information_plan as b


class BusinessPlanTests(unittest.TestCase):
    def setUp(self):
        self.ledger = {"productId": "VL-TEST", "configurationId": "base", "facts": [
            {"id": str(i), "status": "VERIFIED", "final_value": i, "fact_scope": "SOLD_BASE"} for i in range(1, 9)]}
        self.plan = {"productId": "VL-TEST", "configurationId": "base", "ledgerSha256": "actual", "images": [
            {"file": f"PT{i:02d}.png", "buyerQuestion": "What matters?", "headline": "Useful proof", "primaryTheme": str(i),
             "visualProof": "Exact source detail", "fullConfigurationOverview": i == 3,
             "claims": [{"text": "Supported fact", "factIds": [str(i)]}]} for i in range(1, 9)]}
        self.registry = {"assets": []}

    def test_useful_secondary_reuse_allowed_without_low_overlap_score(self):
        self.plan["images"][4]["claims"].append({"text": "Explain the installed capacity", "factIds": ["3"],
            "role": "SECONDARY", "reuseReason": "Explain how the capacity supports the task"})
        out = b.check(self.plan, self.ledger, "actual", self.registry)
        self.assertFalse(out["productionApprovalGranted"])
        self.assertEqual(out["visualQa"], "NOT_ASSESSED")

    def test_unlinked_factory_fact_rejected(self):
        self.ledger["facts"][0]["fact_scope"] = "FACTORY"
        with self.assertRaises(ValueError):
            b.check(self.plan, self.ledger, "actual", self.registry)

    def test_reviewed_component_capability_keeps_qualification(self):
        self.ledger["facts"][0]["fact_scope"] = "PLATFORM_CAPABILITY"
        claim = self.plan["images"][0]["claims"][0]
        claim["capabilityApplicability"] = {"capabilityFactIds": ["1"], "linkedSoldFactIds": ["3"],
            "basis": "Reviewed exact installed component identity and official maximum capability",
            "qualification": "CAPABILITY_NOT_GUARANTEED_RESULT"}
        self.assertEqual(b.check(self.plan, self.ledger, "actual", self.registry)["state"], "PLAN_DECLARATIONS_CHECKED")
        claim["capabilityApplicability"]["linkedSoldFactIds"] = []
        with self.assertRaises(ValueError):
            b.check(self.plan, self.ledger, "actual", self.registry)

    def test_unresolved_and_changed_ledger_rejected(self):
        self.ledger["facts"][0]["status"] = "CONFLICT"
        with self.assertRaises(ValueError):
            b.check(self.plan, self.ledger, "actual", self.registry)
        with self.assertRaises(ValueError):
            b.check(self.plan, self.ledger, "changed", self.registry)

    def test_repeated_complete_configuration_and_office_without_entitlement_rejected(self):
        self.plan["images"][4]["fullConfigurationOverview"] = True
        with self.assertRaises(ValueError):
            b.check(self.plan, self.ledger, "actual", self.registry)
        self.plan["images"][4]["fullConfigurationOverview"] = False
        self.registry["assets"].append({"id": "word", "kind": "SOFTWARE_IDENTITY", "match": {"software": "Word", "entitlementRequired": True}})
        self.plan["images"][1]["brandAssetIds"] = ["word"]
        with self.assertRaises(ValueError):
            b.check(self.plan, self.ledger, "actual", self.registry)


if __name__ == "__main__":
    unittest.main()
