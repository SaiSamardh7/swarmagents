# Requirements: Bulk discount threshold bug (t2)

## Problem statement
`item_total(price, qty)` in `cart.py` does not apply the 15% bulk discount at exactly 10 units. The module docstring and the brief both say the discount applies at `BULK_THRESHOLD` (10) units and above. `test_bulk_discount_at_threshold` expects `item_total(10.0, 10) == 85.0` but gets `100.0`.

## Root-cause hypothesis
The condition in `item_total` is `qty > BULK_THRESHOLD` (strict). It should be `qty >= BULK_THRESHOLD`. This is an off-by-one boundary error. Nothing else is implicated: `BULK_THRESHOLD` is 10, the discount constant is correct, and `cart_total` only delegates to `item_total`.

## Acceptance criteria
- AC-1: `item_total(10.0, 10)` returns `85.0` (discount applies at exactly the threshold).
- AC-2: `item_total(10.0, 9)` returns `90.0` (no discount below the threshold).
- AC-3: `item_total(10.0, 20)` returns `170.0` (discount still applies above the threshold).
- AC-4: `item_total` still raises `ValueError` for negative price or qty.
- AC-5: `cart_total([(10.0, 1), (5.0, 2)])` still returns `21.6`.
- AC-6: `python3 -m unittest discover -s tests` passes with all 6 tests green.
- AC-7: `tests/test_cart.py` is unmodified, and the change to `cart.py` is limited to the threshold comparison (no constants or signatures changed).
