# smartanki/handle_writing.py

import os
import re
import datetime

from smartanki.dictionary_api import get_word_data
from smartanki.translate_to_eng import translate_to_english
from smartanki.writing_utils import check_spelling, check_grammar
from smartanki.vocab_db import add_srs_entry


def handle_writing(args):
    greeting()

    # Read multi-line user input until Ctrl+C
    lines = []
    try:
        while True:
            try:
                line = input()
                lines.append(line)
            except EOFError:
                break
    except KeyboardInterrupt:
        print("\n🛑 Input interrupted. Processing what you wrote...\n")

    user_input = "\n".join(lines).strip()
    if not user_input:
        print("❗ No input provided.")
        return

    print("\n📄 Processing your writing...\n")

    glossary = {}
    unknown_words = []
    grammar_matches = check_grammar(user_input)
    spelling_errors = check_spelling(user_input)

    # 🧠 Extract Russian words in brackets: [Пиренеи]
    extracting(glossary, grammar_matches, spelling_errors, unknown_words, user_input)


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


def greeting():
    print("✍️ Writing Mode — enter your text below.")
    print("📌 Embed unknown Russian words in square brackets. (e.g., The [Пиренеи] are beautiful.)")
    print("⌨️ Press Ctrl+C to finish writing and process the text.\n")


def save_yo_file(glossary, grammar_matches, spelling_errors, unknown_words, user_input):
    os.makedirs("writing_logs", exist_ok=True)
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    words = user_input.split()
    first_words = "-".join(words[:2]) if words else "untitled"
    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '', first_words)
    filename = f"{date}-{safe_name}.txt"
    filepath = os.path.join("writing_logs", filename)
    if unknown_words:
        print(f' ⚠️Не найдено: {unknown_words}\n')
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("✍️ Your Writing:\n")
        f.write(user_input + "\n\n")

        if glossary:
            f.write("📚 Glossary:\n")
            for word, info in glossary.items():
                f.write(f"- {word}: {info['phonetic']} — {info['definition']}\n")
                if info.get("example"):
                    f.write(f"  Example: {info['example']}\n")

        if spelling_errors:
            f.write("\n❌ Misspelled Words:\n")
            for item in spelling_errors:
                if isinstance(item, tuple) and len(item) == 2:
                    word, suggestion = item
                    f.write(f"- {word} ➜ {suggestion}\n")
                else:
                    f.write(f"- {item}\n")

        if grammar_matches:
            f.write("\n🧠 Grammar Suggestions:\n")
            for m in grammar_matches:
                suggestions = f" [Suggestions: {', '.join(m.replacements)}]" if m.replacements else ""
                f.write(f"- {m.message}{suggestions}\n")
        if unknown_words:
            for w in unknown_words:
                f.write(f"  ⚠️ {w}\n")
    return filepath
