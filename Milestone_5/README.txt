README describes how this UVSim software simulator works. 

This program is written in Python and is available through GitHub.

## The program uses the tkinter library for GUI. Tkinter is typically included in Python and does not need to be installed.

## How to Launch the Application
1. Open a terminal or command prompt.
2. Navigate to the directory containing the uvsim_gui.py file.
3. Run the program using the following command:
   python3 main.py

## How to Use the Application
1. After launching application, submit a file using the "Load Program File" button.
2. Hit the "Run Program" button.
3. The program will load the instructions from the file into memory and execute them sequentially.
4. When prompted in a new pop-up window, enter your input for a READ opcode and click "submit".
5. After application is processed, the user can resubmit a new file.
6. Save the current file using the "Save Program File" button.
7. Click the red circle in the top left corner to terminate the program and close window.
8. You can load files from any user-specified folder.
9. You can open multiple files at the same time inside the application, switching between them using tabs.
10. Only one file can be executed at a time.
11. Files can now be edited directly in the GUI after loading, including:
    - Adding new instructions
    - Modifying existing lines
    - Deleting instructions
    - Cutting, copying, and pasting lines
12. Make sure edited files do not exceed the max allowed instruction limit.
    - Legacy format: 100 lines (00–99)
    - New format: 250 lines (000–249)

## How to Change the Color
1. Go to file location of program.
2. Open colors.json.
3. Find primary and off values.
4. Edit in the hex code of desired colors into either Primary or Off values.
5. Hex code format - make sure the hex code stays within quotations. 
      - Hex code starts with a # and is followed by 6 character. Characters range from 0-9 and A-F.
5. Run program as usual.
6. If program does not appear to have changed colors, refer to the error printed to the terminal. Make sure the hex code follow the format above and in the given
examples in colors.json.

Example:
self.primary = "#4C721D"
self.off = "#FFFFFF"

- UVU Default Colors:
  - Primary: #4C721D (Dark Green)
  - Off: #FFFFFF (White)

- A valid hex color must start with # and be followed by exactly six characters (digits 0–9 or letters A–F).
- If entered incorrectly, the application may fail to launch.

## Input File Format
- The input file should contain BasicML instructions, one per line.
- Each instruction must be a signed integer.
  - Legacy format: 5-digit (e.g., +1020 or -4321)
  - New format: 6-digit (e.g., +010007 or +005555)
- Ensure the file includes a HALT instruction (+4300 or +043000) to terminate the program.
- Files must use either 4-digit or 6-digit instructions, not both.

## File Formats and Conversion
- Old files use 4-digit word format and support 100 memory addresses (00–99).
- New files use 6-digit word format and support 250 memory addresses (000–249).
- Your program will automatically detect and support both formats.
- You can also convert 4-digit files to 6-digit format using the built-in file converter.
- During conversion:
  - If the instruction starts with a valid opcode, it will be converted like this:
    1007 → 010007
  - If the instruction is a number (not a command), it will be converted like this:
    5555 → 005555

## Testing the Application
To test the application, submit the file to be tested. If no error occurs, the application should run smoothly. If an error occurs, the instructions will stop being read and the user will be notified of the specific error caught in the .txt file.

When entering a four-digit number (+1235), the number is separated by the first two digits and the last two digits. The 12 is known as the memory code and the 35 is the memory location portion of the code.

In the six-digit format (+010035), the first three digits are the operation code and the last three digits are the memory location.

## BasicML Vocabulary

I/O Operation:
10 = This Reads the Four-Digit Number into Specific Location in Memory. (Read)
11 = Write Four-Digit Number into Specific Location in Memory to Screen. (Write)

Load/Store Operation:
20 = This Loads Another Four-Digit Number from Memory Specific Location into Accumulator. (Load)
21 = This Stores Four-Digit Number into Memory's Specific Location from Accumulator. (Store)

Arithmetic Operation:
30 = This Adds a Four-Digit Number From a Specific Memory Location to the Number in Accumulator.
31 = This Subtracts a Four-Digit Number From Specific Memory Location to the Number in Accumulator.
32 = This Divides a Four-Digit Number From Specific Memory Location to the Number in Accumulator.
33 = This Multiplies a Four-Digit Number From Specific Memory Location to the Number in Accumulator.

Control Operation:
40 = This Branches to Specific Memory Location.
41 = This Branches to Specific Memory Location if Accumulator is Negative. (BRANCHNEG)
42 = This Branches to Specific Memory Location if Accumulator is Zero. (BRANCHZERO)
43 = Stops Program. (Halt)

## New Format Opcodes (6-digit)
010 = Read
011 = Write
020 = Load
021 = Store
030 = Add
031 = Subtract
032 = Divide
033 = Multiply
040 = Branch
041 = Branch if Negative
042 = Branch if Zero
043 = Halt
