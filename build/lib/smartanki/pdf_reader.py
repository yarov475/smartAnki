import pdfplumber

def read_pdf_text(path):
    full_text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
    return full_text
