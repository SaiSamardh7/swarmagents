"""Record validation and normalization."""

ERR_NOT_DICT = "record must be a dict"
ERR_MISSING = "record needs category and amount"
ERR_NOT_NUMBER = "amount must be a number"
ERR_NEGATIVE = "amount must be non-negative"


def _check(record):
    if not isinstance(record, dict):
        raise ValueError(ERR_NOT_DICT)
    if "category" not in record or "amount" not in record:
        raise ValueError(ERR_MISSING)
    amount = record["amount"]
    if not isinstance(amount, (int, float)) or isinstance(amount, bool):
        raise ValueError(ERR_NOT_NUMBER)
    if amount < 0:
        raise ValueError(ERR_NEGATIVE)


def _normalize(record):
    return {"category": str(record["category"]), "amount": float(record["amount"])}


def clean(records):
    """Validate records in input order; return normalized copies."""
    cleaned = []
    for record in records:
        _check(record)
        cleaned.append(_normalize(record))
    return cleaned
