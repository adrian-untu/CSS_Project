from Memory.memory import Memory


class Processor:
    def __init__(self):
        # Initialize 8 data registers
        self.registers = [0] * 8
        # Special-purpose registers
        self.program_counter = 0
        self.stack_pointer = 0xFFFF  # Example stack pointer initialization
        # Flags
        self.flags = {
            'Z': 0,  # Zero flag
            'C': 0,  # Carry flag
            'N': 0,  # Negative flag
            'V': 0   # Overflow flag
        }
        self.memory = Memory()
        self.file_path = 'instructions.txt'

    def set_flag(self, flag, value):
        self.flags[flag] = value

    def get_flag(self, flag):
        return self.flags[flag]

    def push(self, register_index):
        # Ensure register_index is an integer
        register_index = int(register_index)
        # Decrement stack pointer by 2 for 16-bit width data
        self.stack_pointer -= 2
        # Write the register's value to the stack
        self.memory.write(self.stack_pointer, self.registers[register_index])

    def pop(self, register_index):
        # Read the value from the stack into the register
        self.registers[register_index] = self.memory.read(self.stack_pointer)
        # Increment stack pointer by 2 for 16-bit width data
        self.stack_pointer += 2

    def call(self, address):
        # Push the next instruction address onto the stack (program counter + 1 for simplicity)
        self.push(self.program_counter + 1)
        # Set program counter to the new address (function address)
        self.program_counter = address

    def ret(self):
        # Pop the return address off the stack into the program counter
        self.pop('PC')  # Adjust if PC is not handled like a normal register

    def execute_instruction(self, opcode, operand1, operand2=None):
        try:
            operand1 = int(operand1)
            if operand2 is not None:
                operand2 = int(operand2)
            print(f"Executing {opcode} with operands {operand1}, {operand2}")

            if opcode == 'MOV':
                self.registers[operand1] = operand2
                print(f"MOV: Register[{operand1}] = {operand2}")
                print(f"MOV: Stack Pointer at {self.stack_pointer}")

            elif opcode == 'ADD':
                result = self.registers[operand1] + self.registers[operand2]
                self.registers[operand1] = result & 0xFFFF
                self.set_flag('Z', 1 if result == 0 else 0)
                print(f"ADD: Register[{operand1}] = {self.registers[operand1]}, Zero flag set to {self.get_flag('Z')}")
                print(f"ADD: Stack Pointer at {self.stack_pointer}")

            elif opcode == 'PUSH':
                self.push(operand1)
                print(f"PUSH: Stack Pointer at {self.stack_pointer}")

            elif opcode == 'POP':
                self.pop(operand1)
                print(f"POP: Register[{operand1}] = {self.registers[operand1]}, Stack Pointer at {self.stack_pointer}")

            elif opcode == 'CALL':
                self.call(operand1)  # Directly use operand1 as address
                print(f"CALL: Jump to address {operand1}, Stack Pointer at {self.stack_pointer}")

            elif opcode == 'RET':
                self.ret()
                print(f"RET: Return to address at Program Counter {self.program_counter}")

            # Extend with other operations as needed

        except IndexError as e:
            print(f"Error: {e} - Instruction {opcode} with operands {operand1}, {operand2}")

    def load_instructions(self):
        with open(self.file_path, 'r') as file:
            instructions = []
            for line in file:
                # Split the line into components, remove commas, and strip whitespace
                parts = line.strip().replace(',', '').split()
                instructions.append(parts)
        return instructions


def main():
    cpu = Processor()
    instructions = cpu.load_instructions()
    for inst in instructions:
        try:
            if len(inst) == 3:
                cpu.execute_instruction(inst[0], int(inst[1]), int(inst[2]))
            elif len(inst) == 2:
                cpu.execute_instruction(inst[0], int(inst[1]))
        except ValueError as e:
            print(f"Error processing instruction {inst}: {e}")

if __name__ == '__main__':
    main()
