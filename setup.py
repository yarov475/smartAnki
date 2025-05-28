import os
import sys
import re
import csv
from pathlib import Path
from smartanki.main_cli import main
from PyPDF2 import PdfReader

# Define paths
ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = ROOT / "input"
EXPORT_DIR = ROOT / "anki_exports"

# Utility function to simulate CLI
def run_smartanki_test(args, output_path=None):
    if output_path and output_path.exists():
        output_path.unlink()

    sys.argv = ["smartanki"] + args
    main()

    if output_path:
        assert output_path.exists(), f"❌ Expected file not created: {output_path}"
        assert output_path.stat().st_size > 0, f"❌ File is empty: {output_path}"
        output_path.unlink()


def test_txt_input_apkg():
    output = EXPORT_DIR / "Testing.apkg"
    run_smartanki_test([
        str(INPUT_DIR / "sample.txt"),
        "--no-save",
        "--deck-name", "Testing",
        "--offline-translate",
        "--export-apkg"
    ], output)


def test_pdf_input_apkg():
    output = EXPORT_DIR / "Testing.apkg"
    run_smartanki_test([
        str(INPUT_DIR / "sample.pdf"),
        "--no-save",
        "--deck-name", "Testing",
        "--offline-translate",
        "--export-apkg"
    ], output)


def test_csv_output():
    output = EXPORT_DIR / "anki_cards.csv"
    run_smartanki_test([
        str(INPUT_DIR / "sample.txt"),
        "--no-save",
        "--deck-name", "Testing",
        "--offline-translate"
    ], output)


def test_pdf_range_notranslate_apkg():
    output = EXPORT_DIR / "Testing.apkg"
    run_smartanki_test([
        str(INPUT_DIR / "sample.pdf"),
        "--no-save",
        "--deck-name", "Testing",
        "--offline-translate",
        "--export-apkg",
        "--pdf-pages", "1-3",
        "--not-translate"
    ], output)


def test_pdf_output():
    output = EXPORT_DIR / "wordlist.pdf"
    run_smartanki_test([
        str(INPUT_DIR / "sample.pdf"),
        "--no-save",
        "--deck-name", "Testing",
        "--offline-translate",
        "--pdf-output", str(output)
    ], output)


def test_translation_present_in_csv():
    output = EXPORT_DIR / "anki_cards.csv"
    input_path = INPUT_DIR / "sample.txt"

    # Run with translation
    sys.argv = [
        "smartanki",
        str(input_path),
        "--no-save",
        "--deck-name", "Testing",
        "--offline-translate"
    ]
    main()

    assert output.exists(), "❌ CSV file not created"

    with open(output, encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)

    assert len(rows) > 0, "❌ No rows in CSV"

    found = any(
        re.search(r"[A-Za-z]", " ".join(row)) and
        re.search(r"[А-Яа-яЁё]", " ".join(row))
        for row in rows
    )
    assert found, "❌ No row contains both English and Russian text"

    output.unlink()


def test_translation_in_pdf_output():
    output = EXPORT_DIR / "wordlist.pdf"
    input_path = INPUT_DIR / "sample.txt"

    sys.argv = [
        "smartanki",
        str(input_path),
        "--no-save",
        "--deck-name", "Testing",
        "--offline-translate",
        "--pdf-output", str(output)
    ]
    main()

    assert output.exists()

    reader = PdfReader(str(output))
    text = "\n".join([page.extract_text() or "" for page in reader.pages])

    assert re.search(r"[A-Za-z]", text), "❌ No English found in PDF"
    assert re.search(r"[А-Яа-яЁё]", text), "❌ No Russian found in PDF"

    output.unlink()
