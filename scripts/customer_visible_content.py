"""Reject internal production markers in customer copy, never in source metadata.

Raster inspection remains required: this check cannot detect a footer line or
read text embedded in image pixels. Pass exact copy or reviewed OCR, not recipes.
"""
import argparse
import re
from pathlib import Path


PATTERNS = (
    (r'\b(?:VL|VD)\s*-\s*\d+\b', 'internal product ID'),
    (r'\b(?:STYLE\s+PREVIEW|NOT\s+A\s+FINAL\s+LISTING\s+IMAGE)\b', 'production status'),
    (r'\bPT\s*0?[1-8]\b', 'internal page slot'),
    (r'(?m)^\s*0?[1-8]\s*/\s*\S', 'page-navigation eyebrow'),
)


def validate_customer_text(text):
    if not isinstance(text, str):
        raise ValueError('Customer copy must be text')
    normalized = text.translate(str.maketrans({c: '-' for c in '\u2010\u2011\u2012\u2013\u2014\u2212\uff0d'}))
    for pattern, reason in PATTERNS:
        if re.search(pattern, normalized, re.I):
            raise ValueError('Customer-visible content contains ' + reason)


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
