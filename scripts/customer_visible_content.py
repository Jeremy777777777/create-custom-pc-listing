"""Reject internal production markers in customer copy, never in source metadata.

Raster inspection remains required: this check cannot detect a footer line or
read text embedded in image pixels. Pass exact copy or reviewed OCR, not recipes.
"""
import argparse
import re
from pathlib import Path


PATTERNS = (
    (r'\b(?:VL|VD|VA|PL)\s*-\s*\d+\b', 'internal product ID'),
    (r'\b(?:STYLE\s+PREVIEW|NOT\s+A\s+FINAL\s+LISTING\s+IMAGE)\b', 'production status'),
    (r'\bPT\s*0?[1-8]\b', 'internal page slot'),
    (r'(?m)^\s*0?[1-8]\s*/\s*\S', 'page-navigation eyebrow'),
)


def validate_customer_text(text):
    if not isinstance(text, str):
        raise ValueError('Customer copy must be text')
    if re.search(r'[\u3400-\u9fff]', text):
        raise ValueError('Customer-visible content must be English')
    normalized = text.translate(str.maketrans({c: '-' for c in '\u2010\u2011\u2012\u2013\u2014\u2212\uff0d'}))
    for pattern, reason in PATTERNS:
        if re.search(pattern, normalized, re.I):
            raise ValueError('Customer-visible content contains ' + reason)
    from dimension_units import validate_dimension_copy
    validate_dimension_copy(normalized)

def validate_image_plan_copy(plan):
    """Check declared rendered copy only; internal IDs, source notes and questions are metadata."""
    def text(value):
        if isinstance(value, str):
            validate_customer_text(value)
        elif isinstance(value, list):
            for item in value:
                text(item)
        elif isinstance(value, dict):
            for key in ('headline', 'subtitle', 'caption', 'label', 'text', 'capacity',
                        'typicalUse', 'selectionNote', 'useQualification', 'customerCopy', 'customerLabel'):
                if key in value:
                    text(value[key])
    for key in ('headline', 'subtitle', 'caption', 'customerCopy', 'selectionNote', 'useQualification'):
        if key in plan:
            text(plan[key])
    for group in ('ram', 'ssd'):
        if group in plan:
            text(plan[group])
            for tier in plan[group].get('tiers', []):
                text(tier)
    for row in plan.get('images', []):
        for key in ('headline', 'subtitle', 'caption', 'customerCopy'):
            if key in row:
                text(row[key])
        for claim in row.get('claims', []):
            text(claim.get('text'))
        visual = row.get('visualExplanation', {})
        text(visual.get('exactCopy', []))
        for mapping in visual.get('labelToVisualMap', []):
            text(mapping.get('label'))
        # Explicit rendered-copy fields in nested presentation records. Source
        # IDs, research notes and storyboard rationale remain internal metadata.
        presentation = row.get('presentation', {})
        text(presentation.get('customerCopy', []))
        text(presentation.get('screen', {}).get('customerCopy', []))
        text(presentation.get('storyboard', {}).get('accessoryTreatment', {}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--copy-file', type=Path, required=True,
                        help='UTF-8 customer copy or reviewed OCR text only; exclude internal records')
    args = parser.parse_args()
    try:
        validate_customer_text(args.copy_file.read_text(encoding='utf-8'))
    except ValueError as error:
        parser.exit(1, str(error) + '\n')
    print('CUSTOMER_COPY_CHECKED; raster header/footer and readability review still required')


if __name__ == '__main__':
    main()
