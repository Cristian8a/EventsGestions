# modules/database.py
import sqlite3
from datetime import datetime
from typing import Optional, List, Dict
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            lead_id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            whatsapp TEXT,
            company TEXT,
            position TEXT,
            event_id TEXT NOT NULL,
            qr_data TEXT,
            status TEXT NOT NULL,
            registration_date TEXT NOT NULL,
            attendance_date TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_lead(lead: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO leads (lead_id, full_name, email, whatsapp, company, position,
                           event_id, qr_data, status, registration_date, attendance_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        lead["lead_id"],
        lead["full_name"],
        lead["email"],
        lead.get("whatsapp"),
        lead.get("company"),
        lead.get("position"),
        lead["event_id"],
        lead.get("qr_data"),
        lead["status"],
        lead["registration_date"],
        lead.get("attendance_date")
    ))
    conn.commit()
    conn.close()

def update_lead_qr(lead_id: str, qr_data: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE leads SET qr_data = ? WHERE lead_id = ?", (qr_data, lead_id))
    conn.commit()
    conn.close()

def mark_attended(lead_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("UPDATE leads SET status = ?, attendance_date = ? WHERE lead_id = ?",
              ("Attended", now, lead_id))
    conn.commit()
    conn.close()

def get_lead_by_id(lead_id: str) -> Optional[dict]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM leads WHERE lead_id = ?", (lead_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return _row_to_dict(row)

def get_all_leads() -> List[dict]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM leads")
    rows = c.fetchall()
    conn.close()
    return [_row_to_dict(r) for r in rows]

def _row_to_dict(row) -> Dict:
    return {
        "lead_id": row[0],
        "full_name": row[1],
        "email": row[2],
        "whatsapp": row[3],
        "company": row[4],
        "position": row[5],
        "event_id": row[6],
        "qr_data": row[7],
        "status": row[8],
        "registration_date": row[9],
        "attendance_date": row[10],
    }
