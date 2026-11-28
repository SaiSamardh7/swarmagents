"""Legacy reporting monolith. Known mess; see brief.md."""
_CACHE = {}

def summarize(records):
    cleaned = []
    for r in records:
        if not isinstance(r, dict):
            raise ValueError("record must be a dict")
        if "category" not in r or "amount" not in r:
            raise ValueError("record needs category and amount")
        if not isinstance(r["amount"], (int, float)) or isinstance(r["amount"], bool):
            raise ValueError("amount must be a number")
        if r["amount"] < 0:
            raise ValueError("amount must be non-negative")
        cleaned.append({"category": str(r["category"]), "amount": float(r["amount"])})
    total = 0.0
    by_category = {}
    for c in cleaned:
        total += c["amount"]
        by_category[c["category"]] = by_category.get(c["category"], 0.0) + c["amount"]
    count = len(cleaned)
    average = round(total / count, 2) if count else 0.0
    result = {"total": round(total, 2), "count": count, "average": average,
              "by_category": {k: round(v, 2) for k, v in sorted(by_category.items())}}
    _CACHE["last"] = result
    return result

def generate_report(records, fmt):
    cleaned = []
    for r in records:
        if not isinstance(r, dict):
            raise ValueError("record must be a dict")
        if "category" not in r or "amount" not in r:
            raise ValueError("record needs category and amount")
        if not isinstance(r["amount"], (int, float)) or isinstance(r["amount"], bool):
            raise ValueError("amount must be a number")
        if r["amount"] < 0:
            raise ValueError("amount must be non-negative")
        cleaned.append({"category": str(r["category"]), "amount": float(r["amount"])})
    if fmt == "text":
        total = 0.0
        by_category = {}
        for c in cleaned:
            total += c["amount"]
            by_category[c["category"]] = by_category.get(c["category"], 0.0) + c["amount"]
        lines = ["REPORT"]
        for k in sorted(by_category):
            lines.append("%-12s %10.2f" % (k, by_category[k]))
        lines.append("%-12s %10.2f" % ("TOTAL", total))
        count = len(cleaned)
        lines.append("%-12s %10d" % ("COUNT", count))
        avg = round(total / count, 2) if count else 0.0
        lines.append("%-12s %10.2f" % ("AVERAGE", avg))
        out = "\n".join(lines)
        _CACHE["last_text"] = out
        return out
    elif fmt == "csv":
        again = []
        for r in records:
            if not isinstance(r, dict):
                raise ValueError("record must be a dict")
            if "category" not in r or "amount" not in r:
                raise ValueError("record needs category and amount")
            if not isinstance(r["amount"], (int, float)) or isinstance(r["amount"], bool):
                raise ValueError("amount must be a number")
            if r["amount"] < 0:
                raise ValueError("amount must be non-negative")
            again.append({"category": str(r["category"]), "amount": float(r["amount"])})
        lines = ["category,amount"]
        for c in again:
            lines.append("%s,%.2f" % (c["category"], c["amount"]))
        return "\n".join(lines)
    else:
        raise ValueError("unknown format: %s" % fmt)
