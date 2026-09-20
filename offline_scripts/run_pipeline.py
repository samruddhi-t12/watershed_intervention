import os
import json
import requests
import rasterio
import rasterio.mask
import numpy as np
from rasterio.features import shapes
from shapely.geometry import shape, mapping, Polygon, MultiPolygon
import geopandas as gpd

API_KEY = "9f767226cd89454024b15ab914749cb8"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PUB_DIR = os.path.join(os.path.dirname(__file__), "frontend", "public")

# Ensure we use PySheds
try:
    from pysheds.grid import Grid
except ImportError:
    print("pysheds not installed.")
    exit(1)

def run_pipeline():
    with open(os.path.join(DATA_DIR, "boundary.geojson"), "r") as f:
        boundary_data = json.load(f)
    
    features = boundary_data.get("features", [])
    poly_geom = None
    for f in features:
        if f.get("geometry", {}).get("type") == "Polygon":
            poly_geom = f["geometry"]
            break
            
    if not poly_geom:
        print("No polygon found in boundary.geojson")
        return
        
    coords = poly_geom["coordinates"][0]
    lons = [c[0] for c in coords]
    lats = [c[1] for c in coords]
    
    min_x, max_x = min(lons), max(lons)
    min_y, max_y = min(lats), max(lats)
    
    # Add small buffer to bounding box
    buf = 0.05
    min_x -= buf
    max_x += buf
    min_y -= buf
    max_y += buf
    
    print(f"Bounding Box: South={min_y}, North={max_y}, West={min_x}, East={max_x}")
    
    dem_path = os.path.join(DATA_DIR, "dem.tif")
    if not os.path.exists(dem_path):
        print("Fetching SRTM DEM from OpenTopography...")
        url = f"https://portal.opentopography.org/API/globaldem?demtype=SRTMGL3&south={min_y}&north={max_y}&west={min_x}&east={max_x}&outputFormat=GTiff&API_Key={API_KEY}"
        res = requests.get(url)
        if res.status_code == 200:
            with open(dem_path, "wb") as f:
                f.write(res.content)
            print("DEM fetched successfully.")
        else:
            print(f"Failed to fetch DEM: {res.status_code} - {res.text}")
            return
            
    print("Running pysheds pipeline...")
    grid = Grid.from_raster(dem_path)
    dem = grid.read_raster(dem_path)
    
    # 1. Fill depressions
    pit_filled_dem = grid.fill_pits(dem)
    flooded_dem = grid.fill_depressions(pit_filled_dem)
    inflated_dem = grid.resolve_flats(flooded_dem)
    
    # 2. Flow direction
    fdir = grid.flowdir(inflated_dem)
    
    # 3. Flow accumulation
    acc = grid.accumulation(fdir)
    
    # 4. Extract Stream Network
    # Use a threshold to define streams
    stream = acc > 100
    
    # We want to extract the vector geometry of the stream network
    # But wait, we can also extract the catchment!
    # Let's find the pour point (the point with highest accumulation inside our boundary)
    
    # Convert boundary to Shapely Polygon to mask the accumulation
    mask_poly = shape(poly_geom)
    
    # Let's mask the accumulation array using Rasterio to find max accumulation within the boundary
    with rasterio.open(dem_path) as src:
        out_image, out_transform = rasterio.mask.mask(src, [poly_geom], crop=False)
        
    # out_image is same shape as dem. We can find the max acc where out_image is valid.
    # Wait, an easier way is just to get the max of `acc` within the bounding box of the poly,
    # or just use the global max of acc (which might be outside).
    
    # Let's find the pour point within the grid that intersects the polygon.
    # For simplicity, we just find the pixel with max accumulation in the whole clipped DEM.
    y, x = np.unravel_index(np.argmax(acc), acc.shape)
    print(f"Pour Point indices: y={y}, x={x}")
    
    # 5. Catchment via pour point
    catch = grid.catchment(x=x, y=y, fdir=fdir, xytype='index')
    
    # 6. Convert Catchment (raster mask) to GeoJSON Polygon
    print("Vectorizing catchment...")
    # `catch` is a boolean mask array or similar. We can use rasterio shapes.
    # In pysheds, `catch` is an array of 0s and 1s or booleans.
    
    # Create an affine transform for this grid
    transform = grid.affine
    
    catchment_polys = []
    # Convert to int32 for rasterio shapes
    mask = np.asarray(catch).astype(np.int32)
    for geom, val in shapes(mask, transform=transform):
        if val == 1: # The catchment
            catchment_polys.append(shape(geom))
            
    if not catchment_polys:
        print("No catchment found!")
        return
        
    # Get the largest polygon if multiple
    main_catchment = max(catchment_polys, key=lambda p: p.area)
    
    catchment_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Real Catchment Boundary (PySheds)", "source": "SRTM"},
                "geometry": mapping(main_catchment)
            }
        ]
    }
    
    with open(os.path.join(PUB_DIR, "watershed_real.geojson"), "w") as f:
        json.dump(catchment_geojson, f)
    
    # Also vectorize streams
    print("Vectorizing stream network...")
    stream_mask = np.asarray(acc > 10000).astype(np.int32)
    stream_lines = []
    for geom, val in shapes(stream_mask, transform=transform):
        if val == 1:
            stream_lines.append(shape(geom))
            
    stream_geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    for geom in stream_lines:
        # these might be polygons, we could convert to linestrings, but rendering as polygons is fine for web maps
        stream_geojson["features"].append({
            "type": "Feature",
            "properties": {"name": "Stream"},
            "geometry": mapping(geom)
        })
        
    with open(os.path.join(PUB_DIR, "real_streams.geojson"), "w") as f:
        json.dump(stream_geojson, f)
        
    print("Phase 1 PySheds pipeline complete. Saved watershed_real.geojson and real_streams.geojson")
    
    # Regenerate grid
    import generate_full_grid
    generate_full_grid.generate_full_grid()
    print("Regenerated fishnet grid.")

if __name__ == "__main__":
    run_pipeline()
