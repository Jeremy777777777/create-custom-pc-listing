"""Field-specific capacity conventions; installed drive labels are decimal, not OS space."""
from decimal import Decimal
MEMORY_CAPACITY_UNITS={'kb':1/1024**2,'mb':1/1024,'gb':1,'tb':1024}
STORAGE_CAPACITY_UNITS={'kb':1/1000**2,'mb':1/1000,'gb':1,'tb':1000}
STORAGE_FIELDS={'Hard Disk Size','Memory Storage Capacity','Flash Memory Installed Size'}


def capacity_units(field):
    return STORAGE_CAPACITY_UNITS if field in STORAGE_FIELDS else MEMORY_CAPACITY_UNITS


def scaled_capacity(value,factor):
    """Avoid binary floating-point drift when normalizing decimal drive labels."""
    return float(Decimal(str(value))*Decimal(str(factor)))


def check_nominal_storage_basis(fact):
    """A known system/usable-space measurement cannot silently become a drive label."""
    basis=fact.get('evidence',{}).get('capacity_basis')
    if fact['status']=='VERIFIED' and basis not in (None,'DECIMAL_MARKETING'):
        raise ValueError('Sold storage requires decimal nominal capacity; reconcile binary/system/usable-space evidence first')
