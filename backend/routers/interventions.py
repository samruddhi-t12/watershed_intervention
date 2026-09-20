from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.domain import InterventionDB, InterventionSchema
from typing import List

router = APIRouter()

@router.get("/api/v1/interventions", response_model=List[InterventionSchema])
def list_interventions(db: Session = Depends(get_db)):
    return db.query(InterventionDB).all()

@router.get("/api/v1/interventions/{id}", response_model=InterventionSchema)
def get_intervention(id: int, db: Session = Depends(get_db)):
    return db.query(InterventionDB).filter(InterventionDB.id == id).first()

@router.get("/api/v1/queue", response_model=List[InterventionSchema])
def get_queue(db: Session = Depends(get_db)):
    interventions = db.query(InterventionDB).all()
    priority_order = {"P1": 1, "P2": 2, "P3": 3}
    return sorted(interventions, key=lambda x: priority_order.get(x.priority, 4))
