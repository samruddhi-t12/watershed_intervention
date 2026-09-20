import os

content = """import React, { useEffect, useState, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, GeoJSON, ImageOverlay } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import axios from 'axios';
import 'leaflet-side-by-side';

import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25,41],
    iconAnchor: [12,41]
});
L.Marker.prototype.options.icon = DefaultIcon;

const MapController = ({ interventions, selectedId, bounds, activeTab }) => {
  const map = useMap();
  useEffect(() => {
    map.invalidateSize();
    if (selectedId && activeTab === 'Interventions') {
      const inv = interventions.find(i => i.id === selectedId);
      if (inv && inv.lat && inv.lng) {
        map.flyTo([inv.lat, inv.lng], 16, { animate: true });
      }
    } else if (bounds) {
      map.fitBounds(bounds, { padding: [20, 20] });
    }
  }, [selectedId, interventions, map, bounds, activeTab]);
  return null;
};

const getColor = (changeClass) => {
  switch (changeClass) {
    case 'severe_degradation': return '#8B0000';
    case 'moderate_degradation': return '#E07B39';
    case 'stable': return '#C7C7C7';
    case 'improving': return '#90C978';
    case 'strong_improvement': return '#1B5E20';
    default: return '#000000';
  }
};

const LegendControl = () => {
  const map = useMap();
  useEffect(() => {
    const legend = L.control({ position: 'bottomright' });
    legend.onAdd = () => {
      const div = L.DomUtil.create('div', 'bg-white p-4 border border-gray-300 rounded-md shadow-md z-[1000] text-xs font-sans');
      div.innerHTML = `
        <div class="font-bold text-gray-800 uppercase mb-2 tracking-wide border-b border-gray-100 pb-1">Change Class</div>
        <div class="flex flex-col gap-1.5">
          <div class="flex items-center gap-2"><div class="w-4 h-4 rounded-sm border border-gray-400" style="background:#8B0000"></div><span>Severe Degradation</span></div>
          <div class="flex items-center gap-2"><div class="w-4 h-4 rounded-sm border border-gray-400" style="background:#E07B39"></div><span>Moderate Degradation</span></div>
          <div class="flex items-center gap-2"><div class="w-4 h-4 rounded-sm border border-gray-400" style="background:#C7C7C7"></div><span>Stable</span></div>
          <div class="flex items-center gap-2"><div class="w-4 h-4 rounded-sm border border-gray-400" style="background:#90C978"></div><span>Improving</span></div>
          <div class="flex items-center gap-2"><div class="w-4 h-4 rounded-sm border border-gray-400" style="background:#1B5E20"></div><span>Strong Improvement</span></div>
        </div>
      `;
      L.DomEvent.disableClickPropagation(div);
      return div;
    };
    legend.addTo(map);
    return () => { legend.remove(); };
  }, [map]);
  return null;
};

export default function MapViewer({ interventions, selectedId, onSelect, baseMap, activeLayers, demoMode, activeTab, selectedYear, compareYear, swipeMode, setClickedCell }) {
  const [watershedData, setWatershedData] = useState(null);
  const [gridData, setGridData] = useState(null);
  const [rasterErrors, setRasterErrors] = useState({});
  
  const mapRef = useRef(null);
  const layerRightRef = useRef(null);
  const layerLeftRef = useRef(null);
  const sideBySideRef = useRef(null);

  useEffect(() => {
    axios.get('/watershed.geojson').then(res => setWatershedData(res.data)).catch(()=>{});
    axios.get('/change_grid.geojson').then(res => setGridData(res.data)).catch(()=>{});
  }, []);

  const getBaseUrl = () => {
    switch (baseMap) {
      case 'Terrain': return 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png';
      case 'Street': return 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
      case 'Satellite': default: return 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
    }
  };

  const showChangeMaps = activeTab === 'Change Detection' && (
    activeLayers.includes('Integrated Change Index (SCI)') ||
    activeLayers.includes('Vegetation (SAVI)') ||
    activeLayers.includes('Water Conservation (MNDWI)') ||
    activeLayers.includes('Land Use / Degradation') ||
    activeLayers.includes('Drainage Change')
  );

  const getLayerSlug = (layerName) => {
    if (layerName.includes('Degradation')) return 'lulc';
    if (layerName.includes('Drainage')) return 'drainage';
    if (layerName.includes('SAVI')) return 'savi';
    if (layerName.includes('MNDWI')) return 'mndwi';
    return 'sci';
  };

  const activeChangeLayers = activeLayers.filter(l => getLayerSlug(l) !== 'sci' || l.includes('SCI'));

  const handleRasterError = (url) => {
    setRasterErrors(prev => ({ ...prev, [url]: true }));
  };

  const bounds = watershedData ? L.geoJSON(watershedData).getBounds() : [[18.80, 73.80], [18.90, 73.95]];

  useEffect(() => {
    if (mapRef.current && swipeMode && showChangeMaps) {
      const map = mapRef.current;
      if (!sideBySideRef.current && L.control.sideBySide) {
        if (layerLeftRef.current && layerRightRef.current) {
          sideBySideRef.current = L.control.sideBySide(layerLeftRef.current, layerRightRef.current);
          sideBySideRef.current.addTo(map);
        }
      }
    } else {
      if (sideBySideRef.current) {
        sideBySideRef.current.remove();
        sideBySideRef.current = null;
      }
    }
  }, [swipeMode, showChangeMaps]);

  // A wrapper for ImageOverlay to support side-by-side split
  const RasterWrapper = ({ url, bounds, isLeft }) => {
    const map = useMap();
    useEffect(() => {
      const imgLayer = L.imageOverlay(url, bounds, { opacity: 0.8 });
      if (isLeft) layerLeftRef.current = imgLayer;
      else layerRightRef.current = imgLayer;
      
      // We only add it to map via raw Leaflet if we're in swipe mode so side-by-side can grab it.
      imgLayer.addTo(map);
      
      return () => {
        if (sideBySideRef.current) {
          sideBySideRef.current.remove();
          sideBySideRef.current = null;
        }
        map.removeLayer(imgLayer);
        if (isLeft) layerLeftRef.current = null;
        else layerRightRef.current = null;
      };
    }, [map, url, bounds, isLeft]);
    return null;
  };

  return (
    <div className="flex-1 w-full relative min-h-0 min-w-0">
      {!demoMode && interventions.every(i => !i.lat) && activeTab === 'Interventions' && (
        <div className="absolute inset-0 z-[1000] flex flex-col items-center justify-center bg-gray-900/85 text-white p-6 text-center">
          <div className="text-2xl font-bold mb-3">Coordinates Unavailable</div>
          <div className="text-gray-300 text-sm max-w-md leading-relaxed bg-gray-800 p-4 rounded-md border border-gray-700">
            Official spatial coordinates for PUNE-WDC-1 interventions are pending validation. 
            <br/><br/>
            Toggle <strong>DEMO MODE</strong> in the top header to view the application with prototype demonstration coordinates and analytics.
          </div>
        </div>
      )}

      <MapContainer center={[18.85, 73.85]} zoom={13} style={{ height: '100%', width: '100%', background: '#e5e7eb' }} zoomControl={false} ref={mapRef}>
        <TileLayer url={getBaseUrl()} />
        <MapController interventions={interventions} selectedId={selectedId} bounds={bounds} activeTab={activeTab} />

        {activeLayers.includes('Project Boundary') && watershedData && (
          <GeoJSON 
            data={watershedData} 
            style={{ color: '#3b82f6', weight: 3, fillOpacity: 0 }} 
          />
        )}

        {showChangeMaps && gridData && (
          <>
            {/* Render true high-res rasters underneath */}
            {activeChangeLayers.map(l => {
              const slug = getLayerSlug(l);
              const urlLeft = `/rasters/${slug}_${selectedYear}.png`;
              const urlRight = `/rasters/${slug}_${compareYear}.png`;
              
              if (swipeMode) {
                return (
                  <React.Fragment key={slug}>
                    {!rasterErrors[urlLeft] && <RasterWrapper url={urlLeft} bounds={bounds} isLeft={true} />}
                    {!rasterErrors[urlRight] && <RasterWrapper url={urlRight} bounds={bounds} isLeft={false} />}
                  </React.Fragment>
                );
              } else {
                return !rasterErrors[urlLeft] ? (
                  <ImageOverlay 
                    key={urlLeft} 
                    url={urlLeft} 
                    bounds={bounds} 
                    opacity={0.8} 
                    errorOverlayUrl=""
                  />
                ) : null;
              }
            })}

            {/* Invisible Grid for Interactivity/Clicking */}
            <GeoJSON 
              key={`grid-interact-${selectedYear}`}
              data={gridData} 
              style={{
                fillColor: 'transparent',
                weight: 1,
                opacity: 0.1, // faint grid lines to guide the eye
                color: 'rgba(255,255,255,0.2)',
                fillOpacity: 0 // fully transparent fill to see rasters below
              }}
              onEachFeature={(f, l) => {
                l.on('click', () => setClickedCell(f));
              }}
            />
            
            <LegendControl />
          </>
        )}

        {activeLayers.includes('Check Dams') && interventions.filter(i => i.lat && i.lng).map(inv => (
          <Marker 
            key={inv.id} 
            position={[inv.lat, inv.lng]}
            eventHandlers={{ click: () => onSelect(inv.id) }}
          >
            <Popup className="text-sm font-sans">
              <strong className="text-gray-800">CHECK DAM</strong><br/>
              <span className="text-gray-600">Work Code: {inv.work_code}</span><br/>
              <span className="text-gray-600">Project: PUNE-WDC-1</span><br/>
              {activeTab === 'Interventions' && (
                <button className="text-blue-600 font-bold mt-2 hover:underline" onClick={() => onSelect(inv.id)}>Open Evidence</button>
              )}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
      
      {/* Map Tools Overlay */}
      <div className="absolute top-4 right-4 z-[1000] flex flex-col gap-2">
        <button className="w-8 h-8 bg-white border border-gray-300 text-gray-700 rounded-md shadow-sm flex items-center justify-center hover:bg-gray-50 font-bold">+</button>
        <button className="w-8 h-8 bg-white border border-gray-300 text-gray-700 rounded-md shadow-sm flex items-center justify-center hover:bg-gray-50 font-bold">-</button>
        <button className="w-8 h-8 bg-white border border-gray-300 text-gray-700 rounded-md shadow-sm flex items-center justify-center hover:bg-gray-50" title="Measure">📏</button>
        <button className="w-8 h-8 bg-white border border-gray-300 text-gray-700 rounded-md shadow-sm flex items-center justify-center hover:bg-gray-50" title="Fullscreen">⛶</button>
      </div>
    </div>
  );
}
"""

os.makedirs(os.path.join(os.path.dirname(__file__), "frontend", "src", "components"), exist_ok=True)
with open(os.path.join(os.path.dirname(__file__), "frontend", "src", "components", "MapViewer.tsx"), "w", encoding="utf-8") as f:
    f.write(content)
