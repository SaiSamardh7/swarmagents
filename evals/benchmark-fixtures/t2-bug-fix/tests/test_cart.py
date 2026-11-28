import unittest
from cart import item_total, cart_total

class TestCart(unittest.TestCase):
    def test_single_item(self):
        self.assertEqual(item_total(10.0, 1), 10.0)
    def test_no_discount_below_threshold(self):
        self.assertEqual(item_total(10.0, 9), 90.0)
    def test_bulk_discount_at_threshold(self):
        self.assertEqual(item_total(10.0, 10), 85.0)
    def test_bulk_discount_above_threshold(self):
        self.assertEqual(item_total(10.0, 20), 170.0)
    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            item_total(-1.0, 2)
    def test_cart_total_applies_tax(self):
        self.assertEqual(cart_total([(10.0, 1), (5.0, 2)]), 21.6)

if __name__ == "__main__":
    unittest.main()
