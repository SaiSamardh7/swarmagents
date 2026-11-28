import sqlite3

def connect(db_path):
    return sqlite3.connect(db_path)

def add_task(conn, title):
    conn.execute("INSERT INTO tasks (title, done) VALUES (?, 0)", (title,))
    conn.commit()

def list_tasks(conn):
    return conn.execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()
