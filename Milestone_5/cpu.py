from convert import Convert

class CPU:
    def __init__(self):
        self.accumulator = 0
        self.program_counter = 0
        self.halted = False

    def execute(self, instruction, memory):
        opcode = instruction // 1000
        operand = instruction % 1000

        # READ
        if opcode == 10:
            memory.waiting_for_input = True
            if memory.read_callback:
                value = memory.read_callback(operand)
            else:
                value = input("Enter value: ")
            val = Convert.convert_to_int(value)
            if val is False:
                raise ValueError("Invalid entry! Please enter signed 6-digit integers.")
            memory.write(operand, val)
            memory.waiting_for_input = False

        # WRITE
        elif opcode == 11:
            print(memory.read(operand))

        # LOAD
        elif opcode == 20:
            self.accumulator = memory.read(operand)

        # STORE
        elif opcode == 21:
            memory.write(operand, self.accumulator)

        # ADD
        elif opcode == 30:
            self.accumulator = int(self.accumulator) + int(memory.read(operand))

        # SUBTRACT
        elif opcode == 31:
            self.accumulator = int(self.accumulator) - int(memory.read(operand))

        # DIVIDE (fixed integer math)
        elif opcode == 32:
            divisor = memory.read(operand)
            if divisor == 0:
                raise ValueError("Cannot divide by zero.")
            self.accumulator = int(self.accumulator) // divisor

        # MULTIPLY
        elif opcode == 33:
            self.accumulator = int(self.accumulator) * int(memory.read(operand))

        # BRANCH
        elif opcode == 40:
            self.program_counter = operand
            return

        # BRANCHNEG
        elif opcode == 41:
            if self.accumulator < 0:
                self.program_counter = operand
            else:
                self.program_counter += 1
            return

        # BRANCHZERO
        elif opcode == 42:
            if self.accumulator == 0:
                self.program_counter = operand
            else:
                self.program_counter += 1
            return

        # HALT
        elif opcode == 43:
            self.halted = True
            print(f"HALT at memory address [{self.program_counter:03d}]")
            return

        else:
            raise ValueError(f"Unknown opcode '{opcode}' at address {self.program_counter:03d}")

        # Overflow handling
        if self.accumulator > 999999 or self.accumulator < -999999:
            self.accumulator %= 1000000

        self.program_counter += 1
