import tkinter as tk
from CONFIG import *
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
        self.file_path = 'instructions.txt'
        self.instruction_set = {
            'READ': 1,
            'ADD': 2,
            'SUB': 3,
            'MUL': 4,
            'DIV': 5,
            'INC': 6,
            'DEC': 7,
            'AND': 8,
            'OR': 9,
            'XOR': 10,
            'SHL': 11,
            'SHR': 12,

        }

        self.read_flag = False

    def read_from_keyboard(self):
        buffer_content = self.memory.read_data_memory(KEYBOARD_ADDRESS)
        if buffer_content:
            print('buffer content:', buffer_content)
            if buffer_content != 13:
                self.keyboard_input = self.keyboard_input * 10 + int(chr(buffer_content))
                print('modified input register:', self.keyboard_input)
            else:
                self.read_flag = True

        print(self.read_flag)

    def get_input(self):
        return self.keyboard_input

    def display_on_screen(self, result):
        digits = [digit for digit in str(result)]
        print("digits:", digits)
        screen_address_index = SCREEN_ADDRESS

        for digit in digits:
            print('screen address index:', screen_address_index)
            self.memory.write_data_memory(screen_address_index, ord(digit))
            print(self.memory.read_data_memory(screen_address_index))
            screen_address_index += 2

        print('data memory: ', self.memory.data_memory)

    def load_instructions(self):
        with open(self.file_path, 'r') as file:
            instructions = []
            for line_number, line in enumerate(file, start=1):
                # Split the line into components, remove commas, and strip whitespace
                parts = line.strip().replace(',', '').split()
                parts[0] = self.instruction_set[parts[0]]
                instructions.append(parts)
                self.memory.write_instruction_memory(line_number, parts[0])
        print('instruction memory: ', self.memory.instruction_memory)
        return instructions

    def execute_instruction(self, opcode, operand1=None, operand2=None):
        try:
            if operand1 is not None:
                operand1 = int(operand1)
            if operand2 is not None:
                operand2 = int(operand2)
            print(f"Executing {opcode} with operands {operand1}, {operand2}")

            if opcode == 1:
                while not self.read_flag:
                    time.sleep(0.1)

                next_available = self.memory.next_in_data_memory()
                self.memory.write_data_memory(next_available, self.get_input())
                self.registers[operand1] = next_available

                self.read_flag = False
                self.keyboard_input = 0

            elif opcode == 2:
                result = self.memory.read_data_memory(self.registers[operand1]) \
                         + self.memory.read_data_memory(self.registers[operand2])
                next_available = self.memory.next_in_data_memory()
                self.memory.write_data_memory(next_available, result)
                self.registers[operand2 + 1] = next_available
                self.display_on_screen(result)

            elif opcode == 3:
                result = self.memory.read_data_memory(self.registers[operand1]) \
                         - self.memory.read_data_memory(self.registers[operand2])
                next_available = self.memory.next_in_data_memory()
                self.memory.write_data_memory(next_available, result)
                self.registers[operand2 + 1] = next_available
                self.display_on_screen(result)

            elif opcode == 4:
                result = self.memory.read_data_memory(self.registers[operand1]) \
                         * self.memory.read_data_memory(self.registers[operand2])
                next_available = self.memory.next_in_data_memory()
                self.memory.write_data_memory(next_available, result)
                self.registers[operand2 + 1] = next_available
                self.display_on_screen(result)

            elif opcode == 5:
                # TODO : in memory, make the print also work for float numbers
                if self.memory.read_data_memory(self.registers[operand2]) != 0:
                    result = self.memory.read_data_memory(self.registers[operand1]) \
                             // self.memory.read_data_memory(self.registers[operand2])
                else:
                    raise ZeroDivisionError("Attempt to divide by zero.")
                next_available = self.memory.next_in_data_memory()
                self.memory.write_data_memory(next_available, result)
                self.registers[operand2 + 1] = next_available
                self.display_on_screen(result)

            elif opcode == 6:
                result = self.memory.read_data_memory(self.registers[operand1]) + 1
                self.memory.write_data_memory(self.registers[operand1], result)
                self.display_on_screen(result)

            elif opcode == 7:
                result = self.memory.read_data_memory(self.registers[operand1]) - 1
                self.memory.write_data_memory(self.registers[operand1], result)
                self.display_on_screen(result)

            elif opcode == 8:
                result = (self.memory.read_data_memory(self.registers[operand1]) \
                          & self.memory.read_data_memory(self.registers[operand2])) \
                         // self.memory.read_data_memory(self.registers[operand1])
                next_available = self.memory.next_in_data_memory()
                self.memory.write_data_memory(next_available, result)
                self.registers[operand2 + 1] = next_available
                self.display_on_screen(result)

            elif opcode == 9:
                result = (self.memory.read_data_memory(self.registers[operand1]) \
                          | self.memory.read_data_memory(self.registers[operand2]))

                next_available = self.memory.next_in_data_memory()
                self.memory.write_data_memory(next_available, result)
                self.registers[operand2 + 1] = next_available
                self.display_on_screen(result)

            elif opcode == 10:
                result = (self.memory.read_data_memory(self.registers[operand1]) \
                          ^ self.memory.read_data_memory(self.registers[operand2]))

                next_available = self.memory.next_in_data_memory()
                self.memory.write_data_memory(next_available, result)
                self.registers[operand2 + 1] = next_available
                self.display_on_screen(result)

            elif opcode == 11:
                result = (self.memory.read_data_memory(self.registers[operand1]) \
                          << self.memory.read_data_memory(self.registers[operand2])) & 0xFFFF

                next_available = self.memory.next_in_data_memory()
                self.memory.write_data_memory(next_available, result)
                self.registers[operand2 + 1] = next_available
                self.display_on_screen(result)

            elif opcode == 12:
                result = (self.memory.read_data_memory(self.registers[operand1]) \
                          >> self.memory.read_data_memory(self.registers[operand2])) & 0xFFFF

                next_available = self.memory.next_in_data_memory()
                self.memory.write_data_memory(next_available, result)
                self.registers[operand2 + 1] = next_available
                self.display_on_screen(result)



            print('data memory: ', self.memory.data_memory)
            print("Registers:", self.registers)

        except IndexError as e:
            print(f"Error: {e} - Instruction {opcode} with operands {operand1}, {operand2}")


def run_interface():
    root = tk.Tk()

    screen = Screen(processor, master=root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    keyboard = Keyboard(processor, screen, master=root)

    keyboard.pack(side="left")
    screen.pack(side="right")

    root.mainloop()


def run_processor():
    instructions = processor.load_instructions()

    for inst in instructions:
        try:
            if len(inst) == 3:
                processor.execute_instruction(inst[0], int(inst[1]), int(inst[2]))
            elif len(inst) == 2:
                processor.execute_instruction(inst[0], int(inst[1]))
            elif len(inst) == 1:
                processor.execute_instruction(inst[0])
        except ValueError as e:
            print(f"Error processing instruction {inst}: {e}")


if __name__ == '__main__':
    memory = Memory(instruction_size=INSTRUCTION_MEMORY_SIZE, data_size=DATA_MEMORY_SIZE)
    processor = Processor(memory)

    interface_thread = threading.Thread(target=run_interface)
    processor_thread = threading.Thread(target=run_processor)

    interface_thread.start()
    processor_thread.start()

    interface_thread.join()
    processor_thread.join()
