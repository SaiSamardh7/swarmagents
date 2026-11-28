import hashlib
import hmac
import secrets
import sqlite3

_ITERATIONS = 200_000
_SALT_BYTES = 16


def _hash(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, _ITERATIONS)


def connect(path):
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, password TEXT NOT NULL)")
    conn.commit()
    return conn


def register(conn, name, password):
    salt = secrets.token_bytes(_SALT_BYTES)
    stored = (salt + _hash(password, salt)).hex()
    conn.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, stored))
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
        raw = bytes.fromhex(row[0])
    except ValueError:
        return False
    salt, expected = raw[:_SALT_BYTES], raw[_SALT_BYTES:]
    return hmac.compare_digest(_hash(password, salt), expected)
