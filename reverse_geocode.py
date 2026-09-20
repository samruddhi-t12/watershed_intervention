import sqlite3
import requests
import time

def update_locations():
    conn = sqlite3.connect("data/sqlite/demo_db.sqlite")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, lat, lng FROM interventions WHERE lat IS NOT NULL")
    rows = cursor.fetchall()
    
    headers = {
        'User-Agent': 'SIH26WaterMVP/1.0 (Demo Application)'
    }
    
    updates = []
    
    print(f"Reverse geocoding {len(rows)} locations...")
    
    for row in rows:
        inv_id, lat, lng = row
        
        try:
            url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}&zoom=14&addressdetails=1"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                address = data.get('address', {})
                
                # Extract best locality name
                village = address.get('village') or address.get('town') or address.get('hamlet') or address.get('suburb') or address.get('county') or "Unknown Village"
                taluka = address.get('county', 'Khed')
                district = address.get('state_district', 'Pune')
                
                # Format to match DRISHTI style
                location_str = f"{village}, Tal. {taluka.replace(' Sub-District', '')}, Dist. {district.replace(' District', '')}"
                
                print(f"ID {inv_id} -> {location_str}")
                updates.append((location_str, inv_id))
            else:
                print(f"Failed for ID {inv_id}: HTTP {response.status_code}")
                
            time.sleep(1.5) # Respect Nominatim rate limits (1 req/sec)
            
        except Exception as e:
            print(f"Error on ID {inv_id}: {e}")
            
    if updates:
        cursor.executemany("UPDATE interventions SET drishti_location = ? WHERE id = ?", updates)
        conn.commit()
        print("Successfully updated database locations.")
    
    conn.close()

if __name__ == "__main__":
    update_locations()
