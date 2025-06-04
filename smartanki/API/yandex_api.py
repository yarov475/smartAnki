#!/usr/bin/env python3

from __future__ import annotations
import os
import pathlib
from dotenv import load_dotenv
from yandex_cloud_ml_sdk import YCloudML

load_dotenv()

folder_id_token = os.getenv("FOLDER_ID")
yandex_api_key = os.getenv("Y_S_K")

def generate_yandex_image(word: str, output_dir: str = "anki_exports") -> dict | None:
    """
    Generate image from Yandex AI and return local file path.

    Returns:
        {"type": "path", "data": "/absolute/path/to/image.png"} or None
    """
    if not folder_id_token or not yandex_api_key:
        print("❌ Missing Yandex API credentials. Check .env (FOLDER_ID, Y_S_K).")
        return None

    try:
        print(f"🎨 Generating image for '{word}' via Yandex AI...")

        sdk = YCloudML(folder_id=folder_id_token, auth=yandex_api_key)
        model = sdk.models.image_generation("yandex-art").configure(width_ratio=1, height_ratio=1, seed=1863)

        operation = model.run_deferred(word)
        result = operation.wait()

        os.makedirs(output_dir, exist_ok=True)
        image_path = pathlib.Path(output_dir) / f"{word.replace(' ', '_')}_yandex.png"
        image_path.write_bytes(result.image_bytes)

        print(f"✅ Saved Yandex image: {image_path}")
        return {"type": "path", "data": str(image_path)}

    except Exception as e:
        print(f"❌ Yandex AI generation failed for '{word}': {e}")
        return None
