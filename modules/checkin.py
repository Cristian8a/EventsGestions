# modules/checkin.py
import hashlib
from datetime import datetime
from config import SECRET_KEY, EVENT_ID
from . import database

def parse_qr_string(qr_string: str) -> dict:
    """
    Convierte "EVENT:...|LEAD:...|TS:...|HASH:..." en dict.
    """
    parts = qr_string.split("|")
    data = {}
    for p in parts:
        if ":" in p:
            k, v = p.split(":", 1)
            data[k] = v
    return data

def verify_hash(event_id: str, lead_id: str, ts: str, given_hash: str) -> bool:
    base = event_id + lead_id + ts + SECRET_KEY
    expected = hashlib.sha256(base.encode("utf-8")).hexdigest()
    return expected == given_hash

def checkin_from_input():
    print("\n🎫 ESCANEO DE QR")
    print("Pega aquí la cadena completa del QR:")
    qr_string = input().strip()

    result = process_checkin(qr_string)
    print(result)

def process_checkin(qr_string: str) -> str:
    data = parse_qr_string(qr_string)
    event_id = data.get("EVENT")
    lead_id = data.get("LEAD")
    ts = data.get("TS")
    qr_hash = data.get("HASH")

    print("━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"QR Data: {qr_string}")

    if not (event_id and lead_id and ts and qr_hash):
        return "❌ QR inválido: faltan campos"

    if event_id != EVENT_ID:
        return "❌ QR pertenece a otro evento"

    # verificar hash
    if not verify_hash(event_id, lead_id, ts, qr_hash):
        return "❌ QR inválido: hash no coincide (posible falsificación)"

    lead = database.get_lead_by_id(lead_id)
    if not lead:
        return "❌ Lead no existe en la base de datos"

    if lead["status"] == "Attended":
        return "❌ QR ya fue usado anteriormente"

    # todo ok → marcar asistencia
    database.mark_attended(lead_id)

    msg = (
        "✅ VALIDACIÓN EXITOSA\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Bienvenido: {lead['full_name']}\n"
        f"Empresa: {lead.get('company') or 'N/A'}\n"
        f"Status actualizado: Registered → Attended\n"
        f"Hora de entrada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        "🎉 ¡Disfruta el evento!"
    )
    return msg
