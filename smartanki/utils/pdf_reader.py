import pdfplumber
import logging

logging.getLogger("pdfminer").setLevel(logging.ERROR)

def read_pdf_text(path, page_range=None):
    full_text = ""
    with pdfplumber.open(path) as pdf:
        start = 0
        end = len(pdf.pages) - 1
        if page_range:
            start, end = page_range
            end = min(end, len(pdf.pages) - 1)

        for i in range(start, end + 1):
            page = pdf.pages[i]
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    return full_text
