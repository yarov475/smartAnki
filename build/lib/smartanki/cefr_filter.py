# cefr_filter.py

import csv
import re

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

    def is_above_user_level(self, word: str) -> bool:
        word = word.lower().strip()
        word_level = self.cefr_dict.get(word)
        if not word_level:
            # Word not in list, assume it's above level
            return True
        return CEFR_RANK[word_level] > self.user_rank

    def filter_words(self, words):
        """Return only words above the user's CEFR level."""
        return [w for w in words if self.is_above_user_level(w)]
