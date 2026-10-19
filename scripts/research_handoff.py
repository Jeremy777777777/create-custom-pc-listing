"""Cross-stage research checks and summaries; no source authentication or publication."""
from collections import Counter
from pathlib import Path
import math
import re
import json
import hashlib

STATUSES=('VERIFIED','INPUT_UNVERIFIED','CONFLICT','TBD','SOURCE_UNAVAILABLE','NOT_APPLICABLE')


def check_product_location(workbook,product_id,product=None):
    path=Path(workbook).absolute()
    roots=[p for p in path.parents if p.name=='product generated photo']
    if not roots: return  # Explicit scratch/debug files have no canonical directory identity.
    relative=path.relative_to(roots[0])
    if len(relative.parts)!=2 or relative.parts[0]!=product_id:
        raise ValueError('Workbook product directory differs from ledger target or is not top-level')
    if product is not None:
        if not isinstance(product,dict): raise ValueError('Product facts must be an object for directory identity checking')
        from product_identity import product_id as resolve_product_id
        pid=resolve_product_id(product)
        if pid is not None and pid!=product_id:
            raise ValueError('Product directory/ledger/product-facts identity differs')


def coverage_summary(data,projected):
    from serial_research import serial_research_summary
    facts={f['id']:f for f in data['facts']}
    sheets={};unresolved=[]
    for (sheet,attribute),record in projected.items():
        counts=sheets.setdefault(sheet,Counter({s:0 for s in STATUSES}))
        counts[record['status']]+=1
        if record['status'] in ('VERIFIED','NOT_APPLICABLE'): continue
        evidence=facts[record['fact_id']].get('evidence',{})
        unresolved.append({'sheet':sheet,'attribute':attribute,'status':record['status'],
                           'reason':evidence.get('reason') or record['source'],
                           'nextAction':evidence.get('next_action') or None,
                           'owner':evidence.get('owner') or None})
    return {'sheets':{s:{'total':sum(c.values()),'statuses':dict(c)} for s,c in sheets.items()},
            'unresolvedFields':unresolved,
            'missingFollowUpMetadata':[{'sheet':r['sheet'],'attribute':r['attribute'],
                'missing':[key for key in ('nextAction','owner') if not isinstance(r[key],str) or not r[key].strip()]}
                for r in unresolved if any(not isinstance(r[k],str) or not r[k].strip() for k in ('nextAction','owner'))],
            'serialResearch':serial_research_summary(data),
            'factualReadinessAssessed':False}


def internal_storage_total(data):
    """Optional exact component evidence for a total differing from the base drive."""
    configuration=internal_storage_configuration(data)
    return configuration['totalGB'] if configuration else None


def storage_component_records(data):
    """Resolve the same explicit drive dependency graph for exports and image bindings."""
    from product_metadata import selected_facts
    selected=selected_facts(data)
    total=selected.get(('Product Details','Memory Storage Capacity'))
    if total is None: return None
    evidence=total.get('evidence',{})
    ids=evidence.get('storage_component_fact_ids')
    if ids is None: return None
    if evidence.get('storage_scope')!='INTERNAL_TOTAL' or not isinstance(ids,list) or not ids or any(not isinstance(i,str) for i in ids) or len(set(ids))!=len(ids):
        raise ValueError('Internal storage total requires distinct component fact IDs and INTERNAL_TOTAL scope')
    base=selected.get(('Product Details','Hard Disk Size'))
    base_unit=selected.get(('Product Details','Hard Disk Size Unit'))
    if base is None or base['id'] not in ids: raise ValueError('Storage total must include the selected base drive')
    facts={f['id']:f for f in data['facts']};components=[]
    for fid in ids:
        fact=facts.get(fid)
        if fact is None: raise ValueError('Missing storage component fact: '+fid)
        if (fact['sheet']!='Product Details' or fact['configurationId']!=data['configurationId']
            or fact['fact_scope']!='SOLD_BASE'):
            raise ValueError('Storage components require matching SOLD_BASE scope/configuration')
        quantity=fact.get('evidence',{}).get('part_quantity',1)
        if fact['status']=='VERIFIED' and (type(quantity) not in (int,float,str) or quantity not in (1,'1')):
            raise ValueError('Each storage component must describe one physical drive; split quantity-bearing BOM facts into per-drive facts')
        if fid!=base['id']:
            if ((fact['sheet'],fact['attribute']) in selected or
                re.fullmatch(r'(?:Secondary|Additional) internal drive capacity(?: .+)?',fact['attribute']) is None):
                raise ValueError('Storage component requires a dedicated drive-capacity fact, not RAM/VRAM/cache or another template field')
        components.append(fact)
    return {'baseId':base['id'],'baseUnit':base_unit,'components':components}


def storage_dependency_projection(data):
    """Bind referenced hardware/state/source metadata; exclude unrelated research notes."""
    records=storage_component_records(data)
    if records is None: return None
    from product_metadata import selected_facts,check_base_storage_medium
    check_base_storage_medium(selected_facts(data))
    keys=('id','sheet','attribute','status','final_value','fact_scope','configurationId','source',
          'applies_to_sold_configuration','transfer_basis')
    hardware_keys=('oem_part_number','part_description','part_quantity','drive_model','storage_interface',
                   'storage_form_factor','installation_basis','modification_evidence','replacement_check','capacity_basis')
    components=[]
    for fact in sorted(records['components'],key=lambda fact:fact['id']):
        meta=fact.get('evidence',{})
        components.append({**{key:fact[key] for key in keys if key in fact},
                           'storageMedium':meta.get('storage_medium'),
                           'capacityUnit':meta.get('capacity_unit'),
                           'hardwareEvidence':{key:meta[key] for key in hardware_keys if key in meta},
                           'isBaseDrive':fact['id']==records['baseId']})
    unit=records['baseUnit']
    return {'scope':'INTERNAL_TOTAL','components':components,
            'baseUnitFact':{key:unit[key] for key in keys if key in unit} if unit else None}


def internal_storage_configuration(data):
    """Return verified per-drive media/capacities as well as their internal total."""
    from capacity_units import STORAGE_CAPACITY_UNITS,check_nominal_storage_basis,scaled_capacity
    records=storage_component_records(data)
    if records is None: return None
    from product_metadata import selected_facts,check_base_storage_medium
    check_base_storage_medium(selected_facts(data))
    base_unit=records['baseUnit'];total_gb=0;devices=[]
    for fact in records['components']:
        check_nominal_storage_basis(fact)
        fid=fact['id'];meta=fact.get('evidence',{})
        if (fact['status']!='VERIFIED' or fact.get('applies_to_sold_configuration') is not True
            or not fact.get('transfer_basis','').strip()):
            raise ValueError('Storage components require verified applicable SOLD_BASE evidence')
        if fid==records['baseId']:
            unit=base_unit['final_value'] if base_unit and base_unit['status']=='VERIFIED' else None
            medium='ssd'  # Existing selectedBaseConfiguration.ssdGB is the base SSD contract.
        else:
            if meta.get('storage_medium') not in ('INTERNAL_SSD','INTERNAL_HDD'):
                raise ValueError('Storage component must identify internal SSD/HDD, not external/cloud/unknown media')
            unit=meta.get('capacity_unit')
            medium='ssd' if meta['storage_medium']=='INTERNAL_SSD' else 'hdd'
        value=fact['final_value'];unit=str(unit).strip().casefold()
        if type(value) not in (int,float) or not math.isfinite(value) or value<=0 or unit not in ('gb','tb'):
            raise ValueError('Storage component requires positive numeric GB/TB capacity')
        capacity=scaled_capacity(value,STORAGE_CAPACITY_UNITS[unit]);total_gb+=capacity
        devices.append({'factId':fid,'capacityGB':capacity,'medium':medium})
    return {'totalGB':total_gb,'devices':devices}


def check_research_summaries(root, product_id=None):
    """Read-only freshness checking of delivered summaries; never refresh stale conclusions."""
    from research_export import run,load_ledger
    from workbook_paths import current_product_artifacts,files_with_suffix,resolve_workbook_path
    root=Path(root);checked=0
    if product_id is not None and (Path(product_id).name != product_id or any(c in product_id for c in '/\\:')):
        raise ValueError('Summary scope requires a local product ID')
    paths = (files_with_suffix(root/'product generated photo'/product_id, '.research-summary.json')
             if product_id is not None else current_product_artifacts(root,'.research-summary.json'))
    for path in paths:
        summary=json.loads(path.read_text(encoding='utf-8-sig'))
        if not isinstance(summary,dict) or summary.get('artifactRole')!='RESEARCH_COVERAGE_SUMMARY':
            raise ValueError('Invalid research summary artifact role: '+str(path))
        ledger=path.parent/'research-ledger.json';data=load_ledger(ledger)
        check_product_location(path,data['productId'])
        if summary.get('productId')!=data['productId'] or summary.get('configurationId')!=data['configurationId']:
            raise ValueError('Research summary product/configuration is stale: '+str(path))
        name=summary.get('workbookFile')
        if name is not None:
            if not isinstance(name,str) or Path(name).name!=name or any(c in name for c in '/\\:') or not name.casefold().endswith('.xlsx'):
                raise ValueError('Research summary workbook must be a local XLSX filename')
            workbook=resolve_workbook_path(path.parent/name)
        else:
            # Preserve summaries from the first implementation when the old hash
            # identifies exactly one current workbook; never guess by filename.
            matches=[p for p in files_with_suffix(path.parent,'.xlsx') if hashlib.sha256(p.read_bytes()).hexdigest()==summary.get('workbookSha256')]
            if len(matches)!=1: raise ValueError('Research summary workbook binding is stale or ambiguous')
            workbook=matches[0]
        if summary.get('stage') not in ('RESEARCH_REVIEW','LISTING_DRAFT'):
            raise ValueError('Research summary requires a declared current stage')
        current=run(root/'assets/listing-workbook-template.xlsx',ledger,workbook,'draft',stage=summary['stage'])
        for key in ('workbookSha256','ledgerSha256','templateSha256','productFactsSha256','coverageSummary'):
            expected = current[key]
            if (key == 'coverageSummary' and 'serial_research' not in data
                    and isinstance(summary.get(key),dict) and 'serialResearch' not in summary[key]):
                expected = {k:v for k,v in expected.items() if k != 'serialResearch'}
            if key not in summary or json.dumps(summary[key],sort_keys=True)!=json.dumps(expected,sort_keys=True):
                raise ValueError('Research summary is stale or inconsistent: '+key+'; regenerate '+str(path))
        checked+=1
    return checked
