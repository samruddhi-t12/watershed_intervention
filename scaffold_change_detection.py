import os

frontend_files = {
    "frontend/src/App.tsx": """import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MapViewer from './components/MapViewer';
import LeftSidebar from './components/LeftSidebar';
import RightPanel from './components/RightPanel';
import TopNav from './components/TopNav';
import AnalyticsDashboard from './components/AnalyticsDashboard';

export default function App() {
  const [interventions, setInterventions] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [selectedId, setSelectedId] = useState(null);
  const [demoMode, setDemoMode] = useState(false);
  const [activeLayers, setActiveLayers] = useState(['Check Dams', 'Project Boundary']);
  const [baseMap, setBaseMap] = useState('Satellite');
  const [activeTab, setActiveTab] = useState('Interventions');
  const [selectedYear, setSelectedYear] = useState('2025');
  const [compareYear, setCompareYear] = useState('2021');
  const [swipeMode, setSwipeMode] = useState(false);
  const [clickedCell, setClickedCell] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/v1/interventions');
      setInterventions(res.data);
      const mRes = await axios.get('http://127.0.0.1:8000/api/v1/dashboard/metrics');
      setMetrics(mRes.data);
    } catch (e) {
      console.error(e);
    }
  };

  const selectedInv = interventions.find(i => i.id === selectedId);

  return (
    <div className="h-screen w-full flex flex-col bg-gray-50 text-gray-800 font-sans overflow-hidden">
      <TopNav metrics={metrics} demoMode={demoMode} setDemoMode={setDemoMode} activeTab={activeTab} setActiveTab={setActiveTab} />
      
      {activeTab === 'Change Detection' && (
        <div className="bg-white border-b border-gray-300 p-2 flex items-center justify-between px-6 shadow-sm z-40 relative">
          <div className="flex items-center gap-4 flex-1">
            <span className="text-sm font-bold text-gray-700 uppercase">Analysis Year: {selectedYear}</span>
            <input 
              type="range" min="2021" max="2025" step="1" 
              value={selectedYear} onChange={(e) => setSelectedYear(e.target.value)} 
              className="w-64 accent-blue-600"
            />
          </div>
          <div className="flex items-center gap-4">
            <label className="flex items-center gap-2 text-sm font-bold text-gray-700 cursor-pointer">
              <input type="checkbox" checked={swipeMode} onChange={(e) => setSwipeMode(e.target.checked)} className="w-4 h-4 text-blue-600 rounded border-gray-300" />
              SWIPE COMPARE MODE
            </label>
            {swipeMode && (
              <div className="flex items-center gap-2 border-l border-gray-300 pl-4">
                <span className="text-sm font-bold text-gray-500 uppercase">Compare With:</span>
                <select value={compareYear} onChange={(e) => setCompareYear(e.target.value)} className="bg-gray-100 border border-gray-300 rounded px-2 py-1 text-sm outline-none">
                  <option value="2021">2021</option>
                  <option value="2022">2022</option>
                  <option value="2023">2023</option>
                  <option value="2024">2024</option>
                  <option value="2025">2025</option>
                </select>
              </div>
            )}
          </div>
          <div className="absolute top-full left-1/2 -translate-x-1/2 bg-amber-100 text-amber-800 border-x border-b border-amber-300 px-4 py-1 rounded-b-md shadow-md text-xs font-bold tracking-wider z-50">
            DEMO MODE — SYNTHETIC ANALYSIS DATA
          </div>
        </div>
      )}

      <main className="flex-1 flex overflow-hidden">
        {activeTab !== 'Analytics' && (
          <LeftSidebar 
            interventions={interventions} 
            selectedId={selectedId} 
            onSelect={setSelectedId}
            activeLayers={activeLayers}
            setActiveLayers={setActiveLayers}
            baseMap={baseMap}
            setBaseMap={setBaseMap}
            activeTab={activeTab}
          />
        )}
        
        {activeTab === 'Analytics' ? (
          <div className="flex-1 overflow-y-auto bg-gray-50 p-6">
            <AnalyticsDashboard interventions={demoMode ? interventions : interventions.filter(i => i.data_status === 'REAL')} demoMode={demoMode} />
          </div>
        ) : (
          <div className="flex-1 relative flex flex-col bg-gray-200 border-x border-gray-300 min-w-0 min-h-0">
            <MapViewer 
              interventions={demoMode ? interventions : interventions.filter(i => i.data_status === 'REAL')}
              selectedId={selectedId}
              onSelect={setSelectedId}
              baseMap={baseMap}
              activeLayers={activeLayers}
              demoMode={demoMode}
              activeTab={activeTab}
              selectedYear={selectedYear}
              compareYear={compareYear}
              swipeMode={swipeMode}
              setClickedCell={setClickedCell}
            />
          </div>
        )}
        
        {activeTab === 'Change Detection' && clickedCell && (
          <div className="w-[400px] shrink-0 bg-gray-50 flex flex-col h-full shadow-lg z-10 border-l border-gray-300">
            <div className="p-4 bg-white border-b border-gray-200 shrink-0 relative">
              <span className="absolute top-2 right-2 bg-amber-500 text-[10px] font-bold px-2 py-0.5 rounded-full text-white shadow">DEMO</span>
              <h2 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Cell Analysis</h2>
              <div className="text-xl font-bold text-gray-900 leading-tight">Zone #{clickedCell.properties.cell_id}</div>
              <div className="text-sm text-gray-500 font-medium">Year: {selectedYear}</div>
            </div>
            <div className="flex-1 p-4 overflow-y-auto">
              <div className="bg-white border border-gray-300 shadow-sm rounded-md p-4 mb-4">
                <div className="text-xs font-bold text-gray-500 mb-2 uppercase">Classification</div>
                <div className={`text-sm font-extrabold px-3 py-2 rounded-md ${
                  clickedCell.properties.years[selectedYear].changeClass === 'severe_degradation' ? 'bg-red-100 text-red-800 border-red-300' :
                  clickedCell.properties.years[selectedYear].changeClass === 'moderate_degradation' ? 'bg-orange-100 text-orange-800 border-orange-300' :
                  clickedCell.properties.years[selectedYear].changeClass === 'improving' ? 'bg-green-100 text-green-800 border-green-300' :
                  clickedCell.properties.years[selectedYear].changeClass === 'strong_improvement' ? 'bg-green-200 text-green-900 border-green-400' :
                  'bg-gray-200 text-gray-800 border-gray-300'
                } border`}>
                  {clickedCell.properties.years[selectedYear].changeClass.replace('_', ' ').toUpperCase()}
                </div>
                <div className="text-sm text-gray-700 mt-3 font-medium">
                  {clickedCell.properties.years[selectedYear].reasonText}
                </div>
              </div>
              <div className="bg-white border border-gray-300 shadow-sm rounded-md p-4 mb-4">
                <div className="text-xs font-bold text-gray-500 mb-2 uppercase">Metrics</div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-bold text-gray-700">Δ SAVI</span>
                  <span className="text-sm font-extrabold text-blue-600">{clickedCell.properties.years[selectedYear].deltaSAVI > 0 ? '+' : ''}{clickedCell.properties.years[selectedYear].deltaSAVI}</span>
                </div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-bold text-gray-700">Δ MNDWI</span>
                  <span className="text-sm font-extrabold text-blue-600">{clickedCell.properties.years[selectedYear].deltaMNDWI > 0 ? '+' : ''}{clickedCell.properties.years[selectedYear].deltaMNDWI}</span>
                </div>
                <div className="flex justify-between items-center border-t border-gray-100 pt-2 mt-2">
                  <span className="text-sm font-bold text-gray-700">Rainfall Context</span>
                  <span className="text-sm font-bold text-gray-600 bg-gray-100 px-2 py-0.5 rounded">{clickedCell.properties.years[selectedYear].rainfallContext}</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'Interventions' && selectedId && (
          <RightPanel intervention={selectedInv} demoMode={demoMode} />
        )}
      </main>
    </div>
  );
}
""",
    "frontend/src/components/MapViewer.tsx": """import React, { useEffect, useState, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import axios from 'axios';
// Optional import for side-by-side if installed, otherwise we'll handle it carefully
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

  const styleCell = (feature, year) => {
    const changeClass = feature.properties.years[year].changeClass;
    return {
      fillColor: getColor(changeClass),
      weight: 1,
      opacity: 0.2,
      color: 'white',
      fillOpacity: 0.65
    };
  };

  const bounds = watershedData ? L.geoJSON(watershedData).getBounds() : [[18.80, 73.80], [18.90, 73.95]];
  const showChangeMaps = activeTab === 'Change Detection' && activeLayers.includes('Integrated Change Index (SCI)');

  useEffect(() => {
    // Side by side control logic
    if (mapRef.current && swipeMode && showChangeMaps) {
      const map = mapRef.current;
      if (!sideBySideRef.current && L.control.sideBySide) {
        // Need raw leaflet layers to pass to sideBySide
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

  // A simple wrapper to grab Leaflet instances for side-by-side
  const GeoJSONWrapper = ({ data, style, onEachFeature, isLeft }) => {
    const map = useMap();
    useEffect(() => {
      const layer = L.geoJSON(data, { style, onEachFeature });
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
    }, [map, data, style, onEachFeature, isLeft]);
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
            {swipeMode ? (
              <>
                <GeoJSONWrapper 
                  isLeft={true}
                  data={gridData} 
                  style={(f) => styleCell(f, selectedYear)} 
                  onEachFeature={(f, l) => l.on('click', () => setClickedCell(f))}
                />
                <GeoJSONWrapper 
                  isLeft={false}
                  data={gridData} 
                  style={(f) => styleCell(f, compareYear)} 
                  onEachFeature={(f, l) => l.on('click', () => setClickedCell(f))}
                />
              </>
            ) : (
              <GeoJSON 
                key={`grid-${selectedYear}`} // Force re-render on year change
                data={gridData} 
                style={(f) => styleCell(f, selectedYear)}
                onEachFeature={(f, l) => {
                  l.on('click', () => setClickedCell(f));
                }}
              />
            )}
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
}

def create_files():
    for path, content in frontend_files.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    create_files()
