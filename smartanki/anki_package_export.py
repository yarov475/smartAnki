# smartanki/anki_package_export.py

import genanki
import os
from smartanki.dictionary_api import get_word_data
from smartanki.translator import translate_to_russian
from smartanki.anki_export import highlight_word
from smartanki.image_fetcher import fetch_image_url
import requests


def generate_anki_package(
        word_sentence_map,
        cefr_filter,
        output_path="anki_exports/smartanki.apkg",
        translate=True,
        custom_tags=None,
        deck_name="SmartAnki Vocabulary Deck",
        offline_translate=False,
        force_google=False,
        with_images=False,
        force_ai_image=False
):
    media_files = []
    if custom_tags is None:
        custom_tags = []

    model = genanki.Model(
        model_id=1607392319,
        name=deck_name,
        fields=[
            {"name": "Word"},
            {"name": "Phonetic"},
            {"name": "Definition"},
            {"name": "Example"},
            {"name": "Translation"},
            {"name": "POS"},
            {"name": "Tags"},
            {"name": "Image"}
        ],
        templates=[
            {
                "name": "SmartAnki Card",
                "qfmt": """
        <div style='font-size:20px'>
          <b>{{Word}}</b> <i>{{Phonetic}}</i>
        </div>
        {{Image}}
        """,
                "afmt": """
        {{FrontSide}}
        <hr>
        <div style='font-size:18px'><b>Definition:</b><br>{{Definition}}</div><br>
        <div style='color:blue'><b>Example:</b><br>{{Example}}</div><br>
        <div style='color:green'><b>Translation:</b><br>{{Translation}}</div><br>
        <div style='font-style:italic'><b>Part of speech:</b> {{POS}}</div><br>
        <div style='font-style:italic'><b>Tags:</b> {{Tags}}</div>
        """
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
            skipped.append(word)
            continue

        # Highlight word in English sentence
        highlighted_example = highlight_word(sentence, word)

        # Translate and highlight the word in translation
        translation = translate_to_russian(
            sentence,
            offline_only=offline_translate,
            force_google=force_google
        )

        # 🔍 Get CEFR level and source for tagging
        level, source = cefr_filter.get_cefr_level(word, debug=False)

        tags = list(custom_tags)  # Start with user-defined tags
        if level:
            tags.append(f"cefr::{level}")
        if source:
            tags.append(f"source::{source}")

        visible_tags = ", ".join(tags)
        image_html = ""

        if with_images:
            result = fetch_image_url(word, force_ai=force_ai_image)
            if result:
                image_name = f"{word.replace(' ', '_')}_img.png"
                image_path = os.path.join("anki_exports", image_name)

                try:
                    if result["type"] == "url":
                        img_data = requests.get(result["data"]).content
                    else:
                        img_data = result["data"]

                    with open(image_path, "wb") as f:
                        f.write(img_data)

                    media_files.append(image_path)
                    image_html = f"<img src='{os.path.basename(image_path)}' style='max-height:200px;'>"
                except Exception as e:
                    print(f"⚠️ Failed to save image for '{word}': {e}")
        note = genanki.Note(
            model=model,
            fields=[
                word_info["word"],
                word_info["phonetic"],
                word_info["definition"],
                highlighted_example,
                translation,
                word_info["part_of_speech"],
                visible_tags,
                image_html,
            ],
            tags=tags
        )

        deck.add_note(note)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    genanki.Package(deck, media_files).write_to_file(output_path)
    print(f"📦 Anki deck exported to {output_path}")
