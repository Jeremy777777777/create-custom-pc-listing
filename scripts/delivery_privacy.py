"""Screen JSON evidence and project a new shareable connector-readback copy.

Offline only. Never upload, alter facts, authenticate evidence or grant approval.
"""
import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urlsplit, urlunsplit


PRIVATE_KEYS = {
    'serial', 'rawserial', 'serialnumber', 'servicetag', 'sn', 'password',
    'credential', 'credentials', 'authorization', 'cookie', 'cookies',
    'token', 'accesstoken', 'refreshtoken', 'idtoken', 'clientsecret', 'apikey',
}
PRIVATE_QUERY_KEYS = PRIVATE_KEYS | {
    'sig', 'signature', 'xamzsignature', 'xamzcredential', 'xgoogsignature',
    'xgoogcredential', 'auth', 'authcode', 'keypairid', 'policy',
}
READBACK_KEYS = (
    'relativePath', 'id', 'name', 'parents', 'mimeType', 'size', 'webViewLink',
    'md5Checksum', 'sha256Checksum', 'downloadedSha256', 'readBackAtUtc', 'trashed',
)
CANONICAL_RECORDS = {
    'product-facts.json', 'research-ledger.json', 'style-lock.json',
    'visual-review.json', 'semantic-review.json', 'delivery-status.json',
}
URL = re.compile(r'''https?://[^\s<>"']+''', re.I)
LOCAL_PATH = re.compile(r'(?<![a-z0-9])[a-z]:[\\/]|file://|\\\\[^\\\s]+\\|/(?:Users|home)/[^/\s]+', re.I)
SERIAL_PATH = re.compile(r'/(?:service-?tag|serial(?:number)?|sn)/[^/?#\s]+', re.I)


def normalized_key(value):
    return re.sub(r'[^a-z0-9]', '', value.casefold())


def decoded(value):
    for _ in range(3):
        candidate = unquote(value)
        if candidate == value:
            break
        value = candidate
    return value


def private_values(values):
    if not isinstance(values, list) or any(not isinstance(v, str) or len(v.strip()) < 4 for v in values):
        raise ValueError('Private identifiers must be a list of strings of at least four characters')
    return tuple(decoded(v).casefold() for v in values)


def findings(payload, known_private_values=()):
    """Return locations/codes only, never the sensitive field name or value."""
    needles = private_values(list(known_private_values))
    found = set()

    def text(value, location):
        value = decoded(value)
        if any(needle in value.casefold() for needle in needles):
            found.add((location, 'KNOWN_PRIVATE_VALUE'))
        if LOCAL_PATH.search(value):
            found.add((location, 'LOCAL_PRIVATE_PATH'))
        for match in URL.finditer(value):
            try:
                url = urlsplit(match.group())
                if url.username or url.password:
                    found.add((location, 'URL_CREDENTIALS'))
                if any(normalized_key(key) in PRIVATE_QUERY_KEYS for key, _ in parse_qsl(url.query, keep_blank_values=True)):
                    found.add((location, 'PRIVATE_OR_SIGNED_URL'))
                if SERIAL_PATH.search(url.path):
                    found.add((location, 'SERIAL_BEARING_URL'))
            except ValueError:
                found.add((location, 'MALFORMED_URL_REQUIRES_REVIEW'))

    def walk(value, location):
        if isinstance(value, dict):
            for index, (key, child) in enumerate(value.items()):
                key_location = f'{location}/key/{index}'
                child_location = f'{location}/value/{index}'
                text(key, key_location)
                if normalized_key(key) in PRIVATE_KEYS and child not in (None, '', [], {}):
                    found.add((child_location, 'PRIVATE_IDENTIFIER_OR_CREDENTIAL_FIELD'))
                if normalized_key(key) in ('downloadurl', 'fileuri') and child not in (None, '', [], {}):
                    found.add((child_location, 'TRANSIENT_CONNECTOR_REFERENCE'))
                walk(child, child_location)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f'{location}/item/{index}')
        elif isinstance(value, str):
            text(value, location)

    walk(payload, '$')
    return [{'location': location, 'code': code} for location, code in sorted(found)]


def stable_view_link(value, file_id, mime_type):
    if not isinstance(value, str) or not isinstance(file_id, str) or not re.fullmatch(r'[A-Za-z0-9_-]+', file_id):
        raise ValueError('Observed provider view URL and file ID required')
    url = urlsplit(value)
    if url.scheme != 'https' or url.username or url.password or url.port not in (None, 443):
        raise ValueError('Provider view URL must be HTTPS without credentials')
    drive = url.hostname == 'drive.google.com' and url.path == f'/file/d/{file_id}/view'
    office = (url.hostname == 'docs.google.com' and url.path == f'/spreadsheets/d/{file_id}/edit'
              and mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    if not (drive or office):
        raise ValueError('Observed provider view URL does not match the supplied file ID/type')
    return urlunsplit((url.scheme, url.netloc, url.path, '', ''))


def share_readbacks(payload, known_private_values=()):
    """Whitelist a derivative; supplied hashes/times remain unauthenticated input."""
    if not isinstance(payload, dict) or not isinstance(payload.get('files'), list) or not payload['files']:
        raise ValueError('A nonempty connector files list is required')
    rows, excluded = [], len(set(payload) - {'files'})
    for item in payload['files']:
        if not isinstance(item, dict):
            raise ValueError('Connector file entries must be objects')
        if not all(key in item for key in ('id', 'webViewLink', 'mimeType')):
            raise ValueError('File ID, provider view URL and MIME type required')
        row = {key: copy.deepcopy(item[key]) for key in READBACK_KEYS if key in item}
        row['webViewLink'] = stable_view_link(item['webViewLink'], item['id'], item['mimeType'])
        rows.append(row)
        excluded += len(set(item) - set(READBACK_KEYS))
    result = {'artifactRole': 'SHAREABLE_CONNECTOR_READBACKS',
              'verificationStatus': 'SUPPLIED_METADATA_NOT_AUTHENTICATED',
              'excludedFieldCount': excluded, 'files': rows}
    if findings(result, known_private_values):
        raise ValueError('Projected record still contains private content; inspect the input privately')
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('check', 'share-readbacks'))
    parser.add_argument('--input', required=True)
    parser.add_argument('--private-values-file')
    parser.add_argument('--output')
    args = parser.parse_args(argv)
    try:
        source = Path(args.input).resolve()
        raw = source.read_bytes()
        payload = json.loads(raw.decode('utf-8-sig'))
        secrets = [] if not args.private_values_file else private_values(json.loads(Path(args.private_values_file).read_text(encoding='utf-8-sig')))
        digest = hashlib.sha256(raw).hexdigest()
        if args.command == 'share-readbacks':
            if not args.output:
                raise ValueError('A new derivative output path is required')
            result = share_readbacks(payload, secrets)
            result['sourceInputSha256'] = digest
            exit_code = 0
        else:
            issues = findings(payload, secrets)
            result = {'state': 'PRIVATE_CONTENT_DETECTED' if issues else 'SHAREABLE_METADATA_SCREEN_PASS',
                      'inputSha256': digest, 'scope': 'PATTERN_AND_KNOWN_VALUE_SCREEN_ONLY',
                      'manualReviewRequired': True, 'findings': issues}
            exit_code = 1 if issues else 0
        if args.output:
            output = Path(args.output).resolve()
            if output == source or output.name.casefold() in CANONICAL_RECORDS:
                raise ValueError('Use a new noncanonical derivative/report path')
            output.parent.mkdir(parents=True, exist_ok=True)
            with output.open('x', encoding='utf-8') as stream:
                stream.write(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
        if args.command == 'check':
            print(json.dumps(result, ensure_ascii=False))
        else:
            print('SHAREABLE_DERIVATIVE_WRITTEN_NOT_VERIFIED')
        return exit_code
    except (OSError, ValueError, TypeError):
        # Do not echo private filenames, JSON excerpts, identifiers or URLs.
        print('PRIVACY_CHECK_ERROR: inspect inputs privately; no existing file was overwritten')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
