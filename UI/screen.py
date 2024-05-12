import tkinter as tk
from Processor.CONFIG import *


class Screen(tk.Frame):
    def __init__(self, processor, master=None, width=80, height=25):
        super().__init__(master)
        self.width = width
        self.height = height
        self.processor = processor
        self.create_widgets()

    def create_widgets(self):
        self.text = tk.Text(self, width=self.width, height=self.height)
        self.text.pack()
        self.update_screen_integer()

    def update_screen_integer(self):
        print("Updating screen...")
        self.text.delete(1.0, tk.END)

        for i in range(SCREEN_ADDRESS, END_SCREEN_ADDRESS, 2):
            if self.processor.memory.data_memory[i] != '':
                self.text.insert(tk.END, str(chr(self.processor.memory.read_data_memory(i))) + ' ')

        self.text.see(tk.END)
