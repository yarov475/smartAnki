from smartanki.anki_import import import_known_words_from_anki
from smartanki.cefr_filter import CEFRFilter
from smartanki.pdf_reader import read_pdf_text
from smartanki.vocab_db import clear_db, list_known_words, import_from_csv, add_known_words, is_known
from smartanki.utils import clean_word
import os

def handle_admin(args):
    if args.admin_command == "clear-db":
        clear_db()
        print("✅ Known words database cleared.")

    elif args.admin_command == "list-known":
        known = list_known_words()
        print(f"✅ {len(known)} known words:")
        for word in known:
            print("📌", word)

    elif args.admin_command == "import-words":
        path = args.filepath
        ext = path.lower().split(".")[-1]

        cefr = CEFRFilter(args.cefr.upper())
        imported_words = []

        if ext == "csv":
            # Track changes before/after import
            before = set(list_known_words())
            import_from_csv(path)
            after = set(list_known_words())
            imported_words = list(after - before)

        elif ext == "txt":
            with open(path, encoding="utf-8") as f:
                raw_words = [clean_word(line.strip().lower()) for line in f if line.strip()]
            imported_words = [
                word for word in raw_words
                if word and cefr.is_above_user_level(word) and not is_known(word)
            ]
            add_known_words(imported_words)

        elif ext == "pdf":
            text = read_pdf_text(path)
            tokens = text.split()
            raw_words = [clean_word(w.lower()) for w in tokens if w.isalpha()]
            unique_words = list(set(raw_words))
            imported_words = [
                word for word in unique_words
                if word and cefr.is_above_user_level(word) and not is_known(word)
            ]
            add_known_words(imported_words)

        else:
            print(f"❌ Unsupported file type: {args.filepath}")
            return

        print(f"✅ Imported {len(imported_words)} new CEFR-filtered words from: {args.filepath}")
        for w in sorted(imported_words):
            print("  ➕", w)
