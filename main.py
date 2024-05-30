class Processor:
    def __init__(self, bit_size=30):
        self.bit_size = bit_size
        self.accumulator = 0
        self.registers = {'R1': 0, 'R2': 0, 'R3': 0, 'R4': 0}
        self.status = {'sign': 0}
        self.pc = 0
        self.tc = 0

    def to_binary(self, value, bits=None):
        """Convert to binary with bit_size (default: self.bit_size)."""
        if bits is None:
            bits = self.bit_size
        return format(value if value >= 0 else (1 << bits) + value, f'0{bits}b')

    def from_binary(self, binary_str):
        """Convert binary string to integer."""
        if binary_str[0] == '1':  # negative number
            return int(binary_str, 2) - (1 << len(binary_str))
        return int(binary_str, 2)

    def mov(self, value):
        self.accumulator = value

    def save(self, reg):
        self.registers[reg] = self.accumulator

    def bitwise_add(self, byte1, byte2):
        """Perform bitwise addition modulo 2."""
        return byte1 ^ byte2

    def add(self, operand):
        """Add the operand to the accumulator using bitwise addition."""
        operand_value = self.registers[operand] if operand in self.registers else int(operand)
        result = self.bitwise_add(self.accumulator, operand_value)
        self.accumulator = result
        self.status['sign'] = 1 if result < 0 else 0

    def sub(self, operand):
        """Subtract the operand from the accumulator using bitwise addition."""
        operand_value = self.registers[operand] if operand in self.registers else int(operand)
        result = self.bitwise_add(self.accumulator, operand_value)
        self.accumulator = result
        self.status['sign'] = 1 if result < 0 else 0

    def execute(self, command):
        parts = command.split()
        self.tc = 0
        self.pc += 1
        if parts[0] == 'mov':
            self.mov(int(parts[1]))
        elif parts[0] == 'save':
            self.save(parts[1])
        elif parts[0] == 'add':
            self.add(parts[1])
        elif parts[0] == 'sub':
            self.sub(parts[1])
        self.tc += 1

    def run(self, program):
        for command in program:
            self.execute(command)
            self.print_state(command)
            input("Press Enter for next cycle...")

    def print_state(self, command):
        print(f"Komanda = {command}")
        print(f"A = {self.to_binary(self.accumulator)}")
        for reg, val in self.registers.items():
            print(f"{reg} = {self.to_binary(val)}")
        print(f"Ins = {command}")
        print(f"PC = {self.pc}")
        print(f"TC = {self.tc}")
        print(f"PS = {self.status['sign']}")
        print("-" * 40)

def read_program_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Example usage
program = read_program_from_file('program.txt')
cpu = Processor()
cpu.run(program)
