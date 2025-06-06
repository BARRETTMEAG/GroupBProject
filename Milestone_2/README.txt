README describes how this UVSim software simulator works. 

This program is written in python and is available through github. 

Additionally, the program uses the `pytest` library for testing. You can install it using the following command:

## How to Launch the Application
1. Open a terminal or command prompt.
2. Navigate to the directory containing the `main.py` file.
3. Run the program using the following command:

## How to Use the Application
1. When prompted, enter the name of the input file containing your BasicML program. Ensure the file is in the same directory as the `main.py` file or provide the full path to the file.
2. The program will load the instructions from the file into memory and execute them sequentially.
3. Follow any prompts displayed on the console during execution (e.g., entering values for `READ` operations).

## Input File Format
- The input file should contain BasicML instructions, one per line.
- Each instruction must be a signed 5-digit integer (e.g., `+1020` or `-4321`).
- Ensure the file includes a `HALT` instruction (`+4300`) to terminate the program.

## Testing the Application
To run the unit tests for the application, use the following command:

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
