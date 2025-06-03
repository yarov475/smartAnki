import os
import re
import datetime
from textblob import TextBlob
from langdetect import detect
from smartanki.translator import HuggingFaceTranslator
from smartanki.dictionary_api import get_word_data
from smartanki.utils import clean_word
from smartanki.anki_package_export import generate_anki_package
from smartanki.anki_connect_auto_importer import auto_import_to_anki  # if you have this utility
from smartanki.writing_utils import check_grammar

WRITING_DIR = "anki_exports/writing_logs"

os.makedirs(WRITING_DIR, exist_ok=True)

translator = HuggingFaceTranslator("Helsinki-NLP/opus-mt-ru-en")

def is_russian(word):
    try:
        return detect(word) == "ru"
    except Exception:
        return bool(re.search(r"[а-яА-Я]", word))


def handle_writing(import_to_anki=False):
    print("✍️ Writing Mode: Type your text. Use Russian words inline, they will be translated.")
    print("Press Ctrl+C when done.\n")

    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except (EOFError, KeyboardInterrupt):
        print("\n✅ Writing session ended.\n")

    full_text = "\n".join(lines)
    grammar_matches = check_grammar(full_text)

    glossary = []
    glossary_map = {}
    seen = set()
    misspelled = []

    # Token extraction
    for word in re.findall(r"\b[\w\-]+\b", full_text):
        if word.lower() in seen:
            continue

        if is_russian(word):
            seen.add(word.lower())
            try:
                en_word = translator.translate(word)
                en_word = clean_word(en_word)

                if en_word not in glossary_map:
                    word_info = get_word_data(en_word)
                    if word_info and word_info.get("definition"):
                        glossary.append({
                            "russian": word,
                            "english": en_word,
                            "phonetic": word_info.get("phonetic", ""),
                            "definition": word_info["definition"],
                            "example": word_info.get("example", "")
                        })
                        glossary_map[en_word] = full_text  # save original usage for Anki
            except Exception as e:
                print(f"⚠️ Translation failed for '{word}': {e}")

    # Spellcheck
    english_words = [w for w in re.findall(r"\b[\w\-]+\b", full_text) if not is_russian(w)]
    blob = TextBlob(" ".join(english_words))
    misspelled = [w for w in blob.words if w.lower() != w.correct().lower()]

    # Save text file
    first = "_".join(full_text.strip().split()[:2])
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{date}-{first}.txt"
    path = os.path.join(WRITING_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write("✍️ Your Writing:\n" + full_text + "\n\n")
        if glossary:
            f.write("📚 Glossary:\n")
            for g in glossary:
                f.write(f"- {g['english']} ({g['phonetic']}): {g['definition']}\n")
                f.write(f"  Example: {g['example']}\n")
                f.write(f"  From Russian: {g['russian']}\n\n")
                print(g['russian'],'✍️', g['english'],g['phonetic'],g['definition'])
        if misspelled:
            f.write("❌ Misspelled Words:\n")
            for m in sorted(set(misspelled)):
                f.write(f"- {m}\n")
                print(f"❌  {m}\n")
        f.write("\n\n🧠 Grammar Suggestions:\n")
        for m in grammar_matches:
            f.write(f"- {m.message} [Suggestions: {', '.join(m.replacements)}]\n")

    print(f"\n✅ Writing saved: {path}")







    # Optional export to Anki
    if import_to_anki and glossary:
        print("📦 Exporting glossary to Anki...")

        word_sentence_map = {item["english"]: glossary_map[item["english"]] for item in glossary}
        apkg_path = f"anki_exports/{date}-{first}.apkg"

        generate_anki_package(
            word_sentence_map,
            cefr_filter=None,  # No CEFR filtering in this mode
            output_path=apkg_path,
            translate=False,
            custom_tags=["writing"],
            deck_name="SmartAnki Writing Deck",
            offline_translate=True,
            with_images=False,
            force_ai_image=False
        )

        auto_import_to_anki(deck_path=apkg_path, expected_deck_name="SmartAnki Writing Deck")
