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
            />
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
    "frontend/src/components/LeftSidebar.tsx": """import React, { useMemo } from 'react';

export default function LeftSidebar({ interventions, selectedId, onSelect, activeLayers, setActiveLayers, baseMap, setBaseMap, activeTab }) {
  
  const toggleLayer = (layer) => {
    if (activeLayers.includes(layer)) setActiveLayers(activeLayers.filter(l => l !== layer));
    else setActiveLayers([...activeLayers, layer]);
  };

  const LayerCheckbox = ({ label }) => (
    <label className="flex items-center gap-2 text-sm cursor-pointer hover:bg-gray-100 p-1.5 rounded-md transition-colors text-gray-700 font-medium">
      <input type="checkbox" checked={activeLayers.includes(label)} onChange={() => toggleLayer(label)} className="w-4 h-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500" />
      {label}
    </label>
  );

  const sortedInterventions = useMemo(() => {
    return [...interventions].sort((a, b) => {
      const order = { 'FLAGGED': 1, 'REVIEW': 2, 'VERIFIED': 3 };
      if (order[a.status_badge] !== order[b.status_badge]) {
        return order[a.status_badge] - order[b.status_badge];
      }
      if (a.status_badge === 'REVIEW') {
        const confA = a.score_confidence || 0;
        const confB = b.score_confidence || 0;
        return confB - confA;
      }
      return 0;
    });
  }, [interventions]);

  if (activeTab === 'Overview') {
    return (
      <div className="w-[320px] shrink-0 bg-white p-4 border-r border-gray-300">
        <h2 className="text-sm font-bold tracking-wide text-gray-800 uppercase mb-4">Project Overview</h2>
        <div className="text-sm text-gray-600">Select Interventions or Change Detection to view spatial data.</div>
      </div>
    );
  }

  if (activeTab === 'Change Detection') {
    return (
      <div className="w-[320px] shrink-0 bg-white flex flex-col h-full shadow-sm z-10 border-r border-gray-300">
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-sm font-bold tracking-wide text-gray-800 uppercase">Change Detection Layers</h2>
          <div className="text-xs text-gray-500 mt-1">Select analytical raster overlays</div>
        </div>
        
        <div className="flex-1 p-4 flex flex-col gap-4 overflow-y-auto">
          <div>
            <div className="text-xs uppercase text-gray-500 font-bold mb-2">Basemap</div>
            <select 
              value={baseMap} 
              onChange={e => setBaseMap(e.target.value)} 
              className="w-full bg-white border border-gray-300 rounded-md px-3 py-2 text-sm text-gray-800 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 shadow-sm"
            >
              <option>Satellite</option>
              <option>Street</option>
              <option>Terrain</option>
            </select>
          </div>
          
          <div className="border-t border-gray-200 pt-4">
            <div className="text-xs uppercase text-gray-500 font-bold mb-3">Change Detection Maps</div>
            <div className="flex flex-col gap-1">
              <LayerCheckbox label="Land Use / Degradation" />
              <LayerCheckbox label="Drainage Change" />
              <LayerCheckbox label="Vegetation (SAVI)" />
              <LayerCheckbox label="Water Conservation (MNDWI)" />
              <LayerCheckbox label="Integrated Change Index (SCI)" />
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="w-[320px] shrink-0 bg-gray-50 flex flex-col h-full z-10 border-r border-gray-300">
      <div className="p-4 border-b border-gray-200 bg-white shrink-0">
        <h2 className="text-sm font-bold tracking-wide text-gray-800 uppercase">Intervention Queue</h2>
        <input type="text" placeholder="Search work code..." className="w-full mt-3 bg-white border border-gray-300 rounded-md px-3 py-2 text-sm text-gray-800 placeholder-gray-400 shadow-sm outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-shadow" />
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-3 custom-scrollbar">
        {sortedInterventions.map(inv => (
          <div 
            key={inv.id} 
            className={`p-3 rounded-md border transition-all cursor-pointer shadow-sm bg-white ${selectedId === inv.id ? 'border-blue-500 ring-1 ring-blue-500' : 'border-gray-300 hover:border-gray-400'}`}
            onClick={() => onSelect(inv.id)}
          >
            <div className="flex justify-between items-start mb-2">
              <div>
                <div className="text-sm font-bold text-gray-900">{inv.type}</div>
                <div className="text-xs text-gray-500 font-medium">WC: {inv.work_code}</div>
              </div>
              <div className={`text-[10px] font-bold px-2 py-1 rounded shadow-sm border ${inv.status_badge === 'REVIEW' ? 'bg-amber-100 text-amber-800 border-amber-300' : inv.status_badge === 'FLAGGED' ? 'bg-red-100 text-red-800 border-red-300' : 'bg-green-100 text-green-800 border-green-300'}`}>
                {inv.status_badge}
              </div>
            </div>
            {inv.data_status !== 'UNAVAILABLE' && inv.score_impact !== null ? (
              <div className="text-xs text-gray-700 mt-2 bg-gray-50 border border-gray-100 p-2 rounded-md">
                Impact: <span className="font-bold text-gray-900">{inv.score_impact}</span> <span className="mx-1 text-gray-300">|</span> Conf: <span className="font-bold text-gray-900">{inv.score_confidence}</span>
              </div>
            ) : (
              <div className="text-xs text-gray-500 mt-2 italic bg-gray-50 border border-gray-100 p-2 rounded-md">Data Unavailable</div>
            )}
            <div className="text-xs text-gray-600 mt-2 line-clamp-2 leading-relaxed">{inv.priority_reason}</div>
          </div>
        ))}
      </div>

      <div className="border-t border-gray-200 p-4 bg-white shrink-0">
        <h3 className="text-sm font-bold text-gray-800 mb-3 uppercase tracking-wide">Layer Control</h3>
        <div className="mb-4">
          <div className="text-xs uppercase text-gray-500 font-bold mb-2">Basemap</div>
          <select 
            value={baseMap} 
            onChange={e => setBaseMap(e.target.value)} 
            className="w-full bg-white border border-gray-300 rounded-md px-3 py-2 text-sm text-gray-800 outline-none focus:border-blue-500 shadow-sm"
          >
            <option>Satellite</option>
            <option>Street</option>
            <option>Terrain</option>
          </select>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <div className="text-xs uppercase text-gray-500 font-bold mb-2">Context</div>
            <LayerCheckbox label="Project Boundary" />
            <LayerCheckbox label="Check Dams" />
          </div>
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
    <div className="w-[400px] shrink-0 bg-gray-50 flex flex-col h-full shadow-lg z-10 border-l border-gray-300">
      <div className="p-4 bg-white border-b border-gray-200 shrink-0">
        <h2 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Intervention Evidence</h2>
        <div className="text-xl font-bold text-gray-900 leading-tight">{intervention.type}</div>
        <div className="text-sm text-gray-500 font-medium mb-3">Work Code: {intervention.work_code}</div>
        
        <div className="flex items-center justify-between">
          <div className={`text-xs font-bold px-2 py-1 rounded shadow-sm border ${intervention.status_badge === 'REVIEW' ? 'bg-amber-100 text-amber-800 border-amber-300' : intervention.status_badge === 'FLAGGED' ? 'bg-red-100 text-red-800 border-red-300' : 'bg-green-100 text-green-800 border-green-300'}`}>
            {intervention.status_badge}
          </div>
          <div className="text-xs text-gray-500 font-medium bg-gray-100 px-2 py-1 rounded-md border border-gray-200">
            {intervention.lat ? `${intervention.lat.toFixed(6)}, ${intervention.lng.toFixed(6)}` : 'Coordinates unavailable'}
          </div>
        </div>
      </div>

      <div className="flex bg-white border-b border-gray-200 text-sm font-bold text-gray-600 shrink-0">
        <button className={`flex-1 text-center py-3 transition-colors ${tab === 'EVIDENCE' ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50/50' : 'hover:text-gray-900 hover:bg-gray-50'}`} onClick={() => setTab('EVIDENCE')}>EVIDENCE</button>
        <button className={`flex-1 text-center py-3 transition-colors ${tab === 'CHANGE' ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50/50' : 'hover:text-gray-900 hover:bg-gray-50'}`} onClick={() => setTab('CHANGE')}>CHANGE</button>
        <button className={`flex-1 text-center py-3 transition-colors ${tab === 'FLAGS' ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50/50' : 'hover:text-gray-900 hover:bg-gray-50'}`} onClick={() => setTab('FLAGS')}>FLAGS</button>
      </div>

      <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-4 custom-scrollbar">
        {intervention.data_status === 'UNAVAILABLE' ? (
          <div className="text-center text-gray-500 mt-8 text-sm border-2 border-gray-200 border-dashed rounded-md p-6 bg-white shadow-sm">
            <span className="text-2xl block mb-2">📡</span>
            <strong className="text-gray-700 block mb-1">Data not available</strong>
            Waiting for official ingestion for this project.
          </div>
        ) : (
          <>
            {tab === 'EVIDENCE' && (
              <>
                <div className="bg-white border border-gray-300 shadow-sm rounded-md p-4 relative">
                  {intervention.data_status === 'DEMO' && demoMode && <span className="absolute -top-2 -right-2 bg-amber-500 text-[10px] font-bold px-2 py-0.5 rounded-full text-white shadow">DEMO</span>}
                  
                  <div className="flex justify-between items-center mb-4">
                    <div className="text-center flex-1 border-r border-gray-100">
                      <div className="text-xs text-gray-500 font-bold mb-1">IMPACT SCORE</div>
                      <div className="text-3xl font-extrabold text-blue-600">{intervention.score_impact} <span className="text-sm text-gray-400 font-normal">/100</span></div>
                    </div>
                    <div className="text-center flex-1">
                      <div className="text-xs text-gray-500 font-bold mb-1">CONFIDENCE</div>
                      <div className="text-3xl font-extrabold text-gray-800">{intervention.score_confidence} <span className="text-sm text-gray-400 font-normal">/100</span></div>
                    </div>
                  </div>
                  
                  <div className="text-xs font-bold text-gray-800 mb-2 border-b border-gray-100 pb-2 uppercase tracking-wide">Score Breakdown</div>
                  <div className="grid grid-cols-2 gap-y-2 gap-x-4 text-xs font-medium">
                    <div className="flex justify-between items-center bg-gray-50 border border-gray-100 p-1.5 rounded-md"><span>Vegetation</span><span className="text-green-600 font-bold">+{intervention.impact_veg}</span></div>
                    <div className="flex justify-between items-center bg-gray-50 border border-gray-100 p-1.5 rounded-md"><span>Water</span><span className="text-blue-600 font-bold">+{intervention.impact_water}</span></div>
                    <div className="flex justify-between items-center bg-gray-50 border border-gray-100 p-1.5 rounded-md"><span>Structural</span><span className="text-gray-700 font-bold">+{intervention.impact_lulc}</span></div>
                    <div className="flex justify-between items-center bg-gray-50 border border-gray-100 p-1.5 rounded-md"><span>Temporal</span><span className="text-gray-700 font-bold">+{intervention.impact_temporal}</span></div>
                    <div className="flex justify-between items-center bg-gray-50 border border-gray-100 p-1.5 rounded-md"><span>Field</span><span className="text-gray-700 font-bold">+{intervention.impact_field}</span></div>
                  </div>
                  <div className="text-[11px] text-gray-500 italic mt-3 text-center">Evidence-based impact indicator. Not causal proof.</div>
                </div>

                <div className="bg-white border border-gray-300 shadow-sm rounded-md p-4">
                  <h3 className="text-xs font-bold text-gray-800 mb-3 border-b border-gray-100 pb-2 uppercase tracking-wide">Why this intervention?</h3>
                  <div className="text-sm text-gray-700 flex flex-col gap-2 font-medium">
                    {!intervention.flag_water && <div className="flex items-center gap-2"><span className="text-green-500 text-lg leading-none">✓</span> Surface water response detected</div>}
                    {!intervention.flag_veg && <div className="flex items-center gap-2"><span className="text-green-500 text-lg leading-none">✓</span> Vegetation response detected</div>}
                    {!intervention.flag_missing_photo && <div className="flex items-center gap-2"><span className="text-green-500 text-lg leading-none">✓</span> Field evidence available</div>}
                    {intervention.flag_season && <div className="flex items-center gap-2 text-amber-600"><span className="text-lg leading-none">⚠</span> Seasonal variation requires review</div>}
                    {intervention.flag_conflict && <div className="flex items-center gap-2 text-red-600"><span className="text-lg leading-none">⚠</span> Field/Satellite evidence conflict</div>}
                  </div>
                  <div className="text-sm text-gray-800 mt-4 p-3 bg-blue-50 rounded-md border border-blue-200 font-medium shadow-sm">
                    {intervention.priority_reason}
                  </div>
                </div>
                
                <div className="bg-white border border-gray-300 shadow-sm rounded-md p-4">
                  <h3 className="text-xs font-bold text-gray-800 mb-3 border-b border-gray-100 pb-2 uppercase tracking-wide">FIELD EVIDENCE</h3>
                  {intervention.flag_missing_photo ? (
                    <div className="h-28 bg-gray-50 border border-gray-200 rounded-md flex flex-col items-center justify-center text-sm text-gray-500">
                      <span className="text-2xl mb-1">📷</span>
                      <span className="font-bold">Field Photo Unavailable</span>
                    </div>
                  ) : (
                    <div className="flex flex-col gap-3">
                      <div className="h-40 bg-gray-100 border border-gray-300 rounded-md flex items-center justify-center text-sm text-gray-500 font-medium shadow-inner">
                        [ Geo-tagged Photo Proxy ]
                      </div>
                      <div className="text-sm text-gray-800 font-medium bg-gray-50 border border-gray-100 p-2 rounded-md">Visible water accumulation near the structure.</div>
                    </div>
                  )}
                </div>
              </>
            )}

            {tab === 'CHANGE' && (
              <>
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-xs font-bold text-gray-800 uppercase tracking-wide">Change Detection</h3>
                  {intervention.data_status === 'DEMO' && demoMode && <span className="bg-amber-500 text-[10px] font-bold px-1.5 py-0.5 rounded text-white shadow-sm">DEMO</span>}
                </div>
                
                <div className="flex gap-4 mb-4">
                  <div className="flex-1 bg-white border border-gray-300 shadow-sm rounded-md p-3 text-center">
                    <div className="text-xs font-bold text-gray-500 mb-1 tracking-wide">BEFORE</div>
                    <div className="text-sm font-extrabold text-gray-800">May 2023</div>
                  </div>
                  <div className="flex-1 bg-white border border-gray-300 shadow-sm rounded-md p-3 text-center">
                    <div className="text-xs font-bold text-gray-500 mb-1 tracking-wide">AFTER</div>
                    <div className="text-sm font-extrabold text-gray-800">May 2024</div>
                  </div>
                </div>

                <div className="flex flex-col gap-3">
                  <div className="bg-white border border-gray-300 shadow-sm rounded-md p-4">
                    <div className="text-xs font-bold text-gray-500 mb-2 uppercase">Water Spread Change</div>
                    <div className="flex justify-between items-end">
                      <span className="text-2xl font-extrabold text-blue-600">{intervention.water_spread_change > 0 ? '+' : ''}{intervention.water_spread_change}%</span>
                      <span className="text-sm font-medium text-gray-600 bg-gray-50 border border-gray-200 px-2 py-1 rounded-md">1,240 m² → 3,870 m²</span>
                    </div>
                  </div>
                  
                  <div className="bg-white border border-gray-300 shadow-sm rounded-md p-4">
                    <div className="text-xs font-bold text-gray-500 mb-2 uppercase">NDVI (Vegetation) Change</div>
                    <div className="flex justify-between items-end">
                      <span className="text-2xl font-extrabold text-green-600">{intervention.ndvi_change > 0 ? '+' : ''}{intervention.ndvi_change}</span>
                      <span className="text-sm font-medium text-gray-600 bg-gray-50 border border-gray-200 px-2 py-1 rounded-md">0.31 → 0.46</span>
                    </div>
                  </div>
                  
                  <div className="bg-white border border-gray-300 shadow-sm rounded-md p-4">
                    <div className="text-xs font-bold text-gray-500 mb-2 uppercase">MNDWI (Water Index) Change</div>
                    <div className="flex justify-between items-end">
                      <span className="text-2xl font-extrabold text-blue-500">{intervention.mndwi_change > 0 ? '+' : ''}{intervention.mndwi_change}</span>
                    </div>
                  </div>
                </div>
                
                <div className="mt-2 bg-blue-50 border border-blue-200 p-4 rounded-md shadow-sm">
                  <h3 className="text-xs font-bold text-blue-800 mb-2 uppercase tracking-wide">Reference Zone (500m)</h3>
                  <div className="text-sm text-blue-900 font-medium">
                    Intervention shows higher vegetation and water response compared to the 500m surrounding reference zone.
                  </div>
                </div>
              </>
            )}

            {tab === 'FLAGS' && (
              <div className="flex flex-col gap-4">
                {intervention.flag_conflict && (
                  <div className="bg-red-50 border border-red-200 p-4 rounded-md shadow-sm">
                    <div className="flex items-center gap-2 text-red-700 font-bold mb-2 uppercase text-xs tracking-wide">
                      <span className="text-lg">⚠</span> Field / Satellite Conflict
                    </div>
                    <div className="text-sm text-red-900 font-medium mb-3">Field evidence and satellite evidence disagree.</div>
                    <div className="text-xs text-red-800 bg-red-100 border border-red-200 p-2 rounded-md font-medium">Recommended: Mandatory on-site verification.</div>
                  </div>
                )}
                
                {intervention.flag_hydro && (
                  <div className="bg-orange-50 border border-orange-200 p-4 rounded-md shadow-sm">
                    <div className="flex items-center gap-2 text-orange-700 font-bold mb-2 uppercase text-xs tracking-wide">
                      <span className="text-lg">⚠</span> Hydrological Mismatch
                    </div>
                    <div className="text-sm text-orange-900 font-medium">Intervention does not intersect expected drainage network.</div>
                  </div>
                )}
                
                {intervention.flag_season && (
                  <div className="bg-amber-50 border border-amber-200 p-4 rounded-md shadow-sm">
                    <div className="flex items-center gap-2 text-amber-700 font-bold mb-2 uppercase text-xs tracking-wide">
                      <span className="text-lg">⚠</span> Seasonality Conflict
                    </div>
                    <div className="text-sm text-amber-900 font-medium">Observed change may be explained by rainfall/seasonal variation rather than structure impact.</div>
                  </div>
                )}
                
                {!intervention.flag_conflict && !intervention.flag_hydro && !intervention.flag_season && (
                  <div className="text-sm font-bold text-gray-500 p-6 border-2 border-gray-200 border-dashed rounded-md text-center bg-white flex flex-col items-center gap-2 shadow-sm">
                    <span className="text-3xl text-green-500">✓</span>
                    No critical red flags detected.
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </div>
      
      <div className="p-4 bg-gray-50 border-t border-gray-200 text-[11px] text-gray-500 font-medium shrink-0">
        <div className="font-bold mb-2 text-gray-700 uppercase tracking-wide">Data Sources</div>
        <div className="mb-1"><strong className="text-gray-600">Govt/Spatial:</strong> Bhuvan WDC 2.0, WDC PMKSY MIS</div>
        <div className="mb-1"><strong className="text-gray-600">Remote Sensing:</strong> Sentinel-2 (Bhuvan imagery where avail)</div>
        <div><strong className="text-gray-600">Field:</strong> DRISHTI geo-tagged evidence</div>
      </div>
    </div>
  );
}
""",
    "frontend/src/components/MapViewer.tsx": """import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, ImageOverlay } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import axios from 'axios';

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
    map.invalidateSize(); // Ensure map repaints when its container size changes
    
    if (selectedId) {
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

// SVG strings with linear gradients, no text, mimicking analytical rasters
const mapLayersSource = {
  'Land Use / Degradation': 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%"><defs><linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:rgb(34,197,94);stop-opacity:1" /><stop offset="50%" style="stop-color:rgb(234,179,8);stop-opacity:1" /><stop offset="100%" style="stop-color:rgb(239,68,68);stop-opacity:1" /></linearGradient></defs><rect width="100%" height="100%" fill="url(%23grad1)" /></svg>',
  'Drainage Change': 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%"><defs><linearGradient id="grad2" x1="0%" y1="100%" x2="100%" y2="0%"><stop offset="0%" style="stop-color:rgb(191,219,254);stop-opacity:1" /><stop offset="100%" style="stop-color:rgb(37,99,235);stop-opacity:1" /></linearGradient></defs><rect width="100%" height="100%" fill="url(%23grad2)" /></svg>',
  'Vegetation (SAVI)': 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%"><defs><linearGradient id="grad3" x1="0%" y1="50%" x2="100%" y2="50%"><stop offset="0%" style="stop-color:rgb(254,240,138);stop-opacity:1" /><stop offset="100%" style="stop-color:rgb(21,128,61);stop-opacity:1" /></linearGradient></defs><rect width="100%" height="100%" fill="url(%23grad3)" /></svg>',
  'Water Conservation (MNDWI)': 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%"><defs><linearGradient id="grad4" x1="100%" y1="100%" x2="0%" y2="0%"><stop offset="0%" style="stop-color:rgb(207,250,254);stop-opacity:1" /><stop offset="100%" style="stop-color:rgb(3,105,161);stop-opacity:1" /></linearGradient></defs><rect width="100%" height="100%" fill="url(%23grad4)" /></svg>',
  'Integrated Change Index (SCI)': 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%"><defs><linearGradient id="grad5" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:rgb(239,68,68);stop-opacity:1" /><stop offset="50%" style="stop-color:rgb(226,232,240);stop-opacity:1" /><stop offset="100%" style="stop-color:rgb(34,197,94);stop-opacity:1" /></linearGradient></defs><rect width="100%" height="100%" fill="url(%23grad5)" /></svg>'
};

// Custom Leaflet Control for the Legend
const LegendControl = ({ activeLayers, demoMode }) => {
  const map = useMap();
  useEffect(() => {
    if (!activeLayers.length) return;
    
    const legend = L.control({ position: 'bottomright' });
    
    legend.onAdd = () => {
      const div = L.DomUtil.create('div', 'bg-white p-4 border border-gray-300 rounded-md shadow-md z-[1000] w-64 text-sm font-sans');
      let html = '';
      
      activeLayers.forEach(layer => {
        let gradient = '';
        if (layer.includes('Degradation')) gradient = 'from-green-500 via-yellow-500 to-red-500';
        else if (layer.includes('Drainage')) gradient = 'from-blue-200 to-blue-600';
        else if (layer.includes('SAVI')) gradient = 'from-yellow-200 to-green-700';
        else if (layer.includes('MNDWI')) gradient = 'from-cyan-100 to-cyan-700';
        else gradient = 'from-red-500 via-slate-200 to-green-500';

        html += `
          <div class="mb-3 last:mb-0">
            <div class="font-bold text-gray-800 uppercase text-xs mb-1 tracking-wide">${layer}</div>
            <div class="h-3 w-full rounded-sm mb-1 bg-gradient-to-r ${gradient}"></div>
            <div class="flex justify-between text-[10px] text-gray-500 uppercase font-medium">
              <span>Low</span><span>High</span>
            </div>
          </div>
        `;
      });

      if (demoMode) {
        html += `<div class="mt-3 text-[10px] font-bold text-amber-700 bg-amber-100 border border-amber-300 px-2 py-1 rounded inline-block uppercase tracking-wide">DEMO MODE ACTIVE</div>`;
      }
      
      div.innerHTML = html;
      // Prevent clicks on legend from interacting with the map
      L.DomEvent.disableClickPropagation(div);
      return div;
    };
    
    legend.addTo(map);
    return () => { legend.remove(); };
  }, [map, activeLayers, demoMode]);
  
  return null;
};

export default function MapViewer({ interventions, selectedId, onSelect, baseMap, activeLayers, demoMode, activeTab }) {
  const [bounds, setBounds] = useState([[18.80, 73.80], [18.90, 73.95]]);
  
  useEffect(() => {
    axios.get('/bounds.json').then(res => setBounds(res.data.bounds)).catch(()=>{});
  }, []);

  const getBaseUrl = () => {
    switch (baseMap) {
      case 'Terrain': return 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png';
      case 'Street': return 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
      case 'Satellite': default: return 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
    }
  };

  const activeAnalyticalLayers = activeTab === 'Change Detection' ? Object.keys(mapLayersSource).filter(l => activeLayers.includes(l)) : [];

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

      <MapContainer center={[18.85, 73.85]} zoom={13} style={{ height: '100%', width: '100%', background: '#e5e7eb' }} zoomControl={false}>
        <TileLayer url={getBaseUrl()} />
        <MapController interventions={interventions} selectedId={selectedId} bounds={bounds} activeTab={activeTab} />

        {/* Change Detection Raster Overlays */}
        {activeTab === 'Change Detection' && activeAnalyticalLayers.map(layerName => (
          <ImageOverlay key={layerName} url={mapLayersSource[layerName]} bounds={bounds} opacity={0.60} />
        ))}

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
              <button className="text-blue-600 font-bold mt-2 hover:underline" onClick={() => onSelect(inv.id)}>Open Evidence</button>
            </Popup>
          </Marker>
        ))}

        {activeTab === 'Change Detection' && activeAnalyticalLayers.length > 0 && (
          <LegendControl activeLayers={activeAnalyticalLayers} demoMode={demoMode} />
        )}
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
""",
    "frontend/src/components/AnalyticsDashboard.tsx": """import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

export default function AnalyticsDashboard({ interventions, demoMode }) {
  const p1 = interventions.filter(i => i.priority === 'P1').length;
  const p2 = interventions.filter(i => i.priority === 'P2').length;
  const p3 = interventions.filter(i => i.priority === 'P3').length;

  const priorityData = [
    { name: 'P1 (Critical)', count: p1, fill: '#ef4444' }, // red-500
    { name: 'P2 (Review)', count: p2, fill: '#f59e0b' },   // amber-500
    { name: 'P3 (Verified)', count: p3, fill: '#10b981' }  // green-500
  ];

  const conflictCount = interventions.filter(i => i.flag_conflict).length;
  const agreementCount = interventions.filter(i => i.data_status !== 'UNAVAILABLE' && !i.flag_conflict).length;
  const agreementData = [
    { name: 'Conflict', value: conflictCount, fill: '#ef4444' },
    { name: 'Agreement', value: agreementCount, fill: '#3b82f6' }
  ];

  const highConf = interventions.filter(i => (i.score_confidence || 0) >= 75).length;
  const medConf = interventions.filter(i => (i.score_confidence || 0) >= 50 && (i.score_confidence || 0) < 75).length;
  const lowConf = interventions.filter(i => (i.score_confidence || 0) < 50 && i.data_status !== 'UNAVAILABLE').length;

  const confData = [
    { name: 'High', count: highConf, fill: '#10b981' },
    { name: 'Medium', count: medConf, fill: '#f59e0b' },
    { name: 'Low', count: lowConf, fill: '#ef4444' }
  ];

  const impactScores = interventions.filter(i => i.score_impact !== null).map(i => ({ name: i.work_code, impact: i.score_impact }));

  return (
    <div className="max-w-6xl mx-auto flex flex-col gap-6">
      <div className="flex justify-between items-center bg-white p-4 rounded-md shadow-sm border border-gray-300">
        <div>
          <h2 className="text-xl font-bold text-gray-800 uppercase tracking-wide">Analytics Dashboard</h2>
          <p className="text-sm text-gray-500 font-medium mt-1">Aggregated insights for PUNE-WDC-1</p>
        </div>
        {demoMode && <div className="bg-amber-100 text-amber-800 border border-amber-300 font-bold px-3 py-1.5 rounded-md shadow-sm text-sm tracking-wide">DEMO MODE ACTIVE</div>}
      </div>

      <div className="grid grid-cols-2 grid-rows-2 gap-6">
        <div className="bg-white p-6 rounded-md border border-gray-300 shadow-sm h-80 flex flex-col">
          <h3 className="text-sm font-bold text-gray-700 uppercase mb-4 tracking-wide border-b border-gray-100 pb-2">Priority Queue Distribution</h3>
          <div className="flex-1 min-h-0">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={priorityData} layout="vertical" margin={{ left: 20, right: 20, top: 10, bottom: 10 }}>
                <XAxis type="number" />
                <YAxis dataKey="name" type="category" width={110} tick={{ fontSize: 12, fill: '#475569', fontWeight: 600 }} />
                <Tooltip cursor={{ fill: '#f8fafc' }} contentStyle={{ borderRadius: '6px', border: '1px solid #cbd5e1' }} />
                <Bar dataKey="count" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white p-6 rounded-md border border-gray-300 shadow-sm h-80 flex flex-col">
          <h3 className="text-sm font-bold text-gray-700 uppercase mb-4 tracking-wide border-b border-gray-100 pb-2">Evidence Source Agreement</h3>
          <div className="flex-1 min-h-0">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={agreementData} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={70} outerRadius={100} label={{ fill: '#334155', fontSize: 12, fontWeight: 600 }}>
                  {agreementData.map((entry, index) => <Cell key={`cell-${index}`} fill={entry.fill} />)}
                </Pie>
                <Tooltip contentStyle={{ borderRadius: '6px', border: '1px solid #cbd5e1' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white p-6 rounded-md border border-gray-300 shadow-sm h-80 flex flex-col">
          <h3 className="text-sm font-bold text-gray-700 uppercase mb-4 tracking-wide border-b border-gray-100 pb-2">Confidence Score Distribution</h3>
          <div className="flex-1 min-h-0">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={confData} margin={{ left: -10, right: 20, top: 10, bottom: 10 }}>
                <XAxis dataKey="name" tick={{ fontSize: 12, fill: '#475569', fontWeight: 600 }} />
                <YAxis />
                <Tooltip cursor={{ fill: '#f8fafc' }} contentStyle={{ borderRadius: '6px', border: '1px solid #cbd5e1' }} />
                <Bar dataKey="count" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white p-6 rounded-md border border-gray-300 shadow-sm h-80 flex flex-col">
          <h3 className="text-sm font-bold text-gray-700 uppercase mb-4 tracking-wide border-b border-gray-100 pb-2">Impact Score Distribution</h3>
          <div className="flex-1 min-h-0">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={impactScores} margin={{ left: -10, right: 20, top: 10, bottom: 10 }}>
                <XAxis dataKey="name" tick={false} />
                <YAxis domain={[0, 100]} />
                <Tooltip cursor={{ fill: '#f8fafc' }} contentStyle={{ borderRadius: '6px', border: '1px solid #cbd5e1' }} />
                <Bar dataKey="impact" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
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
