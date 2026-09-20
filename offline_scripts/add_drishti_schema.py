import sqlite3
import uuid
import random
from datetime import datetime

def add_drishti_fields():
    conn = sqlite3.connect("data/sqlite/demo_db.sqlite")
    cursor = conn.cursor()
    
    fields = [
        ("drishti_sl_no", "INTEGER"),
        ("drishti_server_time", "VARCHAR"),
        ("drishti_apptype", "VARCHAR"),
        ("drishti_appsubtype", "VARCHAR"),
        ("drishti_fdcprojectname", "VARCHAR"),
        ("drishti_themename", "VARCHAR"),
        ("drishti_profilename", "VARCHAR"),
        ("drishti_observername", "VARCHAR"),
        ("drishti_org", "VARCHAR"),
        ("drishti_mobileno", "VARCHAR"),
        ("drishti_creationtime", "VARCHAR"),
        ("drishti_uuid", "VARCHAR"),
        ("drishti_deviceid", "VARCHAR"),
        ("drishti_name", "VARCHAR"),
        ("drishti_statusofactivity", "VARCHAR"),
        ("drishti_location", "VARCHAR"),
        ("drishti_datecompletion", "VARCHAR"),
        ("drishti_details", "VARCHAR")
    ]
    
    # Try adding columns
    for col, dtype in fields:
        try:
            cursor.execute(f"ALTER TABLE interventions ADD COLUMN {col} {dtype}")
        except sqlite3.OperationalError:
            pass # Column exists
            
    cursor.execute("SELECT id, type, work_code, status_badge FROM interventions")
    rows = cursor.fetchall()
    
    updates = []
    
    for row in rows:
        inv_id, inv_type, work_code, badge = row
        
        sl_no = random.randint(10000, 99999)
        server_time = "2022-11-04 14:32:11.405"
        apptype = "fdc"
        appsubtype = "fdc"
        fdcprojectname = "WDCPMKSY"
        themename = "WDCPMKSYFDC"
        
        profilename = "CheckDamConstruction" if inv_type == "Check Dam" else "FarmPond"
        observername = "Rajesh Patil (Demo)"
        org = "Taluka Agriculture Office"
        mobileno = ""
        
        # Non-zero padded date
        y = random.randint(2017, 2021)
        m = random.randint(1, 12)
        d = random.randint(1, 28)
        h = random.randint(8, 17)
        mi = random.randint(1, 59)
        s = random.randint(1, 59)
        creationtime = f"{y}-{m}-{d} {h}:{mi}:{s}"
        
        rec_uuid = str(uuid.uuid4())
        deviceid = f"DEV-{random.randint(1000,9999)}"
        name = "Check Dam Construction" if inv_type == "Check Dam" else "Water Structure"
        
        status_act = "In Progress" if badge in ["REVIEW", "FLAGGED"] else "Completed"
        
        location = "Chinchbaiwadi, Tal. Khed, Dist. Pune"
        
        # DDMMYYYY
        d_comp = f"{d:02d}{m:02d}{y}"
        details = f"{name} executed under watershed scheme"
        
        updates.append((
            sl_no, server_time, apptype, appsubtype, fdcprojectname, themename,
            profilename, observername, org, mobileno, creationtime, rec_uuid,
            deviceid, name, status_act, location, d_comp, details,
            inv_id
        ))
        
    cursor.executemany("""
        UPDATE interventions SET
            drishti_sl_no = ?,
            drishti_server_time = ?,
            drishti_apptype = ?,
            drishti_appsubtype = ?,
            drishti_fdcprojectname = ?,
            drishti_themename = ?,
            drishti_profilename = ?,
            drishti_observername = ?,
            drishti_org = ?,
            drishti_mobileno = ?,
            drishti_creationtime = ?,
            drishti_uuid = ?,
            drishti_deviceid = ?,
            drishti_name = ?,
            drishti_statusofactivity = ?,
            drishti_location = ?,
            drishti_datecompletion = ?,
            drishti_details = ?
        WHERE id = ?
    """, updates)
    
    conn.commit()
    conn.close()
    print("Added DRISHTI schema fields.")

if __name__ == "__main__":
    add_drishti_fields()
