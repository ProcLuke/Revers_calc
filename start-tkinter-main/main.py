#!/usr/bin/env python3

from os.path import basename, splitext
import tkinter as tk
from oper import operation1, operation2

# from tkinter import ttk


class MyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        if not "textvariable" in kw:
            self.variable = tk.StringVar()
            self.config(textvariable=self.variable)
        else:
            self.variable = kw["textvariable"]

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, new: str):
        self.variable.set(new)


class MyListbox(tk.Listbox):
    def pop(self):
        if self.size() > 0:
            x = self.get("end")
            self.delete("end")
            return x
        else:
            raise IndexError


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
        self.lbl = tk.Label(self, text="Polish cow")
        self.btn = tk.Button(self, text="Destroy", command=self.destroy)
        self.entry = MyEntry(master=self)
        self.entry.bind("<Return>", self.enterHandler)
        self.entry.bind("<KP_Enter>", self.enterHandler)

        self.lbl.pack()
        self.listbox.pack()
        self.entry.pack()
        self.btn.pack()

        self.entry.focus()

    def enterHandler(self, event):
        for token in self.entry.value.split():
            try :
                self.listbox.insert("end", float(token))
            except ValueError:
                self.tokenProcess(token)
        self.entry.value = ""
        self.listbox.see("end")

        x = self.listbox.get("end")

    def tokenProcess(self, token):
        if token in operation2:
            b = self.listbox.get("end")
            self.listbox.delete("end")
            a = self.listbox.get("end")
            self.listbox.delete("end")
            r = operation2[token](a,b)
            self.listbox.insert("end", r)

        if token in operation1:
            a = self.listbox.get("end")
            self.listbox.delete("end")
            r = operation1[token](a)
            self.listbox.insert("end", r)

        match token:
            case "sw" | "switch" if self.listbox.size() >= 2:
                b = self.listbox.get("end")
                self.listbox.delete("end")
                a = self.listbox.get("end")
                self.listbox.delete("end")
                self.listbox.insert("end", b)
                self.listbox.insert("end", a)
            case "D" | "del " if self.listbox.size() >= 1:
                self.listbox.delete("end")

    def destroy(self, event=None):
        super().destroy()


app = Application()
app.mainloop()
