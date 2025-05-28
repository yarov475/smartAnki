# from vocab_db import init_db, list_known_words
#
# init_db()  # Ensures DB exists
#
# words = list_known_words()
# print("Known words:", words)

import argostranslate.package
import argostranslate.translate

argostranslate.package.install_from_path("smartanki/argosmodel/m.zip")

installed_languages = argostranslate.translate.load_installed_languages()
print(installed_languages)
