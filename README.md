Markdown# Python Scientific Calculator CLI

A lightweight, interactive command-line scientific calculator written in Python. Built incrementally using functional modularity, error-handling best practices, and standard math libraries.

---

## 🚀 Features

* **Basic Arithmetic:** Addition, Subtraction, Multiplication, Division (`+`, `-`, `x`, `/`)
* **Advanced Math:** Modulus (`%`), Exponentiation (`^`), Square Root (`sqrt`)
* **Trigonometry:** Sine (`sin`), Cosine (`cos`), Tangent (`tan`) in degrees
* **Logarithms & Factorials:** Base-10 Log (`log`), Natural Log (`ln`), Factorial (`fact`)
* **Robust Error Handling:** Protection against division by zero, negative square roots/logarithms, non-integer factorials, invalid input types, and numeric overflow.

---

## 🛠️ Installation & Usage

### Prerequisites
* Python 3.x installed on your system.

### Running the Calculator

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/scientific-calculator.git](https://github.com/your-username/scientific-calculator.git)
   cd scientific-calculator
Run the script:Bashpython calculator.py
Follow the interactive prompts:Enter your first number.Choose an operation (e.g., +, sqrt, sin, log).If prompted, enter the second number.Type y to calculate another expression or n/q to quit.📜 Commit History & EvolutionThe project was developed in 4 incremental stages to ensure modular code structure and clean version control tracking:CommitMessageDescription & Added FunctionsCommit 1feat: setup basic CLI loop with add, subtract, multiply, and divideInitial release. Core CLI loop, input handling framework, basic arithmetic functions (add, subtract, multiply, divide), zero-division validation, and exit options.Commit 2feat: add modulus, power, and square_root functionsExtended operators. Added modulus, power (**), and square_root using math.sqrt(). Implemented negative input guard clauses for square roots and caught OverflowError.Commit 3feat: add sin, cos, and tan trigonometric operationsTrigonometric support. Added sine, cosine, and tangent using math.sin, math.cos, and math.tan. Converts degrees to radians using math.radians().Commit 4feat: add base-10 log, natural log, and factorial functionsFull scientific capability. Added logarithm (base 10 via math.log10), natural_log (math.log), and factorial (math.factorial). Validated bounds (positive-only logs, non-negative integer factorials).🧪 Example OutputPlaintext================================
        SCIENTIFIC CALCULATOR
================================

Available Operations:
+     Addition
-     Subtraction
x     Multiplication
/     Division
%     Modulus
^     Power
sqrt  Square Root
sin   Sine
cos   Cosine
tan   Tangent
log   Logarithm (base 10)
ln    Natural Logarithm
fact  Factorial
q     Quit

Enter number: 45
Enter operation: sin

Result: 0.7071067811865475

Do you want to continue? (y/n): n

Goodbye! 👋
🤝 ContributingFeel free to fork this repository, open issues, or submit pull requests with enhancements like memory storage, history tracking, or complex number support.