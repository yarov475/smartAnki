# smartanki

📘 SmartAnki – Extract CEFR-based vocabulary and generate Anki flashcards from text or PDF.

## Features

- Extracts vocabulary from `.txt` and `.pdf` files.
- Filters vocabulary based on CEFR (Common European Framework of Reference for Languages) levels.
- Allows users to specify their target CEFR level.
- Saves new and known words to a local database to track learning progress.
- Lemmatizes words to their base form.
- Provides example sentences for new words.
- Can translate example sentences (optional).
- Exports flashcards to:
    - CSV format (compatible with Anki import).
    - Native Anki `.apkg` package format.
- Allows adding custom tags to Anki cards.
- Supports custom naming for the generated Anki deck.
- Can import a list of known words from an Anki-exported CSV file.
- Can export the extracted wordlist to a PDF document for review.
- Easy-to-use Command-Line Interface (CLI).

## Installation

1.  **Clone the repository (or download the source code):**
    ```bash
    git clone <repository-url> # Replace <repository-url> with the actual URL
    cd smartanki
    ```

2.  **Ensure you have Python 3.10 or higher.**

3.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
    Then install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
    Or, if you want to install the package itself (e.g., for CLI usage):
    ```bash
    pip install .
    ```

### Dependencies

The project uses the following main libraries:
-   `spacy`
-   `nltk`
-   `requests`
-   `pdfplumber`
-   `beautifulsoup4`

(These will be installed automatically by `pip install -r requirements.txt` or `pip install .`)

## Usage

`smartanki` is a command-line tool. After installation, you can run it using the `smartanki` command.

### Basic Command

```bash
smartanki <filepath> [options]
```

-   `<filepath>`: (Required) Path to the input file (`.pdf` or `.txt`).

### Options

Here are the available command-line options:

-   `--cefr <level>`: Specify your target CEFR level for vocabulary extraction.
    -   Example: `B1`, `B2`, `C1`.
    -   Default: `B2`.
-   `--csv <output_path>`: Path to save the generated Anki cards in CSV format.
    -   Default: `anki_exports/anki_cards.csv`.
-   `--no-save`: If set, new words found will not be saved to the local vocabulary database.
-   `--not-translate`: If set, example sentences for words will not be translated.
-   `--no-lemmatize`: If set, words will not be lemmatized (i.e., reduced to their base form).
-   `--export-apkg`: If set, generates an Anki `.apkg` package instead of a CSV file.
    -   The package will be saved in the `anki_exports/` directory with a name based on `--deck-name`.
-   `--tags <tag1> <tag2> ...`: Add custom tags to each generated Anki card.
    -   Example: `--tags Chapter1 Literature`.
-   `--deck-name "<name>"`: Specify the name for the Anki deck when using `--export-apkg`.
    -   Default: `"SmartAnki Vocabulary Deck"`.
-   `--debug-cefr`: If set, prints detailed CEFR filtering information during processing.
-   `--import-anki-csv <path_to_anki_csv>`: Import words you already know from an Anki-exported CSV file. This helps `smartanki` identify truly *new* words for you.
    -   The CSV can be in any format, as the tool will guide you through mapping columns.
-   `--pdf-pages <start-end>`: Specify a page range to extract text from a PDF file.
    -   Example: `2-5` (extracts pages 2, 3, 4, and 5). Note: The first page is 1.
-   `--only-import-anki`: If set along with `--import-anki-csv`, the tool will only perform the import operation and then exit, without processing an input file.
-   `--pdf-output <path_to_pdf>`: Optional path to save the extracted wordlist (words and example sentences) as a PDF document.
    -   Example: `--pdf-output my_wordlist.pdf`.

### Examples

1.  **Extract words from a PDF, targeting B1 level, and export to CSV:**
    ```bash
    smartanki input/my_book.pdf --cefr B1 --csv output/my_book_cards.csv
    ```

2.  **Extract words from a text file, generate an Anki package, and add tags:**
    ```bash
    smartanki input/article.txt --export-apkg --deck-name "Article Vocab" --tags CurrentEvents Reading
    ```

3.  **Import known words from an Anki CSV, then process a PDF for C1 words, disabling translation:**
    ```bash
    smartanki input/dune.pdf --import-anki-csv path/to/my_known_words.csv --cefr C1 --not-translate
    ```

4.  **Extract words from specific pages of a PDF:**
    ```bash
    smartanki input/research_paper.pdf --pdf-pages 3-10
    ```

5.  **Only import known words from an Anki CSV and exit:**
    ```bash
    smartanki --import-anki-csv path/to/my_anki_export.csv --only-import-anki
    ```

## How it Works (Briefly)

1.  **Initialization**: The application initializes its database (to store known words) and loads the CEFR word lists. If you provide an Anki CSV export, your known words are imported into this database.
2.  **File Reading**: The input file (`.txt` or `.pdf`) is read. For PDFs, a specified page range can be used.
3.  **Text Analysis & Word Extraction**: The text is processed using `spacy` for natural language understanding. Words are extracted, lemmatized (unless disabled), and compared against your known words database and the target CEFR level.
4.  **New Word Identification**: Words that are not in your known words database and are at or above your specified CEFR level (or not found in CEFR lists, thus assumed to be advanced/specific) are considered "new."
5.  **Context & Translation**: For each new word, an example sentence is extracted from the source text. This sentence can optionally be translated (using an external API).
6.  **Database Update**: New words are typically saved to your local database (unless disabled with `--no-save`).
7.  **Export**: The list of new words, along with their example sentences and translations (if any), is formatted and exported to either a CSV file or an Anki `.apkg` package. Optionally, a PDF wordlist can also be generated.

## Contributing

Contributions are welcome! If you have suggestions for improvements or bug fixes, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature` or `bugfix/YourBugFix`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/YourFeature`).
6.  Open a Pull Request.

Please ensure your code follows the existing style and that any new features are appropriately documented.

## License

This project is licensed under the MIT License. See the `LICENSE.md` file for details (if one exists, or specify your license otherwise).
