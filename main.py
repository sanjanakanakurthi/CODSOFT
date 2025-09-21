
import sys
import os
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import math
import re

BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR / "src"))

class Calculator:
    def __init__(self):
        self.history = []
        self.memory = 0
        self.previous_result = 0
    
    def calculate(self, expression):
        if not expression or expression.strip() == "":
            return "0"
        
        try:
            cleaned = self._clean_expression(expression)
            
            if self._is_simple_number(cleaned):
                result = float(cleaned)
                formatted = self._format_number(result)
                self.history.append(f"{expression}={formatted}")
                return formatted
            
            result = eval(cleaned, {"__builtins__": None, "math": math}, {})
            
            if isinstance(result, (int, float)):
                formatted = self._format_number(result)
                self.history.append(f"{expression}={formatted}")
                self.previous_result = result
                return formatted
            else:
                self.history.append(f"{expression}={str(result)}")
                return str(result)
                
        except ZeroDivisionError:
            raise ValueError("Division by zero")
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")
    
    def memory_add(self, value):
        try:
            self.memory += float(value)
        except ValueError:
            pass
    
    def memory_subtract(self, value):
        try:
            self.memory -= float(value)
        except ValueError:
            pass
    
    def memory_recall(self):
        return self._format_number(self.memory)
    
    def memory_clear(self):
        self.memory = 0
    
    def _clean_expression(self, expr):
        expr = re.sub(r'×', '*', expr)
        expr = re.sub(r'÷', '/', expr)
        expr = re.sub(r'\s+', '', expr)
        expr = re.sub(r'[^0-9+\-*/().]', '', expr)
        return expr
    
    def _is_simple_number(self, expr):
        pattern = r'^[+-]?(\d+(\.\d*)?|\.\d+)$'
        return re.match(pattern, expr) is not None
    
    def _format_number(self, num):
        if num == float('inf'):
            return "∞"
        if num == float('-inf'):
            return "-∞"
        if math.isnan(num):
            return "NaN"
        
        if abs(num) > 1e15:
            return f"{num:.8g}"
        if abs(num) < 1e-10 and num != 0:
            return f"{num:.8g}"
        
        if isinstance(num, float) and num.is_integer():
            return str(int(num))
        
        formatted = f"{num:.10f}".rstrip('0').rstrip('.')
        return formatted if formatted else "0"

class CalculatorGUI:
    def __init__(self, parent, calculator, utils):
        self.root = parent
        self.calculator = calculator
        self.utils = utils
        self.expression = ""
        self.decimal_added = False
        self.display_var = tk.StringVar(value="0")
        self.setup_ui()
        self.setup_keyboard_bindings()
    
    def setup_ui(self):
        self.root.title("Scientific Calculator")
        self.root.geometry("320x450")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.display = tk.Entry(self.root, textvariable=self.display_var, 
                               font=("Arial", 16, "bold"), justify="right", 
                               state="readonly", bg="white", fg="black",
                               relief="solid", borderwidth=2,
                               insertwidth=0)
        self.display.grid(row=0, column=0, columnspan=5, padx=5, pady=10, sticky="ew")
        
        button_configs = {
            'normal': {'bg': '#e0e0e0', 'fg': 'black', 'activebackground': '#d0d0d0'},
            'operator': {'bg': '#ff9500', 'fg': 'white', 'activebackground': '#e68900'},
            'function': {'bg': '#a6a6a6', 'fg': 'white', 'activebackground': '#8c8c8c'},
            'zero': {'bg': '#f0f0f0', 'fg': 'black', 'activebackground': '#e0e0e0'},
            'equals': {'bg': '#ff9500', 'fg': 'white', 'activebackground': '#e68900', 'font': ("Arial", 14, "bold")}
        }
        
        buttons = [
            ('MC', 1, 0, 'function'), ('MR', 1, 1, 'function'), ('M+', 1, 2, 'function'), ('M-', 1, 3, 'function'), ('C', 1, 4, 'function'),
            ('±', 2, 0, 'normal'), ('√', 2, 1, 'function'), ('%', 2, 2, 'normal'), ('÷', 2, 3, 'operator'), ('×', 2, 4, 'operator'),
            ('7', 3, 0, 'normal'), ('8', 3, 1, 'normal'), ('9', 3, 2, 'normal'), ('-', 3, 3, 'operator'), ('+', 3, 4, 'operator'),
            ('4', 4, 0, 'normal'), ('5', 4, 1, 'normal'), ('6', 4, 2, 'normal'), 
            ('1', 5, 0, 'normal'), ('2', 5, 1, 'normal'), ('3', 5, 2, 'normal'), 
            ('0', 6, 0, 'zero'), ('.', 6, 2, 'normal')
        ]
        
        for text, row, col, btn_type in buttons:
            if text == '0':
                btn = tk.Button(self.root, text=text, font=("Arial", 14),
                               command=lambda t=text: self.button_click(t),
                               **button_configs[btn_type], width=10, height=2)
                btn.grid(row=row, column=col, columnspan=2, padx=2, pady=2, sticky="nsew")
            else:
                config = button_configs[btn_type].copy()
                if btn_type == 'equals':
                    config['font'] = ("Arial", 14, "bold")
                btn = tk.Button(self.root, text=text, font=("Arial", 14),
                               command=lambda t=text: self.button_click(t),
                               **config, width=6, height=2)
                btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
        
        equals_btn = tk.Button(self.root, text='=', font=("Arial", 14, "bold"),
                              command=lambda: self.button_click('='),
                              bg="#ff9500", fg="white", activebackground="#e68900",
                              width=6, height=3)
        equals_btn.grid(row=4, column=3, rowspan=3, columnspan=2, padx=2, pady=2, sticky="nsew")
        
        for i in range(7):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)
    
    def setup_keyboard_bindings(self):
        self.root.bind('<Key>', self.on_key_press)
        self.root.focus_set()
    
    def on_key_press(self, event):
        key = event.char
        if key.isdigit():
            self.button_click(key)
        elif key in ['+', '-', '*', '/', '.']:
            op_map = {'*': '×', '/': '÷'}
            self.button_click(op_map.get(key, key))
        elif event.keysym in ['Return', 'KP_Enter']:
            self.button_click('=')
        elif key.lower() == 'c' or event.keysym == 'Escape':
            self.button_click('C')
        elif event.keysym == 'BackSpace':
            self.button_click('⌫')
    
    def button_click(self, char):
        try:
            if char == 'C':
                self.clear_all()
            elif char == '⌫':
                self.backspace()
            elif char == 'MC':
                self.calculator.memory_clear()
                self.display_var.set("0")
                self.expression = ""
            elif char == 'MR':
                result = self.calculator.memory_recall()
                if self.expression == "0" or self.expression == "":
                    self.expression = result
                else:
                    self.expression += result
                self.display_var.set(self.expression)
            elif char == 'M+':
                val = self.evaluate_expression(self.expression)
                if val is not None:
                    self.calculator.memory_add(val)
                    self.display_var.set(f"M={self.calculator.memory_recall()}")
                    self.root.after(1000, lambda: self.display_var.set(self.expression))
            elif char == 'M-':
                val = self.evaluate_expression(self.expression)
                if val is not None:
                    self.calculator.memory_subtract(val)
                    self.display_var.set(f"M={self.calculator.memory_recall()}")
                    self.root.after(1000, lambda: self.display_var.set(self.expression))
            elif char == '±':
                if self.expression and self.expression[-1].isdigit():
                    # Try to toggle sign of the last number in the expression
                    self.toggle_sign_in_expression()
                elif self.expression == "":
                    self.expression = "-"
                    self.display_var.set(self.expression)
                else:
                    pass
            elif char == '%':
                self.apply_percentage()
            elif char == '√':
                self.apply_square_root()
            elif char in ['÷', '×', '+', '-']:
                if self.expression == "" and char == '-':
                    self.expression = '-'
                    self.display_var.set(self.expression)
                else:
                    if self.expression and self.expression[-1] in '+-×÷':
                        self.expression = self.expression[:-1] + char
                    else:
                        self.expression += char
                    self.display_var.set(self.expression)
                self.decimal_added = False
            elif char == '.':
                if not self.decimal_added:
                    if self.expression == "" or self.expression[-1] in '+-×÷':
                        self.expression += '0.'
                    else:
                        self.expression += '.'
                    self.display_var.set(self.expression)
                    self.decimal_added = True
            elif char.isdigit():
                self.expression += char
                self.display_var.set(self.expression)
            elif char == '=':
                self.perform_calculation()
        except Exception as e:
            self.utils['show_error_message'](self.root, f"Error: {str(e)}")
            self.clear_all()
    
    def clear_all(self):
        self.expression = ""
        self.decimal_added = False
        self.display_var.set("0")
    
    def backspace(self):
        if not self.expression:
            self.display_var.set("0")
            return
        removed = self.expression[-1]
        self.expression = self.expression[:-1]
        if removed == '.':
            self.decimal_added = False
        elif removed in '+-×÷':
            # reset decimal_added based on last number
            last_num = re.findall(r'(\d*\.\d*|\d+)', self.expression)
            self.decimal_added = '.' in last_num[-1] if last_num else False
        if self.expression == "":
            self.display_var.set("0")
        else:
            self.display_var.set(self.expression)
    
    def toggle_sign_in_expression(self):
        # Toggle the sign of the last number in the expression
        # Find last number with regex
        parts = re.split(r'([+\-×÷])', self.expression)
        if not parts:
            return
        last_num = parts[-1]
        if last_num == "":
            return
        if last_num.startswith('-'):
            parts[-1] = last_num[1:]
        else:
            parts[-1] = '-' + last_num
        self.expression = ''.join(parts)
        self.display_var.set(self.expression)
    
    def apply_percentage(self):
        # Apply percentage to the last number in expression
        # Find last number with regex
        parts = re.split(r'([+\-×÷])', self.expression)
        if not parts or parts[-1] == "":
            return
        try:
            last_num = parts[-1]
            val = float(last_num)
            val = val / 100
            parts[-1] = self.calculator._format_number(val)
            self.expression = ''.join(parts)
            self.display_var.set(self.expression)
        except ValueError:
            pass
    
    def apply_square_root(self):
        # Apply sqrt to the last number in expression
        parts = re.split(r'([+\-×÷])', self.expression)
        if not parts or parts[-1] == "":
            return
        try:
            last_num = parts[-1]
            val = float(last_num)
            if val < 0:
                raise ValueError("Cannot calculate square root of negative number")
            res = math.sqrt(val)
            parts[-1] = self.calculator._format_number(res)
            self.expression = ''.join(parts)
            self.display_var.set(self.expression)
        except ValueError as e:
            self.utils['show_error_message'](self.root, str(e))
    
    def evaluate_expression(self, expr):
        cleaned = self.calculator._clean_expression(expr)
        try:
            result = eval(cleaned, {"__builtins__": None, "math": math}, {})
            if isinstance(result, (int, float)):
                return result
            return None
        except:
            return None
    
    def perform_calculation(self):
        if not self.expression or self.expression[-1] in '+-×÷':
            self.utils['show_error_message'](self.root, "Incomplete expression")
            return
        try:
            result = self.evaluate_expression(self.expression)
            if result is not None:
                formatted = self.calculator._format_number(result)
                self.calculator.history.append(f"{self.expression}={formatted}")
                self.expression = formatted
                self.display_var.set(formatted)
                self.decimal_added = '.' in formatted
            else:
                self.utils['show_error_message'](self.root, "Error in calculation")
        except Exception as e:
            self.utils['show_error_message'](self.root, f"Calculation error: {str(e)}")
            self.clear_all()

def validate_numeric_input(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def format_result(result):
    try:
        if isinstance(result, str):
            num = float(result)
        else:
            num = result
        
        if num.is_integer():
            return str(int(num))
        if abs(num) > 1e12:
            return f"{num:.2e}"
        return f"{num:.10g}"
    except (ValueError, AttributeError):
        return str(result)

def parse_input(expression):
    if not expression:
        return ""
    cleaned = re.sub(r'[×]', '*', expression)
    cleaned = re.sub(r'[÷]', '/', cleaned)
    cleaned = re.sub(r'\s+', '', cleaned)
    return cleaned.strip()

def show_error_message(parent, message):
    try:
        messagebox.showerror("Calculator Error", message, parent=parent)
    except:
        print(f"Error: {message}")

def clear_inputs(parent):
    pass

def update_history(history_listbox, history):
    if history_listbox:
        history_listbox.delete(0, tk.END)
        for item in history[-20:]:
            history_listbox.insert(tk.END, item)

def show_history_window(calculator_gui):
    history_window = tk.Toplevel(calculator_gui.root)
    history_window.title("Calculation History")
    history_window.geometry("500x400")
    history_window.resizable(True, True)
    
    listbox = tk.Listbox(history_window, font=("Arial", 10))
    listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    update_history(listbox, calculator_gui.calculator.history)
    
    scrollbar = tk.Scrollbar(history_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    
    button_frame = tk.Frame(history_window)
    button_frame.pack(pady=10)
    
    clear_btn = tk.Button(button_frame, text="Clear History", 
                         command=lambda: clear_calculator_history(calculator_gui, listbox))
    clear_btn.pack(side=tk.LEFT, padx=5)
    
    close_btn = tk.Button(button_frame, text="Close", 
                         command=history_window.destroy)
    close_btn.pack(side=tk.LEFT, padx=5)

def clear_calculator_history(calculator_gui, listbox):
    calculator_gui.calculator.history.clear()
    update_history(listbox, calculator_gui.calculator.history)

def main():
    try:
        root = tk.Tk()
        calculator = Calculator()
        utils = {
            'validate_numeric_input': validate_numeric_input,
            'format_result': format_result,
            'parse_input': parse_input,
            'show_error_message': show_error_message,
            'clear_inputs': clear_inputs,
            'update_history': update_history
        }
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Show History", 
                             command=lambda: show_history_window(app))
        app = CalculatorGUI(root, calculator, utils)
        root.mainloop()
    except Exception as e:
        print(f"Application Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
