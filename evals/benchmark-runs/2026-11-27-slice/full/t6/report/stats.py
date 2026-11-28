"""Aggregation: total, count, average, per-category sums."""
from report.validate import clean

PRECISION = 2


def aggregate(cleaned):
    """Unrounded aggregates over already-validated records."""
    total = 0.0
    by_category = {}
    for rec in cleaned:
        total += rec["amount"]
        by_category[rec["category"]] = by_category.get(rec["category"], 0.0) + rec["amount"]
    count = len(cleaned)
    average = round(total / count, PRECISION) if count else 0.0
    return {"total": total, "count": count, "average": average,
            "by_category": by_category}


def summarize(records):
    agg = aggregate(clean(records))
    return {"total": round(agg["total"], PRECISION), "count": agg["count"],
            "average": agg["average"],
            "by_category": {k: round(v, PRECISION)
                            for k, v in sorted(agg["by_category"].items())}}
