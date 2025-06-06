import pytest
from main import CPU
from memory import Memory
from main import UVSim

@pytest.fixture
def setup():
    cpu = CPU()
    memory = Memory()
    return cpu, memory
    
def test_file_open():
    sim = UVSim()
    sim.load_program('Test1.txt') #Assumes existence of Test1.txt
    
    with pytest.raises(OSError):
        sim.load_program('qwertyuiop.txt') #Assumes this file does not exist

def test_program_init():
    sim = UVSim()
    sim.load_program('Test1.txt')

    assert sim.memory.memory[0] == 1007
    assert sim.memory.memory[0] == 1008
    assert sim.memory.memory[0] == 2007
    assert sim.memory.memory[0] == 3008
    assert sim.memory.memory[0] == 2109
    assert sim.memory.memory[0] == 1109
    assert sim.memory.memory[0] == 4300

    sim.load_program('Test2.txt')

    assert sim.memory.memory[0] == 1009
    assert sim.memory.memory[0] == 1010
    assert sim.memory.memory[0] == 2009
    assert sim.memory.memory[0] == 3110
    assert sim.memory.memory[0] == 4107
    assert sim.memory.memory[0] == 1109
    assert sim.memory.memory[0] == 4300
    assert sim.memory.memory[0] == 1110
    assert sim.memory.memory[0] == 4300
    
def test_memory_write_and_read():
    memory = Memory()
    memory.write(10, 1234)
    assert memory.read(10) == 1234

    with pytest.raises(IndexError):
        memory.write(150, 9999)

    with pytest.raises(IndexError):
        memory.read(-1)

def test_load_store(setup):
    cpu, memory = setup
    memory.write(5, 4321)
    cpu.execute(2005, memory.memory)  # LOAD from address 5
    assert cpu.accumulator == 4321

    cpu.execute(2106, memory.memory)  # STORE to address 6
    assert memory.read(6) == 4321

def test_add_subtract(setup):
    cpu, memory = setup
    cpu.accumulator = 100
    memory.write(1, 50)
    cpu.execute(3001, memory.memory)  # ADD from address 1
    assert cpu.accumulator == 150

    memory.write(2, 25)
    cpu.execute(3102, memory.memory)  # SUBTRACT from address 2
    assert cpu.accumulator == 125

def test_multiply_divide(setup):
    cpu, memory = setup
    cpu.accumulator = 10
    memory.write(3, 5)
    cpu.execute(3303, memory.memory)  # MULTIPLY
    assert cpu.accumulator == 50

    memory.write(4, 2)
    cpu.execute(3204, memory.memory)  # DIVIDE
    assert cpu.accumulator == 25.0

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

def test_halt(setup):
    cpu, memory = setup
    cpu.execute(4300, memory.memory)
    assert cpu.halted is True

def test_bad_opcode(setup):
    cpu, memory = setup
    with pytest.raises(ValueError):
        cpu.execute(5555, 8)
    
def test_bad_word_length(setup):
    cpu, memory = setup
    with pytest.raises(ValueError):
        memory.write(5, 12345)

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

def test_bad_word_format():
    sim = UVSim()
    with pytest.raises(TypeError):
        sim.memory.write(0, "TEST")
    
    sim.memory.memory[0] = "TEST"
    with pytest.raises(TypeError):
        sim.run()

def test_improper_word_in_file():
    sim = UVSim()
    with pytest.raises(ValueError):
        sim.load_program('Test3.txt') #Test3.txt contains "11111\n"
        
    with pytest.raises(ValueError):
        sim.load_program('Test4.txt') #Test4.txt contains "TEST\n"
