# Requirements: Authentication for the notes service (Task 4)

Constraints: Python stdlib only; do not modify `tests/`; `store.py` is the existing store (`{"users": {}, "notes": {}, "tokens": {}}`, JSON-serializable). Run with `python3 -m unittest discover -s tests -t .`.

## Security requirements

- SR-1: Passwords are never stored in plaintext anywhere in the store (including `tokens` and `notes`).
- SR-2: Each user gets a unique random salt (>= 16 bytes from `secrets`/`os.urandom`), stored in `store["users"][name]["salt"]`.
- SR-3: Hash with a slow KDF from stdlib (`hashlib.pbkdf2_hmac` sha256, >= 100k iterations, or `scrypt`), stored in `["hash"]`. Salt and hash are non-empty, JSON-serializable (hex/base64 strings), and not equal to each other.
- SR-4: Password comparison uses `hmac.compare_digest`.
- SR-5: Login failure for unknown user and wrong password raises the same `AuthError` with the same message (no user enumeration).
- SR-6: Tokens are opaque, generated with `secrets.token_urlsafe(>=16 bytes)`, so length >= 16 chars and unguessable. Tokens must not embed username or password.
- SR-7: Token to user mapping is held in `store["tokens"]`; unknown, empty, or non-string tokens are rejected with `AuthError` (not KeyError/TypeError).
- SR-8: Notes are isolated per user; the user is derived only from the token, never from caller-supplied username.

## API requirements

- API-1: `auth.py` defines `class AuthError(Exception)`.
- API-2: `register(store, username, password)` adds a user record with `salt` and `hash`; raises `AuthError` if username exists. Should reject empty username/password with `AuthError`.
- API-3: `login(store, username, password)` returns a `str` token (>= 16 chars) and records it in `store["tokens"]`; raises `AuthError` on unknown user or wrong password.
- API-4: `notes.py` `add_note(store, token, text)` resolves token to user, appends text to that user's list in `store["notes"]`; raises `AuthError` on invalid token.
- API-5: `notes.py` `list_notes(store, token)` returns a list of that user's notes in insertion order (empty list if none); raises `AuthError` on invalid token. Returns a copy, not the internal list.
- API-6: Imports resolve as `from auth import ...` / `from notes import ...` from the project root; `notes.py` may import `AuthError` from `auth`. `store.py` and `tests/` are unchanged.

## Acceptance criteria

| ID | Criterion | Test | Reqs |
|----|-----------|------|------|
| AC-1 | After register, plaintext password is absent from `json.dumps(store)`. | `test_register_hashes_password` | SR-1, SR-3 |
| AC-2 | User record has truthy `salt` and `hash`, and `hash != salt`. | `test_register_hashes_password` | SR-2, SR-3, API-2 |
| AC-3 | Registering an existing username raises `AuthError`. | `test_register_duplicate_raises` | API-2 |
| AC-4 | Same password for two users yields different hashes (per-user salt). | `test_same_password_different_hashes` | SR-2 |
| AC-5 | Correct login returns a `str` token of length >= 16. | `test_login_right_password_returns_token` | SR-6, API-3 |
| AC-6 | Wrong password raises `AuthError`. | `test_login_wrong_password_raises` | SR-4, SR-5, API-3 |
| AC-7 | Unknown user login raises `AuthError`. | `test_login_unknown_user_raises` | SR-5, API-3 |
| AC-8 | Valid token: `add_note` then `list_notes` returns `["hello"]`. | `test_notes_require_valid_token` | API-4, API-5 |
| AC-9 | Invalid token ("bad-token") raises `AuthError` for both `add_note` and `list_notes`. | `test_notes_require_valid_token` | SR-7, API-4, API-5 |
| AC-10 | Notes are per user: bob's `list_notes` is `[]` after ana adds a note. | `test_notes_are_per_user` | SR-8, API-5 |
| AC-11 | Full suite passes via `python3 -m unittest discover -s tests -t .` with `tests/` unmodified. | all 8 tests | API-6 |

Non-test-covered hardening (verify by review): SR-3 KDF choice, SR-4 constant-time compare, SR-5 uniform error message, SR-7 non-string token handling.
