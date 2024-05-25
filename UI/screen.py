import tkinter as tk
from Processor.CONFIG import SCREEN_ADDRESS, END_SCREEN_ADDRESS


class Screen(tk.Frame):
    def __init__(self, processor, master=None, width=80, height=25):

        assert processor is not None, "Processor must not be None"
        assert master is not None, "Master (root window) must not be None"
        assert isinstance(width, int) and width > 0, "Width must be a positive integer"
        assert isinstance(height, int) and height > 0, "Height must be a positive integer"

        super().__init__(master)
        self.width = width
        self.height = height
        self.processor = processor
        self.create_widgets()

        assert self.text.cget("width") == width, f"Text widget width must be {width}"
        assert self.text.cget("height") == height, f"Text widget height must be {height}"

    def create_widgets(self):
        self.text = tk.Text(self, width=self.width, height=self.height)
        self.text.pack()

        assert self.text is not None, "Text widget must be created"
        assert self.text.cget("width") == self.width, f"Text widget width must be {self.width}"
        assert self.text.cget("height") == self.height, f"Text widget height must be {self.height}"

        self.update_screen_integer()

    def update_screen_integer(self):
        print("Updating screen...")
        self.text.delete(1.0, tk.END)

        for i in range(SCREEN_ADDRESS, END_SCREEN_ADDRESS, 2):

            assert i >= SCREEN_ADDRESS and i < END_SCREEN_ADDRESS, "Memory address must be within valid range"

            if self.processor.memory.data_memory[i] != '':
                self.text.insert(tk.END, str(chr(self.processor.memory.read_data_memory(i))) + ' ')

        self.text.see(tk.END)

        text_content = self.text.get("1.0", tk.END).strip()
        for ch in text_content:
            assert ch == ' ' or isinstance(ord(ch), int), "Text content must be valid characters"

