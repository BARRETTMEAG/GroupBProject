import os
from memory import Memory
from convert import Convert
from cpu import CPU

class UVSim:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()

    def load_program(self, filename):
        i = 0
        word = ""
        if os.path.isfile(filename):
            with open(filename, "r") as file:
                while True:
                    char = file.read(1)
                    if not char:
                        if word and word != '\n':
                            instruction = Convert.convert_to_int(word)
                            if instruction is False:
                                raise ValueError(f"Invalid word at memory [{i}]")
                            self.memory.write(i, instruction)
                        break
                    word += char
                    if char.isspace():
                        if char == '\n':
                            if not word.strip():
                                raise ValueError(f"Empty word at memory [{i}]")
                            instruction = Convert.convert_to_int(word)
                            if instruction is False:
                                raise ValueError(f"Invalid word at memory [{i}]")
                            self.memory.write(i, instruction)
                            i += 1
                            word = ""
                            continue
                        raise ValueError(f"Invalid space found in word at memory [{i}]")
        else:
            raise FileNotFoundError(f"File '{filename}' not found.")

    def run(self):
        while not self.cpu.halted:
            instruction = self.memory.read(self.cpu.program_counter)
            self.cpu.execute(instruction, self.memory)
