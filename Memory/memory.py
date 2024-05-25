from Processor.CONFIG import DATA_MEMORY_START_ADDRESS, DATA_MEMORY_SIZE


class Memory:
    def __init__(self, instruction_size=1024, data_size=1024):
        assert instruction_size % 1024 == 0, "Instruction memory size must be a multiple of 1 KB"
        assert data_size % 1024 == 0, "Data memory size must be a multiple of 1 KB"
        assert instruction_size <= 65536, "Instruction memory size exceeds the maximum limit"
        assert data_size <= 65536, "Data memory size exceeds the maximum limit"

        self.instruction_memory = [''] * instruction_size
        self.data_memory = [''] * data_size

        assert len(self.instruction_memory) == instruction_size, "Instruction memory initialization failed"
        assert len(self.data_memory) == data_size, "Data memory initialization failed"

    def next_in_data_memory(self):
        for i in range(DATA_MEMORY_START_ADDRESS, DATA_MEMORY_SIZE, 2):
            assert 0 <= i < len(self.data_memory), "Next address out of bounds"
            if self.data_memory[i] == '':
                return i
        return -1

    def read_data_memory(self, address):
        assert 0 <= address < len(self.data_memory) - 1, "Memory address out of bounds"

        if self.data_memory[address] != '':
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
        assert 0 <= address < len(self.data_memory) - 1, "Memory address out of bounds"
        assert 0 <= value < 2 ** 16, "Value doesn't fit within 16 bits"

        if value == '':
            return

        msb = (value >> 8) & 0xFF
        lsb = value & 0xFF

        if address % 2 == 0:
            self.data_memory[address] = format(msb, '08b')
            self.data_memory[address + 1] = format(lsb, '08b')
        else:
            self.data_memory[address - 1] = format(msb, '08b')
            self.data_memory[address] = format(lsb, '08b')

        written_value = self.read_data_memory(address)
        assert written_value == value, f"Memory write failed: expected {value}, got {written_value}"

    def read_instruction_memory(self, address):
        assert 0 <= address < len(self.instruction_memory) - 1, "Memory address out of bounds"

        if self.instruction_memory[address] == '':
            return

        msb = int(self.instruction_memory[address], 2)
        return msb

    def write_instruction_memory(self, address, value):
        assert 0 <= address < len(self.instruction_memory) - 1, "Memory address out of bounds"
        assert 0 <= value < 2 ** 8, "Value doesn't fit within 8 bits"

        msb = value & 0xFF

        assert 0 <= address < len(self.instruction_memory) - 1, "Memory address out of bounds"
        self.instruction_memory[address] = format(msb, '08b')

        written_value = self.read_instruction_memory(address)
        assert written_value == msb, f"Instruction memory write failed: expected {msb}, got {written_value}"

    def clear_data_memory(self, idx):
        assert 0 <= idx < len(self.data_memory), "Memory address out of bounds"
        self.data_memory[idx] = ''
