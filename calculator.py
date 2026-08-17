import math


# -----------------------------
# Basic Operations
# -----------------------------

def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b


def modulus(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a % b


def power(a, b):
    return a ** b


# -----------------------------
# Scientific Operations
# -----------------------------

def square_root(a):
    if a < 0:
        return "Error: Cannot calculate square root of a negative number"
    return math.sqrt(a)


def sine(a):
    return math.sin(math.radians(a))


def cosine(a):
    return math.cos(math.radians(a))


def tangent(a):
    return math.tan(math.radians(a))


def logarithm(a):
    if a <= 0:
        return "Error: Logarithm is only defined for positive numbers"
    return math.log10(a)


def natural_log(a):
    if a <= 0:
        return "Error: Natural logarithm is only defined for positive numbers"
    return math.log(a)


def factorial(a):
    if a < 0 or not a.is_integer():
        return "Error: Factorial requires a non-negative integer"
    return math.factorial(int(a))


# -----------------------------
# Calculator
# -----------------------------

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
    print("sin   Sine")
    print("cos   Cosine")
    print("tan   Tangent")
    print("log   Logarithm (base 10)")
    print("ln    Natural Logarithm")
    print("fact  Factorial")
    print("q     Quit")

    try:
        num1 = float(input("\nEnter number: "))

        op = input("Enter operation: ").lower()

        # Quit
        if op == "q":
            print("\nGoodbye! 👋")
            break

        # Single-number operations
        if op == "sqrt":
            result = square_root(num1)

        elif op == "sin":
            result = sine(num1)

        elif op == "cos":
            result = cosine(num1)

        elif op == "tan":
            result = tangent(num1)

        elif op == "log":
            result = logarithm(num1)

        elif op == "ln":
            result = natural_log(num1)

        elif op == "fact":
            result = factorial(num1)

        # Two-number operations
        elif op in ["+", "-", "x", "/", "%", "^"]:

            num2 = float(input("Enter second number: "))

            if op == "+":
                result = add(num1, num2)

            elif op == "-":
                result = subtract(num1, num2)

            elif op == "x":
                result = multiply(num1, num2)

            elif op == "/":
                result = divide(num1, num2)

            elif op == "%":
                result = modulus(num1, num2)

            elif op == "^":
                result = power(num1, num2)

        else:
            print("Invalid operation!")
            continue

        print("\nResult:", result)

    except ValueError:
        print("\nError: Please enter valid numbers!")

    except OverflowError:
        print("\nError: Number is too large!")

    choice = input("\nDo you want to continue? (y/n): ")

    if choice.lower() != "y":
        print("\nGoodbye! 👋")
        break