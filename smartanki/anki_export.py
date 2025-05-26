import csv
import os
import re
from nltk.corpus import wordnet
from smartanki.dictionary_api import get_word_data
from smartanki.translator import translate_to_russian


def highlight_word(text: str, word: str):
    pattern = re.compile(rf'\b({re.escape(word)})\b', re.IGNORECASE)
    return pattern.sub(r'<b>\1</b>', text)


def get_definition_and_example(word):
    synsets = wordnet.synsets(word)
    if not synsets:
        return ("", "")
    definition = synsets[0].definition()
    examples = synsets[0].examples()
    example = examples[0] if examples else ""
    return (definition, example)


from nltk.corpus import wordnet as wn


def get_better_definition(word):
    synsets = wn.synsets(word)
    if not synsets:
        return "", ""

    # Prefer nouns > verbs > others
    priority = ['n', 'v', 'a', 'r']
    synsets.sort(key=lambda s: priority.index(s.pos()) if s.pos() in priority else 99)

    definition = synsets[0].definition()
    example = synsets[0].examples()[0] if synsets[0].examples() else ""
    return definition, example


def get_phonetic_placeholder(word):
    # Placeholder phonetics (IPA data requires external services or CMU dict)
    return f"/{word}/"


def generate_anki_csv(word_sentence_map, output_file='anki_exports/anki_cards.csv', translate=True):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    skipped = []

    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Word", "Phonetic", "Definition", "Example", "Translation", "POS"])

        for word, sentence in word_sentence_map.items():
            word_info = get_word_data(word)
            if not word_info or not word_info["definition"].strip():
                # print(f"⚠️ Skipping '{word}' – no dictionary data.")
                skipped.append(word)
                continue

            # Highlight English word in English sentence
            highlighted_example = highlight_word(sentence, word)

            translation = ""
            if translate:
                translated_sentence = translate_to_russian(sentence)
                translated_word = translate_to_russian(word)

                # Now try to highlight the translated word in the translated sentence
                if translated_word and translated_word in translated_sentence:
                    translation = highlight_word(translated_sentence, translated_word)
                else:
                    translation = translated_sentence  # fallback without highlighting

            writer.writerow([
                word_info["word"],
                word_info["phonetic"],
                word_info["definition"],
                highlighted_example,
                translation,
                word_info["part_of_speech"]
            ])

    print(f"\n📤 Export complete. Skipped {len(skipped)} words due to missing info.")
    if skipped:
        print("📝 Skipped words:")
        for word in skipped:
            print(f"  - {word}")

    print(f"\n📤 Export complete. Skipped {len(skipped)} words due to missing info.")
    if skipped:
        print("📝 Skipped words:")
        for word in skipped:
            print(f"  - {word}")
