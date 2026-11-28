#!/usr/bin/env python3
"""Deterministic grader for T1. Usage: python3 grade.py <workdir>"""
import re, sys, pathlib
d = pathlib.Path(sys.argv[1])
html_path = d / "index.html"
checks = []
def check(name, ok): checks.append((name, bool(ok)))
if not html_path.exists():
    check("index.html exists", False)
else:
    h = html_path.read_text(encoding="utf-8")
    low = h.lower()
    css = h
    for p in d.glob("*.css"): css += p.read_text(encoding="utf-8")
    check("index.html exists", True)
    check("html lang attribute", re.search(r"<html[^>]*\blang=", low))
    check("meta viewport", "viewport" in low)
    check("exactly one h1", len(re.findall(r"<h1[\s>]", low)) == 1)
    check("hero mentions Lumen", "lumen" in low)
    check("call-to-action link", re.search(r"<a[^>]*href=", low))
    check("3 pricing tiers", all(t in low for t in ("free", "pro", "team")))
    check("FAQ present", "faq" in low or "frequently asked" in low)
    check("footer element", "<footer" in low)
    check("media query", "@media" in css)
    imgs = re.findall(r"<img\b[^>]*>", low)
    check("img alt text", all("alt=" in i for i in imgs))
passed = sum(1 for _, ok in checks if ok)
for name, ok in checks: print(("PASS" if ok else "FAIL"), name)
print(f"SCORE {passed}/{len(checks)}")
sys.exit(0 if passed == len(checks) else 1)
