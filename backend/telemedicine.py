# backend/telemedicine.py
from datetime import datetime

def get_meet_link(prefix="healthcare"):
    room = f"{prefix}-{int(datetime.now().timestamp())}"
    return f"https://meet.jit.si/{room}"
