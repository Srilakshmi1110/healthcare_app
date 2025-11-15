# backend/database.py
import sqlite3
import os
import hashlib
from datetime import datetime

# -----------------------------
# PATH SETTINGS
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "healthcare.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# PASSWORD HASHING
# -----------------------------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# -----------------------------
# DATABASE INITIALIZATION
# -----------------------------
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            created_at TEXT
        )
    """)

    # History table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            event_type TEXT,
            content TEXT,
            timestamp TEXT
        )
    """)

    # Appointments table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            time TEXT,
            notes TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


# Initialize DB on import
init_db()


# -----------------------------
# USER MANAGEMENT
# -----------------------------
def add_user(username: str, password: str) -> bool:
    try:
        conn = get_connection()
        cur = conn.cursor()

        hashed = hash_password(password)

        cur.execute("""
            INSERT INTO users (username, password, created_at)
            VALUES (?, ?, ?)
        """, (username, hashed, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print("add_user error:", e)
        return False


def validate_user(username: str, password: str) -> bool:
    try:
        conn = get_connection()
        cur = conn.cursor()

        hashed = hash_password(password)

        cur.execute("""
            SELECT * FROM users
            WHERE username = ? AND password = ?
        """, (username, hashed))

        user = cur.fetchone()
        conn.close()
        return user is not None

    except Exception as e:
        print("validate_user error:", e)
        return False


# -----------------------------
# HISTORY
# -----------------------------
def add_history(username: str, event_type: str, content: str):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO history (username, event_type, content, timestamp)
            VALUES (?, ?, ?, ?)
        """, (
            username,
            event_type,
            content,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print("add_history error:", e)
        return False


def get_history(username: str):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT username, event_type, content, timestamp 
            FROM history
            WHERE username = ?
            ORDER BY timestamp DESC
        """, (username,))

        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    except Exception as e:
        print("get_history error:", e)
        return []