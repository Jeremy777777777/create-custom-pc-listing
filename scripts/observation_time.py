"""Shared UTC validation for observations; never infer that an event occurred."""
from datetime import datetime, timezone


def utc(value):
    try:
        stamp = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if stamp.tzinfo is None or stamp.utcoffset().total_seconds() != 0 or stamp > datetime.now(timezone.utc):
            raise ValueError()
    except (ValueError, TypeError, AttributeError):
        raise ValueError('Observed non-future UTC time required') from None
    return stamp
