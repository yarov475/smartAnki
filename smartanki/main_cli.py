import argparse
import warnings
from pathlib import Path
from tqdm import tqdm

from smartanki.configurator import setup_config_interactively
from smartanki.review import run_review_session
from smartanki.vocab_db import init_db, clear_db, list_known_words, import_from_csv
from smartanki.extractor import extract_new_words
from smartanki.anki_package_export import generate_anki_package
from smartanki.anki_export import generate_anki_csv
from smartanki.vocab_db import add_srs_entry
from smartanki.dictionary_api import get_word_data
from smartanki.translator import translate_to_russian
from smartanki.pdf_export import export_wordlist_to_pdf
from smartanki.anki_import import import_known_words_from_anki
from smartanki.cefr_filter import CEFRFilter
from smartanki.web_scraper import scrape_webpage
from smartanki.pdf_reader import read_pdf_text
from smartanki.utils import parse_page_range, read_input_text

warnings.filterwarnings("ignore", category=UserWarning)





def handle_admin(args):
    if args.admin_command == "clear-db":
        clear_db()
        print("✅ Known words database cleared.")
    elif args.admin_command == "list-known":
        known = list_known_words()
        print("✅ Known words:")
        for word in known:
            print("-", word)
    elif args.admin_command == "import-csv":
        import_from_csv(args.csv_file)
        print(f"✅ Imported known words from: {args.csv_file}")


def handle_run(args):
    print("🔧 Initializing database and filters...")
    with tqdm(total=3, desc="🔧 Setup", unit="step") as pbar:
        init_db()
        pbar.update(1)
        cefr = CEFRFilter(args.cefr.upper())
        pbar.update(1)
        pbar.update(1)
    print("✅ Setup complete.\n")

    # Handle known word import
    if args.import_anki_csv:
        print(f"📥 Importing known words from: {args.import_anki_csv}")
        import_known_words_from_anki(args.import_anki_csv)
        if args.only_import_anki:
            print("✅ Done. Imported known words only. Exiting.")
            return

    print(f"📖 Reading from {args.filepath}...")
    page_range = parse_page_range(args.pdf_pages) if args.pdf_pages else None
    with tqdm(total=1, desc="📖 Reading file", unit="file") as pbar:
        text = read_input_text(args.filepath, page_range)
        pbar.update(1)
    print(f"✅ File loaded. Length: {len(text):,} characters.\n")

    print("🧠 Extracting new words...")
    with tqdm(total=1, desc="🧠 Analyzing text", unit="task") as pbar:
        word_sentence_map = extract_new_words(
            text=text,
            cefr_filter=cefr,
            auto_save=not args.no_save,
            lemmatize=not args.no_lemmatize,
            debug_cefr=args.debug_cefr,
            top_n=args.top_n
        )
        pbar.update(1)

    print(f"✅ {len(word_sentence_map)} new words found and added to database.\n")

    for word, sentence in word_sentence_map.items():
        word_info = get_word_data(word)
        if not word_info or not word_info.get("definition"):
            print(f"⚠️ Skipping SRS add for '{word}' — no definition found.")
            continue
        translation = translate_to_russian(
            sentence,
            offline_only=args.offline_translate,
            force_google=args.force_google
        )
        add_srs_entry(
            word=word,
            phonetic=word_info.get("phonetic", ""),
            definition=word_info["definition"],
            usage=sentence,
            translation=translation
        )
        print(f"📚 Added to SRS: {word}")

    if args.pdf_output:
        export_wordlist_to_pdf(word_sentence_map, args.pdf_output)

    apkg_path = args.apkg or "anki_exports/smartanki.apkg"
    if args.export_apkg or not args.csv:
        print(f"💾 Exporting Anki deck to {apkg_path}...")
        generate_anki_package(
            word_sentence_map,
            cefr_filter=cefr,
            output_path=apkg_path,
            translate=not args.not_translate,
            custom_tags=args.tags or [],
            deck_name=args.deck_name,
            offline_translate=args.offline_translate,
            force_google=args.force_google,
            with_images=args.with_images,
            force_ai_image=args.force_ai_image
        )

    if args.csv:
        print(f"💾 Exporting Anki cards to CSV: {args.csv}...")
        generate_anki_csv(
            word_sentence_map,
            output_file=args.csv,
            translate=not args.not_translate
        )

    print("🎉 Done! You can now import your Anki deck.")


def handle_config(args):
    if args.config_command == "init":
        setup_config_interactively()


def main():
    parser = argparse.ArgumentParser(prog="smartanki", description="📘 SmartAnki – Vocabulary Extractor & SRS")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # RUN
    parser_run = subparsers.add_parser("run", help="Extract words and generate Anki decks")
    parser_run.add_argument("filepath", help="Path to .txt/.pdf or URL")
    parser_run.add_argument("--cefr", default="B2")
    parser_run.add_argument("--csv")
    parser_run.add_argument("--no-save", action="store_true")
    parser_run.add_argument("--no-lemmatize", action="store_true")
    parser_run.add_argument("--not-translate", action="store_true")
    parser_run.add_argument("--export-apkg", action="store_true")
    parser_run.add_argument("--apkg", default="anki_exports/smartanki.apkg")
    parser_run.add_argument("--deck-name", default="SmartAnki Vocabulary Deck")
    parser_run.add_argument("--tags", nargs="*", default=[])
    parser_run.add_argument("--debug-cefr", action="store_true")
    parser_run.add_argument("--offline-translate", action="store_true")
    parser_run.add_argument("--force-google", action="store_true")
    parser_run.add_argument("--with-images", action="store_true")
    parser_run.add_argument("--force-ai-image", action="store_true")
    parser_run.add_argument("--top-n", type=int)
    parser_run.add_argument("--pdf-pages", help="Page range (e.g., 1-5)")
    parser_run.add_argument("--pdf-output", help="Output PDF word list")
    parser_run.add_argument("--import-anki-csv", help="Import known words from Anki CSV")
    parser_run.add_argument("--only-import-anki", action="store_true")

    # ADMIN
    parser_admin = subparsers.add_parser("admin", help="Administrative tools")
    admin_subparsers = parser_admin.add_subparsers(dest="admin_command", required=True)
    admin_subparsers.add_parser("clear-db", help="Clear known words DB")
    admin_subparsers.add_parser("list-known", help="List known words")
    import_parser = admin_subparsers.add_parser("import-csv", help="Import known words from CSV")
    import_parser.add_argument("csv_file")

    # REVIEW
    subparsers.add_parser("review", help="Run spaced repetition review session")

    parser_config = subparsers.add_parser("config", help="SmartAnki configuration commands")
    config_subparsers = parser_config.add_subparsers(dest="config_command", required=True)

    config_subparsers.add_parser("init", help="Create or update SmartAnki config file")


    args = parser.parse_args()

    if args.command == "run":
        handle_run(args)
    elif args.command == "admin":
        handle_admin(args)
    elif args.command == "review":
        run_review_session()
    elif args.command == "config":
        handle_config(args)


if __name__ == "__main__":
    main()
