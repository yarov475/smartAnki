# smartanki/translator.py
import argostranslate.package

argostranslate.package.install_from_path("smartanki/agrosmodel/en_ru.argosmodel")
from typing import Optional
from googletrans import Translator as GoogleTranslator

# Try to load Argos Translate
try:
    from argostranslate import package, translate as argos_translate
    argos_languages = argos_translate.load_installed_languages()
    en = next((lang for lang in argos_languages if lang.code == "en"), None)
    ru = next((lang for lang in argos_languages if lang.code == "ru"), None)
    _local_translator = en.get_translation(ru) if en and ru else None
except Exception as e:
    print(f"[⚠] Argos Translate init failed: {e}")
    _local_translator = None

_google_translator = GoogleTranslator()


def translate_to_russian(text: str, force_google=False, offline_only=False) -> str:
    """
    Translate English text to Russian using Argos Translate (offline),
    with optional fallback to Google Translate (online).
    """
    if offline_only:
        if _local_translator:
            try:
                return _local_translator.translate(text)
            except Exception as e:
                print(f"[❌ Argos failed] {e}")
        return "[translation unavailable (offline only)]"

    if force_google:
        return _translate_with_google(text)

    # Try Argos first
    if _local_translator:
        try:
            result = _local_translator.translate(text)
            if result.strip():
                return result
        except Exception as e:
            print(f"[Argos failed] {e}")

    # Fall back to Google Translate
    return _translate_with_google(text)


def _translate_with_google(text: str) -> str:
    try:
        return _google_translator.translate(text, src="en", dest="ru").text
    except Exception as e:
        print(f"[Google Translate failed] {e}")
        return "[translation unavailable]"
