import csv
import os
from nltk.corpus import wordnet

def get_definition_and_example(word):
    synsets = wordnet.synsets(word)
    if not synsets:
        return ("", "")
    definition = synsets[0].definition()
    examples = synsets[0].examples()
    example = examples[0] if examples else ""
    return (definition, example)

def get_phonetic_placeholder(word):
    # Placeholder phonetics (IPA data requires external services or CMU dict)
    return f"/{word}/"

def generate_anki_csv(words, output_file='anki_export.csv'):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Word", "Phonetic", "Definition", "Example"])  # Anki field order

        for word in words:
            definition, example = get_definition_and_example(word)
            phonetic = get_phonetic_placeholder(word)
            writer.writerow([word, phonetic, definition, example])

    print(f"✅ Anki CSV created: {output_file}")
