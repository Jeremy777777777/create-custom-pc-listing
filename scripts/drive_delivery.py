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
from observation_time import utc


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def local_file(product, relative):
    part = PurePosixPath(relative)
    if not relative or '\\' in relative or ':' in relative or part.is_absolute() or any(p in ('.', '..') for p in part.parts) or str(part) != relative:
        raise ValueError('Expected a normalized product-relative file path')
    root = Path(product).resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError('File missing or outside product directory')
    if path.suffix.lower() == '.zip':
        raise ValueError('Drive README requires expanded individual files; ZIP backups stay local')
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


def verify(product, upload_plan, readbacks, destinations, context=None):
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
        drive_view = url.netloc == 'drive.google.com' and url.path == '/file/d/' + file_id + '/view'
        office_xlsx_view = (url.netloc == 'docs.google.com' and url.path == '/spreadsheets/d/' + file_id + '/edit'
                            and wanted['mimeType'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        if url.scheme != 'https' or not (drive_view or office_xlsx_view):
            raise ValueError('Expected provider Drive URL for the same file ID')
        checks = [('sha256Checksum', 'sha256'), ('downloadedSha256', 'sha256'), ('md5Checksum', 'md5')]
        present = [(key, local) for key, local in checks if remote.get(key)]
        if not present or any(remote[key].lower() != wanted[local] for key, local in present):
            raise ValueError('Missing or mismatched remote byte checksum: ' + relative)
        results.append({**wanted, 'fileId': file_id, 'parentFolderId': destinations[relative],
                        'url': remote['webViewLink'], 'verifiedBy': [key for key, _ in present],
                        'readBackAtUtc': remote['readBackAtUtc']})
    context_result = None
    if context is not None:
        from delivery_context import validate
        context_result = validate(upload_plan, destinations, context)
    return {'schemaVersion': '1.1', 'artifactRole': 'DRIVE_DELIVERY_RECEIPT',
            'productId': upload_plan['productId'], 'runId': upload_plan['runId'],
            'deliveryState': 'DRIVE_DELIVERY_VERIFIED' if context_result else 'DRIVE_BYTES_MATCHED_CONTEXT_UNCHECKED',
            'destinationPrivacyContext': context_result,
            'verifiedAtUtc': datetime.now(timezone.utc).isoformat(),
            'verificationScope': 'OFFLINE_COMPARISON_OF_SUPPLIED_CONNECTOR_READBACKS',
            'qaStatus': 'UNCHANGED_BY_STORAGE_VERIFICATION',
            'publicationStatus': 'NOT_ASSESSED', 'files': results}


def complete(product, contract_path, contract_sha256, receipt_paths):
    """Accumulate exact-run production-bound receipts; no upload or remote lock."""
    from production_guard import verify as production_verify
    production=production_verify(product,contract_path,contract_sha256)
    contract=read(contract_path)
    if production['mode']=='CONCEPT_ONLY' or not receipt_paths:
        raise ValueError('Actual production receipts required for completion')
    expected=production['files']; received={}; evidence=[]
    for path in receipt_paths:
        receipt=read(path); bound=receipt.get('productionScope',{})
        if (receipt.get('artifactRole')!='DRIVE_DELIVERY_RECEIPT'
                or receipt.get('deliveryState')!='DRIVE_DELIVERY_VERIFIED'
                or receipt.get('productId')!=contract['productId'] or receipt.get('runId')!=contract['runId']
                or receipt.get('productionState')!='SCOPED_PRODUCTION_AND_DRIVE_CHECKS_PASS'
                or bound.get('contractSha256')!=contract_sha256
                or (receipt.get('destinationPrivacyContext') or {}).get('state')!='DESTINATION_AND_PRIVACY_RECORDS_CHECKED'):
            raise ValueError('Completion requires same-run, scope/privacy-verified batch receipts')
        utc(receipt['verifiedAtUtc'])
        rows=receipt.get('files',[])
        if not rows or len({r['relativePath'] for r in rows})!=len(rows):
            raise ValueError('Completion batch has empty or duplicate files')
        for row in rows:
            name=row['relativePath']
            if (name not in expected or row.get('sha256')!=expected[name]
                    or bound.get('files',{}).get(name)!=row['sha256']
                    or not row.get('fileId') or not row.get('parentFolderId') or not row.get('verifiedBy')):
                raise ValueError('Batch file is outside the contract or stale')
            prior=received.get(name)
            if prior and any(prior.get(k)!=row.get(k) for k in ('sha256','fileId','parentFolderId')):
                raise ValueError('Conflicting batch versions require reconciliation')
            received[name]=row
        evidence.append({'sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),
                         'files':sorted(r['relativePath'] for r in rows)})
    missing=sorted(set(expected)-set(received))
    return {'schemaVersion':1,'artifactRole':'DRIVE_CONTRACT_COMPLETION_RECEIPT',
            'productId':contract['productId'],'runId':contract['runId'],'contractSha256':contract_sha256,
            'deliveryState':'DRIVE_DELIVERY_PARTIAL' if missing else 'DRIVE_DELIVERY_VERIFIED',
            'allContractedOutputsVerified':not missing,'remainingContractedFiles':missing,
            'verifiedAtUtc':datetime.now(timezone.utc).isoformat(),'files':[received[n] for n in sorted(received)],
            'batchEvidence':evidence,'productionScope':production,
            'verificationScope':'SUPPLIED_VERIFIED_BATCH_RECEIPTS_NOT_A_FRESH_PROVIDER_READ',
            'publicationStatus':'NOT_ASSESSED'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    make = commands.add_parser('plan')
    make.add_argument('--run-id', required=True)
    make.add_argument('--file', action='append', required=True)
    check = commands.add_parser('verify')
    for flag in ('plan', 'readbacks', 'destinations'):
        check.add_argument('--' + flag, required=True)
    check.add_argument('--context', required=True, help='Observed product folder chain and per-file privacy screens')
    finish=commands.add_parser('complete')
    finish.add_argument('--receipt',action='append',required=True,help='Existing verified production-bound batch receipt')
    for command in (make, check, finish):
        command.add_argument('--product', required=True)
        command.add_argument('--output', required=True)
        command.add_argument('--production-contract', required=True, help='Pre-edit scope contract retained in the run record')
        command.add_argument('--contract-sha256', required=True, help='Independently retained pre-edit contract digest')
    args = parser.parse_args()
    output = Path(args.output).resolve()
    if output.exists() or output.is_relative_to(Path(args.product).resolve()):
        raise ValueError('Use a new output path outside canonical product files')
    if args.command == 'plan':
        from production_guard import verify as production_verify
        contract=read(args.production_contract)
        if args.run_id!=contract['runId']: raise ValueError('Delivery run differs from production contract')
        production=production_verify(args.product,args.production_contract,args.contract_sha256,args.file)
        if production['mode']=='CONCEPT_ONLY': raise ValueError('Concepts cannot use final product delivery')
        result = plan(args.product, args.run_id, args.file)
        if {f['relativePath']:f['sha256'] for f in result['files']}!=production['files']:
            raise ValueError('Files changed between production check and upload planning')
        result['productionScope']=production
    elif args.command=='complete':
        result=complete(args.product,args.production_contract,args.contract_sha256,args.receipt)
    else:
        from production_guard import verify as production_verify
        upload_plan=read(args.plan)
        contract=read(args.production_contract)
        if upload_plan['runId']!=contract['runId']: raise ValueError('Delivery run differs from production contract')
        if any(read(args.context)['fileRoles'].get(n)!=role for n,role in contract['outputs'].items()
               if n in {f['relativePath'] for f in upload_plan['files']}):
            raise ValueError('Delivery roles differ from production contract')
        production=production_verify(args.product,args.production_contract,args.contract_sha256,
                                     [f['relativePath'] for f in upload_plan['files']])
        if production['mode']=='CONCEPT_ONLY': raise ValueError('Concepts cannot use final product delivery')
        result=verify(args.product,upload_plan,read(args.readbacks),read(args.destinations),read(args.context))
        result['productionScope']=production
        result['productionState']='SCOPED_PRODUCTION_AND_DRIVE_CHECKS_PASS'
        result['deliveryScope']='CONTRACT' if set(production['files'])==set(contract['outputs']) else 'BATCH'
        result['allContractedOutputsVerified']=set(production['files'])==set(contract['outputs'])
        result['remainingContractedFiles']=sorted(set(contract['outputs'])-set(production['files']))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(result.get('deliveryState', result.get('state')))


if __name__ == '__main__':
    main()
