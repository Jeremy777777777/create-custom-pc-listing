"""Freeze requested production scope and rerun content gates against actual bytes.

The independently retained contract digest is a trust input, not authentication.
This module never approves style, facts, image quality or marketplace publication.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
MODES = {'FULL_LISTING_WORKFLOW', 'IMAGE_ONLY_WORKFLOW', 'IMAGE_ADJUSTMENT_WORKFLOW', 'CONCEPT_ONLY'}
ROLES = {'RESEARCH', 'LISTING', 'IMAGE', 'QA', 'SOURCE', 'CONCEPT'}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def relative(value):
    if not isinstance(value, str) or not value or '\\' in value or ':' in value:
        raise ValueError('Exact product-relative path required')
    p = PurePosixPath(value)
    if p.is_absolute() or any(part in ('', '.', '..') for part in value.split('/')):
        raise ValueError('Unsafe product-relative path')
    return value


def inventory(product):
    product = Path(product).resolve()
    result = {}
    for path in sorted(product.rglob('*')):
        if path.is_symlink() or (hasattr(path, 'is_junction') and path.is_junction()) or not path.resolve().is_relative_to(product):
            raise ValueError('Linked product paths cannot establish a production baseline')
        if path.is_file():
            result[relative(path.relative_to(product).as_posix())] = sha(path)
    return result


def workflow():
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    paths = ['scripts', 'references', 'assets', 'SKILL.md', 'AGENTS.md']
    if subprocess.check_output(['git', 'status', '--porcelain', '--', *paths], cwd=ROOT, text=True).strip():
        raise ValueError('Production requires a clean committed workflow; do not edit gates during a product run')
    return revision


def validate_contract(contract):
    from gallery_engine import NAMES
    if contract.get('schemaVersion') != 1 or contract.get('mode') not in MODES:
        raise ValueError('Unknown production contract/mode')
    for key in ('productId', 'configurationId', 'requestReference', 'runId'):
        if not isinstance(contract.get(key), str) or not contract[key].strip():
            raise ValueError('Missing production identity/request reference: ' + key)
    if not re.fullmatch(r'[0-9a-f]{40}', contract.get('workflowSha', '')):
        raise ValueError('Exact workflow commit required')
    from observation_time import utc
    utc(contract.get('createdAtUtc'))
    allowed, outputs = contract.get('allowedChanges'), contract.get('outputs')
    if not isinstance(allowed, list) or not allowed or len(allowed) != len(set(allowed)) or not isinstance(outputs, dict) or not outputs:
        raise ValueError('Nonempty exact change and output inventories required')
    for name in allowed: relative(name)
    for name, role in outputs.items():
        relative(name)
        if role not in ROLES: raise ValueError('Unknown output role')
        if name in NAMES and role != 'IMAGE': raise ValueError('Canonical slots cannot be relabelled')
        if role == 'IMAGE' and name not in NAMES: raise ValueError('IMAGE must be a canonical slot')
        if '/' not in name and Path(name).suffix.lower() in {'.xlsx', '.xls', '.xlsm'} and role not in {'RESEARCH', 'LISTING'}:
            raise ValueError('Workbook cannot bypass stage checks by relabelling its role')
        if role in {'RESEARCH', 'LISTING'} and (Path(name).suffix.lower() != '.xlsx' or '/' in name):
            raise ValueError('Original current XLSX must be beside product facts')
    slots = contract.get('selectedSlots', [])
    if not isinstance(slots, list) or len(set(slots)) != len(slots) or not set(slots) <= set(NAMES):
        raise ValueError('Invalid selected image slots')
    if {n for n, role in outputs.items() if role == 'IMAGE'} != set(slots):
        raise ValueError('Image outputs must exactly match requested slots')
    if contract['mode'] == 'IMAGE_ONLY_WORKFLOW' and set(slots) != set(NAMES):
        raise ValueError('Image-only generation requires all eleven slots')
    if contract['mode'] == 'IMAGE_ADJUSTMENT_WORKFLOW' and not slots:
        raise ValueError('Image adjustment needs explicit requested slots')
    if contract['mode'] in {'IMAGE_ONLY_WORKFLOW', 'IMAGE_ADJUSTMENT_WORKFLOW', 'CONCEPT_ONLY'}:
        if any(Path(n).suffix.lower() in {'.xlsx', '.xls', '.xlsm'} for n in allowed) or any(r in {'RESEARCH','LISTING'} for r in outputs.values()):
            raise ValueError('This mode cannot recreate or change workbooks')
    if contract['mode'] == 'CONCEPT_ONLY' and (slots or any(n in NAMES for n in allowed) or any(r not in {'CONCEPT','SOURCE','QA'} for r in outputs.values())):
        raise ValueError('Concepts cannot become canonical completed outputs')
    if contract['mode'] != 'CONCEPT_ONLY' and 'CONCEPT' in outputs.values():
        raise ValueError('Concept output requires explicit concept mode')
    if any(n in NAMES and n not in slots for n in allowed):
        raise ValueError('Unrequested canonical slot in change scope')
    baseline = contract.get('baseline')
    if not isinstance(baseline, dict): raise ValueError('Observed baseline required')
    for name, digest in baseline.items():
        relative(name)
        if not isinstance(digest,str) or not re.fullmatch(r'[0-9a-f]{64}', digest): raise ValueError('Invalid baseline digest')
    if slots:
        approval = contract.get('styleApproval', {})
        if not approval.get('userReference') or not re.fullmatch(r'[0-9a-f]{64}', approval.get('styleLockSha256', '')):
            raise ValueError('Actual USER style approval reference and locked style bytes required')
    return contract


def capture(product, request):
    """Call after observing old bytes, before edits. Request comes from actual scope."""
    product = Path(product).resolve()
    contract = {**request, 'schemaVersion': 1, 'productId': product.name,
                'createdAtUtc': datetime.now(timezone.utc).isoformat(),
                'workflowSha': workflow(), 'baseline': inventory(product)}
    validate_contract(contract)
    if contract.get('selectedSlots') and (sha(product/'style-lock.json')!=contract['styleApproval']['styleLockSha256']
            or read(product/'style-lock.json').get('status')!='APPROVED'):
        raise ValueError('Capture requires the actual user-approved style bytes')
    return contract


def check_scope(product, contract):
    validate_contract(contract)
    product = Path(product).resolve()
    if product.name != contract['productId']: raise ValueError('Wrong product for this production contract')
    actual = inventory(product)
    before = contract['baseline']
    if set(before) - set(actual): raise ValueError('Baseline files deleted; preserve prior files outside this production run')
    changed = {name for name in actual if actual[name] != before.get(name)}
    if not changed <= set(contract['allowedChanges']):
        raise ValueError('Changes outside requested scope: ' + ', '.join(sorted(changed - set(contract['allowedChanges']))))
    if not set(contract['outputs']) <= set(actual): raise ValueError('Requested output is missing')
    facts = read(product/'product-facts.json')
    from product_identity import product_id
    base_id=facts.get('selectedBaseConfiguration',{}).get('id')
    ledger_path=product/'research-ledger.json'
    ledger=read(ledger_path) if ledger_path.exists() else None
    if isinstance(ledger,dict):
        if ledger.get('productId')!=contract['productId'] or ledger.get('configurationId')!=contract['configurationId']:
            raise ValueError('Research identity differs from the frozen request')
        base_id=base_id or ledger.get('configurationId')
    if product_id(facts) != contract['productId'] or base_id != contract['configurationId']:
        raise ValueError('Product/configuration differs from the frozen request')
    if contract.get('selectedSlots'):
        if sha(product/'style-lock.json') != contract['styleApproval']['styleLockSha256'] or read(product/'style-lock.json').get('status') != 'APPROVED':
            raise ValueError('User-approved style lock changed or is not approved')
    return actual, sorted(changed)


def verify(product, contract_path, expected_sha256, planned_files=None):
    # Digest must come from the independently retained pre-edit run record.
    if sha(contract_path) != expected_sha256: raise ValueError('Frozen production contract changed')
    contract = read(contract_path)
    actual, changed = check_scope(product, contract)
    if workflow() != contract['workflowSha']: raise ValueError('Workflow revision differs from production contract')
    product = Path(product).resolve()
    selected = set(planned_files) if planned_files is not None else set(contract['outputs'])
    if not selected or not selected <= set(contract['outputs']): raise ValueError('Delivery exceeds contracted outputs')
    results = {}
    for name in sorted(selected):
        role = contract['outputs'][name]
        if role in {'RESEARCH', 'LISTING'}:
            from workbook_reference_audit import check_paths as check_references
            check_references(product/'research-ledger.json', product/name, required=True)
            from research_export import run
            result = run(ROOT/'assets/listing-workbook-template.xlsx', product/'research-ledger.json', product/name,
                         'draft', contract['productId'], contract['configurationId'],
                         'LISTING_DRAFT' if role == 'LISTING' else 'RESEARCH_REVIEW', check_copy=role=='LISTING')
            from workbook_paths import files_with_suffix
            summaries=[read(p) for p in files_with_suffix(product,'.research-summary.json')
                       if read(p).get('workbookFile','').casefold()==name.casefold()]
            if len(summaries)!=1 or summaries[0].get('productFactsBindingVersion')!=1:
                raise ValueError('Current workbook needs one metadata-bound research summary')
            summary=summaries[0]
            for key in ('productId','configurationId','stage','workbookSha256','ledgerSha256','templateSha256','productFactsSha256','coverageSummary'):
                if summary.get(key)!=result[key]: raise ValueError('Workbook summary stale: '+key)
            from research_audit import validate_summary_trace
            validate_summary_trace(read(product/'research-ledger.json'),summary['researchTrace'])
            trace=summary['researchTrace']
            if trace.get('missingFields',0) and not trace.get('legacyReuse',{}).get('retainedInputs'):
                raise ValueError('New production needs research traces or current dependency-bound legacy reuse')
            results[name] = {'state': result['result'], 'copyChecked':role=='LISTING',
                             'marketplaceExportAssessed':False, 'coverageSummary': result['coverageSummary']}
    slots = [n for n in contract.get('selectedSlots',[]) if n in selected]
    if slots:
        import gallery_engine as gallery
        if contract['mode'] == 'IMAGE_ADJUSTMENT_WORKFLOW':
            report = read(product/'partial-update-qa.json')
            if set(report.get('selectedSlots',[])) != set(contract['selectedSlots']):
                raise ValueError('Partial review scope differs from user request')
            gallery.validate_partial(product, slots)
        else:
            gallery.validate(product)
        results['images'] = {'state': 'SCOPED_IMAGE_EVIDENCE_CHECK_PASS', 'slots': slots}
    if actual != inventory(product): raise ValueError('Product inputs changed while checks ran')
    if sha(contract_path) != expected_sha256: raise ValueError('Contract changed during checks')
    return {'schemaVersion': 1, 'state': 'PRODUCTION_SCOPE_CHECK_PASS', 'productId': contract['productId'],
            'configurationId': contract['configurationId'], 'runId': contract['runId'], 'mode': contract['mode'],
            'contractSha256': expected_sha256, 'workflowSha': contract['workflowSha'],
            'changedFiles': changed, 'files': {n:actual[n] for n in sorted(selected)}, 'checks': results,
            'styleApproval': 'USER_REFERENCE_BOUND' if slots else 'NOT_NEEDED_FOR_THIS_DELIVERY',
            'qualityScope': 'STRUCTURE_AND_SUPPLIED_REVIEW_EVIDENCE_ONLY',
            'publicationStatus': 'NOT_AUTHORIZED_BY_THIS_CHECK'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['capture', 'check'])
    parser.add_argument('--product', required=True)
    parser.add_argument('--request', help='Explicit run scope JSON, for capture')
    parser.add_argument('--contract')
    parser.add_argument('--contract-sha256')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    if output.exists() or output.is_relative_to(Path(args.product).resolve()):
        raise ValueError('Use a new run-record path outside product files')
    if args.command == 'capture':
        if not args.request: parser.error('capture requires --request')
        result = capture(args.product, read(args.request))
    else:
        if not args.contract or not args.contract_sha256: parser.error('check requires contract and independently retained digest')
        result = verify(args.product, args.contract, args.contract_sha256)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'state':result.get('state','PRODUCTION_SCOPE_CAPTURED'), 'sha256':sha(output)}))


if __name__ == '__main__':
    main()
