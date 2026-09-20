import React from 'react';

export default function LeftSidebar({ activeLayers, setActiveLayers, baseMap, setBaseMap, interventions, selectedId, onSelect }) {
  const toggleLayer = (layer) => {
    if (activeLayers.includes(layer)) setActiveLayers(activeLayers.filter(l => l !== layer));
    else setActiveLayers([...activeLayers, layer]);
  };

  const LayerCheckbox = ({ label }) => (
    <div className="flex items-center justify-between hover:bg-slate-50 p-1.5 rounded-md transition-colors w-full">
      <label className="flex items-center gap-2 text-sm cursor-pointer text-slate-700 font-medium flex-1">
        <input type="checkbox" checked={activeLayers.includes(label)} onChange={() => toggleLayer(label)} className="w-4 h-4 text-teal-600 rounded border-slate-300 focus:ring-teal-500" />
        {label}
      </label>
    </div>
  );

  const sorted = [...interventions].sort((a, b) => {
    const order = { 'FLAGGED': 1, 'REVIEW': 2, 'VERIFIED': 3 };
    if (order[a.status_badge] !== order[b.status_badge]) return order[a.status_badge] - order[b.status_badge];
    return (b.score_confidence || 0) - (a.score_confidence || 0);
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
            <div className="text-[11px] uppercase text-slate-500 font-bold mb-1 tracking-wide">Hydrology (Real DEM)</div>
            <div className="flex flex-col gap-0.5 border border-slate-100 p-1 rounded">
              <LayerCheckbox label="Project Boundary" isSynthetic={false} />
              <LayerCheckbox label="Hydrology" isSynthetic={false} />
              <LayerCheckbox label="Terrain Relief" isSynthetic={false} />
            </div>
          </div>
          
          <div>
            <div className="text-[11px] uppercase text-slate-500 font-bold mb-1 tracking-wide">Analytical Overlays</div>
            <div className="flex flex-col gap-0.5 border border-slate-100 p-1 rounded">
              <LayerCheckbox label="Integrated Change Index (SCI)" isSynthetic={true} />
              <LayerCheckbox label="Vegetation (SAVI)" isSynthetic={true} />
              <LayerCheckbox label="Water Conservation (MNDWI)" isSynthetic={true} />
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
