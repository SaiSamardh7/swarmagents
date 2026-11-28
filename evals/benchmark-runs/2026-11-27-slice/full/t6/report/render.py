"""Text and csv rendering plus format dispatch."""
from report.stats import PRECISION, aggregate
from report.validate import clean

FORMAT_TEXT = "text"
FORMAT_CSV = "csv"
TITLE = "REPORT"
CSV_HEADER = "category,amount"
LABEL_TOTAL = "TOTAL"
LABEL_COUNT = "COUNT"
LABEL_AVERAGE = "AVERAGE"
LABEL_WIDTH = 12
VALUE_WIDTH = 10
LINE_AMOUNT = "%-" + str(LABEL_WIDTH) + "s %" + str(VALUE_WIDTH) + "." + str(PRECISION) + "f"
LINE_COUNT = "%-" + str(LABEL_WIDTH) + "s %" + str(VALUE_WIDTH) + "d"
CSV_LINE = "%s,%." + str(PRECISION) + "f"
UNKNOWN_FORMAT = "unknown format: %s"


def _render_text(cleaned):
    agg = aggregate(cleaned)
    lines = [TITLE]
    for key in sorted(agg["by_category"]):
        lines.append(LINE_AMOUNT % (key, agg["by_category"][key]))
    lines.append(LINE_AMOUNT % (LABEL_TOTAL, agg["total"]))
    lines.append(LINE_COUNT % (LABEL_COUNT, agg["count"]))
    lines.append(LINE_AMOUNT % (LABEL_AVERAGE, agg["average"]))
    return "\n".join(lines)


def _render_csv(cleaned):
    lines = [CSV_HEADER]
    for c in cleaned:
        lines.append(CSV_LINE % (c["category"], c["amount"]))
    return "\n".join(lines)


def generate_report(records, fmt):
    cleaned = clean(records)
    if fmt == FORMAT_TEXT:
        return _render_text(cleaned)
    if fmt == FORMAT_CSV:
        return _render_csv(cleaned)
    raise ValueError(UNKNOWN_FORMAT % fmt)
