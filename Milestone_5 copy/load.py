
import os
from convert import Convert
from memory import Memory


class Load_Program():

    def __init__(self):
        self.memory = Memory()

    def load_program(self, filename):
        i = 0
        firstWordLength = 0
        wordConsistencyEnforcer = 0
        word = ""
        if os.path.isfile(filename):
            with open(filename, "r") as file:
                while True:
                    char = file.read(1)
                    if not char:
                        if word and word != '\n' and word != '\t':
                            
                            cleaned = word.strip()  # ADDED
                            unsigned = cleaned.lstrip("+-")  # ADDED

                            # Enforce 4 or 6 digits only (reject 5-digit words)  # ADDED
                            if len(unsigned) not in (4, 6):
                                raise ValueError(f"Only 4-digit or 6-digit words allowed. Invalid word at memory [{i}]: '{cleaned}'")

                            if '+' in word or '-' in word:
                                if len(word) > 8:
                                    raise ValueError(f"Improper word length at memory [{i}]")
                                else:
                                    instruction = Convert.convert_to_int(cleaned)  # use cleaned
                            else:
                                if len(word) > 7:
                                    raise ValueError(f"Improper word length at memory [{i}]")
                                else:
                                    instruction = Convert.convert_to_int(cleaned)  # use cleaned

                            if instruction is False:
                                raise ValueError(f"Invalid word at memory [{i}]")

                            # Validate instruction range (ADDED)
                            if not (-999999 <= instruction <= 999999):
                                raise ValueError(f"Instruction out of range at memory [{i}]: {instruction}")

                            print(f"Loading instruction at memory[{i}]: '{cleaned}' -> {instruction}")  # ADDED DEBUG

                            self.memory.write(i, instruction)
                        break
                    word += char
                    if char.isspace():
                        if char == '\n':
                            stripped = word.strip()  # ADDED
                            unsigned = stripped.lstrip("+-")  # ADDED

                            if not stripped:
                                raise ValueError(f"Empty word at memory [{i}]")

                            # Enforce 4 or 6 digits only (reject 5-digit words)  # ADDED
                            if len(unsigned) not in (4, 6):
                                raise ValueError(f"Only 4-digit or 6-digit words allowed. Invalid word at memory [{i}]: '{stripped}'")

                            if '+' in word or '-' in word:
                                if len(word) > 8:
                                    raise ValueError(f"Improper word length at memory [{i}]")
                                else:
                                    instruction = Convert.convert_to_int(stripped)  # use stripped
                            else:
                                if len(word) > 7:
                                    raise ValueError(f"Improper word length at memory [{i}]")
                                else:
                                    instruction = Convert.convert_to_int(stripped)  # use stripped

                            if instruction is False:
                                raise ValueError(f"Invalid word at memory [{i}]")

                            # Validate instruction range (ADDED)
                            if not (-999999 <= instruction <= 999999):
                                raise ValueError(f"Instruction out of range at memory [{i}]: {instruction}")

                            print(f"Loading instruction at memory[{i}]: '{stripped}' -> {instruction}")  # ADDED DEBUG

                            wordConsistencyEnforcer = len(word)

                            if i == 0:
                                firstWordLength = len(word)

                            if firstWordLength != wordConsistencyEnforcer:
                                raise ValueError(f"All words in the file must be the same size.  Word {i} in the file (0-based) is inconsistent...")

                            self.memory.write(i, instruction)
                            i += 1

                            if i == 250:
                                raise IndexError(f"File exceeds maximum allowable size of 250 lines!")

                            word = ""
                            continue
                        raise ValueError(f"Invalid space found in word at memory [{i}]")
        else:
            raise FileNotFoundError(f"File '{filename}' not found.")
