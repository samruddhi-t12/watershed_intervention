import requests
import json
import os

def fetch_boundary():
    # Overpass query for Chinchbaiwadi or Khed
    query = """
    [out:json];
    relation["name"~"Chinchbaiwadi|Khed",i]["admin_level"];
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
                        way_coords = []
                        for node in member.get("geometry", []):
                            way_coords.append([node["lon"], node["lat"]])
                        if way_coords:
                            coords.append(way_coords)
                
                if coords:
                    # Simplify by just taking the first way or merging them
                    # A proper relation to polygon needs merging. For this prototype, let's take a convex hull or just the first way if it's long.
                    # Or we just use a bounding box approach.
                    features.append({
                        "type": "Feature",
                        "properties": {"name": element.get("tags", {}).get("name", "Unknown")},
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [coords[0]] # Simplification
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
        else:
            print("No features found.")
    else:
        print("Failed to fetch from Overpass API")

if __name__ == "__main__":
    fetch_boundary()
