import unittest
from unittest.mock import MagicMock
from Processor.processor import *
from Processor.CONFIG import *

class TestProcessor(unittest.TestCase):

    def test_and_instruction(self):
        # AND instruction test
        memory = Memory(instruction_size=INSTRUCTION_MEMORY_SIZE, data_size=DATA_MEMORY_SIZE)
        processor = Processor(memory)
        next_available = memory.next_in_data_memory()
        memory.write_data_memory(next_available, 12)
        processor.registers[0] = next_available
        next_available = memory.next_in_data_memory()
        memory.write_data_memory(next_available, 10)
        processor.registers[1] = next_available
        processor.execute_instruction(15, 0, 1)
        expected_result = (12 & 10) // 12
        self.assertEqual(memory.read_data_memory(0), expected_result)

    def test_or_instruction(self):
        # OR instruction test
        memory = Memory(instruction_size=INSTRUCTION_MEMORY_SIZE, data_size=DATA_MEMORY_SIZE)
        processor = Processor(memory)
        next_available = memory.next_in_data_memory()
        memory.write_data_memory(next_available, 12)
        processor.registers[0] = next_available
        next_available = memory.next_in_data_memory()
        memory.write_data_memory(next_available, 10)
        processor.registers[1] = next_available
        processor.execute_instruction(16, 0, 1)
        expected_result = 12 | 10
        self.assertEqual(memory.read_data_memory(0), expected_result)

    def test_xor_instruction(self):
        # XOR instruction test
        memory = Memory(instruction_size=INSTRUCTION_MEMORY_SIZE, data_size=DATA_MEMORY_SIZE)
        processor = Processor(memory)
        next_available = memory.next_in_data_memory()
        memory.write_data_memory(next_available, 12)
        processor.registers[0] = next_available
        next_available = memory.next_in_data_memory()
        memory.write_data_memory(next_available, 10)
        processor.registers[1] = next_available
        processor.execute_instruction(17, 0, 1)
        expected_result = 12 ^ 10
        self.assertEqual(memory.read_data_memory(0), expected_result)

    def test_shl_instruction(self):
        # SHL instruction test
        memory = Memory(instruction_size=INSTRUCTION_MEMORY_SIZE, data_size=DATA_MEMORY_SIZE)
        processor = Processor(memory)
        next_available = memory.next_in_data_memory()
        memory.write_data_memory(next_available, 1)
        processor.registers[0] = next_available
        next_available = memory.next_in_data_memory()
        memory.write_data_memory(next_available, 4)
        processor.registers[1] = next_available
        processor.execute_instruction(18, 0, 1)
        expected_result = (1 << 4) & 0xFFFF
        self.assertEqual(memory.read_data_memory(0), expected_result)

    def test_shr_instruction(self):
        # SHR instruction test
        memory = Memory(instruction_size=INSTRUCTION_MEMORY_SIZE, data_size=DATA_MEMORY_SIZE)
        processor = Processor(memory)
        next_available = memory.next_in_data_memory()
        memory.write_data_memory(next_available, 16)
        processor.registers[0] = next_available
        next_available = memory.next_in_data_memory()
        memory.write_data_memory(next_available, 2)
        processor.registers[1] = next_available
        processor.execute_instruction(19, 0, 1)
        expected_result = (16 >> 2) & 0xFFFF
        self.assertEqual(memory.read_data_memory(0), expected_result)

if __name__ == '__main__':
    unittest.main()
