"""Check Gaming v2 planning inputs, never aesthetic quality or product acceptance."""
import argparse
import json
from pathlib import Path
from customer_visible_content import validate_customer_text, validate_image_plan_copy

PROFILE = 'gaming-visual-explanation-v2'
SLOTS = {f'PT{i:02}.png' for i in range(1, 9)}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def check(plan, registry, require_oem=False, repo=None):
    validate_image_plan_copy(plan)
    if plan.get('designSeries') != 'GAMING' or plan.get('family') != 'G22':
        raise ValueError('This checker applies only to GAMING G22 PT plans; other series use their own rules')
    if plan.get('methodProfile') != PROFILE or registry.get('methodProfile') != PROFILE:
        raise ValueError('Gaming visual-explanation methodProfile must match the reference registry')
    selected = plan.get('selectedSlots', [])
    if not selected or len(set(selected)) != len(selected) or not set(selected) <= SLOTS:
        raise ValueError('Select unique PT01-PT08 filenames; MAIN has separate planning')
    if not nonempty(plan.get('productId')) or not nonempty(plan.get('configurationId')):
        raise ValueError('Actual productId and configurationId required')
    known = {r['driveFileId']: r['sha256'] for r in registry['references']}
    rows = plan.get('images', [])
    for slot in selected:
        matching = [row for row in rows if row.get('file') == slot]
        if len(matching) != 1:
            raise ValueError(slot + ': exactly one page plan required')
        row = matching[0]
        visual = row.get('visualExplanation', {})
        placement = visual.get('oemLogoPlacement')
        if require_oem or plan.get('visualPlanVersion', 1) >= 2:
            import hashlib
            import re
            if (not isinstance(placement, dict)
                    or not all(nonempty(placement.get(k)) for k in
                               ('assetPath', 'assetSha256', 'anchor', 'purpose'))
                    or placement['anchor'] not in {'BRAND_CORNER', 'PRODUCT_IDENTITY', 'FEATURE_HEADER'}
                    or not re.fullmatch('[0-9a-f]{64}', placement['assetSha256'])
                    or placement.get('readingPriority') != 'SECONDARY'
                    or not isinstance(placement.get('protectedElements'), list)
                    or not placement['protectedElements']
                    or not all(nonempty(v) for v in placement['protectedElements'])):
                raise ValueError(slot + ': original OEM semantic placement required')
            asset = Path(placement['assetPath'])
            if (asset.is_absolute() or '..' in asset.parts or '\\' in placement['assetPath']
                    or ':' in placement['assetPath']):
                raise ValueError(slot + ': OEM asset must use a safe relative path')
            if repo is not None:
                asset = (Path(repo) / asset).resolve()
                if not asset.is_relative_to(Path(repo).resolve()) or not asset.is_file():
                    raise ValueError(slot + ': original OEM asset missing/outside repository')
                if hashlib.sha256(asset.read_bytes()).hexdigest() != placement['assetSha256']:
                    raise ValueError(slot + ': original OEM asset hash mismatch')
        for field in ('subject', 'buyerUnderstanding', 'mainVisual', 'composition'):
            if not nonempty(visual.get(field)):
                raise ValueError(slot + ': missing visualExplanation.' + field)
        for field in ('actualProductSourceIds', 'exactCopy', 'avoid', 'selectedCompositionInvariants'):
            items = visual.get(field)
            if not isinstance(items, list) or not items or not all(nonempty(x) for x in items):
                raise ValueError(slot + ': nonempty ' + field + ' required')
        refs = visual.get('referenceImageIds')
        hashes = visual.get('referenceImageSha256', {})
        if not isinstance(refs, list) or not refs or len(set(refs)) != len(refs):
            raise ValueError(slot + ': actual selected reference IDs required')
        for ref in refs:
            if ref not in known or hashes.get(ref) != known[ref]:
                raise ValueError(slot + ': reference ID/hash does not match approved registry')
        for copy in visual['exactCopy']:
            validate_customer_text(copy)
        mappings = visual.get('labelToVisualMap')
        if not isinstance(mappings, list) or not mappings:
            raise ValueError(slot + ': label-to-visual mapping required')
        for mapping in mappings:
            if not isinstance(mapping, dict) or not all(nonempty(mapping.get(k)) for k in ('label', 'visual')):
                raise ValueError(slot + ': each mapping needs label and visual')
            validate_customer_text(mapping['label'])
        if row.get('primaryTheme') == 'Product hero and buying reasons' or row.get('visualProof') == 'PRODUCT_HERO':
            raise ValueError(slot + ': replace the shared Mini PC product-hero seed with Gaming subject-led planning')
    return {'state': 'GAMING_VISUAL_PLAN_INPUTS_CHECKED', 'methodProfile': PROFILE,
            'oemPlacement': 'ORIGINAL_SEMANTIC_PLACEMENT_CHECKED' if require_oem or plan.get('visualPlanVersion', 1) >= 2
                            else 'LEGACY_OEM_PLACEMENT_NOT_ASSESSED',
            'selectedSlots': selected, 'visualQuality': 'REQUIRES_ACTUAL_IMAGE_REVIEW',
            'referenceBytes': 'RETRIEVE_AND_HASH_CHECK_BEFORE_GENERATION',
            'productFacts': 'SEPARATE_APPLICABLE_EVIDENCE_REQUIRED', 'userApproval': 'NOT_GRANTED_BY_THIS_CHECK'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', required=True)
    parser.add_argument('--repo', type=Path, required=True)
    args = parser.parse_args()
    plan = json.loads(Path(args.plan).read_text(encoding='utf-8-sig'))
    registry = json.loads((args.repo / 'assets/gaming-visual-reference-registry.json').read_text(encoding='utf-8-sig'))
    try:
        print(json.dumps(check(plan, registry, require_oem=True, repo=args.repo), indent=2))
    except (ValueError, KeyError, TypeError) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
