"""Record validation (the single source of truth)."""


def _check_record(r):
    if not isinstance(r, dict):
        raise ValueError("record must be a dict")
    if "category" not in r or "amount" not in r:
        raise ValueError("record needs category and amount")
    amount = r["amount"]
    if not isinstance(amount, (int, float)) or isinstance(amount, bool):
        raise ValueError("amount must be a number")
    if amount < 0:
        raise ValueError("amount must be non-negative")


def validate_records(records):
    """Return cleaned records or raise ValueError."""
    cleaned = []
    for r in records:
        _check_record(r)
        cleaned.append({"category": str(r["category"]), "amount": float(r["amount"])})
    return cleaned
