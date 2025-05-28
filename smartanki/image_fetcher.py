import os
import requests
from dotenv import load_dotenv

load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")  # You can store it in .env


def fetch_image_url(word):
    try:
        url = "https://api.unsplash.com/search/photos"
        headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
        params = {"query": word, "per_page": 1}

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        results = response.json().get("results")

        if results:
            print(results[0]["urls"]["small"])
            return results[0]["urls"]["small"]
        print()

    except Exception as e:
        print(f"❌ Failed to fetch image for '{word}': {e}")
    return None
