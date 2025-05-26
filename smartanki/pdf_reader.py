import pdfplumber
import logging

# Suppress annoying CropBox logging from pdfminer
logging.getLogger("pdfminer").setLevel(logging.ERROR)


def read_pdf_text(path):
    full_text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
    return full_text
