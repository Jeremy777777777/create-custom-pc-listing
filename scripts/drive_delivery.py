"""Build byte inventories and compare authenticated Drive connector readbacks.

No network, upload, sharing, QA acceptance or product-record mutation.
"""
import argparse
import hashlib
import json
import mimetypes
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def utc(value):
    stamp = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if stamp.tzinfo is None or stamp.utcoffset().total_seconds() != 0:
        raise ValueError('UTC readback time required')
    return stamp


def local_file(product, relative):
    part = PurePosixPath(relative)
    if not relative or '\\' in relative or ':' in relative or part.is_absolute() or any(p in ('.', '..') for p in part.parts) or str(part) != relative:
        raise ValueError('Expected a normalized product-relative file path')
    root = Path(product).resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError('File missing or outside product directory')
    return path


def entry(product, relative):
    path = local_file(product, relative)
    data = path.read_bytes()
    return {'relativePath': relative, 'size': len(data),
            'mimeType': mimetypes.guess_type(path.name)[0] or 'application/octet-stream',
            'sha256': hashlib.sha256(data).hexdigest(),
            'md5': hashlib.md5(data).hexdigest()}


def plan(product, run_id, files):
    if not run_id.strip() or not files or len({f.casefold() for f in files}) != len(files):
        raise ValueError('Unique explicit files and a run ID required')
    return {'schemaVersion': '1.0', 'artifactRole': 'DRIVE_UPLOAD_PLAN',
            'productId': Path(product).resolve().name, 'runId': run_id,
            'createdAtUtc': datetime.now(timezone.utc).isoformat(),
            'state': 'AWAITING_DRIVE_UPLOAD',
            'files': [entry(product, f) for f in files]}


def verify(product, upload_plan, readbacks, destinations):
    if upload_plan.get('artifactRole') != 'DRIVE_UPLOAD_PLAN' or upload_plan.get('productId') != Path(product).resolve().name or not upload_plan.get('runId'):
        raise ValueError('Wrong plan or product identity')
    planned = upload_plan.get('files', [])
    names = [e['relativePath'] for e in planned]
    rows = readbacks.get('files', [])
    if not names or len({n.casefold() for n in names}) != len(names) or len(rows) != len(names) or {r.get('relativePath') for r in rows} != set(names) or set(destinations) != set(names):
        raise ValueError('Readbacks/destinations must match the exact planned file set')
    created = utc(upload_plan['createdAtUtc'])
    results, ids = [], set()
    for wanted in planned:
        relative = wanted['relativePath']
        if entry(product, relative) != wanted:
            raise ValueError('Local bytes changed after planning: ' + relative)
        remote = next(r for r in rows if r['relativePath'] == relative)
        file_id = remote.get('id')
        if not isinstance(file_id, str) or not file_id or file_id in ids or remote.get('trashed') is True:
            raise ValueError('Missing, duplicate or trashed Drive file')
        ids.add(file_id)
        if not destinations[relative] or destinations[relative] not in remote.get('parents', []):
            raise ValueError('Wrong Drive parent: ' + relative)
        if remote.get('name') != PurePosixPath(relative).name or remote.get('mimeType') != wanted['mimeType'] or int(remote.get('size', -1)) != wanted['size']:
            raise ValueError('Drive name/MIME/size mismatch: ' + relative)
        if utc(remote['readBackAtUtc']) < created:
            raise ValueError('Readback predates this plan')
        url = urlparse(remote.get('webViewLink', ''))
        if url.scheme != 'https' or url.netloc != 'drive.google.com' or url.path != '/file/d/' + file_id + '/view':
            raise ValueError('Expected provider Drive URL for the same file ID')
        checks = [('sha256Checksum', 'sha256'), ('downloadedSha256', 'sha256'), ('md5Checksum', 'md5')]
        present = [(key, local) for key, local in checks if remote.get(key)]
        if not present or any(remote[key].lower() != wanted[local] for key, local in present):
            raise ValueError('Missing or mismatched remote byte checksum: ' + relative)
        results.append({**wanted, 'fileId': file_id, 'parentFolderId': destinations[relative],
                        'url': remote['webViewLink'], 'verifiedBy': [key for key, _ in present],
                        'readBackAtUtc': remote['readBackAtUtc']})
    return {'schemaVersion': '1.0', 'artifactRole': 'DRIVE_DELIVERY_RECEIPT',
            'productId': upload_plan['productId'], 'runId': upload_plan['runId'],
            'deliveryState': 'DRIVE_DELIVERY_VERIFIED',
            'verifiedAtUtc': datetime.now(timezone.utc).isoformat(),
            'verificationScope': 'OFFLINE_COMPARISON_OF_SUPPLIED_CONNECTOR_READBACKS',
            'qaStatus': 'UNCHANGED_BY_STORAGE_VERIFICATION',
            'publicationStatus': 'NOT_ASSESSED', 'files': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    make = commands.add_parser('plan')
    make.add_argument('--run-id', required=True)
    make.add_argument('--file', action='append', required=True)
    check = commands.add_parser('verify')
    for flag in ('plan', 'readbacks', 'destinations'):
        check.add_argument('--' + flag, required=True)
    for command in (make, check):
        command.add_argument('--product', required=True)
        command.add_argument('--output', required=True)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    if output.exists() or output.is_relative_to(Path(args.product).resolve()):
        raise ValueError('Use a new output path outside canonical product files')
    result = plan(args.product, args.run_id, args.file) if args.command == 'plan' else verify(args.product, read(args.plan), read(args.readbacks), read(args.destinations))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(result.get('deliveryState', result.get('state')))


if __name__ == '__main__':
    main()
