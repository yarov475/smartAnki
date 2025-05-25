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

    def get_cefr_level(self, word: str):
        word = word.lower().strip()
        if word in self.cefr_dict:
            return self.cefr_dict[word]

        try:
            fallback_level = self.analyzer.get_average_word_level_CEFR(word)
            if fallback_level is not None:
                return str(fallback_level)  # ✅ Ensure it's a string like "B2"
        except Exception as e:
            print(f"⚠️ Fallback CEFR failed for '{word}': {e}")

        return None

    def is_above_user_level(self, word: str) -> bool:
        level = self.get_cefr_level(word)
        if not level:
            return True  # Treat unknown words as above level
        return CEFR_RANK.get(level, 99) > self.user_rank
