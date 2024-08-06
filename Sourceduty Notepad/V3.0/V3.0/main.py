# Sourceduty Notepad V3.0
# Copyright (C) 2024, Sourceduty 
# This software is free and open-source; anyone can redistribute it and/or modify it.

import tkinter as tk
from text_editor import TextEditor

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()
