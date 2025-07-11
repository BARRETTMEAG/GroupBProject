from memory import Memory
from cpu import CPU

class UVSim:
    def __init__(self, memory = None):
        self.cpu = CPU()
        self.memory = memory if memory else Memory()

    def run(self):
        while not self.cpu.halted:
            instruction = self.memory.read(self.cpu.program_counter)
            self.cpu.execute(instruction, self.memory)
