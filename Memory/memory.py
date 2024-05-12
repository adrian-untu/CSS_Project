from Processor.CONFIG import *
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

