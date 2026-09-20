import os

backend_files = {
    "backend/models/domain.py": """from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Float, Boolean, JSON
from backend.database import Base

class InterventionDB(Base):
    __tablename__ = "interventions"
    id = Column(Integer, primary_key=True, index=True)
    work_code = Column(String, index=True)
    type = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    field_has_photo = Column(Boolean)
    field_water_presence = Column(Float)
    field_vegetation = Column(Float)
    field_image_quality = Column(Float)
    field_geofence_valid = Column(Boolean)
    sat_savi_trend = Column(Float)
    sat_mndwi_trend = Column(Float)
    sat_temporal_consistency = Column(Float)
    sat_cloud_free_ratio = Column(Float)
    ctx_ref_zone_diff = Column(Float)
    ctx_rainfall = Column(String)
    ctx_hydro_valid = Column(Boolean)
    cv_status = Column(String)
    score_impact = Column(Float)
    score_confidence = Column(Float)
    priority = Column(String)
    priority_reason = Column(String)

class InterventionSchema(BaseModel):
    id: int
    work_code: str
    type: str
    lat: float
    lng: float
    field_has_photo: bool
    field_water_presence: float
    field_vegetation: float
    field_image_quality: float
    field_geofence_valid: bool
    sat_savi_trend: float
    sat_mndwi_trend: float
    sat_temporal_consistency: float
    sat_cloud_free_ratio: float
    ctx_ref_zone_diff: float
    ctx_rainfall: str
    ctx_hydro_valid: bool
    cv_status: str
    score_impact: float
    score_confidence: float
    priority: str
    priority_reason: str
    class Config:
        orm_mode = True
""",
    "backend/services/evidence_engine.py": """def process_field_evidence(intervention):
    return {
        "has_photo": intervention.field_has_photo,
        "water_presence": intervention.field_water_presence,
        "vegetation": intervention.field_vegetation,
        "image_quality": intervention.field_image_quality,
        "geofence_valid": intervention.field_geofence_valid
    }
""",
    "backend/services/satellite_engine.py": """def process_satellite_evidence(intervention):
    return {
        "savi_trend": intervention.sat_savi_trend,
        "mndwi_trend": intervention.sat_mndwi_trend,
        "temporal_consistency": intervention.sat_temporal_consistency,
        "cloud_free_ratio": intervention.sat_cloud_free_ratio
    }
""",
    "backend/services/reference_zone.py": """def compare_reference_zone(intervention):
    return intervention.ctx_ref_zone_diff
""",
    "backend/services/rainfall_context.py": """def get_rainfall_context(intervention):
    return intervention.ctx_rainfall
""",
    "backend/services/hydrology_engine.py": """def validate_hydrology(intervention):
    return intervention.ctx_hydro_valid
""",
    "backend/services/cross_validation.py": """def validate_evidence(field, sat):
    # Mock logic based on demo scenarios
    if field['has_photo'] and field['water_presence'] > 0.5 and sat['mndwi_trend'] < 0:
        return "CONFLICT"
    elif field['has_photo'] and field['water_presence'] > 0.5 and sat['mndwi_trend'] > 0:
        return "AGREEMENT"
    else:
        return "INCONCLUSIVE"
""",
    "backend/services/scoring_engine.py": """def calculate_scores(field, sat, cv_status):
    impact = 0.25*sat['savi_trend'] + 0.25*sat['mndwi_trend'] + 0.20*0.5 + 0.15*sat['temporal_consistency'] + 0.15*field['water_presence']
    source_agreement = 1.0 if cv_status == "AGREEMENT" else (0.0 if cv_status == "CONFLICT" else 0.5)
    data_completeness = 1.0 if field['has_photo'] else 0.5
    confidence = 0.25*data_completeness + 0.20*field['image_quality'] + 0.20*0.8 + 0.20*source_agreement + 0.15*sat['cloud_free_ratio']
    return max(0, min(1, impact)), max(0, min(1, confidence))
""",
    "backend/services/priority_engine.py": """def get_priority(cv_status, hydro_valid, confidence, data_completeness):
    if cv_status == "CONFLICT":
        return "P1", "Evidence conflict detected between field photo and satellite trends."
    if not hydro_valid:
        return "P1", "Hydrological validity failure: structure not on modeled drainage line."
    if confidence < 0.5:
        return "P1", "Very low confidence requires immediate field verification."
    
    if data_completeness < 1.0:
        return "P2", "Incomplete evidence (missing field photo)."
    if confidence < 0.75:
        return "P2", "Medium confidence requires routine review."
        
    return "P3", "Evidence is consistent, high confidence, no immediate verification signal."
""",
    "backend/routers/dashboard.py": """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.domain import InterventionDB

router = APIRouter()

@router.get("/api/v1/dashboard/metrics")
def get_metrics(db: Session = Depends(get_db)):
    all_interventions = db.query(InterventionDB).all()
    total = len(all_interventions)
    p1 = len([i for i in all_interventions if i.priority == "P1"])
    p2 = len([i for i in all_interventions if i.priority == "P2"])
    p3 = len([i for i in all_interventions if i.priority == "P3"])
    conflict = len([i for i in all_interventions if i.cv_status == "CONFLICT"])
    
    avg_impact = sum([i.score_impact for i in all_interventions]) / total if total > 0 else 0
    avg_confidence = sum([i.score_confidence for i in all_interventions]) / total if total > 0 else 0
    
    return {
        "total": total,
        "p1": p1,
        "p2": p2,
        "p3": p3,
        "conflicts": conflict,
        "avg_impact": round(avg_impact, 2),
        "avg_confidence": round(avg_confidence, 2)
    }
""",
    "backend/routers/interventions.py": """from fastapi import APIRouter, Depends
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
""",
    "backend/routers/admin.py": """from fastapi import APIRouter
import subprocess
import os

router = APIRouter()

@router.post("/api/v1/admin/reset")
def reset_db():
    script_path = os.path.join(os.path.dirname(__file__), "../../scripts/generate_demo_data.py")
    subprocess.run(["python", script_path], check=True)
    return {"status": "success", "message": "Database reset to deterministic demo state."}
""",
    "backend/main.py": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import dashboard, interventions, admin
from backend.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SIH26015 MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard.router)
app.include_router(interventions.router)
app.include_router(admin.router)

@app.get("/health")
def health():
    return {"status": "ok"}
"""
}

def create_files():
    for path, content in backend_files.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(content)

if __name__ == "__main__":
    create_files()
