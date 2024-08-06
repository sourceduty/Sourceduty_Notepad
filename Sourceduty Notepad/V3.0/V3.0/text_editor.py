# Sourceduty Notepad V3.0
# Copyright (C) 2024, Sourceduty 
# This software is free and open-source; anyone can redistribute it and/or modify it.

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox, simpledialog
from templates import TEMPLATES

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Sourceduty Notepad")
        self.create_menu()
        self.create_widgets()
        self.modes = ["White Mode", "Dark Mode", "Blue Mode"]
        self.current_mode_index = 0
        self.apply_mode()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save As...", command=self.save_file)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all)
        edit_menu.add_command(label="Find", command=self.find)

        mode_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Mode", menu=mode_menu)
        mode_menu.add_command(label="Toggle Mode", command=self.toggle_mode)

        templates_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Templates", menu=templates_menu)
        for template_name in TEMPLATES:
            templates_menu.add_command(label=template_name, command=lambda name=template_name: self.load_template(name))

        control_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Control", menu=control_menu)
        control_menu.add_command(label="Help", command=self.show_help)
        control_menu.add_command(label="About", command=self.show_about)

    def create_widgets(self):
        self.txt_edit = tk.Text(self.root, undo=True)
        self.scrollbar = tk.Scrollbar(self.root, command=self.txt_edit.yview, bg='black', troughcolor='black', activebackground='black', highlightbackground='black')
        self.txt_edit.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_edit.pack(fill=tk.BOTH, expand=1)
        
        self.status_bar = tk.Label(self.root, text="", anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.txt_edit.bind("<<Modified>>", self.on_text_change)
        self.txt_edit.bind("<KeyRelease>", self.on_key_release)

    def apply_mode(self):
        mode = self.modes[self.current_mode_index]
        if mode == "White Mode":
            self.txt_edit.config(bg="white", fg="black", insertbackground="black")
            self.status_bar.config(bg="white", fg="black")
        elif mode == "Dark Mode":
            self.txt_edit.config(bg="black", fg="white", insertbackground="white")
            self.status_bar.config(bg="black", fg="white")
        elif mode == "Blue Mode":
            self.txt_edit.config(bg="lightblue", fg="darkblue", insertbackground="darkblue")
            self.status_bar.config(bg="lightblue", fg="darkblue")
        self.update_status()

    def toggle_mode(self):
        self.current_mode_index = (self.current_mode_index + 1) % len(self.modes)
        self.apply_mode()

    def load_template(self, template_name):
        template_content = TEMPLATES[template_name]
        self.txt_edit.delete(1.0, tk.END)
        self.txt_edit.insert(tk.END, template_content)

    def new_file(self):
        self.txt_edit.delete(1.0, tk.END)
        self.update_status()

    def open_file(self):
        file_path = askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not file_path:
            return
        with open(file_path, "r") as file:
            text = file.read()
            self.txt_edit.delete(1.0, tk.END)
            self.txt_edit.insert(tk.END, text)
        self.update_status()

    def save_file(self):
        file_path = asksaveasfilename(defaultextension="txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not file_path:
            return
        with open(file_path, "w") as file:
            text = self.txt_edit.get(1.0, tk.END)
            file.write(text)
        messagebox.showinfo("Save File", "File saved successfully!")

    def show_about(self):
        about_text = (
            "Sourceduty Notepad\n"
            "\n"
            f"Copyright (C) 2024, Sourceduty - All Rights Reserved.\n"
            "\n"
            "sourceduty@gmail.com"
        )
        messagebox.showinfo("About Sourceduty Notepad", about_text)

    def show_help(self):
        help_text = "github.com/sourceduty"
        messagebox.showinfo("Help - Sourceduty Notepad", help_text)

    def on_text_change(self, event=None):
        self.txt_edit.edit_modified(False)
        self.update_status()

    def on_key_release(self, event):
        self.update_status()

    def update_status(self, event=None):
        words = len(self.txt_edit.get(1.0, 'end-1c').split())
        characters = len(self.txt_edit.get(1.0, 'end-1c'))
        mode = self.modes[self.current_mode_index]
        self.status_bar.config(text=f"Mode: {mode} | Words: {words} | Characters: {characters}")

    def undo(self):
        self.txt_edit.edit_undo()

    def redo(self):
        self.txt_edit.edit_redo()

    def cut(self):
        self.txt_edit.event_generate("<<Cut>>")

    def copy(self):
        self.txt_edit.event_generate("<<Copy>>")

    def paste(self):
        self.txt_edit.event_generate("<<Paste>>")

    def select_all(self):
        self.txt_edit.tag_add("sel", "1.0", "end")

    def find(self):
        query = simpledialog.askstring("Find", "Enter text to find:")
        if query:
            idx = "1.0"
            while True:
                idx = self.txt_edit.search(query, idx, nocase=1, stopindex="end")
                if not idx: break
                lastidx = f"{idx}+{len(query)}c"
                self.txt_edit.tag_add("sel", idx, lastidx)
                idx = lastidx
            self.txt_edit.mark_set("insert", idx)
            self.txt_edit.see(idx)

class OtherClass:
    def __init__(self, root):
        pass
    # Define other classes and methods here if needed.

def main():
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()