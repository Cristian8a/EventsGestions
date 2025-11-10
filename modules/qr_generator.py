# modules/qr_generator.py
import os
import hashlib
import time
import urllib.parse
import requests
from config import SECRET_KEY, QR_FOLDER, USE_REMOTE_QR
from config import EVENT_ID
from . import database

def ensure_qr_folder():
    if not os.path.exists(QR_FOLDER):
        os.makedirs(QR_FOLDER, exist_ok=True)

def build_qr_payload(event_id: str, lead_id: str) -> str:
    timestamp = str(int(time.time() * 1000))
    base_string = event_id + lead_id + timestamp + SECRET_KEY
    hash_hex = hashlib.sha256(base_string.encode("utf-8")).hexdigest()
    qr_data = f"EVENT:{event_id}|LEAD:{lead_id}|TS:{timestamp}|HASH:{hash_hex}"
    return qr_data

def generate_qr_for_lead(lead: dict) -> str:
    ensure_qr_folder()
    qr_data = build_qr_payload(lead["event_id"], lead["lead_id"])
    filename = f"{lead['lead_id']}.png"
    filepath = os.path.join(QR_FOLDER, filename)

    if USE_REMOTE_QR:
        # usamos api.qrserver.com
        encoded = urllib.parse.quote(qr_data)
        url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(resp.content)
        else:
            # fallback simple
            with open(filepath, "wb") as f:
                f.write(resp.content)
    else:
        # generación local
        import qrcode
        img = qrcode.make(qr_data)
        img.save(filepath)

    # guardamos en la base
    database.update_lead_qr(lead["lead_id"], qr_data)

    print("\nQR Generado:")
    print(qr_data)
    print(f"📁 Guardado en: {filepath}")
    print(f"✉️  Email enviado con QR adjunto a {lead['email']} (simulado)")
    if lead.get("whatsapp"):
        print(f"📱 WhatsApp enviado al {lead['whatsapp']} (simulado)")

    return qr_data
