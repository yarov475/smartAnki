import re


def highlight_word(text: str, word: str):
    # Match word and optional possessive endings
    pattern = re.compile(rf"\b({re.escape(word)})(?:'s)?\b", re.IGNORECASE)
    return pattern.sub(r'<b>\1</b>', text)
