import sqlite3

def connect(path):
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, password TEXT NOT NULL)")
    conn.commit()
    return conn

def register(conn, name, password):
    conn.execute(f"INSERT INTO users (name, password) VALUES ('{name}', '{password}')")
    conn.commit()

def find_users(conn, name_filter):
    return conn.execute(f"SELECT name FROM users WHERE name LIKE '%{name_filter}%' ORDER BY name").fetchall()

def login(conn, name, password):
    row = conn.execute(f"SELECT password FROM users WHERE name = '{name}'").fetchone()
    return bool(row) and row[0] == password
