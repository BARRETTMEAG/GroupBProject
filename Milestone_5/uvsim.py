from memory import Memory
from cpu import CPU

class UVSim:
    def __init__(self, memory=None):
        self.memory = memory or Memory()
        self.cpu = CPU()

    def run(self):
        while not self.cpu.halted:
            instr = self.memory.read(self.cpu.program_counter)
            self.cpu.execute(instr, self.memory)
