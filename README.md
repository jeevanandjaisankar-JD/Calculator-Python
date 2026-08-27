# 🧮 Modern Scientific Calculator in Python

A modern, fast, and feature-packed Scientific Calculator application written in Python. Built with both a sleek graphical desktop interface (GUI) and an interactive command-line interface (CLI).

---

## ✨ Features

### 🖥️ Modern Desktop GUI
* **Modern Themes:** Dark and Light mode themes with custom color palettes, smooth hover states, and responsive design.
* **Dual-Line Display:** Live formula history on the top line and bold, high-contrast result/input line on the bottom.
* **Trigonometry (DEG & RAD Modes):** `sin`, `cos`, `tan`, `asin`, `acos`, `atan` with instant degree/radian mode switching.
* **Powers & Roots:** `x²`, `xʸ`, `√x`, `1/x`, `|x|`, and modulus `%`.
* **Logarithms & Factorials:** Base-10 Log (`log₁₀`), Natural Log (`ln`), Factorial (`n!`).
* **Mathematical Constants:** Full support for `π` (pi) and `e`.
* **Memory Bank:** `MC` (Clear), `MR` (Recall), `M+` (Add), `M-` (Subtract), `MS` (Store) with active memory indicators.
* **Calculation History:** Collapsible side drawer preserving recent calculations with click-to-recall and one-click clear.
* **Clipboard Integration:** One-click copy for fast workflow.
* **Full Keyboard Support:** Type directly with your keyboard or numpad.

### ⚡ Comprehensive Error Handling & Engine Safety
* Safe AST-based mathematical parser (no arbitrary `eval`).
* Division-by-zero prevention.
* Non-negative validation for square roots and logarithms.
* Integer domain checks for factorials.

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|---|---|
| `0` - `9`, `.` | Enter numbers & decimals |
| `+`, `-`, `*`, `/`, `^`, `%` | Arithmetic operations |
| `(`, `)` | Parentheses / grouping |
| `Enter` or `=` | Calculate result |
| `Backspace` | Delete last character |
| `Escape` or `c` | Clear display (`AC`) |
| `Ctrl + C` | Copy current result |
| `Ctrl + H` | Toggle calculation history drawer |

---

## 🚀 Getting Started

### Prerequisites
* Python 3.8+ installed (uses standard library `tkinter` and `math` — no external pip dependencies required!).

### Running the Desktop GUI (Default)
```bash
python calculator.py
```
*(or run `python gui.py` directly)*

### Running the Command-Line Interface (CLI)
```bash
python calculator.py --cli
```

### Running the Test Suite
```bash
# Run Core Engine tests
python -m unittest test_calculator.py -v

# Run GUI Integration tests
python -m unittest test_gui.py -v
```

---

## 📁 Project Architecture

```
Calculator-Python/
├── calculator.py         # Main entry point (launches GUI or CLI fallback)
├── calculator_engine.py  # Safe AST evaluation engine, scientific math, memory & history
├── gui.py                # Modern Tkinter desktop application
├── test_calculator.py    # Unit tests for calculation engine
├── test_gui.py           # Integration tests for GUI actions and events
└── README.md             # Project documentation
```

---

## 🤝 Contributing
Feel free to open issues or submit pull requests with additional functions, unit conversions, or graphing capabilities!