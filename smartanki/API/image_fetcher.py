import os
import requests
from dotenv import load_dotenv
load_dotenv()
HUGGINGFACE_TOKEN = os.getenv("hf")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")



from smartanki.API.yandex_api import generate_yandex_image



def fetch_image_url(word: str, force_ai=False, output_dir="anki_exports") -> dict | None:
    if not force_ai:
        try:
            print(f"🌐 Searching Unsplash for '{word}'")
            response = requests.get(
                "https://api.unsplash.com/search/photos",
                headers={"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"},
                params={"query": word, "per_page": 1}
            )
            response.raise_for_status()
            results = response.json().get("results", [])
            if results:
                image_url = results[0]["urls"]["small"]
                image_data = requests.get(image_url).content

                os.makedirs(output_dir, exist_ok=True)
                filepath = os.path.join(output_dir, f"{word.replace(' ', '_')}_unsplash.png")
                with open(filepath, "wb") as f:
                    f.write(image_data)

                return {"type": "path", "data": filepath}
        except Exception as e:
            print(f"❌ Unsplash failed for '{word}': {e}")

    # 🧠 AI fallback → Yandex
    return generate_yandex_image(word, output_dir=output_dir)

