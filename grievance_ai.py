import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import time
import os

# -----------------------------------------
# LOAD TRAINING DATA
# -----------------------------------------
df = pd.read_csv("data/grievances.csv")

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["complaint"])

# -----------------------------------------
# 1. DEPARTMENT CLASSIFICATION
# -----------------------------------------
def classify_department(text):
    t = text.lower()

    # HARD KEYWORDS (always correct)
    electricity_words = ["power", "electricity", "transformer", "street light", "voltage"]
    water_words = ["water", "pipeline", "borewell", "drinking water", "tank"]
    road_words = ["road", "pothole", "accident", "bridge", "damaged road"]
    welfare_words = ["pension", "ration", "widow", "scholarship", "old age"]
    agriculture_words = ["crop", "farmer", "insurance", "subsidy", "seeds"]

    for w in electricity_words:
        if w in t:
            return "Electricity"

    for w in water_words:
        if w in t:
            return "Water"

    for w in road_words:
        if w in t:
            return "Infrastructure"

    for w in welfare_words:
        if w in t:
            return "Social Welfare"

    for w in agriculture_words:
        if w in t:
            return "Agriculture"

    # FALLBACK: machine similarity
    vec = vectorizer.transform([text])
    sim = cosine_similarity(vec, X)
    index = sim.argmax()
    return df.iloc[index]["department"]


# -----------------------------------------
# 2. PRIORITY SCORING (REAL-WORLD LOGIC)
# -----------------------------------------

def priority_score(text):
    text = text.lower()

    urgent_words = [
        "no power", "power cut", "transformer",
        "leakage", "burst", "accident", "danger",
        "injury", "death", "light not working",
        "water not coming", "pipeline damage"
    ]

    medium_words = [
        "delay", "not received", "pending", "slow",
        "not credited", "not working", "complaint"
    ]

    if any(w in text for w in urgent_words):
        return "🔴 HIGH PRIORITY (Immediate Action Required)"

    if any(w in text for w in medium_words):
        return "🟡 MEDIUM PRIORITY (Resolve Soon)"

    return "🟢 LOW PRIORITY (Normal Case)"

# -----------------------------------------
# 3. DUPLICATE COMPLAINT DETECTION
# -----------------------------------------

def is_duplicate(text, db_path="data/grievance_db.csv"):
    if not os.path.exists(db_path):
        return False

    db = pd.read_csv(db_path)

    if db.empty:
        return False

    vec = vectorizer.transform([text])
    old_vec = vectorizer.transform(db["complaint"])

    sim = cosine_similarity(vec, old_vec).max()

    if sim > 0.85:
        return True

    return False

# -----------------------------------------
# 4. TICKET ID GENERATION
# -----------------------------------------

def generate_ticket():
    return "GRV-" + str(random.randint(100000, 999999))

# -----------------------------------------
# 5. FORWARD TO DEPARTMENT (SIMULATION)
# -----------------------------------------

def forward_to_department(dept):
    return f"📨 Complaint forwarded to **{dept} Department** successfully."

# -----------------------------------------
# 6. SAVE COMPLAINT TO DATABASE
# -----------------------------------------

def save_complaint(text, dept, priority, ticket):
    path = "data/grievance_db.csv"

    if os.path.exists(path):
        db = pd.read_csv(path)
    else:
        db = pd.DataFrame(columns=["ticket", "complaint", "department", "priority", "status"])

    new_row = {
        "ticket": ticket,
        "complaint": text,
        "department": dept,
        "priority": priority,
        "status": "Submitted"
    }

    db = pd.concat([db, pd.DataFrame([new_row])], ignore_index=True)
    db.to_csv(path, index=False)

# -----------------------------------------
# 7. TRACK STATUS OF A COMPLAINT
# -----------------------------------------

def track_complaint(ticket):
    path = "data/grievance_db.csv"

    if not os.path.exists(path):
        return "No records found."

    db = pd.read_csv(path)

    match = db[db["ticket"] == ticket]

    if match.empty:
        return "❌ Ticket ID not found. Please check again."

    row = match.iloc[0]
    return f"""
🧾 **Grievance Status**

🔹 Ticket ID: {row['ticket']}
🔹 Department: {row['department']}
🔹 Priority: {row['priority']}
🔹 Status: {row['status']}
"""

# -----------------------------------------
# 8. MAIN FUNCTION CALLED BY STREAMLIT
# -----------------------------------------

def process_grievance(user_text):
    # Duplicate check
    duplicate = is_duplicate(user_text)

    department = classify_department(user_text)
    priority = priority_score(user_text)
    ticket_id = generate_ticket()

    save_complaint(user_text, department, priority, ticket_id)

    forward_msg = forward_to_department(department)

    return {
        "department": department,
        "priority": priority,
        "duplicate": duplicate,
        "ticket": ticket_id,
        "forward": forward_msg
    }
