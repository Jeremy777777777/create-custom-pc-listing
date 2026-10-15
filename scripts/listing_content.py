"""Formal export content checks; drafts keep unresolved evidence without invented values."""
import math
import re
from product_metadata import exact_cpu_model

CAPACITY_PAIRS = {
    'RAM Memory Installed': 'RAM Memory Installed Size Unit',
    'Computer Memory Size': 'Computer Memory Size Unit',
    'RAM Memory Maximum Size': 'RAM Memory Maximum Size Unit',
    'Hard Disk Size': 'Hard Disk Size Unit',
    'Memory Storage Capacity': 'Memory Storage Capacity Unit',
    'Cache Memory Installed Size': 'Cache Memory Installed Size Unit',
    'Flash Memory Installed Size': 'Flash Memory Installed Size Unit',
    'Graphics Ram Size': 'Graphics Ram Size Unit',
}
SPEED_PAIRS = {'Memory Speed':'Memory Speed Unit', 'Memory Clock Speed':'Memory Clock Speed Unit',
               'CPU Base Speed':'CPU Base Speed Unit', 'CPU Model Speed Maximum':'CPU Model Speed Maximum Unit'}
CAPACITY_UNITS = {'kb':1/1024**2, 'mb':1/1024, 'gb':1, 'tb':1024}
SPEED_UNITS = {'mhz':1, 'ghz':1000}
FIELD_UNITS = {
    'RAM Memory Installed': {'gb','mb'}, 'Hard Disk Size': {'gb','tb'},
    'Memory Speed': {'mhz'}, 'Memory Clock Speed': {'mhz','ghz'},
    'CPU Base Speed': {'mhz','ghz'}, 'CPU Model Speed Maximum': {'mhz','ghz'},
}
# Explicit current-template rules. Wording in Definition is not a type declaration.
COUNT_FIELDS = {
    'Product Details': {'Number of Items','Item Package Quantity','Processor Count','Model Year',
        'Total HDMI Ports','Total Thunderbolt Ports','Total USB 2.0 Ports','Total USB 3.0 Ports',
        'Total USB Ports','USB Port Quantity','Number of USB ports','Audio Connector Quantity',
        'Supported Monitor Maximum Quantity','RAM Memory Slot Total Count','HDMI Port Quantity',
        'Number of HDMI ports','Available M2 Slot Count'},
    'Offer': {'Maximum Order Quantity'},
    'Safety&Compliance': {'Number of Batteries','Number of Lithium-ion Cells'},
}
NUMERIC_FIELDS = {
    'Product Details': {'Voltage','Memory Storage Capacity','Computer Memory Size','CPU Base Speed',
                       'Flash Memory Installed Size','Item Weight','Unit Count'},
    'Offer': {'Item Package Length','Item Package Width','Item Package Height'},
    'Safety&Compliance': {'Battery Charge Time','Battery Weight'},
}


def cpu_text(value):
    value=re.sub(r'\((?:r|tm)\)|[®™©]', ' ', str(value), flags=re.I)
    return ' '.join(re.findall(r'[a-z0-9]+',value.casefold()))


def cpu_claims(text):
    """Recognize explicit CPU identities; ordinary numbers/GPU models are not CPU claims."""
    text=cpu_text(re.sub(r'<[^>]+>',' ',text))
    patterns=(
        r'\b(?:intel )?(?:core (?:ultra [3579]|i[3579])|processor|celeron|pentium)(?: processor)? (?:\d{3,5}[a-z]{0,4}|[nug]\d{2,4})\b',
        r'\b(?:amd )?ryzen (?:ai )?[3579] (?:hx |pro )?\d{3,5}[a-z]{0,4}\b',
        r'\b(?:apple )?m\d+ (?:pro|max|ultra)\b|\bapple m\d+\b',
        r'\b(?:qualcomm )?snapdragon x\d[a-z] \d{2} \d{3}\b',
        r'\b(?:cpu|processor) (\d{3,5}[a-z]{0,4}|[nug]\d{2,4})\b',
    )
    for pattern in patterns:
        for match in re.finditer(pattern,text):
            yield match[1] if match.lastindex else match[0]


def capacity_mentions(text):
    """Associate each capacity once, within its clause; distinguish RAM/VRAM/cache/storage."""
    amount=r'(?P<amount>\d+(?:\.\d+)?)\s*(?P<unit>GB|TB|MB)\b'
    labels=r'\b(?:RAM|Memory|LPDDR\dX?|DDR\dX?|GDDR\dX?|VRAM|GPU|Graphics|Video|Cache|SSD|NVMe|HDD|Storage|Solid[ -]State[ -]Drive)\b'
    def category(fragment):
        if re.search(r'\b(?:GDDR\dX?|VRAM|GPU|Graphics|Video)\b',fragment,re.I): return 'vram'
        if re.search(r'\bCache\b',fragment,re.I): return 'cache'
        if re.search(r'\b(?:SSD|NVMe|HDD|Storage|Solid[ -]State[ -]Drive)\b',fragment,re.I): return 'ssd'
        return 'ram'
    gap_words=r'[\s-]*(?:(?:PCIe|Gen\d|M\.2|\d{4}|\d+(?:\.\d+)?|card|system|installed|internal|SO-DIMM|SDRAM|L[123])[\s-]*)*'
    def cluster(matches,fragment,reverse=False):
        if not matches: return []
        ordered=list(reversed(matches)) if reverse else matches
        result=[ordered[0]]
        for item in ordered[1:]:
            gap=fragment[item.end():result[-1].start()] if reverse else fragment[result[-1].end():item.start()]
            if re.fullmatch(gap_words,gap,re.I) is None: break
            result.append(item)
        return list(reversed(result)) if reverse else result
    for clause in re.split(r';|\n|<br\s*/?>|(?<!\d),(?!\d)|\|',text,flags=re.I):
        capacities=list(re.finditer(amount,clause,re.I));assigned=set()
        for index,match in enumerate(capacities):
            left=capacities[index-1].end() if index else 0
            right=capacities[index+1].start() if index+1<len(capacities) else len(clause)
            preceding=[m for m in re.finditer(labels,clause[left:match.start()],re.I) if left+m.start() not in assigned]
            following=list(re.finditer(labels,clause[match.end():right],re.I))
            preceding=cluster(preceding,clause[left:match.start()],True)
            following=cluster(following,clause[match.end():right])
            # Reverse wording requires a directly preceding label (RAM: 16GB),
            # not an unrelated noun elsewhere in the sentence.
            reverse=preceding and re.fullmatch(r'[\s:=\-]*',clause[left+preceding[-1].end():match.start()]) is not None
            if reverse:
                start=left+preceding[0].start();fragment=clause[start:match.start()]
                assigned.update(left+m.start() for m in preceding)
                # Consume same-role suffix labels too (RAM: 16GB DDR5), but
                # leave a different next role (SSD:) available for its amount.
                for label in following:
                    if category(label[0])!=category(fragment): break
                    assigned.add(match.end()+label.start())
            elif following:
                start=match.end()+following[0].start();fragment=clause[start:match.end()+following[-1].end()]
                assigned.update(match.end()+m.start() for m in following)
            else: continue
            yield float(match['amount'])*CAPACITY_UNITS[match['unit'].casefold()],category(fragment)


def base_spec_fragments(product):
    """Use these verified-base fragments when composing new listing copy."""
    base=product['selectedBaseConfiguration']
    for key in ('ramGB','ssdGB'):
        if type(base.get(key)) not in (int,float) or not math.isfinite(base[key]) or base[key]<=0:
            raise ValueError('Verified positive base capacity required: '+key)
    return {'ram':f"{base['ramGB']:g}GB RAM",'ssd':f"{base['ssdGB']:g}GB SSD"}


def validate_listing(projected, product, definitions=None,storage_total_gb=None):
    values = {field:record['value'] for (sheet,field),record in projected.items() if sheet=='Product Details'}
    for key,record in projected.items():
        value=record['value']
        if value is None: continue
        if key[1] in COUNT_FIELDS.get(key[0],set()):
            if type(value) not in (int,float) or not math.isfinite(value) or value<0:
                raise ValueError('Expected a nonnegative numeric count: '+str(key))
            if int(value)!=value: raise ValueError('Expected an integer count: '+str(key))
        elif key[1] in NUMERIC_FIELDS.get(key[0],set()):
            if type(value) not in (int,float) or not math.isfinite(value) or value<0:
                raise ValueError('Expected a nonnegative numeric value: '+str(key))
    resolution=values.get('Resolution')
    if resolution is not None and (not isinstance(resolution,str) or re.fullmatch(r'\s*[1-9]\d*\s*[x×]\s*[1-9]\d*\s*(?:pixels|px)?\s*',resolution,re.I) is None):
        raise ValueError('Resolution must contain positive width x height')
    refresh=values.get('Display Refresh Rate in Hertz')
    if refresh is not None and (type(refresh) not in (int,float) or not math.isfinite(refresh) or refresh<=0):
        raise ValueError('Display refresh rate must be positive; fractional Hz is permitted')
    for field,unit in values.items():
        if field.endswith(' Unit') and field[:-5] in values:
            value=values[field[:-5]]
            if (unit is None)!=(value is None): raise ValueError('Numeric field/unit applicability differs: '+field)
    def required(field):
        record=projected.get(('Product Details',field),{})
        value=record.get('value')
        if record.get('status')!='VERIFIED' or value is None or isinstance(value,str) and not value.strip():
            raise ValueError('Required sold PC field is not verified: '+field)
        return value
    for field in ('Item Name','Model Number','Model Name','Manufacturer','CPU Model','CPU Model Number',
                  'RAM Memory Installed','RAM Memory Installed Size Unit','Hard Disk Size','Hard Disk Size Unit','Operating System'):
        required(field)
    identity=product['identity']; base=product['selectedBaseConfiguration']
    for field in ('Model Number','Model Name','Manufacturer','CPU Model','CPU Model Number','Operating System'):
        if not isinstance(values[field],str): raise ValueError('Expected literal text: '+field)
    title=required('Item Name')
    if not isinstance(title,str) or len(title)>200 or not title.startswith('MegaPC Custom ') or not title.endswith('Win 11 Pro') or 'Created Using ' not in title:
        raise ValueError('Title must follow MegaPC Custom / Created Using / Win 11 Pro and 200-character policy')
    for token in (identity.get('oemBrand'),identity.get('oemModel')):
        if not isinstance(token,str) or not token.strip() or token.casefold() not in title.casefold():
            raise ValueError('Title must identify the verified OEM brand and model')
    if values['Manufacturer'].casefold()!=identity['oemBrand'].casefold() or values['Model Number'].casefold()!=identity['oemModel'].casefold():
        raise ValueError('Workbook OEM identity differs from product facts')
    if values['Operating System'].strip().casefold() not in ('windows 11 pro','microsoft windows 11 pro','win 11 pro'):
        raise ValueError('Sold OS must follow confirmed Windows 11 Pro policy')
    bullets=required('Bullet Point')
    paragraphs=bullets.split('\n\n') if isinstance(bullets,str) else []
    if len(paragraphs)!=5 or any(not p.strip() or '\n' in p for p in paragraphs):
        raise ValueError('Listing needs exactly five bullet paragraphs separated by one blank line')
    normalized={}
    for field,unit_field in {**CAPACITY_PAIRS,**SPEED_PAIRS}.items():
        value,unit=values.get(field),values.get(unit_field)
        if value is None and unit is None: continue
        if type(value) not in (int,float) or not math.isfinite(value) or value<=0:
            raise ValueError('Expected a positive numeric value: '+field)
        units=CAPACITY_UNITS if field in CAPACITY_PAIRS else SPEED_UNITS
        if not isinstance(unit,str) or unit.strip().casefold() not in FIELD_UNITS.get(field,set(units)):
            raise ValueError('Missing or unsupported unit: '+unit_field)
        normalized[field]=value*units[unit.strip().casefold()]
    ram=normalized['RAM Memory Installed']
    if 'Computer Memory Size' in normalized and ram!=normalized['Computer Memory Size']:
        raise ValueError('Installed RAM aliases disagree after unit conversion')
    if 'RAM Memory Maximum Size' in normalized and ram>normalized['RAM Memory Maximum Size']:
        raise ValueError('Installed RAM exceeds verified supported maximum')
    maximum_alias=values.get('Ram Memory Maximum Size')
    if maximum_alias is not None:
        unit=values.get('RAM Memory Maximum Size Unit')
        if isinstance(maximum_alias,str):
            match=re.fullmatch(r'\s*(\d+(?:\.\d+)?)\s*(GB|MB|TB)\s*',maximum_alias,re.I)
            if not match: raise ValueError('RAM maximum alias requires explicit numeric capacity and unit')
            maximum_alias=float(match[1]);unit=match[2]
        if type(maximum_alias) not in (int,float) or not math.isfinite(maximum_alias) or maximum_alias<=0 or not isinstance(unit,str) or unit.strip().casefold() not in CAPACITY_UNITS:
            raise ValueError('RAM maximum alias requires a positive capacity and verified unit')
        maximum=maximum_alias*CAPACITY_UNITS[unit.strip().casefold()]
        if maximum<ram or ('RAM Memory Maximum Size' in normalized and maximum!=normalized['RAM Memory Maximum Size']):
            raise ValueError('Maximum RAM aliases disagree or installed RAM exceeds maximum')
    for key,actual in [('ramGB',ram),('ssdGB',normalized['Hard Disk Size'])]:
        expected=base.get(key)
        if type(expected) not in (int,float) or expected!=actual:
            raise ValueError('Workbook sold capacity differs from selected base: '+key)
    if 'Memory Storage Capacity' in normalized:
        expected=normalized['Hard Disk Size'] if storage_total_gb is None else storage_total_gb
        if normalized['Memory Storage Capacity']!=expected:
            raise ValueError('Internal storage capacity fields disagree; reconcile verified component scope and units')
    cpu=identity.get('cpu')
    for field in ('Item Name','Bullet Point','Product Description'):
        text=values.get(field,'')
        if not isinstance(text,str): raise ValueError('Expected listing text: '+field)
        for capacity,kind in capacity_mentions(text):
            expected={'ram':ram,'ssd':normalized['Hard Disk Size'],'vram':normalized.get('Graphics Ram Size')}.get(kind)
            if expected is not None and capacity!=expected: raise ValueError('Listing copy includes another RAM/SSD configuration or VRAM size: '+field)
    if not isinstance(cpu,str) or not cpu.strip(): raise ValueError('Verified CPU identity required in product facts')
    canonical=' '+cpu_text(cpu)+' '
    model_anchor=cpu_text(exact_cpu_model(cpu))
    aliases=identity.get('cpuFieldAliases',{})
    if not isinstance(aliases,dict) or any(field not in ('CPU Model','CPU Model Number','CPU Model Manufacturer')
        or not isinstance(names,list) or any(not isinstance(name,str) or not cpu_text(name) for name in names)
        for field,names in aliases.items()):
        raise ValueError('CPU aliases require supported field names and lists of verified text equivalents')
    for field in ('CPU Model','CPU Model Number','CPU Model Manufacturer'):
        value=values.get(field)
        if value is None: continue
        accepted=aliases.get(field,[])
        if not isinstance(value,str) or not cpu_text(value) or (' '+cpu_text(value)+' ' not in canonical and cpu_text(value) not in [cpu_text(a) for a in accepted]):
            raise ValueError('Workbook CPU family/model/manufacturer differs from product facts: '+field)
        if field=='CPU Model Number' and ' '+model_anchor+' ' not in ' '+cpu_text(value)+' ':
            if cpu_text(value) not in [cpu_text(a) for a in accepted]:
                raise ValueError('Exact CPU model number required; manufacturer/family is insufficient')
    copy_aliases=[cpu_text(alias) for alias in aliases.get('CPU Model Number',[])]
    for field in ('Item Name','Bullet Point','Product Description'):
        for claim in cpu_claims(values.get(field,'')):
            if ' '+cpu_text(claim)+' ' not in canonical and cpu_text(claim) not in copy_aliases:
                raise ValueError('Listing copy CPU differs from verified CPU identity: '+field)
    # Ambiguous grouping fields (e.g. Ram Memory) and storage-vs-RAM labels are
    # deliberately not equated. Their Definition and evidence require review.
    return {'content':'PASS','sourceAuthenticationInferred':False}
