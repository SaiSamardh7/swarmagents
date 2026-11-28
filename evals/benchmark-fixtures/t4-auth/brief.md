# Task 4: Authentication integration

A tiny notes service (`store.py`) needs authentication. Implement, stdlib only:

- `auth.py`: `register(store, username, password)` storing a salted password hash
  (never the plaintext), raising `AuthError` on duplicate usernames;
  `login(store, username, password)` returning an opaque token string (>= 16 chars)
  and raising `AuthError` on a wrong password; class `AuthError(Exception)`.
- `notes.py`: `add_note(store, token, text)` and `list_notes(store, token)` that
  resolve the token to its user, raise `AuthError` for an invalid token, and keep
  notes per-user.

`tests/test_auth.py` specifies the behavior and currently fails. Make the suite pass
(`python3 -m unittest discover -s tests -t .`) without modifying tests/.
