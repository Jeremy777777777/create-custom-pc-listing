"""Validate recorded ERP/OEM research, never authenticate a lookup or expose serials."""
from datetime import date
from pathlib import Path
import json
import re
import subprocess
from urllib.parse import urlparse, parse_qs

def validate_serial_research(data, required=False, full_research=False):
    record = data.get('serial_research') if isinstance(data, dict) else None
    if record is None:
        if required:
            raise ValueError('serial_research required: record lookup result or the specific incomplete reason')
        return None
    # The shared schema validates shape; this function also supports direct handoff callers.
    from jsonschema import Draft202012Validator
    schema = json.loads((Path(__file__).resolve().parents[1]/'assets/research-ledger-schema.json').read_text(encoding='utf-8'))
    if list(Draft202012Validator(schema['$defs']['serialResearch']).iter_errors(record)):
        raise ValueError('Invalid serial_research record (check required fields/types; private values omitted)')
    outcome = record['outcome']
    if outcome == 'NOT_ASSESSED_LEGACY':
        if required:
            raise ValueError('Legacy serial research must be assessed before new research delivery/export')
        return record
    try:
        reviewed = date.fromisoformat(record['reviewed_date'])
        if reviewed.isoformat() != record['reviewed_date'] or reviewed > date.today():
            raise ValueError()
    except (KeyError, ValueError, TypeError):
        raise ValueError('serial_research requires a valid non-future reviewed_date YYYY-MM-DD') from None
    if full_research and record['workflow_mode'] != 'FULL_LISTING_WORKFLOW':
        raise ValueError('Workbook research/export requires FULL_LISTING_WORKFLOW serial research')
    if outcome == 'NOT_REQUIRED':
        if record['workflow_mode'] == 'FULL_LISTING_WORKFLOW':
            raise ValueError('NOT_REQUIRED cannot bypass full listing serial research')
    elif not record['sources_attempted']:
        raise ValueError('serial_research requires sources_attempted')
    if outcome not in ('COMPLETED', 'NOT_REQUIRED') or record['unresolved_fields']:
        if not record.get('next_action', '').strip() or not record.get('owner', '').strip():
            raise ValueError('Incomplete serial research requires next_action and owner')
    if outcome != 'COMPLETED':
        if record['units'] or record['resolved_fact_ids'] or record['factory_sold_differences']:
            raise ValueError('Incomplete/skipped lookup cannot claim completed unit facts or reconciliation')
        return record
    if not record['units'] or not record['resolved_fact_ids']:
        raise ValueError('Completed serial research requires units and resolved_fact_ids')
    facts = {fact['id']: fact for fact in data.get('facts', [])}
    aliases = set()
    linked = set()
    for unit in record['units']:
        alias = unit['unit_evidence_alias']
        if alias in aliases:
            raise ValueError('Duplicate serial research unit alias')
        aliases.add(alias)
        if unit['target_configuration'] != data.get('configurationId'):
            raise ValueError('Serial research unit belongs to another target configuration')
        url = urlparse(unit['oem_configuration_source'])
        if (url.scheme != 'https' or not url.hostname or url.username or url.password or url.fragment
                or any(key.casefold() in ('serial', 'serialnumber', 'serial_number', 'sn', 'servicetag', 'service_tag')
                       for key in parse_qs(url.query))
                or re.search(r'(?i)/(?:service-?tag|serial(?:number)?|sn)/[^/]+', url.path)):
            raise ValueError('OEM source must be a sanitized HTTPS link without unit serial identifiers')
        if not unit['fact_ids']:
            raise ValueError('Serial unit requires linked factory/current fact IDs')
        for fact_id in unit['fact_ids']:
            fact = facts.get(fact_id)
            if (fact is None or fact['fact_scope'] not in ('FACTORY', 'CURRENT_UNIT')
                    or fact['configurationId'] != data['configurationId']
                    or fact.get('evidence', {}).get('unit_evidence_alias') != alias):
                raise ValueError('Serial unit fact must exist with matching alias, configuration and FACTORY/CURRENT_UNIT scope')
            linked.add(fact_id)
    if not set(record['resolved_fact_ids']).issubset(linked):
        raise ValueError('Resolved serial facts must link to the recorded units')
    if any(facts[fid]['status'] != 'VERIFIED' for fid in record['resolved_fact_ids']):
        raise ValueError('Resolved serial facts must be VERIFIED in their own scope')
    if not record['reconciliation'].strip():
        raise ValueError('Completed serial lookup requires factory/current/sold reconciliation')
    return record


def serial_research_summary(data):
    record = validate_serial_research(data)
    if record is None:
        return {'outcome': 'NOT_ASSESSED_LEGACY', 'recordPresent': False,
                'factualReadinessAssessed': False}
    if record['outcome'] == 'NOT_ASSESSED_LEGACY':
        return {'outcome': 'NOT_ASSESSED_LEGACY', 'recordPresent': True,
                'reason': record['reason'], 'factualReadinessAssessed': False}
    facts = {fact['id']:fact for fact in data.get('facts', [])}
    return {**record, 'recordPresent': True,
            'evidenceKinds': sorted({unit['serial_source_kind'] for unit in record['units']}),
            'resolvedAttributes': [{key:facts[fid][key] for key in ('id','sheet','attribute','fact_scope','status')}
                                   for fid in record['resolved_fact_ids']],
            'factualReadinessAssessed': False}


def check_serial_research_delivery(root, base=None, head=None):
    """Require records on changed/new research; report untouched legacy data separately.

    Revision checks inspect HEAD-side blobs, not possibly different worktree files.
    Local checks compare the worktree to HEAD. Unchanged legacy products remain readable.
    """
    if bool(base) != bool(head):
        raise ValueError('Serial research revision checks require both base and head')
    root = Path(root).resolve()
    def git(*args):
        return subprocess.run(['git', *args], cwd=root, capture_output=True, check=False)
    def blob(revision, path):
        result = git('show', revision + ':' + path)
        return result.stdout if result.returncode == 0 else None
    try:
        top = git('rev-parse', '--show-toplevel')
    except FileNotFoundError:
        if base or (root/'.git').exists():
            raise ValueError('Git required for serial research delivery checks') from None
        top = None
    is_repo = top is not None and top.returncode == 0 and Path(top.stdout.decode().strip()).resolve() == root
    if base and not is_repo:
        raise ValueError('Serial research revisions require a Git checkout')
    changed_products = set()
    if is_repo:
        args = ['diff', '--name-only', '-z', '--no-renames', base or 'HEAD']
        if head:
            args.append(head)
        changes = git(*args, '--', 'product generated photo')
        if changes.returncode:
            raise ValueError('Cannot determine changed serial research delivery')
        paths = changes.stdout.split(b'\0')
        if not head:
            extra = git('ls-files', '--others', '--exclude-standard', '-z', '--', 'product generated photo')
            if extra.returncode:
                raise ValueError('Cannot determine untracked research delivery')
            paths += extra.stdout.split(b'\0')
        for raw in paths:
            parts = raw.decode('utf-8').split('/')
            if len(parts) == 3 and (parts[2] == 'research-ledger.json' or parts[2].casefold().endswith(('.xlsx', '.research-summary.json'))):
                exists = blob(head, raw.decode('utf-8')) is not None if head else (root/raw.decode('utf-8')).is_file()
                if exists:
                    changed_products.add(parts[1])
    if head:
        tree = git('ls-tree', '-r', '--name-only', '-z', head, '--', 'product generated photo')
        if tree.returncode:
            raise ValueError('Cannot read serial research target revision')
        names = [raw.decode('utf-8') for raw in tree.stdout.split(b'\0') if raw]
        ledger_paths = [p for p in names if len(p.split('/')) == 3 and p.endswith('/research-ledger.json')]
    else:
        ledger_paths = [p.relative_to(root).as_posix() for p in (root/'product generated photo').glob('*/research-ledger.json')]
    records = {}; legacy = []
    for path in ledger_paths:
        data = json.loads(blob(head, path).decode('utf-8-sig') if head else (root/path).read_text(encoding='utf-8-sig'))
        product = path.split('/')[1]
        required = product in changed_products
        record = validate_serial_research(data, required=required)
        if record is None or record['outcome'] == 'NOT_ASSESSED_LEGACY':
            legacy.append(product)
        else:
            records[product] = record['outcome']
        if required and record and record['workflow_mode'] != 'FULL_LISTING_WORKFLOW':
            workbook_exists = (any(p.startswith('product generated photo/' + product + '/') and len(p.split('/')) == 3 and p.casefold().endswith('.xlsx') for p in names)
                               if head else any(p.suffix.casefold() == '.xlsx' for p in (root/'product generated photo'/product).iterdir()))
            if workbook_exists:
                raise ValueError('Workbook delivery requires FULL_LISTING_WORKFLOW serial research')
    if changed_products - {p.split('/')[1] for p in ledger_paths}:
        raise ValueError('Changed research workbook/summary requires a scoped ledger with serial_research')
    return {'recordedOutcomes': records, 'legacyNotAssessed': sorted(legacy),
            'changedProductsChecked': sorted(changed_products), 'factualReadinessAssessed': False}
