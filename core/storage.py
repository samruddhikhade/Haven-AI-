# core/storage.py
import sqlite3
import pandas as pd
import datetime
import json

DB_PATH = "haven_storage.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # Checkins Table
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
    # Full Craving Entries Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cravings_entries (
            id TEXT PRIMARY KEY,
            date TEXT,
            time TEXT,
            category TEXT,
            secondary_category TEXT,
            vibe TEXT,
            idea TEXT,
            pantry_matched TEXT,
            note TEXT
        )
    """)
    # Pantry Settings Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_settings (
            key TEXT PRIMARY KEY,
            value TEXT
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
        df = pd.DataFrame()
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

# --- Functions required by your ui/cravings.py ---

def save_craving_entry(entry: dict):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO cravings_entries (
            id, date, time, category, secondary_category, vibe, idea, pantry_matched, note
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        entry.get("id"),
        entry.get("date"),
        entry.get("time"),
        entry.get("category"),
        entry.get("secondary_category"),
        entry.get("vibe"),
        entry.get("idea"),
        entry.get("pantry_matched"),
        entry.get("note")
    ))
    conn.commit()
    conn.close()

def get_cravings_history():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query("SELECT * FROM cravings_entries ORDER BY date DESC, time DESC", conn)
    except Exception:
        df = pd.DataFrame()
    finally:
        conn.close()
    return df

def delete_craving_entry(entry_id: str):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM cravings_entries WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()

def save_pantry(pantry_list: list):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO user_settings (key, value) VALUES ('pantry', ?)", (json.dumps(pantry_list),))
    conn.commit()
    conn.close()

def get_saved_pantry():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("SELECT value FROM user_settings WHERE key = 'pantry'")
        row = cur.fetchone()
        if row and row[0]:
            return json.loads(row[0])
    except Exception:
        pass
    finally:
        conn.close()
    return ["Banana", "Makhana", "Curd", "Oats", "Dark Chocolate", "Milk"]