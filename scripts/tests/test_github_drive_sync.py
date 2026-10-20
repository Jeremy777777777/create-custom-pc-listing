"""Exercise snapshots, retries and publication boundaries without Drive credentials."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import github_drive_sync as sync


class MemoryDrive:
    def __init__(self, config, baseline):
        self.items = {config['baselineReadmeId']: {'data': baseline}}
        for key in ('workflowsFolderId', 'templatesFolderId', 'archiveFolderId', 'adminFolderId'):
            self.items[config[key]] = {'id': config[key], 'mimeType': sync.FOLDER, 'parents': [config['projectFolderId']]}
        self.writes = 0
        self.copies = 0
        self.fail_name = None

    def get(self, file_id):
        return copy.deepcopy(self.items[file_id])

    def download(self, file_id):
        return self.items[file_id]['data']

    def find(self, parent, name, key):
        hits = [m for m in self.items.values() if parent in m.get('parents', []) and m.get('name') == name]
        if len(hits) > 1 or hits and hits[0]['key'] != key:
            raise sync.SyncError('Unmanaged/duplicate name')
        return hits[0] if hits else None

    def folder(self, parent, name, key):
        found = self.find(parent, name, key)
        if found:
            return found['id']
        file_id = 'folder-' + str(len(self.items))
        self.items[file_id] = {'id': file_id, 'name': name, 'parents': [parent], 'key': key, 'mimeType': sync.FOLDER}
        self.writes += 1
        return file_id

    def put(self, parent, name, data, mime, key, mutable=False, copy_from=None):
        if name == self.fail_name:
            raise sync.SyncError('Injected upload failure')
        previous = self.find(parent, name, key)
        if previous and previous['data'] == data:
            return self.get(previous['id'])
        if previous and not mutable:
            raise sync.SyncError('Immutable snapshot differs')
        if copy_from:
            if self.items[copy_from]['data'] != data:
                raise sync.SyncError('Copy source bytes changed')
            self.copies += 1
        file_id = previous['id'] if previous else 'file-' + str(len(self.items))
        self.items[file_id] = {'id': file_id, 'name': name, 'parents': [parent], 'key': key,
                              'mimeType': mime, 'data': data, 'size': str(len(data)),
                              'sha256Checksum': sync.sha(data), 'webViewLink': 'https://drive.google.com/file/d/' + file_id + '/view'}
        self.writes += 1
        return self.get(file_id)

    def json_at(self, parent, name, key):
        previous = self.find(parent, name, key)
        return json.loads(previous['data']) if previous else None


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.command('init', '-q')
        self.command('config', 'user.email', 'fixture@example.invalid')
        self.command('config', 'user.name', 'Fixture')
        self.write('SKILL.md', b'current workflow\n')
        self.write('assets/listing-workbook-template.xlsx', b'original template bytes')
        self.write('history/old.md', b'history is not current')
        self.write('product generated photo/VA-1/PT01.png', b'preserved product output')
        self.commit()
        self.baseline = b'Drive baseline\nNo ZIP uploads.\n'
        self.config = {'repository': 'owner/repo', 'mainBranch': 'main', 'projectFolderId': 'project',
            'workflowsFolderId': 'workflows', 'templatesFolderId': 'templates', 'archiveFolderId': 'archive',
            'adminFolderId': 'admin', 'baselineReadmeId': 'readme', 'baselineReadmeTextSha256': sync.baseline_hash(self.baseline),
            'snapshotFolderName': 'WORKFLOW_SNAPSHOTS', 'currentFolderName': 'GITHUB_CURRENT',
            'excludedFromCurrent': ['history/', 'product generated photo/']}
        self.store = MemoryDrive(self.config, self.baseline)

    def command(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], stderr=subprocess.DEVNULL)

    def write(self, path, data):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    def commit(self):
        self.command('add', '.')
        self.command('commit', '-qm', 'fixture')
        self.commit_id = self.command('rev-parse', 'HEAD').decode().strip()

    def plan(self, branch='main'):
        return sync.make_plan(self.root, self.commit_id, 'owner/repo', branch, self.config)

    def test_exact_commit_ignores_untracked_and_uncommitted_files(self):
        self.write('SKILL.md', b'uncommitted changes')
        self.write('private-experiment.txt', b'not tracked')
        plan = self.plan()
        self.assertEqual(len(plan['files']), 4)
        self.assertEqual(next(r['_data'] for r in plan['files'] if r['path'] == 'SKILL.md'), b'current workflow\n')

    def test_baseline_or_parent_drift_blocks_before_any_write(self):
        self.store.items['readme']['data'] = b'changed baseline'
        with self.assertRaisesRegex(sync.SyncError, 'baseline changed'):
            sync.archive(self.store, self.plan(), self.config)
        self.assertEqual(self.store.writes, 0)
        self.store.items['readme']['data'] = self.baseline
        self.store.items['templates']['parents'] = ['unrelated']
        with self.assertRaisesRegex(sync.SyncError, 'outside'):
            sync.archive(self.store, self.plan(), self.config)
        self.assertEqual(self.store.writes, 0)

    def test_complete_archive_retry_and_current_exclusions(self):
        plan = self.plan()
        archive = sync.archive(self.store, plan, self.config)
        writes = self.store.writes
        retry = sync.archive(self.store, plan, self.config)
        self.assertEqual(self.store.writes, writes)
        self.assertEqual(len(retry['files']), 4)
        current = sync.publish_current(self.store, plan, archive, self.config, lambda: True)
        self.assertEqual({r['path'] for r in current['files']}, {'SKILL.md', 'assets/listing-workbook-template.xlsx'})
        self.assertGreater(self.store.copies, 0)

    def test_branch_or_superseded_main_cannot_replace_current(self):
        plan = self.plan('debug')
        archive = sync.archive(self.store, plan, self.config)
        with self.assertRaises(sync.SyncError):
            sync.publish_current(self.store, plan, archive, self.config, lambda: True)
        plan['branch'] = 'main'
        self.assertEqual(sync.publish_current(self.store, plan, archive, self.config, lambda: False)['state'], 'ARCHIVE_ONLY_SUPERSEDED_MAIN')

    def test_failed_promotion_keeps_previous_pointer_and_prior_backups(self):
        first = self.plan()
        first_archive = sync.archive(self.store, first, self.config)
        first_current = sync.publish_current(self.store, first, first_archive, self.config, lambda: True)
        pointer = next(m for m in self.store.items.values() if m.get('key') == 'current-pointer')
        original_pointer = pointer['data']
        self.command('rm', '-q', 'SKILL.md')
        self.write('NEW.md', b'new rules')
        self.commit()
        second = self.plan()
        second_archive = sync.archive(self.store, second, self.config)
        self.store.fail_name = 'NEW.md'
        with self.assertRaises(sync.SyncError):
            sync.publish_current(self.store, second, second_archive, self.config, lambda: True)
        self.assertEqual(self.store.items[pointer['id']]['data'], original_pointer)
        self.store.fail_name = None
        updated = sync.publish_current(self.store, second, second_archive, self.config, lambda: True)
        self.assertNotIn('SKILL.md', {r['path'] for r in updated['files']})
        self.assertEqual(self.store.items[first_archive['files'][0]['fileId']]['data'], next(r['_data'] for r in first['files'] if r['path'] == first_archive['files'][0]['path']))
        self.assertNotEqual(updated['commit'], first_current['commit'])

    def test_zip_and_symlink_fail_preflight(self):
        self.write('backup.zip', b'ZIP stays local')
        self.commit()
        with self.assertRaisesRegex(sync.SyncError, 'ZIP'):
            self.plan()
        self.command('rm', '-q', 'backup.zip')
        blob = self.command('rev-parse', 'HEAD:SKILL.md')
        self.command('update-index', '--add', '--cacheinfo', '120000,' + blob.decode().strip() + ',link')
        self.command('commit', '-qm', 'symlink fixture')
        self.commit_id = self.command('rev-parse', 'HEAD').decode().strip()
        with self.assertRaisesRegex(sync.SyncError, 'symlink'):
            self.plan()

    def test_lfs_worktree_must_match_committed_object(self):
        data = b'actual large file content'
        pointer = ('version https://git-lfs.github.com/spec/v1\n'
                   'oid sha256:' + sync.sha(data) + '\nsize ' + str(len(data)) + '\n').encode()
        self.write('large.bin', pointer)
        self.commit()
        self.write('large.bin', data)
        row = next(r for r in self.plan()['files'] if r['path'] == 'large.bin')
        self.assertEqual(row['_data'], data)
        self.assertEqual(row['representation'], 'RESOLVED_LFS')
        self.write('large.bin', b'changed locally')
        with self.assertRaisesRegex(sync.SyncError, 'Resolve Git LFS'):
            self.plan()

    def test_main_publication_requires_matching_successful_validation(self):
        self.config['validationWorkflowPath'] = '.github/workflows/validate.yml'
        run = {'head_sha': self.commit_id, 'head_branch': 'main', 'conclusion': 'success',
               'status': 'completed', 'event': 'push', 'path': self.config['validationWorkflowPath'],
               'head_repository': {'full_name': 'owner/repo'}}
        with patch.object(sync, 'github_json', side_effect=[run, {'object': {'sha': self.commit_id}}]):
            self.assertTrue(sync.main_is_valid(self.plan(), self.config, 1))
        run['head_sha'] = '0' * 40
        with patch.object(sync, 'github_json', return_value=run):
            with self.assertRaisesRegex(sync.SyncError, 'Matching successful'):
                sync.main_is_valid(self.plan(), self.config, 1)


if __name__ == '__main__':
    unittest.main()
