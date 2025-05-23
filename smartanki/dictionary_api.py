# smartanki/dictionary_api.py

import requests
from smartanki.wordnet_backup import get_wordnet_data

def get_word_data(word: str):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            print(f"⚠️ API miss for '{word}', falling back to WordNet.")
            return get_wordnet_data(word)

        data = response.json()
        result = {
            "word": word,
            "phonetic": data[0].get("phonetic", f"/{word}/"),
            "definition": "",
            "example": "",
            "part_of_speech": ""
        }

        meanings = data[0].get("meanings", [])
        if meanings:
            defn = meanings[0]["definitions"][0]
            result["definition"] = defn.get("definition", "")
            result["example"] = defn.get("example", "")
            result["part_of_speech"] = meanings[0].get("partOfSpeech", "")

        return result

    except Exception as e:
        print(f"❌ API error for '{word}': {e} – using WordNet fallback.")
        return get_wordnet_data(word)
