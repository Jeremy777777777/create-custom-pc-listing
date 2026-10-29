"""Check a Business Laptop claim/asset plan; this does not accept rendered images."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

import brand_assets


SLOTS = {f"PT{i:02d}.png" for i in range(1, 9)}


def check(plan, ledger, ledger_sha256, registry):
    if plan.get("productId") != ledger.get("productId") or plan.get("configurationId") != ledger.get("configurationId"):
        raise ValueError("Plan and ledger identity/configuration differ")
    if plan.get("ledgerSha256") != ledger_sha256:
        raise ValueError("Plan does not bind the current ledger bytes")
    rows = plan.get("images", [])
    if len(rows) != 8 or {r.get("file") for r in rows} != SLOTS:
        raise ValueError("Plan must cover PT01-PT08 exactly once")
    if {r["file"] for r in rows if r.get("fullConfigurationOverview")} != {"PT03.png"}:
        raise ValueError("PT03 must be the only complete configuration overview")
    facts = {f["id"]: f for f in ledger["facts"]}
    assets = {a["id"]: a for a in registry["assets"]}
    owners = {}
    for row in rows:
        file = row["file"]
        for key in ("buyerQuestion", "headline", "primaryTheme", "visualProof"):
            if not isinstance(row.get(key), str) or not row[key].strip():
                raise ValueError(f"{file}: missing {key}")
        claims = row.get("claims", [])
        if not claims:
            raise ValueError(f"{file}: no evidence-backed content")
        for claim in claims:
            if not claim.get("text") or re.search(r"[\u3400-\u9fff]", claim["text"]):
                raise ValueError(f"{file}: missing/non-English customer copy")
            if not claim.get("factIds"):
                raise ValueError(f"{file}: claim has no canonical fact references")
            role = claim.get("role", "PRIMARY")
            if role not in {"PRIMARY", "SECONDARY"}:
                raise ValueError(f"{file}: invalid claim role")
            if role == "SECONDARY" and not claim.get("reuseReason", "").strip():
                raise ValueError(f"{file}: secondary reuse needs its buyer-purpose explanation")
            for key in claim["factIds"]:
                f = facts.get(key)
                if not f or f.get("status") != "VERIFIED" or f.get("final_value") in (None, ""):
                    raise ValueError(f"{file}: unresolved/absent fact {key}")
                scope = f.get("fact_scope")
                if scope not in {"SOLD_BASE", "CURRENT_UNIT"} and not f.get("applies_to_sold_configuration"):
                    treatment = claim.get("capabilityApplicability", {})
                    links = treatment.get("linkedSoldFactIds", [])
                    linked = all(facts.get(link, {}).get("status") == "VERIFIED" and
                                 facts[link].get("fact_scope") in {"SOLD_BASE", "CURRENT_UNIT"} for link in links)
                    if not (scope == "PLATFORM_CAPABILITY" and key in treatment.get("capabilityFactIds", []) and
                            links and linked and treatment.get("basis", "").strip() and
                            treatment.get("qualification") == "CAPABILITY_NOT_GUARANTEED_RESULT"):
                        raise ValueError(f"{file}: unlinked factory/family fact {key}")
                if role == "PRIMARY":
                    if key in owners and owners[key] != file:
                        raise ValueError(f"{file}: repeated primary explanation for {key}; declare justified secondary reuse")
                    owners[key] = file
        for key in row.get("brandAssetIds", []):
            if key not in assets or not brand_assets.eligible(assets[key], plan.get("brandContext", {})):
                raise ValueError(f"{file}: incompatible/absent brand asset {key}")
            if file == "PT01.png" and assets[key].get("kind") == "OS_IDENTITY":
                raise ValueError("PT01 cannot repeat Windows treatment")
    return {"state": "PLAN_DECLARATIONS_CHECKED", "productId": plan["productId"],
            "imageCount": len(rows), "actualCopyFactReview": "REQUIRED", "visualQa": "NOT_ASSESSED",
            "styleApproval": plan.get("styleApprovalStatus", "PENDING"), "productionApprovalGranted": False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--plan", required=True)
    p.add_argument("--ledger", required=True)
    p.add_argument("--repo", default=str(Path(__file__).resolve().parents[1]))
    a = p.parse_args()
    raw = Path(a.ledger).read_bytes()
    registry = brand_assets.read(Path(a.repo) / brand_assets.REGISTRY)
    brand_assets.verify(a.repo, registry)
    print(json.dumps(check(brand_assets.read(a.plan), json.loads(raw.decode("utf-8-sig")),
                           hashlib.sha256(raw).hexdigest(), registry), indent=2))


if __name__ == "__main__":
    main()
