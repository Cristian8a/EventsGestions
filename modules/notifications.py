# modules/notifications.py
from datetime import datetime, timedelta
from . import database
from config import EVENT_ID

def simulate_reminders(event_date: datetime):
    leads = database.get_all_leads()
    if not leads:
        print("No hay leads registrados todavía.")
        return 
    
    schedule_days = [23, 10, 3]
    for d in schedule_days:
        send_date = event_date - timedelta(days=d)
        print(f"\n📅 Recordatorios D-{d} ({send_date.date()}):")
        for lead in leads:
            print(f"→ Enviar a {lead['email']} / {lead.get('whatsapp') or 'sin whatsapp'} "
                  f"No te olvides de asistir al evento prrillo {EVENT_ID}")
