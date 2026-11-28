#!/usr/bin/env python3
import hashlib, pathlib, subprocess, sys
d = pathlib.Path(sys.argv[1]); fixture = pathlib.Path(__file__).parent
ok = True
for name in ("test_migration.py",):
    a, b = fixture / "tests" / name, d / "tests" / name
    same = b.exists() and hashlib.sha256(a.read_bytes()).digest() == hashlib.sha256(b.read_bytes()).digest()
    print(("PASS" if same else "FAIL"), f"{name} unmodified"); ok = ok and same
r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."], cwd=d, capture_output=True, text=True)
suite = r.returncode == 0
print(("PASS" if suite else "FAIL"), "test suite")
print(r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "")
print(f"SCORE {int(ok)+int(suite)}/2"); sys.exit(0 if ok and suite else 1)
