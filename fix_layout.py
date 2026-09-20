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
  const [activeLayers, setActiveLayers] = useState(['Hydrology', 'Interventions (Check Dams)', 'Project Boundary']);
  const [baseMap, setBaseMap] = useState('Satellite');
  const [activeTab, setActiveTab] = useState('Overview');
  const [selectedYear, setSelectedYear] = useState('T4');
  const [compareYear, setCompareYear] = useState('T0');
  const [swipeMode, setSwipeMode] = useState(false);
  const [clickedCell, setClickedCell] = useState(null);
  const [showSources, setShowSources] = useState(false);
  const [hideBanner, setHideBanner] = useState(false);

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
    <div className="h-screen w-full flex flex-col bg-[#f8fafc] text-slate-800 font-sans overflow-hidden">
      <TopNav metrics={metrics} demoMode={demoMode} setDemoMode={setDemoMode} setShowSources={setShowSources} />
      
      {/* Stat Cards Row */}
      <div className="bg-white border-b border-slate-200 px-6 py-3 flex gap-4 shrink-0 shadow-sm z-30 relative overflow-x-auto">
        <div className="flex-1 min-w-[180px] bg-white border border-slate-200 rounded-md p-3 flex items-center shadow-sm">
          <div className="bg-blue-100 text-blue-600 p-2 rounded-md mr-3">🗺️</div>
          <div><div className="text-xs font-bold text-slate-500 uppercase tracking-wide">Total Interventions</div><div className="text-xl font-extrabold text-slate-800">{interventions.length}</div></div>
        </div>
        <div className="flex-1 min-w-[180px] bg-white border border-slate-200 rounded-md p-3 flex items-center shadow-sm">
          <div className="bg-cyan-100 text-cyan-600 p-2 rounded-md mr-3">💧</div>
          <div><div className="text-xs font-bold text-slate-500 uppercase tracking-wide">Check Dams</div><div className="text-xl font-extrabold text-slate-800">{interventions.filter(i=>i.type==='Check Dam').length}</div></div>
        </div>
        <div className="flex-1 min-w-[180px] bg-white border border-slate-200 rounded-md p-3 flex items-center shadow-sm">
          <div className="bg-green-100 text-green-600 p-2 rounded-md mr-3">📷</div>
          <div><div className="text-xs font-bold text-slate-500 uppercase tracking-wide">Field Evidence</div><div className="text-xl font-extrabold text-slate-800">{interventions.filter(i=>!i.flag_missing_photo).length}</div></div>
        </div>
        <div className="flex-1 min-w-[180px] bg-white border border-slate-200 rounded-md p-3 flex items-center shadow-sm">
          <div className="bg-amber-100 text-amber-600 p-2 rounded-md mr-3">⚠</div>
          <div><div className="text-xs font-bold text-slate-500 uppercase tracking-wide">Needs Review</div><div className="text-xl font-extrabold text-slate-800">{interventions.filter(i=>i.status_badge==='REVIEW').length}</div></div>
        </div>
        <div className="flex-1 min-w-[180px] bg-white border border-slate-200 rounded-md p-3 flex items-center shadow-sm">
          <div className="bg-red-100 text-red-600 p-2 rounded-md mr-3">🚩</div>
          <div><div className="text-xs font-bold text-slate-500 uppercase tracking-wide">Flagged</div><div className="text-xl font-extrabold text-slate-800">{interventions.filter(i=>i.status_badge==='FLAGGED').length}</div></div>
        </div>
      </div>

      <main className="flex-1 flex overflow-hidden">
        <LeftSidebar 
          activeLayers={activeLayers}
          setActiveLayers={setActiveLayers}
          baseMap={baseMap}
          setBaseMap={setBaseMap}
          interventions={interventions}
          selectedId={selectedId}
          onSelect={setSelectedId}
        />
        
        <div className="flex-1 flex flex-col min-w-0 min-h-0 bg-slate-200 border-r border-slate-300 relative">
          
          {/* Map Toolbar (Normal Document Flow) */}
          <div className="bg-white border-b border-slate-300 px-4 py-3 shrink-0 flex items-center justify-center gap-6 shadow-sm z-20">
            <div className="flex items-center gap-3">
              <span className="text-xs font-bold text-slate-600 uppercase tracking-wider">Analysis: {selectedYear}</span>
              <input 
                type="range" min="0" max="4" step="1" 
                value={['T0', 'T1', 'T2', 'T3', 'T4'].indexOf(selectedYear)} 
                onChange={(e) => setSelectedYear(['T0', 'T1', 'T2', 'T3', 'T4'][e.target.value])} 
                className="w-32 accent-teal-600"
              />
            </div>
            <div className="w-px h-6 bg-slate-300"></div>
            <div className="flex items-center gap-3">
              <label className="flex items-center gap-2 text-xs font-bold text-slate-600 uppercase cursor-pointer">
                <input type="checkbox" checked={swipeMode} onChange={(e) => setSwipeMode(e.target.checked)} className="w-4 h-4 text-teal-600 rounded border-slate-300" />
                Swipe Compare
              </label>
              {swipeMode && (
                <select value={compareYear} onChange={(e) => setCompareYear(e.target.value)} className="bg-slate-100 border border-slate-300 rounded px-2 py-1 text-xs outline-none text-slate-700 font-bold">
                  <option value="T0">T0</option>
                  <option value="T1">T1</option>
                  <option value="T2">T2</option>
                  <option value="T3">T3</option>
                  <option value="T4">T4</option>
                </select>
              )}
            </div>
          </div>

          <div className="flex-1 relative min-h-0 min-w-0 z-10">
            {!demoMode && interventions.every(i => !i.lat) && !hideBanner && (
              <div className="absolute top-4 left-4 right-4 z-[2000] flex flex-col items-start bg-slate-900/90 backdrop-blur-sm text-white p-5 rounded-xl border border-slate-700 shadow-2xl max-w-lg">
                <div className="flex justify-between w-full items-start mb-2">
                  <div className="text-lg font-black tracking-tight">Spatial Data Unavailable</div>
                  <button onClick={() => setHideBanner(true)} className="text-slate-400 hover:text-white font-bold text-xl">×</button>
                </div>
                <div className="text-slate-300 text-sm leading-relaxed">
                  Official spatial coordinates for PUNE-WDC-1 interventions are pending ingestion. 
                  <br/>Toggle <strong className="text-amber-400">DEMO MODE</strong> in the top header to initialize prototype data.
                </div>
              </div>
            )}

            <MapViewer 
              interventions={demoMode ? interventions : interventions.filter(i => i.data_status === 'REAL')}
              selectedId={selectedId}
              onSelect={setSelectedId}
              baseMap={baseMap}
              activeLayers={activeLayers}
              demoMode={demoMode}
              selectedYear={selectedYear}
              compareYear={compareYear}
              swipeMode={swipeMode}
              setClickedCell={setClickedCell}
            />
          </div>

        </div>
        
        {selectedId ? (
          <RightPanel intervention={selectedInv} demoMode={demoMode} activeTab={activeTab} setActiveTab={setActiveTab} />
        ) : clickedCell ? (
          <div className="w-[420px] shrink-0 bg-white flex flex-col h-full shadow-2xl z-20">
            <div className="p-5 bg-white border-b border-slate-200 shrink-0 relative">
              <h2 className="text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-1">Cell Analysis</h2>
              <div className="text-2xl font-black text-slate-800 leading-tight">Zone #{clickedCell.properties.cell_id}</div>
              <div className="text-sm text-slate-500 font-medium">Monitoring Period: {selectedYear}</div>
            </div>
            <div className="flex-1 p-5 overflow-y-auto bg-slate-50">
              <div className="bg-white border border-slate-200 shadow-sm rounded-lg p-5 mb-4">
                <div className="text-xs font-bold text-slate-500 mb-2 uppercase tracking-wide">Classification</div>
                <div className={`text-sm font-extrabold px-3 py-2 rounded-md ${
                  clickedCell.properties.years[selectedYear.replace('T', '202')]?.changeClass === 'severe_degradation' ? 'bg-red-50 text-red-700 border-red-200' :
                  clickedCell.properties.years[selectedYear.replace('T', '202')]?.changeClass === 'moderate_degradation' ? 'bg-orange-50 text-orange-700 border-orange-200' :
                  clickedCell.properties.years[selectedYear.replace('T', '202')]?.changeClass === 'improving' ? 'bg-green-50 text-green-700 border-green-200' :
                  clickedCell.properties.years[selectedYear.replace('T', '202')]?.changeClass === 'strong_improvement' ? 'bg-emerald-50 text-emerald-800 border-emerald-200' :
                  'bg-slate-100 text-slate-700 border-slate-200'
                } border`}>
                  {clickedCell.properties.years[selectedYear.replace('T', '202')]?.changeClass.replace('_', ' ').toUpperCase()}
                </div>
                <div className="text-sm text-slate-600 mt-3 font-medium leading-relaxed">
                  {clickedCell.properties.years[selectedYear.replace('T', '202')]?.reasonText}
                </div>
              </div>
            </div>
          </div>
        ) : null}
      </main>

      {showSources && <DataSourcesModal onClose={() => setShowSources(false)} />}
    </div>
  );
}

function DataSourcesModal({ onClose }) {
  return (
    <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-[3000] flex items-center justify-center">
      <div className="bg-white rounded-xl shadow-2xl w-[600px] max-h-[80vh] flex flex-col overflow-hidden border border-slate-200">
        <div className="px-6 py-4 border-b border-slate-200 bg-slate-50 flex justify-between items-center">
          <h2 className="text-lg font-extrabold text-slate-800">Data Sources & Citations</h2>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-700 text-xl font-bold">×</button>
        </div>
        <div className="p-6 overflow-y-auto">
          <div className="mb-6">
            <h3 className="text-sm font-bold text-slate-800 uppercase tracking-widest mb-3 border-b border-slate-100 pb-2">Real / Computed Data</h3>
            <ul className="text-sm text-slate-600 flex flex-col gap-3">
              <li><strong>Administrative Boundary:</strong> OpenStreetMap Overpass API (Pune District).</li>
              <li><strong>Terrain & Hydrology:</strong> SRTM 30m Digital Elevation Model. Stream network computed via <code>pysheds</code> (Flow Direction & Accumulation).</li>
              <li><strong>Government References:</strong> Bhuvan WDC 2.0 / SRISHTI portal (<a href="https://bhuvan-app1.nrsc.gov.in/iwmp/" target="_blank" rel="noreferrer" className="text-teal-600 hover:underline">bhuvan-app1.nrsc.gov.in/iwmp/</a>). System designed to scale with ~17 lakh Drishti geotags and ~30,000 satellite images hosted by NRSC.</li>
            </ul>
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-800 uppercase tracking-widest mb-3 border-b border-slate-100 pb-2">Demo Mode / Synthetic Data</h3>
            <ul className="text-sm text-slate-600 flex flex-col gap-3">
              <li><strong>Analysis Grids:</strong> Multi-year (T0-T4) SAVI, MNDWI, and SCI thematic maps are generated proxy values mirroring typical degradation/improvement distributions for the prototype.</li>
              <li><strong>Scoring:</strong> Impact and Confidence scores are deterministic derived metrics for demonstration of the Evidence Engine.</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
""",
    "frontend/src/components/TopNav.tsx": """import React, { useState, useRef, useEffect } from 'react';

export default function TopNav({ metrics, demoMode, setDemoMode, setShowSources }) {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);
  
  useEffect(() => {
    const handleClick = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) setDropdownOpen(false);
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  const generateReport = () => {
    alert("GENERATING REPORT:\\n\\n1. Executive Summary\\n2. Study Area (Pune-WDC-1)\\n3. Satellite & Ancillary Data (Drishti status)\\n4. Site-wise Changes (T0-T4)\\n5. Conclusions");
  };

  return (
    <header className="bg-[#0f172a] text-white flex items-center justify-between px-6 py-3 shrink-0 shadow-md relative z-40 gap-4 overflow-visible">
      <div className="flex items-center gap-4 shrink-0">
        <div className="font-black text-xl tracking-tight text-white flex items-center gap-2">
          <span className="text-teal-400">💧</span> WDC-PMKSY
        </div>
        <div className="h-5 w-px bg-slate-700"></div>
        <div className="text-sm font-bold text-slate-300 tracking-wide">PUNE-WDC-1</div>
      </div>

      <div className="flex-1 flex justify-center min-w-[200px] max-w-md shrink">
        <div className="relative w-full">
          <input type="text" placeholder="Search work codes..." className="w-full bg-slate-800 text-slate-200 border border-slate-700 rounded-full px-4 py-1.5 text-sm focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500" />
          <span className="absolute right-3 top-1.5 text-slate-400">🔍</span>
        </div>
      </div>

      <div className="flex items-center gap-4 shrink-0">
        <div className="hidden md:flex items-center gap-4">
          <button onClick={() => setShowSources(true)} className="text-xs font-bold text-slate-300 hover:text-white uppercase tracking-wider">
            Data Sources
          </button>
          <button onClick={generateReport} className="bg-teal-600 hover:bg-teal-500 text-white text-xs font-bold uppercase tracking-wider px-4 py-2 rounded shadow transition-colors flex items-center gap-2">
            <span>📄</span> Generate Report
          </button>
        </div>
        
        <div className="md:hidden relative" ref={dropdownRef}>
          <button onClick={() => setDropdownOpen(!dropdownOpen)} className="text-slate-300 hover:text-white px-2 py-1 bg-slate-800 rounded">
            ⋮
          </button>
          {dropdownOpen && (
            <div className="absolute right-0 top-10 w-48 bg-white text-slate-800 rounded-md shadow-lg border border-slate-200 flex flex-col p-2 z-[2000]">
              <button onClick={() => { setShowSources(true); setDropdownOpen(false); }} className="text-left px-3 py-2 text-sm font-bold hover:bg-slate-100 rounded">Data Sources</button>
              <button onClick={() => { generateReport(); setDropdownOpen(false); }} className="text-left px-3 py-2 text-sm font-bold text-teal-600 hover:bg-teal-50 rounded">Generate Report</button>
            </div>
          )}
        </div>

        <label className="flex items-center gap-2 text-xs font-bold bg-slate-800 px-3 py-1.5 rounded-full border border-slate-700 cursor-pointer whitespace-nowrap">
          <span className={demoMode ? "text-amber-400" : "text-slate-400"}>DEMO MODE</span>
          <input type="checkbox" checked={demoMode} onChange={(e) => setDemoMode(e.target.checked)} className="accent-amber-500 w-3 h-3" />
        </label>
        <div className="w-8 h-8 rounded-full bg-teal-800 flex items-center justify-center text-sm font-bold border border-teal-600 shadow-inner shrink-0">NR</div>
      </div>
    </header>
  );
}
""",
    "frontend/src/components/LeftSidebar.tsx": """import React from 'react';

export default function LeftSidebar({ activeLayers, setActiveLayers, baseMap, setBaseMap, interventions, selectedId, onSelect }) {
  const toggleLayer = (layer) => {
    if (activeLayers.includes(layer)) setActiveLayers(activeLayers.filter(l => l !== layer));
    else setActiveLayers([...activeLayers, layer]);
  };

  const LayerCheckbox = ({ label }) => (
    <label className="flex items-center gap-2 text-sm cursor-pointer hover:bg-slate-50 p-1.5 rounded-md transition-colors text-slate-700 font-medium w-full">
      <input type="checkbox" checked={activeLayers.includes(label)} onChange={() => toggleLayer(label)} className="w-4 h-4 text-teal-600 rounded border-slate-300 focus:ring-teal-500" />
      {label}
    </label>
  );

  const sorted = [...interventions].sort((a, b) => {
    const order = { 'FLAGGED': 1, 'REVIEW': 2, 'VERIFIED': 3 };
    if (order[a.status_badge] !== order[b.status_badge]) return order[a.status_badge] - order[b.status_badge];
    return (b.score_confidence || 0) - (a.score_confidence || 0); // Sort by descending confidence as requested
  });

  return (
    <div className="w-[300px] shrink-0 bg-white flex flex-col h-full shadow-md z-20 border-r border-slate-200">
      
      {/* Top half: Filters */}
      <div className="flex-1 flex flex-col min-h-0">
        <div className="p-4 border-b border-slate-200 shrink-0 bg-slate-50">
          <h2 className="text-xs font-extrabold tracking-widest text-slate-800 uppercase">Map Layers</h2>
        </div>
        
        <div className="flex-1 p-4 flex flex-col gap-5 overflow-y-auto">
          <div>
            <div className="text-[11px] uppercase text-slate-500 font-bold mb-2 tracking-wide">Base Map</div>
            <select 
              value={baseMap} 
              onChange={e => setBaseMap(e.target.value)} 
              className="w-full bg-slate-50 border border-slate-200 rounded-md px-3 py-1.5 text-sm text-slate-800 outline-none focus:border-teal-500 shadow-sm font-medium"
            >
              <option>Satellite</option>
              <option>Terrain</option>
              <option>Street</option>
            </select>
          </div>

          <div>
            <div className="text-[11px] uppercase text-slate-500 font-bold mb-1 tracking-wide">Hydrology</div>
            <div className="flex flex-col gap-0.5 border border-slate-100 p-1 rounded">
              <LayerCheckbox label="Project Boundary" />
              <LayerCheckbox label="Hydrology" />
            </div>
          </div>
          
          <div>
            <div className="text-[11px] uppercase text-slate-500 font-bold mb-1 tracking-wide">Analytical Overlays</div>
            <div className="flex flex-col gap-0.5 border border-slate-100 p-1 rounded">
              <LayerCheckbox label="Integrated Change Index (SCI)" />
              <LayerCheckbox label="Vegetation (SAVI)" />
              <LayerCheckbox label="Water Conservation (MNDWI)" />
            </div>
          </div>
        </div>
      </div>

      {/* Bottom half: Queue */}
      <div className="flex-1 flex flex-col min-h-0 border-t border-slate-300">
        <div className="p-4 border-b border-slate-200 shrink-0 bg-slate-50">
          <h2 className="text-xs font-extrabold tracking-widest text-slate-800 uppercase">Intervention Queue</h2>
        </div>
        <div className="flex-1 overflow-y-auto">
          {sorted.map(inv => (
            <div 
              key={inv.id} 
              onClick={() => onSelect(inv.id)}
              className={`p-4 border-b border-slate-100 cursor-pointer transition-colors ${selectedId === inv.id ? 'bg-blue-50/60' : 'hover:bg-slate-50'}`}
            >
              <div className="flex justify-between items-start mb-1">
                <div className="font-bold text-slate-800 text-sm">{inv.work_code}</div>
                <div className={`text-[10px] font-extrabold px-1.5 py-0.5 rounded shadow-sm border ${inv.status_badge === 'REVIEW' ? 'bg-amber-100 text-amber-800 border-amber-300' : inv.status_badge === 'FLAGGED' ? 'bg-red-100 text-red-800 border-red-300' : 'bg-green-100 text-green-800 border-green-300'}`}>
                  {inv.status_badge}
                </div>
              </div>
              <div className="text-xs text-slate-500 font-medium">{inv.type}</div>
              <div className="text-[11px] text-slate-400 mt-2 truncate">{inv.priority_reason}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
""",
    "frontend/src/components/MapViewer.tsx": """import React, { useEffect, useState, useRef } from 'react';
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
      const div = L.DomUtil.create('div', 'bg-white/95 backdrop-blur-sm p-4 border border-slate-200 rounded-xl shadow-lg z-[1000] text-xs font-sans m-4');
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
    axios.get('/watershed_real.geojson').then(res => setWatershedData(res.data)).catch(()=>{});
    axios.get('/real_streams.geojson').then(res => setStreamData(res.data)).catch(()=>{});
    axios.get('/change_grid.geojson').then(res => setGridData(res.data)).catch(()=>{});
  }, []);

  const getBaseUrl = () => {
    switch (baseMap) {
      case 'Terrain': return 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png';
      case 'Street': return 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
      case 'Satellite': default: return 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
    }
  };

  const mapYear = (tLabel) => tLabel.replace('T', '202');

  const styleCell = (feature, tLabel) => {
    const yearStr = mapYear(tLabel);
    const data = feature.properties.years[yearStr];
    let color = data ? getColor(data.changeClass) : 'transparent';
    return {
      fillColor: color,
      weight: 0,
      opacity: 0, 
      fillOpacity: 1 
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
      
      layer.getContainer = () => map.getPane(paneName);
      
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
    <div className="w-full h-full relative">
      <InjectSmoothingCSS />
      <MapContainer 
        center={[18.85, 73.85]} 
        zoom={13} 
        style={{ height: '100%', width: '100%', background: '#e2e8f0', zIndex: 0 }} 
        zoomControl={true}
        ref={mapRef}
      >
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
    </div>
  );
}
""",
    "frontend/src/components/RightPanel.tsx": """import React from 'react';

export default function RightPanel({ intervention, demoMode, activeTab, setActiveTab }) {
  if (!intervention) return null;

  return (
    <div className="w-[420px] shrink-0 bg-[#f8fafc] flex flex-col h-full shadow-2xl z-20 border-l border-slate-300">
      <div className="p-5 bg-white border-b border-slate-200 shrink-0">
        <h2 className="text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-1">Intervention Inspector</h2>
        <div className="text-2xl font-black text-slate-800 leading-tight mb-2">{intervention.type}</div>
        <div className="text-sm text-slate-500 font-medium mb-4">{intervention.work_code}</div>
        
        <div className="flex flex-col gap-3">
          <div className="flex items-start">
            <span className={`text-xs font-extrabold px-2.5 py-1 rounded shadow-sm border ${intervention.status_badge === 'REVIEW' ? 'bg-amber-50 text-amber-800 border-amber-300' : intervention.status_badge === 'FLAGGED' ? 'bg-red-50 text-red-800 border-red-300' : 'bg-emerald-50 text-emerald-800 border-emerald-300'}`}>
              {intervention.status_badge}
            </span>
          </div>
          <div className="flex items-start">
            <span className="text-xs text-slate-600 font-bold bg-slate-100 px-2 py-1 rounded-md border border-slate-200">
              {intervention.lat ? `${intervention.lat.toFixed(6)}, ${intervention.lng.toFixed(6)}` : 'Coords Unavailable'}
            </span>
          </div>
        </div>
      </div>

      <div className="flex bg-white border-b border-slate-200 text-xs font-extrabold text-slate-500 shrink-0 tracking-wider overflow-x-auto">
        {['Overview', 'Evidence', 'Change', 'Flags'].map(tab => (
          <button 
            key={tab}
            className={`flex-1 text-center py-3 min-w-[80px] transition-colors ${activeTab === tab ? 'text-teal-600 border-b-2 border-teal-600 bg-teal-50/30' : 'hover:text-slate-800 hover:bg-slate-50'}`} 
            onClick={() => setActiveTab(tab)}
          >
            {tab.toUpperCase()}
          </button>
        ))}
      </div>

      <div className="flex-1 overflow-y-auto p-5 flex flex-col gap-4">
        {activeTab === 'Overview' && (
          <div className="bg-white border border-slate-200 shadow-sm rounded-xl p-5 relative">
            {intervention.data_status === 'DEMO' && demoMode && <span className="absolute -top-2 -right-2 bg-amber-500 text-[10px] font-bold px-2 py-0.5 rounded-full text-white shadow">DEMO</span>}
            <div className="flex justify-between items-center mb-5">
              <div className="text-center flex-1 border-r border-slate-100">
                <div className="text-xs text-slate-400 font-extrabold tracking-widest mb-1">IMPACT SCORE</div>
                <div className="text-4xl font-black text-blue-600">{intervention.score_impact || '--'}</div>
              </div>
              <div className="text-center flex-1">
                <div className="text-xs text-slate-400 font-extrabold tracking-widest mb-1">CONFIDENCE</div>
                <div className="text-4xl font-black text-slate-800">{intervention.score_confidence || '--'}</div>
              </div>
            </div>
            <div className="text-sm text-slate-700 bg-slate-50 p-4 rounded-lg border border-slate-100 font-medium leading-relaxed">
              {intervention.priority_reason}
            </div>
          </div>
        )}

        {activeTab === 'Evidence' && (
          <div className="bg-white border border-slate-200 shadow-sm rounded-xl p-5">
            <h3 className="text-xs font-extrabold text-slate-800 mb-3 uppercase tracking-widest border-b border-slate-100 pb-2">Drishti Field Photo</h3>
            <div className="h-48 bg-slate-100 border border-slate-300 rounded-lg flex items-center justify-center text-sm text-slate-500 font-medium shadow-inner overflow-hidden">
              📷 Proxy Geotagged Photo
            </div>
          </div>
        )}
        
        {activeTab === 'Change' && (
          <div className="bg-white border border-slate-200 shadow-sm rounded-xl p-5">
            <h3 className="text-xs font-extrabold text-slate-800 mb-3 uppercase tracking-widest border-b border-slate-100 pb-2">Temporal Changes (T0 - T4)</h3>
            <div className="flex flex-col gap-4 mt-4">
              <div className="flex justify-between items-center">
                <span className="text-sm font-bold text-slate-600">Water Spread</span>
                <span className="text-lg font-black text-blue-600">{intervention.water_spread_change > 0 ? '+' : ''}{intervention.water_spread_change}%</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm font-bold text-slate-600">Vegetation (SAVI)</span>
                <span className="text-lg font-black text-green-600">{intervention.ndvi_change > 0 ? '+' : ''}{intervention.ndvi_change}</span>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'Flags' && (
          <div className="flex flex-col gap-4">
            {intervention.flag_conflict && (
              <div className="bg-red-50 border border-red-200 p-5 rounded-xl shadow-sm">
                <div className="flex items-center gap-2 text-red-700 font-bold mb-2 uppercase text-xs tracking-widest">⚠ Field/Satellite Conflict</div>
                <div className="text-sm text-red-900 font-medium">Field evidence and satellite evidence disagree. On-site verification recommended.</div>
              </div>
            )}
            {!intervention.flag_conflict && (
              <div className="text-sm font-bold text-slate-500 p-6 border-2 border-slate-200 border-dashed rounded-xl text-center bg-white">
                No critical red flags detected.
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
"""
}

def write_files():
    for fpath, content in frontend_files.items():
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    write_files()
