import os

frontend_files = {
    "frontend/src/App.tsx": """import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MapViewer from './components/MapViewer';
import LeftSidebar from './components/LeftSidebar';
import RightPanel from './components/RightPanel';
import TopNav from './components/TopNav';

export default function App() {
  const [interventions, setInterventions] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [selectedId, setSelectedId] = useState(null);
  const [demoMode, setDemoMode] = useState(false);
  const [activeLayers, setActiveLayers] = useState(['Check Dams', 'Project Boundary']);
  const [baseMap, setBaseMap] = useState('Satellite');

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
    <div className="h-screen w-full flex flex-col bg-slate-900 text-slate-200 font-sans overflow-hidden">
      <TopNav metrics={metrics} demoMode={demoMode} setDemoMode={setDemoMode} />
      
      <main className="flex-1 flex overflow-hidden">
        {/* LEFT SIDEBAR ~320px */}
        <LeftSidebar 
          interventions={interventions} 
          selectedId={selectedId} 
          onSelect={setSelectedId}
          activeLayers={activeLayers}
          setActiveLayers={setActiveLayers}
          baseMap={baseMap}
          setBaseMap={setBaseMap}
        />
        
        {/* CENTER MAP ~60% */}
        <div className="flex-1 relative bg-slate-800">
          <MapViewer 
            interventions={demoMode ? interventions : interventions.filter(i => i.data_status === 'REAL')}
            selectedId={selectedId}
            onSelect={setSelectedId}
            baseMap={baseMap}
            activeLayers={activeLayers}
            demoMode={demoMode}
          />
        </div>
        
        {/* RIGHT INSPECTION PANEL ~360px */}
        {selectedId && (
          <RightPanel intervention={selectedInv} demoMode={demoMode} />
        )}
      </main>
    </div>
  );
}
""",
    "frontend/src/components/TopNav.tsx": """import React from 'react';

export default function TopNav({ metrics, demoMode, setDemoMode }) {
  return (
    <header className="bg-[#0b1121] text-white flex flex-col shrink-0 shadow-lg border-b border-slate-700 z-50">
      <div className="flex justify-between items-center px-4 py-2 border-b border-slate-800">
        <div className="font-bold tracking-wider text-sm flex items-center gap-3">
          <span className="text-blue-400">WATERSHED EVIDENCE ENGINE</span>
          <span className="text-slate-500 text-xs">|</span>
          <span className="text-slate-300 text-xs">Intervention-level geospatial monitoring</span>
        </div>
        <div className="text-sm font-semibold tracking-wide text-slate-300">
          Maharashtra / Pune / PUNE-WDC-1 /2021-22
        </div>
        <div className="text-xs text-slate-400 flex items-center gap-4">
          <label className="flex items-center gap-2 cursor-pointer bg-slate-800 px-2 py-1 rounded border border-slate-700 hover:bg-slate-700">
            <input type="checkbox" checked={demoMode} onChange={(e) => setDemoMode(e.target.checked)} />
            <span className={demoMode ? "text-yellow-400 font-bold" : ""}>DEMO MODE</span>
          </label>
          <span>Last Updated: Today</span>
          <span className="text-blue-300">Officer Portal</span>
        </div>
      </div>
      
      {metrics && (
        <div className="flex justify-between items-center px-4 py-1 text-xs bg-[#111827]">
          <div className="flex gap-6 text-slate-300">
            <span>Total: <strong className="text-white">{metrics.total}</strong></span>
            <span>Check Dams: <strong className="text-white">{metrics.check_dams}</strong></span>
            <span>Field Evidence: <strong className="text-white">{metrics.field_evidence}</strong></span>
            <span>Needs Review: <strong className="text-yellow-400">{metrics.needs_review}</strong></span>
            <span>Verified: <strong className="text-green-400">{metrics.verified}</strong></span>
            <span>Flagged: <strong className="text-red-400">{metrics.flagged}</strong></span>
          </div>
          <div className="flex gap-4">
            <span className="text-slate-500 cursor-pointer hover:text-white">Overview</span>
            <span className="text-white font-bold cursor-pointer">Interventions</span>
            <span className="text-slate-500 cursor-pointer hover:text-white">Change Detection</span>
            <span className="text-slate-500 cursor-pointer hover:text-white">Analytics</span>
          </div>
        </div>
      )}
    </header>
  );
}
""",
    "frontend/src/components/LeftSidebar.tsx": """import React from 'react';

export default function LeftSidebar({ interventions, selectedId, onSelect, activeLayers, setActiveLayers, baseMap, setBaseMap }) {
  
  const toggleLayer = (layer) => {
    if (activeLayers.includes(layer)) setActiveLayers(activeLayers.filter(l => l !== layer));
    else setActiveLayers([...activeLayers, layer]);
  };

  const LayerCheckbox = ({ label }) => (
    <label className="flex items-center gap-2 text-xs cursor-pointer hover:text-white py-0.5">
      <input type="checkbox" checked={activeLayers.includes(label)} onChange={() => toggleLayer(label)} className="bg-slate-800 border-slate-600 rounded" />
      {label}
    </label>
  );

  return (
    <div className="w-[320px] bg-[#0f172a] border-r border-slate-700 flex flex-col h-full">
      <div className="p-3 border-b border-slate-700 bg-[#1e293b]">
        <h2 className="text-sm font-bold tracking-wide text-slate-200">INTERVENTION QUEUE</h2>
        <input type="text" placeholder="Search work code..." className="w-full mt-2 bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs text-white placeholder-slate-500 outline-none focus:border-blue-500" />
      </div>
      
      <div className="flex-1 overflow-y-auto p-2 flex flex-col gap-2 custom-scrollbar">
        {interventions.map(inv => (
          <div 
            key={inv.id} 
            className={`p-2 rounded border cursor-pointer ${selectedId === inv.id ? 'bg-slate-800 border-blue-500' : 'bg-slate-900/50 border-slate-700 hover:border-slate-500'}`}
            onClick={() => onSelect(inv.id)}
          >
            <div className="flex justify-between items-start mb-1">
              <div>
                <div className="text-xs font-bold text-white">{inv.type}</div>
                <div className="text-[10px] text-slate-400">WC: {inv.work_code}</div>
              </div>
              <div className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${inv.status_badge === 'REVIEW' ? 'bg-yellow-900/50 text-yellow-500 border border-yellow-700' : inv.status_badge === 'FLAGGED' ? 'bg-red-900/50 text-red-400 border border-red-700' : 'bg-green-900/50 text-green-400 border border-green-700'}`}>
                {inv.status_badge}
              </div>
            </div>
            {inv.data_status !== 'UNAVAILABLE' && inv.score_impact !== null ? (
              <div className="text-[10px] text-slate-300 mt-1">
                Impact: <span className="font-bold text-white">{inv.score_impact}</span> | Conf: <span className="font-bold text-white">{inv.score_confidence}</span>
              </div>
            ) : (
              <div className="text-[10px] text-slate-500 mt-1 italic">Data Unavailable</div>
            )}
            <div className="text-[10px] text-slate-400 mt-1 line-clamp-1">{inv.priority_reason}</div>
          </div>
        ))}
      </div>

      <div className="h-64 border-t border-slate-700 p-3 bg-[#1e293b] overflow-y-auto text-slate-300">
        <h3 className="text-xs font-bold text-white mb-2">LAYER CONTROL</h3>
        <div className="mb-3">
          <div className="text-[10px] uppercase text-slate-500 font-bold mb-1">Basemap</div>
          <select 
            value={baseMap} 
            onChange={e => setBaseMap(e.target.value)} 
            className="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs text-white outline-none"
          >
            <option>Satellite</option>
            <option>Street</option>
            <option>Terrain</option>
          </select>
        </div>
        
        <div className="mb-2">
          <div className="text-[10px] uppercase text-slate-500 font-bold mb-1">Watershed</div>
          <LayerCheckbox label="Project Boundary" />
        </div>
        <div className="mb-2">
          <div className="text-[10px] uppercase text-slate-500 font-bold mb-1">Interventions</div>
          <LayerCheckbox label="Check Dams" />
        </div>
        <div className="mb-2">
          <div className="text-[10px] uppercase text-slate-500 font-bold mb-1">Analytics</div>
          <LayerCheckbox label="Water Change" />
          <LayerCheckbox label="Vegetation Change" />
        </div>
      </div>
    </div>
  );
}
""",
    "frontend/src/components/RightPanel.tsx": """import React, { useState } from 'react';

export default function RightPanel({ intervention, demoMode }) {
  const [tab, setTab] = useState('EVIDENCE');

  return (
    <div className="w-[360px] bg-[#0f172a] border-l border-slate-700 flex flex-col h-full overflow-hidden">
      <div className="p-4 bg-[#1e293b] border-b border-slate-700 shrink-0">
        <h2 className="text-sm font-bold text-white uppercase tracking-wide">INTERVENTION EVIDENCE</h2>
        <div className="text-lg font-bold text-blue-400 mt-1">{intervention.type}</div>
        <div className="text-xs text-slate-400 mb-2">Work Code: {intervention.work_code}</div>
        
        <div className="flex items-center justify-between">
          <div className={`text-xs font-bold px-2 py-1 rounded border ${intervention.status_badge === 'REVIEW' ? 'bg-yellow-900/50 text-yellow-500 border-yellow-700' : intervention.status_badge === 'FLAGGED' ? 'bg-red-900/50 text-red-400 border-red-700' : 'bg-green-900/50 text-green-400 border-green-700'}`}>
            {intervention.status_badge}
          </div>
          <div className="text-xs text-slate-500">
            {intervention.lat ? `${intervention.lat.toFixed(6)}, ${intervention.lng.toFixed(6)}` : 'Coordinates unavailable'}
          </div>
        </div>
      </div>

      <div className="flex border-b border-slate-700 bg-slate-900 text-xs font-bold text-slate-400">
        <div className={`flex-1 text-center py-2 cursor-pointer ${tab === 'EVIDENCE' ? 'text-white border-b-2 border-blue-500' : 'hover:text-slate-300'}`} onClick={() => setTab('EVIDENCE')}>EVIDENCE</div>
        <div className={`flex-1 text-center py-2 cursor-pointer ${tab === 'CHANGE' ? 'text-white border-b-2 border-blue-500' : 'hover:text-slate-300'}`} onClick={() => setTab('CHANGE')}>CHANGE</div>
        <div className={`flex-1 text-center py-2 cursor-pointer ${tab === 'FLAGS' ? 'text-white border-b-2 border-blue-500' : 'hover:text-slate-300'}`} onClick={() => setTab('FLAGS')}>FLAGS</div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-6 custom-scrollbar text-sm">
        {intervention.data_status === 'UNAVAILABLE' ? (
          <div className="text-center text-slate-500 mt-10 text-xs border border-slate-700 border-dashed rounded p-4">
            Data not available for this project.<br/>Waiting for official ingestion.
          </div>
        ) : (
          <>
            {tab === 'EVIDENCE' && (
              <>
                <div className="bg-slate-900 border border-slate-700 rounded p-3 relative">
                  {intervention.data_status === 'DEMO' && demoMode && <span className="absolute top-0 right-0 bg-yellow-600 text-[9px] font-bold px-1 rounded-bl text-white">DEMO</span>}
                  <div className="flex justify-between items-center mb-3">
                    <div className="text-center">
                      <div className="text-xs text-slate-400">IMPACT SCORE</div>
                      <div className="text-2xl font-bold text-white">{intervention.score_impact} <span className="text-xs text-slate-500">/ 100</span></div>
                    </div>
                    <div className="text-center">
                      <div className="text-xs text-slate-400">CONFIDENCE</div>
                      <div className="text-2xl font-bold text-white">{intervention.score_confidence} <span className="text-xs text-slate-500">/ 100</span></div>
                    </div>
                  </div>
                  <div className="text-xs text-slate-400 mb-2 border-b border-slate-700 pb-1">Score Breakdown</div>
                  <div className="grid grid-cols-2 gap-y-2 text-xs">
                    <div className="flex justify-between pr-4"><span>Vegetation</span><span className="text-green-400">+{intervention.impact_veg}</span></div>
                    <div className="flex justify-between pr-4"><span>Water</span><span className="text-blue-400">+{intervention.impact_water}</span></div>
                    <div className="flex justify-between pr-4"><span>Structural</span><span className="text-slate-300">+{intervention.impact_lulc}</span></div>
                    <div className="flex justify-between pr-4"><span>Temporal</span><span className="text-slate-300">+{intervention.impact_temporal}</span></div>
                    <div className="flex justify-between pr-4"><span>Field</span><span className="text-slate-300">+{intervention.impact_field}</span></div>
                  </div>
                  <div className="text-[10px] text-slate-500 italic mt-3 text-center">Evidence-based impact indicator</div>
                </div>

                <div>
                  <h3 className="text-xs font-bold text-slate-400 mb-2 uppercase tracking-wide">Why this intervention?</h3>
                  <div className="text-xs text-slate-300 flex flex-col gap-1">
                    {!intervention.flag_water && <div className="text-green-400">✓ Surface water response detected</div>}
                    {!intervention.flag_veg && <div className="text-green-400">✓ Vegetation response detected</div>}
                    {!intervention.flag_missing_photo && <div className="text-green-400">✓ Field evidence available</div>}
                    {intervention.flag_season && <div className="text-yellow-400">⚠ Seasonal variation requires review</div>}
                    {intervention.flag_conflict && <div className="text-red-400">⚠ Field/Satellite evidence conflict</div>}
                  </div>
                  <div className="text-xs text-white mt-3 p-2 bg-slate-800 rounded border border-slate-700">
                    {intervention.priority_reason}
                  </div>
                </div>
                
                <div>
                  <h3 className="text-xs font-bold text-slate-400 mb-2 uppercase tracking-wide">FIELD EVIDENCE</h3>
                  {intervention.flag_missing_photo ? (
                    <div className="h-24 bg-slate-900 border border-slate-700 rounded flex items-center justify-center text-xs text-slate-500 uppercase tracking-widest">
                      Field Photo Unavailable
                    </div>
                  ) : (
                    <div className="flex flex-col gap-2">
                      <div className="h-32 bg-slate-800 border border-slate-700 rounded flex items-center justify-center text-xs text-slate-400">
                        [ Geo-tagged Photo Proxy ]
                      </div>
                      <div className="text-xs text-slate-300">Visible water accumulation near the structure.</div>
                    </div>
                  )}
                </div>
              </>
            )}

            {tab === 'CHANGE' && (
              <>
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wide">CHANGE DETECTION</h3>
                  {intervention.data_status === 'DEMO' && demoMode && <span className="bg-yellow-600 text-[9px] font-bold px-1 rounded text-white">DEMO</span>}
                </div>
                
                <div className="flex gap-2 mb-3">
                  <div className="flex-1 bg-slate-800 border border-slate-700 rounded p-2 text-center text-xs">
                    <div className="text-slate-500 mb-1">BEFORE</div>
                    <div className="text-white">May 2023</div>
                  </div>
                  <div className="flex-1 bg-slate-800 border border-slate-700 rounded p-2 text-center text-xs">
                    <div className="text-slate-500 mb-1">AFTER</div>
                    <div className="text-white">May 2024</div>
                  </div>
                </div>

                <div className="flex flex-col gap-3">
                  <div className="bg-slate-900 border border-slate-700 rounded p-3">
                    <div className="text-xs text-slate-400 mb-1">Water Spread Change</div>
                    <div className="flex justify-between items-end">
                      <span className="text-lg font-bold text-blue-400">{intervention.water_spread_change > 0 ? '+' : ''}{intervention.water_spread_change}%</span>
                      <span className="text-xs text-slate-500">1,240 m² → 3,870 m²</span>
                    </div>
                  </div>
                  <div className="bg-slate-900 border border-slate-700 rounded p-3">
                    <div className="text-xs text-slate-400 mb-1">NDVI (Vegetation) Change</div>
                    <div className="flex justify-between items-end">
                      <span className="text-lg font-bold text-green-400">{intervention.ndvi_change > 0 ? '+' : ''}{intervention.ndvi_change}</span>
                      <span className="text-xs text-slate-500">0.31 → 0.46</span>
                    </div>
                  </div>
                  <div className="bg-slate-900 border border-slate-700 rounded p-3">
                    <div className="text-xs text-slate-400 mb-1">MNDWI (Water Index) Change</div>
                    <div className="flex justify-between items-end">
                      <span className="text-lg font-bold text-blue-400">{intervention.mndwi_change > 0 ? '+' : ''}{intervention.mndwi_change}</span>
                    </div>
                  </div>
                </div>
                
                <div className="mt-4">
                  <h3 className="text-xs font-bold text-slate-400 mb-2 uppercase tracking-wide">REFERENCE ZONE (500m)</h3>
                  <div className="text-xs text-slate-300 border-l-2 border-blue-500 pl-3">
                    Intervention shows higher vegetation and water response compared to the 500m surrounding reference zone.
                  </div>
                </div>
              </>
            )}

            {tab === 'FLAGS' && (
              <div className="flex flex-col gap-3">
                {intervention.flag_conflict && (
                  <div className="bg-red-900/20 border border-red-700/50 p-3 rounded">
                    <div className="text-red-400 text-xs font-bold mb-1 uppercase">Field / Satellite Conflict</div>
                    <div className="text-xs text-slate-300">Field evidence and satellite evidence disagree.</div>
                    <div className="text-[10px] text-slate-500 mt-2">Recommended: On-site verification.</div>
                  </div>
                )}
                {intervention.flag_hydro && (
                  <div className="bg-orange-900/20 border border-orange-700/50 p-3 rounded">
                    <div className="text-orange-400 text-xs font-bold mb-1 uppercase">Hydrological Mismatch</div>
                    <div className="text-xs text-slate-300">Intervention does not intersect expected drainage network.</div>
                  </div>
                )}
                {intervention.flag_season && (
                  <div className="bg-yellow-900/20 border border-yellow-700/50 p-3 rounded">
                    <div className="text-yellow-400 text-xs font-bold mb-1 uppercase">Seasonality Conflict</div>
                    <div className="text-xs text-slate-300">Observed change may be explained by rainfall/seasonal variation rather than structure impact.</div>
                  </div>
                )}
                {!intervention.flag_conflict && !intervention.flag_hydro && !intervention.flag_season && (
                  <div className="text-xs text-slate-500 italic p-3 border border-slate-700 border-dashed rounded text-center">
                    No critical red flags detected.
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </div>
      
      <div className="p-3 bg-slate-900 border-t border-slate-700 text-[9px] text-slate-500">
        <div className="font-bold mb-1 text-slate-400">DATA SOURCES</div>
        <div>Govt/Spatial: Bhuvan WDC 2.0, WDC PMKSY MIS</div>
        <div>Remote Sensing: Sentinel-2 (Bhuvan imagery where avail)</div>
        <div>Field: DRISHTI geo-tagged evidence</div>
      </div>
    </div>
  );
}
""",
    "frontend/src/components/MapViewer.tsx": """import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25,41],
    iconAnchor: [12,41]
});
L.Marker.prototype.options.icon = DefaultIcon;

const MapController = ({ interventions, selectedId }) => {
  const map = useMap();
  useEffect(() => {
    // Fit to project logic: for now center on Khed (18.85, 73.85) 
    // If a marker is selected and it has coords, fly to it.
    if (selectedId) {
      const inv = interventions.find(i => i.id === selectedId);
      if (inv && inv.lat && inv.lng) {
        map.flyTo([inv.lat, inv.lng], 16);
      }
    } else {
      map.flyTo([18.85, 73.85], 13);
    }
  }, [selectedId, interventions, map]);
  return null;
};

export default function MapViewer({ interventions, selectedId, onSelect, baseMap, activeLayers, demoMode }) {
  
  const getBaseUrl = () => {
    switch (baseMap) {
      case 'Terrain': return 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png';
      case 'Street': return 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
      case 'Satellite': default: return 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
    }
  };

  return (
    <div className="h-full w-full relative">
      {!demoMode && interventions.every(i => !i.lat) && (
        <div className="absolute inset-0 z-[1000] flex flex-col items-center justify-center bg-slate-900/80 text-white p-6 text-center">
          <div className="text-2xl font-bold mb-2">Coordinates Unavailable</div>
          <div className="text-slate-400 text-sm max-w-md">
            Official spatial coordinates for PUNE-WDC-1 interventions are pending validation. 
            <br/><br/>
            Toggle <strong>DEMO MODE</strong> in the top header to view the application with prototype demonstration coordinates and analytics.
          </div>
        </div>
      )}

      <MapContainer center={[18.85, 73.85]} zoom={13} style={{ height: '100%', width: '100%', background: '#1e293b' }} zoomControl={false}>
        <TileLayer url={getBaseUrl()} />

        <MapController interventions={interventions} selectedId={selectedId} />

        {activeLayers.includes('Check Dams') && interventions.filter(i => i.lat && i.lng).map(inv => (
          <Marker 
            key={inv.id} 
            position={[inv.lat, inv.lng]}
            eventHandlers={{ click: () => onSelect(inv.id) }}
          >
            <Popup className="text-xs">
              <strong>CHECK DAM</strong><br/>
              Work Code: {inv.work_code}<br/>
              Project: PUNE-WDC-1<br/>
              <button className="text-blue-500 font-bold mt-1" onClick={() => onSelect(inv.id)}>Open Evidence</button>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
      
      {/* Map Tools Overlay */}
      <div className="absolute top-4 right-4 z-[1000] flex flex-col gap-2">
        <button className="w-8 h-8 bg-slate-800 border border-slate-700 text-white rounded shadow flex items-center justify-center hover:bg-slate-700">+</button>
        <button className="w-8 h-8 bg-slate-800 border border-slate-700 text-white rounded shadow flex items-center justify-center hover:bg-slate-700">-</button>
        <button className="w-8 h-8 bg-slate-800 border border-slate-700 text-white rounded shadow flex items-center justify-center hover:bg-slate-700" title="Measure">📏</button>
        <button className="w-8 h-8 bg-slate-800 border border-slate-700 text-white rounded shadow flex items-center justify-center hover:bg-slate-700" title="Fullscreen">⛶</button>
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
