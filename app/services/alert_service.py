from datetime import date, timedelta
from app.models.visit_schedule import VisitSchedule, VisitStatus
from app.models.visit_definiton import VisitDefinition
from app.models.alert import Alert, AlertType

def check_and_create_alert(db):
    today = date.today()
    print(f"Today: {today}")
    visit_schedules = db.query(VisitSchedule).filter(VisitSchedule.status==VisitStatus.SCHEDULED).all()
    print(f"Found {len(visit_schedules)} scheduled visits")
    for visit_schedule in visit_schedules:
        visit_def = db.query(VisitDefinition).filter(VisitDefinition.id == visit_schedule.visit_definition_id).first()
        last_valid_date = visit_schedule.scheduled_date + timedelta(days=visit_def.window_after)
        print(f"Visit {visit_schedule.id}: scheduled={visit_schedule.scheduled_date}, last_valid={last_valid_date}, today={today}")
        if today > last_valid_date:
            existing_alert=db.query(Alert).filter(Alert.visit_schedule_id==visit_schedule.id,
                                                  Alert.alert_type==AlertType.VISIT_OVERDUE,
                                                  Alert.is_resolved==False).first()
            if not existing_alert:
                print(f"Creating OVERDUE alert for visit {visit_schedule.id}")
                overdue_alert=Alert(
                patient_id=visit_schedule.patient_id,
                visit_schedule_id = visit_schedule.id,
                alert_type=AlertType.VISIT_OVERDUE,
                message="The patient has missed the window. Protocol deviation procedures should be initiated.",
                is_resolved=False)
                db.add(overdue_alert)
            # VISIT_OVERDUE
        elif (last_valid_date - today).days <= 2:
            existing_alert=db.query(Alert).filter(Alert.visit_schedule_id==visit_schedule.id,
                                                  Alert.alert_type==AlertType.WINDOW_CLOSING,
                                                  Alert.is_resolved==False).first()
            if not existing_alert:
                window_closing_alert=Alert(
                patient_id=visit_schedule.patient_id,
                visit_schedule_id = visit_schedule.id,
                alert_type=AlertType.WINDOW_CLOSING,
                message="The window is closing. Please alert the patient.",
                is_resolved=False)
                db.add(window_closing_alert)

    db.commit()
    print("Committed to database")