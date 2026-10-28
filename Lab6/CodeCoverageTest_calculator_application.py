import unittest
from calculator import calculate_discount


class TestCalculatorCodeCoverage(unittest.TestCase):
    """Test cases targeting line (statement) coverage of calculator.py."""

    def test_member_expensive_item(self):
        # is_member True and price > 100 -> executes every line (15% discount)
        self.assertAlmostEqual(calculate_discount(150, True), 150 * 0.85)

    def test_member_large_price(self):
        # Another member purchase above 100
        self.assertAlmostEqual(calculate_discount(1000, True), 850.0)

    def test_return_value_type(self):
        # Result should be numeric
        self.assertIsInstance(calculate_discount(200, True), float)


if __name__ == '__main__':
    unittest.main()
