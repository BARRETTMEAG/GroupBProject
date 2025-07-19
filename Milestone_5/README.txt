README describes how this UVSim software simulator works. 

This program is written in python and is available through github. 

## The program uses the `tkinter` library for GUI. Tkinter is typically included in Python and does not need to be installed.

## How to Launch the Application
1. Open a terminal or command prompt.
2. Navigate to the directory containing the `uvsim_gui.py` file.
3. Run the program using the following command: python3 main.py

## How to Use the Application
1. Click Load Program File to open a BasicML program file.
2. The application supports two file formats:
	- Legacy 4-digit files (up to 100 lines)
	- Extended 6-digit files (up to 250 lines)
3. Edit program instructions or data values directly in the interface after loading.
4. Click Run Program to execute the loaded program.
5. When the program requests input (for READ instructions), enter values in the popup and click submit.
6. You can save your work at any time with the Save Program File button.
7. Open multiple files simultaneously in tabs to edit and switch between programs.
8. Execution locks editing and switching until the program finishes or is stopped.
9. Click the red circle (top-left) to close the application.

## How to Change the Color
1. Go to file location of program.
2. Open color_config.py
3. Find self.primary and self.off values.
4. Edit in the hex code of desired colors into the two values, make sure to place a '#' character before every color value, and to enclose entire value including the '#' in quotations.

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
