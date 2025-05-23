# vocab_db.py

import sqlite3
from typing import List

DB_PATH = 'db/user_words.db'

def init_db():
    """Create the database and the table if not exists."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS known_words (
            word TEXT PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

def add_known_words(words: List[str]):
    """Add a list of words to the known words database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for word in words:
        c.execute('INSERT OR IGNORE INTO known_words (word) VALUES (?)', (word.lower(),))
    conn.commit()
    conn.close()

def is_known(word: str) -> bool:
    """Check if a word is already known."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT 1 FROM known_words WHERE word = ?', (word.lower(),))
    result = c.fetchone()
    conn.close()
    return result is not None

def import_from_csv(csv_path: str):
    """Import known words from an existing Anki-style CSV."""
    import csv
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        words = [row[0].strip().lower() for row in reader if row]
    add_known_words(words)
def list_known_words():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT word FROM known_words ORDER BY word')
    words = [row[0] for row in c.fetchall()]
    conn.close()
    return words