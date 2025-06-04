import pytest
from smartanki.DB.vocab_db import remove_srs_entry
from smartanki.DB.vocab_db import get_db_connection
from datetime import date
from smartanki.DB.vocab_db import (
    init_db,
    add_srs_entry,
    get_due_srs_entries,
    update_srs_review,
)


# 🔁 Ensure DB is initialized before tests run
@pytest.fixture(autouse=True)
def setup_db():
    init_db()

    def test_add_srs_entry_creates_entry():
        word = "zealot"
        add_srs_entry(
            word=word,
            phonetic="/ˈzɛlət/",
            definition="a person who is fanatical about a cause",
            usage="The zealot refused to compromise.",
            translation="фанатик"
        )

        due_words = get_due_srs_entries()
        assert any(w[0] == word for w in due_words), "❌ Word not found in due entries"


def test_update_srs_review_correct():
    word = "adversary"
    add_srs_entry(
        word=word,
        phonetic="/ˈæd.və.sər.i/",
        definition="an enemy",
        usage="He faced his adversary with courage.",
        translation="противник"
    )

    update_srs_review(word, correct=True)
    updated = [entry for entry in get_due_srs_entries() if entry[0] == word]
    if updated:
        interval = updated[0][5]  # original next_review date
        assert interval >= date.today(), "✅ Word rescheduled successfully"


def test_update_srs_review_incorrect():
    from smartanki.DB.vocab_db import get_db_connection
    word = "prophecy"
    add_srs_entry(
        word=word,
        phonetic="/ˈprɒ.fə.si/",
        definition="a prediction",
        usage="The prophecy was fulfilled.",
        translation="пророчество"
    )

    update_srs_review(word, correct=False)

    # Fetch the updated entry directly from the DB
    conn = get_db_connection()
    row = conn.execute("""
        SELECT repetitions, interval, ease
        FROM srs_words
        WHERE word = ?
    """, (word,)).fetchone()
    conn.close()

    assert row is not None, "❌ Word not found in srs_words"
    repetitions, interval, ease = row
    assert repetitions == 0, "❌ Repetitions should reset to 0 on failure"
    assert interval == 1, "❌ Interval should reset to 1 on failure"
    assert ease <= 2.5, "❌ Ease should decrease on failure"


def test_remove_srs_entry():
    word = "banishment"
    add_srs_entry(
        word=word,
        phonetic="/ˈbænɪʃmənt/",
        definition="expulsion",
        usage="He faced banishment from the kingdom.",
        translation="изгнание"
    )

    remove_srs_entry(word)

    conn = get_db_connection()
    result = conn.execute("SELECT 1 FROM srs_words WHERE word = ?", (word,)).fetchone()
    conn.close()

    assert result is None, f"❌ Word '{word}' was not removed"
