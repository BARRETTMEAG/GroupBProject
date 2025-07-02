class Memory:
    def __init__(self):
        self.memory = [0] * 100  
        self.read_callback = None
        self.waiting_for_input = False

    def write(self, address, value):
        if 0 <= address < 100:
            if -9999 <= value <= 9999:
                self.memory[address] = value
            else:
                self.memory[address] = value % 10000
        else:
            raise IndexError("Memory address out of range")

    def read(self, address):
        if 0 <= address < 100:
            return self.memory[address]
        else:
            raise IndexError("Memory address out of range")
