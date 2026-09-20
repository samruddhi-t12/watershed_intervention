import sqlite3
import random
import os
import shutil
import json

def populate():
    # 1. Update SQLite
    conn = sqlite3.connect("data/sqlite/demo_db.sqlite")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, work_code FROM interventions ORDER BY id")
    rows = cursor.fetchall()
    
    # First 14 are populated, last 2 remain unavailable
    populate_ids = [r[0] for r in rows[:14]]
    unavailable_ids = [r[0] for r in rows[14:]]
    
    # Get bounding box of watershed roughly for points
    pub_dir = os.path.join(os.path.dirname(__file__), "frontend", "public")
    ws_path = os.path.join(pub_dir, "watershed_real.geojson")
    with open(ws_path) as f:
        poly = json.load(f)["features"][0]["geometry"]["coordinates"][0]
        
    min_lng, max_lng = min(p[0] for p in poly), max(p[0] for p in poly)
    min_lat, max_lat = min(p[1] for p in poly), max(p[1] for p in poly)
    
    def random_point():
        # Rough point in bbox
        return random.uniform(min_lat, max_lat), random.uniform(min_lng, max_lng)
        
    for inv_id in populate_ids:
        lat, lng = random_point()
        score_impact = round(random.uniform(0.3, 0.95), 2)
        score_confidence = round(random.uniform(0.5, 0.95), 2)
        
        # Mix statuses
        r = random.random()
        if r < 0.3:
            badge = "VERIFIED"
            priority = "P3"
            reason = "Consistent positive indicators."
        elif r < 0.7:
            badge = "REVIEW"
            priority = "P2"
            reason = "Moderate discrepancies or partial impact."
        else:
            badge = "FLAGGED"
            priority = "P1"
            reason = "Significant conflict detected."
            
        ndvi_change = round(random.uniform(-0.1, 0.5), 2)
        mndwi_change = round(random.uniform(-0.1, 0.3), 2)
        water_spread = round(random.uniform(-5, 25), 1)
        
        cursor.execute("""
            UPDATE interventions SET 
                lat=?, lng=?, data_status='DEMO', status_badge=?,
                priority=?, priority_reason=?,
                score_impact=?, score_confidence=?,
                ndvi_change=?, mndwi_change=?, water_spread_change=?,
                flag_missing_photo=False
            WHERE id=?
        """, (lat, lng, badge, priority, reason, score_impact, score_confidence, ndvi_change, mndwi_change, water_spread, inv_id))
        
    for inv_id in unavailable_ids:
        cursor.execute("""
            UPDATE interventions SET 
                lat=NULL, lng=NULL, data_status='UNAVAILABLE', status_badge='REVIEW',
                score_impact=NULL, score_confidence=NULL
            WHERE id=?
        """, (inv_id,))
        
    conn.commit()
    conn.close()
    
    # 2. Copy images for the first 14
    photos_dir = os.path.join(pub_dir, "field_photos")
    existing_photos = [f for f in os.listdir(photos_dir) if f.endswith('.jpg')]
    if not existing_photos:
        print("No photos found to copy.")
        return
        
    for row in rows[:14]:
        work_code = row[1]
        target_path = os.path.join(photos_dir, f"{work_code}.jpg")
        if not os.path.exists(target_path):
            src_photo = random.choice(existing_photos)
            shutil.copy(os.path.join(photos_dir, src_photo), target_path)
            
    # For the last 2, make sure there are NO photos
    for row in rows[14:]:
        work_code = row[1]
        target_path = os.path.join(photos_dir, f"{work_code}.jpg")
        if os.path.exists(target_path):
            os.remove(target_path)
            
    print("Database updated for 14 demo records and 2 unavailable. Images duplicated.")

if __name__ == "__main__":
    populate()
