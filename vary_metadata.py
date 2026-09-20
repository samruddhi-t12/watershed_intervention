import sqlite3
import random
import uuid

def vary_drishti_metadata():
    conn = sqlite3.connect("data/sqlite/demo_db.sqlite")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, type, work_code FROM interventions WHERE data_status = 'DEMO'")
    rows = cursor.fetchall()
    
    updates = []
    
    for row in rows:
        inv_id, inv_type, work_code = row
        
        # Vary Dates
        y = random.randint(2017, 2021)
        m = random.randint(1, 12)
        d = random.randint(1, 28)
        
        # DateCompletion format: DDMMYYYY
        d_comp = f"{d:02d}{m:02d}{y}"
        
        # creationtime format: YYYY-M-D H:MM:SS
        h = random.randint(8, 17)
        mi = random.randint(1, 59)
        s = random.randint(1, 59)
        creationtime = f"{y}-{m}-{d} {h}:{mi}:{s}"
        
        # Vary Names / Details
        if inv_type == "Check Dam":
            name = random.choice([
                "Cement Nala Bund",
                "Check Dam Construction",
                "Earthen Gully Plug",
                "Mati Nala Bund",
                "Gabion Structure"
            ])
            profilename = "CheckDamConstruction"
        else:
            name = random.choice([
                "Farm Pond (Plastic Lined)",
                "Continuous Contour Trench",
                "Water Absorption Trench",
                "Deepening of Nala"
            ])
            profilename = "WaterHarvesting"
            
        details = f"{name} executed under watershed scheme by Taluka Agri Dept"
        
        # Vary UUID and SL
        sl_no = random.randint(10000, 99999)
        rec_uuid = str(uuid.uuid4())
        deviceid = f"DEV-{random.randint(1000,9999)}"
        
        updates.append((
            sl_no, creationtime, rec_uuid, deviceid, name, profilename, d_comp, details, inv_id
        ))
        
    cursor.executemany("""
        UPDATE interventions SET
            drishti_sl_no = ?,
            drishti_creationtime = ?,
            drishti_uuid = ?,
            drishti_deviceid = ?,
            drishti_name = ?,
            drishti_profilename = ?,
            drishti_datecompletion = ?,
            drishti_details = ?
        WHERE id = ?
    """, updates)
    
    conn.commit()
    conn.close()
    print("Varied DRISHTI metadata for all demo interventions.")

if __name__ == "__main__":
    vary_drishti_metadata()
