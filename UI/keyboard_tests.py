import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from UI.keyboard import Keyboard

KEYBOARD_ADDRESS = 1022


class TestKeyboard(unittest.TestCase):
    def setUp(self):
        self.patcher_keyboard_address = patch('Processor.CONFIG.KEYBOARD_ADDRESS', KEYBOARD_ADDRESS)

        self.mock_keyboard_address = self.patcher_keyboard_address.start()

        self.processor = MagicMock()
        self.screen = MagicMock()

        self.root = tk.Tk()
        self.keyboard = Keyboard(self.processor, self.screen, self.root)

    def tearDown(self):
        self.patcher_keyboard_address.stop()
        self.root.destroy()

    def test_create_widgets(self):
        self.assertIsInstance(self.keyboard.entry, tk.Entry)
        self.assertIsNotNone(self.keyboard.entry.master)

    def test_on_key_press(self):
        event = MagicMock()
        event.char = 'a'

        self.keyboard.on_key_press(event)

        self.processor.memory.write_data_memory.assert_called_with(KEYBOARD_ADDRESS, ord('a'))
        self.processor.read_from_keyboard.assert_called_once()

    def test_on_key_press_enter_key(self):
        event = MagicMock()
        event.char = '\r'

        self.keyboard.entry.insert(0, 'test')
        self.keyboard.on_key_press(event)

        self.assertEqual(self.keyboard.entry.get(), '')
        self.processor.memory.write_data_memory.assert_called_with(KEYBOARD_ADDRESS, ord('\r'))
        self.processor.read_from_keyboard.assert_called_once()


if __name__ == '__main__':
    unittest.main()
