# UVSim Pseudocode

from memory import Memory

class UVSim:
    def initialize(self):
        self.cpu = CPU()
        self.memory = Memory()

    def load_program(self, program):
        for i, instruction in enumerate(program):
            self.memory.write(i, instruction)

    def run(self):
        while not self.cpu.halted:
            instruction = self.memory.read(self.cpu.program_counter)
            self.cpu.execute(instruction, self.memory)


class CPU:
    def __init__(self):
        self.accumulator = 0
        self.program_counter = 0
        self.halted = False

    def execute(self, instruction, memory):
        opcode = instruction // 100
        operand = instruction % 100

        if opcode == 10:  # READ
            pass

        elif opcode == 11:  # WRITE
            pass

        elif opcode == 20:  # LOAD
            pass

        elif opcode == 21:  # STORE
            pass

        elif opcode == 30:  # ADD
            pass

        elif opcode == 31:  # SUBTRACT
            pass

        elif opcode == 32:  # DIVIDE
            pass

        elif opcode == 33:  # MULTIPLY
            pass

        elif opcode == 40:  # BRANCH
            pass

        elif opcode == 41:  # BRANCHNEG
            pass

        elif opcode == 42:  # BRANCHZERO
            pass
        
        elif opcode == 43:  # HALT
            self.halted = True
            return

        self.program_counter += 1