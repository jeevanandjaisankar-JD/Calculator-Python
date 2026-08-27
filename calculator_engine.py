"""
Core Calculation Engine for the Scientific Calculator.
Provides safe AST-based mathematical evaluation, scientific functions,
degree/radian mode support, memory bank, and calculation history.
"""

import ast
import math
import operator
from typing import Any, Dict, List, Optional, Tuple, Union


class CalculatorError(Exception):
    """Base exception for calculator errors."""
    pass


class CalculatorEngine:
    """Safe mathematical calculation engine with scientific features."""

    def __init__(self):
        self.angle_mode: str = "DEG"  # "DEG" or "RAD"
        self.memory: float = 0.0
        self.memory_active: bool = False
        self.history: List[Dict[str, str]] = []
        self._max_history: int = 50

    # ------------------------------------------------------------------
    # Angle Mode
    # ------------------------------------------------------------------
    def set_angle_mode(self, mode: str) -> str:
        mode = mode.upper()
        if mode in ("DEG", "RAD"):
            self.angle_mode = mode
        return self.angle_mode

    def toggle_angle_mode(self) -> str:
        self.angle_mode = "RAD" if self.angle_mode == "DEG" else "DEG"
        return self.angle_mode

    # ------------------------------------------------------------------
    # Memory Operations
    # ------------------------------------------------------------------
    def memory_clear(self) -> None:
        self.memory = 0.0
        self.memory_active = False

    def memory_recall(self) -> float:
        return self.memory

    def memory_store(self, value: float) -> None:
        self.memory = float(value)
        self.memory_active = True

    def memory_add(self, value: float) -> None:
        self.memory += float(value)
        self.memory_active = True

    def memory_subtract(self, value: float) -> None:
        self.memory -= float(value)
        self.memory_active = True

    # ------------------------------------------------------------------
    # History Operations
    # ------------------------------------------------------------------
    def add_history(self, expression: str, result: str) -> None:
        self.history.append({"expression": expression, "result": result})
        if len(self.history) > self._max_history:
            self.history.pop(0)

    def get_history(self) -> List[Dict[str, str]]:
        return list(reversed(self.history))

    def clear_history(self) -> None:
        self.history.clear()

    # ------------------------------------------------------------------
    # Scientific & Helper Math Functions
    # ------------------------------------------------------------------
    def _sin(self, x: float) -> float:
        rad = math.radians(x) if self.angle_mode == "DEG" else x
        val = math.sin(rad)
        return 0.0 if abs(val) < 1e-15 else val

    def _cos(self, x: float) -> float:
        rad = math.radians(x) if self.angle_mode == "DEG" else x
        val = math.cos(rad)
        return 0.0 if abs(val) < 1e-15 else val

    def _tan(self, x: float) -> float:
        rad = math.radians(x) if self.angle_mode == "DEG" else x
        cos_val = math.cos(rad)
        if abs(cos_val) < 1e-15:
            raise CalculatorError("Error: Tangent is undefined at this angle")
        val = math.tan(rad)
        return 0.0 if abs(val) < 1e-15 else val

    def _asin(self, x: float) -> float:
        if not -1.0 <= x <= 1.0:
            raise CalculatorError("Error: Domain error for asin (input must be between -1 and 1)")
        rad = math.asin(x)
        return math.degrees(rad) if self.angle_mode == "DEG" else rad

    def _acos(self, x: float) -> float:
        if not -1.0 <= x <= 1.0:
            raise CalculatorError("Error: Domain error for acos (input must be between -1 and 1)")
        rad = math.acos(x)
        return math.degrees(rad) if self.angle_mode == "DEG" else rad

    def _atan(self, x: float) -> float:
        rad = math.atan(x)
        return math.degrees(rad) if self.angle_mode == "DEG" else rad

    def _sqrt(self, x: float) -> float:
        if x < 0:
            raise CalculatorError("Error: Cannot calculate square root of a negative number")
        return math.sqrt(x)

    def _cbrt(self, x: float) -> float:
        return math.cbrt(x) if hasattr(math, 'cbrt') else (math.copysign(abs(x) ** (1 / 3), x))

    def _log10(self, x: float) -> float:
        if x <= 0:
            raise CalculatorError("Error: Logarithm only defined for positive numbers")
        return math.log10(x)

    def _ln(self, x: float) -> float:
        if x <= 0:
            raise CalculatorError("Error: Natural logarithm only defined for positive numbers")
        return math.log(x)

    def _log2(self, x: float) -> float:
        if x <= 0:
            raise CalculatorError("Error: Logarithm only defined for positive numbers")
        return math.log2(x)

    def _factorial(self, x: float) -> int:
        if x < 0:
            raise CalculatorError("Error: Factorial requires a non-negative number")
        if not float(x).is_integer():
            raise CalculatorError("Error: Factorial requires an integer")
        if x > 1000:
            raise CalculatorError("Error: Factorial input too large")
        return math.factorial(int(x))

    def _reciprocal(self, x: float) -> float:
        if x == 0:
            raise CalculatorError("Error: Division by zero")
        return 1.0 / x

    def _percentage(self, x: float) -> float:
        return x / 100.0

    # ------------------------------------------------------------------
    # Safe Expression Evaluation (AST)
    # ------------------------------------------------------------------
    def _get_allowed_functions(self) -> Dict[str, Any]:
        return {
            "sin": self._sin,
            "cos": self._cos,
            "tan": self._tan,
            "asin": self._asin,
            "acos": self._acos,
            "atan": self._atan,
            "sqrt": self._sqrt,
            "cbrt": self._cbrt,
            "log": self._log10,
            "log10": self._log10,
            "ln": self._ln,
            "log2": self._log2,
            "fact": self._factorial,
            "factorial": self._factorial,
            "abs": abs,
            "exp": math.exp,
            "floor": math.floor,
            "ceil": math.ceil,
            "rad": math.radians,
            "deg": math.degrees,
        }

    def _get_allowed_constants(self) -> Dict[str, float]:
        last_res = 0.0
        if self.history:
            last_item = self.history[-1]["result"]
            if self._is_float(last_item):
                last_res = float(last_item)
        return {
            "pi": math.pi,
            "π": math.pi,
            "e": math.e,
            "tau": math.tau if hasattr(math, 'tau') else 2 * math.pi,
            "ans": last_res,
        }

    @staticmethod
    def _is_float(val: Any) -> bool:
        try:
            float(val)
            return True
        except (ValueError, TypeError):
            return False

    def sanitize_expression(self, expr: str) -> str:
        """Pre-processes symbols and aliases into standard Python syntax."""
        cleaned = expr.strip()
        cleaned = cleaned.replace("×", "*").replace("÷", "/")
        cleaned = cleaned.replace("−", "-").replace("—", "-")
        cleaned = cleaned.replace("^", "**")
        cleaned = cleaned.replace("π", "pi")
        cleaned = cleaned.replace("√", "sqrt")
        return cleaned

    def evaluate(self, expr_str: str) -> Tuple[bool, Union[float, int, str]]:
        """
        Safely evaluates mathematical expressions using AST.
        Returns: (success: bool, result: float | int | str error_msg)
        """
        if not expr_str or not expr_str.strip():
            return False, "Error: Empty expression"

        sanitized = self.sanitize_expression(expr_str)

        try:
            tree = ast.parse(sanitized, mode="eval")
            result = self._eval_ast_node(tree.body)
            # Normalize float if integer
            if isinstance(result, float):
                if result.is_integer() and abs(result) < 1e15:
                    result = int(result)
                else:
                    # Round tiny floating inaccuracies
                    result = round(result, 12)
                    if isinstance(result, float) and result.is_integer() and abs(result) < 1e15:
                        result = int(result)

            formatted_res = self.format_result(result)
            self.add_history(expr_str, formatted_res)
            return True, formatted_res

        except CalculatorError as ce:
            return False, str(ce)
        except ZeroDivisionError:
            return False, "Error: Division by zero"
        except OverflowError:
            return False, "Error: Number is too large"
        except (SyntaxError, TypeError, ValueError, KeyError):
            return False, "Error: Invalid expression"
        except Exception as ex:
            return False, f"Error: {str(ex)}"

    def _eval_ast_node(self, node: ast.AST) -> Any:
        operators_map = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }

        # Numbers / Literals
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise CalculatorError("Error: Invalid literal in expression")

        # Variables / Constants
        elif isinstance(node, ast.Name):
            constants = self._get_allowed_constants()
            if node.id in constants:
                val = constants[node.id]
                return float(val) if isinstance(val, (int, float, str)) else 0.0
            raise CalculatorError(f"Error: Unknown variable '{node.id}'")

        # Binary Operations: a + b, a - b, a * b, a / b, a ** b, a % b
        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in operators_map:
                raise CalculatorError("Error: Unsupported operator")

            left = self._eval_ast_node(node.left)
            right = self._eval_ast_node(node.right)

            if op_type in (ast.Div, ast.FloorDiv, ast.Mod) and right == 0:
                raise CalculatorError("Error: Division by zero")

            if op_type == ast.Pow:
                if abs(left) > 10000 and right > 100:
                    raise CalculatorError("Error: Number is too large")
                try:
                    res = left ** right
                    if isinstance(res, complex):
                        raise CalculatorError("Error: Complex number result not supported")
                    return res
                except OverflowError:
                    raise CalculatorError("Error: Number is too large")

            return operators_map[op_type](left, right)

        # Unary Operations: -a, +a
        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in operators_map:
                raise CalculatorError("Error: Unsupported unary operator")
            operand = self._eval_ast_node(node.operand)
            return operators_map[op_type](operand)

        # Function Calls: sin(x), sqrt(x), etc.
        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise CalculatorError("Error: Invalid function invocation")
            func_name = node.func.id
            functions = self._get_allowed_functions()
            if func_name not in functions:
                raise CalculatorError(f"Error: Unknown function '{func_name}'")

            args = [self._eval_ast_node(arg) for arg in node.args]
            return functions[func_name](*args)

        else:
            raise CalculatorError("Error: Unsupported mathematical construct")

    @staticmethod
    def format_result(val: Union[int, float, str]) -> str:
        """Formats numbers cleanly without unnecessary trailing zeros."""
        if isinstance(val, (int, float)):
            if isinstance(val, float):
                if val.is_integer() and abs(val) < 1e15:
                    return str(int(val))
                if abs(val) >= 1e15 or (0 < abs(val) < 1e-6):
                    return f"{val:.8e}".replace("e+0", "e+").replace("e-0", "e-")
                formatted = f"{val:.10f}".rstrip("0").rstrip(".")
                return formatted
            return str(val)
        return str(val)
