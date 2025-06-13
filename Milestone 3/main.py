import os
from memory import Memory

def convert_to_int(word):
    try:
        int(word)
        return int(word)
    except ValueError:
        return False

class CPU:
    def __init__(self):
        self.accumulator = 0
        self.program_counter = 0
        self.halted = False

    def execute(self, instruction, memory):
        opcode = instruction // 100
        operand = instruction % 100

        if opcode == 10:  # READ = Read a word from the keyboard into a specific location in memory.
            value = input("Enter the value to be stored: ")
            intValue = convert_to_int(value)
            if intValue is False:
                raise ValueError("Invalid entry! Please enter signed 4-digit integers only...")
            memory.write(operand, intValue)

        elif opcode == 11:  # WRITE = Write a word from a specific location in memory to screen.
            output = int(memory.read(operand))
            print(str(output))

        elif opcode == 20:  # LOAD = Load a word from a specific location in memory into the accumulator.
            self.accumulator = memory.read(operand)

        elif opcode == 21:  # STORE = Store a word from the accumulator into a specific location in memory.
            word = self.accumulator
            memory.write(operand, word)

        elif opcode == 30:  # ADD = Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)
            self.accumulator = int(self.accumulator) + int(memory.read(operand))

        elif opcode == 31:  # SUBTRACT = Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator)
            self.accumulator = int(self.accumulator) - int(memory.read(operand))

        elif opcode == 32:  # DIVIDE = Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator).
            divisor = int(memory.read(operand))
            if divisor == 0:
                raise ValueError("Memory at [" + str(operand) + "] is '0'.  Cannot divide by 0!")
            self.accumulator = int(self.accumulator) / divisor

        elif opcode == 33:  # MULTIPLY = multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator).
            self.accumulator = int(self.accumulator) * int(memory.read(operand))

        elif opcode == 40:  # BRANCH = Branch to a specific location in memory
            self.program_counter = operand
            return

        elif opcode == 41:  # BRANCHNEG = Branch to a specific location in memory if the accumulator is negative.
            if self.accumulator < 0:
                self.program_counter = operand
            else:
                self.program_counter += 1
            return

        elif opcode == 42:  # BRANCHZERO = Branch to a specific location in memory if the accumulator is zero.
            if self.accumulator == 0:
                self.program_counter = operand
            else:
                self.program_counter += 1
            return
        
        elif opcode == 43:  # HALT = Stop the program
            self.halted = True
            print("HALT instruction encountered at memory [" + str(self.program_counter) + "]")
            return

        else:
            raise ValueError("Unknown opcode '" + str(opcode) + "' encountered at memory [" + str(self.program_counter) + "]")

        if self.accumulator > 9999 or self.accumulator < -9999:
            self.accumulator = self.accumulator % 10000
            
        self.program_counter += 1
        return


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
                            instruction = convert_to_int(word)
                            if instruction is False:
                                raise ValueError("This file contains an invalid word at memory [" + str(i) + "]. Words must be signed 4-digit integers (no spaces).")
                        break
                    word += char
                    if char.isspace(): # Program encounters whitespace
                        if char == '\n':
                            if not word or word == '\n':
                                raise ValueError("Empty word found at memory [" + str(i) + "]")
                            instruction = convert_to_int(word)
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


def main():

    sim = UVSim()
    filename = input("Please enter the name of your file: ")
    sim.load_program(filename)
    sim.run()

    # Output code for troubleshooting:
    """
    j = 0
    for i in sim.memory.memory:
        if sim.memory.memory[j]:
            print("Memory at [" + str(j) + "] is: ", str(sim.memory.memory[j]))
            j += 1
        else:
            print("Memory at [" + str(j) + "] is empty.")
            j += 1
    """
    print("Accumulator register value:", str(sim.cpu.accumulator))
    #

if __name__=="__main__":
    main()
