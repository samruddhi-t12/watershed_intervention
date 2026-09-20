import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine, Base
from backend.models.domain import InterventionDB
from backend.services.cross_validation import validate_evidence
from backend.services.scoring_engine import calculate_scores
from backend.services.priority_engine import get_priority

def generate_data():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    # Anchor: Khed, Pune, Maharashtra - Chinchbaiwadi cluster
    # Works: 43933634 to 43933649
    # Base lat, lng roughly for Khed, Pune: 18.847, 73.896
    
    scenarios = [
        # Case A: High-confidence positive-impact (P3)
        {
            "work_code": "43933634",
            "type": "Check Dam",
            "lat": 18.847, "lng": 73.896,
            "field": {"has_photo": True, "water_presence": 0.8, "vegetation": 0.7, "image_quality": 0.9, "geofence_valid": True},
            "sat": {"savi_trend": 0.5, "mndwi_trend": 0.6, "temporal_consistency": 0.8, "cloud_free_ratio": 0.9},
            "ctx": {"ref_zone_diff": 0.4, "rainfall": "Normal", "hydro_valid": True}
        },
        # Case B: Low-confidence / no field photo (P2)
        {
            "work_code": "43933635",
            "type": "Farm Pond",
            "lat": 18.848, "lng": 73.897,
            "field": {"has_photo": False, "water_presence": 0.0, "vegetation": 0.0, "image_quality": 0.0, "geofence_valid": False},
            "sat": {"savi_trend": 0.2, "mndwi_trend": 0.3, "temporal_consistency": 0.6, "cloud_free_ratio": 0.7},
            "ctx": {"ref_zone_diff": 0.1, "rainfall": "Normal", "hydro_valid": True}
        },
        # Case C: Conflicting field-vs-satellite evidence (P1)
        {
            "work_code": "43933636",
            "type": "Contour Trench",
            "lat": 18.849, "lng": 73.898,
            "field": {"has_photo": True, "water_presence": 0.9, "vegetation": 0.8, "image_quality": 0.9, "geofence_valid": True},
            "sat": {"savi_trend": -0.2, "mndwi_trend": -0.4, "temporal_consistency": 0.4, "cloud_free_ratio": 0.8},
            "ctx": {"ref_zone_diff": -0.3, "rainfall": "Deficit", "hydro_valid": True}
        },
        # Case D: Hydrologically invalid check dam (P1)
        {
            "work_code": "43933637",
            "type": "Check Dam",
            "lat": 18.850, "lng": 73.899,
            "field": {"has_photo": True, "water_presence": 0.4, "vegetation": 0.3, "image_quality": 0.7, "geofence_valid": True},
            "sat": {"savi_trend": 0.1, "mndwi_trend": 0.1, "temporal_consistency": 0.5, "cloud_free_ratio": 0.6},
            "ctx": {"ref_zone_diff": 0.0, "rainfall": "Normal", "hydro_valid": False}
        }
    ]

    # Generate more cases up to 16
    for i in range(38, 50): # 43933638 to 43933649
        scenarios.append({
            "work_code": f"439336{i}",
            "type": "Check Dam",
            "lat": 18.850 + (i-38)*0.001, "lng": 73.899 - (i-38)*0.001,
            "field": {"has_photo": True, "water_presence": 0.5, "vegetation": 0.5, "image_quality": 0.8, "geofence_valid": True},
            "sat": {"savi_trend": 0.2, "mndwi_trend": 0.2, "temporal_consistency": 0.7, "cloud_free_ratio": 0.8},
            "ctx": {"ref_zone_diff": 0.2, "rainfall": "Normal", "hydro_valid": True}
        })

    for s in scenarios:
        cv_status = validate_evidence(s['field'], s['sat'])
        impact, confidence = calculate_scores(s['field'], s['sat'], cv_status)
        data_completeness = 1.0 if s['field']['has_photo'] else 0.5
        priority, reason = get_priority(cv_status, s['ctx']['hydro_valid'], confidence, data_completeness)

        db_item = InterventionDB(
            work_code=s['work_code'],
            type=s['type'],
            lat=s['lat'], lng=s['lng'],
            field_has_photo=s['field']['has_photo'],
            field_water_presence=s['field']['water_presence'],
            field_vegetation=s['field']['vegetation'],
            field_image_quality=s['field']['image_quality'],
            field_geofence_valid=s['field']['geofence_valid'],
            sat_savi_trend=s['sat']['savi_trend'],
            sat_mndwi_trend=s['sat']['mndwi_trend'],
            sat_temporal_consistency=s['sat']['temporal_consistency'],
            sat_cloud_free_ratio=s['sat']['cloud_free_ratio'],
            ctx_ref_zone_diff=s['ctx']['ref_zone_diff'],
            ctx_rainfall=s['ctx']['rainfall'],
            ctx_hydro_valid=s['ctx']['hydro_valid'],
            cv_status=cv_status,
            score_impact=impact,
            score_confidence=confidence,
            priority=priority,
            priority_reason=reason
        )
        db.add(db_item)
    
    db.commit()
    db.close()
    print("Demo dataset generated successfully.")

if __name__ == "__main__":
    generate_data()
