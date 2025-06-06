import pytest
from main import CPU, UVSim
from memory import Memory

# --- Branch to a specific part in memory ---
def test_branch():
    cpu = CPU()
    memory = [0] * 100
    cpu.execute(4005, memory)
    assert cpu.program_counter == 5
"""In Spreadsheet: Name: Test Branch Pointer, Definition: Test that branch moves pointer to specific part in memory, Use Case: Branch to specific part in memory, Input: 4005, Output: Counter = 5, Succeeded: Counter = 5"""

def test_branch_executes_until_halt():
    sim = UVSim()
    sim.memory.write(0, 4001)  # BRANCH to line 1
    sim.memory.write(1, 4300)  # HALT
    sim.run()
    assert sim.cpu.halted is True
    assert sim.cpu.program_counter == 1
"""In Spreadsheet: Successful execution after branch, Definition: Test that program continues executing after branching to specific part in memory, Use Case: Branch to specific part in memory, Inpt: 4001, Output: True, Succeeded: Program Halted"""

# --- Print Hello World ---
def test_write_prints_hello_world(monkeypatch, capsys):
    cpu = CPU()
    mem = Memory()
    mem.write(50, "Hello World")
    monkeypatch.setattr("builtins.input", lambda _: "")
    cpu.execute(1150, mem.memory)  # WRITE 50
    captured = capsys.readouterr()
    assert "Hello World" in captured.out
"""In Spreadsheet: Name: Print Hello World, Definition: Test that program can perform basic programming projects such as printing 'Hello World', Use Case: Print Hello World, Input: Hello World, Output: Hello World, Succeeded: Prints Hello World to Console"""

def test_load_then_print_hello_world(monkeypatch, capsys):
    sim = UVSim()
    sim.memory.write(0, 2020)  # LOAD from address 20
    sim.memory.write(1, 2121)  # STORE into address 21
    sim.memory.write(2, 1121)  # WRITE from address 21
    sim.memory.write(3, 4300)  # HALT
    sim.memory.write(20, "Hello World")

    sim.run()
    captured = capsys.readouterr()
    assert "Hello World" in captured.out
    assert sim.cpu.halted is True
"""In Spreadsheet: Name: Load and Print Hello World, Definition: Test that program can load words and print them out correctly, Use Case: Print Hello World, Input: Hello World, Output: Hello World, Succeeded: Prins Hello World to console"""

# --- Store new data to memory ---
def test_load_and_store_value():
    cpu = CPU()
    mem = Memory()
    mem.write(10, 42)
    cpu.execute(2010, mem.memory)  # LOAD from address 10
    assert cpu.accumulator == 42
    cpu.execute(2111, mem.memory)  # STORE to address 11
    assert mem.read(11) == 42
"""In Spreadsheet: Name: Load to Memory, Defintion; Test that program correcty loads and stores values to memory, Use Case: Store new data to memory, Input: 42, Output: True, Succeeded: 42 loaded to address 11 """

def test_invalid_address_raises():
    mem = Memory()
    with pytest.raises(IndexError):
        mem.write(200, 99)
"""In Spreadsheet: Name: Invalid Address, Definition: Catch invalid addresses, Use Case: Store new data to memory, Input: 99, Output: IndexError, Succeeded: IndexError"""

# --- Utilize Mutliplication Opcode ---
def test_multiply_two_values():
    cpu = CPU()
    mem = Memory()
    cpu.accumulator = 6
    mem.write(7, 7)
    cpu.execute(3307, mem.memory)  # MULTIPLY by memory[7]
    assert cpu.accumulator == 42
"""In Spreadsheet: Name: Multiplication, Defintion: Check that program correctly multiplies values, Use Case: Utilize Mutliplication Opcode, Inputs: 6, 7, Ouputs: 42, Succeeded: Accumulator is 42"""

def test_multiplication_with_zero():
    cpu = CPU()
    mem = Memory()
    cpu.accumulator = 0
    mem.write(20, 5)
    cpu.execute(3320, mem.memory)  # MULTIPLY by memory[20]
    assert cpu.accumulator == 0
"""In Spreadsheet: Name: Zero Multiplication, Definition: Check that program correclty multiplies by zero, Use Case: Utilize Multiplication Opcode, Inputs: 5, 0, Outputs: 0, Succeeded: Accumulator is 0"""
