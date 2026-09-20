import os

frontend_files = {
    "frontend/src/App.tsx": """import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MapViewer from './components/MapViewer';
import LeftSidebar from './components/LeftSidebar';
import RightPanel from './components/RightPanel';
import TopNav from './components/TopNav';
import InterventionTable from './components/InterventionTable';

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
      <div className="bg-white border-b border-slate-200 px-6 py-3 flex gap-4 shrink-0 shadow-sm z-30 relative">
        <div className="flex-1 bg-white border border-slate-200 rounded-md p-3 flex items-center shadow-sm">
          <div className="bg-blue-100 text-blue-600 p-2 rounded-md mr-3">🗺️</div>
          <div><div className="text-xs font-bold text-slate-500 uppercase tracking-wide">Total Interventions</div><div className="text-xl font-extrabold text-slate-800">{interventions.length}</div></div>
        </div>
        <div className="flex-1 bg-white border border-slate-200 rounded-md p-3 flex items-center shadow-sm">
          <div className="bg-cyan-100 text-cyan-600 p-2 rounded-md mr-3">💧</div>
          <div><div className="text-xs font-bold text-slate-500 uppercase tracking-wide">Check Dams</div><div className="text-xl font-extrabold text-slate-800">{interventions.filter(i=>i.type==='Check Dam').length}</div></div>
        </div>
        <div className="flex-1 bg-white border border-slate-200 rounded-md p-3 flex items-center shadow-sm">
          <div className="bg-green-100 text-green-600 p-2 rounded-md mr-3">📷</div>
          <div><div className="text-xs font-bold text-slate-500 uppercase tracking-wide">Field Evidence</div><div className="text-xl font-extrabold text-slate-800">{interventions.filter(i=>!i.flag_missing_photo).length}</div></div>
        </div>
        <div className="flex-1 bg-white border border-slate-200 rounded-md p-3 flex items-center shadow-sm">
          <div className="bg-amber-100 text-amber-600 p-2 rounded-md mr-3">⚠</div>
          <div><div className="text-xs font-bold text-slate-500 uppercase tracking-wide">Needs Review</div><div className="text-xl font-extrabold text-slate-800">{interventions.filter(i=>i.status_badge==='REVIEW').length}</div></div>
        </div>
        <div className="flex-1 bg-white border border-slate-200 rounded-md p-3 flex items-center shadow-sm">
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
        />
        
        <div className="flex-1 relative flex flex-col min-w-0 min-h-0 z-10 bg-slate-200">
          {/* Map Toolbar Overlay */}
          <div className="absolute top-4 left-1/2 -translate-x-1/2 bg-white/95 backdrop-blur border border-slate-300 px-4 py-2 rounded-full shadow-lg z-[1000] flex items-center gap-6">
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
          
          <div className="h-[30vh] shrink-0 border-t border-slate-300 bg-white relative z-[1000] flex flex-col">
            <div className="bg-slate-50 border-b border-slate-200 px-4 py-2 flex items-center justify-between shrink-0">
              <h2 className="text-xs font-extrabold text-slate-700 uppercase tracking-widest">Intervention Queue</h2>
            </div>
            <div className="flex-1 overflow-auto">
              <InterventionTable interventions={interventions} selectedId={selectedId} onSelect={setSelectedId} />
            </div>
          </div>
        </div>
        
        {selectedId ? (
          <RightPanel intervention={selectedInv} demoMode={demoMode} activeTab={activeTab} setActiveTab={setActiveTab} />
        ) : clickedCell ? (
          <div className="w-[420px] shrink-0 bg-white flex flex-col h-full shadow-2xl z-20 border-l border-slate-300">
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
    <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-[2000] flex items-center justify-center">
      <div className="bg-white rounded-xl shadow-2xl w-[600px] max-h-[80vh] flex flex-col overflow-hidden border border-slate-200">
        <div className="px-6 py-4 border-b border-slate-200 bg-slate-50 flex justify-between items-center">
          <h2 className="text-lg font-extrabold text-slate-800">Data Sources & Citations</h2>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-700">✕</button>
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
    "frontend/src/components/TopNav.tsx": """import React from 'react';

export default function TopNav({ metrics, demoMode, setDemoMode, setShowSources }) {
  const generateReport = () => {
    alert("GENERATING REPORT:\\n\\n1. Executive Summary\\n2. Study Area (Pune-WDC-1)\\n3. Satellite & Ancillary Data (Drishti status)\\n4. Site-wise Changes (T0-T4)\\n5. Conclusions");
  };

  return (
    <header className="bg-[#0f172a] text-white flex items-center justify-between px-6 py-3 shrink-0 shadow-md relative z-40">
      <div className="flex items-center gap-4">
        <div className="font-black text-xl tracking-tight text-white flex items-center gap-2">
          <span className="text-teal-400">💧</span> WDC-PMKSY
        </div>
        <div className="h-5 w-px bg-slate-700"></div>
        <div className="text-sm font-bold text-slate-300 tracking-wide">PUNE-WDC-1</div>
      </div>

      <div className="flex-1 flex justify-center max-w-md mx-6">
        <div className="relative w-full">
          <input type="text" placeholder="Search work codes, villages..." className="w-full bg-slate-800 text-slate-200 border border-slate-700 rounded-full px-4 py-1.5 text-sm focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500" />
          <span className="absolute right-3 top-1.5 text-slate-400">🔍</span>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <button onClick={() => setShowSources(true)} className="text-xs font-bold text-slate-300 hover:text-white uppercase tracking-wider">
          Data Sources
        </button>
        <button onClick={generateReport} className="bg-teal-600 hover:bg-teal-500 text-white text-xs font-bold uppercase tracking-wider px-4 py-2 rounded shadow transition-colors flex items-center gap-2">
          <span>📄</span> Generate Report
        </button>
        <label className="flex items-center gap-2 text-xs font-bold bg-slate-800 px-3 py-1.5 rounded-full border border-slate-700 cursor-pointer">
          <span className={demoMode ? "text-amber-400" : "text-slate-400"}>DEMO MODE</span>
          <input type="checkbox" checked={demoMode} onChange={(e) => setDemoMode(e.target.checked)} className="accent-amber-500 w-3 h-3" />
        </label>
        <div className="w-8 h-8 rounded-full bg-teal-800 flex items-center justify-center text-sm font-bold border border-teal-600 shadow-inner">NR</div>
      </div>
    </header>
  );
}
""",
    "frontend/src/components/InterventionTable.tsx": """import React from 'react';

export default function InterventionTable({ interventions, selectedId, onSelect }) {
  const sorted = [...interventions].sort((a, b) => {
    const order = { 'FLAGGED': 1, 'REVIEW': 2, 'VERIFIED': 3 };
    if (order[a.status_badge] !== order[b.status_badge]) return order[a.status_badge] - order[b.status_badge];
    return (b.score_impact || 0) - (a.score_impact || 0);
  });

  return (
    <table className="w-full text-left border-collapse text-sm bg-white">
      <thead className="bg-slate-50 sticky top-0 z-10 shadow-sm border-b border-slate-200">
        <tr>
          <th className="px-4 py-2 font-bold text-slate-500 uppercase tracking-wider text-xs">Work Code</th>
          <th className="px-4 py-2 font-bold text-slate-500 uppercase tracking-wider text-xs">Type</th>
          <th className="px-4 py-2 font-bold text-slate-500 uppercase tracking-wider text-xs">Impact</th>
          <th className="px-4 py-2 font-bold text-slate-500 uppercase tracking-wider text-xs">Conf</th>
          <th className="px-4 py-2 font-bold text-slate-500 uppercase tracking-wider text-xs">Status</th>
          <th className="px-4 py-2 font-bold text-slate-500 uppercase tracking-wider text-xs">Reason</th>
        </tr>
      </thead>
      <tbody>
        {sorted.map(inv => (
          <tr 
            key={inv.id} 
            onClick={() => onSelect(inv.id)}
            className={`cursor-pointer transition-colors border-b border-slate-100 ${selectedId === inv.id ? 'bg-blue-50/60' : 'hover:bg-slate-50'}`}
          >
            <td className="px-4 py-2 font-bold text-slate-800">{inv.work_code}</td>
            <td className="px-4 py-2 text-slate-600 font-medium">{inv.type}</td>
            <td className="px-4 py-2 font-extrabold text-blue-600">{inv.score_impact || '--'}</td>
            <td className="px-4 py-2 font-extrabold text-slate-700">{inv.score_confidence || '--'}</td>
            <td className="px-4 py-2">
              <span className={`text-[10px] font-extrabold px-2 py-1 rounded shadow-sm border ${inv.status_badge === 'REVIEW' ? 'bg-amber-100 text-amber-800 border-amber-300' : inv.status_badge === 'FLAGGED' ? 'bg-red-100 text-red-800 border-red-300' : 'bg-green-100 text-green-800 border-green-300'}`}>
                {inv.status_badge}
              </span>
            </td>
            <td className="px-4 py-2 text-xs text-slate-600 font-medium truncate max-w-xs">{inv.priority_reason}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
""",
    "frontend/src/components/LeftSidebar.tsx": """import React from 'react';

export default function LeftSidebar({ activeLayers, setActiveLayers, baseMap, setBaseMap }) {
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

  return (
    <div className="w-[280px] shrink-0 bg-white flex flex-col h-full shadow-md z-20 border-r border-slate-200">
      <div className="p-5 border-b border-slate-200">
        <h2 className="text-xs font-extrabold tracking-widest text-slate-800 uppercase">Map Filters & Layers</h2>
      </div>
      
      <div className="flex-1 p-5 flex flex-col gap-6 overflow-y-auto">
        <div>
          <div className="text-xs uppercase text-slate-500 font-bold mb-2 tracking-wide">Base Map</div>
          <select 
            value={baseMap} 
            onChange={e => setBaseMap(e.target.value)} 
            className="w-full bg-slate-50 border border-slate-200 rounded-md px-3 py-2 text-sm text-slate-800 outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500 shadow-sm font-medium"
          >
            <option>Satellite</option>
            <option>Terrain</option>
            <option>Street</option>
          </select>
        </div>

        <div>
          <div className="text-xs uppercase text-slate-500 font-bold mb-2 tracking-wide">Context & Hydrology</div>
          <div className="flex flex-col gap-0.5 bg-slate-50 p-2 rounded-lg border border-slate-100">
            <LayerCheckbox label="Project Boundary" />
            <LayerCheckbox label="Hydrology" />
          </div>
        </div>

        <div>
          <div className="text-xs uppercase text-slate-500 font-bold mb-2 tracking-wide">Field Evidence</div>
          <div className="flex flex-col gap-0.5 bg-slate-50 p-2 rounded-lg border border-slate-100">
            <LayerCheckbox label="Interventions (Check Dams)" />
          </div>
        </div>
        
        <div>
          <div className="text-xs uppercase text-slate-500 font-bold mb-2 tracking-wide">Analytical Overlays (T0-T4)</div>
          <div className="flex flex-col gap-0.5 bg-slate-50 p-2 rounded-lg border border-slate-100">
            <LayerCheckbox label="Integrated Change Index (SCI)" />
            <LayerCheckbox label="Vegetation (SAVI)" />
            <LayerCheckbox label="Water Conservation (MNDWI)" />
          </div>
        </div>
      </div>
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
        <div className="text-2xl font-black text-slate-800 leading-tight">{intervention.type}</div>
        <div className="text-sm text-slate-500 font-medium mb-4">{intervention.work_code}</div>
        
        <div className="flex items-center gap-3">
          <div className={`text-xs font-extrabold px-2.5 py-1 rounded shadow-sm border ${intervention.status_badge === 'REVIEW' ? 'bg-amber-50 text-amber-800 border-amber-300' : intervention.status_badge === 'FLAGGED' ? 'bg-red-50 text-red-800 border-red-300' : 'bg-emerald-50 text-emerald-800 border-emerald-300'}`}>
            {intervention.status_badge}
          </div>
          <div className="text-xs text-slate-600 font-bold bg-slate-100 px-2 py-1 rounded-md border border-slate-200">
            {intervention.lat ? `${intervention.lat.toFixed(6)}, ${intervention.lng.toFixed(6)}` : 'Coords Unavailable'}
          </div>
        </div>
      </div>

      <div className="flex bg-white border-b border-slate-200 text-xs font-extrabold text-slate-500 shrink-0 tracking-wider">
        {['Overview', 'Evidence', 'Change', 'Flags'].map(tab => (
          <button 
            key={tab}
            className={`flex-1 text-center py-3 transition-colors ${activeTab === tab ? 'text-teal-600 border-b-2 border-teal-600 bg-teal-50/30' : 'hover:text-slate-800 hover:bg-slate-50'}`} 
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

def create_files():
    for path, content in frontend_files.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    create_files()
