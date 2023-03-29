from tkinter.scrolledtext import ScrolledText
from tkinter import *
import re

class Editor(ScrolledText):
    
    def __init__(self):
        super().__init__()
        self.highlighter_dict = {"keyword": "SteelBlue1", "number": "SlateGray4", "string": "OliveDrab4", "definition": "", "comment": "SlateGray1", "selection": "", "builtin": "SteelBlue2", "builtinerror": "SteelBlue4", "builtinwarning": "SteelBlue3"}
        self.keywords = ["False", "True", "NotImplemented","and", "or", "not", "break", "continue", "class", "def", "if", "elif", "else", "for", "while", "in", "is", "None", "lambda", "return", "yield", "async" "nonlocal", "global", "import", "from", "raise", "pass", "with", "finally", "try", "except", "or", "and", "elif", "await", "assert"]
        self.builtins = ["quit", "abs", "aiter", "all", "any", "anext", "ascii", "bin", "bool", "breakpoint", "bytearray", "bytes", "callable", "chr", "classmethod", "compile", "complex", "delattr", "dict", "dir", "divmod", "enumerate", "eval", "exec", "filter", "float", "format", "frozenset", "getattr", "globals", "hasattr", "hash", "help", "hex", "id", "input", "int", "isinstance", "issubclass", "iter", "len", "list", "locals", "map", "max", "memoryview", "min", "next", "object", "oct", "open", "ord", "pow", "print", "property", "range", "repr", "reversed", "round", "set", "setattr", "slice", "sorted", "staticmethod", "str", "sum", "super", "tuple", "type", "vars", "zip"]
        self.errors = ["BaseException", "Exception", "ArithmeticError", "BufferError", "LookupError", "AssertionError", "AtributeError", "EOFError", "FloatingPointError", "GeneratorExit", "ImportError", "ModuleNotFoundError", "IndexError", "KeyError", "KeyboardInterrupt", "MemoryError", "NameError", "NotImplementedError", "OSError", "OverflowError", "RecursionError", "ReferenceError", "RuntimeError", "StopIteration", "StopAsyncIteration", "SyntaxError", "IndentationError", "TabError", "SystemError", "SystemExit", "TypeError", "UnboundLocalError", "UnicodeError", "UnicodeEncodeError", "UnicodeDecodeError", "UnicodeTranslateError", "ValueError", "ZeroDivisionError", "EnviromentError", "IOError", "WindowsError", "BlockingIOError", "ChildProcessError", "ConnectionError", "ConnectionAbortedError", "ConnectionRefusedError", "ConnectionResetError", "FileExistsError", "FileNotFoundError", "InterruptedError", "IsADirectoryError", "NotADirectoryError", "PermissionError", "ProcessLookupError", "TimeoutError"]
        self.warnings = ["Warning", "UserWarning", "DeprecationWarning", "PendingDeprecationWarning", "SyntaxWarning", "RuntimeWarning", "FutureWarning", "ImportWarning", "UnicodeWarning", "EncodingWarning", "BytesWarning", "ResourceWarning"]
        self.strings = ["'[^']*'", "\"[^\"]*\""]
        self.comments = ["#.*"]
        self.digits = ["\d+"]
        
        for tag in self.highlighter_dict:
            self.tag_configure(tag, foreground=self.highlighter_dict[tag])
        self.bind("<KeyRelease>", self.highlight)
    
    def highlight(self, e):
        for tag in self.tag_names():
            self.tag_remove(tag, 1.0, END)
        self.focus = [1, 0]
        lines = self.get(1.0, END).split("\n")
        for line in lines:
            words = line.split(" ")
            for word in words:
                self.focus_start = [str(self.focus[0]), str(self.focus[1])]
                self.focus_end = [str(self.focus[0]), str(self.focus[1] + len(word))]
                if self.check(self.comments, word):
                    self.tag_add("comment", ".".join(self.focus_start), ".".join(self.focus_end))
                else:
                    if self.check(self.strings, word):
                        self.tag_add("string", ".".join(self.focus_start), ".".join(self.focus_end))
                    else:
                        if self.check(self.keywords, word):
                            self.tag_add("keyword", ".".join(self.focus_start), ".".join(self.focus_end))
                        else:
                            if self.check(self.builtins, word):
                                self.tag_add("builtin", ".".join(self.focus_start), ".".join(self.focus_end))
                            else:
                                if self.check(self.errors, word):
                                    self.tag_add("builtinerror", ".".join(self.focus_start), ".".join(self.focus_end))
                                else:
                                    if self.check(self.warnings, word):
                                        self.tag_add("builtinwarning", ".".join(self.focus_start), ".".join(self.focus_end))
                                    else:
                                        if self.check(self.digits, word):
                                            self.tag_add("number", ".".join(self.focus_start), ".".join(self.focus_end))
                self.focus[1] += int(len(word) + 1)
            self.focus[0] += 1
            self.focus[1] = 0

    def check(self, _list, value):
        for item in _list:
             if re.match(item, value):
                return True
                        
                
                
                
            
