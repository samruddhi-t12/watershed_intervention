import sqlite3
import random

def run():
    conn = sqlite3.connect("data/sqlite/demo_db.sqlite")
    c = conn.cursor()
    
    try: c.execute("ALTER TABLE interventions ADD COLUMN cost_estimated INTEGER")
    except: pass
    
    c.execute("SELECT id, type FROM interventions WHERE data_status = 'DEMO'")
    rows = c.fetchall()
    
    updates = []
    for row in rows:
        inv_id, inv_type = row
        
        # Estimate base costs per type
        if "Check Dam" in inv_type or "Cement" in inv_type:
            cost = random.randint(300, 800) * 1000 # 3L to 8L
        elif "Earthen" in inv_type or "Mati" in inv_type:
            cost = random.randint(50, 150) * 1000 # 50k to 1.5L
        elif "Pond" in inv_type:
            cost = random.randint(100, 250) * 1000 # 1L to 2.5L
        else:
            cost = random.randint(80, 200) * 1000
            
        updates.append((cost, inv_id))
        
    c.executemany("UPDATE interventions SET cost_estimated = ? WHERE id = ?", updates)
    conn.commit()
    conn.close()
    print("Populated cost_estimated.")

if __name__ == "__main__":
    run()
