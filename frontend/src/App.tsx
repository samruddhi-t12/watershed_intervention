import React, { useState, useEffect } from 'react';
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
  const [activeLayers, setActiveLayers] = useState(['Hydrology', 'Interventions (Check Dams)', 'Project Boundary', 'Integrated Change Index (SCI)']);
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
      const res = await axios.get('/data/interventions.json');
      setInterventions(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  const handleSelectId = (id) => {
    setSelectedId(id);
    setClickedCell(null);
    setActiveTab('Overview');
  };

  const handleSelectCell = (cell) => {
    setClickedCell(cell);
    setSelectedId(null);
  };

  const handleSearch = (query) => {
    if (!query) return false;
    const inv = interventions.find(i => i.work_code.toLowerCase().includes(query.toLowerCase()));
    if (inv) {
      handleSelectId(inv.id);
      return true;
    }
    return false;
  };

  const selectedInv = interventions.find(i => i.id === selectedId);

  return (
    <div className="h-screen w-full flex flex-col bg-[#f8fafc] text-slate-800 font-sans overflow-hidden">
      <TopNav metrics={metrics} demoMode={demoMode} setDemoMode={setDemoMode} setShowSources={setShowSources} onSearch={handleSearch} interventions={interventions} />
      
      <div className="bg-white border-b border-slate-200 px-6 py-3 flex gap-4 shrink-0 shadow-sm z-30 relative overflow-x-auto">
        <div className="flex-1 min-w-[180px] bg-white border border-slate-200 rounded-md p-3 flex items-center shadow-sm">
          <div className="bg-blue-100 text-blue-600 p-2 rounded-md mr-3">🗺️</div>
          <div><div className="text-xs font-bold text-slate-500 uppercase tracking-wide">Total Interventions</div><div className="text-xl font-extrabold text-slate-800">{interventions.length}</div></div>
        </div>
        <div className="flex-1 min-w-[180px] bg-white border border-slate-200 rounded-md p-3 flex items-center shadow-sm">
          <div className="bg-cyan-100 text-cyan-600 p-2 rounded-md mr-3">🌊</div>
          <div><div className="text-xs font-bold text-slate-500 uppercase tracking-wide">Check Dams</div><div className="text-xl font-extrabold text-slate-800">{interventions.filter(i=>i.type && i.type.includes('Check Dam')).length}</div></div>
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
          onSelect={handleSelectId}
        />
        
        <div className="flex-1 flex flex-col min-w-0 min-h-0 bg-slate-200 border-r border-slate-300 relative">
          
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
              onSelect={handleSelectId}
              baseMap={baseMap}
              activeLayers={activeLayers}
              demoMode={demoMode}
              selectedYear={selectedYear}
              compareYear={compareYear}
              swipeMode={swipeMode}
              setClickedCell={handleSelectCell}
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
                  clickedCell.properties.years[`202${parseInt(selectedYear.replace('T', '')) + 1}`]?.changeClass === 'severe_degradation' ? 'bg-red-50 text-red-700 border-red-200' :
                  clickedCell.properties.years[`202${parseInt(selectedYear.replace('T', '')) + 1}`]?.changeClass === 'moderate_degradation' ? 'bg-orange-50 text-orange-700 border-orange-200' :
                  clickedCell.properties.years[`202${parseInt(selectedYear.replace('T', '')) + 1}`]?.changeClass === 'improving' ? 'bg-green-50 text-green-700 border-green-200' :
                  clickedCell.properties.years[`202${parseInt(selectedYear.replace('T', '')) + 1}`]?.changeClass === 'strong_improvement' ? 'bg-emerald-50 text-emerald-800 border-emerald-200' :
                  'bg-slate-100 text-slate-700 border-slate-200'
                } border`}>
                  {clickedCell.properties.years[`202${parseInt(selectedYear.replace('T', '')) + 1}`]?.changeClass?.replace(/_/g, ' ')?.toUpperCase() || 'NO DATA'}
                </div>
                <div className="text-sm text-slate-600 mt-3 font-medium leading-relaxed">
                  {clickedCell.properties.years[`202${parseInt(selectedYear.replace('T', '')) + 1}`]?.reasonText || 'No analytical data available for this period.'}
                </div>
              </div>
            </div>
          </div>
        ) : null}
      </main>

      {showSources && <DataSourcesModal onClose={() => setShowSources(false)} interventions={interventions} />}
    </div>
  );
}

function DataSourcesModal({ onClose, interventions = [] }) {
  const conflictCount = interventions.filter(i => i.flag_conflict).length;
  const invalidHydroCount = interventions.filter(i => i.flag_hydro).length;
  const missingCoordsCount = interventions.filter(i => i.data_status === 'UNAVAILABLE').length;

  return (
    <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-[3000] flex items-center justify-center">
      <div className="bg-white rounded-xl shadow-2xl w-[700px] max-h-[80vh] flex flex-col overflow-hidden border border-slate-200">
        <div className="px-6 py-5 border-b border-slate-200 bg-slate-50 flex justify-between items-center">
          <h2 className="text-lg font-black text-slate-800">Data Sources & Authoritative Scope</h2>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-700 text-xl font-bold">&times;</button>
        </div>
        <div className="p-6 overflow-y-auto flex flex-col gap-6">
        
          <div className="bg-blue-50/50 border border-blue-100 rounded-lg p-5">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-2 h-2 rounded-full bg-blue-500"></div>
              <h3 className="text-sm font-bold text-blue-900 uppercase tracking-widest">Accountability Signals (Audit)</h3>
            </div>
            <p className="text-sm text-slate-600 mb-3">The Evidence Engine acts as an automated audit layer, identifying misreporting and anomalies in field data:</p>
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-white border border-blue-100 p-3 rounded shadow-sm text-center">
                <div className="text-2xl font-black text-blue-600 mb-1">{conflictCount}</div>
                <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Evidence Conflicts</div>
              </div>
              <div className="bg-white border border-blue-100 p-3 rounded shadow-sm text-center">
                <div className="text-2xl font-black text-blue-600 mb-1">{invalidHydroCount}</div>
                <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Hydrology Failures</div>
              </div>
              <div className="bg-white border border-blue-100 p-3 rounded shadow-sm text-center">
                <div className="text-2xl font-black text-blue-600 mb-1">{missingCoordsCount}</div>
                <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Missing Coordinates</div>
              </div>
            </div>
          </div>
          
          <div className="bg-green-50/50 border border-green-100 rounded-lg p-5">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-2 h-2 rounded-full bg-green-500"></div>
              <h3 className="text-sm font-bold text-green-900 uppercase tracking-widest">Real & Computed Data</h3>
            </div>
            <ul className="text-sm text-slate-700 flex flex-col gap-3 ml-4 list-disc marker:text-green-300">
              <li><strong>Administrative Boundary:</strong> True Khed Taluka catchment polygon.</li>
              <li><strong>Terrain & Hydrology:</strong> SRTM 30m Digital Elevation Model. True geographic stream network computed via <code>pysheds</code> (Flow Direction & Accumulation).</li>
              <li>
                <strong>Government Schema (DRISHTI):</strong> Data model is structurally identical to the Bhuvan WDC 2.0 / SRISHTI portal (<a href="https://bhuvan-app1.nrsc.gov.in/iwmp/" target="_blank" rel="noreferrer" className="text-teal-600 hover:underline">bhuvan-app1.nrsc.gov.in/iwmp/</a>), ensuring full integration readiness. Supported keys:
                <div className="mt-2 flex flex-wrap gap-1">
                  {['Sl.No','Server Time','apptype','appsubtype','FDCprojectname','themename','profilename','observername','org','mobileno','creationtime','uuid','deviceid','Name','StatusOfActivity','WorkCode','Location','DateCompletion','Details'].map(k => (
                    <code key={k} className="text-[10px] bg-white border border-green-200 text-green-800 px-1.5 py-0.5 rounded shadow-sm">{k}</code>
                  ))}
                </div>
              </li>
            </ul>
          </div>
          
          <div className="bg-amber-50/50 border border-amber-100 rounded-lg p-5">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-2 h-2 rounded-full bg-amber-500"></div>
              <h3 className="text-sm font-bold text-amber-900 uppercase tracking-widest">Synthetic Trend Data (Demo)</h3>
            </div>
            <p className="text-sm text-slate-600 mb-3">To demonstrate the Evidence Engine's capabilities prior to full satellite data ingestion, the following analytical layers are generated probabilistically based on actual terrain constraints:</p>
            <ul className="text-sm text-slate-700 flex flex-col gap-3 ml-4 list-disc marker:text-amber-300">
              <li><strong>Analysis Grids (T0-T4):</strong> The Vegetation (SAVI), Water Conservation (MNDWI), and Integrated Change Index (SCI) grids are synthetically computed using proximity to real stream networks and random variance.</li>
              <li><strong>Intervention Evidence Scores:</strong> Impact and Confidence metrics assigned to prototype check dams are derived algorithmically to simulate field-vs-satellite conflict scenarios.</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
