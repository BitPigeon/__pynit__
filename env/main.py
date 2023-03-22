#!/usr/bin/env python

from tkinter.ttk import *
from stuff.Editor import *
from stuff.GetModuleContents import *
import tkinter.messagebox as m
import re
import mysql.connector
import sys

root = Tk()
root.geometry("700x550")
root.title("__pynit__")

editor = Editor()
editor.pack(fill="both", expand=True)
root.mainloop()
