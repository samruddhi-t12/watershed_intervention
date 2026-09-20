import os
import json
import math
from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine, Base
from backend.models.domain import InterventionDB
from backend.services.cross_validation import validate_evidence
from backend.services.scoring_engine import calculate_scores
from backend.services.priority_engine import get_priority

def generate_spatial_data_and_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    # Khed, Pune Bounding Box roughly: Lat 18.80 to 18.90, Lng 73.80 to 73.95
    # Spread 16 interventions
    
    scenarios = [
        # Case A: High-confidence positive-impact (P3)
        {"work_code": "43933634", "type": "Check Dam", "lat": 18.850, "lng": 73.850,
         "field": {"has_photo": True, "water_presence": 0.8, "vegetation": 0.7, "image_quality": 0.9, "geofence_valid": True},
         "sat": {"savi_trend": 0.5, "mndwi_trend": 0.6, "temporal_consistency": 0.8, "cloud_free_ratio": 0.9},
         "ctx": {"ref_zone_diff": 0.4, "rainfall": "Normal", "hydro_valid": True}},
        # Case B: Low-confidence / no field photo (P2)
        {"work_code": "43933635", "type": "Farm Pond", "lat": 18.820, "lng": 73.880,
         "field": {"has_photo": False, "water_presence": 0.0, "vegetation": 0.0, "image_quality": 0.0, "geofence_valid": False},
         "sat": {"savi_trend": 0.2, "mndwi_trend": 0.3, "temporal_consistency": 0.6, "cloud_free_ratio": 0.7},
         "ctx": {"ref_zone_diff": 0.1, "rainfall": "Normal", "hydro_valid": True}},
        # Case C: Conflicting field-vs-satellite evidence (P1)
        {"work_code": "43933636", "type": "Contour Trench", "lat": 18.880, "lng": 73.900,
         "field": {"has_photo": True, "water_presence": 0.9, "vegetation": 0.8, "image_quality": 0.9, "geofence_valid": True},
         "sat": {"savi_trend": -0.2, "mndwi_trend": -0.4, "temporal_consistency": 0.4, "cloud_free_ratio": 0.8},
         "ctx": {"ref_zone_diff": -0.3, "rainfall": "Deficit", "hydro_valid": True}},
        # Case D: Hydrologically invalid check dam (P1)
        {"work_code": "43933637", "type": "Check Dam", "lat": 18.860, "lng": 73.920,
         "field": {"has_photo": True, "water_presence": 0.4, "vegetation": 0.3, "image_quality": 0.7, "geofence_valid": True},
         "sat": {"savi_trend": 0.1, "mndwi_trend": 0.1, "temporal_consistency": 0.5, "cloud_free_ratio": 0.6},
         "ctx": {"ref_zone_diff": 0.0, "rainfall": "Normal", "hydro_valid": False}}
    ]

    # Generate 12 more spread out
    grid_points = [(18.81 + (i//4)*0.02, 73.81 + (i%4)*0.03) for i in range(12)]
    for i in range(12):
        lat, lng = grid_points[i]
        scenarios.append({
            "work_code": f"439336{38+i}", "type": "Check Dam", "lat": lat, "lng": lng,
            "field": {"has_photo": True, "water_presence": 0.5, "vegetation": 0.5, "image_quality": 0.8, "geofence_valid": True},
            "sat": {"savi_trend": 0.2, "mndwi_trend": 0.2, "temporal_consistency": 0.7, "cloud_free_ratio": 0.8},
            "ctx": {"ref_zone_diff": 0.2, "rainfall": "Normal", "hydro_valid": True}
        })

    for s in scenarios:
        cv_status = validate_evidence(s['field'], s['sat'])
        impact, confidence = calculate_scores(s['field'], s['sat'], cv_status)
        data_completeness = 1.0 if s['field']['has_photo'] else 0.5
        priority, reason = get_priority(cv_status, s['ctx']['hydro_valid'], confidence, data_completeness)

        db.add(InterventionDB(
            work_code=s['work_code'], type=s['type'], lat=s['lat'], lng=s['lng'],
            field_has_photo=s['field']['has_photo'], field_water_presence=s['field']['water_presence'],
            field_vegetation=s['field']['vegetation'], field_image_quality=s['field']['image_quality'],
            field_geofence_valid=s['field']['geofence_valid'], sat_savi_trend=s['sat']['savi_trend'],
            sat_mndwi_trend=s['sat']['mndwi_trend'], sat_temporal_consistency=s['sat']['temporal_consistency'],
            sat_cloud_free_ratio=s['sat']['cloud_free_ratio'], ctx_ref_zone_diff=s['ctx']['ref_zone_diff'],
            ctx_rainfall=s['ctx']['rainfall'], ctx_hydro_valid=s['ctx']['hydro_valid'],
            cv_status=cv_status, score_impact=impact, score_confidence=confidence,
            priority=priority, priority_reason=reason
        ))
    
    db.commit()
    db.close()

    # Generate spatial GeoJSON layers
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "geojson")
    os.makedirs(data_dir, exist_ok=True)
    
    # 1. Hydrology (Lines crossing valid interventions)
    hydro_features = []
    for s in scenarios:
        if s["ctx"]["hydro_valid"]:
            # Stream passes through the intervention
            hydro_features.append({
                "type": "Feature",
                "properties": {"order": 2 if s["type"] == "Check Dam" else 1, "type": "Stream"},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [s["lng"] - 0.01, s["lat"] + 0.01],
                        [s["lng"], s["lat"]],
                        [s["lng"] + 0.01, s["lat"] - 0.01]
                    ]
                }
            })
    with open(os.path.join(data_dir, "hydrology.geojson"), "w") as f:
        json.dump({"type": "FeatureCollection", "features": hydro_features}, f)

    # 2. Dense Grid for SAVI and MNDWI to simulate raster
    # We will generate a 30x30 grid over the bounding box
    lat_min, lat_max = 18.80, 18.90
    lng_min, lng_max = 73.80, 73.95
    grid_size = 30
    lat_step = (lat_max - lat_min) / grid_size
    lng_step = (lng_max - lng_min) / grid_size

    def create_grid(value_func, before_func):
        features = []
        for i in range(grid_size):
            for j in range(grid_size):
                clat = lat_min + i * lat_step
                clng = lng_min + j * lng_step
                # Calculate deterministic value based on distance to scenarios
                val_after = value_func(clat, clng)
                val_before = before_func(clat, clng)
                features.append({
                    "type": "Feature",
                    "properties": {"value_after": val_after, "value_before": val_before},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[clng, clat], [clng+lng_step, clat], [clng+lng_step, clat+lat_step], [clng, clat+lat_step], [clng, clat]]]
                    }
                })
        return {"type": "FeatureCollection", "features": features}

    def savi_after(lat, lng):
        base = 0.2
        for s in scenarios:
            dist = math.hypot(lat - s['lat'], lng - s['lng'])
            if dist < 0.02:
                base += s['sat']['savi_trend'] * (1 - dist/0.02)
        return max(-1, min(1, base))
        
    def savi_before(lat, lng):
        return 0.2

    def mndwi_after(lat, lng):
        base = -0.2
        for s in scenarios:
            dist = math.hypot(lat - s['lat'], lng - s['lng'])
            if dist < 0.015:
                base += s['sat']['mndwi_trend'] * (1 - dist/0.015)
        return max(-1, min(1, base))

    def mndwi_before(lat, lng):
        return -0.2

    with open(os.path.join(data_dir, "savi.geojson"), "w") as f:
        json.dump(create_grid(savi_after, savi_before), f)
        
    with open(os.path.join(data_dir, "mndwi.geojson"), "w") as f:
        json.dump(create_grid(mndwi_after, mndwi_before), f)

    print("Redesigned spatial data and DB generated.")

if __name__ == "__main__":
    generate_spatial_data_and_db()
