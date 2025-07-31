from memory import Memory
from convert import Convert

class CPU:
    def __init__(self):
        self.accumulator = 0
        self.program_counter = 0
        self.halted = False

    def execute(self, instruction, memory):
        abs_instr = abs(instruction)

        if abs_instr >= 10000:  # Likely 6-digit format (e.g. 010020)
            instr_str = f"{abs_instr:06d}"  # Always 6 characters with leading 0s
            opcode = int(instr_str[:3])     # First 3 digits
            operand = int(instr_str[3:])    # Last 3 digits
        else:  # 4-digit format (e.g. 1020)
            instr_str = f"{abs_instr:04d}"  # Always 4 characters
            opcode = int(instr_str[:2])     # First 2 digits
            operand = int(instr_str[2:])    # Last 2 digits


        if opcode == 10:  # READ = Read a word from the keyboard into a specific location in memory.
            memory.waiting_for_input = True
            if hasattr(memory, 'read_callback') and memory.read_callback:
                value = memory.read_callback(operand)
            else:
                value = input("Enter the value to be stored: ")
                
            intValue = Convert.convert_to_int(value)  # Corrected reference to convert_to_int
            if intValue is False:
                raise ValueError("Invalid entry! Please enter signed 6-digit integers only...")
            memory.write(operand, intValue)
            memory.waiting_for_input = False

        elif opcode == 11:  # WRITE = Write a word from a specific location in memory to screen.
            output = int(memory.read(operand))
            print(str(output))

        elif opcode == 20:  # LOAD = Load a word from a specific location in memory into the accumulator.
            self.accumulator = memory.read(operand)

        elif opcode == 21:  # STORE = Store a word from the accumulator into a specific location in memory.
            word = self.accumulator
            memory.write(operand, word)

        elif opcode == 30:  # ADD = Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)
            self.accumulator = int(self.accumulator) + int(memory.read(operand))

        elif opcode == 31:  # SUBTRACT = Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator)
            self.accumulator = int(self.accumulator) - int(memory.read(operand))

        elif opcode == 32:  # DIVIDE = Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator).
            divisor = int(memory.read(operand))
            if divisor == 0:
                raise ValueError("Memory at [" + str(operand) + "] is '0'.  Cannot divide by 0!")
            self.accumulator = int(self.accumulator) // divisor

        elif opcode == 33:  # MULTIPLY = multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator).
            self.accumulator = int(self.accumulator) * int(memory.read(operand))

        elif opcode == 40:  # BRANCH = Branch to a specific location in memory
            self.program_counter = operand
            return

        elif opcode == 41:  # BRANCHNEG = Branch to a specific location in memory if the accumulator is negative.
            if self.accumulator < 0:
                self.program_counter = operand
            else:
                self.program_counter += 1
            return

        elif opcode == 42:  # BRANCHZERO = Branch to a specific location in memory if the accumulator is zero.
            if self.accumulator == 0:
                self.program_counter = operand
            else:
                self.program_counter += 1
            return
        
        elif opcode == 43:  # HALT = Stop the program
            self.halted = True
            print("HALT instruction encountered at memory [" + str(self.program_counter) + "]")
            return

        else:
            raise ValueError("Unknown opcode '" + str(opcode) + "' encountered at memory [" + str(self.program_counter) + "]")

        if self.accumulator > 999999 or self.accumulator < -999999:
            self.accumulator = self.accumulator % 1000000
            
        self.program_counter += 1
        return
