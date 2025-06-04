README describes how this UVSim software simulator works. 

This program is written in python and is available through github. 

When entering a four-digit number (+1235), the number is divided by the first two digits and the last two digits. The 12 or whatever number is known as the memory and the 35 would be the memory location portion of the code.

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
