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


# -----------------------------
# Calculator
# -----------------------------

print("================================")
print("        SCIENTIFIC CALCULATOR   ")
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
    print("q     Quit")

    try:
        num1 = float(input("\nEnter number: "))
        op = input("Enter operation: ").lower()

        if op == "q":
            print("\nGoodbye! 👋")
            break

        # Single-number operations
        if op == "sqrt":
            result = square_root(num1)

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