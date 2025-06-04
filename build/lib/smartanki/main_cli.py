# main_cli.py

import argparse
from smartanki.DB.vocab_db import init_db
from smartanki.utils.cefr_filter import CEFRFilter
from smartanki.utils.extractor import extract_new_words
from smartanki.parser.ANKI.anki_export import generate_anki_csv
from smartanki.utils.pdf_reader import read_pdf_text
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
    new_words = extract_new_words(text, cefr, auto_save=True)
    print(f"✅ {len(new_words)} new words found and added to database.")

    # Step 4: Export Anki CSV
    print(f"💾 Exporting Anki cards to {args.csv}...")
    generate_anki_csv(new_words, args.csv)

    print("🎉 Done! You can now import the CSV into Anki.")

if __name__ == "__main__":
    main()
