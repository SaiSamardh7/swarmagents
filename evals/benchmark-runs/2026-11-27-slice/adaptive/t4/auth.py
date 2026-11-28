import hashlib, hmac, secrets


class AuthError(Exception):
    pass


def _hash(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), 200_000).hex()


def _token_key(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def register(store, username, password):
    if username in store["users"]:
        raise AuthError("username taken")
    salt = secrets.token_hex(16)
    store["users"][username] = {"salt": salt, "hash": _hash(password, salt)}


def login(store, username, password):
    rec = store["users"].get(username)
    # Compare against a dummy hash for unknown users to avoid a timing oracle.
    salt = rec["salt"] if rec else "00" * 16
    expected = rec["hash"] if rec else "0" * 64
    ok = hmac.compare_digest(_hash(password, salt), expected)
    if not rec or not ok:
        raise AuthError("invalid credentials")
    token = secrets.token_hex(16)
    store["tokens"][_token_key(token)] = username
    return token


def user_for_token(store, token):
    if not isinstance(token, str):
        raise AuthError("invalid token")
    user = store["tokens"].get(_token_key(token))
    if user is None:
        raise AuthError("invalid token")
    return user
