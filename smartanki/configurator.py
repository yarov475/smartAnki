import json
from pathlib import Path

def setup_config_interactively():
    print("🛠 SmartAnki Configuration Wizard")

    unsplash_key = input("🔑 Enter Unsplash API key: ").strip()
    yandex_key = input("🎨 Enter Yandex Vision/Art API key: ").strip()
    input_dir = input("📂 Default input folder (e.g., input/): ").strip()
    output_dir = input("📁 Default output folder (e.g., anki_exports/): ").strip()

    config = {
        "UNSPLASH_ACCESS_KEY": unsplash_key,
        "YANDEX_KEY": yandex_key,
        "INPUT_DIR": input_dir,
        "EXPORT_DIR": output_dir,
    }

    config_path = Path(".smartanki_config.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    print(f"✅ Config saved to {config_path.resolve()}")
