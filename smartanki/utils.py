import re

from smartanki.pdf_reader import read_pdf_text
from smartanki.web_scraper import scrape_webpage




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




def parse_page_range(range_str):
        try:
            start, end = map(int, range_str.split("-"))
            return start - 1, end - 1  # Convert to 0-based index
        except Exception:
            raise ValueError("❌ Invalid format for --pdf-pages. Use e.g. 2-5")


def read_input_text(path_or_url: str, page_range=None) -> str:
    path = path_or_url.strip().lower()
    if path.endswith(".pdf"):
        return read_pdf_text(path, page_range)
    elif path.endswith(".txt"):
        with open(path, encoding='utf-8') as f:
            return f.read()
    elif path.startswith("http://") or path.startswith("https://"):
        print(f"🌐 Scraping web page: {path_or_url}")
        return scrape_webpage(path)
    else:
        raise ValueError(f"❌ Unsupported file type: {path}. Use a .pdf, .txt, or URL.")


import re


import re

def deck_name_to_filename(deck_name: str) -> str:
    """Convert a deck name to a safe filename ending with .apkg"""
    # Strip leading/trailing whitespace
    safe_name = deck_name.strip()
    # Replace illegal characters on Windows/macOS/Linux
    safe_name = re.sub(r'[<>:"/\\|?*]', '-', safe_name)
    # Replace spaces with hyphens
    safe_name = safe_name.replace(" ", "-")
    # Collapse multiple hyphens
    safe_name = re.sub(r'-+', '-', safe_name)
    # Trim leading/trailing hyphens
    safe_name = safe_name.strip('-')
    # Ensure .apkg extension
    return f"{safe_name}.apkg"





