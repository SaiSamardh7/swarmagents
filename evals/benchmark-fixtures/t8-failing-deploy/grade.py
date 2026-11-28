#!/usr/bin/env python3
import pathlib, re, subprocess, sys
d = pathlib.Path(sys.argv[1])
checks = []
def check(name, ok): checks.append((name, bool(ok)))
r1 = subprocess.run([sys.executable, "build.py"], cwd=d, capture_output=True, text=True)
r2 = subprocess.run([sys.executable, "build.py"], cwd=d, capture_output=True, text=True)
check("build succeeds", r1.returncode == 0)
check("build idempotent (second run)", r2.returncode == 0)
idx, abt = d / "dist" / "index.html", d / "dist" / "about.html"
check("dist/index.html exists", idx.exists())
check("dist/about.html exists", abt.exists())
if idx.exists():
    h = idx.read_text(encoding="utf-8")
    check("index title rendered", "Acme Home" in h)
    check("contact email rendered", re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", h) and "{contact_email}" not in h)
if abt.exists():
    check("about title rendered", "About Acme" in abt.read_text(encoding="utf-8"))
passed = sum(1 for _, ok in checks if ok)
for name, ok in checks: print(("PASS" if ok else "FAIL"), name)
print(f"SCORE {passed}/{len(checks)}"); sys.exit(0 if passed == len(checks) else 1)
