import re
import unicodedata
from typing import List, Tuple

quote_patterns = [
            (r'(\W|^)"(\w)', r'\1“\2'),  # Opening double quotes
            (r'(\w)"(\W|$)', r'\1”\2'),  # Closing double quotes
            (r"(\W|^)'(\w)", r'\1\‘\2'),  # Opening single quotes
            (r"(\w)'(\W|$)", r'\1\’\2'),  # Closing single quotes
        ]
duplicate_quotes = [
            (r'``', '"'),  # LaTeX-style opening quotes
            (r"''", '"'),  # LaTeX-style closing quotes
            (r'`', "'"),  # Backtick to single quote
        ]

def clean_quotes(text: str) -> str:
    """Clean quotes in a single text string"""
    for pattern, replacement in duplicate_quotes:
        text = re.sub(pattern, replacement, text)

    for pattern, replacement in quote_patterns:
        text = re.sub(pattern, replacement, text)

    return text

def find_missed_quotes(text: str, buf: int = 2) -> List[Tuple[int, int, str]]:
    """Find remaining ASCII quotes that might need manual review"""
    missed = []
    for match in re.finditer(r'["\']', text):
        context = text[max(0, match.start() - buf):min(len(text), match.end() + buf)]
        missed.append((match.start(), match.end(), context))
    return missed

def clean_white_spaces(text:str) -> str:
    text = text.replace('-', '–')
    text = text.replace('\t', ' ')
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\r', '\n', text)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r' +([.,!?;:])', r'\1', text)             # Remove space before punctuation
    # text = re.sub(r'([.,!?;:])([^\s])', r'\1 \2', text)     # Add space after punctuation
    return text.strip()

def clean_unicode(text:str) -> str:
    # Remove zero-width characters and other invisible Unicode chars
    # text = ''.join(char for char in text if unicodedata.category(char) != 'Cf')

    # Normalize Unicode (NFC form for consistent character representation)
    text = unicodedata.normalize('NFC', text)
    return text

def clean(text):
    text = clean_quotes(text)
    text = clean_white_spaces(text)
    text = clean_unicode(text)
    return text
