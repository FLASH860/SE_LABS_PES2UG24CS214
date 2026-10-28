import unittest
from calculator import calculate_discount


class TestCalculatorBranchCoverage(unittest.TestCase):
    """Test cases covering every True/False outcome of each decision."""

    def test_member_price_above_100(self):
        # is_member True, price > 100 True -> 15% discount
        self.assertAlmostEqual(calculate_discount(150, True), 127.5)

    def test_member_price_below_100(self):
        # is_member True, price > 100 False -> 10% discount
        self.assertAlmostEqual(calculate_discount(50, True), 45.0)

    def test_non_member_price_above_100(self):
        # is_member False, price > 100 True -> 5% discount
        self.assertAlmostEqual(calculate_discount(200, False), 190.0)

    def test_non_member_price_below_100(self):
        # is_member False, price > 100 False -> no discount
        self.assertAlmostEqual(calculate_discount(80, False), 80.0)

    def test_boundary_price_exactly_100(self):
        # Edge case: price == 100 is NOT > 100, so no extra 5%
        self.assertAlmostEqual(calculate_discount(100, True), 90.0)
        self.assertAlmostEqual(calculate_discount(100, False), 100.0)

    def test_boundary_price_just_above_100(self):
        # Edge case: price just above the threshold
        self.assertAlmostEqual(calculate_discount(100.01, False), 100.01 * 0.95)

    def test_zero_price(self):
        # Edge case: zero price gives zero regardless of membership
        self.assertAlmostEqual(calculate_discount(0, True), 0.0)
        self.assertAlmostEqual(calculate_discount(0, False), 0.0)


if __name__ == '__main__':
    unittest.main()
