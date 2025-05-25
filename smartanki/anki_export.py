import csv
import os
from nltk.corpus import wordnet
from smartanki.dictionary_api import get_word_data

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

# def generate_anki_csv(words, output_file='anki_export.csv'):
#     os.makedirs(os.path.dirname(output_file), exist_ok=True)
#
#     with open(output_file, mode='w', newline='', encoding='utf-8') as f:
#         writer = csv.writer(f)
#         writer.writerow(["Word", "Phonetic", "Definition", "Example"])  # Anki field order
#
#         for word in words:
#             definition, example = get_definition_and_example(word)
#             phonetic = get_phonetic_placeholder(word)
#             writer.writerow([word, phonetic, definition, example])
#
#     print(f"✅ Anki CSV created: {output_file}")
def generate_anki_csv(words, output_file='anki_exports/anki_cards.csv'):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    skipped = []

    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Word", "Phonetic", "Definition", "Example", "POS"])

        for word in words:
            word_info = get_word_data(word)

            if not word_info:
                print(f"⚠️ Skipping '{word}' – no data from API or fallback.")
                skipped.append(word)
                continue

            if not word_info["definition"].strip() and not word_info.get("translation", "").strip():
                print(f"⚠️ Skipping '{word}' – no definition or translation found.")
                skipped.append(word)
                continue

            writer.writerow([
                word_info["word"],
                word_info["phonetic"],
                word_info["definition"],
                word_info["example"],
                word_info["part_of_speech"]
            ])

    print(f"\n📤 Export complete. Skipped {len(skipped)} words due to missing info.")
    if skipped:
        print("📝 Skipped words:")
        for word in skipped:
            print(f"  - {word}")
