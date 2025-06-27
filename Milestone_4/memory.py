class Memory:
    def __init__(self):
        self.memory = [0]*100

    def reset(self):
        self.memory = [0]*100

    def write(self, addr, value):
        if not (0 <= addr < 100): raise IndexError
        self.memory[addr] = value % 10000

    def read(self, addr):
        if not (0 <= addr < 100): raise IndexError
        return self.memory[addr]
