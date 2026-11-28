"""Cart pricing. Bulk discount applies at BULK_THRESHOLD units and above."""
TAX_RATE = 0.08
BULK_THRESHOLD = 10
BULK_DISCOUNT = 0.15

def item_total(price, qty):
    if price < 0 or qty < 0:
        raise ValueError("price and qty must be non-negative")
    subtotal = price * qty
    if qty >= BULK_THRESHOLD:
        subtotal *= (1 - BULK_DISCOUNT)
    return round(subtotal, 2)

def cart_total(items):
    subtotal = sum(item_total(price, qty) for price, qty in items)
    return round(subtotal * (1 + TAX_RATE), 2)
