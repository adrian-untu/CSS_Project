import tkinter as tk
from CONFIG import STACK_ADDRESS, KEYBOARD_ADDRESS, SCREEN_ADDRESS, END_SCREEN_ADDRESS, SCREEN_WIDTH, SCREEN_HEIGHT, INSTRUCTION_MEMORY_SIZE, DATA_MEMORY_SIZE
import time
import threading
from Memory.memory import Memory
from UI.screen import Screen
from UI.keyboard import Keyboard


class Processor:
    def __init__(self, memory):
        self.memory = memory
        self.keyboard_input = 0
        self.registers = [0] * 8
        self.program_counter = 1  # Needed for program flow
        self.stack_pointer = STACK_ADDRESS
        self.flags = {'Z': 0, 'C': 0, 'N': 0, 'V': 0}
        self.file_path = 'instructions.txt'
        self.instruction_set = {
            'READ': 1,
            'ADD': 2,
            'SUB': 3,
            'MUL': 4,
            'DIV': 5,
            'INC': 6,
            'DEC': 7,
            'JMP': 8,
            'JZ': 9,
            'JNZ': 10,
            'CALL': 11,
            'RET': 12,
            'PUSH': 13,
            'POP': 14,
            'AND': 15,
            'OR': 16,
            'XOR': 17,
            'SHL': 18,
            'SHR': 19
        }
        self.read_flag = False
        self.screen_update_callback = None  # Callback function for screen updates
        self.executed_procedures = set()
        self.call_active = False

    def compare(self, reg1, reg2):
        # Assume reg1 and reg2 are register indices
        value1 = self.registers[reg1]
        value2 = self.registers[reg2]
        self.flags['Z'] = 1 if value1 == value2 else 0
        self.flags['C'] = 1 if value1 < value2 else 0
        self.flags['N'] = 1 if (value1 - value2) < 0 else 0

    def update_flags(self, value):
        self.flags['Z'] = 1 if value == 0 else 0
        self.flags['N'] = 1 if value < 0 else 0
        self.flags['C'] = 0  # Typically determined by the context of arithmetic

    def update_arithmetic_flags(self, result, value1, value2, operation='ADD'):
        self.update_flags(result)
        max_int = 0xFFFF
        if operation == 'ADD':
            self.flags['V'] = 1 if (value1 > 0 and value2 > 0 and result < 0) or (
                        value1 < 0 and value2 < 0 and result > 0) else 0
            self.flags['C'] = 1 if value1 + value2 > max_int else 0
        elif operation == 'SUB':
            self.flags['V'] = 1 if (value1 > 0 and value2 < 0 and result < 0) or (
                        value1 < 0 and value2 > 0 and result > 0) else 0
            self.flags['C'] = 1 if value1 < value2 else 0

    def push(self, value):
        self.stack_pointer += 2
        self.memory.write_data_memory(self.stack_pointer, value)

    def pop(self):
        value = self.memory.read_data_memory(self.stack_pointer)
        self.memory.clear_data_memory(self.stack_pointer)
        self.stack_pointer -= 2
        return value

    def jump(self, address):
        self.program_counter = address

    def conditional_jump(self, condition):
        if condition:
            self.program_counter = self.memory.read_data_memory(self.program_counter + 1)

    def call(self, address):
        self.push(self.program_counter)
        self.program_counter = address

    def ret(self):
        self.program_counter = self.pop()
        self.call_active = False

    def read_from_keyboard(self):
        buffer_content = self.memory.read_data_memory(KEYBOARD_ADDRESS)
        if buffer_content:
            if buffer_content != 13:
                self.keyboard_input = self.keyboard_input * 10 + int(chr(buffer_content))
                print('Modified input register:', self.keyboard_input)
            else:
                self.read_flag = True

    def get_input(self):
        return self.keyboard_input

    def display_on_screen(self, result):
        digits = [digit for digit in str(result)]
        screen_address_index = SCREEN_ADDRESS
        for _ in range(SCREEN_ADDRESS, END_SCREEN_ADDRESS):
            self.memory.clear_data_memory(_)
        for digit in digits:
            self.memory.write_data_memory(screen_address_index, ord(digit))
            screen_address_index += 2

        if self.screen_update_callback:
            self.screen_update_callback()  # Call the callback function for screen update
            time.sleep(0.7)

    def load_instructions(self):
        with open(self.file_path, 'r') as file:
            instructions = []
            for line_number, line in enumerate(file, start=1):
                parts = line.strip().replace(',', '').split()
                parts[0] = self.instruction_set[parts[0]]
                instructions.append(parts)
                self.memory.write_instruction_memory(line_number, parts[0])
        print('Instruction memory:', self.memory.instruction_memory)
        return instructions

    def run(self):
        instructions = self.load_instructions()
        while self.memory.read_instruction_memory(self.program_counter) != '' and self.program_counter <= len(instructions):
            try:
                inst = instructions[self.program_counter-1]
                inst_code = self.memory.read_instruction_memory(self.program_counter)

                if self.program_counter in self.executed_procedures:
                    self.program_counter += 1
                    continue

                if inst[0] == 11:
                    self.call_active = True

                if self.call_active is True:
                    self.executed_procedures.add(self.program_counter)

                # else:
                if len(inst) == 3:
                    processor.execute_instruction(inst_code, int(inst[1]), int(inst[2]))
                elif len(inst) == 2:
                    processor.execute_instruction(inst_code, int(inst[1]))
                elif len(inst) == 1:
                    processor.execute_instruction(inst_code)
                if inst[0] not in [8, 11]:
                    self.program_counter += 1

            except ValueError as e:
                print(f"Error processing instruction {inst}: {e}")

    def execute_instruction(self, opcode, operand1=None, operand2=None):
        try:
            operand1 = int(operand1) if operand1 is not None else None
            operand2 = int(operand2) if operand2 is not None else None
            print(
                f"Executing {list(self.instruction_set.keys())[list(self.instruction_set.values()).index(opcode)]} with operands {operand1}, {operand2}")

            if opcode == 1:
                while not self.read_flag:
                    time.sleep(0.1)
                next_available = self.memory.next_in_data_memory()
                self.memory.write_data_memory(next_available, self.get_input())
                self.registers[operand1] = next_available
                self.read_flag = False
                self.keyboard_input = 0

            elif opcode == 2:
                result = self.memory.read_data_memory(self.registers[operand1]) + self.memory.read_data_memory(
                    self.registers[operand2])
                next_available = operand1
                self.memory.write_data_memory(next_available, result)
                self.compare(operand1, operand2)
                self.update_arithmetic_flags(result, self.memory.read_data_memory(self.registers[operand1]),
                                             self.memory.read_data_memory(self.registers[operand2]), 'ADD')
                self.display_on_screen(result)

            elif opcode == 3:
                result = self.memory.read_data_memory(self.registers[operand1]) - self.memory.read_data_memory(
                    self.registers[operand2])
                next_available = operand1
                self.memory.write_data_memory(next_available, result)
                self.compare(operand1, operand2)
                self.update_arithmetic_flags(result, self.memory.read_data_memory(self.registers[operand1]),
                                             self.memory.read_data_memory(self.registers[operand2]), 'SUB')
                self.display_on_screen(result)

            elif opcode == 4:
                result = self.memory.read_data_memory(self.registers[operand1]) * self.memory.read_data_memory(
                    self.registers[operand2])
                next_available = operand1
                self.memory.write_data_memory(next_available, result)
                self.compare(operand1, operand2)
                self.update_flags(result)
                self.display_on_screen(result)

            elif opcode == 5:
                if self.memory.read_data_memory(self.registers[operand2]) != 0:
                    result = self.memory.read_data_memory(self.registers[operand1]) // self.memory.read_data_memory(
                        self.registers[operand2])
                else:
                    raise ZeroDivisionError("Attempt to divide by zero.")
                next_available = operand1
                self.memory.write_data_memory(next_available, result)
                self.compare(operand1, operand2)
                self.update_flags(result)
                self.display_on_screen(result)

            elif opcode == 6:
                result = self.memory.read_data_memory(self.registers[operand1]) + 1
                self.memory.write_data_memory(self.registers[operand1], result)
                self.update_flags(result)
                self.display_on_screen(result)

            elif opcode == 7:
                result = self.memory.read_data_memory(self.registers[operand1]) - 1
                self.memory.write_data_memory(self.registers[operand1], result)
                self.update_flags(result)
                self.display_on_screen(result)

            elif opcode == 8:
                self.jump(operand1)

            elif opcode == 9:
                if self.flags['Z'] == 1:
                    self.jump(operand1)

            elif opcode == 10:
                if self.flags['Z'] == 0:
                    self.jump(operand1)

            elif opcode == 11:
                self.call(operand1)

            elif opcode == 12:
                self.ret()

            elif opcode == 13:
                self.push(self.registers[operand1])

            elif opcode == 14:
                result = self.pop()
                self.display_on_screen(result)

            elif opcode == 15:
                result = (self.memory.read_data_memory(self.registers[operand1]) \
                          & self.memory.read_data_memory(self.registers[operand2])) \
                         // self.memory.read_data_memory(self.registers[operand1])
                next_available = operand1
                self.memory.write_data_memory(next_available, result)
                self.display_on_screen(result)

            elif opcode == 16:
                result = (self.memory.read_data_memory(self.registers[operand1]) \
                          | self.memory.read_data_memory(self.registers[operand2]))

                next_available = operand1
                self.memory.write_data_memory(next_available, result)
                self.display_on_screen(result)

            elif opcode == 17:
                result = (self.memory.read_data_memory(self.registers[operand1]) \
                          ^ self.memory.read_data_memory(self.registers[operand2]))

                next_available = operand1
                self.memory.write_data_memory(next_available, result)
                self.display_on_screen(result)

            elif opcode == 18:
                result = (self.memory.read_data_memory(self.registers[operand1]) \
                          << self.memory.read_data_memory(self.registers[operand2])) & 0xFFFF

                next_available = operand1
                self.memory.write_data_memory(next_available, result)
                self.display_on_screen(result)

            elif opcode == 19:
                result = (self.memory.read_data_memory(self.registers[operand1]) \
                          >> self.memory.read_data_memory(self.registers[operand2])) & 0xFFFF

                next_available = operand1
                self.memory.write_data_memory(next_available, result)
                self.display_on_screen(result)

            print('Data Memory:', self.memory.data_memory)
            print("Registers:", self.registers)
            print("Flags:", self.flags)

        except IndexError as e:
            print(
                f"Error: {e} - Instruction {list(self.instruction_set.keys())[list(self.instruction_set.values()).index(opcode)]} with operands {operand1}, {operand2}")


def run_interface():
    root = tk.Tk()

    screen = Screen(processor, master=root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    keyboard = Keyboard(processor, screen, master=root)

    processor.screen_update_callback = screen.update_screen_integer  # Set the callback function

    keyboard.pack(side="left")
    screen.pack(side="right")

    root.mainloop()


def run_processor():
    processor.run()


if __name__ == '__main__':
    memory = Memory(instruction_size=INSTRUCTION_MEMORY_SIZE, data_size=DATA_MEMORY_SIZE)
    processor = Processor(memory)

    interface_thread = threading.Thread(target=run_interface)
    processor_thread = threading.Thread(target=run_processor)

    interface_thread.start()
    processor_thread.start()

    interface_thread.join()
    processor_thread.join()
