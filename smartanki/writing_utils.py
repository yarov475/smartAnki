import language_tool_python
from spellchecker import SpellChecker
import re

from smartanki.translate_to_eng import translate_to_english


def check_spelling(text):
    # Remove words within square brackets
    filtered_text = re.sub(r'\[[^\]]*\]', '', text)

    spell = SpellChecker()
    words = filtered_text.split()
    misspelled = spell.unknown(words)

    results = []
    for word in misspelled:
        suggestion = spell.correction(word)
        results.append((word, suggestion))

    return results







def check_grammar(text):
    print("checkшта grammar...")
    # Extract words within square brackets
    def extract_and_translate(match):
        word = match.group(1)
        translated_word = translate_to_english(word, offline_only=False)
        return f"[{translated_word}]"

    # Use regular expression to find and translate words in square brackets
    modified_text = re.sub(r'\[([^\]]+)\]', extract_and_translate, text)
    print(modified_text)

    # Check grammar of the modified text
    tool = language_tool_python.LanguageTool('en-US')

    print(f' Текст с переведенными словами: \n {modified_text}')
    return tool.check(modified_text)





