import re
from typing import List


def parse_ingredients(text: str) -> List[str]:
    """
    Parses a block of text and extracts a list of potential ingredient names.

    This is a placeholder implementation. A real-world implementation would be
    much more sophisticated, handling commas, semicolons, parentheses, and other
    delimiters. It might also use a pre-defined list of ingredients to improve accuracy.

    Args:
        text: The raw string extracted from an image via OCR.

    Returns:
        A list of cleaned ingredient strings.
    """
    if not text:
        return []

    # Simple placeholder logic:
    # 1. Split by common delimiters
    # 2. Remove extra whitespace
    # 3. Filter out empty strings

    # This regex splits by comma, semicolon, or newline
    potential_ingredients = re.split(r'[,;\n]', text)

    # Clean up each ingredient
    cleaned_ingredients = []
    for ingredient in potential_ingredients:
        cleaned = ingredient.strip()
        if cleaned:  # Ensure it's not an empty string
            cleaned_ingredients.append(cleaned)

    return cleaned_ingredients


# Example of how we might test this
if __name__ == '__main__':
    sample_text = """
    Active Ingredients: Water, Glycerin, Acetyl-L-carnitine; 
    Cetearyl Alcohol, Phenoxyethanol.
    Inactive Ingredients: Fragrance, Citric Acid
    """
    parsed = parse_ingredients(sample_text)
    print(parsed)
    # Expected output: ['Active Ingredients: Water', 'Glycerin', 'Acetyl-L-carnitine', 'Cetearyl Alcohol', 'Phenoxyethanol.', 'Inactive Ingredients: Fragrance', 'Citric Acid']
    # Note: This simple parser is not perfect, but it's a start!