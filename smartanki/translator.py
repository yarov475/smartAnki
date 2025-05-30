# smartanki/translator.py

from transformers import MarianMTModel, MarianTokenizer
from typing import Optional

class HuggingFaceTranslator:
    def __init__(self, model_name: str):
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name)

    def translate(self, text: str) -> str:
        inputs = self.tokenizer(text, return_tensors="pt", padding=True)
        translated_tokens = self.model.generate(**inputs)
        translated_text = self.tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
        return translated_text

# Initialize Hugging Face translator for English → Russian
_hf_model_name = "Helsinki-NLP/opus-mt-en-ru"
try:
    _hf_translator = HuggingFaceTranslator(_hf_model_name)
except (OSError, FileNotFoundError) as e:
    print(f"[⚠] Hugging Face model '{_hf_model_name}' failed to load. "
          f"Make sure the model is downloaded for offline use. Error: {e}")
    _hf_translator = None
except Exception as e:
    print(f"[⚠] Unexpected error initializing Hugging Face translator: {e}")
    _hf_translator = None

def translate_to_russian(text: str, offline_only: bool = False, force_google: bool = False) -> Optional[str]:
    """
    Translate English text to Russian using Hugging Face model only.
    Google Translate is removed. This version is fully offline.
    """
    if not _hf_translator:
        print("[⚠] Offline translator not available.")
        return None

    try:
        return _hf_translator.translate(text)
    except Exception as e:
        print(f"[⚠] Offline translation failed. Ensure the Hugging Face model is available offline. Error: {e}")
        return None
