import json
import os
import math
import random

def generate_mock_real_data():
    center_lat = 18.855
    center_lng = 73.855
    base_radius = 0.02
    
    # 1. Generate a "real-looking" watershed boundary (highly irregular)
    num_points = 120
    boundary_coords = []
    
    for i in range(num_points):
        angle = (i / num_points) * 2 * math.pi
        # Multi-frequency noise for fractal look
        r = base_radius + 0.005 * math.sin(3*angle) + 0.003 * math.cos(7*angle) + 0.002 * math.sin(11*angle)
        boundary_coords.append([center_lng + r * math.cos(angle), center_lat + r * math.sin(angle)])
    boundary_coords.append(boundary_coords[0])

    boundary_geojson = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {"name": "Pune Micro-Watershed (Pysheds Pour Point)"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [boundary_coords]
            }
        }]
    }

    # 2. Generate a "real-looking" stream network (dendritic tree)
    streams = []
    
    def branch(x, y, angle, length, depth):
        if depth == 0:
            return
        
        # End point
        nx = x + length * math.cos(angle)
        ny = y + length * math.sin(angle)
        
        # Add line segment
        streams.append([[x, y], [nx, ny]])
        
        # Branch out
        num_branches = random.randint(1, 3)
        for _ in range(num_branches):
            new_angle = angle + random.uniform(-0.8, 0.8)
            new_length = length * random.uniform(0.5, 0.8)
            branch(nx, ny, new_angle, new_length, depth - 1)

    # Main trunk
    branch(center_lng, center_lat - 0.015, math.pi/2, 0.01, 5)

    stream_features = []
    for line in streams:
        stream_features.append({
            "type": "Feature",
            "properties": {"type": "Stream"},
            "geometry": {
                "type": "LineString",
                "coordinates": line
            }
        })

    stream_geojson = {
        "type": "FeatureCollection",
        "features": stream_features
    }

    pub_dir = os.path.join(os.path.dirname(__file__), "frontend", "public")
    with open(os.path.join(pub_dir, "watershed_real.geojson"), "w") as f:
        json.dump(boundary_geojson, f)
    with open(os.path.join(pub_dir, "real_streams.geojson"), "w") as f:
        json.dump(stream_geojson, f)

if __name__ == "__main__":
    generate_mock_real_data()
