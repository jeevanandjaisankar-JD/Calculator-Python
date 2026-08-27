"""
Scientific Calculator - Main Application Entry Point.
Runs the modern Graphical User Interface (GUI) by default,
or the interactive Command-Line Interface (CLI) when passed the --cli flag.
"""

import math
import sys
from typing import Union


# -----------------------------
# Basic Operations
# -----------------------------

def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> Union[float, str]:
    if b == 0:
        return "Error: Division by zero"
    return a / b


def modulus(a: float, b: float) -> Union[float, str]:
    if b == 0:
        return "Error: Division by zero"
    return a % b


def power(a: float, b: float) -> float:
    return a ** b


# -----------------------------
# Scientific Operations
# -----------------------------

def square_root(a: float) -> Union[float, str]:
    if a < 0:
        return "Error: Cannot calculate square root of a negative number"
    return math.sqrt(a)


def sine(a: float) -> float:
    return math.sin(math.radians(a))


def cosine(a: float) -> float:
    return math.cos(math.radians(a))


def tangent(a: float) -> float:
    return math.tan(math.radians(a))


def logarithm(a: float) -> Union[float, str]:
    if a <= 0:
        return "Error: Logarithm is only defined for positive numbers"
    return math.log10(a)


def natural_log(a: float) -> Union[float, str]:
    if a <= 0:
        return "Error: Natural logarithm is only defined for positive numbers"
    return math.log(a)


def factorial(a: float) -> Union[int, str]:
    if a < 0 or not float(a).is_integer():
        return "Error: Factorial requires a non-negative integer"
    return math.factorial(int(a))


# -----------------------------
# CLI Interface
# -----------------------------

def run_cli():
    """Runs the interactive command-line interface."""
    print("================================")
    print("        SCIENTIFIC CALCULATOR")
    print("================================")

    while True:
        print("\nAvailable Operations:")
        print("+     Addition")
        print("-     Subtraction")
        print("x     Multiplication")
        print("/     Division")
        print("%     Modulus")
        print("^     Power")
        print("sqrt  Square Root")
        print("sin   Sine (degrees)")
        print("cos   Cosine (degrees)")
        print("tan   Tangent (degrees)")
        print("log   Logarithm (base 10)")
        print("ln    Natural Logarithm")
        print("fact  Factorial")
        print("q     Quit")

        try:
            op_input = input("\nEnter operation (or 'q' to quit): ").strip().lower()
            if op_input == "q":
                print("\nGoodbye! 👋")
                break

            if op_input in ["sqrt", "sin", "cos", "tan", "log", "ln", "fact"]:
                num1 = float(input("Enter number: "))
                if op_input == "sqrt":
                    result = square_root(num1)
                elif op_input == "sin":
                    result = sine(num1)
                elif op_input == "cos":
                    result = cosine(num1)
                elif op_input == "tan":
                    result = tangent(num1)
                elif op_input == "log":
                    result = logarithm(num1)
                elif op_input == "ln":
                    result = natural_log(num1)
                elif op_input == "fact":
                    result = factorial(num1)
            elif op_input in ["+", "-", "x", "*", "/", "%", "^"]:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))

                if op_input == "+":
                    result = add(num1, num2)
                elif op_input == "-":
                    result = subtract(num1, num2)
                elif op_input in ["x", "*"]:
                    result = multiply(num1, num2)
                elif op_input == "/":
                    result = divide(num1, num2)
                elif op_input == "%":
                    result = modulus(num1, num2)
                elif op_input == "^":
                    result = power(num1, num2)
            else:
                print("Invalid operation!")
                continue

            print("\nResult:", result)

        except ValueError:
            print("\nError: Please enter valid numbers!")
        except OverflowError:
            print("\nError: Number is too large!")

        choice = input("\nDo you want to continue? (y/n): ").strip().lower()
        if choice != "y":
            print("\nGoodbye! 👋")
            break


# -----------------------------
# Main Execution
# -----------------------------

def main():
    if "--cli" in sys.argv or "-c" in sys.argv:
        run_cli()
    else:
        try:
            from gui import launch_gui
            launch_gui()
        except Exception as ex:
            print(f"Unable to start GUI ({ex}). Falling back to CLI mode...")
            run_cli()


if __name__ == "__main__":
    main()