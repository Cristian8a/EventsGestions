# config.py
import os

# ID del evento de ejemplo
EVENT_ID = "CONFERENCIA_TECH_NOV25"

# clave secreta para firmar el QR
SECRET_KEY = "MI_CLAVE_SUPER_SECRETA_123"

# ruta de la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "leads.db")

# carpeta para guardar QRs
QR_FOLDER = os.path.join(BASE_DIR, "data", "qr_codes")

# si quieres forzar uso de api.qrserver.com en vez de qrcode local
USE_REMOTE_QR = True  # pon False si quieres usar la librería qrcode
