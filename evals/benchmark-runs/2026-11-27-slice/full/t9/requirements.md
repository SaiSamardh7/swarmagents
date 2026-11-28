# Requirements: userdb security fix (Task 9)

## Scope
Fix `userdb.py` (stdlib only). Public API unchanged: `connect(path)`, `register(conn, name, password)`, `find_users(conn, name_filter)`, `login(conn, name, password)`. Do not modify `tests/`. Suite command: `python3 -m unittest discover -s tests -t .`. `grade.py` statically rejects interpolated SQL.

## Vulnerability classes present
| ID | Class | Location | Detail |
|----|-------|----------|--------|
| V1 | SQL injection (CWE-89), string-interpolated SQL | `register` | f-string INSERT with `name` and `password`; quote in input breaks or alters the statement |
| V2 | SQL injection | `find_users` | f-string `LIKE '%{name_filter}%'`; `%' OR '1'='1` matches all rows; `'; DROP TABLE` stacked-statement attempt |
| V3 | SQL injection | `login` | f-string SELECT with `name`; auth bypass via `' OR '1'='1` |
| V4 | Plaintext password storage (CWE-256/312) | `register`, `login` | password stored and compared as-is |
| V5 | Non-constant-time secret comparison (CWE-208), minor | `login` | `row[0] == password` |
| V6 | LIKE wildcard injection (minor) | `find_users` | user-supplied `%` and `_` act as wildcards even when parameterized |

## Security requirements
- SR1: Every SQL statement uses `?` placeholders with a params tuple. No f-strings, `%` formatting, `.format`, or concatenation to build SQL (including the `CREATE TABLE` in `connect`, which is already static).
- SR2: Passwords are stored only as a salted, slow, stdlib hash: `hashlib.scrypt` or `hashlib.pbkdf2_hmac` (SHA-256, at least 100k iterations), with a per-user random salt from `os.urandom` or `secrets` (at least 16 bytes). The stored value is a self-describing string (e.g. `algo$params$salt_hex$hash_hex`) in the existing `password` column. No schema change is required.
- SR3: `login` re-derives the hash with the stored salt and parameters and compares with `hmac.compare_digest`. It returns exactly `True` or `False`. An unknown user, wrong password, or malformed stored value returns `False` and never raises.
- SR4: `find_users` binds the filter as a parameter (`LIKE ? ESCAPE '\'`). Escape `\`, `%`, `_` in the filter so it is matched literally. Keep the `ORDER BY name` ordering and the `[(name,), ...]` return shape.
- SR5: `register` for a duplicate name keeps the existing behavior (`sqlite3.IntegrityError` from the UNIQUE constraint). Names containing quotes (e.g. `o'hara`) are stored and retrieved verbatim.
- SR6: Do not log or return plaintext passwords. Do not weaken existing behavior; no new third-party dependencies.

## Acceptance criteria
| AC | Criterion | Maps to test | Covers |
|----|-----------|--------------|--------|
| AC1 | Stored `password` value is not equal to, and does not contain, the plaintext | `test_security.TestSecurity.test_password_not_stored_in_plaintext` | V4, SR2 |
| AC2 | `login` returns True for the correct password and False for a wrong one, with hashing in place | `test_security.TestSecurity.test_login_still_works_with_hashing` | V4, SR2, SR3 |
| AC3 | `find_users(conn, "%' OR '1'='1")` returns `[]` | `test_security.TestSecurity.test_find_users_injection_returns_nothing` | V2, SR1, SR4 |
| AC4 | `find_users(conn, "x'; DROP TABLE users; --")` returns `[]` and the users table still holds 1 row | `test_security.TestSecurity.test_find_users_statement_injection_harmless` | V2, SR1 |
| AC5 | `register` accepts `o'hara`; `find_users("hara")` returns `[("o'hara",)]` | `test_security.TestSecurity.test_register_with_quote_in_name` | V1, SR1, SR5 |
| AC6 | register + substring search still works; non-matching filter returns `[]` | `test_basic.TestBasic.test_register_and_find` | regression, SR4 |
| AC7 | `login` True for the right password, False for a wrong password, False for an unknown user | `test_basic.TestBasic.test_login` | regression, V3, SR3 |
| AC8 | Whole suite passes via `python3 -m unittest discover -s tests -t .`; `tests/` unmodified | all 7 tests | all |
| AC9 | Static check: no interpolated SQL anywhere in `userdb.py` (no f-string, `%`, `.format`, or `+` building SQL passed to `execute`) | `grade.py` (no unit test) | V1-V3, SR1 |
| AC10 | Public signatures of `connect`, `register`, `find_users`, `login` are unchanged; `login` returns a real `bool` | `test_basic`, `test_security` (implicit); review | brief, SR3 |
| AC11 | Per-user random salt: two users with the same password have different stored values | no existing test; reviewer or QA check | SR2 |
| AC12 | `find_users` treats `%` and `_` literally (e.g. filter `%` returns no rows when no name contains `%`) | no existing test; reviewer or QA check | V6, SR4 |
| AC13 | `login` with a malformed stored value or an injection-style name (`' OR '1'='1`) returns False without raising | no existing test; reviewer or QA check | V3, SR3 |

AC1-AC8 are covered by existing tests. AC9 is covered by `grade.py`. AC11-AC13 have no existing test and cannot add tests under `tests/`, so QA verifies them with ad-hoc checks.

## Out of scope
Schema migration of existing plaintext rows, password policy, rate limiting, and user deletion.
