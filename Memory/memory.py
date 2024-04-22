class Memory:
    def __init__(self, size=65536):  # Default to max size
        self.memory = [0] * size

    def read(self, address):
        # Ensure we read two consecutive addresses (16-bit wide)
        high = self.memory[address]
        low = self.memory[address + 1]
        return (high << 8) | low

    def write(self, address, value):
        # Split the 16-bit value into two 8-bit parts and write them to consecutive addresses
        high = (value >> 8) & 0xFF
        low = value & 0xFF
        self.memory[address] = high
        self.memory[address + 1] = low
