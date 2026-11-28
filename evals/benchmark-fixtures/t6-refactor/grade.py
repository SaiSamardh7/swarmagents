#!/usr/bin/env python3
import ast, hashlib, pathlib, subprocess, sys
d = pathlib.Path(sys.argv[1]); fixture = pathlib.Path(__file__).parent
checks = []
def check(name, ok): checks.append((name, bool(ok)))
a, b = fixture / "tests" / "test_report.py", d / "tests" / "test_report.py"
check("tests unmodified", b.exists() and hashlib.sha256(a.read_bytes()).digest() == hashlib.sha256(b.read_bytes()).digest())
r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."], cwd=d, capture_output=True, text=True)
check("test suite", r.returncode == 0)
check("legacy.py deleted", not (d / "legacy.py").exists())
for m in ("validate.py", "stats.py", "render.py", "__init__.py"):
    check(f"report/{m} exists", (d / "report" / m).exists())
long_funcs, shim = [], False
for p in (d / "report").glob("*.py"):
    src = p.read_text(encoding="utf-8")
    if "legacy" in src: shim = True
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            span = (node.end_lineno or node.lineno) - node.lineno + 1
            if span > 40: long_funcs.append(f"{p.name}:{node.name}({span})")
check("no legacy references in report/", not shim)
check("no function over 40 lines", not long_funcs)
if long_funcs: print("  long:", ", ".join(long_funcs))
passed = sum(1 for _, ok in checks if ok)
for name, ok in checks: print(("PASS" if ok else "FAIL"), name)
print(f"SCORE {passed}/{len(checks)}"); sys.exit(0 if passed == len(checks) else 1)
