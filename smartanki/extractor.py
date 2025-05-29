import spacy
from smartanki.vocab_db import is_known, add_known_words

nlp = spacy.load("en_core_web_sm")
nlp.max_length = 2_000_000

from collections import Counter

def extract_new_words(
    text: str,
    cefr_filter,
    auto_save=True,
    lemmatize=True,
    debug_cefr=False,
    top_n=None
):
    doc = nlp(text)
    new_word_entries = {}  # word → sentence
    word_freq = Counter()

    # First pass: build frequency for CEFR-filtered unknowns
    for sent in doc.sents:
        for token in sent:
            if not token.is_alpha:
                continue

            word = token.lemma_.lower() if lemmatize else token.text.lower()

            if is_known(word):
                continue

            if not cefr_filter.is_above_user_level(word, debug=debug_cefr):
                continue

            word_freq[word] += 1

    # Get top N words if requested
    filtered_words = word_freq.most_common(top_n) if top_n else word_freq.items()
    filtered_words_set = {word for word, _ in filtered_words}
    if top_n:
        print(f"\n🧠 Top {top_n} most frequent unknown words:")
        for i, (word, count) in enumerate(word_freq.most_common(top_n), 1):
            print(f"{i}. {word} ({count})")

    # Second pass: map each top word to first sentence it occurs in
    for sent in doc.sents:
        for token in sent:
            if not token.is_alpha:
                continue

            word = token.lemma_.lower() if lemmatize else token.text.lower()

            if word in filtered_words_set and word not in new_word_entries:
                new_word_entries[word] = sent.text.strip()

    if auto_save and new_word_entries:
        add_known_words(list(new_word_entries.keys()))

    return new_word_entries
