from memory import Memory
from convert import Convert
from file_converter import FileConverter

class Load_Program:
    def __init__(self):
        self.memory = Memory()

    def detect_format(self, lines):
        stripped = [ln.strip() for ln in lines if ln.strip()]
        if all(len(ln) == 4 for ln in stripped) and len(stripped) <= 100:
            return '4'
        elif all(len(ln) == 6 for ln in stripped) and len(stripped) <= 250:
            return '6'
        else:
            raise ValueError("Unknown or mixed file format")

    def load_program(self, filename):
        lines = open(filename, "r").readlines()
        fmt = self.detect_format(lines)
        for idx, ln in enumerate(lines):
            if idx >= 250:
                raise ValueError("File exceeds max 250 lines")
            word = ln.strip()
            if not word:
                continue
            if fmt == '4':
                word = FileConverter.convert_4_to_6(word)
            val = Convert.convert_to_int(word)
            if val is False:
                raise ValueError(f"Invalid word at memory[{idx:03d}]")
            self.memory.write(idx, val)
