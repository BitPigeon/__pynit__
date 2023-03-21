from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
import re
import sys
import types
import os
import pyclbr

EDITOR_COMMENT_COLOR = "LightSteelBlue3"
EDITOR_STRING_COLOR = "SteelBlue2"
EDITOR_NUMBER_COLOR = "SteelBlue"
EDITOR_KWRDS_COLOR = "CadetBlue3"
EDITOR_MODULE_CALL_COLOR = "CadetBlue4"
EDITOR_MODULE_FUNCTION_CLASS_COLOR = "SteelBlue4"

class Editor(ScrolledText):
    def __init__(self):
        super().__init__()
        self.keywords = ["from", "if", "while", "import", "as", "with", "def", "class", "and", "or", "not", "await", "pass", "True", "False", "None", "break", "except", "in", "raise", "finally", "is", "return", "yield", "continue", "for", "lambda", "try", "nonlocal", "global", "assert", "del", "async", "elif", "or", "else"]
        self.tag_configure("str", foreground=EDITOR_STRING_COLOR)
        self.tag_configure("number", foreground=EDITOR_NUMBER_COLOR)
        self.tag_configure("comment", foreground=EDITOR_COMMENT_COLOR)
        self.tag_configure("keyword", foreground=EDITOR_KWRDS_COLOR)
        self.tag_configure("module", foreground=EDITOR_MODULE_CALL_COLOR)
        self.tag_configure("module_function", foreground=EDITOR_MODULE_FUNCTION_CLASS_COLOR)
        
    def highlight(self, e=None):
        for tag in self.tag_names():
            self.tag_remove(tag, "1.0", "end")
        self.find("[\d\.]+", "number")
        self.find("\".*\"|\".*\"", "str")
        self.find("#.*", "comment")
        self.find("True|False", "boolean")
        for keyword in self.keywords:
            self.find(fr"\b{keyword}\b", "keyword")
        self.highlight_imports()
        
    def find(self, regexp, tag):
        numbers = re.findall(regexp, self.get(1.0, END))
        startidx = "1.0"
        if numbers:
            for number in numbers:
                start = self.search(number, index=startidx, stopindex=END)
                if not number.endswith(".") and not number.endswith("("):
                    end = '%s+%dc' % (start, len(number))
                else:
                    end = '%s+%dc' % (start, len(number) - 1)
                startidx = end
                self.tag_add(tag, start, end)
    
    def save(self, e="close"):
        with open("untitled.py", "w", encoding="utf-8") as file:
            file.write(self.get(1.0, END))
        if e == "close":
            root.destroy()

    def run(self, e=None):
        print("running")

    def highlight_imports(self):
        imports = re.findall("import\s+[^\s]+\n", self.get(1.0, END))
        import_froms = re.findall("from\s+.+\s+import\s+.+\n", self.get(1.0, END))
        import_asses = re.findall("import\s+.+\s+as\s+.+\n", self.get(1.0, END))
        for _import in imports:
            for module in re.sub("import\s+", "", _import).strip().split(","):
                self.find("[^\w]" + module.strip() + "[^\w]", "module")
        for import_from in import_froms:
            for func in re.sub("from\s+.+\s+import\s+", "", import_from).strip().split(","):
                self.find("[^\w]" + func.strip() + "[^\w]", "module_function")
        for import_as in import_asses:
            for module in re.sub("import\s+", "", import_as).split(","):
                self.find("[^\w]" + re.sub(".+\s+as\s+", "", module).strip() + "[^\w]", "module")
                sub = re.sub('.+\s+as\s+', '', module).strip()
            
        
root = Tk()
root.geometry("700x550")
root.title("untitled - pynit")
editor = Editor()
editor.pack(fill="both", expand=True)
editor.bind("<KeyPress>", editor.highlight)
editor.bind("<KeyRelease>", editor.highlight)
root.bind("<Control-s>", editor.save)
root.bind("<F5>", editor.run)
root.protocol("WM_DELETE_WINDOW", editor.save)
root.mainloop()
