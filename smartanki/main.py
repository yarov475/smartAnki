from smartanki.cefr_filter import CEFRFilter
from smartanki.extractor import extract_new_words
from smartanki.anki_export import generate_anki_csv
from vocab_db import init_db
from smartanki.dictionary_api import get_word_data

# Setup
init_db()
cefr = CEFRFilter(csv_path='./data/cefr_wordlist.csv', user_level='B2')

# Input text
text = """In an era characterized by rapid technological advancements and unprecedented global
 interconnectedness, the imperative to cultivate critical thinking and nuanced understanding has never been more pronounced. The proliferation of information, while ostensibly empowering, simultaneously engenders challenges related to discernment and intellectual rigor. Consequently, individuals must navigate a complex landscape where superficial knowledge is ubiquitous, yet profound insight remains elusive. Mastery of language, coupled with an ability to synthesize diverse perspectives, is indispensable for meaningful engagement in contemporary discourse. Ultimately, fostering cognitive agility and epistemic humility will equip society to address multifaceted issues with both creativity and ethical responsibility.."""

# Extract new words and auto-save to DB
new_words = extract_new_words(text, cefr, auto_save=True)

# Generate Anki-ready CSV
generate_anki_csv(new_words, output_file='../anki_exports/anki_cards.csv')
print(new_words)

print(get_word_data("xyzzy"))  # Likely not in API, will use WordNet
print(get_word_data("write"))  # Likely will use API

#  TODO
# 8 work with  pnj jpeg
# cashing
# add audio
# auto import to anki with flag
# make GUI turn to anki addon
#  open in explorer

