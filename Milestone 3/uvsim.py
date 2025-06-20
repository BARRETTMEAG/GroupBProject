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
        if os.path.isfile(filename): # Checks that the file exists
            with open(filename, "r") as file:
                while True:
                    char = file.read(1)
                    if not char:  # End of file
                        if word and word != '\n':
                            instruction = Convert.convert_to_int(word)
                            if instruction is False:
                                raise ValueError("This file contains an invalid word at memory [" + str(i) + "]. Words must be signed 4-digit integers (no spaces).")
                            self.memory.write(i, instruction)
                        break
                    word += char
                    if char.isspace(): # Program encounters whitespace
                        if char == '\n':
                            if not word or word == '\n':
                                raise ValueError("Empty word found at memory [" + str(i) + "]")
                            instruction = Convert.convert_to_int(word)
                            if instruction is False:
                                raise ValueError("This file contains an invalid word at memory [" + str(i) + "]. Words must be signed 4-digit integers (no spaces).")
                            if len(word) < 6:
                                raise ValueError("All words in the file must be signed 4-digit integers.  Invalid word at memory [" + str(i) + "]")
                            self.memory.write(i, instruction)
                            i += 1
                            word = ""
                            continue
                        raise ValueError("Invalid space found in the word at memory [" + str(i) + "]")
                        
        else:
            print(f"The file '{filename}' does not exist.")
            filename = input("Please enter the name of your file: ")
            self.load_program(filename)

    def run(self):
        while not self.cpu.halted:
            instruction = self.memory.read(self.cpu.program_counter)
            self.cpu.execute(instruction, self.memory)
