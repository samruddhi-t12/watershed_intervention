import sqlite3
import json
import math
import os
from shapely.geometry import shape, Point

def validate_check_dams():
    # Load the real stream network
    pub_dir = os.path.join(os.path.dirname(__file__), "frontend", "public")
    streams_path = os.path.join(pub_dir, "real_streams.geojson")
    
    with open(streams_path, "r") as f:
        streams_data = json.load(f)
        
    # Create shapely LineStrings for all streams
    stream_lines = []
    for feature in streams_data.get("features", []):
        geom = shape(feature["geometry"])
        stream_lines.append(geom)

    # Connect to the SQLite database
    db_path = os.path.join(os.path.dirname(__file__), "data", "sqlite", "demo_db.sqlite")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, lat, lng FROM interventions WHERE type='Check Dam' AND lat IS NOT NULL")
    check_dams = cursor.fetchall()
    
    updates = []
    
    # Approx threshold: 0.0005 degrees is roughly 50 meters
    THRESHOLD = 0.0005
    
    valid_count = 0
    invalid_count = 0
    
    for row in check_dams:
        inv_id, lat, lng = row
        point = Point(lng, lat)
        
        # Check distance to nearest stream
        is_valid = False
        for line in stream_lines:
            if point.distance(line) <= THRESHOLD:
                is_valid = True
                break
                
        # flag_hydro is True if the intervention is NOT valid
        updates.append((not is_valid, inv_id))
        
        if is_valid:
            valid_count += 1
        else:
            invalid_count += 1
            
    # Update database: flag_hydro is True if invalid
    cursor.executemany("UPDATE interventions SET flag_hydro = ? WHERE id = ?", updates)
    conn.commit()
    conn.close()
    
    print(f"Hydrological validation complete. Valid: {valid_count}, Invalid/Flagged: {invalid_count}")

if __name__ == "__main__":
    validate_check_dams()
