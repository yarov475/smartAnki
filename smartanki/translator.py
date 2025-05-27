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
except Exception as e:
    print(f"[⚠] Hugging Face model init failed: {e}")
    _hf_translator = None

# Initialize Google Translate as fallback
_google_translator = GoogleTranslator()

def translate_to_russian(text: str, use_local: bool = True) -> Optional[str]:
    """
    Translate English text to Russian.
    If use_local=True and Hugging Face model loaded successfully, use it.
    Otherwise, fallback to Google Translate.
    """
    if use_local and _hf_translator:
        try:
            return _hf_translator.translate(text)
        except Exception as e:
            print(f"[⚠] Local translation failed: {e}")
    # fallback
    try:
        result = _google_translator.translate(text, src="en", dest="ru")
        return result.text
    except Exception as e:
        print(f"[⚠] Google Translate failed: {e}")
        return None
