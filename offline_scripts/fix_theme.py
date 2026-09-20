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
    <div className="h-screen w-full flex flex-col bg-slate-100 text-slate-800 font-sans overflow-hidden">
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
        <div className="flex-1 relative bg-slate-200 border-x border-slate-300">
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
            <button className="text-slate-400 hover:text-white transition-colors">Overview</button>
            <button className="text-white font-bold border-b-2 border-blue-500 pb-0.5">Interventions</button>
            <button className="text-slate-400 hover:text-white transition-colors">Change Detection</button>
            <button className="text-slate-400 hover:text-white transition-colors">Analytics</button>
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
    <label className="flex items-center gap-2 text-sm cursor-pointer hover:bg-slate-200 p-1 rounded transition-colors text-slate-700">
      <input type="checkbox" checked={activeLayers.includes(label)} onChange={() => toggleLayer(label)} className="w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500" />
      {label}
    </label>
  );

  return (
    <div className="w-[320px] bg-slate-50 flex flex-col h-full shadow-[4px_0_15px_-3px_rgba(0,0,0,0.1)] z-10">
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
          <div>
            <div className="text-xs uppercase text-slate-500 font-bold mb-1">Analytics</div>
            <LayerCheckbox label="Water Change" />
            <LayerCheckbox label="Veg. Change" />
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
    <div className="w-[400px] bg-slate-50 flex flex-col h-full shadow-[-4px_0_15px_-3px_rgba(0,0,0,0.1)] z-10">
      <div className="p-5 bg-white border-b border-slate-200 shrink-0">
        <h2 className="text-xs font-extrabold text-slate-500 uppercase tracking-wider mb-1">Intervention Evidence</h2>
        <div className="text-xl font-bold text-slate-900 leading-tight">{intervention.type}</div>
        <div className="text-sm text-slate-500 font-medium mb-3">Work Code: {intervention.work_code}</div>
        
        <div className="flex items-center justify-between">
          <div className={`text-xs font-bold px-2.5 py-1 rounded shadow-sm border ${intervention.status_badge === 'REVIEW' ? 'bg-yellow-100 text-yellow-800 border-yellow-300' : intervention.status_badge === 'FLAGGED' ? 'bg-red-100 text-red-800 border-red-300' : 'bg-green-100 text-green-800 border-green-300'}`}>
            {intervention.status_badge}
          </div>
          <div className="text-xs text-slate-500 font-medium bg-slate-100 px-2 py-1 rounded">
            {intervention.lat ? `${intervention.lat.toFixed(6)}, ${intervention.lng.toFixed(6)}` : 'Coordinates unavailable'}
          </div>
        </div>
      </div>

      <div className="flex bg-white border-b border-slate-200 text-sm font-bold text-slate-500">
        <button className={`flex-1 text-center py-3 transition-colors ${tab === 'EVIDENCE' ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50/30' : 'hover:text-slate-800 hover:bg-slate-50'}`} onClick={() => setTab('EVIDENCE')}>EVIDENCE</button>
        <button className={`flex-1 text-center py-3 transition-colors ${tab === 'CHANGE' ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50/30' : 'hover:text-slate-800 hover:bg-slate-50'}`} onClick={() => setTab('CHANGE')}>CHANGE</button>
        <button className={`flex-1 text-center py-3 transition-colors ${tab === 'FLAGS' ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50/30' : 'hover:text-slate-800 hover:bg-slate-50'}`} onClick={() => setTab('FLAGS')}>FLAGS</button>
      </div>

      <div className="flex-1 overflow-y-auto p-5 flex flex-col gap-6 custom-scrollbar text-sm bg-slate-50">
        {intervention.data_status === 'UNAVAILABLE' ? (
          <div className="text-center text-slate-500 mt-10 text-sm border-2 border-slate-200 border-dashed rounded-lg p-6 bg-white">
            <span className="text-2xl block mb-2">📡</span>
            <strong className="text-slate-700 block mb-1">Data not available</strong>
            Waiting for official ingestion for this project.
          </div>
        ) : (
          <>
            {tab === 'EVIDENCE' && (
              <>
                <div className="bg-white border border-slate-200 shadow-sm rounded-lg p-4 relative">
                  {intervention.data_status === 'DEMO' && demoMode && <span className="absolute -top-2 -right-2 bg-yellow-500 text-[10px] font-bold px-2 py-0.5 rounded-full text-white shadow">DEMO</span>}
                  
                  <div className="flex justify-between items-center mb-4">
                    <div className="text-center flex-1 border-r border-slate-100">
                      <div className="text-xs text-slate-500 font-bold mb-1">IMPACT SCORE</div>
                      <div className="text-3xl font-extrabold text-blue-600">{intervention.score_impact} <span className="text-sm text-slate-400 font-normal">/100</span></div>
                    </div>
                    <div className="text-center flex-1">
                      <div className="text-xs text-slate-500 font-bold mb-1">CONFIDENCE</div>
                      <div className="text-3xl font-extrabold text-slate-700">{intervention.score_confidence} <span className="text-sm text-slate-400 font-normal">/100</span></div>
                    </div>
                  </div>
                  
                  <div className="text-xs font-bold text-slate-800 mb-2 border-b border-slate-100 pb-2 uppercase tracking-wide">Score Breakdown</div>
                  <div className="grid grid-cols-2 gap-y-3 gap-x-4 text-xs font-medium">
                    <div className="flex justify-between items-center bg-slate-50 p-1.5 rounded"><span>Vegetation</span><span className="text-green-600 font-bold">+{intervention.impact_veg}</span></div>
                    <div className="flex justify-between items-center bg-slate-50 p-1.5 rounded"><span>Water</span><span className="text-blue-600 font-bold">+{intervention.impact_water}</span></div>
                    <div className="flex justify-between items-center bg-slate-50 p-1.5 rounded"><span>Structural</span><span className="text-slate-600 font-bold">+{intervention.impact_lulc}</span></div>
                    <div className="flex justify-between items-center bg-slate-50 p-1.5 rounded"><span>Temporal</span><span className="text-slate-600 font-bold">+{intervention.impact_temporal}</span></div>
                    <div className="flex justify-between items-center bg-slate-50 p-1.5 rounded"><span>Field</span><span className="text-slate-600 font-bold">+{intervention.impact_field}</span></div>
                  </div>
                  <div className="text-[11px] text-slate-500 italic mt-4 text-center">Evidence-based impact indicator. Not causal proof.</div>
                </div>

                <div className="bg-white border border-slate-200 shadow-sm rounded-lg p-4">
                  <h3 className="text-xs font-bold text-slate-800 mb-3 border-b border-slate-100 pb-2 uppercase tracking-wide">Why this intervention?</h3>
                  <div className="text-sm text-slate-700 flex flex-col gap-2 font-medium">
                    {!intervention.flag_water && <div className="flex items-center gap-2"><span className="text-green-500 text-lg leading-none">✓</span> Surface water response detected</div>}
                    {!intervention.flag_veg && <div className="flex items-center gap-2"><span className="text-green-500 text-lg leading-none">✓</span> Vegetation response detected</div>}
                    {!intervention.flag_missing_photo && <div className="flex items-center gap-2"><span className="text-green-500 text-lg leading-none">✓</span> Field evidence available</div>}
                    {intervention.flag_season && <div className="flex items-center gap-2 text-yellow-600"><span className="text-lg leading-none">⚠</span> Seasonal variation requires review</div>}
                    {intervention.flag_conflict && <div className="flex items-center gap-2 text-red-600"><span className="text-lg leading-none">⚠</span> Field/Satellite evidence conflict</div>}
                  </div>
                  <div className="text-sm text-slate-800 mt-4 p-3 bg-blue-50 rounded border border-blue-100 font-medium">
                    {intervention.priority_reason}
                  </div>
                </div>
                
                <div className="bg-white border border-slate-200 shadow-sm rounded-lg p-4">
                  <h3 className="text-xs font-bold text-slate-800 mb-3 border-b border-slate-100 pb-2 uppercase tracking-wide">FIELD EVIDENCE</h3>
                  {intervention.flag_missing_photo ? (
                    <div className="h-28 bg-slate-100 border border-slate-200 rounded flex flex-col items-center justify-center text-sm text-slate-500">
                      <span className="text-2xl mb-1">📷</span>
                      <span className="font-bold">Field Photo Unavailable</span>
                    </div>
                  ) : (
                    <div className="flex flex-col gap-3">
                      <div className="h-40 bg-slate-200 border border-slate-300 rounded flex items-center justify-center text-sm text-slate-500 font-medium shadow-inner">
                        [ Geo-tagged Photo Proxy ]
                      </div>
                      <div className="text-sm text-slate-700 font-medium bg-slate-50 p-2 rounded">Visible water accumulation near the structure.</div>
                    </div>
                  )}
                </div>
              </>
            )}

            {tab === 'CHANGE' && (
              <>
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wide">Change Detection</h3>
                  {intervention.data_status === 'DEMO' && demoMode && <span className="bg-yellow-500 text-[10px] font-bold px-1.5 py-0.5 rounded text-white shadow-sm">DEMO</span>}
                </div>
                
                <div className="flex gap-3 mb-4">
                  <div className="flex-1 bg-white border border-slate-200 shadow-sm rounded p-3 text-center">
                    <div className="text-xs font-bold text-slate-500 mb-1 tracking-wide">BEFORE</div>
                    <div className="text-sm font-extrabold text-slate-800">May 2023</div>
                  </div>
                  <div className="flex-1 bg-white border border-slate-200 shadow-sm rounded p-3 text-center">
                    <div className="text-xs font-bold text-slate-500 mb-1 tracking-wide">AFTER</div>
                    <div className="text-sm font-extrabold text-slate-800">May 2024</div>
                  </div>
                </div>

                <div className="flex flex-col gap-3">
                  <div className="bg-white border border-slate-200 shadow-sm rounded-lg p-4">
                    <div className="text-xs font-bold text-slate-500 mb-2 uppercase">Water Spread Change</div>
                    <div className="flex justify-between items-end">
                      <span className="text-2xl font-extrabold text-blue-600">{intervention.water_spread_change > 0 ? '+' : ''}{intervention.water_spread_change}%</span>
                      <span className="text-sm font-medium text-slate-600 bg-slate-50 px-2 py-1 rounded">1,240 m² → 3,870 m²</span>
                    </div>
                  </div>
                  
                  <div className="bg-white border border-slate-200 shadow-sm rounded-lg p-4">
                    <div className="text-xs font-bold text-slate-500 mb-2 uppercase">NDVI (Vegetation) Change</div>
                    <div className="flex justify-between items-end">
                      <span className="text-2xl font-extrabold text-green-600">{intervention.ndvi_change > 0 ? '+' : ''}{intervention.ndvi_change}</span>
                      <span className="text-sm font-medium text-slate-600 bg-slate-50 px-2 py-1 rounded">0.31 → 0.46</span>
                    </div>
                  </div>
                  
                  <div className="bg-white border border-slate-200 shadow-sm rounded-lg p-4">
                    <div className="text-xs font-bold text-slate-500 mb-2 uppercase">MNDWI (Water Index) Change</div>
                    <div className="flex justify-between items-end">
                      <span className="text-2xl font-extrabold text-blue-500">{intervention.mndwi_change > 0 ? '+' : ''}{intervention.mndwi_change}</span>
                    </div>
                  </div>
                </div>
                
                <div className="mt-2 bg-blue-50 border border-blue-100 p-4 rounded-lg">
                  <h3 className="text-xs font-bold text-blue-800 mb-2 uppercase tracking-wide">Reference Zone (500m)</h3>
                  <div className="text-sm text-blue-900 font-medium">
                    Intervention shows higher vegetation and water response compared to the 500m surrounding reference zone.
                  </div>
                </div>
              </>
            )}

            {tab === 'FLAGS' && (
              <div className="flex flex-col gap-3">
                {intervention.flag_conflict && (
                  <div className="bg-red-50 border border-red-200 p-4 rounded-lg shadow-sm">
                    <div className="flex items-center gap-2 text-red-600 font-bold mb-2 uppercase text-xs tracking-wide">
                      <span className="text-lg">⚠</span> Field / Satellite Conflict
                    </div>
                    <div className="text-sm text-red-900 font-medium mb-2">Field evidence and satellite evidence disagree.</div>
                    <div className="text-xs text-red-700 bg-red-100 p-2 rounded">Recommended: Mandatory on-site verification.</div>
                  </div>
                )}
                
                {intervention.flag_hydro && (
                  <div className="bg-orange-50 border border-orange-200 p-4 rounded-lg shadow-sm">
                    <div className="flex items-center gap-2 text-orange-600 font-bold mb-2 uppercase text-xs tracking-wide">
                      <span className="text-lg">⚠</span> Hydrological Mismatch
                    </div>
                    <div className="text-sm text-orange-900 font-medium">Intervention does not intersect expected drainage network.</div>
                  </div>
                )}
                
                {intervention.flag_season && (
                  <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg shadow-sm">
                    <div className="flex items-center gap-2 text-yellow-600 font-bold mb-2 uppercase text-xs tracking-wide">
                      <span className="text-lg">⚠</span> Seasonality Conflict
                    </div>
                    <div className="text-sm text-yellow-900 font-medium">Observed change may be explained by rainfall/seasonal variation rather than structure impact.</div>
                  </div>
                )}
                
                {!intervention.flag_conflict && !intervention.flag_hydro && !intervention.flag_season && (
                  <div className="text-sm font-bold text-slate-500 p-6 border-2 border-slate-200 border-dashed rounded-lg text-center bg-white flex flex-col items-center gap-2">
                    <span className="text-3xl">✓</span>
                    No critical red flags detected.
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </div>
      
      <div className="p-4 bg-slate-100 border-t border-slate-200 text-[10px] text-slate-500 font-medium">
        <div className="font-extrabold mb-1.5 text-slate-700 uppercase tracking-wide">Data Sources</div>
        <div className="mb-0.5"><strong className="text-slate-600">Govt/Spatial:</strong> Bhuvan WDC 2.0, WDC PMKSY MIS</div>
        <div className="mb-0.5"><strong className="text-slate-600">Remote Sensing:</strong> Sentinel-2 (Bhuvan imagery where avail)</div>
        <div><strong className="text-slate-600">Field:</strong> DRISHTI geo-tagged evidence</div>
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
