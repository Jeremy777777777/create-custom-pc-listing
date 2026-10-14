"""Read-only metadata views and hardware research projections; never infer verification."""
import copy
import re

CAPACITY_UNITS={'kb':1/1024**2,'mb':1/1024,'gb':1,'tb':1024}
NON_IMAGE_FIELDS={
    'Customizations','Item Name','Bullet Point','Product Description','Generic Keyword',
    'External Product ID','External Product ID Type','Item Package Quantity','Number of Items',
    'Unit Count','Unit Count Type','Government Contract Name and Number',
}


def selected_facts(ledger):
    from research_export import validate_ledger
    facts=validate_ledger(ledger)
    return {(field['sheet'],field['attribute']):facts[field['selected_fact']] for field in ledger['fields']}


def hardware_projection(ledger,product=None):
    """Bind selected hardware facts, not offer values, research notes or factory alternatives."""
    selected=selected_facts(ledger)
    if product is not None:
        identity=product.get('identity',{})
        pid=identity.get('internalId') if isinstance(identity,dict) else None
        pid=pid or product.get('productId') or product.get('internalId')
        if pid and pid!=ledger['productId']: raise ValueError('Image research belongs to another product')
        base=product.get('selectedBaseConfiguration',{})
        if isinstance(base,dict) and base.get('id') and base['id']!=ledger['configurationId']:
            raise ValueError('Image research belongs to another configuration')
        check_image_cache(selected,product)
    keys=('id','status','final_value','fact_scope','configurationId','source',
          'applies_to_sold_configuration','transfer_basis')
    return {'productId':ledger['productId'],'configurationId':ledger['configurationId'],
            'hardware':[{'sheet':sheet,'attribute':field,**{k:fact[k] for k in keys if k in fact}}
                        for (sheet,field),fact in sorted(selected.items())
                        if sheet=='Product Details' and field not in NON_IMAGE_FIELDS]}


def check_image_cache(selected,product):
    """Known cache fields cannot contradict the authoritative selected hardware facts."""
    identity=product.get('identity',{});identity=identity if isinstance(identity,dict) else {}
    base=product.get('selectedBaseConfiguration',{});base=base if isinstance(base,dict) else {}
    display=product.get('display',{});display=display if isinstance(display,dict) else {}
    def text(value): return ''.join(re.findall(r'[a-z0-9]+',str(value).casefold()))
    def wifi(value):
        found=re.search(r'wi[\s-]?fi\s*(\d+e?)',str(value),re.I)
        return 'wifi'+found[1].casefold() if found else text(value)
    def number(value):
        if type(value) not in (int,float): raise ValueError('Image research/cache requires a numeric value')
        return value
    def compare(field,cached,normalizer=text):
        fact=selected.get(('Product Details',field))
        if fact is None or cached is None: return
        if fact['status']!='VERIFIED' or normalizer(cached)!=normalizer(fact['final_value']):
            raise ValueError('Image cache/research conflict or unresolved selected fact: '+field)
    for field,value in [('Manufacturer',identity.get('oemBrand')),('Model Number',identity.get('oemModel')),
                        ('Operating System',product.get('os')),('Resolution',display.get('resolution'))]: compare(field,value)
    compare('Display Refresh Rate in Hertz',display.get('refreshHz'),number)
    wireless=product.get('wireless')
    if isinstance(wireless,str): compare('Wireless Communication Standard',wireless,wifi)
    elif isinstance(wireless,dict): compare('Wireless Communication Standard',wireless.get('wifi'),wifi)
    for key,raw_key,field,unit_field in [('ramGB','ram','RAM Memory Installed','RAM Memory Installed Size Unit'),
                                        ('ssdGB','internalStorage','Hard Disk Size','Hard Disk Size Unit'),
                                        ('vramGB','gpu','Graphics Ram Size','Graphics Ram Size Unit')]:
        cached=base.get(key)
        if cached is None and isinstance(product.get(raw_key),str):
            match=re.search(r'(\d+(?:\.\d+)?)\s*(GB|MB|TB)\b',product[raw_key],re.I)
            if match: cached=float(match[1])*CAPACITY_UNITS[match[2].casefold()]
        fact,unit=selected.get(('Product Details',field)),selected.get(('Product Details',unit_field))
        if cached is None or fact is None: continue
        if fact['status']!='VERIFIED' or unit is None or unit['status']!='VERIFIED' or type(fact['final_value']) not in (int,float):
            raise ValueError('Image cache/research capacity unresolved: '+field)
        measure=str(unit['final_value']).strip().casefold()
        if type(cached) not in (int,float) or measure not in CAPACITY_UNITS or cached!=fact['final_value']*CAPACITY_UNITS[measure]:
            raise ValueError('Image cache/research capacity conflict: '+field)
    cpu=identity.get('cpu') or product.get('cpu')
    if isinstance(cpu,str):
        fact=selected.get(('Product Details','CPU Model Number'))
        def words(value):
            value=re.sub(r'\((?:r|tm)\)|[®™©]',' ',str(value),flags=re.I)
            return ' '+' '.join(re.findall(r'[a-z0-9]+',value.casefold()))+' '
        if fact is not None and (fact['status']!='VERIFIED' or words(exact_cpu_model(cpu)) not in words(fact['final_value'])):
            raise ValueError('Image cache/research exact CPU conflict')
        for field in ('CPU Model','CPU Model Manufacturer'):
            fact=selected.get(('Product Details',field))
            if fact is not None and (fact['status']!='VERIFIED' or words(fact['final_value']) not in words(cpu)):
                raise ValueError('Image cache/research CPU family/manufacturer conflict: '+field)


def listing_view(raw,ledger):
    """Adapt flat image-only records using verified selected facts, keeping raw bytes intact."""
    if not isinstance(raw,dict): raise ValueError('PRODUCT_METADATA_REQUIRED: product-facts must be an object')
    identity=raw.get('identity',{})
    if not isinstance(identity,(dict,str)): raise ValueError('PRODUCT_METADATA_REQUIRED: identity must be an object or legacy display name')
    view=copy.deepcopy(raw);view['identity']=copy.deepcopy(identity) if isinstance(identity,dict) else {}
    identity=view['identity']
    selected=selected_facts(ledger);provenance={};missing=[]
    pid=identity.get('internalId') or raw.get('productId') or raw.get('internalId')
    if not isinstance(pid,str) or not pid.strip(): missing.append('identity.internalId / productId')
    elif pid!=ledger['productId']: raise ValueError('Product facts identity differs from ledger product')
    else: identity['internalId']=pid
    base=raw.get('selectedBaseConfiguration',{})
    if not isinstance(base,dict): raise ValueError('PRODUCT_METADATA_REQUIRED: selectedBaseConfiguration must be an object')
    view['selectedBaseConfiguration']=base=copy.deepcopy(base)
    if base.get('id') and base['id']!=ledger['configurationId']: raise ValueError('Product facts configuration differs from ledger')
    if pid==ledger['productId']: base.setdefault('id',ledger['configurationId'])
    def verified(field):
        fact=selected.get(('Product Details',field))
        if fact and fact['status']=='VERIFIED':
            provenance[field]=fact['id'];return fact['final_value']
        return None
    for key,field in [('oemBrand','Manufacturer'),('oemModel','Model Number')]:
        value=verified(field)
        if not identity.get(key) and isinstance(value,str): identity[key]=value
        elif value is not None and str(identity.get(key,'')).strip().casefold()!=str(value).strip().casefold():
            raise ValueError('Product facts and selected research disagree: '+field)
        if not isinstance(identity.get(key),str) or not identity[key].strip(): missing.append('identity.'+key+' (verified '+field+')')
    cpu=identity.get('cpu') or raw.get('cpu')
    model=verified('CPU Model Number')
    if not cpu and isinstance(model,str):
        cpu=' '.join(str(v) for v in (verified('CPU Model Manufacturer'),verified('CPU Model'),model) if v)
    if isinstance(cpu,str) and cpu.strip(): identity['cpu']=cpu
    else: missing.append('identity.cpu (verified exact CPU)')
    # A ledger value is not allowed to redefine the exact model independently of cpu.
    if isinstance(model,str): identity.setdefault('cpuModelNumber',model)
    for key,field,unit_field in [('ramGB','RAM Memory Installed','RAM Memory Installed Size Unit'),
                                ('ssdGB','Hard Disk Size','Hard Disk Size Unit')]:
        value,unit=verified(field),verified(unit_field)
        normalized=None
        if type(value) in (int,float) and isinstance(unit,str) and unit.strip().casefold() in CAPACITY_UNITS:
            normalized=value*CAPACITY_UNITS[unit.strip().casefold()]
        if key not in base and normalized is not None: base[key]=normalized
        elif normalized is not None and (type(base.get(key)) not in (int,float) or base[key]!=normalized):
            raise ValueError('Product facts and selected research disagree: '+field)
        if type(base.get(key)) not in (int,float) or base[key]<=0: missing.append('selectedBaseConfiguration.'+key)
    if missing: raise ValueError('PRODUCT_METADATA_REQUIRED: '+ '; '.join(missing))
    return view,{'format':'STRUCTURED' if isinstance(raw.get('identity'),dict) else 'LEGACY_READ_ONLY_ADAPTER',
                 'derivedFromSelectedFacts':provenance,'rawProductFactsRewritten':False}


def exact_cpu_model(cpu):
    """Extract a model anchor from the supplied CPU identity, never from its family field."""
    text=re.sub(r'\([^)]*\)|[®™©]',' ',cpu)
    apple=re.search(r'\bM\d+\s*(?:Pro|Max|Ultra)?\b',text,re.I)
    if apple: return apple.group().strip()
    tokens=re.findall(r'\b[a-z]*\d+[a-z0-9]*\b',text,re.I)
    qualcomm=re.search(r'\bX[12][A-Z]-\d{2}-\d{3}\b',text,re.I)
    if qualcomm: return qualcomm.group()
    if not tokens or len(re.sub(r'\D','',tokens[-1]))<2:
        raise ValueError('Exact CPU model metadata required; family/manufacturer is insufficient')
    return tokens[-1]
