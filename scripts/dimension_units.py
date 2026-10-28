"""Inch-only output boundaries; source evidence retains its original measurements."""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, localcontext
import json
import math
from pathlib import Path
import re

POLICY=json.loads((Path(__file__).resolve().parents[1]/'assets/dimension-units-policy.json').read_text())
UNIT=POLICY['outputUnit']
PAIRS={
 ('Product Details','Screen Size'):'Display Size Unit',
 ('Product Details','Item Length Horizontal Edge'):'Item Length Unit',
 ('Product Details','Item Width Vertical Edge'):'Item Width Unit',
 ('Product Details','Thickness Front to Back'):'Item Thickness Unit',
 ('Offer','Item Package Length'):'Package Length Unit',
 ('Offer','Item Package Width'):'Package Width Unit',
 ('Offer','Item Package Height'):'Package Height Unit',
}
TEXT_FIELDS={('Product Details','Item Dimensions L x W x Thickness'),
             ('Product Details','Screen Bezel Thickness'),('Offer','Item Package Dimensions')}
NUMBER=r'(?:\d+(?:\.\d+)?|\.\d+)'
SEQUENCE=NUMBER+r'(?:\s*(?:x|×|[-–—])\s*'+NUMBER+r')*'
LENGTH_UNIT=r'(?:[A-Za-z]+\.?|["″])'
DIMENSION_CONTEXT=r'\((?:(?:OLED|IPS) chassis|(?:with|without) stand|(?:open|closed) chassis)\)'
SIMPLE_TEXT=re.compile(r'\s*(?P<sequence>'+SEQUENCE+r')\s*(?P<unit>'+LENGTH_UNIT+r')'
    r'(?P<qualifier>\s+(?:minimum|maximum|nominal))?(?P<context>\s*'+DIMENSION_CONTEXT+r')?\s*',re.I)
PROFILE_TEXT=re.compile(r'\s*(?P<sequence>'+NUMBER+r'\s*[x×]\s*'+NUMBER+r')\s*'
    r'(?P<unit>'+LENGTH_UNIT+r')\s*;\s*(?P<clauses>.+?)\s+(?P<axis>thickness|height|depth)\s*',re.I)
PROFILE_CLAUSE=re.compile(r'\s*(?P<label>front|rear|minimum|maximum|nominal)\s*:?\s*'
    r'(?P<sequence>'+NUMBER+r'(?:\s*[-–—]\s*'+NUMBER+r')?)\s*(?P<unit>'+LENGTH_UNIT+r')\s*',re.I)


def to_inches(value, unit):
    """Convert one explicitly-unitized positive measurement, rounded once."""
    if isinstance(value,bool):raise ValueError('Length must be a positive finite measurement')
    try:amount=Decimal(str(value))
    except (InvalidOperation,ValueError):raise ValueError('Length must be numeric') from None
    if not amount.is_finite() or amount<=0:raise ValueError('Length must be positive and finite')
    unit=str(unit).strip().casefold()
    divisors={'mm':POLICY['mmPerInch'],'millimeter':POLICY['mmPerInch'],'millimeters':POLICY['mmPerInch'],
              'cm':POLICY['cmPerInch'],'centimeter':POLICY['cmPerInch'],'centimeters':POLICY['cmPerInch'],
              'm':POLICY['mPerInch'],'meter':POLICY['mPerInch'],'meters':POLICY['mPerInch'],
              'in':'1','inch':'1','inches':'1','"':'1','″':'1'}
    if unit not in divisors and unit not in {'ft','foot','feet'}:raise ValueError('Explicit supported source length unit required')
    try:
        with localcontext() as context:
            context.prec=40
            result=amount*Decimal(POLICY['inchesPerFoot']) if unit in {'ft','foot','feet'} else amount/Decimal(divisors[unit])
            rounded=result.quantize(Decimal(1).scaleb(-POLICY['decimalPlaces']),rounding=ROUND_HALF_UP)
    except InvalidOperation:raise ValueError('Length outside supported conversion precision') from None
    if rounded<=0 or not math.isfinite(float(rounded)):raise ValueError('Conversion precision cannot erase a positive measurement')
    return float(rounded)


def _dimension_parts(value):
    """Parse only explicit geometry, retaining named positions and scope words."""
    simple=SIMPLE_TEXT.fullmatch(str(value))
    if simple:
        return 'simple',simple,[simple]
    profile=PROFILE_TEXT.fullmatch(str(value))
    if not profile:raise ValueError('Dimension text requires explicit units and supported geometry labels')
    clauses=[PROFILE_CLAUSE.fullmatch(part) for part in profile['clauses'].split(',')]
    if not 2<=len(clauses)<=5 or any(c is None for c in clauses):
        raise ValueError('Named dimension profile requires explicit units for each position')
    labels=[c['label'].casefold() for c in clauses]
    if len(labels)!=len(set(labels)):raise ValueError('Duplicate named dimension position')
    return 'profile',profile,[profile,*clauses]


def validate_dimension_text(value):
    """Accept inch geometry, not arbitrary prose or unlabelled mixed dimensions."""
    kind,_,parts=_dimension_parts(value)
    inches={'inches','inch','in','in.','"','″'}
    for part in parts:
        if part['unit'].casefold() not in inches or not positive(part['sequence'],text_allowed=True):
            raise ValueError('Dimension text must explicitly use positive finite inches')
    if kind=='profile':
        positions={p['label'].casefold():[float(n) for n in re.findall(NUMBER,p['sequence'])] for p in parts[1:]}
        for label,values in positions.items():
            if len(values)==2 and values[0]>values[1]:raise ValueError('Named dimension range bounds are reversed')
            other=[n for k,v in positions.items() if k!=label for n in v]
            if label=='maximum' and min(values)<max(other):raise ValueError('Maximum dimension is below another position')
            if label=='minimum' and max(values)>min(other):raise ValueError('Minimum dimension is above another position')
    return {'state':'INCH_DIMENSION_TEXT_CHECK_PASS','representation':kind}


def convert_length_text(value):
    """Convert explicit tuple/range/profile units; never discard scope or labels."""
    kind,match,parts=_dimension_parts(value)
    def converted(part):
        unit=part['unit']
        if unit.casefold()=='in.':unit='in'
        return re.sub(NUMBER,lambda m:format(to_inches(m[0],unit),'.4f').rstrip('0').rstrip('.'),part['sequence'])+' inches'
    if kind=='simple':
        result=converted(match)
        for name in ('qualifier','context'):
            if match[name]:result+=' '+match[name].strip()
    else:
        result=converted(match)+'; '+', '.join(p['label']+' '+converted(p) for p in parts[1:])+' '+match['axis']
    validate_dimension_text(result)
    return result


def positive(value, text_allowed=False):
    if type(value) in (int,float):return math.isfinite(value) and value>0
    if text_allowed and isinstance(value,str):
        value=re.sub(r'\s*(?:inches|inch|in\.?|["″])\s*$','',value,flags=re.I)
        return re.fullmatch(SEQUENCE,value.strip()) is not None and all(float(n)>0 for n in re.findall(NUMBER,value))
    return False


def validate_dimension_copy(text):
    """Catch explicit metric/feet size claims, preserving connector/model names."""
    text=re.sub(r'<[^>]+>',' ',str(text))
    labels=r'(?:length|width|height|depth|thickness|bezel|diagonal|dimensions?|key\s*travel|key\s*pitch)'
    # "1 x 3.5mm audio jack" is a count and named connector, not geometry.
    # An explicit preceding dimensions/width/etc label keeps geometry checkable.
    connector_count=r'\b[1-9]\d*\s*[x×]\s*(?:2\.5|3\.5|6\.35)\s*mm(?=\s*\(?\s*(?:(?:global|universal)\s+)?(?:audio|headphone|headset|microphone|combo|trrs|trs|jack)\b)'
    def connector(match):
        prefix=text[max(0,match.start()-50):match.start()]
        return match[0] if re.search(r'\b'+labels+r'\s*(?::|=|of|is)?\s*$',prefix,re.I) else 'NAMED_AUDIO_CONNECTOR_COUNT'
    text=re.sub(connector_count,connector,text,flags=re.I)
    other=r'(?:mm|cm|m|meters?|metres?|millimet(?:er|re)s?|centimet(?:er|re)s?|feet|foot|ft)\b'
    tuple_claim=NUMBER+r'\s*(?:x|×)\s*'+NUMBER+r'(?:\s*(?:x|×)\s*'+NUMBER+r')?\s*'+other
    repeated_units=NUMBER+r'\s*'+other+r'\s*(?:x|×|by)\s*'+NUMBER+r'(?:\s*'+other+r')?'
    labelled=r'\b'+labels+r'\s*(?::|=|of|is)?\s*'+NUMBER+r'\s*'+other
    positioned=r'\b'+labels+r'\s+(?:front|rear|minimum|maximum|nominal)\s*:?\s*'+NUMBER+r'\s*'+other
    trailing_label=NUMBER+r'\s*'+other+r'\s*'+labels+r'\b'
    if re.search('|'.join((tuple_claim,repeated_units,labelled,positioned,trailing_label)),text,re.I):raise ValueError('Physical dimension copy must use inches')


def validate_dimensions(projected):
    """Check formal and candidate outputs; never rewrite facts/status or evidence."""
    for (sheet,field),unit_field in PAIRS.items():
        record=projected.get((sheet,field),{});units=projected.get((sheet,unit_field),{})
        for name in ('value','value_candidate'):
            value=record.get(name);unit=units.get(name)
            if unit is not None and unit!=UNIT:raise ValueError('Dimension unit must be Inches: '+unit_field)
            if value is not None:
                effective=unit if unit is not None else units.get('value')
                if effective!=UNIT or not positive(value,text_allowed=name=='value_candidate'):
                    raise ValueError('Positive numeric dimension and paired Inches unit required: '+field)
    for key in TEXT_FIELDS:
        for name in ('value','value_candidate'):
            value=projected.get(key,{}).get(name)
            if value is not None:
                try:validate_dimension_text(value)
                except ValueError as exc:raise ValueError('Dimension text must explicitly use inches with retained labels: '+key[1]) from exc
    # Geometry can also occur in pointing-device/keyboard and other descriptions.
    # Never scan Source rows: quoted original measurements retain their units.
    for record in projected.values():
        for name in ('value','value_candidate'):
            if isinstance(record.get(name),str):validate_dimension_copy(record[name])
    return {'state':'INCH_DIMENSIONS_CHECK_PASS','unit':UNIT,'scope':'PHYSICAL_LINEAR_OUTPUTS_NOT_SOURCE_EVIDENCE'}
