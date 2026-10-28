"""Explicit seller-authorized own-brand routing; legacy customized listings stay intact."""
import re

CUSTOM = 'CUSTOMIZED_OEM'
OWN_BRAND = 'MEGAPC_OWN_BRAND'


def resolve(product):
    mode = product.get('listingMode', CUSTOM)
    if mode not in (CUSTOM, OWN_BRAND):
        raise ValueError('Unsupported listingMode')
    if mode == OWN_BRAND:
        identity = product.get('identity', {})
        if str(identity.get('oemBrand', '')).strip().casefold() != 'megapc':
            raise ValueError('Own-brand mode requires MegaPC manufacturer identity')
        basis = product.get('ownBrandAuthority')
        if not isinstance(basis, str) or not basis.strip():
            raise ValueError('Own-brand mode requires explicit seller authorization evidence')
    return mode


def validate_own_brand_copy(text):
    if re.search(r'\b(?:custom(?:ized|ised|ization|isation|ize|ise|izations|isations)?|upgrad(?:e|ed|es|ing)|created\s+using)\b|seal.{0,40}open', text, re.I):
        raise ValueError('Own-brand copy cannot claim customization, upgrades, Created Using or seal opening')
