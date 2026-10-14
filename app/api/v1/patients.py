from fastapi import APIRouter, Depends
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from typing import List
from app.services import patient_service

router = APIRouter()


@router.post("/", response_model=PatientResponse)
def create_patient(patient: PatientCreate, db : Session = Depends(get_db)):
    db_patient=Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    patient_service.create_visit_schedule_for_patient(db_patient, db)
    return db_patient


@router.get("/", response_model=List[PatientResponse])
def get_patients(db:Session = Depends(get_db)):
    patients = db.query(Patient).all()
    return patients


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id==id).first()
    return patient