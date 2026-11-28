import hashlib
import hmac
import secrets
import sqlite3

_ALGO = "pbkdf2_sha256"
_ITERATIONS = 200_000


def _hash_password(password, salt, iterations=_ITERATIONS):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)


def _encode(password):
    salt = secrets.token_bytes(16)
    digest = _hash_password(password, salt)
    return "$".join((_ALGO, str(_ITERATIONS), salt.hex(), digest.hex()))


def connect(path):
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, password TEXT NOT NULL)")
    conn.commit()
    return conn

def register(conn, name, password):
    conn.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, _encode(password)))
    conn.commit()

def find_users(conn, name_filter):
    escaped = name_filter.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return conn.execute(
        "SELECT name FROM users WHERE name LIKE ? ESCAPE '\\' ORDER BY name",
        ("%" + escaped + "%",),
    ).fetchall()

def login(conn, name, password):
    row = conn.execute("SELECT password FROM users WHERE name = ?", (name,)).fetchone()
    if not row:
        return False
    try:
        algo, iterations, salt_hex, hash_hex = row[0].split("$")
        if algo != _ALGO:
            return False
        expected = bytes.fromhex(hash_hex)
        actual = _hash_password(password, bytes.fromhex(salt_hex), int(iterations))
    except (ValueError, AttributeError, TypeError):
        return False
    return hmac.compare_digest(actual, expected)
