# smartanki/wordnet_backup.py

from nltk.corpus import wordnet as wn

def get_wordnet_data(word: str):
    synsets = wn.synsets(word)
    if not synsets:
        return {
            "word": word,
            "phonetic": f"/{word}/",  # placeholder
            "definition": "",
            "example": "",
            "part_of_speech": ""
        }

    syn = synsets[0]
    return {
        "word": word,
        "phonetic": f"/{word}/",  # placeholder
        "definition": syn.definition(),
        "example": syn.examples()[0] if syn.examples() else "",
        "part_of_speech": syn.pos()
    }
