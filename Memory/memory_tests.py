import unittest
from memory import Memory

from Processor.CONFIG import INSTRUCTION_MEMORY_SIZE, DATA_MEMORY_SIZE, DATA_MEMORY_START_ADDRESS


class TestMemory(unittest.TestCase):
    def setUp(self):
        self.memory = Memory(instruction_size=INSTRUCTION_MEMORY_SIZE, data_size=DATA_MEMORY_SIZE)

    def test_write_read_data_memory(self):
        self.memory.write_data_memory(0, 0x1234)
        self.assertEqual(self.memory.read_data_memory(0), 0x1234)

    def test_write_read_instruction_memory(self):
        self.memory.write_instruction_memory(0, 0x56)
        self.assertEqual(self.memory.read_instruction_memory(0), 0x56)

    def test_out_of_bounds_data_memory(self):
        with self.assertRaises(ValueError):
            self.memory.write_data_memory(DATA_MEMORY_SIZE, 0x1234)

        with self.assertRaises(ValueError):
            self.memory.write_data_memory(-1, 0x1234)

    def test_out_of_bounds_instruction_memory(self):
        with self.assertRaises(ValueError):
            self.memory.write_instruction_memory(INSTRUCTION_MEMORY_SIZE, 0x56)

        with self.assertRaises(ValueError):
            self.memory.write_instruction_memory(-1, 0x1234)

    def test_invalid_value_data_memory(self):
        with self.assertRaises(ValueError):
            self.memory.write_data_memory(0, 0x10000)  # Value out of 16-bit range

    def test_invalid_value_instruction_memory(self):
        with self.assertRaises(ValueError):
            self.memory.write_instruction_memory(0, 0x100)  # Value out of 8-bit range

    def test_boundary_case_data_memory(self):
        self.memory.write_data_memory(DATA_MEMORY_SIZE-1, 0xABCD)
        self.assertEqual(self.memory.read_data_memory(DATA_MEMORY_SIZE-1), 0xABCD)

    def test_boundary_case_instruction_memory(self):
        self.memory.write_data_memory(INSTRUCTION_MEMORY_SIZE-1, 0xABCD)
        self.assertEqual(self.memory.read_data_memory(INSTRUCTION_MEMORY_SIZE-1), 0xABCD)

    def test_data_type_consistency(self):
        self.memory.write_data_memory(0, 1234)  # int
        self.assertEqual(self.memory.read_data_memory(0), 1234)

        self.memory.write_data_memory(2, "h")  # character
        self.assertEqual(self.memory.read_data_memory(1), "h")

        self.memory.write_data_memory(4, 3.14)  # float
        self.assertAlmostEqual(self.memory.read_data_memory(2), 3.14)

    def test_memory_initialization(self):
        for i in range(1024):
            self.assertEqual(self.memory.read_data_memory(i), '')
            self.assertEqual(self.memory.read_instruction_memory(i), '')

    def test_next_in_data_memory(self):
        self.assertEqual(self.memory.next_in_data_memory(), DATA_MEMORY_START_ADDRESS)

        self.memory.write_data_memory(DATA_MEMORY_START_ADDRESS, 0x1234)
        self.assertEqual(self.memory.next_in_data_memory(), DATA_MEMORY_START_ADDRESS + 2)

        for i in range(DATA_MEMORY_START_ADDRESS, DATA_MEMORY_START_ADDRESS + DATA_MEMORY_SIZE, 2):
            self.memory.write_data_memory(i, 0xABCD)
        self.assertEqual(self.memory.next_in_data_memory(), -1)

    def test_clear_data_memory(self):
        self.memory.write_data_memory(0, 0x1234)
        self.assertEqual(self.memory.read_data_memory(0), 0x1234)

        self.memory.clear_data_memory(0)
        with self.assertRaises(ValueError):
            self.memory.read_data_memory(0)


if __name__ == '__main__':
    unittest.main()
