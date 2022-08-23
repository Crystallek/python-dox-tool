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
    top.resizable(False, False)

    label = ttk.Label(top, text=text)
    name = ttk.Entry(top)
    checkButtonState = tkinter.IntVar()
    
    if do == "add":
        top.title("Add")
        btn = ttk.Button(top, text="Add", command=lambda: add(name.get(), checkButtonState.get()))
    if do == "addc":
        btn = ttk.Button(top, text="Add", command=lambda: add("Chapter: " + name.get(), None))
    if do == "remove":
        top.title("Remove")
        btn = ttk.Button(top, text="Remove", command=lambda: remove(name.get()))

    label.pack(padx=10, pady=2)
    name.pack(padx=10, pady=2)
    btn.pack(padx=10, pady=2)

    if do == "add":
        btn2 = ttk.Checkbutton(top, text="Geolocate (IPs only)", variable=checkButtonState, takefocus=0)
        btn2.pack()
        top.geometry("200x120")
    else:
        top.geometry("200x90")

def add(text, locator):
    global top
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

def remove(text):
    global top
    global addedEntries
    
    top.destroy()

    index = findindex(len(entriesLabels) - 1, entriesLabels, text)

    for shit in addedEntries[index]:
        try:
            shit.pack_forget()
        except:
            pass
    addedEntries.pop(index)
    entriesLabels.pop(index)

def save():
    global entry1_text, entry1, entriesLabels
    _time = round(time.time())

    with open(f"dox{_time}.txt", "a", encoding="utf-8") as f:
        f.write(pyfiglet.figlet_format(entry1.get(), font='big'))
        f.close()

    for entries in addedEntries:
        try:
            try:
                with open(f"dox{_time}.txt", "a", encoding="utf-8") as f:
                    f.write(F"{entries[1].cget('text').capitalize()}: {entries[0].get()}\n\n\n")
                    f.close()
            except:
                pass

            if f"{entries[1].cget('text')} (IP)" in entriesLabels:
                try: 
                    ipaddress.ip_address(entries[0].get())
                    response = DbIpCity.get(entries[0].get(), api_key='free')
                    r = json.loads(response.to_json())
                    country = pycountry.countries.get(alpha_2=str(r['country']).upper())
                    with open(f"dox{_time}.txt", "a", encoding="utf-8") as f:
                        f.write(f"\nCity: {r['city']}\n")
                        f.write(f"Region: {r['region']}\n")
                        f.write(f"Country: {r['country']} ({country.official_name})\n")
                        f.write(f"Latitude: {r['latitude']}\n")
                        f.write(f"Longitude: {r['longitude']}\n\n")
                        f.write(f"Map view: https://www.google.com/maps/@{r['latitude']},{r['longitude']},17z")
                        f.close()
                except:
                    pass
        except:
            with open(f"dox{_time}.txt", "a", encoding="utf-8") as f:
                f.write(f"{pyfiglet.figlet_format(str(entries[1].cget('text')).removeprefix('Chapter: '), font='big')}\n")
    
    with open(f"dox{_time}.txt", "a", encoding="utf-8") as f:
        f.write(F"Created with superior DOX TOOL by Crystallek#3348 (https://github.com/Crystallek/dox-app)")
        f.close()

app = ttkthemes.ThemedTk(theme="arc")
app.geometry("650x500")
app.resizable(False, False)

menubar = Menu(app)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Add", command=lambda: popup("Add", "add"))
filemenu.add_command(label="Add Chapter", command=lambda: popup("Add Chapter", "addc"))
filemenu.add_command(label="Remove", command=lambda: popup("Remove", "remove"))
filemenu.add_command(label="Save", command=lambda: save())
filemenu.add_separator()
filemenu.add_command(label="Exit (ALT + F4)", command=lambda: exit())
menubar.add_cascade(label="Main", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="GitHub", command=lambda: webbrowser.open_new("https://github.com/Crystallek/dox-app"))
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

app.mainloop()
