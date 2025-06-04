# vocab_db.py

import sqlite3
import os
import csv
from typing import List
from contextlib import closing
from smartanki.utils.utils import clean_word

# === DB SETUP ===

DB_DIR = os.path.join(os.path.dirname(__file__), '..', 'db')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'user_words.db')


def add_known_words(words: List[str]):
    """Add a list of words to the known words database."""
    with get_db_connection() as conn:
        c = conn.cursor()
        for word in words:
            word = clean_word(word)
            c.execute('INSERT OR IGNORE INTO known_words (word) VALUES (?)', (word,))
        conn.commit()

def get_db_connection():
    return sqlite3.connect(DB_PATH)


def init_srs_table():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS srs_words (
        word TEXT PRIMARY KEY,
        phonetic TEXT,
        definition TEXT,
        usage TEXT,
        translation TEXT,
        next_review DATE,
        interval INTEGER,
        repetitions INTEGER,
        ease REAL,
        last_seen DATE
    )
    """)
    conn.commit()
    conn.close()


def init_db():
    """Create the known_words table if it does not exist."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS known_words (
            word TEXT PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()
    init_srs_table()


# === DB OPERATIONS ===



def is_known(word: str) -> bool:
    """Check if a word is marked as known."""
    word = clean_word(word)
    with closing(get_db_connection()) as conn:
        c = conn.cursor()
        c.execute('SELECT 1 FROM known_words WHERE word = ?', (word,))
        return c.fetchone() is not None





def list_known_words() -> List[str]:
    """List all known words in alphabetical order."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT word FROM known_words ORDER BY word')
    words = [row[0] for row in c.fetchall()]
    conn.close()
    return words


def print_known_words():
    """Print known words to console."""
    words = list_known_words()
    print(f"📚 {len(words)} known words:")
    for word in words:
        print(f"  • {word}")


def clear_db():
    """Clear all known words."""
    conn = get_db_connection()
    conn.execute("DELETE FROM known_words")
    conn.commit()
    conn.close()


def import_from_csv(csv_path: str):
    """Import known words from a CSV file (first column)."""
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        words = [row[0].strip().lower() for row in reader if row]
    add_known_words(words)


def get_db_path() -> str:
    """Return full DB file path (for debugging/info)."""
    return DB_PATH


def add_srs_entry(word, phonetic, definition, usage, translation):
    from datetime import date
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
    INSERT OR REPLACE INTO srs_words (
        word, phonetic, definition, usage, translation,
        next_review, interval, repetitions, ease, last_seen
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        word.lower(), phonetic, definition, usage, translation,
        date.today(), 1, 0, 2.5, date.today()
    ))
    conn.commit()
    conn.close()


def get_due_words():
    from datetime import date
    conn = get_db_connection()
    c = conn.cursor()
    today = date.today().isoformat()
    c.execute("SELECT word FROM srs_words WHERE next_review <= ?", (today,))
    words = [row[0] for row in c.fetchall()]
    conn.close()
    return words


def get_due_srs_entries():
    from datetime import date
    conn = get_db_connection()
    c = conn.cursor()
    today = date.today().isoformat()
    c.execute("""
        SELECT word, phonetic, definition, usage, translation, interval, repetitions, ease
        FROM srs_words
        WHERE next_review <= ?
        ORDER BY next_review ASC
    """, (today,))
    return c.fetchall()


def remove_srs_entry(word: str):
    """Remove a word from the spaced repetition system."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM srs_words WHERE word = ?", (word.lower(),))
    conn.commit()
    conn.close()


def update_srs_review(word, correct: bool):
    from datetime import date, timedelta
    conn = get_db_connection()
    c = conn.cursor()
    result = c.execute("SELECT interval, repetitions, ease FROM srs_words WHERE word = ?", (word,)).fetchone()
    if not result:
        return

    interval, repetitions, ease = result

    if correct:
        repetitions += 1
        ease = min(2.5, ease + 0.1)
        interval = int(interval * ease)
    else:
        repetitions = 0
        ease = max(1.3, ease - 0.2)
        interval = 1

    next_review = date.today() + timedelta(days=interval)

    c.execute("""
        UPDATE srs_words
        SET interval = ?, repetitions = ?, ease = ?, next_review = ?, last_seen = ?
        WHERE word = ?
    """, (interval, repetitions, ease, next_review, date.today(), word))

    conn.commit()
    conn.close()
