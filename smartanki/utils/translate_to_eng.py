# smartanki/translator.py

from transformers import MarianMTModel, MarianTokenizer
from typing import Optional


class HuggingFaceTranslator_to_eng:
    def __init__(self, model_name: str):
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name)

    def translate_to_eng(self, text: str) -> str:
        inputs = self.tokenizer(text, return_tensors="pt", padding=True)
        translated_tokens = self.model.generate(**inputs)
        translated_text = self.tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
        return translated_text


# Initialize Hugging Face translator for English → Russian
_hf_model_name_en = "Helsinki-NLP/opus-mt-ru-en"
try:
    _hf_translator = HuggingFaceTranslator_to_eng(_hf_model_name_en)
except (OSError, FileNotFoundError) as e:
    print(f"[⚠] Hugging Face model '{_hf_model_name_en}' failed to load. "
          f"Make sure the model is downloaded for offline use. Error: {e}")
    _hf_translator = None
except Exception as e:
    print(f"[⚠] Unexpected error initializing Hugging Face translator: {e}")
    _hf_translator = None


def translate_to_english(text: str, offline_only: bool = False, force_google: bool = False) -> Optional[str]:
    """
    Translate English text to Russian using Hugging Face model only.
    Google Translate is removed. This version is fully offline.
    """
    if not _hf_translator:
        print("[⚠] Offline translator not available.")
        return None

    try:
        return _hf_translator.translate_to_eng(text)
    except Exception as e:
        print(f"[⚠] Offline translation failed. Ensure the Hugging Face model is available offline. Error: {e}")
        return None



