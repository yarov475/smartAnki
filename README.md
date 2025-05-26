# Smart Anki Vocabulary Builder

This project helps language learners identify and learn new vocabulary from texts. It leverages your Common European Framework of Reference for Languages (CEFR) level to tailor the vocabulary extraction process, ensuring you focus on words that are most relevant to your learning stage. Extracted vocabulary can then be easily exported for use with Anki, a popular spaced repetition flashcard program.

## Features

- **CEFR Level Filtering:** The tool utilizes a CEFR wordlist to pinpoint words that are above the user's designated language proficiency level (e.g., B2). This ensures that learners are challenged with new vocabulary appropriate for their current stage.
- **New Word Extraction:** Input text is processed and tokenized (broken down into individual words). The tool then identifies words that are not already part of the user's known vocabulary, focusing on unfamiliar terms.
- **Vocabulary Database:** A local SQLite database (`db/user_words.db`) stores all the words the user has already learned. This prevents repetition of known vocabulary. New words identified by the tool are automatically added to this database.
- **Anki CSV Export:** The application generates a CSV file (`anki_exports/anki_cards.csv`) formatted for easy import into Anki. Each entry in the CSV includes the new word, a placeholder for its phonetic transcription, its definition, and an example sentence (definitions and example sentences are sourced from WordNet).

## How to Use

### Prerequisites

1.  **Python 3.x:** Ensure you have Python 3 installed.
2.  **Install Libraries:** Install the necessary Python libraries using pip:
    ```bash
    pip install spacy nltk
    ```
3.  **Download spaCy Model:** Download the English language model for spaCy:
    ```bash
    python -m spacy download en_core_web_sm
    ```
4.  **Download NLTK Data:** Download the WordNet corpus for NLTK:
    ```bash
    python -m nltk.downloader wordnet
    ```

### Running the Project

1.  **Main Script:** The primary script for the project is `main.py`.
2.  **Input Text:** Open `main.py` and modify the `text` variable to include the text you want to analyze.
    ```python
    # Example in main.py
    text = """Your multiline text goes here.
    It can span across several lines.
    This is the content the script will process to find new vocabulary.
    """
    ```
3.  **Execute:** Run the script from your terminal:
    ```bash
    python main.py
    ```
    This will:
    *   Extract new words from the provided `text` that are above your specified CEFR level and not already in your vocabulary database.
    *   Save these new words to the `db/user_words.db` database.
    *   Generate an Anki-ready CSV file at `anki_exports/anki_cards.csv`.

### Customizing CEFR Level

-   You can adjust the target CEFR level by modifying the `user_level` variable in `main.py`. For example, to set your level to B1, change it to:
    ```python
    # In main.py
    user_level = 'B1'
    ```
    The script will then filter words against the B1 CEFR wordlist.

### Importing Known Words

-   If you have an existing list of known words (e.g., from an Anki export), you can import them into the vocabulary database.
-   The `vocab_db.py` script contains a function `import_from_csv(csv_filepath)` for this purpose.
-   **How to use:**
    1.  Ensure your known words are in a CSV file where the first column contains the words. The default path for this user data CSV is `data/user_anki.csv`.
    2.  You can call this function by:
        *   Uncommenting and modifying the relevant lines in `main.py`:
            ```python
            # In main.py, within the if __name__ == "__main__": block (or elsewhere as needed)
            # from vocab_db import import_from_csv
            # import_from_csv('data/user_anki.csv') # Make sure the path is correct
            ```
        *   Or by running it as a separate Python script execution, ensuring you properly initialize the database connection if needed.
-   Importing your known words will prevent the tool from suggesting words you've already learned.

## Project Structure

### Python Files

-   `main.py`: The main script to run the vocabulary extraction and Anki export process.
-   `extractor.py`: Contains the logic for extracting new words from text using spaCy and CEFR filtering.
-   `vocab_db.py`: Manages the SQLite database of known words.
-   `anki_export.py`: Generates the Anki-compatible CSV file with definitions and examples.
-   `cefr_filter.py`: Filters words based on the CEFR level.
-   `utils.py`: Contains utility functions used across the project. *(Note: This file might be empty or not present if no common utilities have been identified yet.)*

### Directories

-   `data/`: Contains data files like the CEFR wordlist (`cefr_wordlist.csv`) and example user Anki CSV (`user_anki.csv`).
-   `db/`: Stores the user's vocabulary database (`user_words.db`).
-   `anki_exports/`: The default output directory for generated Anki CSV files (e.g., `anki_cards.csv`).
-   `.idea/`: This directory contains project-specific settings for IDEs like PyCharm or IntelliJ. It can generally be ignored if you are using a different editor or not modifying project configurations.

## Future Improvements / Contributing

This project is a starting point, and there are many ways it could be enhanced:

-   **Phonetic Transcriptions:** Integrate a proper phonetic transcription service or library (e.g., using an API or a local tool) to replace the current placeholder in the Anki export.
-   **Multi-language Support:** Extend the tool to support languages other than English. This would involve finding or creating CEFR-equivalent wordlists for other languages and adapting the NLP pipeline (e.g., using different spaCy models).
-   **Graphical User Interface (GUI):** Develop a simple GUI (e.g., using Tkinter, PyQt, or a web framework like Flask/Django) to make the tool more accessible for non-programmers. This could allow users to easily input text, set their CEFR level, and manage their vocabulary database without editing Python scripts.
-   **Enhanced Example Sentences:** Implement an option to fetch example sentences from alternative sources if WordNet does not provide a suitable one, or to allow users to choose their preferred source.
-   **Multi-Word Expressions:** Improve the handling of multi-word expressions, idioms, and phrasal verbs. Currently, the tool primarily focuses on single-word tokens.
-   **Customizable CEFR Wordlists:** Provide instructions or a script for users to build, update, or customize the CEFR wordlist from other linguistic resources or their own data.
-   **Contextual Definitions:** Fetch multiple definitions or definitions that are more context-aware based on the input text.
-   **Interactive Learning:** Add features for interactive review or learning of the new words directly within the application.

Contributions are welcome! Please feel free to fork the repository, make your changes, and submit a pull request. If you have ideas for other features or improvements, don't hesitate to open an issue to discuss them.

## License

This project is licensed under the MIT License.
