# smartanki/translator.py

from googletrans import Translator

translator = Translator()

def translate_to_russian(text: str) -> str:
    try:
        result = translator.translate(text, src="en", dest="ru")
        return result.text
    except Exception as e:
        print(f"❌ Google Translate failed for: '{text[:80]}...': {e}")
        return ""
