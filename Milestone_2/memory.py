class Memory:
    def __init__(self):
        self.memory = [0] * 100  # Initialize memory with 100 words (00-99)

    def write(self, address, value):
        if 0 <= address < 100:
            if -9999 <= value <= 9999:  # Ensure value is a signed four-digit integer
                self.memory[address] = value
            else:
                raise ValueError("Value must be a signed four-digit integer")
        else:
            raise IndexError("Memory address out of range")


    def read(self, address):
        if 0 <= address < 100:
            return self.memory[address]
        else:
            raise IndexError("Memory address out of range")