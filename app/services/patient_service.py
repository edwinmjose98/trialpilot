from app.models.visit_definiton import VisitDefinition
from datetime import timedelta
from app.models.visit_schedule import VisitSchedule

def create_visit_schedule_for_patient(patient,db):
    visit_definitions = db.query(VisitDefinition).filter(VisitDefinition.protocol_id==patient.protocol_id).all()

    for visit_def in visit_definitions:
        scheduled_date = patient.enrollment_date + timedelta(days=visit_def.day_number)
        visit_schedule = VisitSchedule(patient_id=patient.id, scheduled_date=scheduled_date, visit_definition_id = visit_def.id)
        db.add(visit_schedule)

    db.commit()