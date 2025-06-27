from memory import Memory
from cpu import CPU

class UVSim:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.output_callback = None

    def load_program(self, filename):
        self.memory.reset()
        lines = open(filename).read().split()
        for i, word in enumerate(lines):
            iv = int(word)
            self.memory.write(i, iv)

    def step(self):
        inst = self.memory.read(self.cpu.program_counter)
        out = self.cpu.execute(inst, self.memory, inp_callback=self.read_callback)
        if out is not None:
            self.output_callback(out)
        return inst

    def reset(self):
        self.cpu.reset()
