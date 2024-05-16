import unittest
from unittest.mock import MagicMock
import processor
from Memory import memory

class TestProcessor(unittest.TestCase):
    def setUp(self):
        self.memory = memory.Memory
        self.processor = processor.Processor

    def test_and_instruction(self):
        # AND instruction test
        self.memory = memory.Memory
        self.processor = processor.Processor

        self.processor.registers[0] = 0
        self.processor.registers[1] = 1
        self.memory.write_data_memory(0, 12)
        self.memory.write_data_memory(1, 10)
        self.processor.execute_instruction(15, 0, 1)
        expected_result = (12 & 10) // 12
        self.assertEqual(self.memory.read_data_memory(0), expected_result)

    def test_or_instruction(self):
        # OR instruction test
        self.processor.registers[0] = 0
        self.processor.registers[1] = 1
        self.memory.write_data_memory(0, 12)
        self.memory.write_data_memory(1, 10)
        self.processor.execute_instruction(16, 0, 1)
        expected_result = 12 | 10
        self.assertEqual(self.memory.read_data_memory(0), expected_result)

    def test_xor_instruction(self):
        # XOR instruction test
        self.processor.registers[0] = 0
        self.processor.registers[1] = 1
        self.memory.write_data_memory(0, 12)
        self.memory.write_data_memory(1, 10)
        self.processor.execute_instruction(17, 0, 1)
        expected_result = 12 ^ 10
        self.assertEqual(self.memory.read_data_memory(0), expected_result)

    def test_shl_instruction(self):
        # SHL instruction test
        self.processor.registers[0] = 0
        self.processor.registers[1] = 1
        self.memory.write_data_memory(0, 1)
        self.memory.write_data_memory(1, 4)
        self.processor.execute_instruction(18, 0, 1)
        expected_result = (1 << 4) & 0xFFFF
        self.assertEqual(self.memory.read_data_memory(0), expected_result)

    def test_shr_instruction(self):
        # SHR instruction test
        self.processor.registers[0] = 0
        self.processor.registers[1] = 1
        self.memory.write_data_memory(0, 16)
        self.memory.write_data_memory(1, 2)
        self.processor.execute_instruction(19, 0, 1)
        expected_result = (16 >> 2) & 0xFFFF
        self.assertEqual(self.memory.read_data_memory(0), expected_result)

if __name__ == '__main__':
    unittest.main()
