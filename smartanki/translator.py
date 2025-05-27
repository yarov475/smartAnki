# smartanki/translator.py
from transformers import MarianMTModel, MarianTokenizer
from typing import Optional
from googletrans import Translator as GoogleTranslator

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
except (OSError, FileNotFoundError) as e: # More specific errors for model file issues
    print(f"[⚠] Hugging Face model '{_hf_model_name}' failed to load. This can be due to missing model files (ensure it's downloaded, e.g., by running with internet first) or network issues. Error: {e}")
    _hf_translator = None
except Exception as e: # General catch for other init errors
    print(f"[⚠] Hugging Face model init failed: {e}")
    _hf_translator = None

# Initialize Google Translate as fallback
_google_translator = GoogleTranslator()

def translate_to_russian(text: str, offline_only: bool = False, force_google: bool = False) -> Optional[str]:
    """
    Translate English text to Russian.
    Allows specifying translation method: force Google, offline only, or hybrid (offline first).
    """
    if force_google:
        try:
            result = _google_translator.translate(text, src="en", dest="ru")
            return result.text
        except Exception as e:
            print(f"[⚠] Google Translate failed: {e}")
            return None
    elif offline_only:
        if _hf_translator:
            try:
                return _hf_translator.translate(text)
            except Exception as e:
                print(f"[⚠] Offline translation failed. Helsinki-NLP/opus-mt-en-ru model may not be available or configured correctly. Please ensure it's downloaded and accessible by the Hugging Face transformers library. No fallback to online translation. Error: {e}")
                return None
        else:
            print(f"[⚠] Offline translation failed. Helsinki-NLP/opus-mt-en-ru model may not be available or configured correctly. Please ensure it's downloaded and accessible by the Hugging Face transformers library. No fallback to online translation.")
            return None
    else: # Default: try Hugging Face first, then Google Translate
        if _hf_translator:
            try:
                return _hf_translator.translate(text)
            except Exception as e:
                print(f"[⚠] Local Hugging Face translation failed: {e}")
        # Fallback to Google Translate
        try:
            result = _google_translator.translate(text, src="en", dest="ru")
            return result.text
        except Exception as e:
            print(f"[⚠] Google Translate failed: {e}")
            return None
