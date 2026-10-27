"""Normalize actual DOM captures; no inferred options or cross-context unions."""
import argparse,collections,hashlib,json,os,re,tempfile
from pathlib import Path
import openpyxl
REPO=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--captures-dir',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--unmapped-report',type=Path)
args=parser.parse_args();ROOT=args.captures_dir
book=openpyxl.load_workbook(REPO/'assets/listing-workbook-template.xlsx',read_only=True)
fields={s.title:[c.value for c in list(s[1])[1:]] for s in book};book.close()
def field_name(sheet,label):
 if label in fields[sheet]:return label
 matches=[v for v in fields[sheet] if str(v).casefold()==str(label).casefold()]
 return matches[0] if len(matches)==1 else None
captures=[('seller-aio-product-details.json','Product Details'),('seller-aio-offer.json','Offer'),('seller-aio-safety.json','Safety&Compliance'),('seller-notebook-product-details.json','Product Details'),('seller-notebook-offer.json','Offer'),('seller-notebook-safety.json','Safety&Compliance')]
captures += [('seller-desktop-product-details.json','Product Details'),('seller-desktop-offer.json','Offer'),('seller-desktop-safety.json','Safety&Compliance')]
aliases={
 'country_of_origin-*-value':'Country/Region of Origin',
 'merchant_shipping_group-*-value':'Shipping Template',
 'merchant_suggested_asin-*-value':'Merchant Suggested ASIN',
 'contribution_sku-*-value':'SKU',
 'batteries_required-*-value':'Are batteries required?',
 'externally_assigned_product_identifier-*-type':None,
 'product_site_launch_date-*-value':'Product Site Launch Date',
 'purchasable_offer-*-discounted_price-*-schedule-*-start_at':'Sale Start Date',
 'purchasable_offer-*-discounted_price-*-schedule-*-end_at':'Sale End Date',
 'purchasable_offer-*-start_at-value':'Offering Release Date',
 'merchant_release_date-*-value':'Merchant Release Date',
 'gift_options-*-can_be_messaged':'Offering Can Be Gift Messaged',
 'gift_options-*-can_be_wrapped':'Is Gift Wrap Available',
 'is_this_product_subject_to_buyer_age_restrictions-*-value':'Is This Product Subject To Buyer Age Restrictions',
 'gpsr_safety_attestation-*-value':'Safety Attestation',
 'ships_globally-*-value':'Ships Globally',
 'has_replaceable_battery-*-value':'Has Replaceable Battery',
 'has_less_than_30_percent_state_of_charge-*-value':'Has Less than 30 Percent State of Charge',
 'is_oem_sourced_product-*-value':'Is OEM Sourced Product',
 'modified_product-*-value':'Modified Product',
}
contexts={};unmapped=[]
reviewed_aliases=json.loads((REPO/'assets/amazon-selection-aliases.json').read_text(encoding='utf-8'))['fields']
for name,sheet in captures:
 path=ROOT/name
 if not path.exists():continue
 raw=path.read_bytes();data=json.loads(raw);key=(data['marketplaceId'],data['locale'],data['productType'],data.get('itemTypeKeyword','__NOT_DISPLAYED__'))
 ctx=contexts.setdefault(key,{'marketplaceId':key[0],'locale':key[1],'productType':key[2],'itemTypeKeyword':key[3],'controls':[]})
 pred={r['name']:r for r in data.get('predictive',[])}
 grouped=collections.defaultdict(list)
 for control in data['controls']:
  if not control.get('name'):continue
  p=re.sub(r'-\d+(?=-|$)','-*',control['name']);grouped[p].append(control)
 for radio in data.get('radio',data.get('radios',[])):
  p=re.sub(r'-\d+(?=-|$)','-*',radio['name'])
  if p not in grouped:
   grouped[p].append({'tag':'KAT-RADIOBUTTON','name':radio['name'],'label':aliases.get(p),'radio':radio})
 for p,controls in grouped.items():
  c=controls[0];tag=c['tag'];label=c.get('label');attribute=field_name(sheet,label)
  if p in aliases:attribute=field_name(sheet,aliases[p])
  options=[];complete=False
  if tag=='KAT-DROPDOWN':
   kind='CLOSED';options=c.get('options',[]);complete=len(options)==c.get('optionCount',len(options))
  elif tag=='KAT-RADIOBUTTON':
   kind='CLOSED';options=[{'value':x.get('radio',{}).get('value') if isinstance(x.get('radio'),dict) else x.get('value'),'label':x.get('radio',{}).get('label') if isinstance(x.get('radio'),dict) else x.get('label')} for x in controls]
   if data.get('radios') or data.get('radio'):
    options=[x for x in data.get('radios',data.get('radio',[])) if re.sub(r'-\d+(?=-|$)','-*',x.get('name',''))==p]
   complete=True
  elif tag=='KAT-PREDICTIVE-INPUT':
   kind='SUGGESTED';r=pred.get(c['name'],{});options=r.get('options',[]);complete=(bool(r) and len(options)==r.get('optionCount',r.get('count',len(options))) and all(x=='height: 0px' for x in r.get('padding',[])))
  elif tag=='KAT-DATE-PICKER':kind='DATE'
  else:kind='NUMBER' if c.get('inputType')=='number' else 'TEXT'
  # Shipping templates are account-managed; catalog them as unobserved, not universal values.
  if p.startswith('merchant_shipping_group-'):kind='ACCOUNT_CLOSED';options=[];complete=False
  unique={}
  for o in options:
   code=o.get('value');text=o.get('label')
   if code is None or not str(code).strip() or not text:continue
   option={'code':str(code),'label':str(text).strip(),'disabled':bool(o.get('disabled',False))}
   if str(code) in unique and unique[str(code)]!=option:raise ValueError('Conflicting labels for one observed option code')
   unique[str(code)]=option
  normalized={'sheet':sheet,'attribute':attribute,'path':p,'label':label,'kind':kind,'options':list(unique.values()),'complete':complete,'repeatable':len(set(x['name'] for x in controls))>1 and tag!='KAT-RADIOBUTTON','observedAtUtc':data['observedAtUtc'],'evidenceSha256':hashlib.sha256(raw).hexdigest(),'evidenceFile':name}
  if p in reviewed_aliases:
   rule=reviewed_aliases[p]
   normalized['aliases']={k:v for k,v in rule['aliases'].items() if v in unique}
   normalized['aliasBasis']=rule['basis']
  if not attribute:unmapped.append({'sheet':sheet,'path':p,'label':label,'kind':kind})
  ctx['controls'].append(normalized)
if not contexts:raise ValueError('No observed capture inputs')
result={'schemaVersion':1,'scope':'OBSERVED_US_ENGLISH_UI_SCHEMA_ONLY','contexts':list(contexts.values())}
args.output.parent.mkdir(parents=True,exist_ok=True)
with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',newline='\n',suffix='.json',dir=args.output.parent,delete=False) as handle:
 temporary=Path(handle.name);handle.write(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
try:
 from amazon_selection import read_catalog
 read_catalog(temporary)
 os.replace(temporary,args.output)
finally:temporary.unlink(missing_ok=True)
if args.unmapped_report:args.unmapped_report.write_text(json.dumps(unmapped,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'contexts':len(contexts),'controls':sum(len(c['controls']) for c in contexts.values()),'unmapped':len(unmapped)},indent=2))
