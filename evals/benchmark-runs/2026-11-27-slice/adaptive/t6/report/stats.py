"""Aggregate statistics."""

ROUND_DIGITS = 2


def compute_stats(cleaned):
    total = 0.0
    by_category = {}
    for c in cleaned:
        total += c["amount"]
        by_category[c["category"]] = by_category.get(c["category"], 0.0) + c["amount"]
    count = len(cleaned)
    average = round(total / count, ROUND_DIGITS) if count else 0.0
    return {"total": total, "count": count, "average": average,
            "by_category": by_category}


def summarize(records):
    from .validate import validate_records
    s = compute_stats(validate_records(records))
    return {"total": round(s["total"], ROUND_DIGITS), "count": s["count"],
            "average": s["average"],
            "by_category": {k: round(v, ROUND_DIGITS)
                            for k, v in sorted(s["by_category"].items())}}
