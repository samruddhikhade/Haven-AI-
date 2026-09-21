# core/storage.py
import sqlite3
import pandas as pd
import datetime

DB_PATH = "haven_storage.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            age REAL,
            systolic_bp REAL,
            diastolic_bp REAL,
            weight REAL,
            heart_rate REAL,
            blood_sugar REAL,
            has_headache INTEGER,
            has_vision INTEGER,
            has_edema INTEGER,
            symptoms_count INTEGER,
            current_map REAL,
            delta_map REAL,
            delta_weight REAL,
            risk_tier TEXT,
            risk_percentage REAL,
            mood TEXT,
            water_glasses INTEGER,
            journal_note TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_recent_checkins(limit: int = 7):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(f"SELECT * FROM checkins ORDER BY id DESC LIMIT {int(limit)}", conn)
    except Exception:
        df = pd.DataFrame(columns=[
            "id", "date", "age", "systolic_bp", "diastolic_bp", "weight", 
            "heart_rate", "blood_sugar", "has_headache", "has_vision", 
            "has_edema", "symptoms_count", "current_map", "delta_map", 
            "delta_weight", "risk_tier", "risk_percentage", "mood", 
            "water_glasses", "journal_note"
        ])
    finally:
        conn.close()
    return df

def save_checkin(record: dict):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    
    cur.execute("""
        INSERT INTO checkins (
            date, age, systolic_bp, diastolic_bp, weight, heart_rate, blood_sugar,
            has_headache, has_vision, has_edema, symptoms_count, current_map,
            delta_map, delta_weight, risk_tier, risk_percentage, mood, water_glasses, journal_note
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record.get("date", today_str),
        float(record.get("age", 28.0)),
        float(record.get("systolic_bp", 120.0)),
        float(record.get("diastolic_bp", 80.0)),
        float(record.get("weight", 65.0)),
        float(record.get("heart_rate", 76.0)),
        float(record.get("blood_sugar", 5.8)),
        int(record.get("has_headache", 0)),
        int(record.get("has_vision", 0)),
        int(record.get("has_edema", 0)),
        int(record.get("symptoms_count", 0)),
        float(record.get("current_map", 93.3)),
        float(record.get("delta_map", 0.0)),
        float(record.get("delta_weight", 0.0)),
        str(record.get("risk_tier", "Gentle & Steady")),
        float(record.get("risk_percentage", 15.0)),
        str(record.get("mood", "Calm")),
        int(record.get("water_glasses", 5)),
        str(record.get("journal_note", ""))
    ))
    conn.commit()
    conn.close()