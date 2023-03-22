from tkinter.scrolledtext import ScrolledText
from tkinter import *

class Editor(ScrolledText):
    
    def __init__(self):
        super().__init__()
        self.highlighter_dict = {"keyword": "SteelBlue1", "number": "", "string": "", "definition": "", "comment": "", "selection": "", "builtin": "SteelBlue3", "builtinerror": "SteelBlue2"}
        self.keywords = ["False", "True", "NotImplemented","and", "or", "not", "break", "continue", "class", "def", "if", "elif", "else", "for", "while", "in", "is", "None", "lambda", "return", "yield", "async" "nonlocal", "global", "import", "from", "raise", "pass", "with", "finally", "try", "except", "or", "and", "elif", "await", "assert"]
        self.builtins = ["quit", "abs", "aiter", "all", "any", "anext", "ascii", "bin", "bool", "breakpoint", "bytearray", "bytes", "callable", "chr", "classmethod", "compile", "complex", "delattr", "dict", "dir", "divmod", "enumerate", "eval", "exec", "filter", "float", "format", "frozenset", "getattr", "globals", "hasattr", "hash", "help", "hex", "id", "input", "int", "isinstance", "issubclass", "iter", "len", "list", "locals", "map", "max", "memoryview", "min", "next", "object", "oct", "open", "ord", "pow", "print", "property", "range", "repr", "reversed", "round", "set", "setattr", "slice", "sorted", "staticmethod", "str", "sum", "super", "tuple", "type", "vars", "zip"]
        self.errors = ["BaseException", "Exception", "ArithmeticError", "BufferError", "LookupError", "AssertionError", "AtributeError", "EOFError", "FloatingPointError", "GeneratorExit", "ImportError", "ModuleNotFoundError", "IndexError", "KeyError", "KeyboardInterrupt", "MemoryError", "NameError", "NotImplementedError", "OSError", "OverflowError", "RecursionError", "ReferenceError", "RuntimeError", "StopIteration", "StopAsyncIteration", "SyntaxError", "IndentationError", "TabError", "SystemError", "SystemExit", "TypeError", "UnboundLocalError", "UnicodeError", "UnicodeEncodeError", "UnicodeDecodeError", "UnicodeTranslateError", "ValueError", "ZeroDivisionError", "EnviromentError", "IOError", "WindowsError", "BlockingIOError", "ChildProcessError", "ConnectionError", "ConnectionAbortedError", "ConnectionRefusedError", "ConnectionResetError", "FileExistsError", "FileNotFoundError", "InterruptedError", "IsADirectoryError"]
        
        for tag in self.highlighter_dict:
            self.tag_configure(tag, foreground=self.highlighter_dict[tag])
        self.bind("<KeyRelease>", self.highlight)

    def highlight(self, e):
        for tag in self.tag_names():
            self.tag_remove(tag, "1.0", "end")
        length = IntVar()
        for keyword in self.keywords:
            keyword = "([^A-Za-z0-9_-]|\s)?" + keyword + "[\s:.,\n]"
            start = 1.0
            while start:
                start = self.search(keyword, start, stopindex=END, count=length, regexp=1)
                if start:
                    end = str(start).split(".")[0] + "." + str(int(str(start).split(".")[1]) + length.get())
                    highlighted = self.get(start, end)
                    if highlighted[-1:] != keyword[-1:]:
                        end = str(start).split(".")[0] + "." + str(int(str(start).split(".")[1]) + length.get() - 1)
                    self.tag_add("keyword", start, end)
                    start = end
        for builtin in self.builtins:
            builtin = "([^A-Za-z0-9_-]|\s)?" + builtin + "[\s:.,\n()]"
            start = 1.0
            while start:
                start = self.search(builtin, start, stopindex=END, count=length, regexp=1)
                if start:
                    end = str(start).split(".")[0] + "." + str(int(str(start).split(".")[1]) + length.get())
                    highlighted = self.get(start, end)
                    if highlighted[-1:] != builtin[-1:]:
                        end = str(start).split(".")[0] + "." + str(int(str(start).split(".")[1]) + length.get() - 1)
                    self.tag_add("builtin", start, end)
                    start = end
        for error in self.errors:
            error = "([^A-Za-z0-9_-]|\s)?" + error + "[\s:.,\n()]"
            start = 1.0
            while start:
                start = self.search(error, start, stopindex=END, count=length, regexp=1)
                if start:
                    end = str(start).split(".")[0] + "." + str(int(str(start).split(".")[1]) + length.get())
                    highlighted = self.get(start, end)
                    if highlighted[-1:] != error[-1:]:
                        end = str(start).split(".")[0] + "." + str(int(str(start).split(".")[1]) + length.get() - 1)
                    self.tag_add("builtinerror", start, end)
                    start = end
