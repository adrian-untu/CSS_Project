import unittest

from Processor.processor import *
from Processor.CONFIG import *
from unittest.mock import MagicMock


class UnitTestsProcessor(unittest.TestCase):
    def test_addition(self):
        memory = Memory(instruction_size=INSTRUCTION_MEMORY_SIZE, data_size=DATA_MEMORY_SIZE)
        processor = Processor(memory)
        next_available = memory.next_in_data_memory()
        memory.write_data_memory(next_available, 12)
        processor.registers[0] = next_available
        next_available = memory.next_in_data_memory()
        memory.write_data_memory(next_available, 14)
        processor.registers[1] = next_available
        result = processor.execute_instruction(2, 0, 1)
        self.assertEqual(result, 26)

    def test_substitution(self):
        memory = Memory(instruction_size=INSTRUCTION_MEMORY_SIZE, data_size=DATA_MEMORY_SIZE)
        processor = Processor(memory)
        next_available = memory.next_in_data_memory()
        memory.write_data_memory(next_available, 25)
        processor.registers[0] = next_available
        next_available = memory.next_in_data_memory()
        memory.write_data_memory(next_available, 21)
        processor.registers[1] = next_available
        result = processor.execute_instruction(3, 0, 1)
        self.assertEqual(result, 4)

    def test_multiplication(self):
        memory = Memory(instruction_size=INSTRUCTION_MEMORY_SIZE, data_size=DATA_MEMORY_SIZE)
        processor = Processor(memory)
        next_available = memory.next_in_data_memory()
        memory.write_data_memory(next_available, 15)
        processor.registers[0] = next_available
        next_available = memory.next_in_data_memory()
        memory.write_data_memory(next_available, 23)
        processor.registers[1] = next_available
        result = processor.execute_instruction(4, 0, 1)
        self.assertEqual(result, 345)

    def test_division(self):
        memory = Memory(instruction_size=INSTRUCTION_MEMORY_SIZE, data_size=DATA_MEMORY_SIZE)
        processor = Processor(memory)
        next_available = memory.next_in_data_memory()
        memory.write_data_memory(next_available, 25)
        processor.registers[0] = next_available
        next_available = memory.next_in_data_memory()
        memory.write_data_memory(next_available, 5)
        processor.registers[1] = next_available
        result = processor.execute_instruction(5, 0, 1)
        self.assertEqual(result, 5)

    def test_zero_flag(self):
        memory = Memory(instruction_size=INSTRUCTION_MEMORY_SIZE, data_size=DATA_MEMORY_SIZE)
        processor = Processor(memory)
        # Test setting the zero flag
        next_available = memory.next_in_data_memory()
        memory.write_data_memory(next_available, 0)
        processor.registers[0] = next_available
        next_available = memory.next_in_data_memory()
        memory.write_data_memory(next_available, 0)
        processor.registers[1] = next_available
        processor.execute_instruction(2, 0, 1)  # ADD
        self.assertEqual(processor.flags['Z'], 1)

    def test_jump(self):
        memory = Memory(instruction_size=INSTRUCTION_MEMORY_SIZE, data_size=DATA_MEMORY_SIZE)
        processor = Processor(memory)
        # Test unconditional jump
        processor.jump(5)
        self.assertEqual(processor.program_counter, 5)

    def test_push_and_pop(self):
        memory = Memory(instruction_size=INSTRUCTION_MEMORY_SIZE, data_size=DATA_MEMORY_SIZE)
        processor = Processor(memory)
        # Test stack operations PUSH and POP
        processor.push(42)
        result = processor.pop()
        self.assertEqual(result, 42)

    def test_display_on_screen(self):
        memory = Memory(instruction_size=INSTRUCTION_MEMORY_SIZE, data_size=DATA_MEMORY_SIZE)
        processor = Processor(memory)
        processor.screen_update_callback = MagicMock()
        for result in [0, 5, 99, 1000, 65535]:  # single-digit, multi-digit, edge cases
            processor.display_on_screen(result)

            digits = [digit for digit in str(result)]
            screen_address_index = SCREEN_ADDRESS
            for digit in digits:
                self.assertEqual(memory.read_data_memory(screen_address_index), ord(digit))
                screen_address_index += 2

            processor.screen_update_callback.assert_called()

    def test_read_from_keyboard(self):
        memory = Memory(instruction_size=INSTRUCTION_MEMORY_SIZE, data_size=DATA_MEMORY_SIZE)
        processor = Processor(memory)
        processor.screen_update_callback = MagicMock()
        memory.write_data_memory(KEYBOARD_ADDRESS, ord('a'))
        processor.read_from_keyboard()
        self.assertEqual(processor.keyboard_input, 0)

        memory.write_data_memory(KEYBOARD_ADDRESS, ord('1'))
        processor.read_from_keyboard()
        memory.write_data_memory(KEYBOARD_ADDRESS, ord('2'))
        processor.read_from_keyboard()
        memory.write_data_memory(KEYBOARD_ADDRESS, ord('3'))
        processor.read_from_keyboard()
        self.assertEqual(processor.keyboard_input, 123)

        memory.write_data_memory(KEYBOARD_ADDRESS, 13)
        processor.read_from_keyboard()
        self.assertTrue(processor.read_flag)
        self.assertEqual(processor.get_input(), 123)

    def test_read_instruction(self):
        memory = Memory(instruction_size=INSTRUCTION_MEMORY_SIZE, data_size=DATA_MEMORY_SIZE)
        processor = Processor(memory)
        processor.screen_update_callback = MagicMock()
        input_value = 1234
        for register_index in range(8):
            processor.keyboard_input = input_value
            processor.read_flag = True

            next_available_address = memory.next_in_data_memory()
            opcode = 1
            processor.execute_instruction(opcode, register_index)

            stored_value = memory.read_data_memory(next_available_address)
            self.assertEqual(stored_value, input_value)
            self.assertEqual(processor.registers[register_index], next_available_address)
            self.assertFalse(processor.read_flag)
            self.assertEqual(processor.keyboard_input, 0)

        # no available memory slots
        for i in range(0, len(memory.data_memory), 2):
            memory.write_data_memory(i, i)

        processor.keyboard_input = input_value
        processor.read_flag = True

        opcode = 1
        register_index = 0

        with self.assertRaises(ValueError):
            processor.execute_instruction(opcode, register_index)

        self.assertFalse(processor.read_flag)
        self.assertEqual(processor.keyboard_input, 0)


if __name__ == '__main__':
    unittest.main()
