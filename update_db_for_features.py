import sqlite3
import random

def run():
    conn = sqlite3.connect("data/sqlite/demo_db.sqlite")
    c = conn.cursor()
    
    # 1. Add new columns if they don't exist
    try: c.execute("ALTER TABLE interventions ADD COLUMN ref_ndvi_change FLOAT")
    except: pass
    try: c.execute("ALTER TABLE interventions ADD COLUMN ref_mndwi_change FLOAT")
    except: pass
    try: c.execute("ALTER TABLE interventions ADD COLUMN rainfall_context VARCHAR")
    except: pass
    try: c.execute("ALTER TABLE interventions ADD COLUMN cv_signal_text VARCHAR")
    except: pass
    
    # 2. Update rows
    c.execute("SELECT id, score_impact, ndvi_change, mndwi_change FROM interventions WHERE lat IS NOT NULL")
    rows = c.fetchall()
    
    updates = []
    for row in rows:
        inv_id, score_impact, ndvi, mndwi = row
        score_impact = score_impact or 0.6
        
        # Split score_impact into 5 parts
        parts = [random.random() for _ in range(5)]
        s = sum(parts)
        parts = [p / s * score_impact for p in parts]
        i_veg, i_wat, i_lulc, i_temp, i_fld = [round(x, 2) for x in parts]
        i_veg = round(score_impact - (i_wat + i_lulc + i_temp + i_fld), 2)
        
        # Ref zones (slightly lower than intervention)
        ref_ndvi = round(ndvi - random.uniform(0.05, 0.15) if ndvi else 0, 2)
        ref_mndwi = round(mndwi - random.uniform(0.05, 0.15) if mndwi else 0, 2)
        
        # Rainfall context
        rain = random.choice(["Rainfall: +15% Above average (Monsoon)", "Rainfall: -5% Below average (Deficit)", "Rainfall: Typical seasonal baseline"])
        
        # CV Signal
        cv_sig = f"Automated visual signal: {random.randint(25, 60)}% Greenness, {random.randint(5, 30)}% Water detected"
        
        updates.append((i_veg, i_wat, i_lulc, i_temp, i_fld, ref_ndvi, ref_mndwi, rain, cv_sig, inv_id))
        
    c.executemany("""
        UPDATE interventions SET 
            impact_veg=?, impact_water=?, impact_lulc=?, impact_temporal=?, impact_field=?,
            ref_ndvi_change=?, ref_mndwi_change=?, rainfall_context=?, cv_signal_text=?
        WHERE id=?
    """, updates)
    
    conn.commit()
    conn.close()
    print("DB updated successfully")

if __name__ == "__main__":
    run()
