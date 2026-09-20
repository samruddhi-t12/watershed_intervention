import sqlite3
import json
import os

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

conn = sqlite3.connect('data/sqlite/demo_db.sqlite')
conn.row_factory = dict_factory
cursor = conn.cursor()

cursor.execute("SELECT * FROM interventions")
rows = cursor.fetchall()

os.makedirs('frontend/public/data', exist_ok=True)

with open('frontend/public/data/interventions.json', 'w') as f:
    json.dump(rows, f, indent=2)

print("Dumped", len(rows), "records to frontend/public/data/interventions.json")
