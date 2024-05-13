import tkinter as tk
from Processor.CONFIG import KEYBOARD_ADDRESS


class Keyboard(tk.Frame):
    def __init__(self, processor, screen, master=None):
        super().__init__(master)
        self.entry = tk.Entry(self)
        self.processor = processor
        self.screen = screen
        self.create_widgets()

    def on_key_press(self, event):
        char = event.char
        if char:
            self.processor.memory.write_data_memory(KEYBOARD_ADDRESS, ord(char))
            self.processor.read_from_keyboard()
            if char == '\r':
                self.entry.delete(0, tk.END)  # Clear entry field
                # self.screen.update_screen_integer()

    def create_widgets(self):
        self.entry.pack()
        self.entry.bind("<Key>", self.on_key_press)
