class Memory:
    def __init__(self, size=65536):  # Default to max size
        self.memory = [0] * size

    def read(self, address):
        high = self.memory[address]
        low = self.memory[address + 1]
        return (high << 8) | low

    def write(self, address, value):
        high = (value >> 8) & 0xFF
        low = value & 0xFF
        self.memory[address] = high
        self.memory[address + 1] = low


class SimpleProcessor:
    def __init__(self):
        self.registers = {f'R{i}': 0 for i in range(8)}
        self.flags = {'Z': 0, 'C': 0, 'N': 0, 'V': 0}
        self.special_registers = {'SP': 0xFFF0, 'PC': 0}  # Stack pointer, Program counter
        self.memory = Memory()

    def set_register(self, reg, value):
        if reg in self.registers:
            value &= 0xFFFF
            self.registers[reg] = value
        else:
            raise ValueError("Invalid register specified.")

    def compare(self, reg1, reg2):
        if reg1 in self.registers and reg2 in self.registers:
            value1 = self.registers[reg1]
            value2 = self.registers[reg2]
            self.flags['Z'] = 1 if value1 == value2 else 0
            self.flags['C'] = 1 if value1 < value2 else 0
            self.flags['N'] = 1 if (value1 - value2) & 0x8000 else 0

    def execute_unary_operation(self, operation, reg):
        if reg in self.registers:
            if operation == "NOT":
                self.registers[reg] = ~self.registers[reg] & 0xFFFF
            elif operation == "INC":
                self.registers[reg] = (self.registers[reg] + 1) & 0xFFFF
            elif operation == "DEC":
                self.registers[reg] = (self.registers[reg] - 1) & 0xFFFF
            self.update_flags(self.registers[reg])

    def execute_binary_operation(self, operation, dest, src):
        if dest in self.registers and (src in self.registers or isinstance(src, int)):
            src_value = self.registers[src] if src in self.registers else src & 0xFFFF
            dest_value = self.registers[dest]
            print(operation)
            if operation == "ADD":
                result = dest_value + src_value
                self.registers[dest] = result & 0xFFFF
                self.flags['C'] = 1 if result > 0xFFFF else 0
            elif operation == "SUB":
                result = dest_value - src_value
                self.registers[dest] = result & 0xFFFF
                self.flags['C'] = 1 if dest_value < src_value else 0
            elif operation == "MUL":
                result = dest_value * src_value
                self.registers[dest] = result & 0xFFFF
                self.flags['C'] = 1 if result > 0xFFFF else 0
            elif operation == "DIV":
                if src_value != 0:
                    self.registers[dest] = dest_value // src_value
                else:
                    raise ZeroDivisionError("Attempt to divide by zero.")
            elif operation == "AND":
                self.registers[dest] = dest_value & src_value
            elif operation == "OR":
                self.registers[dest] = dest_value | src_value
            elif operation == "XOR":
                self.registers[dest] = dest_value ^ src_value
            elif operation == "SHL":
                self.registers[dest] = (dest_value << src_value) & 0xFFFF
            elif operation == "SHR":
                self.registers[dest] = (dest_value >> src_value) & 0xFFFF
            self.update_flags(self.registers[dest])

    def update_flags(self, value):
        self.flags['Z'] = 1 if value == 0 else 0
        self.flags['N'] = 1 if value & 0x8000 else 0

    def __str__(self):
        return f'Registers: {self.registers}\nFlags: {self.flags}\nSP: {self.special_registers["SP"]}\nPC: {self.special_registers["PC"]}'


def main():
    processor = SimpleProcessor()
    processor.set_register('R1', 0x0010)
    processor.execute_binary_operation("ADD", 'R1', 0x0020)
    print(processor)



if __name__ == '__main__':
    main()

