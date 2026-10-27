"""Conspicuously synthetic audit records, restricted to the TEST-PC fixture.

These are unit-test inputs, never browser observations for a real product.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import workbook_reference_audit as contract


def bind_selections(data):
    """TEST-PC uses observed notebook controls to exercise projection mechanics.

    This synthetic fixture context is not an assertion about any real Dell unit.
    Schema-specific mismatch tests own their deliberately incompatible values.
    """
    if data['productId'] != 'TEST-PC':
        raise ValueError('Synthetic helper is TEST-PC only')
    from amazon_selection import read_catalog, CONTEXT_KEYS
    catalog, sha = read_catalog()
    context = next(c for c in catalog['contexts'] if c['productType'] == 'NOTEBOOK_COMPUTER')
    controls = {(c['sheet'], c['attribute']): c for c in context['controls'] if c.get('attribute')}
    fields = []
    for mapping in data['fields']:
        key = (mapping['sheet'], mapping['attribute'])
        control = controls.get(key)
        fields.append({'sheet': key[0], 'attribute': key[1],
            **({'decision': 'DIRECT', 'path': control['path']} if control else
               {'decision': 'UNOBSERVED', 'reason': 'Synthetic fixture field not displayed in observed context'})})
    data['amazon_selection'] = {'schemaVersion': 1, 'catalogSha256': sha,
        'context': {k: context[k] for k in CONTEXT_KEYS}, 'fields': fields}
    return data


def write_audit(ledger):
    ledger=Path(ledger);raw=ledger.read_bytes();data=json.loads(raw.decode('utf-8-sig'))
    if data['productId']!='TEST-PC':raise ValueError('Synthetic audit helper is TEST-PC only')
    facts=contract.selected(data);references={};reviews=[]
    for fact in facts:
        sources=contract.urls(fact['source'])+contract.urls(fact.get('value_candidate_source'))
        sources+=contract.urls(fact.get('evidence',{}).get('fcc_official_url')) if fact['attribute']=='FCC ID' else []
        for url in sources:
            references[url]={'url':url,'resolvedUrl':url,'observedAtUtc':datetime.now(timezone.utc).isoformat(),
                'method':'BROWSER','outcome':'OPENED','title':'SYNTHETIC UNIT TEST PAGE',
                'evidence':'Synthetic test input; no real browser lookup was performed.',
                'limitations':'SYNTHETIC TEST ONLY, NOT PRODUCT RESEARCH'}
        reviews.append({'factId':fact['id'],'factSha256':contract.digest(fact),'primaryUrl':sources[0] if sources else None,
            'basis':'Synthetic fixture disposition','supportScope':'DISPOSITION'})
    catalog_reference=data.get('amazon_selection',{}).get('catalogReference')
    if catalog_reference:
        references[catalog_reference]={'url':catalog_reference,'resolvedUrl':catalog_reference,
            'observedAtUtc':datetime.now(timezone.utc).isoformat(),'method':'BROWSER','outcome':'OPENED',
            'title':'SYNTHETIC UI OPTIONS PAGE','evidence':'Synthetic TEST-PC input; no real lookup.',
            'limitations':'SYNTHETIC TEST ONLY, NOT PRODUCT RESEARCH'}
    audit={'schemaVersion':1,'productId':data['productId'],'configurationId':data['configurationId'],
        'ledgerSha256':hashlib.sha256(raw).hexdigest(),'references':list(references.values()),'fieldReviews':reviews}
    (ledger.parent/'reference-audit.json').write_text(json.dumps(audit),encoding='utf-8')
    return audit
