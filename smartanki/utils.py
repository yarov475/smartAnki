import re

def clean_word(word: str) -> str:
    """
    Cleans a word by:
    - Lowercasing
    - Stripping whitespace
    - Normalizing apostrophes (e.g., ` ’ → ')
    - Removing possessive 's
    - Removing punctuation (preserving hyphens)
    """
    word = word.strip().lower()

    # Normalize apostrophes and backticks to straight quote
    word = word.replace("’", "'").replace("`", "'").replace("‘", "'")

    # Remove possessive 's (but not plural 's')
    word = re.sub(r"'s\b", "", word)

    # Remove leading/trailing quotes
    word = word.strip("'\"")

    # Remove any remaining non-word characters except hyphens
    word = re.sub(r"[^\w\-]", "", word)

    return word
