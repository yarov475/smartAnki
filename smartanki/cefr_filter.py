from cefrpy import CEFRAnalyzer

from smartanki.utils import clean_word

CEFR_RANK = {
    'A1': 1, 'A2': 2,
    'B1': 3, 'B2': 4,
    'C1': 5, 'C2': 6
}


class CEFRFilter:
    def __init__(self, user_level: str):
        self.user_level = user_level
        self.user_rank = self.rank_cefr(user_level)
        self.analyzer = CEFRAnalyzer()

    def is_above_user_level(self, word: str, debug: bool = False) -> bool:
        word = clean_word(word)
        level, _ = self.get_cefr_level(word, debug=debug)
        if level is None:
            if debug:
                print(f"⚠️ CEFR missing for '{word}' – treating as advanced")
            return True
        return self.rank_cefr(level) > self.user_rank

    def get_cefr_level(self, word: str, debug: bool = False):
        word = clean_word(word)
        try:
            cefr_obj = self.analyzer.get_average_word_level_CEFR(word)
            # Convert CEFRLevel object to string
            cefr_str = str(cefr_obj) if cefr_obj is not None else None
            if debug:
                print(f"🧠 CEFR ({word}) = {cefr_str}")
            return cefr_str, "cefrpy"
        except Exception as e:
            if debug:
                print(f"Error getting CEFR for {word}: {e}")
            return None, None

    def rank_cefr(self, level: str) -> int:
        if level is None:
            return 99
        # Ensure level is a string
        level_str = str(level) if not isinstance(level, str) else level
        return CEFR_RANK.get(level_str, 99)
