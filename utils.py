import re
from typing import Union

def validate_numeric_input(value: str) -> bool:
    pattern = r'^-?\d*\.?\d+$'
    return bool(re.match(pattern, value))

def format_result(value: Union[int, float]) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)

def parse_input(value: str) -> Union[int, float]:
    if not validate_numeric_input(value):
        raise ValueError("Invalid numeric input")
    return float(value)

def show_error_message(title: str, message: str):
    from tkinter import messagebox
    messagebox.showerror(title, message)

def clear_inputs(num1_entry, num2_entry):
    num1_entry.delete(0, 'end')
    num2_entry.delete(0, 'end')

def update_history(history_text, operation: str, result: str):
    timestamp = f"{operation} = {result}"
    history_text.insert('end', f"{timestamp}\n")
    history_text.see('end')