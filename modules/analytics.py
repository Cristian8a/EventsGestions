# modules/analytics.py
from . import database

def show_dashboard():
    leads = database.get_all_leads()
    total = len(leads)
    attended = sum(1 for l in leads if l["status"] == "Attended")
    not_attended = total - attended
    attendance_rate = (attended / total * 100) if total else 0

    print("\n📊 DASHBOARD DEL EVENTO")
    print("━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Total de registros: {total}")
    print(f"Total de asistentes: {attended}")
    print(f"Tasa de asistencia: {attendance_rate:.2f}%")
    print(f"No asistieron: {not_attended}")

    print("\nLista de registrados:")
    for l in leads:
        print(f"- {l['lead_id']} | {l['full_name']} | {l['email']} | {l['status']}")
