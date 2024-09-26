import xml.etree.ElementTree as ET
import re
from tkinter import *
from tkinter import ttk, messagebox, PhotoImage

## FUNCTIONS ##

# Convert button function carries user input to main
def convert_click():
    cat = cat_input.get()
    eng = eng_input.get()
    if root.winfo_exists():
        main(cat, eng)

def main(c = None, e = None):
    c = input_strip(c)
    e = input_strip(e)
    try:
        # Runs user input through the check function then calls corresponding functions.
        result = input_check(c, e)
        if result == "empty":
            messagebox.showerror(message="Please enter a word // Si us plau, introdueix una paraula")
        if result == "clear":
            messagebox.showerror(message="Please clear input // Si us plau, esborra l'entrada")
        if result == "c2e":
            cat_to_eng(c)
            update_gui_c2e(c)
        if result == "e2c":
            eng_to_cat(e)
            update_gui_e2c(e)
    except (TypeError, KeyError, TclError):
        return

def input_check(c, e):
    if c == "" and e == "":
        return "empty"
    elif len(c) > 0 and len(e) > 0:
        return "clear"
    elif len(c) > 0 and e == "":
        return "c2e"
    elif len(e) > 0 and c == "":
        return "e2c"
    
def input_strip(w):
    if w is not None:
        strip = re.sub(r"[\d]", "", w)
        return strip.strip()
    else:
        return

def cat_to_eng(c):
        letter = first_letter(c)
        tree = ET.parse(f"cateng\\{letter}.dic")
        root = tree.getroot()
        result = get_translation(c, root)
        if result == None:
            return "nothing found!"
        else:
            return result

def eng_to_cat(e):
        letter = first_letter(e)
        tree = ET.parse(f"engcat\\{letter}.dic")
        root = tree.getroot()
        result = get_translation(e, root)
        if result == None:
            return "cap resultat!"
        else:
            return result

def first_letter(w):
    letter = w[0]
    return letter

def get_translation(w, r):
    for entry in r.findall("Entry"):
        if entry.text == w or entry.text == w.title() or entry.text == w.lower():
            translations = entry.findall(".//translation")
            for translation in translations:
                return translation.text
            

def update_gui_c2e(c):
    c2e_text = cat_to_eng(c)
    result = f"{c2e_text}"
    eng_result.config(text=result)
    cat_result.config(text=c)
    #equals_label.config(text= "=")

def update_gui_e2c(e):
    e2c_text = eng_to_cat(e)
    result = f"{e2c_text}"
    cat_result.config(text=result)
    eng_result.config(text=e)
    #equals_label.config(text= "=")

# Clear button to reset all fields
def clear_click():
    eng_input.delete(0, END)
    cat_input.delete(0, END)
    eng_result.config(text="")
    cat_result.config(text="")
    #equals_label.config(text= "")

def on_closing():
    root.destroy()

##### GUI #####

root = Tk()
root.option_add("*font", "lato 11")
root.bind("<Return>", lambda event: convert_click())
root.bind("<Escape>", lambda event: clear_click())

# Set the size of the window
window_width = 650
window_height = 600

# Get current screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Find center points of x and y axis
center_x = int((screen_width / 2 - window_width / 2))
center_y = int((screen_height / 2 - window_height / 2))

# Set window position to middle of screen
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

# Set window title
root.title("Diccionari")

# Set window colour
root.configure(background="azure")

# Set window icon
root.iconbitmap("catico.ico")

# Configure grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

# Disable window resize
root.resizable(False, False)

flag = PhotoImage(file="flags.png")
flag_label = ttk.Label(root, image=flag, borderwidth=0, background="azure")
flag_label.grid(columnspan=3, column=0, row=0, padx=22, pady=10)

# English Label
eng_label = ttk.Label(root, text="English")
eng_label.grid(column=0, row=2, padx=5, pady=7)
eng_label.config(background="azure", foreground="gray4")

# Eng input field
eng_input_box = StringVar()
eng_input = ttk.Entry(root, width=30, textvariable=eng_input_box, background="gray3")
eng_input.grid(column=0, row=3, padx=2, pady=2, sticky=E)

# Eng result
eng_result = ttk.Label(root, text="")
eng_result.grid(column=0, row=6, padx=5, pady=5)
eng_result.config(background="azure", foreground="gray4", wraplength=200)

# Equals label
#equals_label = ttk.Label(root, text="")
#equals_label.grid(column=1, row=6, padx=0, pady=5, rowspan=3)
#equals_label.config(background="azure", foreground="gray4")

# Catalan label
cat_label = ttk.Label(root, text="Català")
cat_label.grid(column=2, row=2, padx=5, pady=5)
cat_label.config(background="azure", foreground="gray4")

# Catalan input field
cat_input_box = StringVar()
cat_input = ttk.Entry(root, width=30, textvariable=cat_input_box)
cat_input.grid(column=2, row=3, padx=2, pady=2, sticky=W)

# Cat result
cat_result = ttk.Label(root, text="")
cat_result.grid(column=2, row=6, padx=5, pady=5)
cat_result.config(background="azure", foreground="gray4", wraplength=200)

# Clear button
button_clear = ttk.Button(root, text="Clear // Esborrar", command=clear_click)
button_clear.grid(column=2, row=4, padx=5, pady=5)

# Convert button
button_go = ttk.Button(root, text="Translate // Traduir", command=convert_click)
button_go.grid(column=0, row=4, padx=5, pady=5)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

if __name__ == "__main__":
    main()