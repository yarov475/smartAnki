import requests
import subprocess
import os
import time
import platform

import requests
import os
import time

def wait_for_anki(max_retries=5, delay=2):
    url = "http://localhost:8765"
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=2)
            return True
        except Exception:
            print("⏳ Waiting for AnkiConnect to become available...")
            time.sleep(delay)
    return False

def import_deck(deck_path):
    if not wait_for_anki():
        print("❌ Final attempt failed. Please import manually.")
        return False

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
        if result.get("error") is None:
            print("✅ Deck imported to Anki via AnkiConnect.")
            return True
        else:
            print(f"❌ AnkiConnect returned an error: {result['error']}")
            return False
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False



def launch_anki():
    try:
        system = platform.system()
        if system == "Windows":
            subprocess.Popen(["anki"], shell=True)
        elif system == "Darwin":
            subprocess.Popen(["open", "-a", "Anki"])
        elif system == "Linux":
            subprocess.Popen(["anki"])
        else:
            print(f"⚠️ Unknown OS: {system}")
            return False
        return True
    except Exception as e:
        print(f"❌ Failed to start Anki: {e}")
        return False
