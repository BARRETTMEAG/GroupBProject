README describes how this UVSim software simulator works. 

This program is written in python and is available through github. 

## The program uses the `tkinter` library for testing. You can install it using the following command:

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

## How to Launch the Application
1. Open a terminal or command prompt.
2. Navigate to the directory containing the `uvsim_gui.py` file.
3. Run the program using the following command: python3 main.py

## How to Use the Application
1. After launching application, submit a file using the "Load Program File" button.
2. Hit the "Run Program" button.
2. The program will load the instructions from the file into memory and execute them sequentially.
2. When prompted a new pop up window, enter in your input for a READ opcode and click "submit"
3. After application is processed, the user can resubmit a new file.

## Input File Format
- The input file should contain BasicML instructions, one per line.
- Each instruction must be a signed 5-digit integer (e.g., `+1020` or `-4321`).
- Ensure the file includes a `HALT` instruction (`+4300`) to terminate the program.

## Testing the Application
To test the application submit the file to be tested. If no error occurs the application should run smoothly. If an error occurs the instructions will stop being read and the user will be notified of the specific error caught in the .txt file.

When entering a four-digit number (+1235), the number is separated by the first two digits and the last two digits. The 12 or whatever number is known as the memory and the 35 would be the memory location portion of the code.

BasicML vocabulary defined as follows:

00 = Starts Memory Location Program

I/0 operation:

10 = This Reads the Four-Digit Number into Specific Location in Memory. (Read)

11 = Write Four-Digit Number into Specific Location in Memory to Screen. (Write)

Load/store operations:
20 = This Loads Another Four-Digit Number from Memory Specific Location into Accumulator. (Load)

21 = This Stores Four-Digit Number into Memory's Specific Location from Accumulator. (Store)

Arithmetic operation:
30 = This Adds a Four-Digit Number From a Specific Memory Location to the Number in Accumulator. (leave the result in the accumulator)

31 = This Subtracts a Four-Digit Number From Specific Memory Location to the Number in Accumulator. (leave the result in the accumulator)

32 = This Divides a Four-Digit Number From Specific Memory Location to the Number in Accumulator. (leave the result in the accumulator)

33 = This Multiplies a Four-Digit Number From Specific Memory Location to the Number in Accumulator. (leave the result in the accumulator)

Control operation:
40 = This Branches to Specific Memory Location.

41 = This Branches to Specific Memory Location if Accumulator is Negative. (BRANCHNEG)

42 = This Branches to Specific Memory Location if Accumulator is Zero. (BRANCHZERO)

43 = Stops Program. (Halt)
