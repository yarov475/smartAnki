# smartanki_gui.py
import sys
import os
from argparse import Namespace

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit,
    QPushButton, QFileDialog, QLabel, QHBoxLayout
)
from PyQt6.QtGui import QIcon

from smartanki.pdf_reader import read_pdf_text
from smartanki.run_CLI import handle_run  # <-- This is your CLI logic refactored into a function
from smartanki.utils import parse_page_range

class SmartAnkiGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📘 SmartAnki - GUI Mode")
        self.setGeometry(100, 100, 900, 600)
        self.file_path = None

        # Widgets
        self.layout = QVBoxLayout()
        self.label = QLabel("📄 Enter text or load a file:")
        self.text_edit = QTextEdit()

        self.load_file_btn = QPushButton("📂 Load File")
        self.run_btn = QPushButton("🚀 Generate Anki Deck")

        # Output info
        self.status_label = QLabel("")

        # Layout
        button_row = QHBoxLayout()
        button_row.addWidget(self.load_file_btn)
        button_row.addWidget(self.run_btn)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text_edit)
        self.layout.addLayout(button_row)
        self.layout.addWidget(self.status_label)

        self.setLayout(self.layout)

        # Signals
        self.load_file_btn.clicked.connect(self.load_file)
        self.run_btn.clicked.connect(self.run_smartanki)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text/PDF Files (*.txt *.pdf)")
        if file_path:
            self.file_path = file_path
            try:
                if file_path.lower().endswith(".txt"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        self.text_edit.setPlainText(f.read())
                    self.status_label.setText(f"✅ Loaded text from: {file_path}")
                elif file_path.lower().endswith(".pdf"):
                    pdf_text = read_pdf_text(file_path)
                    self.text_edit.setPlainText(pdf_text)
                    self.status_label.setText(f"✅ Loaded PDF from: {file_path}")
                else:
                    self.text_edit.setPlainText("")  # Don't preview unsupported file types
                    self.status_label.setText(f"📌 File type not supported: {file_path}")
            except Exception as e:
                self.status_label.setText(f"❌ Error reading file: {e}")

    def run_smartanki(self):
        if not self.text_edit.toPlainText() and not self.file_path:
            self.status_label.setText("❗ Please load a file or enter text first.")
            return

        args = Namespace(
            filepath=self.file_path,
            cefr="B2",
            csv=None,
            no_save=False,
            no_lemmatize=False,
            not_translate=False,
            export_apkg=True,
            apkg="anki_exports/gui_output.apkg",
            deck_name="SmartAnki GUI Deck",
            tags=[],
            debug_cefr=False,
            offline_translate=False,
            force_google=False,
            with_images= False,
            force_ai_image=False,
            top_n=None,
            pdf_pages=None,
            pdf_output=None,
            import_anki_csv=None,
            only_import_anki=False,
            import_to_anki=False,
        )

        try:
            handle_run(args, override_text=self.text_edit.toPlainText())
            self.status_label.setText("✅ Anki deck created: anki_exports/gui_output.apkg")
        except Exception as e:
            self.status_label.setText(f"❌ Failed: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SmartAnkiGUI()
    window.show()
    sys.exit(app.exec())
