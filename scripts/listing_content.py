"""Formal export content checks; drafts keep unresolved evidence without invented values."""
import math
import re

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
SPEED_UNITS = {'mhz':1, 'ghz':1000, 'mt/s':1}


def validate_listing(projected, product, definitions=None):
    values = {field:record['value'] for (sheet,field),record in projected.items() if sheet=='Product Details'}
    for key,definition in (definitions or {}).items():
        value=projected[key]['value']
        if value is None: continue
        definition=str(definition).casefold()
        if 'numeric value' in definition or 'number of ' in definition:
            if type(value) not in (int,float) or not math.isfinite(value) or value<0:
                raise ValueError('Template Definition requires a nonnegative number: '+str(key))
            if 'number of ' in definition and int(value)!=value:
                raise ValueError('Template Definition requires an integer count: '+str(key))
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
        if not isinstance(unit,str) or unit.strip().casefold() not in units:
            raise ValueError('Missing or unsupported unit: '+unit_field)
        normalized[field]=value*units[unit.strip().casefold()]
    for field,value in values.items():
        # Numeric template counts/sizes must never accept bool, negative or fractional counts.
        if value is not None and (field.endswith('Count') or field in ('Processor Count','Model Year')):
            if type(value) not in (int,float) or not math.isfinite(value) or value<0 or int(value)!=value:
                raise ValueError('Expected a nonnegative integer: '+field)
    ram=normalized['RAM Memory Installed']
    if 'Computer Memory Size' in normalized and ram!=normalized['Computer Memory Size']:
        raise ValueError('Installed RAM aliases disagree after unit conversion')
    if 'RAM Memory Maximum Size' in normalized and ram>normalized['RAM Memory Maximum Size']:
        raise ValueError('Installed RAM exceeds verified supported maximum')
    for key,actual in [('ramGB',ram),('ssdGB',normalized['Hard Disk Size'])]:
        expected=base.get(key)
        if type(expected) not in (int,float) or expected!=actual:
            raise ValueError('Workbook sold capacity differs from selected base: '+key)
    cpu=identity.get('cpu')
    for field in ('Item Name','Bullet Point','Product Description'):
        text=values.get(field,'')
        if not isinstance(text,str): raise ValueError('Expected listing text: '+field)
        for amount,unit,kind in re.findall(r'(?i)\b(\d+(?:\.\d+)?)\s*(GB|TB|MB)\s*(?:DDR\d\s*)?(RAM|SSD)\b',text):
            capacity=float(amount)*CAPACITY_UNITS[unit.casefold()]
            expected=ram if kind.casefold()=='ram' else normalized['Hard Disk Size']
            if capacity!=expected: raise ValueError('Listing copy includes another RAM/SSD configuration: '+field)
    if cpu and str(values['CPU Model Number']).casefold() not in str(cpu).casefold():
        raise ValueError('Workbook CPU model differs from product facts')
    # Ambiguous grouping fields (e.g. Ram Memory) and storage-vs-RAM labels are
    # deliberately not equated. Their Definition and evidence require review.
    return {'content':'PASS','sourceAuthenticationInferred':False}
