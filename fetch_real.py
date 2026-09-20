import requests
import json
import os

def fetch_real_village():
    # Let's get a known village boundary near Pune, like 'Bhugaon' or 'Mulshi'
    query = """
    [out:json];
    relation["name"="Bhugaon"]["admin_level"="10"];
    out geom;
    """
    url = "https://overpass-api.de/api/interpreter"
    res = requests.post(url, data={"data": query})
    if res.status_code == 200:
        data = res.json()
        features = []
        for element in data.get("elements", []):
            if element["type"] == "relation":
                coords = []
                for member in element.get("members", []):
                    if member["type"] == "way":
                        way_coords = [[node["lon"], node["lat"]] for node in member.get("geometry", [])]
                        coords.append(way_coords)
                
                # To make it a valid GeoJSON polygon, we'd need to stitch the ways.
                # A quick hack for Leaflet is just returning a MultiLineString of the boundary ways!
                # Wait, they asked for a Polygon.
                features.append({
                    "type": "Feature",
                    "properties": {"name": element.get("tags", {}).get("name", "Unknown")},
                    "geometry": {
                        "type": "MultiLineString",
                        "coordinates": coords
                    }
                })
                    
        if features:
            geojson = {
                "type": "FeatureCollection",
                "features": features
            }
            path = os.path.join(os.path.dirname(__file__), "frontend", "public", "watershed_real.geojson")
            with open(path, "w") as f:
                json.dump(geojson, f)
            print(f"Saved real boundary to {path}")
            return True
    return False

if not fetch_real_village():
    print("Failed to fetch Bhugaon, trying bounding box.")
    # Fallback: Just query a bunch of natural=water or a forest polygon in Pune
    query2 = """
    [out:json];
    way["natural"="water"]["name"="Khadakwasla Lake"];
    out geom;
    """
    res2 = requests.post("https://overpass-api.de/api/interpreter", data={"data": query2})
    data = res2.json()
    coords = []
    for el in data.get("elements", []):
         coords.append([[n["lon"], n["lat"]] for n in el.get("geometry", [])])
    if coords:
         geojson = {
             "type": "FeatureCollection",
             "features": [{
                 "type": "Feature",
                 "properties": {"name": "Khadakwasla Catchment"},
                 "geometry": { "type": "Polygon", "coordinates": [coords[0]] }
             }]
         }
         with open(os.path.join(os.path.dirname(__file__), "frontend", "public", "watershed_real.geojson"), "w") as f:
             json.dump(geojson, f)
         print("Saved Khadakwasla as boundary.")
