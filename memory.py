class Memory:
    def __init__(self):
        self.memory = [0] * 100  # Initialize memory with 100 words (00-99)

    def write(self, address, value):
        if 0 <= address < 100:
            self.memory[address] = value
        else:
            raise IndexError("Memory address out of range")

    def read(self, address):
        if 0 <= address < 100:
            return self.memory[address]
        else:
            raise IndexError("Memory address out of range")