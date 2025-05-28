# smartanki/main_cli.py

import argparse
import warnings
from tqdm import tqdm
from smartanki.vocab_db import init_db
from smartanki.cefr_filter import CEFRFilter
from smartanki.extractor import extract_new_words
from smartanki.anki_export import generate_anki_csv
from smartanki.anki_package_export import generate_anki_package
from smartanki.pdf_reader import read_pdf_text
from smartanki.anki_import import import_known_words_from_anki
from smartanki.pdf_reader import read_pdf_text
from smartanki.pdf_export import export_wordlist_to_pdf
warnings.filterwarnings("ignore", category=UserWarning)


def read_input_text(path, page_range=None):
    """
    Reads text from a .txt or .pdf file.

    Args:
        path (str): Path to the input file.
        page_range (tuple[int, int] or None): Optional 0-based page range (start, end) for PDFs.

    Returns:
        str: The full text extracted from the file.

    Raises:
        ValueError: If the file extension is unsupported.
    """
    path = path.strip().lower()

    if path.endswith(".pdf"):
        return read_pdf_text(path, page_range)

    elif path.endswith(".txt"):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    else:
        raise ValueError(f"❌ Unsupported file type: {path}. Use a .pdf or .txt file.")


def main():
    parser = argparse.ArgumentParser(description="📘 SmartAnki CLI – CEFR Vocabulary Extractor + Anki Deck Generator")
    parser.add_argument("filepath", nargs="?", help="Path to input file (.pdf or .txt)")
    parser.add_argument("--cefr", default="B2", help="User CEFR level (default: B2)")
    parser.add_argument("--csv", default="anki_exports/anki_cards.csv", help="CSV output path")
    parser.add_argument("--no-save", action="store_true", help="Don't save new words to database")
    parser.add_argument("--not-translate", action="store_true", help="Disable sentence translation")
    parser.add_argument("--no-lemmatize", action="store_true", help="Disable lemmatization")
    parser.add_argument("--export-apkg", action="store_true", help="Export as native Anki .apkg file")
    parser.add_argument("--tags", nargs="*", default=[], help="Custom tags for each card (space-separated)")
    parser.add_argument("--deck-name", default="SmartAnki Vocabulary Deck", help="Name of the Anki deck")
    parser.add_argument("--debug-cefr", action="store_true", help="Print CEFR debug info")
    parser.add_argument("--import-anki-csv", help="Import known words from a raw Anki-exported CSV (any format)")
    parser.add_argument("--pdf-pages", help="Page range to extract from PDF (e.g. 2-5). First page is 1.")
    parser.add_argument("--only-import-anki", action="store_true",help="Only import Anki CSV and exit (no extraction or export)")
    parser.add_argument("--pdf-output", help="Optional: path to save the extracted words as a PDF word list")
    parser.add_argument("--offline-translate",action="store_true",help=" only use Helsinki-NLP/opus-mt-en-ru model to translatr "
    )
    parser.add_argument(
        "--with-images",
        action="store_true",
        help="Include Unsplash images in Anki cards"
    )

    parser.add_argument(
        "--force-google",
        action="store_true",
        help="Force use of Google Translate (ignore Argos)."
    )

    args = parser.parse_args()
    if args.import_anki_csv:
        print(f"📥 Importing known words from: {args.import_anki_csv}")
        import_known_words_from_anki(args.import_anki_csv)

        if args.only_import_anki:
            print("✅ Done. Imported known words only. Exiting.")
            return

    def parse_page_range(range_str):
        try:
            start, end = map(int, range_str.split("-"))
            return start - 1, end - 1  # Convert to 0-based index
        except Exception:
            raise ValueError("❌ Invalid format for --pdf-pages. Use e.g. 2-5")

    # STEP 1: Init DB + Filters
    print("🔧 Initializing database and filters...")
    with tqdm(total=3, desc="🔧 Setup", unit="step") as pbar:
        init_db()
        pbar.update(1)
        cefr = CEFRFilter("./data/cefr_wordlist.csv", args.cefr.upper())
        pbar.update(1)
        pbar.update(1)  # Placeholder for any setup steps
    print("✅ Setup complete.\n")

    # STEP 2: Read File
    print(f"📖 Reading from {args.filepath}...")

    # Parse PDF page range (if provided)
    page_range = None
    if args.pdf_pages:
        try:
            start, end = map(int, args.pdf_pages.split("-"))
            page_range = (start - 1, end - 1)  # 0-based indexing
        except ValueError:
            raise ValueError("❌ Invalid format for --pdf-pages. Use e.g. 2-5")

    # Read and show progress
    with tqdm(total=1, desc="📖 Reading file", unit="file") as pbar:
        text = read_input_text(args.filepath, page_range=page_range)
        pbar.update(1)

    print(f"✅ File loaded. Length: {len(text):,} characters.\n")

    # STEP 3: Extract Words
    print("🧠 Extracting new words...")
    word_sentence_map = {}
    with tqdm(total=1, desc="🧠 Analyzing text", unit="task") as pbar:
        word_sentence_map = extract_new_words(
            text,
            cefr_filter=cefr,
            auto_save=not args.no_save,
            lemmatize=not args.no_lemmatize,
            debug_cefr=args.debug_cefr
        )
        pbar.update(1)

    print(f"✅ {len(word_sentence_map)} new words found and added to database.\n")
    if args.pdf_output:
        export_wordlist_to_pdf(word_sentence_map, args.pdf_output)
    # STEP 4: Export
    if args.export_apkg:
        print(f"📦 Generating Anki deck: {args.deck_name}")
        generate_anki_package(
            word_sentence_map,
            cefr_filter=cefr,
            output_path=f"anki_exports/{args.deck_name.replace(' ', '_')}.apkg",
            translate=not args.not_translate,
            custom_tags=args.tags,
            deck_name=args.deck_name,
            offline_translate=args.offline_translate,
            force_google=args.force_google,
            with_images=args.with_images
        )

    else:
        print(f"💾 Exporting Anki cards to {args.csv}...")
        generate_anki_csv(
            word_sentence_map,
            output_file=args.csv,
            translate=not args.not_translate
        )

    print("🎉 Done! You can now import your Anki deck.")


if __name__ == "__main__":
    main()
