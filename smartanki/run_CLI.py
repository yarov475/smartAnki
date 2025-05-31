from tqdm import tqdm

from smartanki.anki_export import generate_anki_csv
from smartanki.anki_import import import_known_words_from_anki
from smartanki.anki_package_export import generate_anki_package
from smartanki.cefr_filter import CEFRFilter
from smartanki.dictionary_api import get_word_data
from smartanki.extractor import extract_new_words
from smartanki.pdf_export import export_wordlist_to_pdf
from smartanki.translator import translate_to_russian
from smartanki.utils import parse_page_range, read_input_text
from smartanki.vocab_db import init_db, add_srs_entry


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
