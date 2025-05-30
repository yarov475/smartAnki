from smartanki.vocab_db import get_due_srs_entries, update_srs_review, remove_srs_entry
from datetime import date


def run_review_session():
    entries = get_due_srs_entries()
    if not entries:
        print("🎉 No words due for review today!")
        return

    print(f"📘 Starting review session: {len(entries)} word(s) due today\n")

    for word, phonetic, definition, usage, translation, interval, repetitions, ease in entries:
        print('**********************************************************************************')
        print("🔹", word, f"({phonetic})")
        input("🔸 Press Enter to show meaning...")

        print("\n📖 Definition:", definition)
        print("💬 Usage:", usage)
        print("🌍 Translation:", translation)

        response = input("\n✅ Did you remember it? (y = yes, n = no, d = delete): ").strip().lower()

        if response == "d":
            remove_srs_entry(word)
            print(f"🗑️  Removed '{word}' from review list.\n" + "-" * 40)
            continue

        correct = response == "y"
        update_srs_review(word, correct)
