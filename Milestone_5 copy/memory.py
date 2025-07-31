class MemoryRegister:
    def __init__(self, value=0):
        self.set(value)

    def set(self, value):
        if not isinstance(value, int):
            raise ValueError("MemoryRegister must store an integer.")
        if -999999 <= value <= 999999:
            self.value = value
        else:
            self.value = value % 1000000  # Wrap into valid range (keeps negatives)

    def get(self):
        return self.value

    def __repr__(self):
        return f"MemoryRegister({self.value})"
class Memory:
    def __init__(self):
        self.memory = [MemoryRegister() for _ in range(250)]
        self.read_callback = None
        self.waiting_for_input = False

    def write(self, address, value):
        if 0 <= address < 250:
            self.memory[address].set(value)
        else:
            raise IndexError("Memory address out of range")

    def read(self, address):
        if 0 <= address < 250:
            return self.memory[address].get()
        else:
            raise IndexError("Memory address out of range")
