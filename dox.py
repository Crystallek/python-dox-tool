import ttkthemes
import webbrowser
from tkinter import*
from tkinter import ttk

entriesLabels = []
addedEntries = []
#scrollbar moment

def findindex(index, array, sub):
    counter = 0
    while counter <= index:
        if sub == array[counter]: 
            return counter
        else: 
            counter += 1

def popup(text, do):
    global top
    top = Toplevel(app)
    top.geometry("200x90")
    top.resizable(False, False)

    label = ttk.Label(top, text=text)
    name = ttk.Entry(top)

    if do == "add":
        top.title("Add")
        btn = ttk.Button(top, text="Add", command=lambda: add(name.get()))
    if do == "remove":
        top.title("Remove")
        btn = ttk.Button(top, text="Remove", command=lambda: remove(name.get()))

    label.pack(padx=10, pady=2)
    name.pack(padx=10, pady=2)
    btn.pack(padx=10, pady=2)

def add(text):
    global top
    top.destroy()

    if text in entriesLabels:
        return

    entry = ttk.Entry(app, width=1000)
    entry_label = ttk.Label(app, text=text)
    
    entry_label.pack(padx=10, pady=10)
    entry.pack(padx=10, pady=0)

    addedEntries.append([entry, entry_label])

def remove(text):
    global top
    global addedEntries
    
    top.destroy()

    index = findindex(len(entriesLabels) - 1, entriesLabels, text)

    for shit in addedEntries[index]:
        shit.pack_forget()
    addedEntries.pop(index)
    entriesLabels.pop(index)

def save():
    for entries in addedEntries:
        print(entries[1].cget("text"), entries[0].get())

app = ttkthemes.ThemedTk(theme="arc")
app.geometry("500x500")

menubar = Menu(app)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Add", command=lambda: popup("Add", "add"))
filemenu.add_command(label="Remove", command=lambda: popup("Remove", "remove"))
filemenu.add_command(label="Save", command=lambda: save())
filemenu.add_separator()
filemenu.add_command(label="Exit", command=lambda: exit())
menubar.add_cascade(label="Main", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="GitHub", command=lambda: webbrowser.open_new("https://github.com/Crystallek/dox-app"))
#helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

app.config(menu=menubar)

entry1_text = ttk.Label(app, text="DOX NAME")
entry1 = ttk.Entry(app, width=1000)
entry1_text.pack(padx=10, pady=10)
entry1.pack(padx=10, pady=0)

app.mainloop()
