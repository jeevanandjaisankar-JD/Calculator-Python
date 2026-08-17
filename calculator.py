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


# -----------------------------
# Calculator
# -----------------------------

print("================================")
print("        BASIC CALCULATOR        ")
print("================================")

while True:
    print("\nAvailable Operations:")
    print("+     Addition")
    print("-     Subtraction")
    print("x     Multiplication")
    print("/     Division")
    print("q     Quit")

    try:
        num1 = float(input("\nEnter number: "))
        op = input("Enter operation: ").lower()

        if op == "q":
            print("\nGoodbye! 👋")
            break

        if op in ["+", "-", "x", "/"]:
            num2 = float(input("Enter second number: "))

            if op == "+":
                result = add(num1, num2)
            elif op == "-":
                result = subtract(num1, num2)
            elif op == "x":
                result = multiply(num1, num2)
            elif op == "/":
                result = divide(num1, num2)

            print("\nResult:", result)
        else:
            print("Invalid operation!")
            continue

    except ValueError:
        print("\nError: Please enter valid numbers!")

    choice = input("\nDo you want to continue? (y/n): ")
    if choice.lower() != "y":
        print("\nGoodbye! 👋")
        break