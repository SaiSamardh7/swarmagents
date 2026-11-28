"""Report rendering and generate_report."""
from .stats import compute_stats
from .validate import validate_records

LABEL_WIDTH = 12
NUM_WIDTH = 10


def _row(label, value, spec):
    return ("%%-%ds %%%d%s" % (LABEL_WIDTH, NUM_WIDTH, spec)) % (label, value)


def render_text(cleaned):
    s = compute_stats(cleaned)
    lines = ["REPORT"]
    for k in sorted(s["by_category"]):
        lines.append(_row(k, s["by_category"][k], ".2f"))
    lines.append(_row("TOTAL", s["total"], ".2f"))
    lines.append(_row("COUNT", s["count"], "d"))
    lines.append(_row("AVERAGE", s["average"], ".2f"))
    return "\n".join(lines)


def render_csv(cleaned):
    lines = ["category,amount"]
    for c in cleaned:
        lines.append("%s,%.2f" % (c["category"], c["amount"]))
    return "\n".join(lines)


_RENDERERS = {"text": render_text, "csv": render_csv}


def generate_report(records, fmt):
    cleaned = validate_records(records)
    if fmt not in _RENDERERS:
        raise ValueError("unknown format: %s" % fmt)
    return _RENDERERS[fmt](cleaned)
