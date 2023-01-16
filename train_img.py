import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

window = tk.Tk()
window.title("Signature Verification System")
greeting = tk.Label(
    text="Add images to import")
greeting.pack()
window.geometry("600x500")


def sel_train():
    def directory0():
        root = tk.Tk()
        root.withdraw()
        dirname0 = filedialog.askdirectory(
            parent=root, initialdir="/", title='Please select a directory for class 0.')
        return dirname0

    def directory1():
        root = tk.Tk()
        root.withdraw()
        dirname1 = filedialog.askdirectory(
            parent=root, initialdir="/", title='Please select a directory for class 1.')
        return dirname1

    dir0 = directory0()
    dir1 = directory1()
    print(dir0)
    print(dir1)

    def myButton1():
        win = Tk()
        win.title("Import images")
        win.geometry("400x400")

        label1 = Label(win, text="Enter name/unique id")
        label1.pack()

        entry = Entry(win, width=40)
        entry.focus_set()
        entry.pack()

        btn1 = ttk.Button(win, text="Enter", width=20)
        btn1.pack(pady=0)

        label2 = Label(win, text="Import images")
        label2.pack(pady=0)

        ttk.Button(win, text="Class 0", width=20,
                   command=directory0).pack(pady=0)
        ttk.Button(win, text="Class 1", width=20,
                   command=directory1).pack(pady=0)
        win.mainloop()

    button1 = tk.Button(
        text="Add images",
        width=15,
        height=2,
        bg="red",
        fg="yellow",
        command=myButton1
    )

    button1.pack(padx=0, pady=5)
    window.mainloop()
