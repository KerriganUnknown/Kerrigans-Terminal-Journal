import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
import sys
import os
import shutil
#sound
import pygame
pygame.mixer.init()

#------------for button click sound
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS  # PyInstaller temporary folder
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
    
#-----------typing click
typing_sound = pygame.mixer.Sound(resource_path("assets/audio/keyboard_click.wav"))
typing_sound.set_volume(0.05)  # keep it subtle

def play_typing_sound(event):
    if event.char and event.char.isprintable():
        typing_sound.play()

#-----------------sound - UI button click
click_sound = pygame.mixer.Sound(resource_path("assets/audio/button_click.wav"))
click_sound.set_volume(0.1)  # adjust volume to taste

def make_button(parent, text, command, **kwargs):
    """Creates a Tkinter button that plays a click sound automatically."""
    def wrapped_command():
        click_sound.play()  # play the sound
        command()           # run the original function
    return tk.Button(parent, text=text, command=wrapped_command, **kwargs)

#-------------------sound - loading screen
def play_loading_sound():
    pygame.mixer.music.load(resource_path("assets/audio/loading_sound.wav"))
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()

# -------------------- Create root --------------------
root = tk.Tk()
root.withdraw()  # hide main window

# Function to check for font
def check_font(font_name):
    available_fonts = tkFont.families()
    if font_name not in available_fonts:
        messagebox.showerror(
            "Font Not Found",
            f"The required font '{font_name}' is not installed on your system.\n\n"
            "Please install it from:\n"
            "assets/font/FSEX300.ttf\n"
            "right-click to install"
        )
        sys.exit()  # prevent app from launching

# Check for the required font
check_font("Fixedsys Excelsior 3.01")

# -------------------- Resource Path --------------------
def resource_path(relative_path):
    try:
        base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
    
# Path where the user’s journal will live
writable_journal = os.path.join(os.path.dirname(sys.executable), "journal_entries.txt")

# Copy the bundled one if it doesn't exist yet
if not os.path.exists(writable_journal):
    bundled_journal = resource_path("journal_entries.txt")  # reads from PyInstaller bundle
    shutil.copy(bundled_journal, writable_journal)

# Use this path everywhere
journal_file = writable_journal

# -------------------- Fonts --------------------
FONT_LABEL = ("Fixedsys Excelsior 3.01", 14)
FONT_ENTRY = ("Fixedsys Excelsior 3.01", 14)
FONT_BUTTON = ("Fixedsys Excelsior 3.01", 14)
FONT_TEXT = ("Fixedsys Excelsior 3.01", 14)
FONT_TITLE = ("Fixedsys Excelsior 3.01", 16, "bold")

# -------------------- Colors --------------------
LEFT_BG = "#0a0f0a"
RIGHT_BG = "#1a1f1a"
ENTRY_BG = "#0f1a0f"
ENTRY_FG = "#33ff33"
BUTTON_BG = "#222922"
BUTTON_FG = "#99ff99"
TITLE_BG = "#050a05"
TITLE_FG = "#33ff33"
BUTTON_HOVER_BG = "#339933"

#-----------------------Title Length------------------------
MAX_TITLE_LENGTH = 30 

# -------------------- Helper Functions --------------------
def center_root():
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

# -------------------- Custom Popups --------------------
def create_title_bar(parent, title_text):
    title_bar = tk.Frame(parent, bg=TITLE_BG, relief="raised", bd=0, height=30)
    title_bar.pack(fill="x")

    title_label = tk.Label(title_bar, text=title_text, font=FONT_TITLE,
                           bg=TITLE_BG, fg=TITLE_FG, anchor="w")
    title_label.pack(side="left", padx=10)

    move_data = {"x": 0, "y": 0}

    def start_move_popup(event):
        move_data["x"] = event.x
        move_data["y"] = event.y

    def on_motion_popup(event):
        dx = event.x - move_data["x"]
        dy = event.y - move_data["y"]
        parent.geometry(f"+{parent.winfo_x() + dx}+{parent.winfo_y() + dy}")

    title_bar.bind("<Button-1>", start_move_popup)
    title_bar.bind("<B1-Motion>", on_motion_popup)
    title_label.bind("<Button-1>", start_move_popup)
    title_label.bind("<B1-Motion>", on_motion_popup)


def show_info(title, message, extra_height=0):
    popup = tk.Toplevel(root)
    popup.withdraw()
    popup.title(title)
    popup.transient(root)
    popup.configure(bg=LEFT_BG)
    popup.resizable(False, False)
    popup.iconbitmap(resource_path("assets/images/Terminal_icon.ico")) 

    base_width = 320
    base_height = 190 + extra_height 

    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x = (screen_width // 2) - (base_width // 2)
    y = (screen_height // 2) - (base_height // 2)
    popup.geometry(f"{base_width}x{base_height}+{x}+{y}")

    tk.Label(popup, text=message, font=FONT_LABEL,
             bg=LEFT_BG, fg=ENTRY_FG, wraplength=280, justify="center").pack(expand=True, pady=(40, 10))

    make_button(popup, text="[ OK ]", font=FONT_BUTTON,
              bg=BUTTON_BG, fg=BUTTON_FG,
              activebackground="#339933", activeforeground="#000000",
              width=12, command=popup.destroy).pack(pady=20)

    popup.deiconify()
    popup.grab_set()
    root.wait_window(popup)

def show_custom_confirm(title, message):
    result = {"value": False}

    popup = tk.Toplevel(root)
    popup.title(title)
    popup.transient(root)
    popup.configure(bg=LEFT_BG)
    popup.resizable(False, False)
    popup.iconbitmap(resource_path("assets/images/Terminal_icon.ico")) 

    window_width = 320
    window_height = 190
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    popup.geometry(f"{window_width}x{window_height}+{x}+{y}")

    tk.Label(popup, text=message, font=FONT_LABEL,
             bg=LEFT_BG, fg=ENTRY_FG, wraplength=280, justify="center").pack(expand=True, pady=(40, 10))

    button_frame = tk.Frame(popup, bg=LEFT_BG)
    button_frame.pack(pady=20)

    def yes(): 
        result["value"] = True
        popup.destroy()
    def no(): 
        result["value"] = False
        popup.destroy()

    make_button(button_frame, text="[ Yes ]", font=FONT_BUTTON,
              bg=BUTTON_BG, fg=BUTTON_FG, activebackground=BUTTON_HOVER_BG,
              activeforeground="#000000", width=10, command=yes).pack(side="left", padx=10)
    make_button(button_frame, text="[ No ]", font=FONT_BUTTON,
              bg=BUTTON_BG, fg=BUTTON_FG, activebackground=BUTTON_HOVER_BG,
              activeforeground="#000000", width=10, command=no).pack(side="left", padx=10)

    def key_handler(event):
        if event.keysym == "Return":
            yes()
        elif event.keysym == "Escape":
            no()

    popup.bind("<Key>", key_handler)

    popup.grab_set()
    root.wait_window(popup)
    return result["value"]

# -------------------- Main Window --------------------
root.iconbitmap(resource_path("assets/images/Terminal_icon.ico"))
root.title("[ReelCore Terminal MODEL E-8872]")
root.geometry("600x460")
root.minsize(400, 350)
root.configure(bg=LEFT_BG)
root.resizable(True, True)

# -------------------- Left Frame --------------------
left_frame = tk.Frame(root, bg=LEFT_BG)
left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

# -------------------- Headers --------------------
tk.Label(
    left_frame,
    text="[Welcome to Analog Industries (TM) YomaLink]",
    font=("Fixedsys Excelsior 3.01", 18),
    bg=LEFT_BG,
    fg=ENTRY_FG,
).pack(anchor="w", padx=10, pady=(5, 2)) 

tk.Label(
    left_frame,
    text="[Personal Journal]",
    font=("Fixedsys Excelsior 3.01", 16),
    bg=LEFT_BG,
    fg=ENTRY_FG,
).pack(anchor="w", padx=10, pady=(2, 2))  

tk.Label(left_frame, text="[Search]:", font=FONT_LABEL, bg=LEFT_BG, fg=ENTRY_FG).pack(
    anchor="w", padx=10, pady=(2, 0)
)

search_var = tk.StringVar()
search_entry = tk.Entry(
    left_frame,
    font=FONT_ENTRY,
    textvariable=search_var,
    bg=ENTRY_BG,
    fg=ENTRY_FG,
    insertbackground=ENTRY_FG,
    insertwidth=3
)
search_entry.pack(fill="x", padx=10, pady=(0, 5))
search_entry.bind("<Key>", play_typing_sound)

def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg='grey')
    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=ENTRY_FG)
            filter_entries()  
    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg='grey')
            filter_entries()
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

add_placeholder(search_entry, "Type to filter entries...")

listbox_frame = tk.Frame(left_frame, bg=LEFT_BG)
listbox_frame.pack(expand=True, fill="both", padx=10, pady=(0, 10))

entries_listbox = tk.Listbox(
    listbox_frame,
    font=FONT_TEXT,
    bg=ENTRY_BG,
    fg=ENTRY_FG,
    selectbackground="#339933",
    selectforeground="#0a0f0a",
    exportselection=False,
    selectmode="extended"
)
entries_listbox.pack(side="left", fill="both", expand=True)

# Scrollbar for the listbox
entries_scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=entries_listbox.yview)
entries_scrollbar.pack(side="right", fill="y")

# Link scrollbar to listbox
entries_listbox.config(yscrollcommand=entries_scrollbar.set)

all_entries = []

# -------------------- Load & Filter Entries --------------------
def load_entries():
    global all_entries
    entries_listbox.delete(0, tk.END)
    all_entries = []
    try:
        with open("journal_entries.txt", "r", encoding="utf-8") as f:
            data = f.read().split("\n---\n")
            for entry in data:
                if entry.strip() != "":
                    title = entry.strip().split("\n")[0]
                    all_entries.append(title)
        for title in all_entries:
            entries_listbox.insert(tk.END, f"[{title}]")
    except FileNotFoundError:
        pass

def filter_entries(*args):
    query = search_var.get().strip().lower()
   
    if search_entry.cget("fg") == "grey" or query == "":
        entries_listbox.delete(0, tk.END)
        for title in all_entries:
            entries_listbox.insert(tk.END, f"[{title}]")
        return

    entries_listbox.delete(0, tk.END)
    for title in all_entries:
        if query in title.lower():
            entries_listbox.insert(tk.END, f"[{title}]")

search_var.trace_add("write", filter_entries)

# -------------------- Entry Windows --------------------
def new_entry():
    title_window = tk.Toplevel(root)
    title_window.transient(root)
    title_window.configure(bg=LEFT_BG)
    title_window.resizable(False, False)
    title_window.iconbitmap(resource_path("assets/images/Terminal_icon.ico")) 

    window_width, window_height = 400, 150
    screen_width = title_window.winfo_screenwidth()
    screen_height = title_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    title_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    content_frame = tk.Frame(title_window, bg=LEFT_BG)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tk.Label(content_frame, text="Enter Entry Title:", font=FONT_LABEL, bg=LEFT_BG, fg=ENTRY_FG).pack(anchor="w")

    entry_var = tk.StringVar()
    title_entry = tk.Entry(content_frame, font=FONT_ENTRY, bg=ENTRY_BG, fg=ENTRY_FG,
                           insertbackground=ENTRY_FG, insertwidth=3, textvariable=entry_var, width=30)
    title_entry.pack(pady=(0, 5))
    title_entry.focus()
    
    #typing sound
    title_entry.bind("<Key>", play_typing_sound)

    CHAR_LIMIT = 30  

    def enforce_limit(*args):
        value = entry_var.get()
        if len(value) > CHAR_LIMIT:
            entry_var.set(value[:CHAR_LIMIT])
        char_count_label.config(text=f"{len(entry_var.get())}/{CHAR_LIMIT}")

    entry_var.trace_add("write", enforce_limit)

    char_count_label = tk.Label(content_frame, text=f"0/{CHAR_LIMIT}", font=FONT_LABEL,
                                bg=LEFT_BG, fg=ENTRY_FG)
    char_count_label.pack(anchor="e")


    def submit_title():
        title = entry_var.get().strip()
        if not title:
            show_info("Warning", "Title cannot be empty!")
            return

        if title in all_entries:
            overwrite = show_custom_confirm(
                "Duplicate Entry",
                f"An entry titled '{title}' already exists.\nDo you want to overwrite it?"
            )
            if not overwrite:
                return
        if title not in all_entries:
            all_entries.append(title)
            entries_listbox.insert(tk.END, f"[{title}]")
        title_window.destroy()
        open_entry_window(title)

    title_entry.bind("<Return>", lambda event: submit_title())

    make_button(
        content_frame,
        text="[Save]",
        font=FONT_BUTTON,
        bg=BUTTON_BG,
        fg=BUTTON_FG,
        activebackground=BUTTON_HOVER_BG,  
        activeforeground="#000000",         
        width=16,
        command=submit_title
    ).pack(pady=(5,0))

def open_entry_window(title):
    entry_window = tk.Toplevel(root)
    entry_window.withdraw() 
    entry_window.title(f"Entry: {title}")
    entry_window.iconbitmap(resource_path("assets/images/Terminal_icon.ico"))
    entry_window.configure(bg=LEFT_BG)
    entry_window.minsize(600, 400)

    create_title_bar(entry_window, f"Entry: {title}")

    bottom_frame = tk.Frame(entry_window, bg=LEFT_BG)
    bottom_frame.pack(side="bottom", fill="x", padx=10, pady=5)

    text_frame = tk.Frame(entry_window, bg=LEFT_BG)
    text_frame.pack(fill="both", expand=True, padx=10, pady=(10,0))

    text_scrollbar = tk.Scrollbar(text_frame, orient="vertical")
    text_scrollbar.pack(side="right", fill="y")

    text_area = tk.Text(
        text_frame, font=FONT_TEXT, bg=ENTRY_BG, fg=ENTRY_FG,
        insertbackground=ENTRY_FG, insertwidth=3,
        yscrollcommand=text_scrollbar.set, wrap="word"
    )
    text_area.pack(fill="both", expand=True)
    text_area.focus_set()

    text_scrollbar.config(command=text_area.yview)

    MAX_ENTRY_CHARS = 5000

    # create a label below your Text widget
    char_count_label = tk.Label(bottom_frame, text=f"0/{MAX_ENTRY_CHARS}", 
                                font=FONT_LABEL, bg=LEFT_BG, fg=ENTRY_FG)
    char_count_label.pack(anchor="e", padx=10, pady=(0,5))

    def handle_key(event):
        # typing sound
        if event.char and event.char.isprintable():
            typing_sound.play()

        # character count
        current_length = len(text_area.get("1.0", "end-1c"))
        char_count_label.config(text=f"{current_length}/{MAX_ENTRY_CHARS}")

        # char limit
        if current_length >= MAX_ENTRY_CHARS and event.keysym not in (
            "BackSpace", "Delete", "Left", "Right", "Up", "Down"
        ):
            return "break"

    text_area.bind("<KeyRelease>", handle_key)

    try:
        with open("journal_entries.txt", "r", encoding="utf-8") as f:
            data = f.read().split("\n---\n")
            for entry in data:
                if entry.startswith(title + "\n") or entry.strip() == title:
                    content = "\n".join(entry.split("\n")[1:])
                    text_area.insert("1.0", content)
                    char_count_label.config(text=f"{len(text_area.get('1.0', 'end-1c'))}/{MAX_ENTRY_CHARS}")
                    break
    except FileNotFoundError:
        pass

    def save_and_close():
        content = text_area.get("1.0", tk.END)
        updated_entries = []
        try:
            with open("journal_entries.txt", "r", encoding="utf-8") as f:
                data = f.read().split("\n---\n")
        except FileNotFoundError:
            data = []

        found = False
        for entry in data:
            if entry.startswith(title + "\n") or entry.strip() == title:
                if content:
                    updated_entries.append(f"{title}\n{content}")
                found = True
            else:
                updated_entries.append(entry)
        if not found and content:
            updated_entries.append(f"{title}\n{content}")

        with open("journal_entries.txt", "w", encoding="utf-8") as f:
            f.write("\n---\n".join(updated_entries) + "\n---\n")
        entry_window.destroy()

    make_button(
        bottom_frame,
        text="[Save and Return]",
        font=FONT_BUTTON,
        bg=BUTTON_BG,
        fg=BUTTON_FG,
        activebackground=BUTTON_HOVER_BG, 
        activeforeground="#000000",        
        width=16,
        command=save_and_close
    ).pack()

    # ---------------- Center & Show ----------------
    entry_window.update_idletasks()  
    width = entry_window.winfo_width()
    height = entry_window.winfo_height()
    screen_width = entry_window.winfo_screenwidth()
    screen_height = entry_window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    entry_window.geometry(f"{width}x{height}+{x}+{y}")

    entry_window.deiconify() 
    entry_window.grab_set()  

# -------------------- Entry Actions --------------------
def open_selected():
    selection = entries_listbox.curselection()
    if not selection:
        show_info("Open Entry", "Please select an entry to open.")
        return
    title = entries_listbox.get(selection[0])[1:-1]
    open_entry_window(title)

def show_custom_rename(old_title):
    result = {"value": None}

    popup = tk.Toplevel(root)
    popup.title("Rename Entry")
    popup.transient(root)
    popup.configure(bg=LEFT_BG)
    popup.resizable(False, False)
    popup.iconbitmap(resource_path("assets/images/Terminal_icon.ico"))  

    window_width = 400
    window_height = 190
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    popup.geometry(f"{window_width}x{window_height}+{x}+{y}")

    tk.Label(popup, text="Rename Entry:", font=FONT_LABEL,
             bg=LEFT_BG, fg=ENTRY_FG).pack(pady=(30, 10))

    entry_var = tk.StringVar()
    entry = tk.Entry(popup, font=FONT_ENTRY, bg=ENTRY_BG, fg=ENTRY_FG,
                     insertbackground=ENTRY_FG, justify="center", textvariable=entry_var, width=30)
    entry.pack(pady=(0, 5))
    entry.insert(0, old_title)
    entry.focus_set()
    
    #----typing sound
    entry.bind("<Key>", play_typing_sound)

    CHAR_LIMIT = 30
    char_count_label = tk.Label(popup, text=f"{len(old_title)}/{CHAR_LIMIT}", font=FONT_LABEL,
                                bg=LEFT_BG, fg=ENTRY_FG)
    char_count_label.pack(anchor="e", padx=10)

    def enforce_limit(*args):
        value = entry_var.get()
        if len(value) > CHAR_LIMIT:
            entry_var.set(value[:CHAR_LIMIT])
        char_count_label.config(text=f"{len(entry_var.get())}/{CHAR_LIMIT}")

    entry_var.trace_add("write", enforce_limit)

    def confirm():
        new_title_candidate = entry_var.get().strip()
        if new_title_candidate == "":
            show_info("Invalid Name", "Please enter a valid title!")
            return
        result["value"] = new_title_candidate
        popup.destroy()

    make_button(popup, text="[ OK ]", font=FONT_BUTTON, bg=BUTTON_BG, fg=BUTTON_FG,
              activebackground=BUTTON_HOVER_BG, width=10, command=confirm).pack(side="left", padx=30, pady=20)
    make_button(popup, text="[ Cancel ]", font=FONT_BUTTON, bg=BUTTON_BG, fg=BUTTON_FG,
              activebackground=BUTTON_HOVER_BG, width=10, command=popup.destroy).pack(side="right", padx=30, pady=20)

    popup.bind("<Return>", lambda event: confirm())

    popup.grab_set()
    root.wait_window(popup)
    return result["value"]

def rename_selected():
    global all_entries

    selection = entries_listbox.curselection()
    if not selection:
        show_info("Rename Entry", "Please select an entry to rename.")
        return

    old_index = selection[0]
    old_title = all_entries[old_index]

    new_title = show_custom_rename(old_title)
    if not new_title:
        return
    new_title = new_title.strip()
    if new_title == old_title:
        return

    try:
        with open("journal_entries.txt", "r", encoding="utf-8") as f:
            data = [e for e in f.read().split("\n---\n") if e.strip()]
    except FileNotFoundError:
        data = []

    old_file_index = None
    duplicate_index = None
    for i, entry in enumerate(data):
        title = entry.split("\n")[0]
        if title == old_title:
            old_file_index = i
        elif title == new_title:
            duplicate_index = i

    if old_file_index is None:
        show_info("Error", "Original entry not found.")
        return

    old_content = "\n".join(data[old_file_index].split("\n")[1:])

    if duplicate_index is not None:
        overwrite = show_custom_confirm(
            "Duplicate Entry",
            f"An entry titled '{new_title}' already exists.\nDo you want to overwrite it?"
        )
        if not overwrite:
            return
        data[duplicate_index] = f"{new_title}\n{old_content}" if old_content else new_title
        all_entries[duplicate_index] = new_title
        if old_file_index != duplicate_index:
            data.pop(old_file_index)
            if old_index < duplicate_index:
                duplicate_index -= 1
            all_entries.pop(old_index)
    else:
        data[old_file_index] = f"{new_title}\n{old_content}" if old_content else new_title
        all_entries[old_index] = new_title

    with open("journal_entries.txt", "w", encoding="utf-8") as f:
        f.write("\n---\n".join(data) + "\n---\n")

    refresh_entries()
    if duplicate_index is not None:
        entries_listbox.selection_set(duplicate_index)
    else:
        entries_listbox.selection_set(old_index)


def move_up():
    selection = list(entries_listbox.curselection())
    if not selection or selection[0] == 0:
        return 

    for i in selection:
        all_entries[i - 1], all_entries[i] = all_entries[i], all_entries[i - 1]

    refresh_entries()

    entries_listbox.selection_clear(0, tk.END)
    for i in [x - 1 for x in selection]:
        entries_listbox.selection_set(i)

    persist_entries_order()

def move_down():
    selection = list(entries_listbox.curselection())
    if not selection or selection[-1] == len(all_entries) - 1:
        return 

    for i in reversed(selection):
        all_entries[i + 1], all_entries[i] = all_entries[i], all_entries[i + 1]

    refresh_entries()

    entries_listbox.selection_clear(0, tk.END)
    for i in [x + 1 for x in selection]:
        entries_listbox.selection_set(i)

    persist_entries_order()

def delete_selected():
    selection = entries_listbox.curselection()
    if not selection:
        show_info("Delete Entry", "Please select an entry to delete.")
        return

    titles = [all_entries[i] for i in selection]
    display_titles = ", ".join([t if len(t) <= 20 else t[:20]+"…" for t in titles])
    if not show_custom_confirm("Delete Entries", f"Delete {display_titles}?"):
        return

    for index in reversed(selection):
        all_entries.pop(index)
        entries_listbox.delete(index)

    persist_entries_order()

def refresh_entries():
    entries_listbox.delete(0, tk.END)
    for title in all_entries:
        entries_listbox.insert(tk.END, f"[{title}]")

def persist_entries_order():
    updated_entries = []
    try:
        with open("journal_entries.txt", "r", encoding="utf-8") as f:
            data = f.read().split("\n---\n")
    except FileNotFoundError:
        data = []

    for title in all_entries:
        content = ""
        for entry in data:
            if entry.startswith(title + "\n") or entry.strip() == title:
                content = "\n".join(entry.split("\n")[1:])
                break
        updated_entries.append(f"{title}\n{content}" if content else title)

    with open("journal_entries.txt", "w", encoding="utf-8") as f:
        f.write("\n---\n".join(updated_entries) + "\n---\n")

# -------------------- Main Buttons --------------------
button_frame_main = tk.Frame(left_frame, bg=LEFT_BG)
button_frame_main.pack(side="bottom", fill="x", padx=6, pady=6)

make_button(button_frame_main, text="[New]", font=FONT_BUTTON, bg=BUTTON_BG, fg=BUTTON_FG,
            relief="groove", bd=2, activebackground="#339933", command=new_entry).pack(side="left", padx=5)

open_button = make_button(
    button_frame_main, text="[Open]", font=FONT_BUTTON, bg=BUTTON_BG, fg=BUTTON_FG,
    relief="groove", bd=2, activebackground="#339933", command=open_selected
)
open_button.pack(side="left", padx=5)

rename_button = make_button(button_frame_main, text="[Rename]", font=FONT_BUTTON, bg=BUTTON_BG, fg=BUTTON_FG,
                            relief="groove", bd=2, activebackground="#339933", command=rename_selected)
rename_button.pack(side="left", padx=5)

make_button(button_frame_main, text="[Move Up]", font=FONT_BUTTON, bg=BUTTON_BG, fg=BUTTON_FG,
            relief="groove", bd=2, activebackground="#339933", command=move_up).pack(side="left", padx=5)

make_button(button_frame_main, text="[Move Down]", font=FONT_BUTTON, bg=BUTTON_BG, fg=BUTTON_FG,
            relief="groove", bd=2, activebackground="#339933", command=move_down).pack(side="left", padx=5)

make_button(button_frame_main, text="[Delete]", font=FONT_BUTTON, bg=BUTTON_BG, fg=BUTTON_FG,
            relief="groove", bd=2, activebackground="#339933", command=delete_selected).pack(side="left", padx=5)

# -------------------- Button Enable/Disable Logic --------------------
def update_button_states(event=None):
    selection = entries_listbox.curselection()
    if len(selection) == 1:
        rename_button.config(state="normal")
        open_button.config(state="normal")
    else:
        rename_button.config(state="disabled")
        open_button.config(state="disabled")

entries_listbox.bind("<<ListboxSelect>>", update_button_states)

update_button_states()

# -------------------- Double Click --------------------
def on_entry_double_click(event):
    selection = entries_listbox.curselection()
    if selection:
        title = entries_listbox.get(selection[0])[1:-1]
        open_entry_window(title)

entries_listbox.bind("<Double-1>", on_entry_double_click)

# -------------------- Loading Screen --------------------
def show_loading_screen():
    play_loading_sound()
    loading_screen = tk.Toplevel(root)
    loading_screen.title("ReelCore Terminal Boot")
    loading_screen.configure(bg=LEFT_BG)
    loading_screen.geometry("500x365")
    loading_screen.resizable(False, False)
    loading_screen.transient(root)
    loading_screen.grab_set()
    loading_screen.iconbitmap(resource_path("assets/images/Terminal_icon.ico"))

    # Center window
    screen_width = loading_screen.winfo_screenwidth()
    screen_height = loading_screen.winfo_screenheight()
    x = (screen_width // 2) - 250
    y = (screen_height // 2) - 182
    loading_screen.geometry(f"500x365+{x}+{y}")

    # Fonts and colors
    header_font = ("Fixedsys Excelsior 3.01", 14, "bold")  # slightly smaller
    title_font = ("Fixedsys Excelsior 3.01", 32, "bold")   # slightly smaller
    small_font = ("Fixedsys Excelsior 3.01", 16)
    bar_fill_color = "#33ff33"

    # Header Labels
    tk.Label(
        loading_screen,
        text="ANALOG INDUSTRIES (TM)\nYOMALINK PROTOCOL",
        font=header_font,
        bg=LEFT_BG,
        fg=ENTRY_FG
    ).pack(pady=(6, 0))

    tk.Label(
        loading_screen,
        text="CLAYMORE OPERATING\nSYSTEMS",
        font=title_font,
        bg=LEFT_BG,
        fg=ENTRY_FG
    ).pack(pady=(0, 0))

    # Version label
    tk.Label(
        loading_screen,
        text="v1.1.0",
        font=small_font,
        bg=LEFT_BG,
        fg=ENTRY_FG
    ).pack(pady=(0, 6))

    tk.Label(
        loading_screen,
        text="© 1986–2025 ErriganK SYSTEMS",
        font=small_font,
        bg=LEFT_BG,
        fg=ENTRY_FG
    ).pack(pady=(0, 6))


    # Loading message
    loading_msg = tk.Label(
        loading_screen,
        text="ACCESSING DATA VAULTS . . .",
        font=header_font,
        bg=LEFT_BG,
        fg=ENTRY_FG
    )
    loading_msg.pack(pady=(0, 2))

    # Progress Bar
    progress_frame = tk.Frame(loading_screen, bg=LEFT_BG)
    progress_frame.pack(pady=(0, 10), fill="x", padx=40)
    progress_bar = tk.Canvas(progress_frame, bg=ENTRY_BG, height=30, highlightthickness=0)
    progress_bar.pack(fill="x")

    outline_thickness = 3
    padding = 2
    height = 30
    progress_bar.update_idletasks()
    canvas_width = progress_bar.winfo_width()
    progress_bar.create_rectangle(
        padding, padding,
        canvas_width - padding, height - padding,
        outline=bar_fill_color, width=outline_thickness
    )

    # Steps
    steps = [
        (25, "BOOT SEQUENCE INITIATED..."),
        (50, "INITIALIZING SECTORS..."),
        (75, "SYNCING ENTRIES..."),
        (100, "LOADING INTERFACE MODULES...")
    ]

    def update_progress(index=0):
        if index >= len(steps):
            final_label = tk.Label(
                loading_screen,
                text="SYSTEM ONLINE",
                font=header_font,
                bg=LEFT_BG,
                fg=ENTRY_FG
            )
            final_label.pack(pady=(4, 0))

            def flash(times=4):
                if times > 0:
                    final_label.config(fg=LEFT_BG if final_label.cget("fg") == ENTRY_FG else ENTRY_FG)
                    loading_screen.after(250, lambda: flash(times - 1))
                else:
                    journal_label = tk.Label(
                        loading_screen,
                        text="",
                        font=header_font,
                        bg=LEFT_BG,
                        fg=ENTRY_FG
                    )
                    journal_label.pack(pady=(1, 0))

                    def type_text(label, text, idx=0):
                        display_text = text[:idx] + ("█" if idx <= len(text) else "")
                        label.config(text=display_text)
                        if idx < len(text):
                            loading_screen.after(80, lambda: type_text(label, text, idx + 1))
                        else:
                            def blink_cursor(times=6, visible=True):
                                if times > 0:
                                    label.config(text=text + ("█" if visible else ""))
                                    loading_screen.after(300, lambda: blink_cursor(times-1, not visible))
                                else:
                                    loading_screen.after(500, lambda: [loading_screen.destroy(), root.deiconify(), center_root()])
                            blink_cursor()
                    type_text(journal_label, "Journal Initialized")
            flash()
            return

        percent, message = steps[index]
        progress_bar.update_idletasks()
        canvas_width = progress_bar.winfo_width()
        max_width = canvas_width - 2*(padding + outline_thickness)
        prev_width = (steps[index-1][0]/100)*max_width if index > 0 else 0
        target_width = (percent/100)*max_width

        step_count = 12
        step_duration = 80

        for i in range(1, step_count + 1):
            def mini_step(i=i):
                fill_width = int(prev_width + (target_width - prev_width)*i/step_count)
                fill_width = min(fill_width, max_width)
                progress_bar.delete("fill")

                # CRT glow effect: layered rectangles
                for glow_offset in [2, 1, 0]:
                    progress_bar.create_rectangle(
                        padding + outline_thickness - glow_offset,
                        padding + outline_thickness - glow_offset,
                        padding + outline_thickness + fill_width + glow_offset,
                        height - padding - outline_thickness + glow_offset,
                        fill=bar_fill_color,
                        width=0,
                        stipple="gray25",
                        tags="fill"
                    )

            loading_screen.after(i*step_duration, mini_step)

        # Update message
        loading_screen.after(step_count*step_duration, lambda: loading_msg.config(text=message))

        # Next step
        loading_screen.after(step_count*step_duration + 200, lambda: update_progress(index + 1))

    update_progress()

# -------------------- Initialize --------------------
root.withdraw()
root.update() 
show_loading_screen()
load_entries()
root.mainloop()

