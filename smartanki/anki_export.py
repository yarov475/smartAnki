import csv
import os
from smartanki.dictionary_api import get_word_data
from smartanki.highlight_word import highlight_word
from smartanki.translator import translate_to_russian
from smartanki.utils import clean_word


def generate_anki_csv(word_sentence_map, output_file='anki_exports/anki_cards.csv', translate=True):
    dir_path = os.path.dirname(output_file)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    skipped = []

    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Word", "Phonetic", "Definition", "Example", "Translation", "POS"])

        for word, sentence in word_sentence_map.items():
            cleaned_word = clean_word(word)
            word_info = get_word_data(cleaned_word)
            if not word_info or not word_info["definition"].strip():
                skipped.append(word)
                continue

            # Highlight English word in English sentence
            highlighted_example = highlight_word(sentence, word)

            translation = ""
            if translate:
                translated_sentence = translate_to_russian(sentence)
                translated_word = translate_to_russian(word)

                if translated_word and translated_word in translated_sentence:
                    translation = highlight_word(translated_sentence, translated_word)
                else:
                    translation = translated_sentence

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

