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
INCH_TEXT=re.compile(r'\s*('+SEQUENCE+r')\s*(?:inches|inch|in\.?|["″])\s*',re.I)


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


def convert_length_text(value):
    """Convert a shared-unit dimension tuple/range without changing order/bounds."""
    match=re.fullmatch(r'\s*('+SEQUENCE+r')\s*([A-Za-z]+|["″])\s*',str(value))
    if not match:raise ValueError('Dimension text requires an explicit shared source unit')
    converted=re.sub(NUMBER,lambda m:format(to_inches(m[0],match[2]),'.4f').rstrip('0').rstrip('.'),match[1])
    return converted+' inches'


def positive(value, text_allowed=False):
    if type(value) in (int,float):return math.isfinite(value) and value>0
    if text_allowed and isinstance(value,str):
        value=re.sub(r'\s*(?:inches|inch|in\.?|["″])\s*$','',value,flags=re.I)
        return re.fullmatch(SEQUENCE,value.strip()) is not None and all(float(n)>0 for n in re.findall(NUMBER,value))
    return False


def validate_dimension_copy(text):
    """Catch explicit metric/feet size claims, preserving connector/model names."""
    text=re.sub(r'<[^>]+>',' ',str(text))
    other=r'(?:mm|cm|meters?|metres?|millimet(?:er|re)s?|centimet(?:er|re)s?|feet|foot|ft)\b'
    tuple_claim=NUMBER+r'\s*(?:x|×)\s*'+NUMBER+r'(?:\s*(?:x|×)\s*'+NUMBER+r')?\s*'+other
    labelled=r'\b(?:length|width|height|depth|thickness|bezel|diagonal|dimensions?)\s*(?::|=|of|is)?\s*'+NUMBER+r'\s*'+other
    if re.search(tuple_claim+'|'+labelled,text,re.I):raise ValueError('Physical dimension copy must use inches')


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
                match=INCH_TEXT.fullmatch(str(value))
                if not match or not positive(match[1],text_allowed=True):raise ValueError('Dimension text must explicitly use inches: '+key[1])
    for key,record in projected.items():
        if key[0]=='Product Details' and key[1] in {'Item Name','Bullet Point','Product Description'}:
            for name in ('value','value_candidate'):
                if record.get(name) is not None:validate_dimension_copy(record[name])
    return {'state':'INCH_DIMENSIONS_CHECK_PASS','unit':UNIT,'scope':'PHYSICAL_LINEAR_OUTPUTS_NOT_SOURCE_EVIDENCE'}
