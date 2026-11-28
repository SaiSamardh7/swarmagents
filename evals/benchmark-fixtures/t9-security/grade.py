#!/usr/bin/env python3
import hashlib, pathlib, re, subprocess, sys
d = pathlib.Path(sys.argv[1]); fixture = pathlib.Path(__file__).parent
checks = []
def check(name, ok): checks.append((name, bool(ok)))
for name in ("test_basic.py", "test_security.py"):
    a, b = fixture / "tests" / name, d / "tests" / name
    check(f"{name} unmodified", b.exists() and hashlib.sha256(a.read_bytes()).digest() == hashlib.sha256(b.read_bytes()).digest())
r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."], cwd=d, capture_output=True, text=True)
check("test suite", r.returncode == 0)
src = (d / "userdb.py").read_text(encoding="utf-8") if (d / "userdb.py").exists() else ""
bad = re.search(r'execute\(\s*f["\']', src) or re.search(r'execute\([^)]*\.format\(', src) or re.search(r'execute\([^)]*%\s*\(', src)
check("no interpolated SQL in userdb.py", src and not bad)
passed = sum(1 for _, ok in checks if ok)
for name, ok in checks: print(("PASS" if ok else "FAIL"), name)
print(f"SCORE {passed}/{len(checks)}"); sys.exit(0 if passed == len(checks) else 1)
