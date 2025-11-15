# app.py — Telemed Unified AI Assistant (Final Stable Version)
import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

# -------------------------------------------------------
# BACKEND IMPORTS (Smart + Fallback)
# -------------------------------------------------------
BACKEND_AVAILABLE = False

try:
    from backend.ai_model import (
        analyze_symptoms,
        analyze_mood,
        analyze_pdf,
        full_image_analysis,
        medvit_biobert_pipeline
    )

    from backend.appointments import save_appointment, get_appointments
    from backend.telemedicine import get_meet_link
    from backend.pdf_module import generate_pdf, generate_prescription_pdf
    from backend.database import add_user, validate_user, add_history, get_history
    from backend.chat_prescription_ai import chat_to_prescription

    BACKEND_AVAILABLE = True

except Exception as e:
    st.sidebar.error("Backend import error — Demo Mode Enabled")

    # FALLBACK SAFE MODE
    def analyze_symptoms(t): return "Symptoms appear mild."
    def analyze_mood(t): return "Your mood seems neutral today."
    def analyze_pdf(t): return "PDF processed. No major findings."
    def full_image_analysis(x):
        return {
            "medical_label": "Normal",
            "medical_confidence": 0.8,
            "emotion": "Neutral",
            "mental_state": "Stable"
        }
    def medvit_biobert_pipeline(i, t):
        return {
            "medical_label": "Normal",
            "medical_confidence": 0.76,
            "text_diagnosis": "Mild condition",
            "text_confidence": 0.70
        }
    def chat_to_prescription(x):
        return {
            "diagnosis": "Mild Viral Infection",
            "medicines": ["Paracetamol 500mg — twice daily"]
        }

    def save_appointment(a, b, c, d): return True
    def get_appointments(): return pd.DataFrame()
    def get_meet_link(): return "https://meet.jit.si/demo-room"
    def generate_pdf(a, b): return b"DEMO PDF"
    def generate_prescription_pdf(a, b, c, d, e): return b"DEMO PRESCRIPTION"
    def add_user(a, b): return True
    def validate_user(a, b): return True
    def add_history(a, b, c): return None
    def get_history(a): return []


# -------------------------------------------------------
# STREAMLIT CONFIG
# -------------------------------------------------------
st.set_page_config(page_title="Telemed Unified AI Assistant", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "jitsi_room" not in st.session_state:
    st.session_state.jitsi_room = None


# -------------------------------------------------------
# JITSI VIDEO EMBED
# -------------------------------------------------------
def embed_jitsi(room):
    components.html(
        f"""
        <iframe src="https://meet.jit.si/{room}"
                style="width:100%; height:600px; border:none;">
        </iframe>
        """,
        height=600,
    )


# -------------------------------------------------------
# LOGIN / REGISTER
# -------------------------------------------------------
if not st.session_state.logged_in:
    st.title("Login / Register")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # LOGIN TAB
    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            if validate_user(u, p):
                st.session_state.logged_in = True
                st.session_state.current_user = u
                st.rerun()
            else:
                st.error("Invalid username or password")

    # REGISTER TAB
    with tab2:
        new_u = st.text_input("New Username")
        new_p = st.text_input("New Password", type="password")

        if st.button("Register"):
            if add_user(new_u, new_p):
                st.success("Registration successful. Please log in.")
            else:
                st.error("User already exists.")

    st.stop()


# -------------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------------
st.sidebar.title(f"Welcome, {st.session_state.current_user}")

page = st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "Symptom Checker",
        "Mental Health",
        "PDF Analyzer",
        "Appointments",
        "Telemedicine",
        "Patient History",
        "Prescription",
        "Chat Prescription AI",
        "Image + Text Analyzer"
    ]
)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()


# -------------------------------------------------------
# HOME PAGE
# -------------------------------------------------------
if page == "Home":
    st.title("Telemed Unified AI Assistant")
    st.write("Your all-in-one AI-powered healthcare assistant.")


# -------------------------------------------------------
# SYMPTOM CHECKER
# -------------------------------------------------------
elif page == "Symptom Checker":
    st.title("Symptom Checker")

    text = st.text_area("Describe your symptoms")

    if "symptom_result" not in st.session_state:
        st.session_state.symptom_result = None

    if st.button("Analyze Symptoms"):
        if not text.strip():
            text = "no symptoms"
        st.session_state.symptom_result = analyze_symptoms(text)

    if st.session_state.symptom_result:
        st.info(st.session_state.symptom_result)


# -------------------------------------------------------
# MENTAL HEALTH ANALYZER
# -------------------------------------------------------
elif page == "Mental Health":
    st.title("Mental Health Analyzer")

    text = st.text_area("How are you feeling today?")

    if "mood_result" not in st.session_state:
        st.session_state.mood_result = None

    if st.button("Analyze Mood"):
        if not text.strip():
            text = "no input"
        st.session_state.mood_result = analyze_mood(text)

    if st.session_state.mood_result:
        st.success(st.session_state.mood_result)


# -------------------------------------------------------
# PDF ANALYZER
# -------------------------------------------------------
elif page == "PDF Analyzer":
    st.title("PDF Analyzer")

    file = st.file_uploader("Upload PDF", type="pdf")

    if "pdf_result" not in st.session_state:
        st.session_state.pdf_result = None

    if st.button("Analyze PDF"):
        if file:
            st.session_state.pdf_result = analyze_pdf(file)

    if st.session_state.pdf_result:
        st.text_area("PDF Result", st.session_state.pdf_result, height=300)


# -------------------------------------------------------
# APPOINTMENTS
# -------------------------------------------------------
elif page == "Appointments":
    st.title("Appointments")

    name = st.text_input("Patient Name")
    date = st.date_input("Date")
    time = st.time_input("Time")
    notes = st.text_area("Notes")

    if st.button("Save Appointment"):
        save_appointment(name, str(date), str(time), notes)
        st.success("Appointment saved successfully.")

    st.subheader("All Appointments")
    st.dataframe(get_appointments())


# -------------------------------------------------------
# TELEMEDICINE PAGE
# -------------------------------------------------------
elif page == "Telemedicine":
    st.title("Telemedicine Video Call")

    if st.button("Generate Meeting Link"):
        room = "telemed-" + str(datetime.now().timestamp()).replace(".", "")
        st.session_state.jitsi_room = room
        st.write(f"Meeting Link: https://meet.jit.si/{room}")

    if st.session_state.jitsi_room:
        embed_jitsi(st.session_state.jitsi_room)


# -------------------------------------------------------
# PATIENT HISTORY
# -------------------------------------------------------
elif page == "Patient History":
    st.title("Patient History")

    df = pd.DataFrame(get_history(st.session_state.current_user))
    if df.empty:
        st.info("No history found.")
    else:
        st.dataframe(df)


# -------------------------------------------------------
# PRESCRIPTION GENERATOR
# -------------------------------------------------------
elif page == "Prescription":
    st.title("Prescription Generator")

    patient = st.text_input("Patient Name", st.session_state.current_user)
    symptoms = st.text_area("Symptoms")
    diagnosis = st.text_input("Diagnosis")
    meds_raw = st.text_area("Medicines (one per line)")
    doctor = st.text_input("Doctor Name", "Dr. Kavya")

    if st.button("Generate Prescription PDF"):
        meds = [m.strip() for m in meds_raw.split("\n") if m.strip()]
        pdf = generate_prescription_pdf(patient, doctor, symptoms, diagnosis, meds)

        st.download_button("Download Prescription", pdf, "prescription.pdf")


# -------------------------------------------------------
# CHAT PRESCRIPTION AI
# -------------------------------------------------------
elif page == "Chat Prescription AI":
    st.title("AI Doctor Chat")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    msg = st.text_input("Describe your issue")

    if st.button("Send"):
        if msg.strip():
            out = chat_to_prescription(msg)
            ai_reply = (
                f"Diagnosis: {out['diagnosis']}\n"
                f"Medicines:\n" +
                "\n".join([f"- {m}" for m in out["medicines"]])
            )
            st.session_state.chat_history.append(("You", msg))
            st.session_state.chat_history.append(("AI Doctor", ai_reply))

    for sender, msg in st.session_state.chat_history:
        st.write(f"{sender}:** {msg}")


# -------------------------------------------------------
# MULTIMODAL IMAGE + TEXT ANALYZER
# -------------------------------------------------------
elif page == "Image + Text Analyzer":
    st.title("Multimodal AI")

    img = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    txt = st.text_area("Enter symptoms / description")

    if "multi_result" not in st.session_state:
        st.session_state.multi_result = None

    if st.button("Analyze"):
        if img:
            st.session_state.multi_result = medvit_biobert_pipeline(img, txt)

    if st.session_state.multi_result:
        st.json(st.session_state.multi_result)
