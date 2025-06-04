import spacy
from collections import Counter
from smartanki.utils.utils import clean_word
from smartanki.DB.vocab_db import is_known, add_known_words

nlp = spacy.load("en_core_web_sm")
nlp.max_length = 2_000_000  # Allow long texts

def extract_new_words(
    text: str,
    cefr_filter,
    auto_save=True,
    lemmatize=True,
    debug_cefr=False,
    top_n=None
):
    doc = nlp(text)
    word_freq = Counter()
    new_word_entries = {}  # cleaned_word → sentence

    # First pass: build frequency of clean unknown CEFR-filtered words
    for sent in doc.sents:
        for token in sent:
            if not token.is_alpha:
                continue

            raw = token.lemma_ if lemmatize else token.text
            word = clean_word(raw)

            if not word:
                continue

            if is_known(word):
                continue

            if not cefr_filter.is_above_user_level(word, debug=debug_cefr):
                continue

            word_freq[word] += 1

    # Select top N if requested
    if top_n:
        filtered = word_freq.most_common(top_n)
        filtered_words_set = {word for word, _ in filtered}

        print(f"\n🧠 Top {top_n} most frequent unknown words:")
        for i, (word, count) in enumerate(filtered, 1):
            print(f"{i}. {word} ({count})")
    else:
        filtered_words_set = set(word_freq)

    # Second pass: map first sentence where each top word appears
    for sent in doc.sents:
        for token in sent:
            if not token.is_alpha:
                continue

            raw = token.lemma_ if lemmatize else token.text
            word = clean_word(raw)

            if word in filtered_words_set and word not in new_word_entries:
                new_word_entries[word] = sent.text.strip()

    if auto_save and new_word_entries:
        add_known_words(list(new_word_entries.keys()))

    return new_word_entries
