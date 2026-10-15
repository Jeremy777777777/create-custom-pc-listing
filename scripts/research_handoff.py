"""Cross-stage research checks and summaries; no source authentication or publication."""
from collections import Counter
from pathlib import Path
import math

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
        identity=product.get('identity',{})
        pid=identity.get('internalId') if isinstance(identity,dict) else None
        pid=pid or product.get('productId') or product.get('internalId')
        if pid is not None and pid!=product_id:
            raise ValueError('Product directory/ledger/product-facts identity differs')


def coverage_summary(data,projected):
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
            'factualReadinessAssessed':False}


def internal_storage_total(data):
    """Optional exact component evidence for a total differing from the base drive."""
    from product_metadata import CAPACITY_UNITS,selected_facts
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
    facts={f['id']:f for f in data['facts']};total_gb=0
    for fid in ids:
        fact=facts.get(fid)
        if fact is None: raise ValueError('Missing storage component fact: '+fid)
        meta=fact.get('evidence',{})
        if (fact['sheet']!='Product Details' or fact['configurationId']!=data['configurationId']
            or fact['status']!='VERIFIED' or fact['fact_scope']!='SOLD_BASE'
            or fact.get('applies_to_sold_configuration') is not True or not fact.get('transfer_basis','').strip()):
            raise ValueError('Storage components require verified applicable SOLD_BASE evidence')
        if fid==base['id']:
            unit=base_unit['final_value'] if base_unit and base_unit['status']=='VERIFIED' else None
        else:
            if meta.get('storage_medium') not in ('INTERNAL_SSD','INTERNAL_HDD'):
                raise ValueError('Storage component must identify internal SSD/HDD, not external/cloud/unknown media')
            unit=meta.get('capacity_unit')
        value=fact['final_value'];unit=str(unit).strip().casefold()
        if type(value) not in (int,float) or not math.isfinite(value) or value<=0 or unit not in ('gb','tb'):
            raise ValueError('Storage component requires positive numeric GB/TB capacity')
        total_gb+=value*CAPACITY_UNITS[unit]
    return total_gb
