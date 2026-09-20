import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
import json

with rasterio.open('data/dem.tif') as src:
    dem = src.read(1).astype(np.float32)
    bounds = src.bounds
    
    ls = LightSource(azdeg=315, altdeg=45)
    
    nodata = src.nodata
    if nodata is not None:
        mask = dem == nodata
        dem[mask] = np.nan
    else:
        mask = np.isnan(dem)
        
    hs = ls.hillshade(dem, vert_exag=10000)
    
    img = np.zeros((hs.shape[0], hs.shape[1], 4), dtype=np.uint8)
    img[..., 0] = hs * 255
    img[..., 1] = hs * 255
    img[..., 2] = hs * 255
    img[..., 3] = np.where(mask, 0, 150) # Alpha channel with slight opacity natively
    
    from PIL import Image
    im = Image.fromarray(img)
    im.save('frontend/public/hillshade.png')
    
    leaflet_bounds = [[bounds.bottom, bounds.left], [bounds.top, bounds.right]]
    print("Leaflet Bounds:", leaflet_bounds)
