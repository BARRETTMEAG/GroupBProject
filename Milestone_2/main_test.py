import pytest
from main import CPU
from memory import Memory
from main import UVSim

@pytest.fixture
def setup():
    cpu = CPU()
    memory = Memory()
    return cpu, memory
    
# Testing files, even if it exist if not
def test_file_open():
    sim = UVSim()
    sim.load_program('Test1.txt') #Assumes existence of Test1.txt
    
    with pytest.raises(OSError):
        sim.load_program('qwertyuiop.txt') #Assumes this file does not exist

# Testing the inital program of Test1.txt and Test2.txt
def test_program_init():
    sim = UVSim()
    sim.load_program('Test1.txt')

    assert sim.memory.memory[0] == 1007
    assert sim.memory.memory[1] == 1008
    assert sim.memory.memory[2] == 2007
    assert sim.memory.memory[3] == 3008
    assert sim.memory.memory[4] == 2109
    assert sim.memory.memory[5] == 1109
    assert sim.memory.memory[6] == 4300

    sim.load_program('Test2.txt')

    assert sim.memory.memory[0] == 1009
    assert sim.memory.memory[1] == 1010
    assert sim.memory.memory[2] == 2009
    assert sim.memory.memory[3] == 3110
    assert sim.memory.memory[4] == 4107
    assert sim.memory.memory[5] == 1109
    assert sim.memory.memory[6] == 4300
    assert sim.memory.memory[7] == 1110
    assert sim.memory.memory[8] == 4300

# Tests writing and reading memory
def test_memory_write_and_read():
    memory = Memory()
    memory.write(10, 1234)
    assert memory.read(10) == 1234

    with pytest.raises(IndexError):
        memory.write(150, 9999)

    with pytest.raises(IndexError):
        memory.read(-1)

# Tests loading from stored memory
def test_load_store(setup):
    cpu, memory = setup
    memory.write(5, 4321)
    cpu.execute(2005, memory.memory)  # LOAD from address 5
    assert cpu.accumulator == 4321

    cpu.execute(2106, memory.memory)  # STORE to address 6
    assert memory.read(6) == 4321

# Tests the both the addition and subtraction of memory
def test_add_subtract(setup):
    cpu, memory = setup
    cpu.accumulator = 100
    memory.write(1, 50)
    cpu.execute(3001, memory.memory)  # ADD from address 1
    assert cpu.accumulator == 150

    memory.write(2, 25)
    cpu.execute(3102, memory.memory)  # SUBTRACT from address 2
    assert cpu.accumulator == 125

# Tests the multipication and division of memory
def test_multiply_divide(setup):
    cpu, memory = setup
    cpu.accumulator = 10
    memory.write(3, 5)
    cpu.execute(3303, memory.memory)  # MULTIPLY
    assert cpu.accumulator == 50

    memory.write(4, 2)
    cpu.execute(3204, memory.memory)  # DIVIDE
    assert cpu.accumulator == 25.0

# Tests memory branch operations (branch, branchneg, branchzero, and if no branching) 
def test_branch_operations(setup):
    cpu, memory = setup
    cpu.execute(4007, memory.memory)  # BRANCH to 07
    assert cpu.program_counter == 7

    cpu.accumulator = -1
    cpu.execute(4109, memory.memory)  # BRANCHNEG to 09
    assert cpu.program_counter == 9

    cpu.accumulator = 0
    cpu.execute(4202, memory.memory)  # BRANCHZERO to 02
    assert cpu.program_counter == 2

    cpu.accumulator = 5
    cpu.program_counter = 0
    cpu.execute(4203, memory.memory)  # Should not branch
    assert cpu.program_counter == 1 # PC moves up one instead of branching

# Tests Halt
def test_halt(setup):
    cpu, memory = setup
    cpu.execute(4300, memory.memory)
    assert cpu.halted is True

# Tests bad opcode
def test_bad_opcode(setup):
    cpu, memory = setup
    with pytest.raises(ValueError):
        cpu.execute(5555, 8)

# Tests bad word length
def test_bad_word_length(setup):
    cpu, memory = setup
    with pytest.raises(ValueError):
        memory.write(5, 12345)

# Tests negative values
def test_negative_values():
    sim = UVSim()
    memory = sim.memory
    sim.cpu.accumulator = 100
    memory.write(0, 3003)
    memory.write(1, 3004)
    memory.write(2, 4300)
    memory.write(3, -30)
    memory.write(4, -50)
    sim.run()
    assert sim.cpu.accumulator == 20

# Tests when subtracting negatives
def test_subtract_negative():
    sim = UVSim()
    memory = sim.memory
    sim.cpu.accumulator = 100
    memory.write(0, 3103)
    memory.write(1, 3104)
    memory.write(2, 4300)
    memory.write(3, -30)
    memory.write(4, -50)
    sim.run()
    assert sim.cpu.accumulator == 180

# Tests bad word format
def test_bad_word_format():
    sim = UVSim()
    with pytest.raises(TypeError):
        sim.memory.write(0, "TEST")
    
    sim.memory.memory[0] = "TEST"
    with pytest.raises(TypeError):
        sim.run()

# Tests improper word in file
def test_improper_word_in_file():
    sim = UVSim()
    with pytest.raises(ValueError):
        sim.load_program('Test3.txt') #Test3.txt contains "11111\n"
        
    with pytest.raises(ValueError):
        sim.load_program('Test4.txt') #Test4.txt contains "TEST\n"

# --- Branch to a specific part in memory ---
def test_branch(setup):
    cpu, memory = setup
    cpu.execute(4005, memory.memory)
    assert cpu.program_counter == 5

# Tests branching executes until halt command
def test_branch_executes_until_halt():
    sim = UVSim()
    sim.memory.write(0, 4001)  # BRANCH to line 1
    sim.memory.write(1, 4300)  # HALT
    sim.run()
    assert sim.cpu.halted is True
    assert sim.cpu.program_counter == 1

# --- Print Hello World ---
def test_write_prints_hello_world(monkeypatch, capsys, setup):
    cpu, mem = setup
    mem.write(50, "Hello World")
    monkeypatch.setattr("builtins.input", lambda _: "")
    cpu.execute(1150, mem.memory)  # WRITE 50
    captured = capsys.readouterr()
    assert "Hello World" in captured.out

# Tests input and print hello world
def test_input_then_print_hello_world(monkeypatch, capsys):
    sim = UVSim()
    sim.memory.write(0, 1020)  # READ into address 20
    sim.memory.write(1, 1120)  # WRITE from address 20
    sim.memory.write(2, 4300)  # HALT

    # User input of "Hello World"
    monkeypatch.setattr("builtins.input", lambda _: "Hello World")

    sim.run()
    captured = capsys.readouterr()
    assert "Hello World" in captured.out
    assert sim.cpu.halted is True

# --- Load and Store Data to memory and accumulator ---
def test_load_and_store_value(setup):
    cpu, mem = setup
    mem.write(10, 42)
    cpu.execute(2010, mem.memory)  # LOAD from address 10
    assert cpu.accumulator == 42
    cpu.execute(2111, mem.memory)  # STORE to address 11
    assert mem.read(11) == 42

# Tests what araises when invalid address submitted
def test_invalid_address_raises():
    mem = Memory()
    with pytest.raises(IndexError):
        mem.write(200, 99)

# --- Utilize Multiplication Opcode ---
def test_multiply_two_values(setup):
    cpu, mem = setup
    cpu.accumulator = 6
    mem.write(7, 7)
    cpu.execute(3307, mem.memory)  # MULTIPLY by memory[7]
    assert cpu.accumulator == 42

# Tests Multiplication with zero
def test_multiplication_with_zero(setup):
    cpu, mem = setup
    cpu.accumulator = 0
    mem.write(20, 5)
    cpu.execute(3320, mem.memory)  # MULTIPLY by memory[20]
    assert cpu.accumulator == 0

# --- Utilize Division Opcode ---
def test_divide_two_values(setup):
    cpu, mem = setup
    cpu.accumulator = 42
    mem.write(5, 7)
    cpu.execute(3205, mem.memory)  # DIVIDE by memory[5]
    assert cpu.accumulator == 6

# Tests division by zero
def test_division_by_zero(setup):
    cpu, mem = setup
    cpu.accumulator = 10
    mem.write(3, 0)
    with pytest.raises(ZeroDivisionError):
        cpu.execute(3203, mem.memory)  # DIVIDE by memory[3]
