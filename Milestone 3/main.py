import os
from memory import Memory
from convert import Convert
from cpu import CPU
from uvsim import UVSim

def main():

    sim = UVSim()
    filename = input("Please enter the name of your file: ")
    sim.load_program(filename)
    sim.run()

    # Output code for troubleshooting:
    """
    j = 0
    for i in sim.memory.memory:
        if sim.memory.memory[j]:
            print("Memory at [" + str(j) + "] is: ", str(sim.memory.memory[j]))
            j += 1
        else:
            print("Memory at [" + str(j) + "] is empty.")
            j += 1
    """
    print("Accumulator register value:", str(sim.cpu.accumulator))
    #

if __name__=="__main__":
    main()
