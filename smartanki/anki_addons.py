# from anki.importing import TextImporter
# from anki.importing.apkg import AnkiPackageImporter
# from aqt import mw
#
#
# def import_text_file(file_path, deck_name):
#     # Select or create deck
#     did = mw.col.decks.id(deck_name)
#     mw.col.decks.select(did)
#
#     # Set note type
#     m = mw.col.models.byName("Basic")
#     deck = mw.col.decks.get(did)
#     deck['mid'] = m['id']
#     mw.col.decks.save(deck)
#     m['did'] = did
#
#     # Import the file
#     ti = TextImporter(mw.col, file_path)
#     ti.initMapping()
#     ti.run()
#
#
# def import_apkg_file(apkg_path):
#     imp = AnkiPackageImporter(mw.col, apkg_path)
#     imp.run()
