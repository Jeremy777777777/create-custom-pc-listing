"""Verify immutable earlier-stage workbook bundles; never approve them for export."""
import hashlib
import json
import re
import subprocess
from pathlib import Path


def check_snapshot(directory):
    directory = Path(directory).resolve()
    if (directory/'snapshot.json').is_symlink():
        raise ValueError('Snapshot receipt must be a local regular file')
    receipt = json.loads((directory/'snapshot.json').read_text(encoding='utf-8-sig'))
    required = {'schemaVersion', 'artifactRole', 'exportEligible', 'productId',
                'configurationId', 'stage', 'files'}
    if (not isinstance(receipt, dict) or set(receipt) != required
            or type(receipt['schemaVersion']) is not int or receipt['schemaVersion'] != 1):
        raise ValueError('Invalid snapshot receipt schema')
    if receipt['artifactRole'] != 'HISTORICAL_SNAPSHOT' or receipt['exportEligible'] is not False:
        raise ValueError('Snapshot must remain historical and ineligible for export')
    if receipt['stage'] not in ('RESEARCH_REVIEW', 'LISTING_DRAFT'):
        raise ValueError('Invalid snapshot stage')
    for field in ('productId', 'configurationId'):
        if not isinstance(receipt[field], str) or not receipt[field].strip():
            raise ValueError('Snapshot requires product/configuration IDs')
    if not isinstance(receipt['files'], dict) or set(receipt['files']) != {'workbook', 'ledger', 'template'}:
        raise ValueError('Snapshot must bind workbook, original ledger and original template')
    paths = set()
    for role, record in receipt['files'].items():
        if not isinstance(record, dict) or set(record) != {'path', 'sha256'}:
            raise ValueError('Invalid snapshot file record')
        name, sha = record['path'], record['sha256']
        if (not isinstance(name, str) or not name or name in ('.', '..')
                or any(c in name for c in '/\\:') or Path(name).name != name):
            raise ValueError('Snapshot paths must be local filenames')
        target = (directory/name).resolve()
        if target.parent != directory or target in paths:
            raise ValueError('Snapshot file escapes its bundle or duplicates another role')
        paths.add(target)
        if not isinstance(sha, str) or re.fullmatch(r'[0-9a-f]{64}', sha) is None:
            raise ValueError('Invalid snapshot SHA256')
        if hashlib.sha256(target.read_bytes()).hexdigest() != sha:
            raise ValueError('Snapshot bytes changed: ' + role)
    expected = paths | {directory/'snapshot.json'}
    if set(directory.iterdir()) != expected:
        raise ValueError('Snapshot bundle contains undeclared files or subdirectories')
    return {'result': 'SNAPSHOT_HASHES_VERIFIED', 'exportEligible': False, 'stage': receipt['stage'],
            'productId': receipt['productId'], 'configurationId': receipt['configurationId']}


def check_snapshots(root):
    checked = 0
    products = Path(root)/'product generated photo'
    for parent in products.glob('*/workbook-snapshots'):
        if parent.is_symlink() or not parent.is_dir():
            raise ValueError('Snapshot root must be a real directory')
        for bundle in parent.iterdir():
            if bundle.is_symlink() or not bundle.is_dir():
                raise ValueError('Snapshot root contains a non-bundle entry')
            result = check_snapshot(bundle)
            if result['productId'] != parent.parent.name:
                raise ValueError('Snapshot product ID differs from its product folder')
            checked += 1
    return checked


def check_snapshot_history(root, base=None, head=None):
    """Existing bundles are append-only relative to the trusted Git base tree."""
    if bool(base)!=bool(head): raise ValueError('Snapshot history requires both base and head')
    if not base: return
    def tree(revision):
        raw=subprocess.check_output(['git','ls-tree','-rz',revision],cwd=root)
        result={}
        for entry in raw.split(b'\0'):
            if not entry: continue
            metadata,name=entry.split(b'\t',1); path=name.decode('utf-8')
            if path.startswith('product generated photo/') and '/workbook-snapshots/' in path:
                result[path]=metadata.split()[2]
        return result
    before,after=tree(base),tree(head)
    for path,blob in before.items():
        if after.get(path)!=blob: raise ValueError('Historical snapshot changed/deleted: '+path)
    old_bundles={str(Path(p).parent).replace('\\','/') for p in before}
    for path in after.keys()-before.keys():
        if str(Path(path).parent).replace('\\','/') in old_bundles: raise ValueError('Cannot append files to an existing snapshot bundle')
