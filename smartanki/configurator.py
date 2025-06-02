import json
from pathlib import Path

def setup_config_interactively():
    print("🔧 Initializing SmartAnki config...")
    unsplash = input("🔑 Enter your Unsplash API key: ").strip()
    huggingface = input("🔑 Enter your Hugging Face token: ").strip()
    input =  input("📁 Enter default output folder (or leave empty for 'input'): ").strip() or "input"
    output = input("📁 Enter default output folder (or leave empty for 'anki_exports'): ").strip() or "anki_exports"

    with open(".env", "w", encoding="utf-8") as f:
        f.write(f"UNSPLASH_ACCESS_KEY={unsplash}\n")
        f.write(f"HUGGINGFACE_TOKEN={huggingface}\n")
        f.write(f"INPUT_FOLDER={input}\n")
        f.write(f"OUTPUT_FOLDER={output}\n")

    print("✅ .env file created!")
