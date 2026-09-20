import os
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
