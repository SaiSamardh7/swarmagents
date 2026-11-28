# Task 9: Security-sensitive change

`userdb.py` works but has security flaws: SQL built by string interpolation
(injectable) and plaintext password storage. Fix it, stdlib only:

- All SQL uses parameterized queries; a malicious search filter returns no spurious
  rows and cannot execute statements.
- Passwords are stored as salted hashes (never plaintext); `login` still returns
  True/False exactly as before.
- The public API (`connect`, `register`, `find_users`, `login`) keeps its signatures.

`tests/test_basic.py` passes today and must keep passing. `tests/test_security.py`
currently fails; make the whole suite pass
(`python3 -m unittest discover -s tests -t .`) without modifying tests/.
grade.py also statically rejects interpolated SQL.
