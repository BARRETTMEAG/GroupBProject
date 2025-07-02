class CPU:
    def __init__(self):
        self.accumulator = 0; self.program_counter = 0; self.halted = False

    def reset(self):
        self.accumulator = 0; self.program_counter = 0; self.halted = False

    def execute(self, instruction, memory, inp_callback=None):
        opcode, operand = divmod(instruction, 100)
        if opcode == 10:
            val = inp_callback(operand) if inp_callback else int(input())
            memory.write(operand, val)
        elif opcode == 11:
            return memory.read(operand)
        self.program_counter += 1
