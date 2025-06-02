# smartanki/anki_auto_importer.py

import os
import time
import subprocess
import requests

ANKI_EXECUTABLE = r"C:\Users\yayar\AppData\Local\Programs\Anki\anki.exe"
ANKI_CONNECT_URL = "http://localhost:8765"


def launch_anki():
    if os.path.exists(ANKI_EXECUTABLE):
        print("🚀 Launching Anki...")
        subprocess.Popen([ANKI_EXECUTABLE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)
    else:
        print("❌ Anki executable not found.")
        return False
    return True


def wait_for_anki(max_retries=10, delay=2):
    for _ in range(max_retries):
        try:
            response = requests.get(ANKI_CONNECT_URL, timeout=2)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            print("⏳ Waiting for AnkiConnect to become available...from anki connect")
            time.sleep(delay)
    return False


def import_apkg(deck_path):
    print('import deck from auto import ')
    abs_path = os.path.abspath(deck_path)
    payload = {
        "action": "importPackage",
        "version": 6,
        "params": {
            "path": abs_path
        }
    }
    try:
        response = requests.post(ANKI_CONNECT_URL, json=payload)
        result = response.json()
        if result.get("error") is None:
            print(f"✅ Deck imported from: {abs_path}")
            return True
        else:
            print(f"❌ AnkiConnect import error: {result['error']}")
            return False
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def deck_exists(deck_name):
    payload = {
        "action": "deckNames",
        "version": 6
    }
    try:
        response = requests.post(ANKI_CONNECT_URL, json=payload)
        result = response.json()
        return deck_name in result.get("result", [])
    except Exception as e:
        print(f"❌ Failed to fetch deck list: {e}")
        return False


def close_anki():
    try:
        subprocess.call(["taskkill", "/IM", "anki.exe", "/F"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("🔒 Anki closed after import.")
    except Exception as e:
        print(f"⚠️ Failed to close Anki: {e}")


def auto_import_to_anki(deck_path, expected_deck_name):
    print("📦 Starting automated Anki import...")

    launch_anki()

    if not wait_for_anki():
        print("❌ AnkiConnect did not respond in time.")
        return

    if not import_apkg(deck_path):
        return

    if deck_exists(expected_deck_name):
        print(f"📚 Deck '{expected_deck_name}' confirmed in Anki.")
        close_anki()
        print("🎉 Cards imported and Anki closed successfully.")
    else:
        print(f"⚠️ Deck '{expected_deck_name}' was not found after import.")
