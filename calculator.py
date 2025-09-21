
import math
from typing import Union

class CalculationResult:
    def __init__(self, value=0, operation='', operands=None, expression='', error=''):
        self.value = value
        self.operation = operation
        self.operands = operands if operands is not None else []
        self.expression = expression
        self.error = error

class BasicCalculator:
    def __init__(self):
        self.history = CalculationHistory()

class CalculationHistory:
    def __init__(self):
        self.records = []
    def add_calculation(self, expression, result, operation, operands):
        self.records.append({
            "expression": expression,
            "result": result,
            "operation": operation,
            "operands": operands
        })

class ScientificCalculator(BasicCalculator):
    def __init__(self):
        super().__init__()
        self.math_constants = {
            'pi': math.pi,
            'e': math.e,
            'phi': (1 + math.sqrt(5)) / 2
        }

    def square_root(self, value: Union[int, float]) -> CalculationResult:
        try:
            if value < 0:
                raise ValueError("Square root of negative number")
            result = math.sqrt(float(value))
            expression = f"√{value}"
            self.history.add_calculation(expression, result, '√', [value])
            return CalculationResult(result, '√', [value], expression)
        except ValueError as e:
            return CalculationResult(0, '√', [value], error=str(e))

    def power(self, base: Union[int, float], exponent: Union[int, float]) -> CalculationResult:
        try:
            result = math.pow(float(base), float(exponent))
            expression = f"{base}^{exponent}"
            self.history.add_calculation(expression, result, '^', [base, exponent])
            return CalculationResult(result, '^', [base, exponent], expression)
        except Exception as e:
            return CalculationResult(0, '^', [base, exponent], error=str(e))

    def logarithm(self, value: Union[int, float], base: float = 10) -> CalculationResult:
        try:
            if value <= 0:
                raise ValueError("Logarithm of non-positive number")
            if base <= 0 or base == 1:
                raise ValueError("Invalid logarithm base")
            result = math.log(float(value), base)
            expression = f"log_{base}({value})"
            self.history.add_calculation(expression, result, 'log', [value, base])
            return CalculationResult(result, 'log', [value, base], expression)
        except ValueError as e:
            return CalculationResult(0, 'log', [value, base], error=str(e))

    def sine(self, angle: Union[int, float]) -> CalculationResult:
        try:
            result = math.sin(math.radians(float(angle)))
            expression = f"sin({angle}°)"
            self.history.add_calculation(expression, result, 'sin', [angle])
            return CalculationResult(result, 'sin', [angle], expression)
        except Exception as e:
            return CalculationResult(0, 'sin', [angle], error=str(e))

    def cosine(self, angle: Union[int, float]) -> CalculationResult:
        try:
            result = math.cos(math.radians(float(angle)))
            expression = f"cos({angle}°)"
            self.history.add_calculation(expression, result, 'cos', [angle])
            return CalculationResult(result, 'cos', [angle], expression)
        except Exception as e:
            return CalculationResult(0, 'cos', [angle], error=str(e))

    def get_constant(self, name: str) -> CalculationResult:
        if name in self.math_constants:
            value = self.math_constants[name]
            expression = f"constant({name})"
            self.history.add_calculation(expression, value, 'const', [value])
            return CalculationResult(value, 'const', [value], expression)
        return CalculationResult(0, 'const', [], error=f"Unknown constant: {name}")

    def factorial(self, n: Union[int, float]) -> CalculationResult:
        try:
            n_int = int(float(n))
            if n_int < 0:
                raise ValueError("Factorial not defined for negative numbers")
            if n_int > 20:
                raise ValueError("Factorial too large for computation (max 20!)")
            result = math.factorial(n_int)
            expression = f"{n_int}!"
            self.history.add_calculation(expression, result, '!', [n_int])
            return CalculationResult(result, '!', [n_int], expression)
        except (ValueError, TypeError) as e:
            operand = [float(n)] if isinstance(n, (int, float)) else []
            return CalculationResult(0, '!', operand, error=str(e))
        except Exception as e:
            return CalculationResult(0, '!', error=f"Factorial calculation failed: {str(e)}")

def perform_operation(calculator, operation, args):
    if operation in ['sqrt', 'sin', 'cos', 'log', 'fact']:
        if len(args) != 1 and operation != 'log':
            return CalculationResult(error=f"{operation} requires exactly 1 operand")
        if operation == 'log':
            if len(args) == 1:
                args = [args[0], 10]
            elif len(args) != 2:
                return CalculationResult(error="log requires 1 or 2 operands")
        if operation == 'fact':
            try:
                args = [int(float(args[0]))]
            except (ValueError, TypeError):
                return CalculationResult(error="Factorial requires a valid integer input")
        if not hasattr(calculator, operation if operation != 'fact' else 'factorial'):
            return CalculationResult(error=f"Operation {operation} not supported")
        method = getattr(calculator, operation if operation != 'fact' else 'factorial')
        result = method(*args)
        return result
    return CalculationResult(error=f"Operation {operation} not supported")
