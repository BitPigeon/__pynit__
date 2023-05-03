#!/usr/bin/env python

from tkinter import END, Tk, filedialog
from tkinter.scrolledtext import ScrolledText
import re
import os

class Editor(ScrolledText):
    
    def __init__(self):
        super().__init__()
        self.keywords = ["False", "True", "NotImplemented", "as", "and", "or", "not", "break", "continue", "class", "def", "if", "elif", "else", "for", "while", "in", "is", "None", "lambda", "return", "yield", "async" "nonlocal", "global", "import", "from", "raise", "pass", "with", "finally", "try", "except", "or", "and", "elif", "await", "assert"]
        self.builtins = ["quit", "abs", "aiter", "all", "any", "anext", "ascii", "bin", "bool", "breakpoint", "bytearray", "bytes", "callable", "chr", "classmethod", "compile", "complex", "delattr", "dict", "dir", "divmod", "enumerate", "eval", "exec", "filter", "float", "format", "frozenset", "getattr", "globals", "hasattr", "hash", "help", "hex", "id", "input", "int", "isinstance", "issubclass", "iter", "len", "list", "locals", "map", "max", "memoryview", "min", "next", "object", "oct", "open", "ord", "pow", "print", "property", "range", "repr", "reversed", "round", "set", "setattr", "slice", "sorted", "staticmethod", "str", "sum", "super", "tuple", "type", "vars", "zip", "BaseException", "Exception", "ArithmeticError", "BufferError", "LookupError", "AssertionError", "AtributeError", "EOFError", "FloatingPointError", "GeneratorExit", "ImportError", "ModuleNotFoundError", "IndexError", "KeyError", "KeyboardInterrupt", "MemoryError", "NameError", "NotImplementedError", "OSError", "OverflowError", "RecursionError", "ReferenceError", "RuntimeError", "StopIteration", "StopAsyncIteration", "SyntaxError", "IndentationError", "TabError", "SystemError", "SystemExit", "TypeError", "UnboundLocalError", "UnicodeError", "UnicodeEncodeError", "UnicodeDecodeError", "UnicodeTranslateError", "ValueError", "ZeroDivisionError", "EnviromentError", "IOError", "WindowsError", "BlockingIOError", "ChildProcessError", "ConnectionError", "ConnectionAbortedError", "ConnectionRefusedError", "ConnectionResetError", "FileExistsError", "FileNotFoundError", "InterruptedError", "IsADirectoryError", "NotADirectoryError", "PermissionError", "ProcessLookupError", "TimeoutError", "Warning", "UserWarning", "DeprecationWarning", "PendingDeprecationWarning", "SyntaxWarning", "RuntimeWarning", "FutureWarning", "ImportWarning", "UnicodeWarning", "EncodingWarning", "BytesWarning", "ResourceWarning"]

        bold = ("Liberation Mono", 9, "bold")
        self.tag_configure("builtin", font=bold)
        self.tag_configure("number", font=bold)
        self.tag_configure("string", font=bold)
        self.tag_configure("keyword", font=bold)
        self.tag_configure("comment", foreground="Gray64")
        self.tag_configure("suggestion", foreground="Gray86")

        self.bind("<<Modified>>", self.highlight)
        self.bind("<Return>", self.indent)
        self.bind("<Control-o>", self.open)

        self.config(tabs=16)
        self.config(wrap="none")
        self.config(insertwidth=1)
        self.config(relief="flat")
        self.config(undo=True)
        self.config(font=("Liberation Mono", 9))

        self.path = None
    
    def highlight(self, e):

        for tag in self.tag_names():
            self.tag_remove(tag, 1.0, END)

        line = 1
        index = 0

        src = self.get(1.0, END)

        while len(src) > 0:
            if src[0] == "#":
                value = "#"
                src = src[1:]
                while (len(src) > 0) and (not src[0] == "\n"):
                    value += src[0]
                    src = src[1:]
                self.tag_add("comment", str(line) + "." + str(index), str(line) + "." + str(index + len(value)))
                index += len(value)
            elif src[0] == "\"":
                value = "\""
                src = src[1:]
                while (len(src) > 0) and (not src[0] == "\"") and (not src[0] == "\n"):
                    value += src[0]
                    src = src[1:]
                if src[0] == "\"":
                    value += "\""
                    src = src[1:]
                self.tag_add("string", str(line) + "." + str(index), str(line) + "." + str(index + len(value)))
                index += len(value)
            elif src[0] == "'":
                value = "'"
                src = src[1:]
                while (len(src) > 0) and (not src[0] == "'") and (not src[0] == "\n"):
                    value += src[0]
                    src = src[1:]
                if src[0] == "'":
                    value += "'"
                    src = src[1:]
                self.tag_add("string", str(line) + "." + str(index), str(line) + "." + str(index + len(value)))
                index += len(value)
            elif src[0] in " \t":
                src = src[1:]
                index += 1
            elif src[0] == "\n":
                line += 1
                index = 0
                src = src[1:]
            elif src[0].isalpha(): 
                value = ""
                while (len(src) > 0) and (src[0].isalpha() or src[0].isnumeric() or (src[0] == "_")):
                    value += src[0]
                    src = src[1:]
                if (value in self.builtins):
                    self.tag_add("builtin", str(line) + "." + str(index), str(line) + "." + str(index + len(value)))
                elif (value in self.keywords):
                    self.tag_add("keyword", str(line) + "." + str(index), str(line) + "." + str(index + len(value)))
                elif (value == "self"):
                    self.tag_add("keyword", str(line) + "." + str(index), str(line) + "." + str(index + len(value)))
                index += len(value)
            elif src[0].isnumeric(): 
                value = ""
                while (len(src) > 0) and (src[0].isnumeric()):
                    value += src[0]
                    src = src[1:]
                self.tag_add("number", str(line) + "." + str(index), str(line) + "." + str(index + len(value)))
                index += len(value)
            else:
                src = src[1:]
                index += 1

        self.edit_modified(0)

    def indent(self, _):

        line = self.get("insert linestart", "insert")

        match = re.match(r'(\s+)', line)
        whitespace = match.group(0) if match else ""
        if line.endswith(":",):
            whitespace += "\t"
        self.insert("insert", f"\n{whitespace}")

        return "break"
    def open(self, _):
        home = os.environ['HOME']
        file = filedialog.askopenfile(title="Load a File", initialdir=home)
        self.path = file.name
        self.delete(1.0, END)
        self.insert(1.0, file.read())
        file.close()

root = Tk()
root.geometry("750x500")
root.title("__pynit__")

editor = Editor()
editor.pack(fill="both", expand=True)
root.mainloop()
