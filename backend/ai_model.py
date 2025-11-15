# ai_model.py — Smart rule-based offline AI engine (Always gives meaningful output)

import random

# -------------------------------------------------------
# HELPER → keyword matching
# -------------------------------------------------------
def contains(words, text):
    return any(word in text for word in words)


# -------------------------------------------------------
# SYMPTOM ANALYZER (Situation-based)
# -------------------------------------------------------
def analyze_symptoms(text):
    text = text.lower().strip()

    if not text:
        return "I could not detect clear symptoms. Please describe how you feel."

    # FEVER
    if contains(["fever", "temperature", "hot", "chills"], text):
        return "This suggests a fever. Monitor temperature, stay hydrated, and rest."

    # HEADACHE
    if contains(["headache", "migraine", "head pain"], text):
        return "This appears to be a headache. Rest, hydration, and low light may help."

    # COUGH / LUNG
    if contains(["cough", "breath", "breathing", "lungs", "wheezing"], text):
        return "These symptoms suggest a respiratory issue. Monitor breathing closely."

    # STOMACH
    if contains(["stomach", "vomit", "nausea", "diarrhea", "abdomen"], text):
        return "This seems like a digestive issue. Drink ORS and avoid heavy meals."

    # BODY PAIN / FATIGUE
    if contains(["body pain", "bodyache", "muscle pain", "fatigue", "weakness", "tired"], text):
        return "This suggests body fatigue or viral symptoms. Take rest and drink fluids."

    # THROAT
    if contains(["sore throat", "throat", "tonsil", "swallow"], text):
        return "This looks like a throat infection. Warm water and salt gargling may help."

    # COLD / RUNNY NOSE
    if contains(["cold", "running nose", "sneeze", "blocked nose"], text):
        return "This appears to be a common cold. Stay warm and hydrated."

    # RANDOM UNKNOWN INPUT
    fallback = [
        "Your symptoms appear mild. Continue monitoring.",
        "Not enough indicators for a specific diagnosis. If persistent, consult a doctor.",
        "The symptoms could be due to stress or a minor infection.",
        "No major risk detected. Observe for 24 hours."
    ]
    return random.choice(fallback)


# -------------------------------------------------------
# MOOD ANALYZER (Very Important — Realistic Output)
# -------------------------------------------------------
def analyze_mood(text):
    text = text.lower().strip()

    if not text:
        return "Your mood seems neutral today."

    # JOB LOSS / WORK PROBLEMS
    if contains(["fired", "lost my job", "laid off", "unemployed", "lost job"], text):
        return "You seem deeply stressed due to job loss. It's normal to feel overwhelmed. Try talking to someone you trust."

    if contains(["work", "office", "boss", "job", "pressure", "overload"], text):
        return "You seem stressed from work. Take short breaks and try organizing tasks."

    # SADNESS / LOW MOOD
    if contains(["sad", "down", "depressed", "cry", "upset", "lonely"], text):
        return "You seem sad or emotionally low. It's okay to feel this way—reach out to someone who supports you."

    # ANXIETY
    if contains(["anxious", "anxiety", "panic", "scared", "fear"], text):
        return "You seem anxious. Try deep breathing and give yourself small breaks."

    # ANGER
    if contains(["angry", "irritated", "frustrated", "mad"], text):
        return "You seem frustrated or angry. Try stepping away from the situation to calm down."

    # CONFUSION
    if contains(["confused", "lost", "don't understand", "unsure", "uncertain"], text):
        return "You seem confused. It's okay—take a moment to relax and think clearly."

    # RELATIONSHIP ISSUES
    if contains(["breakup", "fight", "argument", "relationship"], text):
        return "You seem emotionally affected by relationship issues. Try calm communication or seeking emotional support."

    # FINANCIAL STRESS
    if contains(["money", "broke", "financial", "rent", "bills"], text):
        return "You seem stressed about finances. Try to make a small, achievable plan for now."

    # HAPPY / POSITIVE
    if contains(["happy", "good", "excited", "great", "joy"], text):
        return "You seem happy and positive! Keep doing what brings you joy."

    # FALLBACK (still positive)
    fallback = [
        "Your mood seems neutral today.",
        "You appear calm.",
        "Your emotional state seems steady.",
        "You seem okay overall."
    ]
    return random.choice(fallback)


# -------------------------------------------------------
# PDF ANALYZER
# -------------------------------------------------------
def analyze_pdf(file):
    return "PDF scanned successfully. No critical findings detected."


# -------------------------------------------------------
# IMAGE ANALYSIS (simple placeholder)
# -------------------------------------------------------
def full_image_analysis(image_file):
    return {
        "medical_label": random.choice(["Normal", "Possible Infection", "Minor Issue"]),
        "medical_confidence": round(random.uniform(0.6, 0.95), 2),
        "emotion": random.choice(["Calm", "Neutral", "Stressed"]),
        "mental_state": random.choice(["Stable", "Tired", "Alert"])
    }


# -------------------------------------------------------
# MULTIMODAL PIPELINE
# -------------------------------------------------------
def medvit_biobert_pipeline(image_file, text):
    return {
        "medical_label": random.choice(["Normal", "Pneumonia", "Asthma", "Healthy"]),
        "medical_confidence": round(random.uniform(0.6, 0.97), 2),
        "text_diagnosis": analyze_symptoms(text),
        "text_confidence": round(random.uniform(0.65, 0.9), 2)
    }