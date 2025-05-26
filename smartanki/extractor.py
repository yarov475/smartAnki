import spacy
from smartanki.vocab_db import is_known, add_known_words

nlp = spacy.load("en_core_web_sm")


def extract_new_words(text: str, cefr_filter, auto_save=True, lemmatize=True, debug_cefr=False):
    doc = nlp(text)
    new_word_entries = {}  # word → example sentence

    for sent in doc.sents:
        for token in sent:
            if not token.is_alpha:
                continue

            word = token.lemma_.lower() if lemmatize else token.text.lower()

            if is_known(word):
                continue

            if not cefr_filter.is_above_user_level(word, debug=debug_cefr):
                continue

            if word not in new_word_entries:
                new_word_entries[word] = sent.text.strip()

    if auto_save and new_word_entries:
        add_known_words(list(new_word_entries.keys()))

    return new_word_entries  # 🔁 Now returns dict {word: sentence}
