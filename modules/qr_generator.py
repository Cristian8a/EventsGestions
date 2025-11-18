# modules/qr_generator.py
import os
import hashlib
import time
import urllib.parse
import requests
from config import SECRET_KEY, QR_FOLDER, USE_REMOTE_QR, CHECKIN_BASE_URL
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
    qr_payload = build_qr_payload(lead["event_id"], lead["lead_id"])

    # 🔴 LO IMPORTANTE: el QR va a contener una URL con el payload como query
    encoded_payload = urllib.parse.quote(qr_payload)
    qr_url = f"{CHECKIN_BASE_URL}?q={encoded_payload}"

    filename = f"{lead['lead_id']}.png"
    filepath = os.path.join(QR_FOLDER, filename)

    if USE_REMOTE_QR:
        encoded_url = urllib.parse.quote(qr_url)
        url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded_url}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(resp.content)
        else:
            with open(filepath, "wb") as f:
                f.write(resp.content)
    else:
        import qrcode
        img = qrcode.make(qr_url)
        img.save(filepath)

    # Guardas el payload “lógico” en la base (no la URL)
    database.update_lead_qr(lead["lead_id"], qr_payload)

    print("\nQR Generado:")
    print(qr_url)  # opcionalmente mostrar la URL
    print(f"📁 Guardado en: {filepath}")
    print(f"✉️  Email enviado con QR adjunto a {lead['email']} (simulado)")
    if lead.get("whatsapp"):
        print(f"📱 WhatsApp enviado al {lead['whatsapp']} (simulado)")

    return qr_payload
