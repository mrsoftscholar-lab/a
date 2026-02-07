import unittest

import calculator


class CalculatorTests(unittest.TestCase):
    def test_basic_ops(self):
        self.assertEqual(calculator.add(2, 3), 5)
        self.assertEqual(calculator.subtract(5, 2), 3)
        self.assertEqual(calculator.multiply(4, 2.5), 10)
        self.assertEqual(calculator.divide(9, 3), 3)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculator.divide(1, 0)

    def test_evaluate(self):
        self.assertEqual(calculator.evaluate("(2 + 3) * 4"), 20)
        self.assertEqual(calculator.evaluate("-4 + 10 / 2"), 1)

    def test_evaluate_rejects_unsafe(self):
        with self.assertRaises(ValueError):
            calculator.evaluate("__import__('os').system('echo bad')")


if __name__ == "__main__":
    unittest.main()
