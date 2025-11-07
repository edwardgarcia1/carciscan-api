import re
from typing import List

def parse_ingredients(text: str) -> List[str]:
    """
    Parses OCR text and extracts a list of potential ingredient names.

    Heuristics:
    - Splits text by common delimiters (comma, semicolon, colon, newline, etc.)
    - Strips extra whitespace and removes duplicates
    - Filters out entries that are clearly too long to be single ingredients
      (e.g., paragraphs or marketing descriptions)
    - Normalizes capitalization
    """
    if not text:
        return []

    # Normalize spacing and punctuation
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[:]', ': ', text)  # ensure colons have space after for consistent splitting

    # Split by common delimiters
    potential_ingredients = re.split(r'[,;•:()\[\].]', text)

    cleaned_ingredients = []
    for ing in potential_ingredients:
        ing = ing.strip()
        if not ing:
            continue

        # Remove starting bullets, numbering, or phrases like "and"
        ing = re.sub(r'^(and\s+|[\-\*\d\)]+)\s*', '', ing)

        # Filter out long or unlikely ingredients
        if len(ing.split()) > 20:
            continue

        # Remove trailing periods or commas
        ing = re.sub(r'[\.,]+$', '', ing)

        # Normalize capitalization (optional)
        ing = ing.strip().capitalize()

        cleaned_ingredients.append(ing)

    # Deduplicate while preserving order
    seen = set()
    unique_ingredients = []
    for ing in cleaned_ingredients:
        if ing.lower() not in seen:
            seen.add(ing.lower())
            unique_ingredients.append(ing)

    return unique_ingredients
