"""Screen JSON evidence and project a new shareable connector-readback copy.

Offline only. Never upload, alter facts, authenticate evidence or grant approval.
"""
import argparse
import copy
import hashlib
import json
import re
import zipfile
from datetime import datetime, timezone
from decimal import Decimal
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
        elif type(value) in (int, float) or isinstance(value, Decimal):
            # JSON numbers may be serials too. Decimal preserves large/exponent
            # literals before binary float rounding can lose identifier digits.
            number = Decimal(str(value))
            text(str(value), location)
            if number.is_finite():
                for needle in needles:
                    if needle.isascii() and needle.isdigit() and number == Decimal(needle):
                        found.add((location, 'KNOWN_PRIVATE_VALUE'))

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


def screen_file(path, known_private_values=(), serials_used=None, visual_review=None):
    """Screen actual delivery bytes, including OOXML links/comments/hidden sheets.

    Images and unparsed formats need a separate current-byte inspection record.
    No OCR, redaction, upload or factual/rights approval is implied.
    """
    path = Path(path)
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if serials_used not in (True, False):
        raise ValueError('Declare whether this run used raw serials')
    needles = private_values(list(known_private_values))
    if serials_used and not needles:
        raise ValueError('This run used serials; private known-value inventory required')
    suffix = path.suffix.casefold()
    inspected = False
    issues = findings({'filename': path.name}, needles)
    if suffix == '.json':
        issues += findings(json.loads(raw.decode('utf-8-sig'), parse_float=Decimal), needles)
        inspected = True
    elif suffix in {'.txt', '.md', '.csv', '.tsv', '.html', '.xml', '.yaml', '.yml', '.py', '.ps1'}:
        issues += findings({'text': raw.decode('utf-8-sig')}, needles)
        inspected = True
    elif suffix == '.xlsx':
        import io
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            entries = archive.infolist()
            if len(entries) > 10000 or sum(e.file_size for e in entries) > 64 * 1024 * 1024:
                raise ValueError('Workbook package too large for bounded privacy screening')
            for index, entry in enumerate(entries):
                # Scan every XML/rels part, including hidden content and document properties.
                if entry.filename.endswith(('.xml', '.rels')):
                    from xml.etree import ElementTree
                    node = ElementTree.fromstring(archive.read(entry))
                    content = list(node.itertext()) + [v for element in node.iter() for v in element.attrib.values()]
                    issues += findings({'part': index, 'text': '\n'.join(content)}, needles)
                    # OOXML preserves numbers as decimal/exponent literals. Match
                    # their exact value, without Excel/binary float rounding.
                    for cell in node.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c'):
                        if cell.get('t', 'n') != 'n':
                            continue
                        value = cell.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                        if value is not None and value.text:
                            from decimal import InvalidOperation
                            try:
                                number = Decimal(value.text)
                            except InvalidOperation:
                                raise ValueError('Invalid workbook numeric literal; private value omitted') from None
                            issues += findings({'part': index, 'numericCell': number}, needles)
            inspected = not any(e.filename.startswith(('xl/media/', 'xl/embeddings/')) for e in entries)
    elif suffix in {'.png', '.jpg', '.jpeg', '.webp'}:
        from PIL import Image
        with Image.open(path) as image:
            metadata = {str(k): str(v) for k, v in image.info.items()}
            metadata.update({str(k): str(v) for k, v in image.getexif().items()})
            issues += findings(metadata, needles)
    manual = not inspected
    if manual and visual_review is not None:
        if (visual_review.get('sha256') != digest or visual_review.get('result') != 'NO_PRIVATE_CONTENT'
                or not isinstance(visual_review.get('reviewer'), str) or not visual_review['reviewer'].strip()
                or not isinstance(visual_review.get('notes'), str) or not visual_review['notes'].strip()):
            raise ValueError('Actual current-byte privacy inspection required')
        stamp = datetime.fromisoformat(visual_review['reviewedAtUtc'].replace('Z', '+00:00'))
        if stamp.tzinfo is None or stamp.utcoffset().total_seconds() != 0 or stamp > datetime.now(timezone.utc):
            raise ValueError('Actual UTC inspection time required')
        manual = False
    return {'state': 'PRIVATE_CONTENT_DETECTED' if issues else 'MANUAL_REVIEW_REQUIRED' if manual else 'DELIVERY_PRIVACY_SCREEN_PASS',
            'inputSha256': digest, 'scope': 'PATTERN_KNOWN_VALUES_AND_SUPPLIED_INSPECTION',
            'serialInventoryDeclared': serials_used, 'manualReviewRequired': manual,
            'unknownSensitiveContentRequiresReview': True, 'findings': issues}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('check', 'share-readbacks', 'check-file'))
    parser.add_argument('--input', required=True)
    parser.add_argument('--private-values-file')
    parser.add_argument('--output')
    parser.add_argument('--serials-used', choices=('yes', 'no'))
    parser.add_argument('--visual-review', help='Actual hash-bound privacy inspection for images/unparsed content')
    args = parser.parse_args(argv)
    try:
        source = Path(args.input).resolve()
        raw = source.read_bytes()
        payload = None if args.command == 'check-file' else json.loads(
            raw.decode('utf-8-sig'), parse_float=Decimal if args.command == 'check' else float)
        secrets = [] if not args.private_values_file else private_values(json.loads(Path(args.private_values_file).read_text(encoding='utf-8-sig')))
        digest = hashlib.sha256(raw).hexdigest()
        if args.command == 'check-file':
            review = None if not args.visual_review else json.loads(Path(args.visual_review).read_text(encoding='utf-8-sig'))
            result = screen_file(source, secrets, None if args.serials_used is None else args.serials_used == 'yes', review)
            exit_code = 0 if result['state'] == 'DELIVERY_PRIVACY_SCREEN_PASS' else 1
        elif args.command == 'share-readbacks':
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
        if args.command in ('check', 'check-file'):
            print(json.dumps(result, ensure_ascii=False))
        else:
            print('SHAREABLE_DERIVATIVE_WRITTEN_NOT_VERIFIED')
        return exit_code
    except (OSError, ValueError, TypeError, KeyError, zipfile.BadZipFile):
        # Do not echo private filenames, JSON excerpts, identifiers or URLs.
        print('PRIVACY_CHECK_ERROR: inspect inputs privately; no existing file was overwritten')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
