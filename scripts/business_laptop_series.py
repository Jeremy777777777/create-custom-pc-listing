"""Plan/check complete Business Laptop coverage; no rendering, approval or QA grant."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

import brand_assets
import business_information_plan
from gallery_engine import NAMES
from product_identity import product_id

ROOT = Path(__file__).resolve().parents[1]
PROFILE = 'assets/business-laptop-series-profile.json'
INPUTS = ('product-facts.json', 'research-ledger.json', 'style-lock.json')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def contained(root, relative):
    if not isinstance(relative, str) or not relative or '\\' in relative or ':' in relative:
        raise ValueError('Product-relative input path required')
    value = Path(relative)
    result = (Path(root) / value).resolve()
    if value.is_absolute() or '..' in value.parts or not result.is_relative_to(Path(root).resolve()):
        raise ValueError('Input path leaves product directory')
    return result


def inputs(product, information_plan, repo, require_presentation=False):
    p, repo = Path(product), Path(repo)
    path = contained(p, information_plan)
    facts, ledger, style = (brand_assets.read(p / name) for name in INPUTS)
    if product_id(facts) != p.name or ledger.get('productId') != p.name:
        raise ValueError('Product identity differs from directory')
    configuration = facts.get('selectedBaseConfiguration', {}).get('id')
    if configuration and configuration != ledger.get('configurationId'):
        raise ValueError('Product cache and sold configuration differ')
    info = brand_assets.read(path)
    registry = brand_assets.read(repo / brand_assets.REGISTRY)
    brand_assets.verify(repo, registry)
    claim_check = business_information_plan.check(info, ledger, digest(p/'research-ledger.json'), registry, require_presentation)
    profile = brand_assets.read(repo / PROFILE)
    rows = profile.get('slots', [])
    if profile.get('designSeries') != 'BUSINESS_LAPTOP' or len(rows) != 11 or {r.get('file') for r in rows} != set(NAMES):
        raise ValueError('Business profile must contain the eleven canonical slots')
    bound = {name: digest(p/name) for name in INPUTS}
    bound[information_plan] = digest(path)
    return ledger, style, info, profile, bound, claim_check


def build(product, information_plan, workflow_sha, request_reference, preserve=(), repo=ROOT, require_presentation=False):
    p = Path(product)
    if not re.fullmatch('[0-9a-f]{40}', workflow_sha) or not request_reference.strip():
        raise ValueError('Exact workflow commit and actual request reference required')
    preserve = list(preserve)
    if len(set(preserve)) != len(preserve) or not set(preserve) <= set(NAMES):
        raise ValueError('Preserve only unique canonical image names')
    ledger, style, info, profile, bound, _ = inputs(p, information_plan, repo, require_presentation)
    # This is a planning inventory. Production still uses the existing frozen contract.
    return {'schemaVersion': 1, 'artifactRole': 'BUSINESS_LAPTOP_SERIES_PLAN',
            'productId': p.name, 'configurationId': ledger['configurationId'],
            'workflowSha': workflow_sha, 'requestReference': request_reference,
            'scope': 'FULL_SERIES', 'informationPlanPath': information_plan,
            'presentationContractVersion': 2 if require_presentation else None,
            'profilePath': PROFILE, 'profileSha256': digest(Path(repo)/PROFILE),
            'inputSha256': bound,
            'slots': [{'file': n, 'action': 'PRESERVE' if n in preserve else 'PRODUCE',
                       **({'preservedSha256': digest(p/n)} if n in preserve else {})} for n in NAMES],
            'styleApprovalStatus': style.get('style_approval_status', style.get('status', 'PENDING')),
            'visualQa': 'NOT_ASSESSED', 'productionApprovalGranted': False,
            'nextStep': 'Freeze authorized production scope; apply the profile and claim plan, render/review, then use existing gallery and Drive gates.'}


def check(plan, product, repo=ROOT):
    p = Path(product)
    if plan.get('schemaVersion') != 1 or plan.get('artifactRole') != 'BUSINESS_LAPTOP_SERIES_PLAN' or plan.get('scope') != 'FULL_SERIES':
        raise ValueError('Complete Business Laptop plan required')
    if not re.fullmatch('[0-9a-f]{40}', plan.get('workflowSha', '')) or not plan.get('requestReference', '').strip():
        raise ValueError('Missing workflow/request binding')
    ledger, style, _, _, bound, claim_check = inputs(p, plan['informationPlanPath'], repo, plan.get('presentationContractVersion') == 2)
    if plan.get('productId') != p.name or plan.get('configurationId') != ledger['configurationId']:
        raise ValueError('Series identity/configuration differs')
    if plan.get('profilePath') != PROFILE or plan.get('profileSha256') != digest(Path(repo)/PROFILE) or plan.get('inputSha256') != bound:
        raise ValueError('Series inputs/profile changed; reconcile the plan')
    if plan.get('styleApprovalStatus') != style.get('style_approval_status', style.get('status', 'PENDING')):
        raise ValueError('Style approval echo differs from actual input')
    slots = plan.get('slots', [])
    if len(slots) != 11 or {r.get('file') for r in slots} != set(NAMES):
        raise ValueError('Full series must account for all eleven files exactly once')
    preserved = []
    for row in slots:
        name = row['file']
        if row.get('action') not in {'PRESERVE', 'PRODUCE'}:
            raise ValueError('Explicit produce/preserve action required')
        if row['action'] == 'PRESERVE':
            if not re.fullmatch('[0-9a-f]{64}', row.get('preservedSha256', '')) or digest(p/name) != row['preservedSha256']:
                raise ValueError('Approved preserved bytes changed: '+name)
            preserved.append(name)
        elif row.get('preservedSha256') is not None:
            raise ValueError('Produce action cannot claim preserved bytes')
    if plan.get('productionApprovalGranted') is not False or plan.get('visualQa') != 'NOT_ASSESSED':
        raise ValueError('Planning must not assert production approval or visual QA')
    return {'state': 'BUSINESS_SERIES_PLAN_CHECKED', 'productId': p.name,
            'accountedSlots': 11, 'produceCount': 11-len(preserved), 'preservedSlots': preserved,
            'claimPlan': claim_check, 'productionApprovalGranted': False,
            'visualQa': 'NOT_ASSESSED', 'publicationStatus': 'NOT_ASSESSED'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    make = sub.add_parser('plan')
    make.add_argument('--information-plan', required=True, help='Path relative to product directory')
    make.add_argument('--request-reference', required=True)
    make.add_argument('--preserve', action='append', default=[])
    make.add_argument('--output', required=True, help='New run-record path outside product directory')
    validate = sub.add_parser('check')
    validate.add_argument('--plan', required=True)
    for cmd in (make, validate):
        cmd.add_argument('--product', required=True)
        cmd.add_argument('--repo', default=str(ROOT))
    args = parser.parse_args()
    from production_guard import workflow
    # workflow() checks the running checkout, so --repo must identify that checkout.
    if Path(args.repo).resolve() != ROOT:
        raise ValueError('Run the script from the selected maintained checkout')
    if args.command == 'plan':
        output, product = Path(args.output).resolve(), Path(args.product).resolve()
        if output.exists() or output.is_relative_to(product):
            raise ValueError('New output outside canonical product directory required')
        result = build(product, args.information_plan, workflow(), args.request_reference, args.preserve, args.repo, require_presentation=True)
        check(result, product, args.repo)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print('BUSINESS_SERIES_PLAN_WRITTEN_NOT_APPROVED')
    else:
        plan = brand_assets.read(args.plan)
        if plan.get('presentationContractVersion') != 2:
            raise ValueError('New Business production requires the current reference-adaptation plan')
        if plan.get('workflowSha') != workflow():
            raise ValueError('Selected workflow changed; reconcile the series plan')
        print(json.dumps(check(plan, args.product, args.repo), indent=2))


if __name__ == '__main__':
    main()
