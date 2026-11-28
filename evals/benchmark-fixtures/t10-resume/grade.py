#!/usr/bin/env python3
import hashlib, pathlib, re, subprocess, sys
d = pathlib.Path(sys.argv[1]); fixture = pathlib.Path(__file__).parent
checks = []
def check(name, ok): checks.append((name, bool(ok)))
for name in ("test_base.py", "test_export.py", "test_stats.py"):
    a, b = fixture / "tests" / name, d / "tests" / name
    check(f"{name} unmodified", b.exists() and hashlib.sha256(a.read_bytes()).digest() == hashlib.sha256(b.read_bytes()).digest())
r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."], cwd=d, capture_output=True, text=True)
check("test suite", r.returncode == 0)
wg = (d / ".swarmagents" / "runs" / "run-01" / "workgraph.yml").read_text(encoding="utf-8")
resume_ok = True
for m in re.finditer(r"artifact: (\S+), sha256: ([0-9a-f]{64})", wg):
    f = d / m.group(1)
    same = f.exists() and hashlib.sha256(f.read_bytes()).hexdigest() == m.group(2)
    check(f"done artifact untouched: {m.group(1)}", same); resume_ok = resume_ok and same
passed = sum(1 for _, ok in checks if ok)
for name, ok in checks: print(("PASS" if ok else "FAIL"), name)
print(f"SCORE {passed}/{len(checks)}"); sys.exit(0 if passed == len(checks) else 1)
