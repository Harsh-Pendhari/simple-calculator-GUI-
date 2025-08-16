import tkinter as tk
from tkinter import font
import re

error_state = False

def button_click_handler(text):
    global error_state

    if text == 'x':
        text = "*"

    current_state = entry.get()

    if error_state and text not in ['C', '=']:
        entry.set("")
        current_state = ""
        error_state = False
    elif error_state and text == 'C':
        entry.set("")
        current_state = ""
        error_state = False

    if text == 'C':
        entry.set("")
        error_state = False

    elif text == '=':
        processed_state = current_state
        processed_state = re.sub(r'(^|(?<=[^.\d]))0+(\d+)', r'\1\2', processed_state)
        try:
            result = eval(processed_state)
            entry.set(result)
            error_state = False
        except Exception:
            entry.set("Invalid")
            error_state = True

    elif text == '%':
        try:
            result = eval(current_state) / 100
            entry.set(result)
            error_state = False
        except Exception:
            entry.set("Invalid")
            error_state = True

    elif text in '+-*/' and current_state[-1:] in '+-*/':
        return

    else:
        entry.set(current_state + text)
        error_state = False

def keyboard_handler(event):
    key = event.char
    keysym = event.keysym

    if key.isdigit() or key in ['.', '(', ')']:
        button_click_handler(key)
    elif key == '+' or key == '-' or key == '*':
        button_click_handler(key)
    elif key == '/':
        button_click_handler(key)
    elif key == 'x':
        button_click_handler('x')
    elif keysym == "Return":
        button_click_handler("=")
    elif keysym == "BackSpace":
        current_text = entry.get()
        entry.set(current_text[:-1])
    elif keysym == "space":
        button_click_handler("C")

root = tk.Tk()
root.geometry("400x550")
root.title("Simple Calculator")
root.iconbitmap(r'calculator_icon.ico')
root.resizable(False, False)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=5)
root.grid_columnconfigure(2, weight=1)

entry = tk.StringVar(value="")

live_entry = tk.Entry(root, width=20, font = font.Font(size=35), state="readonly", textvariable = entry,)
live_entry.grid(row=0, column=1, padx=20, pady=(50, 0), sticky="ew") 
# sticky="ew":  Makes the entry widget expand horizontally to fill the available space (after padding) in column 1

button_frame = tk.Frame(root) # Frame to hold BUTTONS
button_frame.grid(row=1, column=1, sticky="ew", padx=20, pady=(20,0))

# Configure columns within the button_frame for uniform button sizing (SAME AS ABOVE WHERE WE CONFIGURE THE GRID)
for i in range(4):
    button_frame.grid_columnconfigure(i, weight=1, uniform="button_group")

button_layout = [
    ["C", "(", ")", "/"],
    ["7", "8", "9", "x"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "=", "%"],
]

for row_index, row_buttons in enumerate(button_layout):
    for column_index, button_text in enumerate(row_buttons):
        button = tk.Button(
            button_frame,
            text=button_text,
            font=font.Font(size=20),
            height=1,
            command=lambda text=button_text: button_click_handler(text),
        )
        button.grid(row=row_index, column=column_index, sticky="nsew", padx=5, pady=5)

root.bind("<Key>", keyboard_handler)

root.mainloop()
