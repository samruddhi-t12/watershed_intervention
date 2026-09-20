import os
import json
import math
import random
import sqlite3

def generate_data():
    db_path = os.path.join(os.path.dirname(__file__), "backend", "test.db") # Wait, what is the DB path? It's "backend/database.db" or "backend/test.db" ?
    # In earlier scripts, database is created in the root or backend folder depending on engine bind. Let's just use the coordinates we know: 18.85, 73.85 and 18.86, 73.86
    interventions = [
        {"id": 1, "lat": 18.850, "lng": 73.850, "type": "Check Dam", "priority": "P2", "status_badge": "REVIEW"},
        {"id": 2, "lat": 18.860, "lng": 73.860, "type": "Check Dam", "priority": "P1", "status_badge": "FLAGGED"},
    ]
    
    # Try fetching from sqlite if exists
    db_file = os.path.join(os.path.dirname(__file__), "backend", "water.db")
    if not os.path.exists(db_file):
        db_file = "water.db"
    
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("SELECT id, lat, lng, type, priority, status_badge FROM interventions WHERE lat IS NOT NULL")
        rows = c.fetchall()
        if rows:
            interventions = [{"id": r[0], "lat": r[1], "lng": r[2], "type": r[3], "priority": r[4], "status_badge": r[5]} for r in rows]
        conn.close()
    except Exception as e:
        pass

    center_lat = 18.855
    center_lng = 73.855

    # Generate irregular watershed boundary
    num_points = 16
    boundary_coords = []
    base_radius = 0.02 # approx 2km
    for i in range(num_points):
        angle = (i / num_points) * 2 * math.pi
        r = base_radius + random.uniform(-0.005, 0.005)
        boundary_coords.append([center_lng + r * math.cos(angle), center_lat + r * math.sin(angle)])
    boundary_coords.append(boundary_coords[0]) # close polygon

    boundary_geojson = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {"name": "PUNE-WDC-1 Micro-Watershed"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [boundary_coords]
            }
        }]
    }

    # Generate grid intersecting bounding box
    min_lng = min(p[0] for p in boundary_coords)
    max_lng = max(p[0] for p in boundary_coords)
    min_lat = min(p[1] for p in boundary_coords)
    max_lat = max(p[1] for p in boundary_coords)

    step = 0.0015 # ~150m grid
    grid_features = []

    # Point in polygon check
    def point_in_polygon(x, y, poly):
        n = len(poly)
        inside = False
        p1x, p1y = poly[0]
        for i in range(1, n + 1):
            p2x, p2y = poly[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    years = [2021, 2022, 2023, 2024, 2025]
    rainfall_data = {
        2021: {"context": "Normal", "factor": 1.0},
        2022: {"context": "Excess Rainfall", "factor": 1.2},
        2023: {"context": "Deficit Rainfall", "factor": 0.6},
        2024: {"context": "Normal", "factor": 1.0},
        2025: {"context": "Normal", "factor": 1.0}
    }

    cell_id = 0
    lat = min_lat
    while lat < max_lat:
        lng = min_lng
        while lng < max_lng:
            # Check center of cell
            clat = lat + step/2
            clng = lng + step/2
            if point_in_polygon(clng, clat, boundary_coords):
                
                # Calculate distance effects to interventions
                closest_inv = None
                min_dist = float('inf')
                for inv in interventions:
                    dist = math.sqrt((clat - inv["lat"])**2 + (clng - inv["lng"])**2)
                    if dist < min_dist:
                        min_dist = dist
                        closest_inv = inv
                
                # Base coherence values using a combo of perlin-like sin waves and distance
                base_veg = math.sin(clat * 1000) * math.cos(clng * 1000) * 0.2
                base_water = math.cos(clat * 800) * math.sin(clng * 800) * 0.2
                
                yearly_data = {}
                for yr in years:
                    r_context = rainfall_data[yr]["context"]
                    r_factor = rainfall_data[yr]["factor"]
                    
                    time_progression = (yr - 2021) / 4.0
                    
                    is_near_flagged = closest_inv and closest_inv["status_badge"] == "FLAGGED" and min_dist < 0.008
                    is_near_verified = closest_inv and closest_inv["status_badge"] != "FLAGGED" and min_dist < 0.008
                    
                    if is_near_flagged:
                        change_val = base_veg - 0.3 * time_progression * r_factor
                    elif is_near_verified:
                        change_val = base_veg + 0.6 * time_progression * r_factor
                    else:
                        change_val = base_veg + 0.1 * time_progression * r_factor
                        
                    change_val += random.uniform(-0.05, 0.05)
                    
                    if change_val < -0.3:
                        cClass = "severe_degradation"
                        reason = f"Severe loss of biomass, unresponsive to {r_context.lower()}."
                    elif change_val < -0.1:
                        cClass = "moderate_degradation"
                        reason = f"Negative trend observed during {r_context.lower()}."
                    elif change_val < 0.1:
                        cClass = "stable"
                        reason = f"Stable baseline under {r_context.lower()} conditions."
                    elif change_val < 0.3:
                        cClass = "improving"
                        reason = f"Positive moisture/vegetation retention despite {r_context.lower()}."
                    else:
                        cClass = "strong_improvement"
                        reason = f"Strong structural improvement fully leveraging {r_context.lower()}."
                        
                    yearly_data[str(yr)] = {
                        "deltaSAVI": round(change_val * 0.8, 3),
                        "deltaMNDWI": round(change_val * 0.5, 3),
                        "rainfallContext": r_context,
                        "changeClass": cClass,
                        "reasonText": reason
                    }

                grid_features.append({
                    "type": "Feature",
                    "properties": {
                        "cell_id": cell_id,
                        "years": yearly_data
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[lng, lat], [lng+step, lat], [lng+step, lat+step], [lng, lat+step], [lng, lat]]]
                    }
                })
                cell_id += 1
            lng += step
        lat += step

    grid_geojson = {
        "type": "FeatureCollection",
        "features": grid_features
    }

    os.makedirs(os.path.join(os.path.dirname(__file__), "frontend", "public"), exist_ok=True)
    with open(os.path.join(os.path.dirname(__file__), "frontend", "public", "watershed.geojson"), "w") as f:
        json.dump(boundary_geojson, f)
    with open(os.path.join(os.path.dirname(__file__), "frontend", "public", "change_grid.geojson"), "w") as f:
        json.dump(grid_geojson, f)

if __name__ == "__main__":
    generate_data()
