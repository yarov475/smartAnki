import argparse


def parser_function():
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
    return parser
