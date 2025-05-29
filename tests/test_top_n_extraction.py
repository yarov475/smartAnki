import pytest
from collections import defaultdict
from smartanki.extractor import extract_new_words

# Mock spaCy
import spacy
nlp = spacy.load("en_core_web_sm")



@pytest.fixture(autouse=True)
def patch_known_words(monkeypatch):
    monkeypatch.setattr("smartanki.extractor.is_known", lambda w: False)
    monkeypatch.setattr("smartanki.extractor.add_known_words", lambda words: None)

class MockCEFR:
    """Mock CEFR filter that accepts only selected words"""
    def __init__(self, allowed_words):
        self.allowed_words = set(allowed_words)
    def is_above_user_level(self, word, debug=False):
        return word in self.allowed_words

def test_extract_top_n_words():
    text = """
    The prophecy was written long ago. The prophecy foretold the coming of a hero.
    This hero would bring redemption and face the adversary. 
    The prophecy became legend. Many spoke of the prophecy.
    """
    # We only accept these as "above CEFR level"
    cefr_filter = MockCEFR(["prophecy", "redemption", "adversary", "hero"])

    top_n = 2
    results = extract_new_words(
        text=text,
        cefr_filter=cefr_filter,
        auto_save=False,
        lemmatize=True,
        debug_cefr=False,
        top_n=top_n
    )

    # ✅ Check correct number of words
    assert len(results) == top_n, f"Expected {top_n} words, got {len(results)}"

    # ✅ 'prophecy' appears 4 times, should always be in result
    assert "prophecy" in results

    # ✅ Second most frequent should be either 'hero' or another known frequent word
    word_counts = defaultdict(int)
    doc = nlp(text)
    for token in doc:
        if token.is_alpha:
            word = token.lemma_.lower()
            word_counts[word] += 1
    sorted_words = sorted(
        [w for w in word_counts if w in cefr_filter.allowed_words],
        key=lambda w: -word_counts[w]
    )

    top_words_expected = set(sorted_words[:top_n])
    assert set(results.keys()).issubset(top_words_expected), \
        f"Unexpected words extracted: {set(results.keys()) - top_words_expected}"
