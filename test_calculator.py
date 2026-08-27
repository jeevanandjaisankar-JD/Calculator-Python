"""
Unit tests for the Scientific Calculator Engine.
"""

import math
import unittest
from calculator_engine import CalculatorEngine, CalculatorError


class TestCalculatorEngine(unittest.TestCase):

    def setUp(self):
        self.engine = CalculatorEngine()

    def test_basic_arithmetic(self):
        ok, res = self.engine.evaluate("2 + 3")
        self.assertTrue(ok)
        self.assertEqual(res, "5")

        ok, res = self.engine.evaluate("10 - 4")
        self.assertTrue(ok)
        self.assertEqual(res, "6")

        ok, res = self.engine.evaluate("7 * 8")
        self.assertTrue(ok)
        self.assertEqual(res, "56")

        ok, res = self.engine.evaluate("15 / 3")
        self.assertTrue(ok)
        self.assertEqual(res, "5")

        ok, res = self.engine.evaluate("10 % 3")
        self.assertTrue(ok)
        self.assertEqual(res, "1")

        ok, res = self.engine.evaluate("2 ^ 3")
        self.assertTrue(ok)
        self.assertEqual(res, "8")

    def test_unicode_and_display_operators(self):
        ok, res = self.engine.evaluate("4 × 5")
        self.assertTrue(ok)
        self.assertEqual(res, "20")

        ok, res = self.engine.evaluate("10 ÷ 2")
        self.assertTrue(ok)
        self.assertEqual(res, "5")

        ok, res = self.engine.evaluate("8 − 3")
        self.assertTrue(ok)
        self.assertEqual(res, "5")

    def test_order_of_operations_and_parentheses(self):
        ok, res = self.engine.evaluate("2 + 3 * 4")
        self.assertTrue(ok)
        self.assertEqual(res, "14")

        ok, res = self.engine.evaluate("(2 + 3) * 4")
        self.assertTrue(ok)
        self.assertEqual(res, "20")

        ok, res = self.engine.evaluate("-(5 + 3)")
        self.assertTrue(ok)
        self.assertEqual(res, "-8")

    def test_scientific_functions(self):
        # Square root
        ok, res = self.engine.evaluate("sqrt(144)")
        self.assertTrue(ok)
        self.assertEqual(res, "12")

        # Cube root
        ok, res = self.engine.evaluate("cbrt(27)")
        self.assertTrue(ok)
        self.assertEqual(res, "3")

        # Factorial
        ok, res = self.engine.evaluate("fact(5)")
        self.assertTrue(ok)
        self.assertEqual(res, "120")

        # Logarithms
        ok, res = self.engine.evaluate("log(100)")
        self.assertTrue(ok)
        self.assertEqual(res, "2")

        ok, res = self.engine.evaluate("ln(e)")
        self.assertTrue(ok)
        self.assertEqual(res, "1")

        # Constants
        ok, res = self.engine.evaluate("2 * pi")
        self.assertTrue(ok)
        self.assertAlmostEqual(float(res), 2 * math.pi, places=5)

    def test_trigonometry_degree_and_radian_modes(self):
        # Default is DEG
        self.assertEqual(self.engine.angle_mode, "DEG")
        ok, res = self.engine.evaluate("sin(30)")
        self.assertTrue(ok)
        self.assertAlmostEqual(float(res), 0.5, places=5)

        ok, res = self.engine.evaluate("cos(60)")
        self.assertTrue(ok)
        self.assertAlmostEqual(float(res), 0.5, places=5)

        ok, res = self.engine.evaluate("tan(45)")
        self.assertTrue(ok)
        self.assertAlmostEqual(float(res), 1.0, places=5)

        # Toggle to RAD
        self.engine.toggle_angle_mode()
        self.assertEqual(self.engine.angle_mode, "RAD")

        ok, res = self.engine.evaluate("sin(pi / 6)")
        self.assertTrue(ok)
        self.assertAlmostEqual(float(res), 0.5, places=5)

        ok, res = self.engine.evaluate("cos(0)")
        self.assertTrue(ok)
        self.assertEqual(res, "1")

    def test_error_handling(self):
        # Division by zero
        ok, res = self.engine.evaluate("5 / 0")
        self.assertFalse(ok)
        self.assertIn("Division by zero", res)

        # Modulo by zero
        ok, res = self.engine.evaluate("5 % 0")
        self.assertFalse(ok)
        self.assertIn("Division by zero", res)

        # Negative square root
        ok, res = self.engine.evaluate("sqrt(-9)")
        self.assertFalse(ok)
        self.assertIn("negative number", res)

        # Negative log
        ok, res = self.engine.evaluate("log(-10)")
        self.assertFalse(ok)
        self.assertIn("positive numbers", res)

        # Negative factorial
        ok, res = self.engine.evaluate("fact(-3)")
        self.assertFalse(ok)
        self.assertIn("non-negative", res)

        # Non-integer factorial
        ok, res = self.engine.evaluate("fact(3.5)")
        self.assertFalse(ok)
        self.assertIn("integer", res)

        # Syntax error
        ok, res = self.engine.evaluate("5 ++ * 2")
        self.assertFalse(ok)
        self.assertIn("Invalid expression", res)

    def test_memory_bank(self):
        self.assertFalse(self.engine.memory_active)
        self.engine.memory_store(50)
        self.assertTrue(self.engine.memory_active)
        self.assertEqual(self.engine.memory_recall(), 50.0)

        self.engine.memory_add(25)
        self.assertEqual(self.engine.memory_recall(), 75.0)

        self.engine.memory_subtract(10)
        self.assertEqual(self.engine.memory_recall(), 65.0)

        self.engine.memory_clear()
        self.assertFalse(self.engine.memory_active)
        self.assertEqual(self.engine.memory_recall(), 0.0)

    def test_history(self):
        self.engine.evaluate("10 + 20")
        self.engine.evaluate("sqrt(16)")
        history = self.engine.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["expression"], "sqrt(16)")
        self.assertEqual(history[0]["result"], "4")
        self.assertEqual(history[1]["expression"], "10 + 20")
        self.assertEqual(history[1]["result"], "30")

        self.engine.clear_history()
        self.assertEqual(len(self.engine.get_history()), 0)


if __name__ == "__main__":
    unittest.main()
