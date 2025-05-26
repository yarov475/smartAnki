# smartanki/anki_package_export.py

import genanki
import os
from smartanki.dictionary_api import get_word_data
from smartanki.translator import translate_to_russian
from smartanki.anki_export import highlight_word

def generate_anki_package(word_sentence_map, output_path="anki_exports/smartanki.apkg", translate=True):
    model = genanki.Model(
        model_id=1607392319,
        name='SmartAnkiModel',
        fields=[
            {"name": "Word"},
            {"name": "Phonetic"},
            {"name": "Definition"},
            {"name": "Example"},
            {"name": "Translation"},
            {"name": "POS"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "<div style='font-size:20px'><b>{{Word}}</b> <i>{{Phonetic}}</i></div>",
                "afmt": "{{FrontSide}}<hr><div style='font-size:18px'>{{Definition}}</div><br><div style='color:blue'>{{Example}}</div><br><div style='color:green'>{{Translation}}</div><br><i>{{POS}}</i>",
            }
        ]
    )

    deck = genanki.Deck(
        deck_id=2059400110,
        name='SmartAnki Vocabulary Deck'
    )

    skipped = []

    for word, sentence in word_sentence_map.items():
        word_info = get_word_data(word)
        if not word_info or not word_info["definition"].strip():
            print(f"⚠️ Skipping '{word}' – no definition available.")
            skipped.append(word)
            continue

        # Highlight word in English sentence
        highlighted_example = highlight_word(sentence, word)

        # Translate and highlight the word in translation
        translation = ""
        if translate:
            translated_sentence = translate_to_russian(sentence)
            translated_word = translate_to_russian(word)
            if translated_word in translated_sentence:
                translation = highlight_word(translated_sentence, translated_word)
            else:
                translation = translated_sentence

        note = genanki.Note(
            model=model,
            fields=[
                word_info["word"],
                word_info["phonetic"],
                word_info["definition"],
                highlighted_example,
                translation,
                word_info["part_of_speech"]
            ]
        )

        deck.add_note(note)

    # Ensure output folder exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save deck to file
    genanki.Package(deck).write_to_file(output_path)
    print(f"📦 Anki deck exported to {output_path}")
