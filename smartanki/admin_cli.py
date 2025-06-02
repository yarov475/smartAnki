from smartanki.anki_import import import_known_words_from_anki
from smartanki.pdf_reader import read_pdf_text
from smartanki.vocab_db import clear_db, list_known_words, import_from_csv


def handle_admin(args):
    if args.admin_command == "clear-db":
        clear_db()
        print("✅ Known words database cleared.")
    elif args.admin_command == "list-known":
        known = list_known_words()
        print("✅ Known words:")
        for word in known:
            print("-", word)
    elif args.admin_command == "import-words":
        path = args.filepath.lower()
        if path.endswith(".csv"):
            import_from_csv(path)
        elif path.endswith(".txt"):
            with open(path, encoding="utf-8") as f:
                words = [line.strip().lower() for line in f if line.strip()]
                from smartanki.vocab_db import add_known_words
                add_known_words(words)
        elif path.endswith(".pdf"):
            text = read_pdf_text(path)
            words = [w.strip().lower() for w in text.split() if w.isalpha()]
            from smartanki.vocab_db import add_known_words
            add_known_words(words)
        else:
            print(f"❌ Unsupported file type: {args.filepath}")
            return
        print(f"✅ Imported words from: {args.filepath}")
