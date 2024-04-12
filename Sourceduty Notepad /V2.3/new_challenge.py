# Sourceduty Notepad V2.4
# Copyright (C) 2024, Sourceduty 

def new_challenge(self):
    challenges = [
        "Write a short story about a character facing their greatest fear.",
        "Describe a scene from an imaginary world with vivid detail.",
        "Create a dialogue between two characters who have just met."
        # Add more challenges as needed
    ]
    challenge_text = random.choice(challenges)
    self.txt_edit.insert(tk.END, "\n\n" + challenge_text + "\n\n")
    self.update_status()
