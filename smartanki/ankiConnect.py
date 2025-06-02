import requests
import os

def import_deck(deck_path):
    anki_url = "http://localhost:8765"

    payload = {
        "action": "importPackage",
        "version": 6,
        "params": {
            "path": os.path.abspath(deck_path)
        }
    }

    try:
        response = requests.post(anki_url, json=payload)
        response.raise_for_status()
        result = response.json()
        print("✅ Response from AnkiConnect:", result)
        return result
    except requests.exceptions.RequestException as e:
        print(f"❌ An error occurred: {e}")
        return None

# ✅ Correct path usage
deck_path = r"E:\Python apps\smartAnki\anki_exports\smartanki.apkg"
import_deck(deck_path)
