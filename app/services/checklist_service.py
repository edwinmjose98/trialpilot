from app.models.procedure_definition import ProcedureDefinition
from app.models.checklist_item import ChecklistItem

def create_checklist_item(visit_schedule, db):
    # for visit_schedule in visit_schedule:
    procedure_defintions = db.query(ProcedureDefinition).filter(ProcedureDefinition.visit_definition_id==visit_schedule.visit_definition_id).all()
    for proc_def in procedure_defintions:
        checkListitem = ChecklistItem(visit_schedule_id = visit_schedule.id,
                                      procedure_definition_id = proc_def.id
                                      )
        
        db.add(checkListitem)

    db.commit()