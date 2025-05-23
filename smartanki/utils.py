from vocab_db import init_db, list_known_words

init_db()  # Ensures DB exists

words = list_known_words()
print("Known words:", words)