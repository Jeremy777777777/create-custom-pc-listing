"""Keep new product business files out of workflow-code commits after Drive cutover."""
import argparse
import subprocess
from pathlib import Path


def check(root, base, head):
    changed = subprocess.check_output(
        ['git', 'diff', '--name-only', '-z', '--no-renames', base, head, '--', 'product generated photo/'],
        cwd=root).decode('utf-8').split('\0')
    reusable = {'product generated photo/README.md', 'product generated photo/image-manifest-template.md'}
    forbidden = [name for name in changed if name and name not in reusable]
    if forbidden:
        raise ValueError('Final product files belong in Google Drive; remove business-file changes from this workflow commit: ' + ', '.join(forbidden))
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', default='.')
    parser.add_argument('--base', required=True)
    parser.add_argument('--head', required=True)
    args = parser.parse_args()
    check(Path(args.directory), args.base, args.head)
    print('DRIVE_STORAGE_BOUNDARY_PASS: no product business-file changes in workflow commit')
