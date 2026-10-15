"""Resolve canonical internal identifiers without silently choosing a conflicting alias."""


def product_id(product):
    if not isinstance(product,dict): raise ValueError('Product facts must be an object')
    identity=product.get('identity',{})
    identifiers=[product.get('internalId'),product.get('productId')]
    if isinstance(identity,dict):identifiers.append(identity.get('internalId'))
    supplied=[value for value in identifiers if value is not None]
    if any(not isinstance(value,str) or not value.strip() or value!=value.strip() for value in supplied):
        raise ValueError('Product facts internal identifiers must be nonblank exact text')
    if len(set(supplied))>1:
        raise ValueError('Product facts contain conflicting internal product identifiers')
    return supplied[0] if supplied else None
