# modules/registration.py
import re
import time
import random
from datetime import datetime
from typing import Tuple, Optional
from config import EVENT_ID
from . import database

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

def generate_salesforce_like_id() -> str:
    """
    Genera algo del estilo 00Q5g00000ABC123 (no es exacto al de Salesforce, pero sirve para demo).
    """
    prefix = "00Q"
    middle = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=9))
    suffix = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=3))
    return f"{prefix}{middle}{suffix}"

def validate_email(email: str) -> bool:
    return re.match(EMAIL_REGEX, email) is not None

def register_lead_interactive() -> Optional[dict]:
    print("\n=== REGISTRO DE ASISTENTE ===")
    full_name = input("Nombre completo: ").strip()
    email = input("Email: ").strip()
    whatsapp = input("WhatsApp (+52...): ").strip()
    company = input("Empresa: ").strip()
    position = input("Cargo: ").strip()

    if not full_name or not email:
        print("❌ Error: nombre y email son obligatorios")
        return None
    if not validate_email(email):
        print("❌ Error: email no válido")
        return None

    lead_id = generate_salesforce_like_id()
    lead = {
        "lead_id": lead_id,
        "full_name": full_name,
        "email": email,
        "whatsapp": whatsapp,
        "company": company,
        "position": position,
        "event_id": EVENT_ID,
        "qr_data": None,
        "status": "Registered",
        "registration_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "attendance_date": None,
    }

    database.insert_lead(lead)

    print("\n✅ REGISTRO EXITOSO")
    print("━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Lead ID: {lead_id}")
    print(f"Nombre: {full_name}")
    print(f"Email: {email}")
    print(f"Evento: {EVENT_ID}")

    return lead
