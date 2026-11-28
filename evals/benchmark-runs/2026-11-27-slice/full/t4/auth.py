import hashlib
import hmac
import secrets

ITERATIONS = 200_000
_GENERIC = "invalid username or password"


class AuthError(Exception):
    pass


def _hash(password, salt_hex):
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), ITERATIONS
    ).hex()


def register(store, username, password):
    if not isinstance(username, str) or not isinstance(password, str) or not username or not password:
        raise AuthError("username and password required")
    if username in store["users"]:
        raise AuthError("username already exists")
    salt = secrets.token_bytes(16).hex()
    store["users"][username] = {"salt": salt, "hash": _hash(password, salt)}


def login(store, username, password):
    rec = store["users"].get(username) if isinstance(username, str) else None
    if rec is None or not isinstance(password, str):
        # burn comparable work so unknown users are not timing-distinguishable
        _hash(password if isinstance(password, str) else "", "00" * 16)
        raise AuthError(_GENERIC)
    if not hmac.compare_digest(_hash(password, rec["salt"]), rec["hash"]):
        raise AuthError(_GENERIC)
    token = secrets.token_urlsafe(32)
    store["tokens"][token] = username
    return token


def user_for_token(store, token):
    if not isinstance(token, str) or not token:
        raise AuthError("invalid token")
    user = store["tokens"].get(token)
    if user is None:
        raise AuthError("invalid token")
    return user
