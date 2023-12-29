# Sourceduty Notepad V1.0
# Copyright (C) 2023, Sourceduty 
# This software is free and open-source; anyone can redistribute it and/or modify it.

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox

class TextEditor:
    TEMPLATES = {
        "Book Index": (
            "CONTENTS\n\n"
            "Chapter 1 ............................... 1\n"
            "Chapter 2 ............................... 14\n"
            "Chapter 3 ............................... 23\n"
            "Chapter 4 ............................... 43\n"
            "Chapter 5 ............................... 56\n"
            "Chapter 6 ............................... 75\n"
            "Chapter 7 ............................... 78\n"
            "Chapter 8 ............................... 92\n"
            "Chapter 9 ............................... 101\n"
        ),
        "Invoice": (
            "Invoice\n"
            "------------------------------------\n"
            "Item Description      Quantity    Price\n"
            "------------------------------------\n"
            "Widget A                10       $2.99\n"
            "Widget B                5        $3.99\n"
            "------------------------------------\n"
            "Total:                             $49.85\n"
        ),
        "Instructions": (
            "Instructions for Building a Bookshelf\n"
            "-------------------------------------\n"
            "1. Gather all materials and tools.\n"
            "2. Assemble the sides, top, and bottom.\n"
            "3. Attach the back panel.\n"
            "4. Insert the shelves.\n"
            "5. Sand and finish as desired.\n"
        ),
        "Recipe": (
            "Recipe: Chocolate Chip Cookies\n"
            "Ingredients:\n"
            "- 2 1/4 cups all-purpose flour\n"
            "- 1/2 tsp baking soda\n"
            "- 1 cup unsalted butter, room temperature\n"
            "- 1/2 cup granulated sugar\n"
            "- 1 cup packed light-brown sugar\n"
            "- 1 tsp salt\n"
            "- 2 tsp pure vanilla extract\n"
            "- 2 large eggs\n"
            "- 2 cups semisweet and/or milk chocolate chips\n"
            "Instructions:\n"
            "- Preheat oven to 350 degrees.\n"
            "- In a small bowl, whisk together the flour and baking soda; set aside.\n"
            "- Combine the butter with both sugars; beat on medium speed until light and fluffy.\n"
            "- Reduce speed to low; add the salt, vanilla, and eggs. Beat until well mixed.\n"
            "- Add the flour mixture; mix until just combined.\n"
            "- Stir in the chocolate chips.\n"
            "- Drop heaping tablespoon-size balls of dough about 2 inches apart on baking sheets.\n"
            "- Bake until cookies are golden around the edges but still soft in the center, 8 to 10 minutes.\n"
            "- Remove from oven, and let cool on baking sheet 1 to 2 minutes.\n"
            "- Transfer to a wire rack, and let cool completely.\n"
        ),
        "Project Plan": (
            "| Task            | Jan | Feb | Mar | Apr | May | Jun |\n"
            "|-----------------|-----|-----|-----|-----|-----|-----|\n"
            "| Research        | ### | ### |     |     |     |     |\n"
            "| Design          |     | ### | ### |     |     |     |\n"
            "| Development     |     |     | ### | ### | ### |     |\n"
            "| Testing         |     |     |     |     | ### | ### |\n"
            "| Implementation  |     |     |     |     |     | ### |\n"
        ),
        "Grid Template": (
            "+--+--+--+--+--+\n"
            "|  |  |  |  |  |\n"
            "+--+--+--+--+--+\n"
            "|  |  |  |  |  |\n"
            "+--+--+--+--+--+\n"
            "|  |  |  |  |  |\n"
            "+--+--+--+--+--+\n"
            "|  |  |  |  |  |\n"
            "+--+--+--+--+--+\n"
        ),
        "Meeting Agenda": "Meeting Agenda:\n- Topic 1\n- Topic 2\n- Conclusion\n",
        "Business Letter": "Business Letter:\nDear [Name],\n\n[Body]\n\nSincerely,\n[Your Name]\n",
        "Shopping List": "Shopping List:\n- Item 1\n- Item 2\n- Item 3\n",
        "To-Do List": "To-Do List:\n- Task 1\n- Task 2\n- Task 3\n",
        "Event Invitation": "Event Invitation:\nYou are invited to [Event Name] on [Date] at [Location].\n",
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Sourceduty Notepad V1.0")
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

        mode_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Mode", menu=mode_menu)
        mode_menu.add_command(label="Toggle Mode", command=self.toggle_mode)

        templates_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Templates", menu=templates_menu)
        for template_name in self.TEMPLATES:
            templates_menu.add_command(label=template_name, command=lambda name=template_name: self.insert_template(name))

        control_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Control", menu=control_menu)
        control_menu.add_command(label="Help", command=self.show_help)
        control_menu.add_command(label="About", command=self.show_about)

    def create_widgets(self):
        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.line_number_bar = tk.Text(self.root, width=4, padx=3, takefocus=0, border=0,
                                       background='orange', state='disabled', wrap='none', yscrollcommand=self.scroll_text)
        self.line_number_bar.grid(row=0, column=0, sticky='nsew')

        self.txt_edit = tk.Text(self.root, yscrollcommand=self.scroll_text)
        self.txt_edit.grid(row=0, column=2, sticky="nsew")

        self.scrollbar.config(command=self.txt_edit.yview)
        self.txt_edit.config(yscrollcommand=self.scrollbar.set)

        self.status_bar = tk.Label(self.root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=1, column=0, columnspan=3, sticky="ew")

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(2, weight=1)

        self.txt_edit.bind("<Key>", self.on_key_press)
        self.txt_edit.bind("<KeyRelease>", self.on_key_release)

    def scroll_text(self, *args):
        self.txt_edit.yview_moveto(args[0])
        self.line_number_bar.yview_moveto(args[0])

    def insert_template(self, template_name):
        template = self.TEMPLATES.get(template_name, "")
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
        self.root.title("Sourceduty Notepad V1.0 - New File")
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
            self.root.title(f"Sourceduty Notepad V1.0 - {filepath}")
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
            self.root.title(f"Sourceduty Notepad V1.0 - {filepath}")
        except Exception as e:
            messagebox.showerror("Save File", f"Failed to save file: {e}")

    def show_about(self):
        about_text = (
            "Sourceduty Notepad V1.0\n"
            "\n"
            f"Copyright (C) 2024, Sourceduty - All Rights Reserved.\n"
            "\n"
            "sourceduty@gmail.com"
        )
        messagebox.showinfo("About Sourceduty Notepad V1.0", about_text)

    def show_help(self):
        help_text = "github.com/sourceduty"
        messagebox.showinfo("Help - Sourceduty Notepad V1.0", help_text)

    def on_key_press(self, event):
        self.update_line_numbers()
        self.scroll_text("1.0")

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

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()
