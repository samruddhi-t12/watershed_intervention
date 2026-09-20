import os
import json

frontend_files = {
    "frontend/public/bounds.json": """{
  "bounds": [[18.80, 73.80], [18.90, 73.95]]
}""",
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
    <div className="h-screen w-full flex flex-col bg-slate-100 text-slate-800 font-sans overflow-hidden">
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
          <div className="flex-1 overflow-y-auto bg-slate-100 p-6">
            <AnalyticsDashboard interventions={demoMode ? interventions : interventions.filter(i => i.data_status === 'REAL')} demoMode={demoMode} />
          </div>
        ) : (
          <div className="flex-1 relative bg-slate-200 border-x border-slate-300">
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
    "frontend/src/components/TopNav.tsx": """import React from 'react';

export default function TopNav({ metrics, demoMode, setDemoMode, activeTab, setActiveTab }) {
  const TabButton = ({ label }) => (
    <button 
      className={`transition-colors ${activeTab === label ? 'text-white font-bold border-b-2 border-blue-500 pb-0.5' : 'text-slate-400 hover:text-white'}`}
      onClick={() => setActiveTab(label)}
    >
      {label}
    </button>
  );

  return (
    <header className="bg-slate-900 text-slate-100 flex flex-col shrink-0 shadow-md z-50">
      <div className="flex justify-between items-center px-5 py-3 border-b border-slate-700">
        <div className="font-bold tracking-wider text-sm flex items-center gap-3">
          <span className="text-blue-400">WATERSHED EVIDENCE ENGINE</span>
          <span className="text-slate-500 text-xs">|</span>
          <span className="text-slate-300 text-xs font-normal">Intervention-level geospatial monitoring</span>
        </div>
        <div className="text-sm font-semibold tracking-wide text-white">
          Maharashtra / Pune / PUNE-WDC-1 / 2021-22
        </div>
        <div className="text-xs flex items-center gap-4">
          <label className="flex items-center gap-2 cursor-pointer bg-slate-800 hover:bg-slate-700 transition-colors px-3 py-1.5 rounded border border-slate-600">
            <input type="checkbox" checked={demoMode} onChange={(e) => setDemoMode(e.target.checked)} className="cursor-pointer" />
            <span className={demoMode ? "text-yellow-400 font-bold" : "text-slate-300"}>DEMO MODE</span>
          </label>
          <span className="text-slate-400">Last Updated: Today</span>
          <span className="text-blue-300 font-medium">Officer Portal</span>
        </div>
      </div>
      
      {metrics && (
        <div className="flex justify-between items-center px-5 py-2 text-xs bg-slate-800 shadow-inner">
          <div className="flex gap-6 text-slate-300">
            <span>Total: <strong className="text-white bg-slate-700 px-1.5 py-0.5 rounded">{metrics.total}</strong></span>
            <span>Check Dams: <strong className="text-white bg-slate-700 px-1.5 py-0.5 rounded">{metrics.check_dams}</strong></span>
            <span>Field Evidence: <strong className="text-white bg-slate-700 px-1.5 py-0.5 rounded">{metrics.field_evidence}</strong></span>
            <span>Needs Review: <strong className="text-yellow-400 bg-yellow-900/40 px-1.5 py-0.5 rounded border border-yellow-700/50">{metrics.needs_review}</strong></span>
            <span>Verified: <strong className="text-green-400 bg-green-900/40 px-1.5 py-0.5 rounded border border-green-700/50">{metrics.verified}</strong></span>
            <span>Flagged: <strong className="text-red-400 bg-red-900/40 px-1.5 py-0.5 rounded border border-red-700/50">{metrics.flagged}</strong></span>
          </div>
          <div className="flex gap-5">
            <TabButton label="Overview" />
            <TabButton label="Interventions" />
            <TabButton label="Change Detection" />
            <TabButton label="Analytics" />
          </div>
        </div>
      )}
    </header>
  );
}
""",
    "frontend/src/components/LeftSidebar.tsx": """import React from 'react';

export default function LeftSidebar({ interventions, selectedId, onSelect, activeLayers, setActiveLayers, baseMap, setBaseMap, activeTab }) {
  
  const toggleLayer = (layer) => {
    if (activeLayers.includes(layer)) setActiveLayers(activeLayers.filter(l => l !== layer));
    else setActiveLayers([...activeLayers, layer]);
  };

  const LayerCheckbox = ({ label }) => (
    <label className="flex items-center gap-2 text-sm cursor-pointer hover:bg-slate-200 p-1 rounded transition-colors text-slate-700 font-medium">
      <input type="checkbox" checked={activeLayers.includes(label)} onChange={() => toggleLayer(label)} className="w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500" />
      {label}
    </label>
  );

  if (activeTab === 'Overview') {
    return (
      <div className="w-[320px] bg-slate-50 p-4 border-r border-slate-300">
        <h2 className="text-sm font-extrabold tracking-wide text-slate-800 uppercase mb-4">Project Overview</h2>
        <div className="text-sm text-slate-600">Select Interventions or Change Detection to view spatial data.</div>
      </div>
    );
  }

  if (activeTab === 'Change Detection') {
    return (
      <div className="w-[320px] bg-slate-50 flex flex-col h-full shadow-[4px_0_15px_-3px_rgba(0,0,0,0.1)] z-10 border-r border-slate-300">
        <div className="p-4 border-b border-slate-200 bg-white">
          <h2 className="text-sm font-extrabold tracking-wide text-slate-800 uppercase">Change Detection Layers</h2>
          <div className="text-xs text-slate-500 mt-1">Select analytical raster overlays</div>
        </div>
        
        <div className="flex-1 p-4 bg-white flex flex-col gap-4">
          <div>
            <div className="text-xs uppercase text-slate-500 font-bold mb-1.5">Basemap</div>
            <select 
              value={baseMap} 
              onChange={e => setBaseMap(e.target.value)} 
              className="w-full bg-slate-50 border border-slate-300 rounded px-2 py-1.5 text-sm text-slate-800 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
            >
              <option>Satellite</option>
              <option>Street</option>
              <option>Terrain</option>
            </select>
          </div>
          
          <div className="border-t border-slate-200 pt-4">
            <div className="text-xs uppercase text-slate-500 font-bold mb-2">Change Detection Maps</div>
            <div className="flex flex-col gap-2">
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

  // Interventions Tab
  return (
    <div className="w-[320px] bg-slate-50 flex flex-col h-full shadow-[4px_0_15px_-3px_rgba(0,0,0,0.1)] z-10 border-r border-slate-300">
      <div className="p-4 border-b border-slate-200 bg-white">
        <h2 className="text-sm font-extrabold tracking-wide text-slate-800 uppercase">Intervention Queue</h2>
        <input type="text" placeholder="Search work code..." className="w-full mt-3 bg-white border border-slate-300 rounded px-3 py-2 text-sm text-slate-800 placeholder-slate-400 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-shadow" />
      </div>
      
      <div className="flex-1 overflow-y-auto p-3 flex flex-col gap-3 custom-scrollbar bg-slate-50">
        {interventions.map(inv => (
          <div 
            key={inv.id} 
            className={`p-3 rounded-lg border transition-all cursor-pointer shadow-sm ${selectedId === inv.id ? 'bg-blue-50 border-blue-400 ring-1 ring-blue-400' : 'bg-white border-slate-200 hover:border-slate-400 hover:shadow-md'}`}
            onClick={() => onSelect(inv.id)}
          >
            <div className="flex justify-between items-start mb-2">
              <div>
                <div className="text-sm font-bold text-slate-900">{inv.type}</div>
                <div className="text-xs text-slate-500 font-medium">WC: {inv.work_code}</div>
              </div>
              <div className={`text-[10px] font-bold px-2 py-1 rounded shadow-sm ${inv.status_badge === 'REVIEW' ? 'bg-yellow-100 text-yellow-800 border border-yellow-300' : inv.status_badge === 'FLAGGED' ? 'bg-red-100 text-red-800 border border-red-300' : 'bg-green-100 text-green-800 border border-green-300'}`}>
                {inv.status_badge}
              </div>
            </div>
            {inv.data_status !== 'UNAVAILABLE' && inv.score_impact !== null ? (
              <div className="text-xs text-slate-600 mt-2 bg-slate-100 p-1.5 rounded">
                Impact: <span className="font-bold text-slate-900">{inv.score_impact}</span> <span className="mx-1 text-slate-400">|</span> Conf: <span className="font-bold text-slate-900">{inv.score_confidence}</span>
              </div>
            ) : (
              <div className="text-xs text-slate-500 mt-2 italic bg-slate-100 p-1.5 rounded">Data Unavailable</div>
            )}
            <div className="text-xs text-slate-600 mt-2 line-clamp-2 leading-relaxed">{inv.priority_reason}</div>
          </div>
        ))}
      </div>

      <div className="border-t border-slate-300 p-4 bg-white shadow-[0_-4px_10px_-5px_rgba(0,0,0,0.05)]">
        <h3 className="text-sm font-extrabold text-slate-800 mb-3 uppercase tracking-wide">Layer Control</h3>
        <div className="mb-4">
          <div className="text-xs uppercase text-slate-500 font-bold mb-1.5">Basemap</div>
          <select 
            value={baseMap} 
            onChange={e => setBaseMap(e.target.value)} 
            className="w-full bg-slate-50 border border-slate-300 rounded px-2 py-1.5 text-sm text-slate-800 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
          >
            <option>Satellite</option>
            <option>Street</option>
            <option>Terrain</option>
          </select>
        </div>
        <div className="grid grid-cols-2 gap-x-2 gap-y-4">
          <div>
            <div className="text-xs uppercase text-slate-500 font-bold mb-1">Context</div>
            <LayerCheckbox label="Project Boundary" />
            <LayerCheckbox label="Check Dams" />
          </div>
        </div>
      </div>
    </div>
  );
}
""",
    "frontend/src/components/MapViewer.tsx": """import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, ImageOverlay, Rectangle } from 'react-leaflet';
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

const MapController = ({ interventions, selectedId, bounds }) => {
  const map = useMap();
  useEffect(() => {
    if (selectedId) {
      const inv = interventions.find(i => i.id === selectedId);
      if (inv && inv.lat && inv.lng) {
        map.flyTo([inv.lat, inv.lng], 16);
      }
    } else if (bounds) {
      map.fitBounds(bounds);
    }
  }, [selectedId, interventions, map, bounds]);
  return null;
};

// Generates placeholder transparent SVGs inline if real PNGs aren't available
const generatePlaceholderSVG = (color, text) => {
  return `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 100 100" preserveAspectRatio="none"><rect width="100" height="100" fill="${color}" fill-opacity="0.4" /><text x="50" y="50" font-family="sans-serif" font-size="10" text-anchor="middle" alignment-baseline="middle" fill="white" opacity="0.8">${text}</text></svg>`;
};

const mapLayersSource = {
  'Land Use / Degradation': generatePlaceholderSVG('orange', 'LULC Degradation'),
  'Drainage Change': generatePlaceholderSVG('blue', 'Drainage Change'),
  'Vegetation (SAVI)': generatePlaceholderSVG('green', 'SAVI Gradient'),
  'Water Conservation (MNDWI)': generatePlaceholderSVG('cyan', 'MNDWI Water'),
  'Integrated Change Index (SCI)': generatePlaceholderSVG('purple', 'Integrated Change Index')
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
    <div className="h-full w-full relative">
      {!demoMode && interventions.every(i => !i.lat) && activeTab === 'Interventions' && (
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
        <MapController interventions={interventions} selectedId={selectedId} bounds={bounds} />

        {/* Change Detection Raster Overlays */}
        {activeTab === 'Change Detection' && activeAnalyticalLayers.map(layerName => (
          <ImageOverlay key={layerName} url={mapLayersSource[layerName]} bounds={bounds} opacity={0.7} />
        ))}

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
      
      {/* Legend overlay for Change Detection */}
      {activeTab === 'Change Detection' && activeAnalyticalLayers.length > 0 && (
        <div className="absolute bottom-6 right-6 bg-white p-3 border-2 border-slate-800 rounded shadow-lg z-[1000]">
          {activeAnalyticalLayers.map(layer => (
            <div key={layer} className="mb-2 last:mb-0 text-xs font-bold text-slate-800 uppercase tracking-tight">
              <div className="mb-1">{layer}</div>
              <div className={`h-2 w-32 rounded mb-1 bg-gradient-to-r ${
                layer.includes('Degradation') ? 'from-green-500 via-yellow-500 to-red-500' :
                layer.includes('Drainage') ? 'from-blue-200 to-blue-700' :
                layer.includes('SAVI') ? 'from-yellow-200 to-green-700' :
                layer.includes('MNDWI') ? 'from-cyan-100 to-cyan-700' :
                'from-red-500 via-slate-200 to-green-500'
              }`} />
              <div className="flex justify-between text-[9px] text-slate-500 uppercase">
                <span>Low</span><span>High</span>
              </div>
            </div>
          ))}
          <div className="mt-2 text-[10px] font-bold text-yellow-600 bg-yellow-100 px-1 py-0.5 rounded inline-block">DEMO MODE</div>
        </div>
      )}

      {/* Map Tools Overlay */}
      <div className="absolute top-4 right-4 z-[1000] flex flex-col gap-2">
        <button className="w-8 h-8 bg-white border border-slate-300 text-slate-700 rounded shadow flex items-center justify-center hover:bg-slate-50 font-bold">+</button>
        <button className="w-8 h-8 bg-white border border-slate-300 text-slate-700 rounded shadow flex items-center justify-center hover:bg-slate-50 font-bold">-</button>
        <button className="w-8 h-8 bg-white border border-slate-300 text-slate-700 rounded shadow flex items-center justify-center hover:bg-slate-50" title="Measure">📏</button>
        <button className="w-8 h-8 bg-white border border-slate-300 text-slate-700 rounded shadow flex items-center justify-center hover:bg-slate-50" title="Fullscreen">⛶</button>
      </div>
    </div>
  );
}
""",
    "frontend/src/components/AnalyticsDashboard.tsx": """import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Histogram } from 'recharts';

export default function AnalyticsDashboard({ interventions, demoMode }) {
  const p1 = interventions.filter(i => i.priority === 'P1').length;
  const p2 = interventions.filter(i => i.priority === 'P2').length;
  const p3 = interventions.filter(i => i.priority === 'P3').length;

  const priorityData = [
    { name: 'P1 (Critical)', count: p1, fill: '#ef4444' },
    { name: 'P2 (Review)', count: p2, fill: '#f59e0b' },
    { name: 'P3 (Verified)', count: p3, fill: '#10b981' }
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
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-extrabold text-slate-800 uppercase">Analytics Dashboard</h2>
          <p className="text-sm text-slate-500 font-medium">Aggregated insights for PUNE-WDC-1</p>
        </div>
        {demoMode && <div className="bg-yellow-100 text-yellow-800 border border-yellow-300 font-bold px-3 py-1 rounded shadow-sm text-sm">DEMO MODE ACTIVE</div>}
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm h-72">
          <h3 className="text-sm font-bold text-slate-600 uppercase mb-4">Priority Queue Distribution</h3>
          <ResponsiveContainer width="100%" height="85%">
            <BarChart data={priorityData} layout="vertical" margin={{ left: 20, right: 20 }}>
              <XAxis type="number" />
              <YAxis dataKey="name" type="category" width={100} tick={{ fontSize: 12, fill: '#64748b' }} />
              <Tooltip cursor={{ fill: '#f1f5f9' }} />
              <Bar dataKey="count" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm h-72">
          <h3 className="text-sm font-bold text-slate-600 uppercase mb-4">Evidence Source Agreement</h3>
          <ResponsiveContainer width="100%" height="85%">
            <PieChart>
              <Pie data={agreementData} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={60} outerRadius={80} label>
                {agreementData.map((entry, index) => <Cell key={`cell-${index}`} fill={entry.fill} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm h-72">
          <h3 className="text-sm font-bold text-slate-600 uppercase mb-4">Confidence Score Distribution</h3>
          <ResponsiveContainer width="100%" height="85%">
            <BarChart data={confData} margin={{ left: -20, right: 20 }}>
              <XAxis dataKey="name" tick={{ fontSize: 12, fill: '#64748b' }} />
              <YAxis />
              <Tooltip cursor={{ fill: '#f1f5f9' }} />
              <Bar dataKey="count" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm h-72">
          <h3 className="text-sm font-bold text-slate-600 uppercase mb-4">Impact Score Distribution</h3>
          <ResponsiveContainer width="100%" height="85%">
            <BarChart data={impactScores} margin={{ left: -20, right: 20 }}>
              <XAxis dataKey="name" tick={false} />
              <YAxis domain={[0, 100]} />
              <Tooltip cursor={{ fill: '#f1f5f9' }} />
              <Bar dataKey="impact" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
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
