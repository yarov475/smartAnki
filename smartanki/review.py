from smartanki.vocab_db import get_due_srs_entries, update_srs_review
from datetime import date


def run_review_session():
    entries = get_due_srs_entries()
    if not entries:
        print("🎉 No words due for review today!")
        return

    print(f"📘 Starting review session: {len(entries)} word(s) due today\n")

    for word, phonetic, definition, usage, translation, interval, repetitions, ease in entries:
        print("🔹", word, f"({phonetic})")
        input("🔸 Press Enter to show meaning...")

        print("\n📖 Definition:", definition)
        print("💬 Usage:", usage)
        print("🌍 Translation:", translation)

        response = input("\n✅ Did you remember it? (y/n): ").strip().lower()
        correct = response == "y"

        update_srs_review(word, correct)
        print("🔄 Review updated.\n" + "-" * 40)
