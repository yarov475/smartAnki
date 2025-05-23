

import spacy
from cefr_filter import CEFRFilter
from vocab_db import is_known, add_known_words

nlp = spacy.load("en_core_web_sm")

def extract_new_words(text: str, cefr_filter: CEFRFilter, auto_save=True) -> list:
    """Tokenizes input text and returns new words above user level.
    Optionally adds them to the known words DB.
    """
    doc = nlp(text)
    new_words = set()

    for token in doc:
        if not token.is_alpha:
            continue

        word = token.text.lower().strip()

        if is_known(word):
            continue

        if not cefr_filter.is_above_user_level(word):
            continue

        new_words.add(word)

    new_words = sorted(new_words)

    # Automatically save to DB if flag is on
    if auto_save and new_words:
        add_known_words(new_words)

    return new_words
