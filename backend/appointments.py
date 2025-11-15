# backend/appointments.py
import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "healthcare.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    # keep minimal appointment schema
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

init_db()

def save_appointment(name: str, date: str, time: str, notes: str):
    """Save appointment; return inserted row id or None on failure."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO appointments (name, date, time, notes, created_at) VALUES (?, ?, ?, ?, ?)",
            (name, date, time, notes, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        rowid = cur.lastrowid
        conn.close()
        return rowid
    except Exception as e:
        print("save_appointment error:", e)
        return None

def get_appointments():
    """Return list of dicts representing appointments (ordered by date/time)."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM appointments ORDER BY date ASC, time ASC")
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        print("get_appointments error:", e)
        return []