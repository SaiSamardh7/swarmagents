# Task 2: Small bug fix

`python3 -m unittest discover -s tests` fails: `test_bulk_discount_at_threshold` in
`tests/test_cart.py`. The bulk discount is documented to apply **at** 10 units and above.
Fix the bug in `cart.py` without modifying the tests, and keep every other test passing.
