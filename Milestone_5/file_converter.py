class FileConverter:
    VALID_OPCODES = {10,11,20,21,30,31,32,33,40,41,42,43}

    @staticmethod
    def convert_4_to_6(word_str):
        val = int(word_str)
        first_two = val // 100
        if first_two in FileConverter.VALID_OPCODES:
            opcode = first_two
            operand = val % 100
            return f"{opcode:03d}{operand:03d}"
        else:
            return f"{val:+06d}"

    @staticmethod
    def convert_file(input_path, output_path):
        with open(input_path, "r") as inp, open(output_path, "w") as out:
            for line in inp:
                s = line.strip()
                if not s: continue
                out.write(FileConverter.convert_4_to_6(s) + "\n")
