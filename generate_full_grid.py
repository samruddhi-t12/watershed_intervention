import json
import os
import math
import random

def point_in_polygon(x, y, poly):
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n+1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def generate_full_grid():
    pub_dir = os.path.join(os.path.dirname(__file__), "frontend", "public")
    try:
        with open(os.path.join(pub_dir, "watershed_real.geojson")) as f:
            ws = json.load(f)
            # Find the largest polygon
            poly = ws["features"][0]["geometry"]["coordinates"][0]
            
        with open(os.path.join(pub_dir, "real_streams.geojson")) as f:
            streams = json.load(f)
            stream_lines = []
            from shapely.geometry import shape, Point
            for feature in streams.get("features", []):
                stream_lines.append(shape(feature["geometry"]))
    except Exception as e:
        print("Error loading geojson", e)
        return

    min_lng = min([p[0] for p in poly])
    max_lng = max([p[0] for p in poly])
    min_lat = min([p[1] for p in poly])
    max_lat = max([p[1] for p in poly])

    step = 0.01 # ~1km
    
    features = []
    cell_id = 0
    
    lng = min_lng
    while lng < max_lng:
        lat = min_lat
        while lat < max_lat:
            center_x = lng + step/2
            center_y = lat + step/2
            if point_in_polygon(center_x, center_y, poly):
                
                # compute distance to nearest stream
                pt = Point(center_x, center_y)
                min_stream_dist = 9999
                for line in stream_lines:
                    d = pt.distance(line)
                    if d < min_stream_dist:
                        min_stream_dist = d
                
                # Generate years data
                years = {}
                for y_idx in range(5):
                    year = f"202{y_idx+1}"
                    # Base value on distance from stream: closer = better improvement
                    # max expected distance in a dense network is ~0.1 degrees
                    normalized_dist = min(min_stream_dist / 0.05, 1.0)
                    
                    # Add temporal progression: values get better over the years
                    temporal_boost = y_idx * 0.15
                    
                    noise = random.uniform(-0.15, 0.15)
                    # val ranges from roughly -1 to 1
                    # Close to stream (dist ~ 0) -> 1 - 0 = 1 + boost
                    # Far from stream -> 1 - 1 = 0 + noise
                    val = (1.0 - normalized_dist * 1.5) + temporal_boost + noise
                    
                    if val > 0.6:
                        c_class = "strong_improvement"
                    elif val > 0.2:
                        c_class = "improving"
                    elif val > -0.2:
                        c_class = "stable"
                    elif val > -0.6:
                        c_class = "moderate_degradation"
                    else:
                        c_class = "severe_degradation"
                        
                    years[year] = {
                        "changeClass": c_class,
                        "deltaSAVI": val * 0.4,
                        "deltaMNDWI": val * 0.2,
                        "reasonText": f"Synthetic analytical output indicating {c_class.replace('_', ' ')} based on local variance."
                    }
                
                features.append({
                    "type": "Feature",
                    "properties": {
                        "cell_id": cell_id,
                        "years": years
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[lng, lat], [lng+step, lat], [lng+step, lat+step], [lng, lat+step], [lng, lat]]]
                    }
                })
                cell_id += 1
            lat += step
        lng += step
        
    grid_geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    with open(os.path.join(pub_dir, "change_grid.geojson"), "w") as f:
        json.dump(grid_geojson, f)

if __name__ == "__main__":
    generate_full_grid()
