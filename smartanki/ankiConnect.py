import requests
import os


def import_deck(deck_path):
    anki_url = "http://localhost:8765"

    payload = {
        "action": "importPackage",
        "version": 6,
        "params": {
            "path": deck_path
        }
    }

    try:
        response = requests.post(anki_url, json=payload)
        response.raise_for_status()
        print("Deck imported successfully!")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


# Usage
deck_path = "E:\Python apps\smartAnki\anki_exports\smartanki_auto.apkg"
import_deck(deck_path)
