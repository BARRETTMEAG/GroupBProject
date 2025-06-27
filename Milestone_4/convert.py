class Convert:
    @staticmethod
    def convert_to_int(word):
        try:
            i = int(word)
            if -9999 <= i <= 9999:
                return i
        except:
            pass
        return False
