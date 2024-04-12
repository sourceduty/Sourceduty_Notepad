# Sourceduty Notepad V2.0
# Copyright (C) 2023, Sourceduty 
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
        self.mode = "Note Mode" 
        self.toggle_mode()
        self.update_status()

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
        for template_name in TEMPLATES:  # Access TEMPLATES from the templates module
            templates_menu.add_command(label=template_name, command=lambda name=template_name: self.insert_template(name))

        control_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Control", menu=control_menu)
        control_menu.add_command(label="Help", command=self.show_help)
        control_menu.add_command(label="About", command=self.show_about)

    def create_widgets(self):
        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.line_number_bar = tk.Text(self.root, width=4, padx=3, takefocus=0, border=0,
                                   background='orange', state='disabled', wrap='none')
        self.line_number_bar.grid(row=0, column=0, sticky='nsew')

        self.txt_edit = tk.Text(self.root, yscrollcommand=self.scroll_text)
        self.txt_edit.grid(row=0, column=2, sticky="nsew")

        self.scrollbar.config(command=self.txt_edit.yview)
        self.txt_edit.config(yscrollcommand=self.scrollbar.set)

        self.status_bar = tk.Label(self.root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=1, column=0, columnspan=3, sticky="ew")

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(2, weight=1)

        self.txt_edit.bind("<MouseWheel>", self.on_mouse_wheel)
        self.line_number_bar.bind("<MouseWheel>", self.on_mouse_wheel)
        self.txt_edit.bind("<Key>", self.on_key_event)
        self.txt_edit.bind("<Configure>", self.update_line_numbers)

    def on_mouse_wheel(self, event):
        self.line_number_bar.yview_scroll(-1*(event.delta//120), "units")
        self.txt_edit.yview_scroll(-1*(event.delta//120), "units")
        return "break"


    def on_key_event(self, event):
        self.update_line_numbers()
        self.update_status()

    def update_line_numbers(self, event=None):
        self.line_number_bar.config(state='normal')
        self.line_number_bar.delete('1.0', 'end')
        lines = self.txt_edit.get(1.0, "end-1c").count('\n') + 1
        line_numbers = '\n'.join(str(i) for i in range(1, lines+1))
        self.line_number_bar.insert('1.0', line_numbers)
        self.line_number_bar.config(state='disabled')

    def scroll_text(self, *args):
        self.line_number_bar.yview_moveto(args[0])
        self.txt_edit.yview_moveto(args[0])

    def insert_template(self, template_name):
        template = TEMPLATES.get(template_name, "")
        self.txt_edit.insert(tk.END, template)
        self.update_status()
        self.txt_edit.see(tk.END)

    def toggle_mode(self):
        self.mode = "Note Mode" if self.mode == "Dev Mode" else "Dev Mode"
        self.update_editor_appearance()
        self.update_status()

    def update_editor_appearance(self):
        if self.mode == "Dev Mode":
            self.txt_edit.config(bg='black', fg='white', insertbackground='white')
            self.line_number_bar.config(bg='blue', fg='white')
            self.line_number_bar.config(state='normal')  # Enable line numbering
            self.update_line_numbers()
        else:
            self.txt_edit.config(bg='white', fg='black', insertbackground='black')
            self.line_number_bar.config(bg='orange', fg='black')
            self.line_number_bar.config(state='disabled')  # Disable line numbering

    def new_file(self):
        self.txt_edit.delete(1.0, tk.END)
        self.line_number_bar.delete(1.0, tk.END)
        self.line_number_bar.insert(tk.END, "1")
        self.root.title("Sourceduty Notepad - New File")
        self.update_status()

    def open_file(self):
        filepath = askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not filepath:
            return
        try:
            self.txt_edit.delete(1.0, tk.END)
            self.line_number_bar.delete(1.0, tk.END)
            self.line_number_bar.insert(tk.END, "1")
            with open(filepath, "r") as input_file:
                text = input_file.read()
                self.txt_edit.insert(tk.END, text)
                self.update_line_numbers()
            self.root.title(f"Sourceduty Notepad - {filepath}")
        except Exception as e:
            messagebox.showerror("Open File", f"Failed to open file: {e}")
        self.update_status()

    def save_file(self):
        filepath = asksaveasfilename(
            defaultextension="txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        try:
            with open(filepath, "w") as output_file:
                text = self.txt_edit.get(1.0, tk.END)
                output_file.write(text)
            self.root.title(f"Sourceduty Notepad - {filepath}")
        except Exception as e:
            messagebox.showerror("Save File", f"Failed to save file: {e}")

    def show_about(self):
        about_text = (
            "Sourceduty Notepad\n"
            "\n"
            f"Copyright (C) 2023, Sourceduty - All Rights Reserved.\n"
            "\n"
            "sourceduty@gmail.com"
        )
        messagebox.showinfo("About Sourceduty Notepad", about_text)

    def show_help(self):
        help_text = "github.com/sourceduty"
        messagebox.showinfo("Help - Sourceduty Notepad", help_text)

    def on_key_press(self, event):
        self.update_line_numbers()


    def on_key_release(self, event):
        self.update_status()

    def get_line_numbers(self):
        text = self.txt_edit.get(1.0, "end-1c")
        lines = text.split("\n")
        line_numbers = "\n".join(str(i) for i in range(1, len(lines) + 1))
        return line_numbers

    def update_line_numbers(self):
        line_numbers = self.get_line_numbers()
        self.line_number_bar.config(state='normal')
        self.line_number_bar.delete('1.0', 'end')
        self.line_number_bar.insert('1.0', line_numbers)
        self.line_number_bar.config(state='disabled')

    def update_status(self, event=None):
        words = len(self.txt_edit.get(1.0, 'end-1c').split())
        characters = len(self.txt_edit.get(1.0, 'end-1c'))
        self.status_bar.config(text=f"Mode: {self.mode} | Words: {words} | Characters: {characters}")

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
