import tkinter as tk
from CONFIG import *
import time
import threading


class Processor:
    def __init__(self, memory):
        self.memory = memory
        self.keyboard_input = 0
        self.registers = [0] * 8
        self.file_path = 'instructions.txt'
        self.instruction_set = {
            'READ': 1,
            'ADD': 2,
            'SUB': 3
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

    def execute_instruction(self, opcode, operand1, operand2=None):
        try:
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

                print('data memory: ', self.memory.data_memory)

            elif opcode == 3:
                result = self.memory.read_data_memory(self.registers[operand1]) \
                         - self.memory.read_data_memory(self.registers[operand2])
                next_available = self.memory.next_in_data_memory()
                self.memory.write_data_memory(next_available, result)
                self.registers[operand2 + 1] = next_available
                self.display_on_screen(result)

                print('data memory: ', self.memory.data_memory)

            print("Registers:", self.registers)

        except IndexError as e:
            print(f"Error: {e} - Instruction {opcode} with operands {operand1}, {operand2}")


class Memory:
    def __init__(self, instruction_size=1024, data_size=1024):
        self.instruction_memory = [''] * instruction_size
        self.data_memory = [''] * data_size

    def next_in_data_memory(self):
        for i in range(DATA_MEMORY_START_ADDRESS, DATA_MEMORY_SIZE, 2):
            if self.data_memory[i] == '':
                return i
        return -1

    def read_data_memory(self, address):
        if 0 <= address < len(self.data_memory) - 1:
            if address % 2 == 0:
                msb = int(self.data_memory[address], 2)
                lsb = int(self.data_memory[address + 1], 2)
            else:
                msb = int(self.data_memory[address - 1], 2)
                lsb = int(self.data_memory[address], 2)
            return (msb << 8) | lsb
        else:
            print("Invalid memory address:", address)
            raise ValueError("Memory address out of bounds")

    def write_data_memory(self, address, value):
        if 0 <= value < 2 ** 16:
            msb = (value >> 8) & 0xFF
            lsb = value & 0xFF

            # TODO: the memory address must be empty
            if 0 <= address < len(self.data_memory) - 1:
                if address % 2 == 0:
                    self.data_memory[address] = format(msb, '08b')
                    self.data_memory[address + 1] = format(lsb, '08b')
                else:
                    self.data_memory[address - 1] = format(msb, '08b')
                    self.data_memory[address] = format(lsb, '08b')
            else:
                print("Invalid memory address:", address)
                raise ValueError("Memory address out of bounds")

        else:
            print("Invalid value:", value)
            raise ValueError("Value doesn't fit within 16 bits")

    def read_instruction_memory(self, address):
        if 0 <= address < len(self.instruction_memory) - 1:
            msb = int(self.instruction_memory[address], 2)
            return msb
        else:
            print("Invalid memory address:", address)
            raise ValueError("Memory address out of bounds")

    def write_instruction_memory(self, address, value):
        if 0 <= value < 2 ** 8:
            msb = value & 0xFF

            if 0 <= address < len(self.instruction_memory) - 1:
                self.instruction_memory[address] = format(msb, '08b')
            else:
                print("Invalid memory address:", address)
                raise ValueError("Memory address out of bounds")

        else:
            print("Invalid value:", value)
            raise ValueError("Value doesn't fit within 8 bits")

    def clear_data_memory(self):
        self.data_memory = [''] * len(self.data_memory)


class Keyboard(tk.Frame):
    def __init__(self, processor, screen, master=None):
        super().__init__(master)
        self.entry = tk.Entry(self)
        self.processor = processor
        self.screen = screen
        self.create_widgets()

    def on_key_press(self, event):
        char = event.char
        if char:
            self.processor.memory.write_data_memory(KEYBOARD_ADDRESS, ord(char))
            print('data memory: ', self.processor.memory.data_memory)
            self.processor.read_from_keyboard()
            if char == '\r':
                self.entry.delete(0, tk.END)  # Clear entry field
            self.screen.update_screen_integer()

    def create_widgets(self):
        self.entry.pack()
        self.entry.bind("<Key>", self.on_key_press)


class Screen(tk.Frame):
    def __init__(self, processor, master=None, width=80, height=25):
        super().__init__(master)
        self.width = width
        self.height = height
        self.processor = processor
        self.create_widgets()

    def create_widgets(self):
        self.text = tk.Text(self, width=self.width, height=self.height)
        self.text.pack()
        self.update_screen_integer()

    def update_screen_integer(self):
        print("Updating screen...")
        self.text.delete(1.0, tk.END)

        for i in range(SCREEN_ADDRESS, END_SCREEN_ADDRESS, 2):
            if self.processor.memory.data_memory[i] != '' or self.processor.memory.data_memory[i] != '':
                print(str(self.processor.memory.read_data_memory(i)))
                self.text.insert(tk.END, str(chr(self.processor.memory.read_data_memory(i))) + ' ')

        self.text.see(tk.END)


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
