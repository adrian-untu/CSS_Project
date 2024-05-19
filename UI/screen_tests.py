import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from UI.screen import Screen

DATA_MEMORY_SIZE = 1024
SCREEN_ADDRESS = DATA_MEMORY_SIZE - 256
END_SCREEN_ADDRESS = DATA_MEMORY_SIZE - 4


class TestScreen(unittest.TestCase):
    def setUp(self):
        self.patcher_screen_address = patch('Processor.CONFIG.SCREEN_ADDRESS', SCREEN_ADDRESS)
        self.patcher_end_screen_address = patch('Processor.CONFIG.END_SCREEN_ADDRESS', END_SCREEN_ADDRESS)

        self.mock_screen_address = self.patcher_screen_address.start()
        self.mock_end_screen_address = self.patcher_end_screen_address.start()

        self.processor = MagicMock()
        self.processor.memory.data_memory = [''] * DATA_MEMORY_SIZE  # Ensure enough memory
        self.processor.memory.read_data_memory = MagicMock(side_effect=lambda x: ord('A') if x % 2 == 0 else ord('B'))

        self.root = tk.Tk()
        self.screen = Screen(self.processor, self.root)

    def tearDown(self):
        self.patcher_screen_address.stop()
        self.patcher_end_screen_address.stop()
        self.root.destroy()

    def test_create_widgets(self):
        self.assertIsInstance(self.screen.text, tk.Text)
        self.assertEqual(self.screen.text.cget("width"), 80)
        self.assertEqual(self.screen.text.cget("height"), 25)

    def test_update_screen_integer(self):
        self.processor.memory.data_memory[SCREEN_ADDRESS] = 65  # 'A'
        self.processor.memory.data_memory[SCREEN_ADDRESS + 2] = 65  # 'A'
        self.processor.memory.data_memory[SCREEN_ADDRESS + 4] = 65  # 'A'

        self.screen.update_screen_integer()
        expected_text = "A A A "
        actual_text = self.screen.text.get(1.0, tk.END).replace('\n', ' ')

        self.assertEqual(actual_text.strip(), expected_text.strip())

    def test_update_screen_integer_empty(self):
        for i in range(SCREEN_ADDRESS, SCREEN_ADDRESS + 6, 2):
            self.processor.memory.data_memory[i] = ''

        self.screen.update_screen_integer()
        actual_text = self.screen.text.get(1.0, tk.END).strip()
        self.assertEqual(actual_text, '')


if __name__ == '__main__':
    unittest.main()
