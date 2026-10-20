"""Back up exact Git commits to Drive and publish only validated main views.

No source code is executed, no permissions are changed, and no file is deleted.
Google SDK imports occur only for a live sync; planning/tests use the standard library.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
from datetime import datetime, timezone
from urllib.request import Request, urlopen

FOLDER = 'application/vnd.google-apps.folder'
FIELDS = 'id,name,mimeType,parents,size,md5Checksum,sha256Checksum,appProperties,webViewLink,trashed'
SECRETS = ('GOOGLE_DRIVE_CLIENT_ID', 'GOOGLE_DRIVE_CLIENT_SECRET', 'GOOGLE_DRIVE_REFRESH_TOKEN')
MIMES = {'.md': 'text/markdown', '.json': 'application/json', '.py': 'text/x-python',
         '.ps1': 'text/plain', '.txt': 'text/plain', '.csv': 'text/csv',
         '.yml': 'text/yaml', '.yaml': 'text/yaml', '.png': 'image/png',
         '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.pdf': 'application/pdf',
         '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
         '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
         '.ipynb': 'application/x-ipynb+json'}


class SyncError(ValueError):
    pass


def now():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def baseline_hash(data):
    return sha(data.decode('utf-8-sig').replace('\r\n', '\n').encode())


def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True, check=False)
    if result.returncode:
        raise SyncError('Cannot read the selected Git commit; no source commands were executed')
    return result.stdout


def make_plan(root, commit, repository, branch, config):
    if not re.fullmatch(r'[0-9a-f]{40}', commit) or repository != config['repository']:
        raise SyncError('Exact configured repository and full commit SHA required')
    if git(root, 'rev-parse', 'HEAD').decode().strip() != commit:
        raise SyncError('Source checkout does not match the requested commit')
    rows = []
    for entry in git(root, 'ls-tree', '-rz', '--full-tree', commit).split(b'\0'):
        if not entry:
            continue
        header, raw_path = entry.split(b'\t', 1)
        mode, kind, blob = header.decode().split()
        path = raw_path.decode('utf-8')
        parts = PurePosixPath(path)
        if (kind != 'blob' or mode not in ('100644', '100755') or parts.is_absolute()
                or any(p in ('.', '..') for p in parts.parts) or '\\' in path or ':' in path):
            raise SyncError('Unsupported symlink/submodule/path: ' + path)
        if parts.suffix.lower() == '.zip':
            raise SyncError('Drive README excludes ZIP uploads; resolve tracked ZIP scope first: ' + path)
        if any(p == '.env' or p.startswith('.env.') and p not in ('.env.example', '.env.sample') for p in parts.parts):
            raise SyncError('Credential/environment files cannot be backed up: ' + path)
        data = git(root, 'cat-file', 'blob', blob)
        representation = 'GIT_BLOB'
        if data.startswith(b'version https://git-lfs.github.com/spec/v1\n'):
            pointer = data.decode('ascii')
            data = (Path(root) / path).read_bytes()
            oid = re.search(r'^oid sha256:([0-9a-f]{64})$', pointer, re.MULTILINE)
            length = re.search(r'^size ([0-9]+)$', pointer, re.MULTILINE)
            if not oid or not length or sha(data) != oid[1] or len(data) != int(length[1]):
                raise SyncError('Resolve Git LFS content before backup: ' + path)
            representation = 'RESOLVED_LFS'
        role = 'ARCHIVE_ONLY' if any(path.startswith(p) for p in config['excludedFromCurrent']) else 'WORKFLOW'
        if path in config.get('includedReusableProductPaths', []):
            role = 'WORKFLOW'
        if role == 'WORKFLOW' and (parts.parts[0] == 'assets' or path in config.get('includedReusableProductPaths', [])) and (parts.name.endswith('-schema.json') or 'template' in parts.name.lower()):
            role = 'TEMPLATE'
        rows.append({'path': path, 'gitBlob': blob, 'gitMode': mode, 'representation': representation,
                     'size': len(data), 'sha256': sha(data), 'md5': hashlib.md5(data).hexdigest(),
                     'mimeType': MIMES.get(parts.suffix.lower(), 'application/octet-stream'),
                     'currentRole': role, '_data': data})
    if not rows or len({r['path'].casefold() for r in rows}) != len(rows):
        raise SyncError('Empty or case-colliding Git inventory')
    return {'schemaVersion': 1, 'repository': repository, 'commit': commit, 'branch': branch,
            'plannedAtUtc': now(), 'state': 'PLANNED_NOT_UPLOADED', 'files': rows}


def public_plan(plan):
    return {**plan, 'files': [{k: v for k, v in row.items() if k != '_data'} for row in plan['files']]}


def remote_matches(meta, data, name, parent, mime):
    if (meta.get('trashed') or meta.get('name') != name or parent not in meta.get('parents', [])
            or meta.get('mimeType') != mime or int(meta.get('size', -1)) != len(data)):
        return False
    checks = [('sha256Checksum', sha(data)), ('md5Checksum', hashlib.md5(data).hexdigest())]
    supplied = [(key, expected) for key, expected in checks if meta.get(key)]
    return bool(supplied) and all(meta[key].lower() == expected for key, expected in supplied)


class GoogleDrive:
    """Small SDK adapter with owned namespaces and pre-generated mutation IDs."""
    def __init__(self, owner):
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        self.owner = owner
        credentials = Credentials(None, refresh_token=os.environ[SECRETS[2]],
                                  token_uri='https://oauth2.googleapis.com/token',
                                  client_id=os.environ[SECRETS[0]], client_secret=os.environ[SECRETS[1]])
        self.api = build('drive', 'v3', credentials=credentials, cache_discovery=False)
        self.child_cache = {}

    def get(self, file_id):
        return self.api.files().get(fileId=file_id, fields=FIELDS, supportsAllDrives=True).execute(num_retries=3)

    def download(self, file_id):
        from googleapiclient.http import MediaIoBaseDownload
        output = io.BytesIO()
        request = self.api.files().get_media(fileId=file_id, supportsAllDrives=True)
        download = MediaIoBaseDownload(output, request, chunksize=1024 * 1024)
        done = False
        while not done:
            _, done = download.next_chunk(num_retries=3)
        return output.getvalue()

    def children(self, parent):
        if parent not in self.child_cache:
            found, page = [], None
            while True:
                response = self.api.files().list(q="'" + parent.replace("'", "\\'") + "' in parents and trashed = false",
                    fields='nextPageToken,files(' + FIELDS + ')', pageSize=1000, pageToken=page,
                    supportsAllDrives=True, includeItemsFromAllDrives=True).execute(num_retries=3)
                found.extend(response.get('files', []))
                page = response.get('nextPageToken')
                if not page:
                    break
            self.child_cache[parent] = found
        return self.child_cache[parent]

    def tags(self, key):
        return {'syncOwner': self.owner, 'syncKey': sha(key.encode())}

    def existing(self, parent, name, key):
        hits = [f for f in self.children(parent) if f['name'] == name]
        if len(hits) > 1:
            raise SyncError('Duplicate Drive names require reconciliation: ' + name)
        if hits and any(hits[0].get('appProperties', {}).get(k) != v for k, v in self.tags(key).items()):
            raise SyncError('Unmanaged Drive name collision; existing content was preserved: ' + name)
        return hits[0] if hits else None

    def new_id(self):
        return self.api.files().generateIds(count=1, space='drive').execute(num_retries=3)['ids'][0]

    def remember(self, parent, metadata):
        rows = self.child_cache.setdefault(parent, [])
        rows[:] = [r for r in rows if r['id'] != metadata['id']]
        rows.append(metadata)

    def folder(self, parent, name, key):
        previous = self.existing(parent, name, key)
        if previous:
            if previous['mimeType'] != FOLDER:
                raise SyncError('Expected a managed folder: ' + name)
            return previous['id']
        file_id = self.new_id()
        body = {'id': file_id, 'name': name, 'mimeType': FOLDER, 'parents': [parent], 'appProperties': self.tags(key)}
        try:
            self.api.files().create(body=body, fields=FIELDS, supportsAllDrives=True).execute(num_retries=3)
        except Exception:
            # The predetermined ID makes uncertain create retries duplicate-safe.
            self.get(file_id)
        meta = self.get(file_id)
        if meta.get('name') != name or meta.get('mimeType') != FOLDER or parent not in meta.get('parents', []):
            raise SyncError('Folder readback mismatch')
        self.remember(parent, meta)
        return file_id

    def put(self, parent, name, data, mime, key, mutable=False, copy_from=None):
        from googleapiclient.http import MediaIoBaseUpload
        previous = self.existing(parent, name, key)
        if previous:
            meta = self.get(previous['id'])
            if remote_matches(meta, data, name, parent, mime):
                return meta
            if not mutable:
                raise SyncError('Immutable Drive snapshot differs: ' + name)
            file_id = previous['id']
        else:
            file_id = self.new_id()
        body = {'name': name, 'mimeType': mime, 'appProperties': self.tags(key)}
        try:
            if previous:
                request = self.api.files().update(fileId=file_id, body=body,
                    media_body=MediaIoBaseUpload(io.BytesIO(data), mimetype=mime, resumable=True),
                    fields=FIELDS, supportsAllDrives=True)
                response = None
                while response is None:
                    _, response = request.next_chunk(num_retries=3)
            elif copy_from:
                body.update(id=file_id, parents=[parent])
                self.api.files().copy(fileId=copy_from, body=body, fields=FIELDS,
                                      supportsAllDrives=True).execute(num_retries=3)
            else:
                body.update(id=file_id, parents=[parent])
                request = self.api.files().create(body=body,
                    media_body=MediaIoBaseUpload(io.BytesIO(data), mimetype=mime, resumable=True),
                    fields=FIELDS, supportsAllDrives=True)
                response = None
                while response is None:
                    _, response = request.next_chunk(num_retries=3)
        except Exception:
            # Only actual readback may recover an uncertain write. Never replay a new ID.
            meta = self.get(file_id)
            if not remote_matches(meta, data, name, parent, mime):
                raise SyncError('Uncertain Drive write; incomplete result is not delivery success') from None
        meta = self.get(file_id)
        if not remote_matches(meta, data, name, parent, mime):
            if (meta.get('trashed') or int(meta.get('size', -1)) != len(data)
                    or meta.get('name') != name or parent not in meta.get('parents', [])
                    or meta.get('mimeType') != mime or self.download(file_id) != data):
                raise SyncError('Drive byte/metadata readback mismatch: ' + name)
        self.remember(parent, meta)
        return meta

    def json_at(self, parent, name, key):
        previous = self.existing(parent, name, key)
        return json.loads(self.download(previous['id'])) if previous else None


def check_baseline(store, config):
    # Validate all fixed destination parents before any writes.
    for key in ('workflowsFolderId', 'templatesFolderId', 'archiveFolderId', 'adminFolderId'):
        meta = store.get(config[key])
        if meta.get('trashed') or meta.get('mimeType') != FOLDER or config['projectFolderId'] not in meta.get('parents', []):
            raise SyncError('Configured destination is outside the verified project root: ' + key)
    if baseline_hash(store.download(config['baselineReadmeId'])) != config['baselineReadmeTextSha256']:
        raise SyncError('Drive README baseline changed; explain/review differences before updating the baseline hash')


def nested(store, base, path, key):
    parent = base
    walked = []
    for part in PurePosixPath(path).parts[:-1]:
        walked.append(part)
        parent = store.folder(parent, part, key + ':directory:' + '/'.join(walked))
    return parent


def archive(store, plan, config):
    check_baseline(store, config)
    commit = plan['commit']
    root = store.folder(config['archiveFolderId'], config['snapshotFolderName'], 'snapshot-root')
    folder = store.folder(root, commit, 'snapshot:' + commit)
    existing = store.json_at(folder, 'SNAPSHOT.json', 'snapshot-manifest:' + commit)
    public = public_plan(plan)
    signature = sha(encoded(public['files']))
    if existing and existing.get('inventorySha256') != signature:
        raise SyncError('Committed snapshot inventory changed; original snapshot was preserved')
    state = store.json_at(config['adminFolderId'], 'github-sync-objects.json', 'object-index') or {'objects': {}}
    objects = state['objects']
    rows = []
    for row in plan['files']:
        parent = nested(store, folder, 'files/' + row['path'], 'snapshot:' + commit)
        # Unchanged content can be copied server-side from a retained snapshot.
        prior = objects.get(row['sha256'])
        meta = store.put(parent, PurePosixPath(row['path']).name, row['_data'], row['mimeType'],
                         'snapshot:' + commit + ':' + row['path'], copy_from=prior)
        objects[row['sha256']] = meta['id']
        rows.append({**{k: v for k, v in row.items() if k != '_data'}, 'fileId': meta['id'],
                     'parentFolderId': parent, 'url': meta.get('webViewLink'), 'verifiedAtUtc': now()})
    receipt = {'schemaVersion': 1, 'repository': plan['repository'], 'commit': commit,
               'inventorySha256': signature, 'state': 'WORKFLOW_SNAPSHOT_VERIFIED',
               'snapshotFolderId': folder, 'verifiedAtUtc': now(), 'files': rows,
               'productQa': 'UNCHANGED', 'publication': 'NOT_EXECUTED'}
    # Seal only after every selected file is read back. Retrying the same commit
    # keeps the original seal, while verifying all actual bytes again above.
    store.put(folder, 'SNAPSHOT.json', encoded(existing or receipt), 'application/json', 'snapshot-manifest:' + commit)
    store.put(config['adminFolderId'], 'github-sync-objects.json', encoded({'objects': objects}),
              'application/json', 'object-index', mutable=True)
    store.put(config['adminFolderId'], 'github-sync-' + commit + '.json', encoded(existing or receipt),
              'application/json', 'sync-receipt:' + commit)
    return receipt


def publish_current(store, plan, snapshot, config, check_main):
    if plan['branch'] != config['mainBranch'] or snapshot['state'] != 'WORKFLOW_SNAPSHOT_VERIFIED':
        raise SyncError('Only a verified main snapshot can become current')
    if not check_main():
        return {'state': 'ARCHIVE_ONLY_SUPERSEDED_MAIN', 'commit': plan['commit']}
    roots = {role: store.folder(config[key], config['currentFolderName'], 'current-root:' + role)
             for role, key in [('WORKFLOW', 'workflowsFolderId'), ('TEMPLATE', 'templatesFolderId')]}
    versions = {role: store.folder(root, plan['commit'], 'current-version:' + role + ':' + plan['commit'])
                for role, root in roots.items()}
    source = {r['path']: r for r in snapshot['files']}
    rows = []
    for row in plan['files']:
        role = row['currentRole']
        if role == 'ARCHIVE_ONLY':
            continue
        parent = nested(store, versions[role], row['path'], 'current:' + plan['commit'] + ':' + role)
        meta = store.put(parent, PurePosixPath(row['path']).name, row['_data'], row['mimeType'],
                         'current:' + plan['commit'] + ':' + row['path'], copy_from=source[row['path']]['fileId'])
        rows.append({'path': row['path'], 'fileId': meta['id'], 'sha256': row['sha256'],
                     'parentFolderId': parent, 'url': meta.get('webViewLink')})
    if not check_main():
        return {'state': 'ARCHIVE_ONLY_SUPERSEDED_MAIN', 'commit': plan['commit']}
    pointer = {'schemaVersion': 1, 'state': 'CURRENT_WORKFLOW_VERIFIED', 'repository': plan['repository'],
               'commit': plan['commit'], 'verifiedAtUtc': now(), 'sourceSnapshotFolderId': snapshot['snapshotFolderId'],
               'workflowFolderId': versions['WORKFLOW'], 'templatesFolderId': versions['TEMPLATE'], 'files': rows}
    # CURRENT.json is the single publication point across both current views.
    # Previous version folders remain intact; deletions are represented only by
    # absence from this new manifest, never propagated into prior snapshots.
    store.put(roots['WORKFLOW'], 'CURRENT.json', encoded(pointer), 'application/json', 'current-pointer', mutable=True)
    return pointer


def github_json(repository, path):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'listing-drive-sync'}
    if os.environ.get('GITHUB_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
    with urlopen(Request('https://api.github.com/repos/' + repository + '/' + path, headers=headers), timeout=60) as response:
        return json.load(response)


def main_is_valid(plan, config, run_id):
    run = github_json(plan['repository'], 'actions/runs/' + str(int(run_id)))
    if (run.get('head_sha') != plan['commit'] or run.get('head_branch') != config['mainBranch']
            or run.get('conclusion') != 'success' or run.get('status') != 'completed'
            or run.get('event') != 'push' or run.get('path') != config['validationWorkflowPath']
            or run.get('head_repository', {}).get('full_name') != config['repository']):
        raise SyncError('Matching successful trusted main validation run required for current publication')
    return github_json(plan['repository'], 'git/ref/heads/' + config['mainBranch'])['object']['sha'] == plan['commit']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--commit', required=True)
    parser.add_argument('--repository', required=True)
    parser.add_argument('--branch', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--plan-only', action='store_true')
    parser.add_argument('--promote', action='store_true')
    parser.add_argument('--ci-run-id', type=int)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result = {'state': 'SYNC_NOT_COMPLETED'}
    exit_code = 0
    try:
        config = json.loads(args.config.read_text(encoding='utf-8-sig'))
        plan = make_plan(args.source, args.commit, args.repository, args.branch, config)
        if args.plan_only:
            result = public_plan(plan)
        else:
            missing = [key for key in SECRETS if not os.environ.get(key)]
            if missing:
                result = {'state': 'BLOCKED_MISSING_DRIVE_AUTH', 'missingSecretNames': missing,
                          'commit': args.commit, 'plannedFileCount': len(plan['files'])}
                raise SyncError('Configure the listed GitHub Actions Secrets; no Drive sync was performed')
            store = GoogleDrive(args.repository)
            if args.promote and (not args.ci_run_id or not main_is_valid(plan, config, args.ci_run_id)):
                raise SyncError('Current promotion requires the successful main validation run and current head')
            result = archive(store, plan, config)
            if args.promote:
                result = publish_current(store, plan, result, config, lambda: main_is_valid(plan, config, args.ci_run_id))
    except Exception as error:
        if result.get('state') not in ('BLOCKED_MISSING_DRIVE_AUTH',):
            result = {'state': 'SYNC_FAILED', 'commit': args.commit}
        result['error'] = str(error) if isinstance(error, SyncError) else 'Sync failed (' + type(error).__name__ + '); review private runner diagnostics without exposing credentials'
        exit_code = 1
    args.output.write_bytes(encoded(result))
    print(json.dumps({k: result[k] for k in ('state', 'commit', 'missingSecretNames', 'error') if k in result}))
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
