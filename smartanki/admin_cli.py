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
    elif args.admin_command == "import-csv":
        import_from_csv(args.csv_file)
        print(f"✅ Imported known words from: {args.csv_file}")
