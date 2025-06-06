import os
from memory import Memory

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
            memory[operand] = value

        elif opcode == 11:  # WRITE = Write a word from a specific location in memory to screen.
            print(str(memory[operand]))

        elif opcode == 20:  # LOAD = Load a word from a specific location in memory into the accumulator.
            self.accumulator = memory[operand]

        elif opcode == 21:  # STORE = Store a word from the accumulator into a specific location in memory.
            memory[operand] = self.accumulator

        elif opcode == 30:  # ADD = Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)
            self.accumulator = int(self.accumulator) + int(memory[operand])

        elif opcode == 31:  # SUBTRACT = Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator)
            self.accumulator = int(self.accumulator) - int(memory[operand])

        elif opcode == 32:  # DIVIDE = Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator).
            self.accumulator = int(self.accumulator) / int(memory[operand])

        elif opcode == 33:  # MULTIPLY = multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator).
            self.accumulator = int(self.accumulator) * int(memory[operand])

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
                        break
                    if not char.isspace():
                        word += char
                    elif char.isspace(): # Program encounters whitespace
                        if not word:
                            continue # Skips words containing only blank spaces
                        elif len(word) != 5: # Validates length of word (including sign)
                            raise ValueError("Incorrect word length encountered at memory [" + str(i) + "]")
                        else:
                            instruction = int(word) # Convert word to instruction of type integer when an 'enter' char is encountered
                            self.memory.write(i, instruction)
                            i += 1
                            word = ""
        else:
            print(f"The file '{filename}' does not exist.")
            filename = input("Please enter the name of your file: ")
            self.load_program(filename)

    def run(self):
        while not self.cpu.halted:
            instruction = self.memory.read(self.cpu.program_counter)
            self.cpu.execute(instruction, self.memory.memory)


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
