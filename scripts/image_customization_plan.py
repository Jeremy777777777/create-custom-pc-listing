"""Build/check the universal PT05 choice-page brief; never render or approve an image."""
import argparse
import hashlib
import json
from pathlib import Path
import re

from customization_policy import research, fragments
from listing_mode import resolve, CUSTOM
from product_metadata import selected_facts, hardware_projection

VERSION = 'universal-customization-image-v1'
RAM_TIERS = (
    ('8GB', 'Everyday browsing and documents'),
    ('16GB', 'Daily multitasking and study'),
    ('32GB', 'Larger spreadsheets and creative projects'),
    ('64GB', 'Memory-intensive projects and workflows'),
)
SSD_TIERS = (
    ('512GB', 'Everyday apps and essential files'),
    ('1TB', 'More room for projects and games'),
    ('2TB', 'Larger photo, video and game libraries'),
    ('4TB', 'Extensive project and media collections'),
)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def research_view(product, ledger):
    """PT05 uses researched RAM and seller choices, without unrelated CPU/SSD gates."""
    from product_identity import product_id
    from capacity_units import capacity_units, scaled_capacity
    if product_id(product) != ledger['productId']:
        raise ValueError('Customization image product identity mismatch')
    base=product.get('selectedBaseConfiguration',{})
    if base.get('id') and base['id']!=ledger['configurationId']:
        raise ValueError('Customization image configuration mismatch')
    info=research(product,ledger,required=True)
    if info is None:
        raise ValueError('Own-brand products retain their independent route')
    selected=selected_facts(ledger)
    key=('Product Details','RAM Memory Installed')
    unit_key=('Product Details','RAM Memory Installed Size Unit')
    ram,unit=selected.get(key),selected.get(unit_key)
    units=capacity_units(key[1])
    if (not ram or not unit or unit['status']!='VERIFIED'
            or type(ram['final_value']) not in (int,float) or ram['final_value']<=0
            or str(unit['final_value']).strip().casefold() not in units):
        raise ValueError('Customization image requires verified installed RAM and its capacity unit')
    amount=scaled_capacity(ram['final_value'],units[str(unit['final_value']).strip().casefold()])
    hardware_projection(ledger,product,required_fields={key,unit_key})
    if 'customization' in product and product['customization']!=info:
        raise ValueError('Product customization cache disagrees with selected RAM research')
    return {'customization':info,'selectedBaseConfiguration':{'id':ledger['configurationId'],'ramGB':amount}}


def production_check(directory):
    """Mandatory current PT05 research gate; no raster or style approval implied."""
    from research_export import load_ledger
    directory=Path(directory)
    product=json.loads((directory/'product-facts.json').read_text(encoding='utf-8-sig'))
    if resolve(product)!=CUSTOM:
        return {'state':'OWN_BRAND_SEPARATE_ROUTE','file':'PT05.png'}
    path=directory/'research-ledger.json'
    if not path.is_file():
        raise ValueError('Customized PT05 requires its current RAM research ledger')
    view=research_view(product,load_ledger(path))
    labels=fragments(view)
    return {'state':'CUSTOMIZATION_RESEARCH_CHECK_PASS','file':'PT05.png',
            'replaceable':view['customization']['replaceable'],
            'memoryType':view['customization']['memoryType'],'expectedLabels':labels,
            'visualQa':'SEPARATE_ACTUAL_REVIEW_REQUIRED'}


def build(product, ledger, product_sha256, ledger_sha256):
    for value in (product_sha256, ledger_sha256):
        if not re.fullmatch('[0-9a-f]{64}', str(value)):
            raise ValueError('Actual product/ledger SHA256 bindings required')
    if resolve(product) != CUSTOM:
        raise ValueError('Own-brand products retain their independent route; customization page is not automatic')
    view = research_view(product, ledger)
    info = view['customization']
    parts = fragments(view)
    replaceable = info['replaceable']
    return {
        'schemaVersion': 1, 'artifactRole': 'UNIVERSAL_CUSTOMIZATION_IMAGE_PLAN',
        'methodProfile': VERSION, 'productId': ledger['productId'],
        'configurationId': ledger['configurationId'],
        'productFactsSha256': product_sha256, 'ledgerSha256': ledger_sha256,
        'file': 'PT05.png', 'fullConfigurationOverview': False,
        'buyerQuestion': 'Which memory and storage options fit my needs?',
        'headline': 'Choose Your Memory and Storage',
        'claimScope': 'SELLER_OPTIONS_NOT_INSTALLED_CONFIGURATION',
        'sellerPolicyReference': 'references/customization-options-policy.md',
        'hardwareFactIds': [info['ramFactId']],
        'ram': {'replaceable': replaceable, 'memoryType': info['memoryType'],
                'label': parts['ram'], 'fixedCapacityGB': None if replaceable else view['selectedBaseConfiguration']['ramGB'],
                'tiers': [{'capacity': capacity, 'typicalUse': use} for capacity, use in RAM_TIERS] if replaceable else []},
        'ssd': {'label': parts['ssd'],
                'tiers': [{'capacity': capacity, 'typicalUse': use} for capacity, use in SSD_TIERS]},
        'selectionNote': ('Choose one RAM and one SSD option; only your selected configuration is supplied.'
                          if replaceable else 'RAM is fixed. Choose one SSD option; only your selected configuration is supplied.'),
        'useQualification': 'Use examples are illustrative; results depend on the workload and other hardware.',
        'visualBrief': 'Two clear RAM/SSD groups, prominent capacities and one short use caption per tier; fixed RAM uses one fixed-memory summary plus four SSD choices. Choose explanatory tier illustrations before any product anchor. Business Laptop PT05 is product-free. Adapt the approved series palette and layout.',
        'reviewWidthsPx': [400, 200], 'visualQa': 'NOT_ASSESSED', 'productionApprovalGranted': False,
    }


def check(plan, product, ledger, product_sha256, ledger_sha256):
    from customer_visible_content import validate_image_plan_copy
    validate_image_plan_copy(plan)
    expected = build(product, ledger, product_sha256, ledger_sha256)
    if plan != expected:
        raise ValueError('Customization image plan differs from current inputs, options or universal PT05 contract')
    return {'state': 'CUSTOMIZATION_IMAGE_PLAN_CHECKED', 'productId': expected['productId'],
            'file': 'PT05.png', 'ramOptionCount': len(expected['ram']['tiers']),
            'ssdOptionCount': 4, 'visualQa': 'NOT_ASSESSED', 'productionApprovalGranted': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'check'])
    parser.add_argument('--product-facts', required=True, type=Path)
    parser.add_argument('--ledger', required=True, type=Path)
    parser.add_argument('--plan', required=True, type=Path)
    args = parser.parse_args()
    from research_export import validate_ledger
    product_raw, ledger_raw = args.product_facts.read_bytes(), args.ledger.read_bytes()
    product, ledger = json.loads(product_raw.decode('utf-8-sig')), json.loads(ledger_raw.decode('utf-8-sig'))
    validate_ledger(ledger)
    inputs = product, ledger, digest(product_raw), digest(ledger_raw)
    if args.command == 'build':
        result = build(*inputs)
        # A brief is a supporting record; never replace product facts, a ledger,
        # another existing artifact, or create a purported final image file.
        if args.plan.suffix.lower() != '.json' or args.plan.name in {'product-facts.json', 'research-ledger.json'}:
            raise ValueError('A new supporting JSON plan path is required')
        with args.plan.open('x', encoding='utf-8', newline='\n') as output:
            output.write(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
        print(json.dumps(check(result, *inputs)))
    else:
        print(json.dumps(check(json.loads(args.plan.read_text(encoding='utf-8-sig')), *inputs)))


if __name__ == '__main__':
    main()
