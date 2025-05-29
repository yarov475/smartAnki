# vocab_db.py

import sqlite3
import os
import csv
from typing import List

# === DB SETUP ===

DB_DIR = os.path.join(os.path.dirname(__file__), '..', 'db')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'user_words.db')

def get_db_connection():
    return sqlite3.connect(DB_PATH)


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

# === DB OPERATIONS ===

def add_known_words(words: List[str]):
    """Add words to the known_words table, ignoring duplicates."""
    conn = get_db_connection()
    c = conn.cursor()
    c.executemany('INSERT OR IGNORE INTO known_words (word) VALUES (?)',
                  [(word.lower(),) for word in words])
    conn.commit()
    conn.close()


def is_known(word: str) -> bool:
    """Check if a word is marked as known."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT 1 FROM known_words WHERE word = ?', (word.lower(),))
    result = c.fetchone()
    conn.close()
    return result is not None


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
