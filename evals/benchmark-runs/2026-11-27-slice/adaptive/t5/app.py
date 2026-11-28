import sqlite3

def connect(db_path):
    return sqlite3.connect(db_path)

def add_task(conn, title, priority=2):
    conn.execute("INSERT INTO tasks (title, done, priority) VALUES (?, 0, ?)", (title, priority))
    conn.commit()

def list_tasks(conn):
    return conn.execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()
