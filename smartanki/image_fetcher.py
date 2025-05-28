import os
import requests
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

# Fallback AI image generation from Hugging Face
def generate_ai_image_bytes(word):
    print(f"🤖 Generating AI image for '{word}' via Hugging Face...")
    # url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
    url = "https://api-inference.huggingface.co/models/nitrosocke/Arcane-Diffusion"

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": f"An abstract illustration of {word}"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=45)
        response.raise_for_status()
        return response.content  # binary image
    except Exception as e:
        print(f"❌ AI fallback failed for '{word}': {e}")
        return None

# Main image fetcher
def fetch_image_url(word: str, force_ai=False):
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
                return {"type": "url", "data": results[0]["urls"]["small"]}
        except Exception as e:
            print(f"❌ Unsplash failed for '{word}': {e}")

    # Fallback or forced
    image_data = generate_ai_image_bytes(word)
    if image_data:
        return {"type": "bytes", "data": image_data}

    return None
