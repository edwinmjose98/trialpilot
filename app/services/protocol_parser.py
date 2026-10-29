from openai import OpenAI
from app.core.config import settings
import json
from app.models.visit_definiton import VisitDefinition
from app.models.procedure_definition import ProcedureDefinition
client = OpenAI(api_key=settings.OPENAI_API_KEY)
def parse_protocol_text(protocol_text: str)-> dict:
    prompt = f"""
You are a clinical trial expert. Read this protocol document and extract all study visits with their timing and required procedures. The schedule might be in a table, or described in prose. Use your medical knowledge to identify it regardless of format.
I want you to take the knowledge of these timing and required procedures and return the entire data in the form of a json objedt structure given below. 
'day_number' is the number of days from the patient's enrollment/baseline date (Day 0). Screening visits have negative day numbers.

{{
"visit_definitions": [ {{ "name": "Screening", "day_number": -28, "window_before": 0, "window_after": 3, "is_mandatory": true, "procedures": [ {{"name": "CBC", "procedure_type": "LAB", "is_mandatory": true}}, {{"name": "CMP", "procedure_type": "LAB", "is_mandatory": true}} ] }},
{{ "name": "Baseline", "day_number": 0, "window_before": 0, "window_after": 0, "is_mandatory": true, "procedures": [ {{"name": "CT Scan", "procedure_type": "IMAGING", "is_mandatory": true}}, {{"name": "CMP", "procedure_type": "LAB", "is_mandatory": true}} ] }},
{{ "name": "Week 4", "day_number": 28, "window_before": 3, "window_after": 3, "is_mandatory": true, "procedures": [ {{"name": "CBC", "procedure_type": "LAB", "is_mandatory": true}}, {{"name": "CMP", "procedure_type": "LAB", "is_mandatory": true}} ] }} ] }}
Procedure types must be one of: LAB, ASSESSMENT, IMAGING, QUESTIONNAIRE, TREATMENT


Protocol document: {protocol_text}

Extract ALL visits found in the document, not just the first one. If a procedure's mandatory status is not explicitly stated, assume it is mandatory.
Return only valid JSON, no explanation.
"""
    response = client.chat.completions.create(model="gpt-4o", messages = [{"role":"user", "content": prompt}],response_format={"type":"json_object"})
    return json.loads(response.choices[0].message.content)

def save_parsed_protocol(protocol_id, parsed_data, db):
    for visit in parsed_data["visit_definitions"]:
        visit_def = VisitDefinition(protocol_id=protocol_id,
                                    name=visit["name"],
                                    day_number=visit["day_number"],
                                    window_before=visit["window_before"],
                                    window_after=visit["window_after"],
                                    is_mandatory=visit["is_mandatory"])
        db.add(visit_def)
        db.flush()
        for procedure_def in visit.get("procedures", []):
            proc = ProcedureDefinition(visit_definition_id=visit_def.id, name=procedure_def["name"], procedure_type=procedure_def["procedure_type"], is_mandatory=procedure_def["is_mandatory"])
            db.add(proc)
            
    db.commit()