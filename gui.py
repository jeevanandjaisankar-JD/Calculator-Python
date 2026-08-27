"""
Modern Desktop Graphical User Interface for the Scientific Calculator.
Built with Tkinter, featuring Dark/Light themes, responsive keypads,
trigonometry modes, memory bank, history drawer, and full keyboard navigation.
"""

import sys
import tkinter as tk
from tkinter import font as tkfont
from typing import Dict, Optional

from calculator_engine import CalculatorEngine


# Enable High DPI awareness on Windows
try:
    if sys.platform == "win32":
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


# ----------------------------------------------------------------------
# Theme Color Schemes
# ----------------------------------------------------------------------
THEMES = {
    "dark": {
        "bg_main": "#121316",
        "bg_card": "#1c1d22",
        "bg_display": "#24262d",
        "display_border": "#32353e",
        "text_primary": "#ffffff",
        "text_secondary": "#9ca3af",
        "text_accent": "#60a5fa",
        # Keypad button colors
        "btn_num_bg": "#23262f",
        "btn_num_fg": "#f3f4f6",
        "btn_num_hover": "#313540",
        "btn_op_bg": "#2563eb",
        "btn_op_fg": "#ffffff",
        "btn_op_hover": "#1d4ed8",
        "btn_sci_bg": "#1e222b",
        "btn_sci_fg": "#93c5fd",
        "btn_sci_hover": "#2d3340",
        "btn_fn_bg": "#2d313b",
        "btn_fn_fg": "#e2e8f0",
        "btn_fn_hover": "#3b404d",
        "btn_eq_bg": "#059669",
        "btn_eq_fg": "#ffffff",
        "btn_eq_hover": "#047857",
        "btn_clear_bg": "#dc2626",
        "btn_clear_fg": "#ffffff",
        "btn_clear_hover": "#b91c1c",
        "btn_del_bg": "#7c2d12",
        "btn_del_fg": "#fdba74",
        "btn_del_hover": "#9a3412",
        # Memory & Header buttons
        "btn_header_bg": "#2a2d36",
        "btn_header_fg": "#cbd5e1",
        "btn_header_hover": "#373b47",
        "badge_active_bg": "#2563eb",
        "badge_active_fg": "#ffffff",
        # History panel
        "history_bg": "#18191e",
        "history_item_bg": "#23262f",
        "history_item_hover": "#2e323e",
        "history_expr_fg": "#9ca3af",
        "history_res_fg": "#38bdf8",
        "border_color": "#2c303a",
    },
    "light": {
        "bg_main": "#f1f5f9",
        "bg_card": "#ffffff",
        "bg_display": "#ffffff",
        "display_border": "#e2e8f0",
        "text_primary": "#0f172a",
        "text_secondary": "#64748b",
        "text_accent": "#2563eb",
        # Keypad button colors
        "btn_num_bg": "#ffffff",
        "btn_num_fg": "#0f172a",
        "btn_num_hover": "#e2e8f0",
        "btn_op_bg": "#2563eb",
        "btn_op_fg": "#ffffff",
        "btn_op_hover": "#1d4ed8",
        "btn_sci_bg": "#f8fafc",
        "btn_sci_fg": "#1e40af",
        "btn_sci_hover": "#e2e8f0",
        "btn_fn_bg": "#f1f5f9",
        "btn_fn_fg": "#334155",
        "btn_fn_hover": "#e2e8f0",
        "btn_eq_bg": "#10b981",
        "btn_eq_fg": "#ffffff",
        "btn_eq_hover": "#059669",
        "btn_clear_bg": "#ef4444",
        "btn_clear_fg": "#ffffff",
        "btn_clear_hover": "#dc2626",
        "btn_del_bg": "#fee2e2",
        "btn_del_fg": "#991b1b",
        "btn_del_hover": "#fecaca",
        # Memory & Header buttons
        "btn_header_bg": "#e2e8f0",
        "btn_header_fg": "#334155",
        "btn_header_hover": "#cbd5e1",
        "badge_active_bg": "#2563eb",
        "badge_active_fg": "#ffffff",
        # History panel
        "history_bg": "#f8fafc",
        "history_item_bg": "#ffffff",
        "history_item_hover": "#f1f5f9",
        "history_expr_fg": "#64748b",
        "history_res_fg": "#0284c7",
        "border_color": "#cbd5e1",
    }
}


class ModernButton(tk.Frame):
    """Custom styled button with smooth hover effects and click feedback."""

    def __init__(self, parent, text: str, command=None, bg_color="#23262f", fg_color="#ffffff",
                 hover_color="#313540", font=("Segoe UI", 11), width=4, height=1, **kwargs):
        super().__init__(parent, bg=bg_color, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.fg_color = fg_color

        self.label = tk.Label(
            self,
            text=text,
            bg=bg_color,
            fg=fg_color,
            font=font,
            cursor="hand2",
            padx=6,
            pady=6,
        )
        self.label.pack(fill="both", expand=True)

        # Bind hover and click events
        self.label.bind("<Enter>", self._on_enter)
        self.label.bind("<Leave>", self._on_leave)
        self.label.bind("<Button-1>", self._on_click)

    def _on_enter(self, event):
        self.configure(bg=self.hover_color)
        self.label.configure(bg=self.hover_color)

    def _on_leave(self, event):
        self.configure(bg=self.bg_color)
        self.label.configure(bg=self.bg_color)

    def _on_click(self, event):
        if self.command:
            self.command()

    def update_colors(self, bg_color: str, fg_color: str, hover_color: str):
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.hover_color = hover_color
        self.configure(bg=bg_color)
        self.label.configure(bg=bg_color, fg=fg_color)

    def set_text(self, text: str):
        self.label.configure(text=text)


class ScientificCalculatorGUI:
    """Main Application GUI for the Scientific Calculator."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.engine = CalculatorEngine()
        self.current_theme = "dark"
        self.colors = THEMES[self.current_theme]

        # State tracking
        self.current_input: str = "0"
        self.expression_preview: str = ""
        self.just_calculated: bool = False
        self.history_visible: bool = False

        # Configure Root Window
        self.root.title("Scientific Calculator")
        self.root.minsize(440, 640)
        self.root.geometry("450x660")
        self.root.configure(bg=self.colors["bg_main"])

        # Track registered widgets for dynamic theming
        self.themed_widgets = []
        self.buttons: Dict[str, ModernButton] = {}

        self._build_ui()
        self._bind_keyboard_shortcuts()

    # ------------------------------------------------------------------
    # UI Layout Construction
    # ------------------------------------------------------------------
    def _build_ui(self):
        # Master container for calculator and history drawer
        self.main_container = tk.Frame(self.root, bg=self.colors["bg_main"])
        self.main_container.pack(fill="both", expand=True)

        # Left: Calculator body
        self.calc_frame = tk.Frame(self.main_container, bg=self.colors["bg_main"], padx=14, pady=12)
        self.calc_frame.pack(side="left", fill="both", expand=True)

        # Right: History panel (hidden by default)
        self.history_panel = tk.Frame(
            self.main_container,
            bg=self.colors["history_bg"],
            width=260,
            padx=10,
            pady=12,
            highlightthickness=1,
            highlightbackground=self.colors["border_color"]
        )

        self._build_header()
        self._build_display()
        self._build_memory_bar()
        self._build_keypad()
        self._build_history_panel()

    def _build_header(self):
        """Top bar with angle mode, memory badge, copy, history toggle, and theme switch."""
        self.header_frame = tk.Frame(self.calc_frame, bg=self.colors["bg_main"])
        self.header_frame.pack(fill="x", pady=(0, 10))

        # Left header buttons (Angle mode DEG/RAD and Memory indicator)
        left_box = tk.Frame(self.header_frame, bg=self.colors["bg_main"])
        left_box.pack(side="left")

        self.btn_angle = ModernButton(
            left_box,
            text=f"📐 {self.engine.angle_mode}",
            command=self._on_toggle_angle,
            bg_color=self.colors["btn_header_bg"],
            fg_color=self.colors["text_accent"],
            hover_color=self.colors["btn_header_hover"],
            font=("Segoe UI", 9, "bold"),
        )
        self.btn_angle.pack(side="left", padx=(0, 6))

        self.lbl_memory_badge = tk.Label(
            left_box,
            text="M",
            bg=self.colors["btn_header_bg"],
            fg=self.colors["text_secondary"],
            font=("Segoe UI", 9, "bold"),
            padx=8,
            pady=3,
        )
        self.lbl_memory_badge.pack(side="left", padx=2)

        # Right header buttons (Copy, History, Theme)
        right_box = tk.Frame(self.header_frame, bg=self.colors["bg_main"])
        right_box.pack(side="right")

        self.btn_copy = ModernButton(
            right_box,
            text="📋 Copy",
            command=self._on_copy_result,
            bg_color=self.colors["btn_header_bg"],
            fg_color=self.colors["btn_header_fg"],
            hover_color=self.colors["btn_header_hover"],
            font=("Segoe UI", 9),
        )
        self.btn_copy.pack(side="left", padx=3)

        self.btn_history_toggle = ModernButton(
            right_box,
            text="🕒 History",
            command=self._toggle_history,
            bg_color=self.colors["btn_header_bg"],
            fg_color=self.colors["btn_header_fg"],
            hover_color=self.colors["btn_header_hover"],
            font=("Segoe UI", 9),
        )
        self.btn_history_toggle.pack(side="left", padx=3)

        self.btn_theme = ModernButton(
            right_box,
            text="🌙" if self.current_theme == "dark" else "☀️",
            command=self._toggle_theme,
            bg_color=self.colors["btn_header_bg"],
            fg_color=self.colors["btn_header_fg"],
            hover_color=self.colors["btn_header_hover"],
            font=("Segoe UI", 9),
        )
        self.btn_theme.pack(side="left", padx=(3, 0))

    def _build_display(self):
        """Dual-line high contrast display."""
        self.display_frame = tk.Frame(
            self.calc_frame,
            bg=self.colors["bg_display"],
            highlightbackground=self.colors["display_border"],
            highlightthickness=1,
            padx=14,
            pady=10,
        )
        self.display_frame.pack(fill="x", pady=(0, 10))

        # Upper formula line
        self.lbl_preview = tk.Label(
            self.display_frame,
            text="",
            bg=self.colors["bg_display"],
            fg=self.colors["text_secondary"],
            font=("Segoe UI", 11),
            anchor="e",
        )
        self.lbl_preview.pack(fill="x")

        # Lower primary display
        self.lbl_display = tk.Label(
            self.display_frame,
            text=self.current_input,
            bg=self.colors["bg_display"],
            fg=self.colors["text_primary"],
            font=("Segoe UI", 26, "bold"),
            anchor="e",
        )
        self.lbl_display.pack(fill="x", pady=(4, 0))

        # Status toast for feedback
        self.lbl_toast = tk.Label(
            self.calc_frame,
            text="",
            bg=self.colors["bg_main"],
            fg=self.colors["text_accent"],
            font=("Segoe UI", 9, "italic"),
            anchor="e"
        )
        self.lbl_toast.pack(fill="x", pady=(0, 4))

    def _build_memory_bar(self):
        """Memory action row: MC, MR, M+, M-, MS."""
        self.mem_frame = tk.Frame(self.calc_frame, bg=self.colors["bg_main"])
        self.mem_frame.pack(fill="x", pady=(0, 8))

        mem_buttons = [
            ("MC", self._on_memory_clear),
            ("MR", self._on_memory_recall),
            ("M+", self._on_memory_add),
            ("M−", self._on_memory_sub),
            ("MS", self._on_memory_store),
        ]

        for i, (text, action) in enumerate(mem_buttons):
            self.mem_frame.columnconfigure(i, weight=1, uniform="mem")
            btn = ModernButton(
                self.mem_frame,
                text=text,
                command=action,
                bg_color=self.colors["btn_header_bg"],
                fg_color=self.colors["btn_header_fg"],
                hover_color=self.colors["btn_header_hover"],
                font=("Segoe UI", 10, "bold"),
            )
            btn.grid(row=0, column=i, padx=2, sticky="nsew")
            self.buttons[f"mem_{text}"] = btn

    def _build_keypad(self):
        """Unified scientific and standard keypads."""
        self.keypad_frame = tk.Frame(self.calc_frame, bg=self.colors["bg_main"])
        self.keypad_frame.pack(fill="both", expand=True)

        # 5 Columns layout
        for col in range(5):
            self.keypad_frame.columnconfigure(col, weight=1, uniform="keypad")

        # Keypad Layout Definition: (Text, Action, Category)
        layout = [
            # Row 0 (Scientific Functions 1)
            [("sin", lambda: self._insert_function("sin("), "sci"),
             ("cos", lambda: self._insert_function("cos("), "sci"),
             ("tan", lambda: self._insert_function("tan("), "sci"),
             ("π", lambda: self._insert_symbol("pi"), "sci"),
             ("e", lambda: self._insert_symbol("e"), "sci")],

            # Row 1 (Scientific Functions 2)
            [("asin", lambda: self._insert_function("asin("), "sci"),
             ("acos", lambda: self._insert_function("acos("), "sci"),
             ("atan", lambda: self._insert_function("atan("), "sci"),
             ("log₁₀", lambda: self._insert_function("log("), "sci"),
             ("ln", lambda: self._insert_function("ln("), "sci")],

            # Row 2 (Powers, Roots, Factorial)
            [("x²", lambda: self._apply_unary_op("** 2"), "sci"),
             ("xʸ", lambda: self._insert_symbol("^"), "sci"),
             ("√x", lambda: self._insert_function("sqrt("), "sci"),
             ("n!", lambda: self._insert_function("fact("), "sci"),
             ("|x|", lambda: self._insert_function("abs("), "sci")],

            # Row 3 (Grouping, Clear & Delete)
            [("(", lambda: self._insert_symbol("("), "fn"),
             (")", lambda: self._insert_symbol(")"), "fn"),
             ("%", lambda: self._insert_symbol("%"), "fn"),
             ("⌫ DEL", self._on_backspace, "del"),
             ("AC", self._on_clear, "clear")],

            # Row 4 (Digits 7-9 & Division)
            [("7", lambda: self._insert_digit("7"), "num"),
             ("8", lambda: self._insert_digit("8"), "num"),
             ("9", lambda: self._insert_digit("9"), "num"),
             ("÷", lambda: self._insert_operator("/"), "op"),
             ("1/x", self._on_reciprocal, "sci")],

            # Row 5 (Digits 4-6 & Multiplication)
            [("4", lambda: self._insert_digit("4"), "num"),
             ("5", lambda: self._insert_digit("5"), "num"),
             ("6", lambda: self._insert_digit("6"), "num"),
             ("×", lambda: self._insert_operator("*"), "op"),
             ("±", self._on_toggle_sign, "num")],

            # Row 6 (Digits 1-3 & Subtraction)
            [("1", lambda: self._insert_digit("1"), "num"),
             ("2", lambda: self._insert_digit("2"), "num"),
             ("3", lambda: self._insert_digit("3"), "num"),
             ("−", lambda: self._insert_operator("-"), "op"),
             ("Ans", self._on_insert_ans, "sci")],

            # Row 7 (0, Dot, Equals, Addition)
            [("0", lambda: self._insert_digit("0"), "num"),
             (".", lambda: self._insert_digit("."), "num"),
             ("=", self._on_calculate, "eq"),
             ("+", lambda: self._insert_operator("+"), "op"),
             ("Rad/Deg", self._on_toggle_angle, "fn")]
        ]

        for row_idx, row in enumerate(layout):
            self.keypad_frame.rowconfigure(row_idx, weight=1, uniform="keypad")
            for col_idx, item in enumerate(row):
                text, action, category = item
                bg, fg, hover = self._get_category_colors(category)
                font_weight = "bold" if category in ("eq", "clear", "del", "op") else "normal"
                font_size = 11 if category in ("num", "op", "eq") else 10

                btn = ModernButton(
                    self.keypad_frame,
                    text=text,
                    command=action,
                    bg_color=bg,
                    fg_color=fg,
                    hover_color=hover,
                    font=("Segoe UI", font_size, font_weight),
                )
                btn.grid(row=row_idx, column=col_idx, padx=2, pady=2, sticky="nsew")
                self.buttons[f"btn_{row_idx}_{col_idx}"] = btn

    def _get_category_colors(self, category: str):
        if category == "num":
            return self.colors["btn_num_bg"], self.colors["btn_num_fg"], self.colors["btn_num_hover"]
        elif category == "op":
            return self.colors["btn_op_bg"], self.colors["btn_op_fg"], self.colors["btn_op_hover"]
        elif category == "sci":
            return self.colors["btn_sci_bg"], self.colors["btn_sci_fg"], self.colors["btn_sci_hover"]
        elif category == "fn":
            return self.colors["btn_fn_bg"], self.colors["btn_fn_fg"], self.colors["btn_fn_hover"]
        elif category == "eq":
            return self.colors["btn_eq_bg"], self.colors["btn_eq_fg"], self.colors["btn_eq_hover"]
        elif category == "clear":
            return self.colors["btn_clear_bg"], self.colors["btn_clear_fg"], self.colors["btn_clear_hover"]
        elif category == "del":
            return self.colors["btn_del_bg"], self.colors["btn_del_fg"], self.colors["btn_del_hover"]
        return self.colors["btn_fn_bg"], self.colors["btn_fn_fg"], self.colors["btn_fn_hover"]

    def _build_history_panel(self):
        """Right-side collapsible history drawer."""
        # Top title & clear
        hist_header = tk.Frame(self.history_panel, bg=self.colors["history_bg"])
        hist_header.pack(fill="x", pady=(0, 10))

        lbl_title = tk.Label(
            hist_header,
            text="Calculation History",
            bg=self.colors["history_bg"],
            fg=self.colors["text_primary"],
            font=("Segoe UI", 11, "bold"),
        )
        lbl_title.pack(side="left")

        btn_clear_hist = ModernButton(
            hist_header,
            text="Clear",
            command=self._on_clear_history,
            bg_color=self.colors["btn_del_bg"],
            fg_color=self.colors["btn_del_fg"],
            hover_color=self.colors["btn_del_hover"],
            font=("Segoe UI", 9, "bold"),
        )
        btn_clear_hist.pack(side="right")

        # Scrollable container for history items
        self.hist_canvas = tk.Canvas(
            self.history_panel,
            bg=self.colors["history_bg"],
            highlightthickness=0,
        )
        self.hist_scrollbar = tk.Scrollbar(
            self.history_panel,
            orient="vertical",
            command=self.hist_canvas.yview,
        )
        self.hist_scroll_content = tk.Frame(self.hist_canvas, bg=self.colors["history_bg"])

        self.hist_scroll_content.bind(
            "<Configure>",
            lambda e: self.hist_canvas.configure(scrollregion=self.hist_canvas.bbox("all")),
        )
        self.hist_canvas.create_window((0, 0), window=self.hist_scroll_content, anchor="nw", width=230)
        self.hist_canvas.configure(yscrollcommand=self.hist_scrollbar.set)

        self.hist_canvas.pack(side="left", fill="both", expand=True)
        self.hist_scrollbar.pack(side="right", fill="y")

    # ------------------------------------------------------------------
    # Keyboard Event Bindings
    # ------------------------------------------------------------------
    def _bind_keyboard_shortcuts(self):
        self.root.bind("<Key>", self._on_key_press)
        self.root.bind("<Return>", lambda e: self._on_calculate())
        self.root.bind("<KP_Enter>", lambda e: self._on_calculate())
        self.root.bind("<BackSpace>", lambda e: self._on_backspace())
        self.root.bind("<Escape>", lambda e: self._on_clear())
        self.root.bind("<Control-c>", lambda e: self._on_copy_result())
        self.root.bind("<Control-h>", lambda e: self._toggle_history())

    def _on_key_press(self, event):
        char = event.char
        if not char:
            return

        if char in "0123456789.":
            self._insert_digit(char)
        elif char in "+-*/%^()":
            self._insert_operator(char)
        elif char == "=":
            self._on_calculate()
        elif char.lower() == "c":
            self._on_clear()

    # ------------------------------------------------------------------
    # Calculation & Input Operations
    # ------------------------------------------------------------------
    def _insert_digit(self, digit: str):
        self._clear_toast()
        if self.just_calculated:
            self.current_input = ""
            self.just_calculated = False

        if self.current_input == "0" and digit != ".":
            self.current_input = digit
        elif digit == "." and "." in self.current_input.split()[-1] if self.current_input else False:
            return
        else:
            self.current_input += digit

        self._update_display()

    def _insert_operator(self, op: str):
        self._clear_toast()
        self.just_calculated = False
        display_op = f" {op} "
        self.current_input += display_op
        self._update_display()

    def _insert_symbol(self, sym: str):
        self._clear_toast()
        if self.just_calculated:
            self.current_input = ""
            self.just_calculated = False

        if self.current_input == "0":
            self.current_input = sym
        else:
            self.current_input += sym
        self._update_display()

    def _insert_function(self, fn_str: str):
        self._clear_toast()
        if self.just_calculated:
            self.current_input = ""
            self.just_calculated = False

        if self.current_input == "0":
            self.current_input = fn_str
        else:
            self.current_input += fn_str
        self._update_display()

    def _apply_unary_op(self, op_suffix: str):
        self._clear_toast()
        self.current_input = f"({self.current_input}){op_suffix}"
        self._update_display()

    def _on_reciprocal(self):
        self._clear_toast()
        self.current_input = f"1 / ({self.current_input})"
        self._update_display()

    def _on_toggle_sign(self):
        self._clear_toast()
        if self.current_input.startswith("-("):
            self.current_input = self.current_input[2:-1]
        elif self.current_input.startswith("-"):
            self.current_input = self.current_input[1:]
        elif self.current_input == "0":
            return
        else:
            self.current_input = f"-({self.current_input})"
        self._update_display()

    def _on_insert_ans(self):
        self._clear_toast()
        if self.engine.history:
            last_res = self.engine.history[-1]["result"]
            if self.just_calculated or self.current_input == "0":
                self.current_input = last_res
            else:
                self.current_input += last_res
            self.just_calculated = False
            self._update_display()
        else:
            self._show_toast("No previous answer stored")

    def _on_backspace(self):
        self._clear_toast()
        if self.just_calculated:
            self.current_input = "0"
            self.just_calculated = False
        elif len(self.current_input) > 1:
            # Handle trailing spaces for operators
            if self.current_input.endswith(" "):
                self.current_input = self.current_input.rstrip()
            self.current_input = self.current_input[:-1].rstrip()
            if not self.current_input:
                self.current_input = "0"
        else:
            self.current_input = "0"

        self._update_display()

    def _on_clear(self):
        self._clear_toast()
        self.current_input = "0"
        self.expression_preview = ""
        self.just_calculated = False
        self._update_display()

    def _on_calculate(self):
        if not self.current_input or self.current_input.strip() == "":
            return

        expr = self.current_input
        success, result = self.engine.evaluate(expr)

        if success:
            self.expression_preview = f"{expr} ="
            self.current_input = str(result)
            self.just_calculated = True
            self._update_display()
            self._refresh_history_ui()
        else:
            self._show_toast(result)

    # ------------------------------------------------------------------
    # Header & Memory Actions
    # ------------------------------------------------------------------
    def _on_toggle_angle(self):
        mode = self.engine.toggle_angle_mode()
        self.btn_angle.set_text(f"📐 {mode}")
        self._show_toast(f"Switched to {mode} mode")

    def _on_copy_result(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.current_input)
        self._show_toast("Copied to clipboard!")

    def _on_memory_store(self):
        try:
            val = float(self.current_input)
            self.engine.memory_store(val)
            self._update_memory_ui()
            self._show_toast(f"Stored {val} in memory")
        except ValueError:
            self._show_toast("Error: Display must be a valid number to store")

    def _on_memory_recall(self):
        if self.engine.memory_active:
            recalled = self.engine.format_result(self.engine.memory_recall())
            if self.just_calculated or self.current_input == "0":
                self.current_input = recalled
            else:
                self.current_input += recalled
            self.just_calculated = False
            self._update_display()
            self._show_toast(f"Recalled {recalled} from memory")
        else:
            self._show_toast("Memory is empty")

    def _on_memory_add(self):
        try:
            val = float(self.current_input)
            self.engine.memory_add(val)
            self._update_memory_ui()
            self._show_toast(f"Added {val} to memory")
        except ValueError:
            self._show_toast("Error: Invalid number")

    def _on_memory_sub(self):
        try:
            val = float(self.current_input)
            self.engine.memory_subtract(val)
            self._update_memory_ui()
            self._show_toast(f"Subtracted {val} from memory")
        except ValueError:
            self._show_toast("Error: Invalid number")

    def _on_memory_clear(self):
        self.engine.memory_clear()
        self._update_memory_ui()
        self._show_toast("Memory cleared")

    def _update_memory_ui(self):
        if self.engine.memory_active:
            self.lbl_memory_badge.configure(
                bg=self.colors["badge_active_bg"],
                fg=self.colors["badge_active_fg"]
            )
        else:
            self.lbl_memory_badge.configure(
                bg=self.colors["btn_header_bg"],
                fg=self.colors["text_secondary"]
            )

    # ------------------------------------------------------------------
    # History Panel UI
    # ------------------------------------------------------------------
    def _toggle_history(self):
        if self.history_visible:
            self.history_panel.pack_forget()
            self.history_visible = False
            self.root.geometry(f"450x{self.root.winfo_height()}")
        else:
            self.history_panel.pack(side="right", fill="both")
            self.history_visible = True
            self.root.geometry(f"710x{self.root.winfo_height()}")
            self._refresh_history_ui()

    def _refresh_history_ui(self):
        for widget in self.hist_scroll_content.winfo_children():
            widget.destroy()

        history_items = self.engine.get_history()
        if not history_items:
            lbl_empty = tk.Label(
                self.hist_scroll_content,
                text="No calculations yet",
                bg=self.colors["history_bg"],
                fg=self.colors["text_secondary"],
                font=("Segoe UI", 10, "italic"),
                pady=20,
            )
            lbl_empty.pack(fill="x")
            return

        for item in history_items:
            card = tk.Frame(
                self.hist_scroll_content,
                bg=self.colors["history_item_bg"],
                padx=8,
                pady=6,
                cursor="hand2",
                highlightthickness=1,
                highlightbackground=self.colors["border_color"]
            )
            card.pack(fill="x", pady=3)

            lbl_expr = tk.Label(
                card,
                text=item["expression"],
                bg=self.colors["history_item_bg"],
                fg=self.colors["history_expr_fg"],
                font=("Segoe UI", 9),
                anchor="e",
            )
            lbl_expr.pack(fill="x")

            lbl_res = tk.Label(
                card,
                text=f"= {item['result']}",
                bg=self.colors["history_item_bg"],
                fg=self.colors["history_res_fg"],
                font=("Segoe UI", 12, "bold"),
                anchor="e",
            )
            lbl_res.pack(fill="x")

            # Click history card to load result
            def make_click_handler(res_val=item["result"]):
                return lambda e: self._load_history_result(res_val)

            card.bind("<Button-1>", make_click_handler())
            lbl_expr.bind("<Button-1>", make_click_handler())
            lbl_res.bind("<Button-1>", make_click_handler())

    def _load_history_result(self, result_val: str):
        self.current_input = result_val
        self.just_calculated = False
        self._update_display()
        self._show_toast(f"Loaded {result_val} from history")

    def _on_clear_history(self):
        self.engine.clear_history()
        self._refresh_history_ui()
        self._show_toast("History cleared")

    # ------------------------------------------------------------------
    # Display & Notification Updates
    # ------------------------------------------------------------------
    def _update_display(self):
        # Auto adjust font size if input is very long
        font_size = 26
        if len(self.current_input) > 18:
            font_size = 18
        elif len(self.current_input) > 26:
            font_size = 14

        self.lbl_display.configure(
            text=self.current_input,
            font=("Segoe UI", font_size, "bold")
        )
        self.lbl_preview.configure(text=self.expression_preview)

    def _show_toast(self, message: str):
        self.lbl_toast.configure(text=message)
        self.root.after(3500, self._clear_toast)

    def _clear_toast(self):
        self.lbl_toast.configure(text="")

    # ------------------------------------------------------------------
    # Theme Switching
    # ------------------------------------------------------------------
    def _toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.colors = THEMES[self.current_theme]
        self.btn_theme.set_text("🌙" if self.current_theme == "dark" else "☀️")
        self._apply_theme()

    def _apply_theme(self):
        self.root.configure(bg=self.colors["bg_main"])
        self.main_container.configure(bg=self.colors["bg_main"])
        self.calc_frame.configure(bg=self.colors["bg_main"])
        self.header_frame.configure(bg=self.colors["bg_main"])
        self.mem_frame.configure(bg=self.colors["bg_main"])
        self.keypad_frame.configure(bg=self.colors["bg_main"])
        self.lbl_toast.configure(bg=self.colors["bg_main"], fg=self.colors["text_accent"])

        self.display_frame.configure(
            bg=self.colors["bg_display"],
            highlightbackground=self.colors["display_border"]
        )
        self.lbl_display.configure(
            bg=self.colors["bg_display"],
            fg=self.colors["text_primary"]
        )
        self.lbl_preview.configure(
            bg=self.colors["bg_display"],
            fg=self.colors["text_secondary"]
        )

        # Header buttons
        for btn in (self.btn_copy, self.btn_history_toggle, self.btn_theme):
            btn.update_colors(
                self.colors["btn_header_bg"],
                self.colors["btn_header_fg"],
                self.colors["btn_header_hover"]
            )
        self.btn_angle.update_colors(
            self.colors["btn_header_bg"],
            self.colors["text_accent"],
            self.colors["btn_header_hover"]
        )
        self._update_memory_ui()

        # Memory buttons
        for key, btn in self.buttons.items():
            if key.startswith("mem_"):
                btn.update_colors(
                    self.colors["btn_header_bg"],
                    self.colors["btn_header_fg"],
                    self.colors["btn_header_hover"]
                )

        # Keypad buttons
        layout_categories = [
            ["sci", "sci", "sci", "sci", "sci"],
            ["sci", "sci", "sci", "sci", "sci"],
            ["sci", "sci", "sci", "sci", "sci"],
            ["fn", "fn", "fn", "del", "clear"],
            ["num", "num", "num", "op", "sci"],
            ["num", "num", "num", "op", "num"],
            ["num", "num", "num", "op", "sci"],
            ["num", "num", "eq", "op", "fn"],
        ]
        for row_idx, row in enumerate(layout_categories):
            for col_idx, category in enumerate(row):
                btn_key = f"btn_{row_idx}_{col_idx}"
                if btn_key in self.buttons:
                    bg, fg, hover = self._get_category_colors(category)
                    self.buttons[btn_key].update_colors(bg, fg, hover)

        # History panel
        self.history_panel.configure(
            bg=self.colors["history_bg"],
            highlightbackground=self.colors["border_color"]
        )
        self.hist_canvas.configure(bg=self.colors["history_bg"])
        self.hist_scroll_content.configure(bg=self.colors["history_bg"])
        self._refresh_history_ui()


def launch_gui():
    """Entrypoint function to run the Desktop Calculator GUI."""
    root = tk.Tk()
    app = ScientificCalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
