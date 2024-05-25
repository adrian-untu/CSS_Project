import tkinter as tk
from Processor.CONFIG import KEYBOARD_ADDRESS


class Keyboard(tk.Frame):
    def __init__(self, processor, screen, master=None):
        super().__init__(master)
        assert processor is not None, "Processor should not be None"
        assert screen is not None, "Screen should not be None"

        self.entry = tk.Entry(self)
        self.processor = processor
        self.screen = screen
        self.create_widgets()

        assert self.entry is not None, "Entry widget should be created"
        assert isinstance(self.processor, object), "Processor should be an object"
        assert isinstance(self.screen, object), "Screen should be an object"

    def on_key_press(self, event):
        char = event.char
        if char:
            assert len(char) == 1, "Only single characters should be processed"
            self.processor.memory.write_data_memory(KEYBOARD_ADDRESS, ord(char))

            assert self.processor.memory.read_data_memory(KEYBOARD_ADDRESS) == ord(char), "Memory should contain the " \
                                                                                          "written character"

            self.processor.read_from_keyboard()

            if char == '\r':
                self.entry.delete(0, tk.END)
                assert self.entry.get() == '', "Entry should be cleared after Enter key is pressed"

    def create_widgets(self):
        self.entry.pack()
        self.entry.bind("<Key>", self.on_key_press)

