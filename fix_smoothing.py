import os

content = """import React, { useEffect, useState, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, GeoJSON } from 'react-leaflet';
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

const MapController = ({ interventions, selectedId, bounds }) => {
  const map = useMap();
  useEffect(() => {
    map.invalidateSize();
    if (selectedId) {
      const inv = interventions.find(i => i.id === selectedId);
      if (inv && inv.lat && inv.lng) {
        map.flyTo([inv.lat, inv.lng], 16, { animate: true });
      }
    } else if (bounds) {
      map.fitBounds(bounds, { padding: [20, 20] });
    }
  }, [selectedId, interventions, map, bounds]);
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
      const div = L.DomUtil.create('div', 'bg-white/90 backdrop-blur p-4 border border-slate-200 rounded-xl shadow-lg z-[1000] text-xs font-sans');
      div.innerHTML = `
        <div class="font-extrabold text-slate-800 uppercase mb-2 tracking-widest border-b border-slate-200 pb-2">Analysis Index</div>
        <div class="flex flex-col gap-2">
          <div class="flex items-center gap-3"><div class="w-4 h-4 rounded-sm border border-slate-400" style="background:#8B0000"></div><span class="font-bold text-slate-700">Severe Degradation</span></div>
          <div class="flex items-center gap-3"><div class="w-4 h-4 rounded-sm border border-slate-400" style="background:#E07B39"></div><span class="font-bold text-slate-700">Moderate Degradation</span></div>
          <div class="flex items-center gap-3"><div class="w-4 h-4 rounded-sm border border-slate-400" style="background:#C7C7C7"></div><span class="font-bold text-slate-700">Stable</span></div>
          <div class="flex items-center gap-3"><div class="w-4 h-4 rounded-sm border border-slate-400" style="background:#90C978"></div><span class="font-bold text-slate-700">Improving</span></div>
          <div class="flex items-center gap-3"><div class="w-4 h-4 rounded-sm border border-slate-400" style="background:#1B5E20"></div><span class="font-bold text-slate-700">Strong Improvement</span></div>
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

// Add a custom style rule to globally smooth GeoJSONs with a specific className
const InjectSmoothingCSS = () => {
  useEffect(() => {
    const style = document.createElement('style');
    style.innerHTML = `
      .smooth-grid-pane svg path {
        stroke: none !important;
        stroke-width: 0 !important;
      }
      .smooth-grid-pane svg {
        filter: blur(8px) saturate(1.2);
        opacity: 0.75;
      }
    `;
    document.head.appendChild(style);
    return () => document.head.removeChild(style);
  }, []);
  return null;
};

export default function MapViewer({ interventions, selectedId, onSelect, baseMap, activeLayers, demoMode, selectedYear, compareYear, swipeMode, setClickedCell }) {
  const [watershedData, setWatershedData] = useState(null);
  const [gridData, setGridData] = useState(null);
  const [streamData, setStreamData] = useState(null);
  
  const mapRef = useRef(null);
  const layerRightRef = useRef(null);
  const layerLeftRef = useRef(null);
  const sideBySideRef = useRef(null);

  useEffect(() => {
    // Load the real geographic static outputs generated offline
    axios.get('/watershed_real.geojson').then(res => setWatershedData(res.data)).catch(()=>{});
    axios.get('/real_streams.geojson').then(res => setStreamData(res.data)).catch(()=>{});
    // Load the generated T0-T4 demo grid
    axios.get('/change_grid.geojson').then(res => setGridData(res.data)).catch(()=>{});
  }, []);

  const getBaseUrl = () => {
    switch (baseMap) {
      case 'Terrain': return 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png';
      case 'Street': return 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
      case 'Satellite': default: return 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
    }
  };

  // Convert T0..T4 to 2021..2025 for looking up the generated backend data
  const mapYear = (tLabel) => tLabel.replace('T', '202');

  const styleCell = (feature, tLabel) => {
    const yearStr = mapYear(tLabel);
    const data = feature.properties.years[yearStr];
    let color = data ? getColor(data.changeClass) : 'transparent';
    return {
      fillColor: color,
      weight: 0,
      opacity: 0, 
      fillOpacity: 1 // Full opacity to feed into the SVG blur filter correctly
    };
  };

  const bounds = watershedData ? L.geoJSON(watershedData).getBounds() : [[18.80, 73.80], [18.90, 73.95]];
  const showChangeMaps = activeLayers.includes('Integrated Change Index (SCI)') || activeLayers.includes('Vegetation (SAVI)') || activeLayers.includes('Water Conservation (MNDWI)');

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

  // A wrapper for GeoJSON to support side-by-side split pane extraction
  const SwipeableGeoJSON = ({ data, tLabel, isLeft, onEachFeature }) => {
    const map = useMap();
    useEffect(() => {
      const paneName = isLeft ? 'leftPane' : 'rightPane';
      if (!map.getPane(paneName)) {
        map.createPane(paneName);
        map.getPane(paneName).style.zIndex = 400;
        map.getPane(paneName).classList.add('smooth-grid-pane');
      }
      const layer = L.geoJSON(data, { 
        style: (f) => styleCell(f, tLabel), 
        onEachFeature,
        pane: paneName
      });
      if (isLeft) layerLeftRef.current = layer;
      else layerRightRef.current = layer;
      layer.addTo(map);
      
      return () => {
        if (sideBySideRef.current) {
          sideBySideRef.current.remove();
          sideBySideRef.current = null;
        }
        map.removeLayer(layer);
        if (isLeft) layerLeftRef.current = null;
        else layerRightRef.current = null;
      };
    }, [map, data, tLabel, isLeft, onEachFeature]);
    return null;
  };

  // Custom pane for non-swiped smoothed grid
  const SmoothPaneCreator = () => {
    const map = useMap();
    useEffect(() => {
      if (!map.getPane('smoothPane')) {
        map.createPane('smoothPane');
        map.getPane('smoothPane').style.zIndex = 400;
        map.getPane('smoothPane').classList.add('smooth-grid-pane');
      }
    }, [map]);
    return null;
  };

  return (
    <div className="flex-1 w-full relative min-h-0 min-w-0">
      <InjectSmoothingCSS />
      
      {!demoMode && interventions.every(i => !i.lat) && (
        <div className="absolute inset-0 z-[2000] flex flex-col items-center justify-center bg-slate-900/80 backdrop-blur-sm text-white p-6 text-center">
          <div className="text-3xl font-black mb-4 tracking-tight">Spatial Data Unavailable</div>
          <div className="text-slate-300 text-sm max-w-lg leading-relaxed bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-2xl">
            Official spatial coordinates for PUNE-WDC-1 interventions are pending ingestion from the state node. 
            <br/><br/>
            Toggle <strong>DEMO MODE</strong> in the top header to initialize prototype coordinates and analytical metrics.
          </div>
        </div>
      )}

      <MapContainer center={[18.85, 73.85]} zoom={13} style={{ height: '100%', width: '100%', background: '#e2e8f0' }} zoomControl={false} ref={mapRef}>
        <TileLayer url={getBaseUrl()} />
        <MapController interventions={interventions} selectedId={selectedId} bounds={bounds} />
        <SmoothPaneCreator />

        {activeLayers.includes('Project Boundary') && watershedData && (
          <GeoJSON 
            data={watershedData} 
            style={{ color: '#0f172a', weight: 4, fillOpacity: 0, opacity: 0.8 }} 
          />
        )}
        
        {activeLayers.includes('Hydrology') && streamData && (
          <GeoJSON 
            data={streamData} 
            style={{ color: '#3b82f6', weight: 2, opacity: 0.9 }} 
          />
        )}

        {showChangeMaps && gridData && (
          <>
            {swipeMode ? (
              <>
                <SwipeableGeoJSON 
                  isLeft={true} data={gridData} tLabel={selectedYear} 
                  onEachFeature={(f, l) => l.on('click', () => setClickedCell(f))}
                />
                <SwipeableGeoJSON 
                  isLeft={false} data={gridData} tLabel={compareYear} 
                  onEachFeature={(f, l) => l.on('click', () => setClickedCell(f))}
                />
              </>
            ) : (
              <GeoJSON 
                key={`grid-${selectedYear}`}
                data={gridData} 
                pane="smoothPane"
                style={(f) => styleCell(f, selectedYear)}
                onEachFeature={(f, l) => {
                  l.on('click', () => setClickedCell(f));
                }}
              />
            )}
            <LegendControl />
          </>
        )}

        {activeLayers.includes('Interventions (Check Dams)') && interventions.filter(i => i.lat && i.lng).map(inv => (
          <Marker 
            key={inv.id} 
            position={[inv.lat, inv.lng]}
            eventHandlers={{ click: () => onSelect(inv.id) }}
          >
            <Popup className="text-sm font-sans rounded-xl p-0 overflow-hidden border-0 shadow-lg">
              <div className="bg-slate-50 border-b border-slate-200 px-3 py-2 font-black text-slate-800 uppercase tracking-widest text-xs">Check Dam</div>
              <div className="p-3">
                <div className="text-slate-600 font-medium mb-1">{inv.work_code}</div>
                <button className="bg-teal-600 hover:bg-teal-500 text-white font-bold w-full mt-2 py-1.5 rounded transition-colors" onClick={() => onSelect(inv.id)}>Inspect Evidence</button>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
      
      {/* Map Tools Overlay */}
      <div className="absolute top-4 right-4 z-[1000] flex flex-col gap-2">
        <button className="w-10 h-10 bg-white border border-slate-200 text-slate-700 rounded-xl shadow-md flex items-center justify-center hover:bg-slate-50 font-black text-lg transition-colors">+</button>
        <button className="w-10 h-10 bg-white border border-slate-200 text-slate-700 rounded-xl shadow-md flex items-center justify-center hover:bg-slate-50 font-black text-lg transition-colors">-</button>
      </div>
    </div>
  );
}
"""

os.makedirs(os.path.join(os.path.dirname(__file__), "frontend", "src", "components"), exist_ok=True)
with open(os.path.join(os.path.dirname(__file__), "frontend", "src", "components", "MapViewer.tsx"), "w", encoding="utf-8") as f:
    f.write(content)
