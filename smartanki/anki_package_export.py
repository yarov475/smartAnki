import os
import genanki
from gtts import gTTS

from smartanki.dictionary_api import get_word_data
from smartanki.translator import translate_to_russian
from smartanki.highlight_word import highlight_word
from smartanki.image_fetcher import fetch_image_url
from smartanki.utils import clean_word


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
        name='SmartAnkiModel',
        fields=[
            {"name": "Word"},
            {"name": "Phonetic"},
            {"name": "Definition"},
            {"name": "Example"},
            {"name": "Translation"},
            {"name": "POS"},
            {"name": "Tags"},
            {"name": "Image"},
            {"name": "Audio"},
        ],
        templates=[
            {
                "name": "SmartAnki Card",
                "qfmt": """
                <div style='font-size:20px'> <b>{{Word}}</b> [<i>{{Phonetic}}</i>] </div>
                <div style='text-align: center'>  {{Image}} </div>
                 <div style='text-align: center'> {{Audio}} </div>
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
        name=deck_name
    )

    skipped = []

    # Ensure output folder exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    media_output_dir = os.path.dirname(output_path)

    for word, sentence in word_sentence_map.items():
        cleaned_word = clean_word(word)
        word_info = get_word_data(cleaned_word)
        if not word_info or not word_info.get("definition", "").strip():
            print(f"⚠️ Skipping '{word}' – no definition available.")
            skipped.append(word)
            continue

        highlighted_example = highlight_word(sentence, word)
        translation = translate_to_russian(
            sentence,
            offline_only=offline_translate,
            force_google=force_google
        )

        # Tags
        level, source = cefr_filter.get_cefr_level(word, debug=False)
        tags = list(custom_tags)

        if level:
            tags.append(f"cefr::{level}")  # ✅ Safe: no tuple, just string
        if level and isinstance(level, str):
            tags.append(f"cefr::{level}")

        visible_tags = ", ".join(tags)
        print(f"🔖 Tags for '{word}': {tags}")

        # 🔽 Image Handling
        image_html = ""
        if with_images:
            try:
                result = fetch_image_url(word, force_ai=force_ai_image, output_dir=media_output_dir)
                if result and result["type"] == "path":
                    image_path = result["data"]
                    image_name = os.path.basename(image_path)
                    image_html = f"<img src='{image_name}' style='max-height:200px;'>"
                    media_files.append(image_path)
            except Exception as e:
                print(f"⚠️ Failed to fetch/save image for '{word}': {e}")
        audio_filename = f"{word}.mp3".replace(" ", "_")
        audio_path = os.path.join(media_output_dir, audio_filename)

        # Generate with gTTS only if not exists
        if not os.path.exists(audio_path):
            try:
                tts = gTTS(text=word, lang='en')
                tts.save(audio_path)
                print(f"🔊 Audio generated for '{word}'")
            except Exception as e:
                print(f"⚠️ Failed to generate audio for '{word}': {e}")
                audio_filename = ""  # skip audio on failure

        # Add to media if audio generated
        if audio_filename:
            media_files.append(audio_path)
            audio_html = f"[sound:{audio_filename}]"
        else:
            audio_html = ""

        # ✅ Create the card
        note = genanki.Note(
            model=model,
            fields=[
                word_info["word"],
                word_info.get("phonetic", ""),
                word_info["definition"],
                highlighted_example,
                translation,
                word_info.get("part_of_speech", ""),
                visible_tags,
                image_html,
                audio_html
            ],
            tags=tags
        )

        deck.add_note(note)

    # Save the package
    genanki.Package(deck, media_files=media_files).write_to_file(output_path)
    print(f"📦 Anki deck exported to local  {output_path} ")

# TODO add closing anki if failed
