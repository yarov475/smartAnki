# smartanki/handle_writing.py

from smartanki.utils.writing_cli_extracting import extracting
from smartanki.utils.writing_greating import greeting
from smartanki.utils.writing_utils import check_spelling, check_grammar


def handle_writing(args):
    greeting()

    # Read multi-line user input until Ctrl+C
    lines = []
    try:
        while True:
            try:
                line = input()
                lines.append(line)
            except EOFError:
                break
    except KeyboardInterrupt:
        print("\n🛑 Input interrupted. Processing what you wrote...\n")

    user_input = "\n".join(lines).strip()
    if not user_input:
        print("❗ No input provided.")
        return

    print("\n📄 Processing your writing...\n")

    glossary = {}
    unknown_words = []
    grammar_matches = check_grammar(user_input)
    spelling_errors = check_spelling(user_input)

    # 🧠 Extract Russian words in brackets: [Пиренеи]
    extracting(glossary, grammar_matches, spelling_errors, unknown_words, user_input)


