class Convert:
    @staticmethod
    def convert_to_int(word):
        try:
            if isinstance(word, int):
                return word
            return int(word.strip())
        except Exception:
            return False
