"""Connector/local/browser run records and scoped delivery preparation.

No upload, browser execution, permission change, publication or automatic review.
The existing production and Drive validators remain the delivery authority.
"""
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

MODES = {'CONNECTOR', 'LOCAL', 'BROWSER', 'MIXED'}
ID = r'[A-Za-z0-9][A-Za-z0-9._-]{0,127}'


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def no_links(path):
    # OneDrive cloud reparse points are not necessarily links. Reject actual
    # symlinks/junctions, never every Windows ReparsePoint attribute.
    path = Path(path).absolute()
    for item in (path, *path.parents):
        if item.is_symlink() or (hasattr(item, 'is_junction') and item.is_junction()):
            raise ValueError('Run path traverses a real link/junction')


def safe_file(root, relative):
    part = PurePosixPath(relative)
    if (not relative or '\\' in relative or ':' in relative or part.is_absolute()
            or any(v in ('', '.', '..') for v in relative.split('/'))):
        raise ValueError('Exact run-relative file required')
    no_links(Path(root)/relative)
    target = (Path(root)/relative).resolve()
    if not target.is_relative_to(Path(root).resolve()):
        raise ValueError('Run file escapes its directory')
    return target


def write(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')


def delivery_batches(data):
    """Read old single-plan manifests without rewriting their released evidence."""
    if 'deliveryBatches' in data:
        return data['deliveryBatches']
    if data['deliveryState'] == 'STAGED_NOT_UPLOADED':
        return [{'batchId':'batch-001', 'path':'delivery-plan.json',
                 'sha256':data.get('deliveryPlanSha256')}]
    return []


def create(run, product, task_id, run_id, request_reference, mode, workflow_sha):
    from product_identity import product_id
    if (mode not in MODES or not re.fullmatch(ID, task_id) or not re.fullmatch(ID, run_id)
            or not request_reference.strip() or not re.fullmatch('[0-9a-f]{40}', workflow_sha)):
        raise ValueError('Actual request, task/run IDs, execution mode and workflow SHA required')
    from production_guard import workflow
    if workflow()!=workflow_sha:
        raise ValueError('Run the task from its clean pinned workflow checkout; requested SHA differs')
    facts = read(Path(product)/'product-facts.json')
    if product_id(facts) != Path(product).name:
        raise ValueError('Exact product identity differs from its directory')
    no_links(run)
    Path(run).mkdir(parents=True, exist_ok=False)
    record = {'schemaVersion': 2, 'artifactRole': 'SCOPED_WORKFLOW_RUN',
              'taskId': task_id, 'runId': run_id, 'productId': Path(product).name,
              'requestReference': request_reference, 'workflowSha': workflow_sha,
              'createdAtUtc': now(),
              'inputObservation': {'productFactsSha256': sha(Path(product)/'product-facts.json'),
                                   'scope': 'Observed initial input; current production uses its own frozen contract'},
              'execution': {'mode': mode, 'state': 'NOT_STARTED', 'evidence': []},
              'deliveryState': 'NOT_PREPARED', 'publicationState': 'NOT_PERFORMED'}
    write(Path(run)/'run-manifest.json', record)
    return record


def validate(run, product=None):
    no_links(run)
    data = read(safe_file(run, 'run-manifest.json'))
    if (data.get('schemaVersion') != 2 or data.get('artifactRole') != 'SCOPED_WORKFLOW_RUN'
            or any(not re.fullmatch(ID, str(data.get(k, ''))) for k in ('taskId', 'runId', 'productId'))
            or not data.get('requestReference') or not re.fullmatch('[0-9a-f]{40}', data.get('workflowSha', ''))):
        raise ValueError('Invalid run identity/request')
    execution = data.get('execution', {})
    from observation_time import utc
    utc(data['createdAtUtc'])
    if execution.get('mode') not in MODES or execution.get('state') not in {
            'NOT_STARTED', 'COMPLETED', 'PARTIAL', 'BLOCKED', 'FAILED'}:
        raise ValueError('Invalid execution mode/state')
    evidence = execution.get('evidence')
    if not isinstance(evidence, list) or bool(evidence) == (execution['state'] == 'NOT_STARTED'):
        raise ValueError('Execution state and actual supplied evidence disagree')
    for row in evidence:
        utc(row['recordedAtUtc'])
        item = safe_file(run, row['path'])
        if sha(item) != row.get('sha256'):
            raise ValueError('Execution evidence changed')
        supplied = read(item)
        if (supplied.get('source') not in MODES or supplied.get('outcome') not in {'SUCCEEDED','PARTIAL','BLOCKED','FAILED'}
                or not isinstance(supplied.get('notes'), str) or not supplied['notes'].strip()):
            raise ValueError('Execution evidence requires its actual source/outcome')
        if execution['mode'] != 'MIXED' and supplied['source'] != execution['mode']:
            raise ValueError('Evidence source differs from execution mode; use MIXED for combined work')
    if len({row['path'] for row in evidence}) != len(evidence):
        raise ValueError('Duplicate execution evidence')
    outcomes = [read(safe_file(run, row['path']))['outcome'] for row in evidence]
    expected = ('NOT_STARTED' if not outcomes else 'FAILED' if 'FAILED' in outcomes else
                'BLOCKED' if 'BLOCKED' in outcomes else 'PARTIAL' if 'PARTIAL' in outcomes else 'COMPLETED')
    if execution['state'] != expected:
        raise ValueError('Execution state differs from its recorded outcomes')
    if data.get('publicationState') != 'NOT_PERFORMED':
        raise ValueError('Run wrapper cannot claim publication completion')
    if data.get('deliveryState') not in {'NOT_PREPARED','STAGED_NOT_UPLOADED'}:
        raise ValueError('Run wrapper cannot claim upload/publication completion')
    if data['deliveryState']=='STAGED_NOT_UPLOADED':
        if sha(safe_file(run,'delivery-plan.json')) != data.get('deliveryPlanSha256'):
            raise ValueError('Released delivery plan changed')
        batches = delivery_batches(data)
        if (not isinstance(batches,list) or not batches
                or len({str(b.get('batchId','')).casefold() for b in batches})!=len(batches)
                or len({b.get('path') for b in batches})!=len(batches)):
            raise ValueError('Unique released delivery batches required')
        contract_sha = data.get('deliveryContractSha256')
        for index, batch in enumerate(batches):
            batch_id = batch.get('batchId','')
            if not isinstance(batch_id,str) or not re.fullmatch(ID,batch_id):
                raise ValueError('Exact safe delivery batch ID required')
            expected_path = 'delivery-plan.json' if index==0 else 'delivery-plans/'+batch_id+'.json'
            if batch.get('path')!=expected_path or sha(safe_file(run,expected_path))!=batch.get('sha256'):
                raise ValueError('Released delivery plan changed')
            plan = read(safe_file(run,expected_path)); scope = plan.get('productionScope',{})
            if (plan.get('artifactRole')!='DRIVE_UPLOAD_PLAN' or plan.get('runId')!=data['runId']
                    or plan.get('productId')!=data['productId'] or scope.get('workflowSha')!=data['workflowSha']
                    or scope.get('runId')!=data['runId']
                    or not re.fullmatch('[0-9a-f]{64}',scope.get('contractSha256',''))):
                raise ValueError('Released batch differs from its run/production contract')
            contract_sha = contract_sha or scope['contractSha256']
            if scope['contractSha256']!=contract_sha:
                raise ValueError('Delivery batches must share the same frozen contract')
    elif data.get('deliveryBatches') or data.get('deliveryContractSha256'):
        raise ValueError('Unstaged run cannot contain released delivery batches')
    if product is not None:
        from product_identity import product_id
        if data['productId'] != Path(product).name or product_id(read(Path(product)/'product-facts.json')) != data['productId']:
            raise ValueError('Run and current product identity differ')
    return data


def record_evidence(run, evidence_path, acceptance_reference=None):
    from delivery_privacy import screen_file
    data = validate(run)
    if data['deliveryState']!='NOT_PREPARED':
        raise ValueError('A released stage is immutable; record later execution in a successor run')
    supplied = read(evidence_path)
    if (supplied.get('source') not in MODES
            or supplied.get('outcome') not in {'SUCCEEDED','PARTIAL','BLOCKED','FAILED'}
            or not isinstance(supplied.get('notes'), str) or not supplied['notes'].strip()):
        raise ValueError('Supply actual sanitized source/outcome and substantive notes')
    if data['execution']['mode'] != 'MIXED' and supplied['source'] != data['execution']['mode']:
        raise ValueError('Evidence source differs from execution mode')
    screen = screen_file(evidence_path, serials_used=False)
    if screen['state'] != 'DELIVERY_PRIVACY_SCREEN_PASS':
        raise ValueError('Sanitize actual execution evidence before recording')
    relative = 'evidence/'+sha(evidence_path)+'.json'
    target = safe_file(run, relative)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.read_bytes() != Path(evidence_path).read_bytes():
        raise ValueError('Evidence collision')
    target.write_bytes(Path(evidence_path).read_bytes())
    rows = data['execution']['evidence']
    if not any(row['path'] == relative for row in rows):
        rows.append({'path': relative, 'sha256': sha(target), 'recordedAtUtc': now()})
    outcomes = [read(safe_file(run, row['path']))['outcome'] for row in rows]
    state = ('FAILED' if 'FAILED' in outcomes else 'BLOCKED' if 'BLOCKED' in outcomes
             else 'PARTIAL' if 'PARTIAL' in outcomes else 'COMPLETED')
    data['execution']['state'] = state
    if acceptance_reference:
        data['scopedAcceptanceReference'] = acceptance_reference
    write(Path(run)/'run-manifest.json', data)
    return validate(run)


def stage(run, product, contract_path, contract_sha256, files, batch_id=None):
    import production_guard
    import drive_delivery
    data = validate(run, product)
    if data['execution']['state'] not in {'COMPLETED','PARTIAL'}:
        raise ValueError('Record completed execution evidence before staging delivery')
    if data['execution']['state'] == 'PARTIAL' and not str(data.get('scopedAcceptanceReference', '')).strip():
        raise ValueError('Partial execution needs explicit scoped acceptance and retained unresolved work')
    contract = read(contract_path)
    if contract['runId'] != data['runId'] or contract['workflowSha'] != data['workflowSha']:
        raise ValueError('Run differs from its actual frozen production contract')
    batches = delivery_batches(data)
    if batches:
        first = read(safe_file(run,batches[0]['path']))
        if first['productionScope']['contractSha256']!=contract_sha256:
            raise ValueError('Delivery batches must share the same frozen contract')
    if batch_id is None:
        index = len(batches)+1
        existing = {b['batchId'].casefold() for b in batches}
        while ('batch-'+str(index).zfill(3)).casefold() in existing:
            index += 1
        batch_id = 'batch-'+str(index).zfill(3)
    if not isinstance(batch_id,str) or not re.fullmatch(ID,batch_id):
        raise ValueError('Exact safe delivery batch ID required')
    if any(b['batchId'].casefold()==batch_id.casefold() for b in batches):
        raise ValueError('Delivery batch ID already released; use a distinct batch ID')
    production = production_guard.verify(product, contract_path, contract_sha256, files)
    if production['mode'] == 'CONCEPT_ONLY':
        raise ValueError('Concepts cannot become canonical delivery through a run wrapper')
    plan = drive_delivery.plan(product, data['runId'], files)
    if {r['relativePath']: r['sha256'] for r in plan['files']} != production['files']:
        raise ValueError('Production bytes changed while staging')
    relative = 'delivery-plan.json' if not batches else 'delivery-plans/'+batch_id+'.json'
    plan.update(taskId=data['taskId'], executionMode=data['execution']['mode'], productionScope=production,
                batchId=batch_id, planRelativePath=relative)
    output = safe_file(run, relative)
    if output.exists():
        raise ValueError('Released delivery plan already exists; preserve it and use a new batch ID')
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x',encoding='utf-8',newline='\n') as handle:
        handle.write(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
    data['deliveryState'] = 'STAGED_NOT_UPLOADED'
    if not batches:
        data['deliveryPlanSha256'] = sha(output)
    data['deliveryContractSha256'] = contract_sha256
    data['deliveryBatches'] = [*batches, {'batchId':batch_id,'path':relative,'sha256':sha(output)}]
    write(Path(run)/'run-manifest.json', data)
    return plan


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['create','validate','record','stage'])
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--product', type=Path)
    parser.add_argument('--task-id')
    parser.add_argument('--run-id')
    parser.add_argument('--request-reference')
    parser.add_argument('--mode', choices=sorted(MODES), default='CONNECTOR')
    parser.add_argument('--workflow-sha')
    parser.add_argument('--evidence', type=Path)
    parser.add_argument('--acceptance-reference')
    parser.add_argument('--production-contract', type=Path)
    parser.add_argument('--contract-sha256')
    parser.add_argument('--file', action='append')
    parser.add_argument('--batch-id', help='Optional unique batch ID inside the same frozen run')
    args = parser.parse_args()
    try:
        if args.command == 'create':
            if not all((args.product,args.task_id,args.run_id,args.request_reference,args.workflow_sha)):
                parser.error('create requires product, task/run IDs, request reference and workflow SHA')
            result = create(args.run,args.product,args.task_id,args.run_id,args.request_reference,args.mode,args.workflow_sha)
        elif args.command == 'record':
            if not args.evidence: parser.error('record requires actual evidence')
            result = record_evidence(args.run,args.evidence,args.acceptance_reference)
        elif args.command == 'stage':
            if not all((args.product,args.production_contract,args.contract_sha256,args.file)):
                parser.error('stage requires product, frozen contract/digest and explicit files')
            result = stage(args.run,args.product,args.production_contract,args.contract_sha256,args.file,args.batch_id)
        else:
            result = validate(args.run,args.product)
        print(json.dumps({'state':result.get('state',result.get('deliveryState','RUN_STRUCTURE_CHECKED')),
                          'runId':result['runId'],'batchId':result.get('batchId'),
                          'planRelativePath':result.get('planRelativePath'),
                          'scope':'SUPPLIED_EVIDENCE_AND_LOCAL_STRUCTURE_ONLY'}))
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(1,str(error)+'\n')


if __name__ == '__main__':
    main()
