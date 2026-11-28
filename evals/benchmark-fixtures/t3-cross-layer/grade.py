#!/usr/bin/env python3
"""Grader for T3: full suite passes, test files unmodified. Usage: python3 grade.py <workdir>"""
import hashlib, pathlib, subprocess, sys
d = pathlib.Path(sys.argv[1])
fixture = pathlib.Path(__file__).parent
ok_tests = True
for name in ("test_core.py", "test_archive.py"):
    a, b = fixture / "tests" / name, d / "tests" / name
    same = b.exists() and hashlib.sha256(a.read_bytes()).digest() == hashlib.sha256(b.read_bytes()).digest()
    print(("PASS" if same else "FAIL"), f"{name} unmodified"); ok_tests = ok_tests and same
r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."], cwd=d, capture_output=True, text=True)
ok = r.returncode == 0
print(("PASS" if ok else "FAIL"), "test suite")
print(r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "")
print(f"SCORE {int(ok_tests)+int(ok)}/2")
sys.exit(0 if ok_tests and ok else 1)
