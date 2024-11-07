#!/usr/bin/env python3

from os.path import basename, splitext
import tkinter as tk
from oper import operation1, operation2



class MyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        if not "textvariable" in kw:
            self.variable = tk.StringVar()
            self.config(textvariable=self.variable)
        else:
            self.variable = kw["textvariable"]
        
        self.history = []
        self.history_index = -1

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, new: str):
        self.variable.set(new)
    
    def add_to_history(self, text):
        self.history.append(text)
        self.history_index = len(self.history)

    def get_previous_history(self):
        if self.history and self.history_index > 0:
            self.history_index -= 1
            self.value = self.history[self.history_index]

    def get_next_history(self):
        if self.history and self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.value = self.history[self.history_index]
        elif self.history_index == len(self.history) - 1:
            self.value = ""
            self.history_index += 1


class MyListbox(tk.Listbox):
    def pop(self):
        if self.size() > 0:
            x = self.get("end")
            self.delete("end")
            return x
        else:
            raise IndexError("Zásobník je prázdný")

class Application(tk.Tk):
    name = basename(splitext(basename(__file__.capitalize()))[0])
    name = "Foo"
    font_setting = ("Verdana", 12)

    def __init__(self):
        super().__init__(className=self.name)
        self.option_add("*Font", self.font_setting)
        self.title(self.name)
        self.bind("<Escape>", self.destroy)

        self.listbox = MyListbox(master=self)
        self.lbl = tk.Label(self, text="Calc")
        self.btn = tk.Button(self, text="Destroy", command=self.destroy)
        self.entry = MyEntry(master=self)
        self.entry.bind("<Return>", self.enterHandler)
        self.entry.bind("<KP_Enter>", self.enterHandler)
        self.entry.bind("<Up>", lambda e: self.entry.get_previous_history())
        self.entry.bind("<Down>", lambda e: self.entry.get_next_history())

        self.status_bar = tk.Label(self, text="", relief=tk.SUNKEN, anchor="w")

        self.lbl.pack()
        self.listbox.pack()
        self.entry.pack()
        self.btn.pack()
        self.status_bar.pack(fill=tk.X)
        
        self.entry.focus()
        
    def enterHandler(self, event):
        entry_value = self.entry.value.strip()
        if entry_value:
            self.entry.add_to_history(entry_value)
            self.process_tokens(entry_value)
            self.entry.value = ""

    def process_tokens(self, text):
        tokens = text.split()
        for token in tokens:
            try:
                self.listbox.insert("end", float(token))
            except ValueError:
                try:
                    self.tokenProcess(token)
                except Exception as e:
                    self.update_status(str(e))
        self.listbox.see("end")

    def tokenProcess(self, token):
        if token in operation2:
            try:
                b = float(self.listbox.pop())
                a = float(self.listbox.pop())
                if token == '/' and b == 0:
                    raise ZeroDivisionError("Dělení nulou")
                result = operation2[token](a, b)
                self.listbox.insert("end", result)
            except IndexError:
                self.update_status("Nedostatek čísel v zásobníku")
            except ZeroDivisionError:
                self.update_status("Dělení nulou")

        elif token in operation1:
            try:
                a = float(self.listbox.pop())
                result = operation1[token](a)
                self.listbox.insert("end", result)
            except IndexError:
                self.update_status("Nedostatek čísel v zásobníku")

        match token:
            case "sw" | "switch" if self.listbox.size() >= 2:
                b = self.listbox.pop()
                a = self.listbox.pop()
                self.listbox.insert("end", b)
                self.listbox.insert("end", a)
            case "D" | "del" if self.listbox.size() >= 1:
                self.listbox.pop()

    def update_status(self, message):
        self.status_bar.config(text=message)

    def destroy(self, event=None):
        super().destroy()


app = Application()
app.mainloop()
