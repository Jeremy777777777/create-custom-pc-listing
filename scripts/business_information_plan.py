"""Check a Business Laptop claim/asset plan; this does not accept rendered images."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

import brand_assets


SLOTS = {f"PT{i:02d}.png" for i in range(1, 9)}
LAYOUTS = dict(zip((f'PT{i:02d}.png' for i in range(1, 9)),
    ('PRODUCT_HERO', 'LIFESTYLE_PHOTO', 'CONFIGURATION_COMPOSITE', 'DISPLAY_FOCUS',
     'OPTIONS_COMPARISON', 'INPUT_DETAIL', 'FEATURE_DETAIL', 'PORT_MAP')))
LOGO_ANCHORS = {'OEM': 'BRAND_CORNER', 'CPU': 'PROCESSOR_GROUP', 'GPU': 'GRAPHICS_GROUP',
                'OS': 'SYSTEM_GROUP', 'SOFTWARE': 'SOFTWARE_GROUP'}
SUBJECTS = {'WHOLE_PRODUCT', 'PRODUCT_DETAIL', 'SCREEN_DETAIL', 'USAGE_SCENE',
            'OPTIONS_GUIDE', 'ACCESSORIES'}


def check_storyboard(plan, ledger):
    """Require explicit subject/visibility decisions before rendering new pages."""
    full_views = set(); front_pages = []
    facts = {f['id']: f for f in ledger['facts']}
    for row in plan['images']:
        name = row['file']; item = row['presentation']; shot = item.get('storyboard', {})
        if (shot.get('subject') not in SUBJECTS
                or shot.get('productVisibility') not in {'FULL', 'PARTIAL', 'NONE'}
                or not isinstance(shot.get('productPresenceReason'), str)
                or not shot['productPresenceReason'].strip()):
            raise ValueError(name+': storyboard needs its subject, product visibility and buyer-purpose reason')
        visibility = shot['productVisibility']; framing = shot.get('framing')
        if visibility == 'NONE':
            if framing != 'NONE' or shot.get('productViewId') or item['screen']['shown']:
                raise ValueError(name+': product-free storyboard cannot declare a product view or screen')
        else:
            if (framing not in {'FRONT', 'THREE_QUARTER', 'SIDE', 'REAR', 'DETAIL', 'SCENE'}
                    or not isinstance(shot.get('productViewId'), str)
                    or shot['productViewId'] not in item['visualSourceIds']):
                raise ValueError(name+': visible product needs its actual source-linked framing/view')
            if visibility == 'FULL':
                if shot['productViewId'] in full_views:
                    raise ValueError('Do not repeat the same full-product view across supporting pages')
                full_views.add(shot['productViewId'])
                if framing == 'FRONT': front_pages.append(name)
        if name == 'PT05.png' and (shot['subject'] != 'OPTIONS_GUIDE' or visibility != 'NONE'):
            raise ValueError('PT05 must explain the choices without another laptop image')
        treatment = shot.get('accessoryTreatment')
        if shot['subject'] == 'ACCESSORIES' or treatment is not None:
            if (not isinstance(treatment, dict)
                    or treatment.get('supplyStatus') not in {'INCLUDED', 'NOT_INCLUDED', 'CONTEXT_ONLY'}
                    or not isinstance(treatment.get('customerLabel'), str)
                    or not treatment['customerLabel'].strip()):
                raise ValueError(name+': accessory storyboard must state supply status and customer label')
            if treatment['supplyStatus'] == 'INCLUDED':
                ids = treatment.get('factIds', [])
                claims = {key for claim in row['claims'] for key in claim['factIds']}
                if not ids or not set(ids) <= claims or any(
                        key not in facts or facts[key].get('status') != 'VERIFIED'
                        or not re.search(r'Included|Accessor|Bundl|Package Contents',
                                         str(facts[key].get('attribute', '')), re.I) for key in ids):
                    raise ValueError(name+': included accessories need verified page-linked package facts')
    if len(front_pages) > 1:
        raise ValueError('Use a full front product view at most once across PT01-PT08')
    return {'state': 'STORYBOARD_DECLARATIONS_CHECKED', 'fullFrontSupportingPages': front_pages,
            'actualSourceAngleAndSequenceReview': 'REQUIRED', 'visualQa': 'NOT_ASSESSED'}


def check_presentation(plan, ledger, registry, required=False):
    """Check reference-adaptation declarations, not actual visual quality or truth."""
    review = plan.get('businessDesignReview')
    if review is None:
        if required: raise ValueError('New Business production requires the reference-adaptation design review')
        return {'state': 'LEGACY_PRESENTATION_NOT_ASSESSED'}
    if (not isinstance(review, dict) or review.get('schemaVersion') not in (1, 2)
            or not all(isinstance(review.get(k), str) and review[k].strip()
                       for k in ('referenceUrl', 'observedDate', 'lessonAndAdaptation'))):
        raise ValueError('Business design review needs the observed reference and actual adaptation')
    if required and review['schemaVersion'] != 2:
        raise ValueError('New Business production requires the version 2 storyboard review')
    from datetime import date
    observed = date.fromisoformat(review['observedDate'])
    if observed.isoformat() != review['observedDate'] or observed > date.today():
        raise ValueError('Invalid reference observation date')
    facts = {f['id']: f for f in ledger['facts']}
    assets = {a['id']: a for a in registry['assets']}
    screens = []
    for row in plan['images']:
        name = row['file']; item = row.get('presentation', {})
        if item.get('layoutFamily') != LAYOUTS[name]:
            raise ValueError(name+': use its distinct buyer-question layout family')
        if (not isinstance(item.get('visualSourceIds'), list) or not item['visualSourceIds']
                or not all(isinstance(v, str) and v.strip() for v in item['visualSourceIds'])
                or not isinstance(item.get('proofPurpose'), str) or not item['proofPurpose'].strip()):
            raise ValueError(name+': actual visual sources and their explanatory purpose required')
        screen = item.get('screen', {})
        if type(screen.get('shown')) is not bool:
            raise ValueError(name+': explicit screen visibility required')
        if screen['shown']:
            if not all(isinstance(screen.get(k), str) and screen[k].strip() for k in ('contentId', 'purpose')):
                raise ValueError(name+': screen content must serve its page')
            if screen['contentId'] in screens and not screen.get('reuseReason', '').strip():
                raise ValueError(name+': repeated screen artwork needs a distinct buyer-purpose reason')
            screens.append(screen['contentId'])
        if name == 'PT02.png' and not item.get('sceneAction', '').strip():
            raise ValueError('PT02 needs a coherent person/task/product use scene')
        placements = item.get('logoAssignments', [])
        ids = [p.get('assetId') for p in placements]
        if len(ids) != len(set(ids)) or set(ids) != set(row.get('brandAssetIds', [])):
            raise ValueError(name+': every selected logo needs one semantic placement')
        claim_ids = {key for c in row['claims'] for key in c['factIds']}
        for placement in placements:
            role = placement.get('role')
            if (role not in LOGO_ANCHORS or placement.get('anchor') != LOGO_ANCHORS[role]
                    or placement.get('readingPriority') != 'SECONDARY'
                    or not placement.get('purpose', '').strip()):
                raise ValueError(name+': logo needs a subordinate, meaning-related anchor')
            if name == 'PT05.png' and role != 'OEM':
                raise ValueError('PT05 is a capacity-choice page, not a CPU/GPU/OS logo panel')
            related = placement.get('relatedFactIds', [])
            if not related or any(k not in facts or facts[k].get('status') != 'VERIFIED' for k in related):
                raise ValueError(name+': logo must explain verified applicable facts')
            if role != 'OEM' and not set(related) <= claim_ids:
                raise ValueError(name+': logo facts must belong to its page content')
            asset = assets.get(placement['assetId'], {})
            kinds = {'OEM': {'OEM_BRAND', 'HARDWARE_BRAND'},
                     'CPU': {'CPU_FAMILY_BADGE', 'HARDWARE_BRAND'},
                     'GPU': {'GPU_FAMILY_BADGE', 'GPU_BRAND', 'HARDWARE_BRAND'},
                     'OS': {'OS_IDENTITY'}, 'SOFTWARE': {'SOFTWARE_IDENTITY'}}
            if asset.get('kind') not in kinds[role]:
                raise ValueError(name+': original logo kind does not match its semantic role')
            fields = ' '.join(str(facts[k].get('attribute', '')) for k in related)
            pattern = {'OEM': r'Manufacturer|Brand', 'CPU': r'CPU|Processor',
                       'GPU': r'GPU|Graphics', 'OS': r'Operating System',
                       'SOFTWARE': r'Software|License|Entitlement'}[role]
            if not re.search(pattern, fields, re.I):
                raise ValueError(name+': logo role does not match the referenced hardware/software fact')
    if len(screens) >= 3 and len(set(screens)) == 1:
        raise ValueError('A full Business series cannot repeat one screen composition on every visible-screen page')
    storyboard = (check_storyboard(plan, ledger) if review['schemaVersion'] == 2
                  else {'state': 'LEGACY_STORYBOARD_NOT_ASSESSED'})
    return {'state': 'BUSINESS_PRESENTATION_DECLARATIONS_CHECKED', 'storyboardReview': storyboard,
            'actualRenderedLayoutReview': 'REQUIRED', 'visualQa': 'NOT_ASSESSED'}


def check(plan, ledger, ledger_sha256, registry, require_presentation=False):
    from customer_visible_content import validate_image_plan_copy
    validate_image_plan_copy(plan)
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
    presentation = check_presentation(plan, ledger, registry, require_presentation)
    return {"state": "PLAN_DECLARATIONS_CHECKED", "productId": plan["productId"],
            "presentationReview": presentation,
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
                           hashlib.sha256(raw).hexdigest(), registry, require_presentation=True), indent=2))


if __name__ == "__main__":
    main()
