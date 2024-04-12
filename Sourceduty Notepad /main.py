# Sourceduty Notepad V1.2
# Copyright (C) 2023, Sourceduty 
# This software is free and open-source; anyone can redistribute it and/or modify it.

import tkinter as tk
from text_editor import TextEditor

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()
