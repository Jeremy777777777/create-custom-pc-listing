"""Bind operative image-rule sections to scoped policy; check in production/CI.

Refresh is an explicit workflow-maintenance operation, never a product-review
migration. Existing hashes and approvals are not rewritten.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

POLICY = 'assets/workflow-execution-policy.json'


def source_bytes(root, row):
    name = row.get('path', '')
    part = PurePosixPath(name)
    if (not name or part.is_absolute() or any(p in ('', '.', '..') for p in name.split('/'))
            or '\\' in name or ':' in name or part.parts[0] not in {'references', 'assets'}):
        raise ValueError('Policy source must be an exact maintained relative path')
    root = Path(root).resolve()
    path = (root/name).resolve()
    if not path.is_relative_to(root):
        raise ValueError('Policy source leaves its checkout')
    text = path.read_text(encoding='utf-8-sig').replace('\r\n', '\n')
    heading = row.get('section')
    if heading is not None:
        lines = text.splitlines(keepends=True)
        matches = [i for i, line in enumerate(lines) if line.rstrip('\r\n') == heading]
        if len(matches) != 1 or not re.fullmatch(r'#{1,6} .+', heading):
            raise ValueError('Policy section missing or ambiguous: '+name)
        start = matches[0]; level = len(heading.split(' ', 1)[0]); end = len(lines)
        for i in range(start+1, len(lines)):
            mark = re.match(r'^(#{1,6}) ', lines[i])
            if mark and len(mark[1]) <= level:
                end = i; break
        text = ''.join(lines[start:end])
    return text.encode('utf-8')


def selected_sources(policy, series, kind, root, historical=False, extra_keys=()):
    rows = []
    for key in ('shared', kind, series, *extra_keys):
        sources = policy['imageReview'][key].get('sourceBindings', [])
        rows.extend(sources.get(kind, []) if isinstance(sources, dict) else sources)
    if not rows:
        return None  # Exact legacy-v2 binding compatibility.
    result = []
    for row in rows:
        if not isinstance(row, dict) or not re.fullmatch('[0-9a-f]{64}', row.get('sha256', '')):
            raise ValueError('Pinned image policy source hash required')
        if not historical and hashlib.sha256(source_bytes(root, row)).hexdigest() != row['sha256']:
            raise ValueError('Image rule source changed; refresh the maintained policy before production: '+row['path'])
        result.append(row)
    return result


def check(root, refresh=False):
    root = Path(root)
    policy = json.loads((root/POLICY).read_text(encoding='utf-8-sig'))
    count = 0
    for rule in policy['imageReview'].values():
        groups = rule.get('sourceBindings', [])
        rows = [r for v in groups.values() for r in v] if isinstance(groups, dict) else groups
        for row in rows:
            actual = hashlib.sha256(source_bytes(root, row)).hexdigest()
            if refresh:
                row['sha256'] = actual
            elif row.get('sha256') != actual:
                raise ValueError('Image policy source/version is stale: '+row['path'])
            count += 1
    if not count:
        raise ValueError('Current policy requires scoped rule-source bindings')
    if refresh:
        (root/POLICY).write_text(json.dumps(policy, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
    return {'state': 'IMAGE_POLICY_SOURCES_REFRESHED' if refresh else 'IMAGE_POLICY_SOURCES_CHECKED', 'sourceCount': count}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['check', 'refresh'])
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(check(args.repo, args.command == 'refresh')))


if __name__ == '__main__':
    main()
