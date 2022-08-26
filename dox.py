from ip2geotools.databases.noncommercial import DbIpCity
import ttkthemes
import webbrowser
import tkinter
import pyfiglet
import time
import ipaddress
import os
import json
import pycountry
from tkinter import ttk
from tkinter import *

os.chdir(os.path.dirname(__file__))

scrollbarfix = True
entriesLabels = []
addedEntries = []
writeToFile = []
font = "big"


def findindex(array, sub):
    counter = 0
    while counter <= len(array) - 1:
        if str(sub) == array[counter]: 
            return counter
        else: 
            counter += 1

def change(a, b, top):
    global entriesLabels
    global addedEntries

    top.destroy()

    index1 = findindex(entriesLabels, a)
    index2 = findindex(entriesLabels, b)

    entriesLabels[index1] = b
    entriesLabels[index2] = a

    addedEntries[index1][1]["text"] = b
    addedEntries[index2][1]["text"] = a

def popup(text, do):
    top = Toplevel(app)
    top.resizable(False, False)

    label = ttk.Label(top, text=text)
    name = ttk.Entry(top)
    checkButtonState = tkinter.IntVar()
    
    if do == "add":
        top.title("Add")
        btn = ttk.Button(top, text="Add", command=lambda: add(name.get(), checkButtonState.get(), top))
    if do == "addc":
        btn = ttk.Button(top, text="Add", command=lambda: add("Chapter: " + name.get(), None, top))
    if do == "remove":
        top.title("Remove")
        btn = ttk.Button(top, text="Remove", command=lambda: remove(name.get(), top))
    if do == "rename":
        top.title("Rename")
        name2 = ttk.Entry(top)
        btn = ttk.Button(top, text="Rename", command=lambda: rename(name.get(), name2.get(), top))
    if do == "changepos":
        top.title("Change position")
        name2 = ttk.Entry(top)
        btn = ttk.Button(top, text="Change", command=lambda: change(name.get(), name2.get(), top))

    label.pack(padx=10, pady=2)
    name.pack(padx=10, pady=2)

    try:
        name2.pack(padx=10, pady=2)
    except: 
        pass

    btn.pack(padx=10, pady=2)

    if do == "add":
        btn2 = ttk.Checkbutton(top, text="Geolocate (IPs only)", variable=checkButtonState, takefocus=0)
        btn2.pack()
        top.geometry("200x120")
    elif do == "rename" or do == "changepos":
        top.geometry("200x120")
    else:
        top.geometry("200x90")

def add(text, locator, top):
    global scrollbarfix

    top.destroy()
    
    if text in entriesLabels or text == "":
        return

    entry_label = ttk.Label(second_frame, text=text)
    entry_label.pack(padx=10, pady=10)
    
    if "Chapter:" in text:
        addedEntries.append([None, entry_label])
    else:
        entry = ttk.Entry(second_frame, width=100)
        entry.pack(padx=10, pady=0)
        addedEntries.append([entry, entry_label])

    if locator == 1:
        entriesLabels.append(text + " (IP)")
    else:
        entriesLabels.append(text)

    if scrollbarfix: app.geometry("650x501") #scrollbar lazy fix
    else: app.geometry("650x500")
    scrollbarfix = not scrollbarfix

def remove(text, top):
    global addedEntries
    
    top.destroy()

    index = findindex(entriesLabels, text)

    for shit in addedEntries[index]:
        try:
            shit.pack_forget()
        except:
            pass
    addedEntries.pop(index)
    entriesLabels.pop(index)

def save():
    global entry1_text
    global entry1
    global entry2_text
    global entry2 
    global entriesLabels

    _time = round(time.time())

    with open(f"dox{_time}.txt", "a", encoding="utf-8") as f:
        f.write(f"{pyfiglet.figlet_format(entry1.get(), font=font)}\nReason for dox: {entry2.get()}\n\n")
        f.close()

    for entries in addedEntries:
        try:
            try:
                with open(f"dox{_time}.txt", "a", encoding="utf-8") as f:
                    f.write(F"{entries[1].cget('text').capitalize()}: {entries[0].get()}\n")
                    f.close()
            except:
                with open(f"dox{_time}.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n{pyfiglet.figlet_format(str(entries[1].cget('text')).removeprefix('Chapter: '), font=font)}")

            if f"{entries[1].cget('text')} (IP)" in entriesLabels:
                try: 
                    ipaddress.ip_address(entries[0].get())
                    response = DbIpCity.get(entries[0].get(), api_key='free')
                    r = json.loads(response.to_json())
                    country = pycountry.countries.get(alpha_2=str(r['country']).upper())
                    with open(f"dox{_time}.txt", "a", encoding="utf-8") as f:
                        f.write(f"""\nCity: {r['city']}\n
                        Region: {r['region']}\n
                        Country: {r['country']} ({country.official_name})\n
                        Latitude: {r['latitude']}\n
                        Longitude: {r['longitude']}\n\n
                        Map view: https://www.google.com/maps/@{r['latitude']},{r['longitude']},17z\n\n""")
                        f.close()
                except:
                    pass
        except:
            pass
    
    with open(f"dox{_time}.txt", "a", encoding="utf-8") as f:
        f.write(F"\n\n\nCreated with superior DOX TOOL by Crystallek#3348 (https://github.com/Crystallek/python-dox-tool)")
        f.close()

    os.system(f"start notepad.exe {os.path.dirname(__file__)}\\dox{_time}.txt")

def rename(a, b, top):
    global entriesLabels
    global addedEntries

    top.destroy()
    index = findindex(entriesLabels, a)
    entriesLabels[index] = b
    addedEntries[index][1]["text"] = b

app = ttkthemes.ThemedTk(theme="arc")
app.geometry("650x500")
app.resizable(False, False)
app.title("DOX TOOL")

menubar = Menu(app)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Add", command=lambda: popup("Add", "add"))
filemenu.add_command(label="Add Chapter", command=lambda: popup("Add Chapter", "addc"))
filemenu.add_command(label="Remove", command=lambda: popup("Remove", "remove"))
filemenu.add_command(label="Rename", command=lambda: popup("Rename", "rename"))
filemenu.add_command(label="Change position", command=lambda: popup("Change position", "changepos"))
filemenu.add_command(label="Save", command=lambda: save())
filemenu.add_separator()
filemenu.add_command(label="Exit (ALT + F4)", command=lambda: exit())
menubar.add_cascade(label="Main", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="GitHub", command=lambda: webbrowser.open_new("https://github.com/Crystallek/python-dox-tool"))
menubar.add_cascade(label="Help", menu=helpmenu)

app.config(menu=menubar)

main_frame = Frame(app, takefocus=0)
main_frame.pack(fill=BOTH, expand=1)

main_canvas = Canvas(main_frame, takefocus=0)
main_canvas.pack(side=LEFT, fill=BOTH, expand=1)

main_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=main_canvas.yview)
main_scrollbar.pack(side=RIGHT, fill=Y)

main_canvas.configure(yscrollcommand=main_scrollbar.set)
main_canvas.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))

second_frame = Frame(main_canvas, takefocus=0)
main_canvas.create_window((0,0), window=second_frame, anchor="nw")

entry1_text = ttk.Label(second_frame, text="DOX NAME")
entry1 = ttk.Entry(second_frame, width=100)
entry1_text.pack(padx=10, pady=10)
entry1.pack(padx=10, pady=0)

entry2_text = ttk.Label(second_frame, text="DOX REASON")
entry2 = ttk.Entry(second_frame, width=100)
entry2_text.pack(padx=10, pady=10)
entry2.pack(padx=10, pady=0)

app.mainloop()
