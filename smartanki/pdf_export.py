# smartanki/pdf_export.py

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import cm
from smartanki.dictionary_api import get_word_data

def export_wordlist_to_pdf(word_sentence_map, output_path="anki_exports/wordlist.pdf"):
    doc = SimpleDocTemplate(output_path, pagesize=A4, title="SmartAnki Word List")
    styles = getSampleStyleSheet()
    elements = []

    for word, sentence in word_sentence_map.items():
        word_info = get_word_data(word)
        if not word_info:
            continue

        # Word title
        entry = f"<b>{word_info['word']}</b>  <i>{word_info['phonetic']}</i><br/>"
        # Definition
        entry += f"<b>Definition:</b> {word_info['definition']}<br/>"
        # Example
        entry += f"<b>Example:</b> {sentence}<br/><br/>"

        elements.append(Paragraph(entry, styles["Normal"]))
        elements.append(Spacer(1, 0.5 * cm))

    doc.build(elements)
    print(f"📝 PDF word list saved to: {output_path}")
