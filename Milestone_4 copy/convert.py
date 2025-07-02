class Convert:
    @staticmethod
    def convert_to_int(word):
        try:
            return int(word.strip())
        except ValueError:
            return False
