class MemoryRegister:
    def __init__(self, value=0):
        self.set(value)

    def set(self, value):
        if not isinstance(value, int):
            raise ValueError("MemoryRegister must store an integer.")
        if -9999 <= value <= 9999:
            self.value = value
        else:
            self.value = value % 10000  # Wrap into valid range

    def get(self):
        return self.value

    def __repr__(self):
        return f"MemoryRegister({self.value})"
class Memory:
    def __init__(self):
        self.memory = [MemoryRegister() for _ in range(100)]
        self.read_callback = None
        self.waiting_for_input = False

    def write(self, address, value):
        if 0 <= address < 100:
            self.memory[address].set(value)
        else:
            raise IndexError("Memory address out of range")

    def read(self, address):
        if 0 <= address < 100:
            return self.memory[address].get()
        else:
            raise IndexError("Memory address out of range")
