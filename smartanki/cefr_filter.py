# smartanki/cefr_filter.py

import csv
import re
from cefrpy import CEFRAnalyzer

CEFR_RANK = {
    'A1': 1, 'A2': 2,
    'B1': 3, 'B2': 4,
    'C1': 5, 'C2': 6
}


class CEFRFilter:
    def __init__(self, csv_path: str, user_level: str):
        self.cefr_dict = {}  # word → level
        self.user_level = user_level.upper()
        self.user_rank = CEFR_RANK[self.user_level]
        self.analyzer = CEFRAnalyzer()  # ✅ Use correct class
        self.load_cefr_csv(csv_path)

    def load_cefr_csv(self, csv_path):
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 2:
                    continue
                raw_word, level = row[0].strip(), row[1].strip().upper()
                for w in re.split(r'[/,]', raw_word):
                    word = w.strip().lower()
                    self.cefr_dict[word] = level

    def get_cefr_level(self, word: str, debug=False):
        word = word.lower().strip()

        if word in self.cefr_dict:
            level = self.cefr_dict[word]
            if debug:
                print(f"[DEBUG] CEFR level for '{word}': {level} (source: csv)")
            return level, "csv"

        try:
            fallback_level = self.analyzer.get_average_word_level_CEFR(word)
            if fallback_level is not None:
                level_str = str(fallback_level)
                if debug:
                    print(f"[DEBUG] CEFR level for '{word}': {level_str} (source: cefrpy)")
                return level_str, "cefrpy"
        except Exception as e:
            if debug:
                print(f"[DEBUG] Failed to classify '{word}' via cefrpy: {e}")

        return None, "unknown"

    def is_above_user_level(self, word: str, debug=False) -> bool:
        level, source = self.get_cefr_level(word, debug=debug)
        if not level:
            return True  # Assume it's advanced
        return CEFR_RANK.get(level, 99) > self.user_rank

