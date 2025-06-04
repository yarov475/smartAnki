import re

from smartanki.dictionary_api import get_word_data
from smartanki.translate_to_eng import translate_to_english
from smartanki.vocab_db import add_srs_entry
from smartanki.writing_save_to_filei import save_yo_file


def extracting(glossary, grammar_matches, spelling_errors, unknown_words, user_input):
    russian_pattern = r"\[([а-яА-ЯёЁ\s\-]+)\]"
    matches = re.findall(russian_pattern, user_input)
    print(f"🕵️ Found Russian bracketed words: {matches}")
    for ru_word in matches:
        ru_word = ru_word.strip()
        en_translation = translate_to_english(ru_word)

        if not en_translation:
            print(f"⚠️ Could not translate: {ru_word}")
            unknown_words.append(ru_word)
            continue

        en_word = en_translation.lower().strip()
        word_info = get_word_data(en_word)

        if not word_info or not word_info.get("definition"):
            print(f"⚠️ No dictionary data found for: {en_word}")
            unknown_words.append(en_word)
            continue

        glossary[en_word] = word_info
        example = word_info.get("example", "")

        print(f"\n📚 {en_word}: {word_info['phonetic']} — {word_info['definition']}")
        if example:
            print(f"   📖 Example: {example}")

        add_srs_entry(
            word=en_word,
            phonetic=word_info.get("phonetic", ""),
            definition=word_info["definition"],
            usage=user_input,
            translation=ru_word,
        )
    # Grammar output
    if grammar_matches:
        print(f"\n🧠 Grammar issues found: {len(grammar_matches)}")
        for m in grammar_matches:
            print(f"⚠️ {m.message}")
            if m.replacements:
                print(f"   💡 Suggestion: {', '.join(m.replacements)}")
    else:
        print("✅ No grammar issues found.")
    # Save to writing_logs/
    filepath = save_yo_file(glossary, grammar_matches, spelling_errors, unknown_words, user_input)
    print(f"\n📝 Writing saved to: {filepath}")
