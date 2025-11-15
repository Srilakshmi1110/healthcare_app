# backend/chat_prescription_ai.py
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "..", "data", "prescription_data.csv")  # project/data/prescription_data.csv

# Load CSV once; if missing, fallback to minimal table
try:
    df = pd.read_csv(CSV_PATH)
except Exception as e:
    df = pd.DataFrame([
        {"symptom_keyword": "fever", "diagnosis": "Likely Viral Fever", "medicine_1": "Paracetamol", "med1_dosage": "500mg — 1 tablet twice daily",
         "medicine_2": "ORS", "med2_dosage": "As needed", "medicine_3": "Rest", "med3_dosage": "—"}
    ])

def chat_to_prescription(user_text: str):
    user_text = (user_text or "").lower()
    for _, row in df.iterrows():
        kw = str(row.get("symptom_keyword","")).lower()
        if kw and kw in user_text:
            meds = []
            for i in [1,2,3]:
                med = row.get(f"medicine_{i}", None)
                dose = row.get(f"med{i}_dosage", "")
                if med and str(med).strip():
                    meds.append(f"{med} — {dose}".strip())
            return {"diagnosis": row.get("diagnosis", "Uncertain"), "medicines": meds or ["Please consult a doctor."]}
    # default
    return {"diagnosis": "Could not detect a clear condition", "medicines": ["Please consult a doctor for an accurate prescription."]}
