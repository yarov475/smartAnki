# main_cli.py

import argparse

from smartanki import cefr_filter
from smartanki.vocab_db import init_db
from smartanki.extractor import extract_new_words
from smartanki.anki_export import generate_anki_csv
from smartanki.pdf_reader import read_pdf_text
from smartanki.anki_package_export import generate_anki_package
from smartanki.cefr_filter import CEFRFilter



import warnings


warnings.filterwarnings("ignore", category=UserWarning)


def read_input_text(path):
    if path.lower().endswith(".pdf"):
        return read_pdf_text(path)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(description="📘 SmartAnki CLI – CEFR Vocabulary Extractor")
    parser.add_argument("filepath", help="Path to input file (.pdf or .txt)")
    parser.add_argument("--cefr", default="B2", help="User CEFR level (default: B2)")
    parser.add_argument("--csv", default="anki_exports/anki_cards.csv", help="Output CSV path")
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't store extracted words in the known words database"
    )
    parser.add_argument(
        "--no-lemmatize",
        action="store_true",
        help="Disable lemmatization (by default, words are lemmatized)"
    )
    parser.add_argument(
        "--debug-cefr",
        action="store_true",
        help="Print source of CEFR level for each word"
    )
    parser.add_argument(
        "--not-translate",
        action="store_true",
        help="Disable sentence translation (enabled by default)"
    )
    parser.add_argument(
        "--export-apkg",
        action="store_true",
        help="Export Anki .apkg deck (instead of just CSV)"
    )
    parser.add_argument(
        "--tags",
        nargs="*",
        default=[],
        help="Custom tags to add to every Anki card (space-separated, e.g. --tags cefr::B2 topic::science)"
    )

    args = parser.parse_args()

    # Step 1: Init
    print("🔧 Initializing database and filters...")
    init_db()
    cefr = CEFRFilter("data/cefr_wordlist.csv", args.cefr.upper())


    # Step 2: Load text
    print(f"📖 Reading from {args.filepath}...")
    text = read_input_text(args.filepath)

    # Step 3: Extract words
    print("🧠 Extracting new words...")
    word_sentence_map = extract_new_words(
        text,
        cefr,
        auto_save=not args.no_save,
        lemmatize=not args.no_lemmatize,
        debug_cefr=args.debug_cefr
    )

    word_count = len(word_sentence_map)
    print(f"✅ {word_count} new words found and added to database.")

    # Step 4: Export Anki CSV
    print(f"💾 Exporting Anki cards to {args.csv}...")
    generate_anki_csv(
        word_sentence_map,
        args.csv,
        translate=not args.not_translate
    )
    if args.export_apkg:
        cefr = CEFRFilter("data/cefr_wordlist.csv", args.cefr.upper())
        generate_anki_package(
            word_sentence_map,
            cefr,
            output_path="anki_exports/smartanki.apkg",
            translate=not args.not_translate,
            custom_tags=args.tags
        )
        print("🎉 Done! You can now anki package  into Anki.")
    else:
        generate_anki_csv(word_sentence_map, args.csv, translate=not args.not_translate, custom_tags=args.tags)
        print("🎉 Done! You can now import the CSV into Anki.")

    if __name__ == "__main__":
        main()
