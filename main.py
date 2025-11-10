# main.py
import os
from datetime import datetime
from config import DB_PATH, QR_FOLDER, EVENT_ID
from modules import database, registration, qr_generator, checkin, notifications, analytics

def ensure_folders():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(QR_FOLDER, exist_ok=True)

def simulate_full_flow():
    """
    Crea varios leads de prueba, genera sus QRs y prueba distintos casos de check-in.
    """
    print("\n=== SIMULACIÓN COMPLETA ===")
    sample_names = [
        ("Juan Pérez", "juan.perez@example.com"),
        ("María López", "maria.lopez@example.com"),
        ("Carlos Ruiz", "carlos.ruiz@example.com"),
        ("Ana Torres", "ana.torres@example.com"),
        ("Luis García", "luis.garcia@example.com"),
        ("Sofía Hernández", "sofia.hdz@example.com"),
        ("Pedro Sánchez", "pedro.sanchez@example.com"),
        ("Laura Díaz", "laura.diaz@example.com"),
        ("Marta Castillo", "marta.castillo@example.com"),
        ("Diego Molina", "diego.molina@example.com"),
    ]

    created = []
    for name, email in sample_names:
        lead = {
            "lead_id": registration.generate_salesforce_like_id(),
            "full_name": name,
            "email": email,
            "whatsapp": "+52 3312345678",
            "company": "Tech Corp",
            "position": "Asistente",
            "event_id": EVENT_ID,
            "qr_data": None,
            "status": "Registered",
            "registration_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "attendance_date": None,
        }
        database.insert_lead(lead)
        qr_data = qr_generator.generate_qr_for_lead(lead)
        created.append((lead, qr_data))

    print("\n✅ Se crearon 10 leads de prueba.")

    # caso válido
    print("\n--- Caso: Check-in VÁLIDO ---")
    valid_qr = created[0][1]
    print(checkin.process_checkin(valid_qr))

    # caso duplicado
    print("\n--- Caso: Check-in DUPLICADO ---")
    print(checkin.process_checkin(valid_qr))

    # caso hash inválido
    print("\n--- Caso: QR con HASH inválido ---")
    bad_qr = valid_qr.replace("a", "b", 1)  # truco rápido para romperlo
    print(checkin.process_checkin(bad_qr))

    # caso evento diferente
    print("\n--- Caso: Evento diferente ---")
    wrong_event_qr = valid_qr.replace(EVENT_ID, "OTRO_EVENTO_XXX", 1)
    print(checkin.process_checkin(wrong_event_qr))

    # caso lead que no existe
    print("\n--- Caso: Lead inexistente ---")
    # tomamos estructura del QR válido y cambiamos LEAD
    parts = valid_qr.split("|")
    fake_parts = []
    for p in parts:
        if p.startswith("LEAD:"):
            fake_parts.append("LEAD:00QFAKE000000000")
        else:
            fake_parts.append(p)
    fake_qr = "|".join(fake_parts)
    print(checkin.process_checkin(fake_qr))

    print("\n--- Métricas después de la simulación ---")
    analytics.show_dashboard()

def show_menu():
    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Registrar nuevo asistente")
        print("2. Ver todos los registrados")
        print("3. Simular envío de recordatorios")
        print("4. Día del evento - Check-in")
        print("5. Ver métricas del evento")
        print("6. Simular flujo completo (demo)")
        print("7. Salir")

        choice = input("Selecciona una opción: ").strip()
        if choice == "1":
            lead = registration.register_lead_interactive()
            if lead:
                qr_generator.generate_qr_for_lead(lead)
        elif choice == "2":
            leads = database.get_all_leads()
            print("\n=== LEADS REGISTRADOS ===")
            for l in leads:
                print(f"{l['lead_id']} | {l['full_name']} | {l['email']} | {l['status']}")
        elif choice == "3":
            # fecha del evento simulada
            event_date = datetime(2025, 11, 20, 9, 0, 0)
            notifications.simulate_reminders(event_date)
        elif choice == "4":
            checkin.checkin_from_input()
        elif choice == "5":
            analytics.show_dashboard()
        elif choice == "6":
            simulate_full_flow()
        elif choice == "7":
            print("Saliendo...")
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    ensure_folders()
    database.init_db()
    show_menu()
