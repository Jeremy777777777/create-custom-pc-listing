"""Read-only metadata views and hardware research projections; never infer verification."""
import copy
import re

from capacity_units import capacity_units,STORAGE_FIELDS,check_nominal_storage_basis,scaled_capacity,CAPACITY_NUMBER,capacity_number
from product_identity import product_id
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
    for (sheet,field),fact in selected.items():
        if sheet=='Product Details' and field in STORAGE_FIELDS: check_nominal_storage_basis(fact)
    if product is not None:
        pid=product_id(product)
        if pid and pid!=ledger['productId']: raise ValueError('Image research belongs to another product')
        base=product.get('selectedBaseConfiguration',{})
        if isinstance(base,dict) and base.get('id') and base['id']!=ledger['configurationId']:
            raise ValueError('Image research belongs to another configuration')
        check_image_cache(selected,product)
    keys=('id','status','final_value','fact_scope','configurationId','source',
          'applies_to_sold_configuration','transfer_basis')
    projection={'productId':ledger['productId'],'configurationId':ledger['configurationId'],
            'hardware':[{'sheet':sheet,'attribute':field,**{k:fact[k] for k in keys if k in fact}}
                        for (sheet,field),fact in sorted(selected.items())
                        if sheet=='Product Details' and field not in NON_IMAGE_FIELDS]}
    from research_handoff import storage_dependency_projection
    dependencies=storage_dependency_projection(ledger)
    if dependencies is not None: projection['storageDependencies']=dependencies
    bases={field:fact['evidence']['capacity_basis'] for (sheet,field),fact in selected.items()
           if sheet=='Product Details' and field in STORAGE_FIELDS and 'capacity_basis' in fact.get('evidence',{})}
    if bases: projection['storageCapacityBasis']=bases
    return projection


def check_image_cache(selected,product):
    """Images require verified corresponding facts as well as consistent metadata."""
    check_metadata_consistency(selected,product,require_verified=True)


def check_metadata_consistency(selected,product,require_verified=False):
    """Reconcile every explicit cache representation; never overwrite a conflict."""
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
        if not require_verified and fact['status']!='VERIFIED': return
        if fact['status']!='VERIFIED' or normalizer(cached)!=normalizer(fact['final_value']):
            raise ValueError('Image cache/research conflict or unresolved selected fact: '+field)
    for field,value in [('Manufacturer',identity.get('oemBrand')),('Model Number',identity.get('oemModel')),
                        ('Operating System',product.get('os'))]: compare(field,value)
    compare('Resolution',display.get('resolution'),resolution_dimensions)
    compare('Display Refresh Rate in Hertz',display.get('refreshHz'),number)
    wireless=product.get('wireless')
    if isinstance(wireless,str): compare('Wireless Communication Standard',wireless,wifi)
    elif isinstance(wireless,dict): compare('Wireless Communication Standard',wireless.get('wifi'),wifi)
    if isinstance(product.get('internalStorage'),str) and base_storage_medium_conflict(product['internalStorage']):
        raise ValueError('Base storage medium conflicts with selected base SSD contract; reconcile internalStorage')
    for key,raw_key,field,unit_field in [('ramGB','ram','RAM Memory Installed','RAM Memory Installed Size Unit'),
                                        ('ssdGB','internalStorage','Hard Disk Size','Hard Disk Size Unit'),
                                        ('vramGB','gpu','Graphics Ram Size','Graphics Ram Size Unit')]:
        units=capacity_units(field)
        cached_values=[] if base.get(key) is None else [base[key]]
        if isinstance(product.get(raw_key),str):
            match=re.search(r'(?<![\w.,])('+CAPACITY_NUMBER+r')\s*(GiB|MiB|TiB|GB|MB|TB)\b',product[raw_key],re.I)
            if match and key=='ssdGB' and 'i' in match[2].casefold():
                raise ValueError('Image storage cache has binary/system capacity; reconcile nominal drive evidence')
            if match: cached_values.append(scaled_capacity(capacity_number(match[1]),units[match[2].casefold().replace('i','')]))
        fact,unit=selected.get(('Product Details',field)),selected.get(('Product Details',unit_field))
        if not cached_values or fact is None: continue
        if not require_verified and fact['status']!='VERIFIED': continue
        if field in STORAGE_FIELDS: check_nominal_storage_basis(fact)
        if fact['status']!='VERIFIED' or unit is None or unit['status']!='VERIFIED' or type(fact['final_value']) not in (int,float):
            raise ValueError('Metadata cache/research capacity differs in value/type or is unresolved: '+field)
        measure=str(unit['final_value']).strip().casefold()
        if measure not in units or any(type(cached) not in (int,float) or cached!=scaled_capacity(fact['final_value'],units[measure]) for cached in cached_values):
            raise ValueError('Image cache/research capacity conflict: '+field)
    aliases=cpu_aliases(identity)
    cpus=[cpu for cpu in (identity.get('cpu'),product.get('cpu')) if isinstance(cpu,str) and cpu.strip()]
    if not cpus and 'cpuModelNumber' in identity:
        model=selected.get(('Product Details','CPU Model Number'))
        if model and model['status']=='VERIFIED':
            canonical=' '.join(str(fact['final_value']) for field in ('CPU Model Manufacturer','CPU Model','CPU Model Number')
                               if (fact:=selected.get(('Product Details',field))) and fact['status']=='VERIFIED')
            if not cpu_field_matches('CPU Model Number',identity['cpuModelNumber'],canonical,aliases):
                raise ValueError('Exact CPU model cache conflicts with selected CPU evidence')
        elif model and require_verified:
            raise ValueError('Explicit CPU model cache has unresolved selected CPU evidence')
    for cpu in cpus:
        if 'cpuModelNumber' in identity and not cpu_field_matches('CPU Model Number',identity['cpuModelNumber'],cpu,aliases):
            raise ValueError('Exact CPU model cache conflicts with canonical CPU identity')
        for field in ('CPU Model Number','CPU Model','CPU Model Manufacturer'):
            fact=selected.get(('Product Details',field))
            if fact is None or not require_verified and fact['status']!='VERIFIED': continue
            if fact['status']!='VERIFIED' or not cpu_field_matches(field,fact['final_value'],cpu,aliases):
                raise ValueError('Exact CPU model/family/manufacturer cache/research conflict: '+field)
    check_base_storage_medium(selected)


def cpu_text(value):
    value=re.sub(r'\((?:r|tm)\)|[®™©]',' ',str(value),flags=re.I)
    return ' '.join(re.findall(r'[a-z0-9]+',value.casefold()))


def cpu_aliases(identity):
    aliases=identity.get('cpuFieldAliases',{})
    if not isinstance(aliases,dict) or any(field not in ('CPU Model','CPU Model Number','CPU Model Manufacturer')
        or not isinstance(names,list) or any(not isinstance(name,str) or not cpu_text(name) for name in names)
        for field,names in aliases.items()):
        raise ValueError('CPU aliases require supported field names and lists of verified text equivalents')
    return aliases


def cpu_field_matches(field,value,cpu,aliases):
    """One CPU field rule for metadata, listing copy attributes and image caches."""
    if not isinstance(value,str) or not cpu_text(value): return False
    model=cpu_text(exact_cpu_model(cpu)) if field=='CPU Model Number' else None
    normalized=cpu_text(value)
    if normalized in [cpu_text(alias) for alias in aliases.get(field,[])]: return True
    if ' '+normalized+' ' not in ' '+cpu_text(cpu)+' ': return False
    return field!='CPU Model Number' or ' '+model+' ' in ' '+normalized+' '


def check_base_storage_medium(selected):
    """The established base SSD contract cannot coexist with an explicit HDD claim."""
    base=selected.get(('Product Details','Hard Disk Size'))
    if base and base['status']=='VERIFIED' and base.get('evidence',{}).get('storage_medium') in ('INTERNAL_HDD','EMMC','EXTERNAL_SSD','EXTERNAL_HDD'):
        raise ValueError('Base storage medium conflicts with selected base SSD contract')
    fact=selected.get(('Product Details','Hard Disk Description'))
    if fact is None or fact['status']!='VERIFIED': return
    if base_storage_medium_conflict(fact['final_value']):
        raise ValueError('Base storage medium conflicts with selected base SSD contract; reconcile Hard Disk Description')


def base_storage_medium_conflict(value):
    value=cpu_text(value)
    return bool(re.search(r'\b(?:hdd|hard disk drive|hybrid|sshd|emmc)\b',value)
                and not re.search(r'\b(?:ssd|nvme|solid state drive)\b',value))


def listing_view(raw,ledger):
    """Adapt flat image-only records using verified selected facts, keeping raw bytes intact."""
    if not isinstance(raw,dict): raise ValueError('PRODUCT_METADATA_REQUIRED: product-facts must be an object')
    identity=raw.get('identity',{})
    if not isinstance(identity,(dict,str)): raise ValueError('PRODUCT_METADATA_REQUIRED: identity must be an object or legacy display name')
    view=copy.deepcopy(raw);view['identity']=copy.deepcopy(identity) if isinstance(identity,dict) else {}
    identity=view['identity']
    selected=selected_facts(ledger);provenance={};missing=[]
    pid=product_id(raw)
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
        units=capacity_units(field)
        if field in STORAGE_FIELDS:
            fact=selected.get(('Product Details',field))
            if fact: check_nominal_storage_basis(fact)
        normalized=None
        if type(value) in (int,float) and isinstance(unit,str) and unit.strip().casefold() in units:
            normalized=scaled_capacity(value,units[unit.strip().casefold()])
        if key not in base and normalized is not None: base[key]=normalized
        elif normalized is not None and (type(base.get(key)) not in (int,float) or base[key]!=normalized):
            raise ValueError('Product facts and selected research disagree: '+field)
        if type(base.get(key)) not in (int,float) or base[key]<=0: missing.append('selectedBaseConfiguration.'+key)
    if missing: raise ValueError('PRODUCT_METADATA_REQUIRED: '+ '; '.join(missing))
    check_metadata_consistency(selected,view)
    return view,{'format':'STRUCTURED' if isinstance(raw.get('identity'),dict) else 'LEGACY_READ_ONLY_ADAPTER',
                 'derivedFromSelectedFacts':provenance,'rawProductFactsRewritten':False}


def exact_cpu_model(cpu):
    """Extract a model anchor from the supplied CPU identity, never from its family field."""
    text=re.sub(r'\([^)]*\)|[®™©]',' ',cpu)
    apple=re.search(r'\bM\d+\s*(?:Pro|Max|Ultra)?\b',text,re.I)
    if apple: return apple.group().strip()
    qualcomm=re.search(r'\bX[12][A-Z]-\d{2}-\d{3}\b',text,re.I)
    if qualcomm: return qualcomm.group()
    # Specifications appended to a CPU name are not model numbers. Keep an
    # ambiguous identity explicit rather than choosing its last number.
    text=re.sub(r'\b\d+(?:\.\d+)?[\s-]*(?:w(?:atts)?|[mg]hz|[kmgt]b|cores?|threads?)\b',' ',text,flags=re.I)
    tokens=[token for token in re.findall(r'\b[a-z]*\d+[a-z0-9]*\b',text,re.I)
            if len(re.sub(r'\D','',token))>=2]
    tokens=list({token.casefold():token for token in tokens}.values())
    if len(tokens)!=1:
        raise ValueError('Exact CPU model metadata required; family/manufacturer is insufficient')
    return tokens[0]


def resolution_dimensions(value):
    """Normalize only the supported width/height spelling, never guess a resolution."""
    match=re.fullmatch(r'\s*([1-9]\d*)\s*[x×]\s*([1-9]\d*)\s*(?:pixels|px)?\s*',str(value),re.I)
    if not match: raise ValueError('Resolution must contain positive width x height')
    return tuple(map(int,match.groups()))
