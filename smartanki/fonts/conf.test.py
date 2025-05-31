import json
from pathlib import Path

def load_config():
    config_path = Path(".smartanki_config.json")
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}
