class MemoryRegister:
    def __init__(self, value=0):
        self.set(value)

    def set(self, value):
        if not isinstance(value, int):
            raise ValueError("MemoryRegister must store an integer.")
        if -999999 <= value <= 999999:
            self.value = value
        else:
            self.value = value % 1000000  # Wrap to six-digit range

    def get(self):
        return self.value

class Memory:
    def __init__(self):
        self.memory = [MemoryRegister() for _ in range(250)]
        self.read_callback = None
        self.waiting_for_input = False

    def write(self, address, value):
        if not (0 <= address < 250):
            raise IndexError("Memory address out of range 000–249")
        if not isinstance(value, int):
            raise ValueError("MemoryRegister must store an integer.")
        self.memory[address].set(value)

    def read(self, address):
        if not (0 <= address < 250):
            raise IndexError("Memory address out of range 000–249")
        return self.memory[address].get()
