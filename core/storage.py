# core/storage.py
import sqlite3
import os
import pandas as pd
from datetime import datetime

DB_PATH = "haven_storage.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS checkins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        date TEXT,
        age INTEGER,
        systolic_bp REAL,
        diastolic_bp REAL,
        current_map REAL,
        heart_rate REAL,
        weight REAL,
        blood_sugar REAL,
        symptoms_count INTEGER,
        has_headache INTEGER,
        has_vision INTEGER,
        has_edema INTEGER,
        risk_percentage REAL,
        risk_tier TEXT,
        mood TEXT,
        water_glasses INTEGER,
        craving TEXT,
        craving_vibe TEXT,
        journal_note TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_checkin(data: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Calculate symptoms_count safely if missing
    s_count = data.get("symptoms_count", sum([
        int(data.get("has_headache", 0)),
        int(data.get("has_vision", 0)),
        int(data.get("has_edema", 0))
    ]))

    cursor.execute("""
    INSERT INTO checkins (
        timestamp, date, age, systolic_bp, diastolic_bp, current_map,
        heart_rate, weight, blood_sugar, symptoms_count, has_headache,
        has_vision, has_edema, risk_percentage, risk_tier, mood,
        water_glasses, craving, craving_vibe, journal_note
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        datetime.now().strftime("%b %d, %Y"),
        data.get("age", 28),
        data.get("systolic_bp", 120),
        data.get("diastolic_bp", 80),
        data.get("current_map", 93.3),
        data.get("heart_rate", 75),
        data.get("weight", 65.0),
        data.get("blood_sugar", 6.0),
        s_count,
        int(data.get("has_headache", 0)),
        int(data.get("has_vision", 0)),
        int(data.get("has_edema", 0)),
        data.get("risk_percentage", 10.0),
        data.get("risk_tier", "Balanced & Low Risk"),
        data.get("mood", "😊 Happy"),
        data.get("water_glasses", 6),
        data.get("craving", "None"),
        data.get("craving_vibe", "None"),
        data.get("journal_note", "")
    ))
    conn.commit()
    conn.close()

def get_recent_checkins(limit: int = 14) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(f"SELECT * FROM checkins ORDER BY id DESC LIMIT {limit}", conn)
    conn.close()
    if not df.empty:
        df = df.sort_values(by="id", ascending=True)
    return df

# --- CRAVING CORNER EXTENSION ---
import os
import json
import pandas as pd

CRAVINGS_DB_FILE = "haven_cravings.csv"
PANTRY_DB_FILE = "haven_pantry.json"

def get_cravings_history():
    if not os.path.exists(CRAVINGS_DB_FILE):
        return pd.DataFrame(columns=[
            "id", "date", "time", "category", "secondary_category", 
            "vibe", "idea", "pantry_matched", "note"
        ])
    try:
        df = pd.read_csv(CRAVINGS_DB_FILE)
        return df
    except Exception:
        return pd.DataFrame()

def save_craving_entry(entry: dict):
    df = get_cravings_history()
    new_entry_df = pd.DataFrame([entry])
    df = pd.concat([new_entry_df, df], ignore_index=True)
    df.to_csv(CRAVINGS_DB_FILE, index=False)

def delete_craving_entry(entry_id: str):
    df = get_cravings_history()
    if not df.empty and "id" in df.columns:
        df = df[df["id"] != entry_id]
        df.to_csv(CRAVINGS_DB_FILE, index=False)

# 1. Pehle save_pantry define hona zaroori hai
def save_pantry(items: list):
    with open(PANTRY_DB_FILE, "w") as f:
        json.dump(items, f)

# 2. Fir get_saved_pantry usko bina kisi error ke use karega
def get_saved_pantry():
    if not os.path.exists(PANTRY_DB_FILE):
        default_pantry = ["Banana", "Curd / Yogurt", "Makhana", "Milk", "Oats", "Peanut Butter"]
        save_pantry(default_pantry)
        return default_pantry
    try:
        with open(PANTRY_DB_FILE, "r") as f:
            saved = json.load(f)
            return [x if x != "Yogurt" else "Curd / Yogurt" for x in saved]
    except Exception:
        return ["Banana", "Curd / Yogurt", "Makhana"]

# core/storage.py ke aakhiri hisse mein paste karein
SANCTUARY_LOG_FILE = "haven_sanctuary.csv"

def get_sanctuary_history():
    if not os.path.exists(SANCTUARY_LOG_FILE):
        return pd.DataFrame(columns=["id", "date", "time", "activity_type", "duration_min", "sound_used", "feedback"])
    try:
        df = pd.read_csv(SANCTUARY_LOG_FILE)
        return df.fillna("")
    except Exception:
        return pd.DataFrame(columns=["id", "date", "time", "activity_type", "duration_min", "sound_used", "feedback"])

def save_sanctuary_session(entry):
    df = get_sanctuary_history()
    new_df = pd.concat([pd.DataFrame([entry]), df], ignore_index=True)
    new_df.to_csv(SANCTUARY_LOG_FILE, index=False)
    