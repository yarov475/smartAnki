# smartanki/anki_import.py

import csv
from smartanki.vocab_db import add_known_words
import re

def import_known_words_from_anki(csv_path):
    words = set()
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            for cell in row:
                word_candidate = cell.strip().lower()
                if re.match(r"^[a-zA-Z\-']{2,}$", word_candidate):
                    words.add(word_candidate)
    if not words:
        print("⚠️ No valid words found in imported file.")
        return

    add_known_words(words)
    print(f"✅ Imported {len(words)} known words from '{csv_path}' into your database.")

    # TODO delete this
