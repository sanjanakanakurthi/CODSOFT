import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable

class CalculatorGUI:
    def __init__(self, root: tk.Tk, calculator, utils):
        self.root = root
        self.calculator = calculator
        self.utils = utils
        self.setup_window()
        self.create_widgets()
        self.setup_styles()
    
    def setup_window(self):
        self.root.title("Advanced Calculator - CodSoft")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        title_label = ttk.Label(main_frame, text="Calculator", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        ttk.Label(main_frame, text="First Number:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.num1_entry = ttk.Entry(main_frame, width=20, font=('Arial', 12))
        self.num1_entry.grid(row=1, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        
        ttk.Label(main_frame, text="Second Number:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.num2_entry = ttk.Entry(main_frame, width=20, font=('Arial', 12))
        self.num2_entry.grid(row=2, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="+", command=self.add_operation, 
                  width=5).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="-", command=self.subtract_operation,
                  width=5).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="×", command=self.multiply_operation,
                  width=5).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="÷", command=self.divide_operation,
                  width=5).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Clear", command=self.clear_all,
                  width=10).grid(row=2, column=0, columnspan=2, pady=10)
        
        self.result_label = ttk.Label(main_frame, text="Result: ", 
                                     font=('Arial', 12, 'bold'))
        self.result_label.grid(row=4, column=0, columnspan=2, pady=20)
        
        history_frame = ttk.LabelFrame(main_frame, text="History", padding="5")
        history_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.history_text = tk.Text(history_frame, height=8, width=40, 
                                   font=('Courier', 10), state='disabled')
        self.history_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, 
                                 command=self.history_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.history_text.config(yscrollcommand=scrollbar.set)
        
        ttk.Button(main_frame, text="Exit", command=self.root.quit,
                  width=10).grid(row=6, column=0, columnspan=2, pady=10)
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)
    
    def setup_styles(self):
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 10, 'bold'), padding=5)
        style.configure('TLabel', font=('Arial', 10))
    
    def get_inputs(self):
        num1_str = self.num1_entry.get().strip()
        num2_str = self.num2_entry.get().strip()
        
        if not num1_str or not num2_str:
            self.utils.show_error_message("Error", "Please enter both numbers")
            return None, None
        
        try:
            num1 = self.utils.parse_input(num1_str)
            num2 = self.utils.parse_input(num2_str)
            return num1, num2
        except ValueError as e:
            self.utils.show_error_message("Error", str(e))
            return None, None
    
    def update_result(self, result):
        formatted_result = self.utils.format_result(result)
        self.result_label.config(text=f"Result: {formatted_result}")
        return formatted_result
    
    def log_operation(self, operation: str, result: str):
        self.utils.update_history(self.history_text, operation, result)
    
    def add_operation(self):
        num1, num2 = self.get_inputs()
        if num1 is not None and num2 is not None:
            try:
                result = self.calculator.add(num1, num2)
                formatted_result = self.update_result(result)
                self.log_operation(f"{num1} + {num2}", formatted_result)
            except Exception as e:
                self.utils.show_error_message("Error", str(e))
    
    def subtract_operation(self):
        num1, num2 = self.get_inputs()
        if num1 is not None and num2 is not None:
            try:
                result = self.calculator.subtract(num1, num2)
                formatted_result = self.update_result(result)
                self.log_operation(f"{num1} - {num2}", formatted_result)
            except Exception as e:
                self.utils.show_error_message("Error", str(e))
    
    def multiply_operation(self):
        num1, num2 = self.get_inputs()
        if num1 is not None and num2 is not None:
            try:
                result = self.calculator.multiply(num1, num2)
                formatted_result = self.update_result(result)
                self.log_operation(f"{num1} × {num2}", formatted_result)
            except Exception as e:
                self.utils.show_error_message("Error", str(e))
    
    def divide_operation(self):
        num1, num2 = self.get_inputs()
        if num1 is not None and num2 is not None:
            try:
                result = self.calculator.divide(num1, num2)
                formatted_result = self.update_result(result)
                self.log_operation(f"{num1} ÷ {num2}", formatted_result)
            except ZeroDivisionError:
                self.utils.show_error_message("Error", "Cannot divide by zero")
            except Exception as e:
                self.utils.show_error_message("Error", str(e))
    
    def clear_all(self):
        self.utils.clear_inputs(self.num1_entry, self.num2_entry)
        self.result_label.config(text="Result: ")
        self.history_text.config(state='normal')
        self.history_text.delete(1.0, 'end')
        self.history_text.config(state='disabled')