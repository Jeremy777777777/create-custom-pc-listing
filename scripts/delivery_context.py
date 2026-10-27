"""Validate supplied Drive chain/privacy evidence and revision preconditions offline."""
import hashlib
import json
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
from observation_time import utc

ROOT = Path(__file__).resolve().parents[1]
FOLDER = 'application/vnd.google-apps.folder'
ROLES = {'RESEARCH': ('03_RESEARCH', 'FINAL'), 'LISTING': ('01_LISTING',),
         'IMAGE': ('02_IMAGES',), 'QA': ('04_QA',), 'SOURCE': ('90_SOURCE',)}


def check_revision(baseline, observed):
    """Call immediately before writes; cannot lock Drive or prevent a later race."""
    if baseline.get('productId') != observed.get('productId') or not baseline.get('productId'):
        raise ValueError('Revision product mismatch')
    def rows(record):
        found = {}
        for row in record['files']:
            key = row['relativePath']
            if key in found or not all(row.get(k) for k in ('id', 'sha256', 'parentFolderId')):
                raise ValueError('Incomplete/duplicate revision inventory')
            found[key] = tuple(row[k] for k in ('id', 'sha256', 'parentFolderId'))
        return found
    if rows(baseline) != rows(observed):
        raise ValueError('CURRENT_REVISION_CHANGED: reconcile before overwriting')
    if utc(observed['readBackAtUtc']) < utc(baseline['readBackAtUtc']):
        raise ValueError('Revision observation predates baseline')
    return {'state': 'PREWRITE_REVISION_MATCHED', 'scope': 'SUPPLIED_READBACKS_NOT_A_REMOTE_LOCK'}


def check_history(previous_bytes, current_bytes, expected_previous_sha256):
    if hashlib.sha256(previous_bytes).hexdigest() != expected_previous_sha256:
        raise ValueError('Previous ledger differs from verified Drive baseline')
    previous, current = (json.loads(raw.decode('utf-8-sig')) for raw in (previous_bytes, current_bytes))
    if isinstance(previous, dict):
        if not isinstance(current, dict):
            raise ValueError('Scoped Drive ledger cannot be removed/downgraded')
        if any(previous.get(k) != current.get(k) for k in ('productId', 'configurationId')):
            raise ValueError('Drive history identity/configuration changed; reconcile separately')
    return {'state': 'DRIVE_LEDGER_CONTINUITY_CHECKED', 'scope': 'SUPPLIED_PREVIOUS_BYTES_ONLY'}


def source_parent(nodes, root, relative):
    """Resolve the source's relative directories without flattening or leaving its root."""
    parent = root
    for section in relative.parts[:-1]:
        hits = [node for node in nodes.values()
                if node['name'] == section and node.get('parents') == [parent]]
        if len(hits) != 1:
            raise ValueError('Missing/ambiguous source subfolder chain')
        parent = hits[0]['id']
    return parent


def validate(upload_plan, destinations, context):
    policy = json.loads((ROOT/'assets/delivery-storage.json').read_text(encoding='utf-8'))
    product_id = upload_plan['productId']
    if context.get('productId') != product_id:
        raise ValueError('Destination context product mismatch')
    created = utc(upload_plan['createdAtUtc'])
    nodes = {}
    for node in context.get('folders', []):
        if (node.get('id') in nodes or node.get('mimeType') != FOLDER or node.get('trashed') is True
                or not node.get('id') or not node.get('name') or utc(node['readBackAtUtc']) < created):
            raise ValueError('Invalid/stale folder readback')
        nodes[node['id']] = node
    project_id, products_id = policy['projectFolderId'], policy['productsFolderId']
    if project_id not in nodes or products_id not in nodes or project_id not in nodes[products_id].get('parents', []):
        raise ValueError('Pinned project/products chain missing')
    products = [n for n in nodes.values() if n['name'] == product_id and products_id in n.get('parents', [])]
    if len(products) != 1:
        raise ValueError('Exact unique product folder required')
    roles = context.get('fileRoles', {})
    checks = context.get('privacyChecks', {})
    names = {row['relativePath'] for row in upload_plan['files']}
    if set(roles) != names or set(checks) != names:
        raise ValueError('Every planned file requires a role and current privacy screen')
    if not isinstance(context.get('serialsUsed'), bool):
        raise ValueError('Run serial-use declaration required')
    for row in upload_plan['files']:
        name = row['relativePath']
        relative = PurePosixPath(name)
        if (not name or '\\' in name or ':' in name or relative.is_absolute()
                or '..' in relative.parts or str(relative) != name):
            raise ValueError('Expected a normalized product-relative file path')
        role = roles[name]
        if role not in ROLES:
            raise ValueError('Unknown delivery role')
        basename = relative.name.upper()
        expected = ('IMAGE' if basename in {'MAIN-STRICT.JPG', 'MAIN-ENHANCED-FRONT-CANDIDATE.PNG', 'MAIN-ENHANCED-THREE-QUARTER-CANDIDATE.PNG'} or basename in {f'PT{i:02}.PNG' for i in range(1,9)}
                    else 'RESEARCH' if 'RESEARCH_REVIEW' in basename or basename in {'RESEARCH-LEDGER.JSON', 'PRODUCT-FACTS.JSON'}
                    else 'LISTING' if 'LISTING_DRAFT' in basename else None)
        # Canonical slots are top-level product files. Nested clean masters and
        # historical source records may share their basenames but remain SOURCE.
        if len(relative.parts) == 1 and expected and role != expected:
            raise ValueError('Canonical file role mismatch')
        if len(relative.parts) > 1 and expected and role != 'SOURCE':
            raise ValueError('Nested canonical names must be supporting SOURCE files')
        parent = products[0]['id']
        for section in ROLES[role]:
            hits = [n for n in nodes.values() if n['name'] == section and parent in n.get('parents', [])]
            if len(hits) != 1:
                raise ValueError('Missing/ambiguous role folder chain')
            parent = hits[0]['id']
        if role == 'SOURCE':
            parent = source_parent(nodes, parent, relative)
        if destinations.get(name) != parent:
            raise ValueError('File destination does not match product/role chain')
        check = checks[name]
        if (check.get('state') != 'DELIVERY_PRIVACY_SCREEN_PASS' or check.get('inputSha256') != row['sha256']
                or check.get('manualReviewRequired') is not False
                or check.get('serialInventoryDeclared') is not context['serialsUsed']):
            raise ValueError('Missing/stale actual-byte privacy screen')
    return {'state': 'DESTINATION_AND_PRIVACY_RECORDS_CHECKED',
            'scope': 'OFFLINE_COMPARISON_CONNECTOR_AUTHENTICATION_STILL_REQUIRED'}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    revision = commands.add_parser('revision')
    revision.add_argument('--baseline', type=Path, required=True)
    revision.add_argument('--observed', type=Path, required=True)
    history = commands.add_parser('history')
    history.add_argument('--previous', type=Path, required=True)
    history.add_argument('--current', type=Path, required=True)
    history.add_argument('--previous-sha256', required=True,
                         help='Hash from a verified previous receipt or observed legacy baseline adoption')
    args = parser.parse_args()
    if args.command == 'revision':
        result = check_revision(json.loads(args.baseline.read_text(encoding='utf-8-sig')),
                                json.loads(args.observed.read_text(encoding='utf-8-sig')))
    else:
        result = check_history(args.previous.read_bytes(), args.current.read_bytes(), args.previous_sha256)
    print(json.dumps(result))
