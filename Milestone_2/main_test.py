import pytest
from main import CPU
from memory import Memory
from main import UVSim

@pytest.fixture
def setup():
    cpu = CPU()
    memory = Memory()
    return cpu, memory

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
    assert cpu.program_counter == 0

def test_halt(setup):
    cpu, memory = setup
    cpu.execute(4300, memory.memory)
    assert cpu.halted is True
