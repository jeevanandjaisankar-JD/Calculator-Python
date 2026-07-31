import math

print("Advanced Calculator")

while True:
    try:
        num1 = float(input("Enter first number: "))
        op = input("Enter operation (+, -, x, /, %, ^, sqrt): ")

        if op == "sqrt":
            print("Result:", math.sqrt(num1))
        else:
            num2 = float(input("Enter second number: "))

            if op == "+":
                print("Result:", num1 + num2)
            elif op == "-":
                print("Result:", num1 - num2)
            elif op == "x":
                print("Result:", num1 * num2)
            elif op == "/":
                if num2 != 0:
                    print("Result:", num1 / num2)
                else:
                    print("Error: Division by zero")
            elif op == "%":
                print("Result:", num1 % num2)
            elif op == "^":
                print("Result:", num1 ** num2)
            else:
                print("Invalid operation")
    except ValueError:
        print("Please enter valid numbers!")

    choice = input("Do you want to continue? (y/n): ")
    if choice.lower() != "y":
        print("Goodbye!")
        break
