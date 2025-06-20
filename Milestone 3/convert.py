class Convert:
    @staticmethod
    def convert_to_int(word):
        try:
            int(word)
            return int(word)
        except ValueError:
            return False