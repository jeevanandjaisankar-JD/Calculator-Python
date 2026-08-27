"""
GUI Integration Tests for ScientificCalculatorGUI.
"""

import tkinter as tk
import unittest
from gui import ScientificCalculatorGUI


class TestCalculatorGUI(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = ScientificCalculatorGUI(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_basic_calc_flow(self):
        self.app._insert_digit("1")
        self.app._insert_digit("2")
        self.app._insert_operator("+")
        self.app._insert_digit("8")
        self.app._on_calculate()
        self.assertEqual(self.app.current_input, "20")
        self.assertEqual(self.app.expression_preview, "12 + 8 =")

    def test_scientific_input_flow(self):
        self.app._insert_function("sqrt(")
        self.app._insert_digit("8")
        self.app._insert_digit("1")
        self.app._insert_symbol(")")
        self.app._on_calculate()
        self.assertEqual(self.app.current_input, "9")

    def test_trigonometry_angle_toggle(self):
        self.assertEqual(self.app.engine.angle_mode, "DEG")
        self.app._insert_function("sin(")
        self.app._insert_digit("3")
        self.app._insert_digit("0")
        self.app._insert_symbol(")")
        self.app._on_calculate()
        self.assertAlmostEqual(float(self.app.current_input), 0.5, places=4)

        # Toggle to RAD
        self.app._on_toggle_angle()
        self.assertEqual(self.app.engine.angle_mode, "RAD")

    def test_unary_and_reciprocal(self):
        self.app.current_input = "4"
        self.app._apply_unary_op("** 2")
        self.app._on_calculate()
        self.assertEqual(self.app.current_input, "16")

        self.app.current_input = "5"
        self.app._on_reciprocal()
        self.app._on_calculate()
        self.assertEqual(self.app.current_input, "0.2")

    def test_memory_flow(self):
        self.app.current_input = "50"
        self.app._on_memory_store()
        self.assertTrue(self.app.engine.memory_active)
        self.assertEqual(self.app.engine.memory_recall(), 50.0)

        self.app.current_input = "10"
        self.app._on_memory_add()
        self.assertEqual(self.app.engine.memory_recall(), 60.0)

        self.app._on_clear()
        self.app._on_memory_recall()
        self.assertEqual(self.app.current_input, "60")

        self.app._on_memory_clear()
        self.assertFalse(self.app.engine.memory_active)

    def test_history_toggle_and_recall(self):
        self.assertFalse(self.app.history_visible)
        self.app._toggle_history()
        self.assertTrue(self.app.history_visible)

        self.app._insert_digit("7")
        self.app._insert_operator("*")
        self.app._insert_digit("6")
        self.app._on_calculate()
        self.assertEqual(self.app.current_input, "42")

        # Load history item
        self.app._load_history_result("42")
        self.assertEqual(self.app.current_input, "42")

        self.app._toggle_history()
        self.assertFalse(self.app.history_visible)

    def test_theme_toggle(self):
        self.assertEqual(self.app.current_theme, "dark")
        self.app._toggle_theme()
        self.assertEqual(self.app.current_theme, "light")
        self.app._toggle_theme()
        self.assertEqual(self.app.current_theme, "dark")

    def test_backspace_and_clear(self):
        self.app._insert_digit("1")
        self.app._insert_digit("2")
        self.app._insert_digit("3")
        self.app._on_backspace()
        self.assertEqual(self.app.current_input, "12")
        self.app._on_clear()
        self.assertEqual(self.app.current_input, "0")


if __name__ == "__main__":
    unittest.main()
