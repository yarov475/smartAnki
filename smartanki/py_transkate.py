# smartanki/translator_english.py

from argostranslate import translate, package
import os

def ensure_ru_en_model_installed():
    """Check and install RU → EN model if not yet installed."""
    installed_langs = translate.get_installed_languages()
    has_model = any(
        lang.code == "ru" and any(t.code == "en" for t in lang.translations)
        for lang in installed_langs
    )
    if not has_model:
        print("🌐 Downloading Argos RU→EN model (first time only)...")
        package.update_package_index()
        available = package.get_available_packages()
        ru_en_pkg = next(p for p in available if p.from_code == "ru" and p.to_code == "en")
        downloaded_path = ru_en_pkg.download()
        package.install_from_path(downloaded_path)
        print("✅ RU→EN model installed.")


from smartanki.translator_english import translate_ru_to_en

print(translate_ru_to_en("яблоко"))  # → apple


print(translate_ru_to_en("яблоко"))  # → apple
