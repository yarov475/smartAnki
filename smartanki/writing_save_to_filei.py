import datetime
import os
import re


def save_yo_file(glossary, grammar_matches, spelling_errors, unknown_words, user_input):
    os.makedirs("writing_logs", exist_ok=True)
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    words = user_input.split()
    first_words = "-".join(words[:2]) if words else "untitled"
    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '', first_words)
    filename = f"{date}-{safe_name}.txt"
    filepath = os.path.join("writing_logs", filename)
    if unknown_words:
        print(f' ⚠️Не найдено: {unknown_words}\n')
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("✍️ Your Writing:\n")
        f.write(user_input + "\n\n")

        if glossary:
            f.write("📚 Glossary:\n")
            for word, info in glossary.items():
                f.write(f"- {word}: {info['phonetic']} — {info['definition']}\n")
                if info.get("example"):
                    f.write(f"  Example: {info['example']}\n")

        if spelling_errors:
            f.write("\n❌ Misspelled Words:\n")
            for item in spelling_errors:
                if isinstance(item, tuple) and len(item) == 2:
                    word, suggestion = item
                    f.write(f"- {word} ➜ {suggestion}\n")
                else:
                    f.write(f"- {item}\n")

        if grammar_matches:
            f.write("\n🧠 Grammar Suggestions:\n")
            for m in grammar_matches:
                suggestions = f" [Suggestions: {', '.join(m.replacements)}]" if m.replacements else ""
                f.write(f"- {m.message}{suggestions}\n")
        if unknown_words:
            for w in unknown_words:
                f.write(f"  ⚠️ {w}\n")
    return filepath
