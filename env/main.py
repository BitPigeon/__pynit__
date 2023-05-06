#!/usr/bin/env python

from tkinter import END, Tk, filedialog
from tkinter.scrolledtext import ScrolledText
from threading import Thread
import subprocess
import re
import os
import sys

class Input:
    pass

def write(string):
    output.config(state="normal")
    output.insert(END, string)
    output.config(state="disabled")

def err(string):
    output.config(state="normal")
    output.insert(END, string, "err")
    output.config(state="disabled")

class Editor(ScrolledText):

    "The editor for the pynit gui."
    
    def __init__(self):

        "Initialize the editor."
        
        super().__init__()

        # Define the keywords and builtins for highlighting.
        self.keywords = ["False", "True", "NotImplemented", "as", "and", "or", "not", "break", "continue", "class", "def", "if", "elif", "else", "for", "while", "in", "is", "None", "lambda", "return", "yield", "async" "nonlocal", "global", "import", "from", "raise", "pass", "with", "finally", "try", "except", "or", "and", "elif", "await", "assert"]
        self.builtins = ["quit", "abs", "aiter", "all", "any", "anext", "ascii", "bin", "bool", "breakpoint", "bytearray", "bytes", "callable", "chr", "classmethod", "compile", "complex", "delattr", "dict", "dir", "divmod", "enumerate", "eval", "exec", "filter", "float", "format", "frozenset", "getattr", "globals", "hasattr", "hash", "help", "hex", "id", "input", "int", "isinstance", "issubclass", "iter", "len", "list", "locals", "map", "max", "memoryview", "min", "next", "object", "oct", "open", "ord", "pow", "print", "property", "range", "repr", "reversed", "round", "set", "setattr", "slice", "sorted", "staticmethod", "str", "sum", "super", "tuple", "type", "vars", "zip", "BaseException", "Exception", "ArithmeticError", "BufferError", "LookupError", "AssertionError", "AtributeError", "EOFError", "FloatingPointError", "GeneratorExit", "ImportError", "ModuleNotFoundError", "IndexError", "KeyError", "KeyboardInterrupt", "MemoryError", "NameError", "NotImplementedError", "OSError", "OverflowError", "RecursionError", "ReferenceError", "RuntimeError", "StopIteration", "StopAsyncIteration", "SyntaxError", "IndentationError", "TabError", "SystemError", "SystemExit", "TypeError", "UnboundLocalError", "UnicodeError", "UnicodeEncodeError", "UnicodeDecodeError", "UnicodeTranslateError", "ValueError", "ZeroDivisionError", "EnviromentError", "IOError", "WindowsError", "BlockingIOError", "ChildProcessError", "ConnectionError", "ConnectionAbortedError", "ConnectionRefusedError", "ConnectionResetError", "FileExistsError", "FileNotFoundError", "InterruptedError", "IsADirectoryError", "NotADirectoryError", "PermissionError", "ProcessLookupError", "TimeoutError", "Warning", "UserWarning", "DeprecationWarning", "PendingDeprecationWarning", "SyntaxWarning", "RuntimeWarning", "FutureWarning", "ImportWarning", "UnicodeWarning", "EncodingWarning", "BytesWarning", "ResourceWarning"]

        # Define the bold font for the highlighting.
        bold = ("Liberation Mono", 9, "bold")

        # Add the tags for highlighting.
        self.tag_configure("builtin", font=bold)
        self.tag_configure("number", font=bold)
        self.tag_configure("string", font=bold)
        self.tag_configure("keyword", font=bold)
        self.tag_configure("comment", foreground="Gray64")
        self.tag_configure("suggestion", foreground="Gray86")

        # Bind events to make it work properly.
        self.bind("<<Modified>>", self.highlight)
        self.bind("<Return>", self.indent)
        self.bind("<F5>", self.thread_run)
        self.bind("<Control-o>", self.open)
        self.bind("<Control-s>", self.save)
        self.bind("<Control-l>", self.thread_lint)
        self.bind("<Control-n>", self.new)

        # Configure visual options for the editor
        self.config(tabs=16)
        self.config(wrap="none")
        self.config(insertwidth=1)
        self.config(relief="flat")
        self.config(undo=True)
        self.config(font=("Liberation Mono", 9))

        # Define variables
        self.path = None
        self.saved = True

    def highlight(self, e):

        "Highlight all the code."

        # Remove all tags in the editor.
        for tag in self.tag_names():
            self.tag_remove(tag, 1.0, END)

        # Set the variables that define the location in the string.
        line = 1
        index = 0

        # Get the source code.
        src = self.get(1.0, END)

        # Loop through the code.
        while len(src) > 0:

            # Define comment.
            if src[0] == "#":

                # Set the value to the starting pound sign and remove it from the code.
                value = "#"
                src = src[1:]

                # Highlight until newline or the end of the code.
                while (len(src) > 0) and (not src[0] == "\n"):

                    # Add the current character to the value and remove it from the code.
                    value += src[0]
                    src = src[1:]

                # Add the tag comment to the line.
                self.tag_add("comment", str(line) + "." + str(index), str(line) + "." + str(index + len(value)))

                # Change the column by the length of the comment.
                index += len(value)

            # Define double-quoted string
            elif src[0] == "\"":

                # Set the value to the starting double-quote sign and remove it from the code.
                value = "\""
                src = src[1:]

                # Highlight until closing double-quote or newline or the end of the code.
                while (len(src) > 0) and (not src[0] == "\"") and (not src[0] == "\n"):
                    
                    # Add the current character to the value and remove it from the code.
                    value += src[0]
                    src = src[1:]

                # If there is a closing double-quote, add it to the value and remove it from the code.
                if src[0] == "\"":
                    value += "\""
                    src = src[1:]

                # Add the tag string to the value.
                self.tag_add("string", str(line) + "." + str(index), str(line) + "." + str(index + len(value)))

                # Change the column by the length of the string.
                index += len(value)

            # Define single-quoted string.
            elif src[0] == "'":

                # Set the value to the starting single-quote sign and remove it from the code.
                value = "'"
                src = src[1:]

                # Highlight until the closing single-quote sign or newline or the end of the code.
                while (len(src) > 0) and (not src[0] == "'") and (not src[0] == "\n"):

                    # Add the current character to the value and remove it from the code.
                    value += src[0]
                    src = src[1:]

                # If there is a closing single-quote, add it to the value and remove it from the code.
                if src[0] == "'":
                    value += "'"
                    src = src[1:]

                # Add the tag string to the value.
                self.tag_add("string", str(line) + "." + str(index), str(line) + "." + str(index + len(value)))

                # Change the column by the length of the string.
                index += len(value)

            # Define ignored values.
            elif src[0] in " \t":

                # Skip over the value.
                src = src[1:]
                index += 1

            # Define newline.
            elif src[0] == "\n":

                # Change the row and reset the column
                line += 1
                index = 0

                # Skip over the character.
                src = src[1:]

            # Define keywords, identifiers and builtins.
            elif src[0].isalpha():

                # Reset the value.
                value = ""

                # Highlight until the end of the code or until a character that is not alpha, numeric or underslash
                while (len(src) > 0) and (src[0].isalpha() or src[0].isnumeric() or (src[0] == "_")):

                    # Add the current character to the value and remove it from the code.
                    value += src[0]
                    src = src[1:]

                # Check if value is a builtin.
                if (value in self.builtins):

                    # Add the tag builtin to the value.
                    self.tag_add("builtin", str(line) + "." + str(index), str(line) + "." + str(index + len(value)))

                # Check if value is a keyword.
                elif (value in self.keywords):

                    # Add the tag keyword to the value.
                    self.tag_add("keyword", str(line) + "." + str(index), str(line) + "." + str(index + len(value)))

                # Check if the value is a self keyword.
                elif (value == "self"):

                    # Add the tag keyword to the value.
                    self.tag_add("keyword", str(line) + "." + str(index), str(line) + "." + str(index + len(value)))

                # Change the column by the length of the keyword/builtin/identifier
                index += len(value)

            # Define numeric values.
            elif src[0].isnumeric():

                # Reset the value.
                value = ""

                # Highlight until the value is not numeric or the end of the code.
                while (len(src) > 0) and (src[0].isnumeric()):

                    # Add the current character to the value and remove it from the code.
                    value += src[0]
                    src = src[1:]

                # Add the tag number to the value.
                self.tag_add("number", str(line) + "." + str(index), str(line) + "." + str(index + len(value)))

                # Change column by the length of the number.
                index += len(value)

            # Define not recognized.
            else:
                # Skip over the value.
                src = src[1:]
                index += 1

        # Set self.edit_modified to allow the <<Modified>> event to trigger agian.
        self.edit_modified(0)

        # Set the code to not saved.
        self.saved = False

    def thread_run(self, _):

        "Thread the run function for better performance."

        # Create a new thread for the run function and start it.
        Thread(target=self.run).start()

    def run(self):

        "Run all of the code."

        # Save the code if it is not saved.
        if (not self.path) or (not self.saved):
            self.save(0)

        # Set output state to normal, so we can insert the header.
        output.config(state="normal")

        # Insert the header and a newline.
        output.insert(END, f"RUN - {self.path.upper()}", "header")
        output.insert(END, "\n")

        # Set output state to disabled, so the user cannot edit the output.
        output.config(state="disabled")

        # Run the code using the python3 command.
        run = subprocess.Popen(["python3", self.path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

        # Loop through the output.
        while True:

            # Define stdout, sterr and stdin.
            stdout = run.stdout.readline().decode()
            stderr = run.stderr.readline().decode()

            # If there is no output, break the loop.
            if (not stdout) and (not stderr):
                break

            # If the output is output, write it normally.
            if stdout:
                write(stdout)
            # If the output is an error, write it with red text.
            elif stderr:
                err(stderr)

    def thread_lint(self, _):

        "Thread the lint function for better performance."

        # Create a new thread for the lint function and start it.
        Thread(target=self.lint).start()

    def lint(self):

        "Lint the code with pylint."

        # Save the code if it is not saved.
        if (not self.path) or (not self.saved):
            self.save(0)

        # Lint the code using the pylint commmand.
        file = os.popen("pylint " + self.path)

        # Set the output state to normal, so we can insert the header.
        output.config(state="normal")

        # Insert the header and a newline.
        output.insert(END, f"LINT - {self.path.upper()}", "header")
        output.insert(END, "\n")

        # Set output state to disabled, so the user cannot edit the output.
        output.config(state="disabled")

        # Get the results of the lint.
        lint = file.read()

        # Set the output state to normal, so we can insert the results.
        output.config(state="normal")

        # Insert the results.
        output.insert(END, lint)

        # Set output state to disabled, so the user cannot edit the output.
        output.config(state="disabled")

        # Close the output file.
        file.close()

    def save(self, _):

        "Save the code."

        # Get the home enviroment.
        home = os.environ['HOME']

        # If this file has been saved before, open the path the user specified.
        if self.path:
            file = open(self.path, "w")

        # If this file has not been saved before, prompt the user for a path until a result.
        else:
            while not self.path:
                file = filedialog.asksaveasfile(title="Save Your File", initialdir=home)
                self.path = file.name

        # Write the contents of the editor into the file.
        file.write(self.get(1.0, END))

        # Close the file.
        file.close()

        # Set the output state to normal, so we can insert the header.
        output.config(state="normal")

        # Insert the header and a newline.
        output.insert(END, f"SAVE - {self.path.upper()}", "header")
        output.insert(END, "\n")

        # Set output state to disabled, so the user cannot edit the output.
        output.config(state="disabled")

        # Set the saved variabe to True.
        self.saved = True

    def new(self, _):

        "Create a new file."

        # If the old file is not saved, save it.
        if not self.saved:
            self.save(0)

        # Clear the editor.
        self.delete(1.0, END)

        # Undefine the path.
        self.path = None

        # Set the output state to normal, so we can insert the header.
        output.config(state="normal")

        # Insert the header and a newline.
        output.insert(END, "CREATE NEW FILE", "header")
        output.insert(END, "\n")

        # Set output state to disabled, so the user cannot edit the output.
        output.config(state="disabled")

        # Set the saved variable to False.
        self.saved = False

    def indent(self, _):

        "Auto indent."

        # Get the cursor's line.
        line = self.get("insert linestart", "insert")

        # Match the whitespace at the start of the line.
        match = re.match(r'(\s+)', line)

        # Get the whitespace as a string.
        whitespace = match.group(0) if match else ""

        # If the line ends with a colon, indent the next line.
        if line.endswith(":",):
            whitespace += "\t"

        # Insert the whitespace into the next line.
        self.insert("insert", f"\n{whitespace}")

        # Return "break" to not allow tkinter to do it's default action.
        return "break"

    def open(self, _):

        "Open a new file."

        # Get the home enviroment.
        home = os.environ['HOME']

        # Ask for the new file until it gets results.
        while not self.path:
            file = filedialog.askopenfile(title="Load a File", initialdir=home)
            self.path = file.name

        # Delete the contents of the editor.
        self.delete(1.0, END)

        # Insert the contents of the file into the editor.
        self.insert(1.0, file.read())

        # Close the file.
        file.close()

        # Set the output state to normal, so we can insert the header.
        output.config(state="normal")

        # Insert the header and a newline.
        output.insert(END, f"OPEN - {self.path.upper()}", "header")
        output.insert(END, "\n")

        # Set output state to disabled, so the user cannot edit the output.
        output.config(state="disabled")

        # Set the saved variable to True.
        self.saved = True

class Out(ScrolledText):

    "The output console."
    
    def __init__(self):

        "Intialize the console."
        
        super().__init__()

        # Configure the console's visual options.
        self.config(state="disabled")
        self.config(tabs=16)
        self.config(relief="flat")
        self.config(font=("Liberation Mono", 7))

        # Add tags to the console.
        self.tag_configure("header", justify="center", font=("Liberation Mono", 8, "bold"))
        self.tag_configure("err", foreground="red")

        # Bind clear function to backspace key.
        self.bind("<BackSpace>", self.clear)

    def clear(self, _):

        "Clear the console."

        # Set the output state to normal, so we can clear the console.
        self.config(state="normal")

        # Delete all text in the console.
        self.delete(1.0, END)

        # Set output state to disabled, so the user cannot edit the output.
        self.config(state="disabled")

# Make the root window.
root = Tk()

# Set the window's visual options.
root.geometry("750x500")
root.title("__pynit__")

# Make a new editor instance.
editor = Editor()

# Make a new output instance.
output = Out()

# Show the editor and the console.
editor.pack(fill="both", expand=True)
output.pack(fill="both", expand=True)

# Set the window into mainloop.
root.mainloop()

