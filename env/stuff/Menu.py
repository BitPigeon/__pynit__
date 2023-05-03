from tkinter import *
from tkinter.ttk import *

class Menu(Menubar):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.parent.config(menu=self)
        self.file_menu = Menubar(root, tearoff=0)
        self.file_menu.add_seperator()
        self.file_menu.add_command("Close", command=self.close_main_window)
    def close_main_window(self):
        self.parent.destroy()
