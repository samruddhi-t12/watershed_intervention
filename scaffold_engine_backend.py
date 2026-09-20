import os
import sys

backend_files = {
    "backend/models/domain.py": """from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, Boolean
from backend.database import Base

class InterventionDB(Base):
    __tablename__ = "interventions"
    id = Column(Integer, primary_key=True, index=True)
    work_code = Column(String, index=True)
    type = Column(String)
    data_status = Column(String) # REAL, DEMO, UNAVAILABLE
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    
    score_impact = Column(Float, nullable=True)
    score_confidence = Column(Float, nullable=True)
    priority = Column(String)
    status_badge = Column(String)
    priority_reason = Column(String)
    
    impact_veg = Column(Float, nullable=True)
    impact_water = Column(Float, nullable=True)
    impact_lulc = Column(Float, nullable=True)
    impact_temporal = Column(Float, nullable=True)
    impact_field = Column(Float, nullable=True)
    
    ndvi_change = Column(Float, nullable=True)
    mndwi_change = Column(Float, nullable=True)
    water_spread_change = Column(Float, nullable=True)
    
    flag_hydro = Column(Boolean, default=False)
    flag_water = Column(Boolean, default=False)
    flag_veg = Column(Boolean, default=False)
    flag_season = Column(Boolean, default=False)
    flag_conflict = Column(Boolean, default=False)
    flag_missing_photo = Column(Boolean, default=True)

class InterventionSchema(BaseModel):
    id: int
    work_code: str
    type: str
    data_status: str
    lat: Optional[float]
    lng: Optional[float]
    score_impact: Optional[float]
    score_confidence: Optional[float]
    priority: str
    status_badge: str
    priority_reason: str
    impact_veg: Optional[float]
    impact_water: Optional[float]
    impact_lulc: Optional[float]
    impact_temporal: Optional[float]
    impact_field: Optional[float]
    ndvi_change: Optional[float]
    mndwi_change: Optional[float]
    water_spread_change: Optional[float]
    flag_hydro: bool
    flag_water: bool
    flag_veg: bool
    flag_season: bool
    flag_conflict: bool
    flag_missing_photo: bool
    class Config:
        from_attributes = True
""",
    "backend/routers/dashboard.py": """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.domain import InterventionDB

router = APIRouter()

@router.get("/api/v1/dashboard/metrics")
def get_metrics(db: Session = Depends(get_db)):
    all_invs = db.query(InterventionDB).all()
    total = len(all_invs)
    check_dams = len([i for i in all_invs if i.type == "Check Dam"])
    field_evidence = len([i for i in all_invs if not i.flag_missing_photo])
    needs_review = len([i for i in all_invs if i.status_badge == "REVIEW"])
    verified = len([i for i in all_invs if i.status_badge == "VERIFIED"])
    flagged = len([i for i in all_invs if i.status_badge == "FLAGGED"])
    
    return {
        "total": total,
        "check_dams": check_dams,
        "field_evidence": field_evidence,
        "needs_review": needs_review,
        "verified": verified,
        "flagged": flagged,
        "satellite_coverage": 1 if any(i.data_status == "DEMO" or i.data_status == "REAL" for i in all_invs) else 0
    }
""",
    "scripts/seed_engine.py": """import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine, Base
from backend.models.domain import InterventionDB

def seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    work_codes = [str(x) for x in range(43933634, 43933650)]
    
    for idx, wc in enumerate(work_codes):
        if idx == 0:
            db.add(InterventionDB(
                work_code=wc, type="Check Dam", data_status="DEMO",
                lat=18.850, lng=73.850,
                score_impact=72, score_confidence=84,
                priority="P2", status_badge="REVIEW", priority_reason="Water response detected, seasonal variation requires review",
                impact_veg=18, impact_water=24, impact_lulc=14, impact_temporal=9, impact_field=7,
                ndvi_change=0.15, mndwi_change=0.22, water_spread_change=212,
                flag_hydro=False, flag_water=False, flag_veg=False, flag_season=True, flag_conflict=False, flag_missing_photo=False
            ))
        elif idx == 1:
            db.add(InterventionDB(
                work_code=wc, type="Check Dam", data_status="DEMO",
                lat=18.860, lng=73.860,
                score_impact=30, score_confidence=40,
                priority="P1", status_badge="FLAGGED", priority_reason="Evidence conflict detected",
                impact_veg=5, impact_water=5, impact_lulc=5, impact_temporal=10, impact_field=5,
                ndvi_change=-0.05, mndwi_change=-0.10, water_spread_change=-10,
                flag_hydro=True, flag_water=True, flag_veg=True, flag_season=False, flag_conflict=True, flag_missing_photo=False
            ))
        else:
            db.add(InterventionDB(
                work_code=wc, type="Check Dam", data_status="UNAVAILABLE",
                lat=None, lng=None,
                score_impact=None, score_confidence=None,
                priority="P3", status_badge="REVIEW", priority_reason="Coordinates unavailable",
                impact_veg=None, impact_water=None, impact_lulc=None, impact_temporal=None, impact_field=None,
                ndvi_change=None, mndwi_change=None, water_spread_change=None,
                flag_hydro=False, flag_water=False, flag_veg=False, flag_season=False, flag_conflict=False, flag_missing_photo=True
            ))
            
    db.commit()
    db.close()
    
    geojson_dir = os.path.join(os.path.dirname(__file__), "..", "data", "geojson")
    if os.path.exists(geojson_dir):
        for f in os.listdir(geojson_dir):
            if f.endswith(".geojson"):
                os.remove(os.path.join(geojson_dir, f))

if __name__ == "__main__":
    seed()
"""
}

def create_files():
    for path, content in backend_files.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    create_files()
