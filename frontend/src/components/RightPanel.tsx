import React from 'react';

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
            
            {intervention.cost_estimated && (
              <div className="mt-4 pt-4 border-t border-slate-100 flex justify-between items-center text-xs">
                <div>
                  <div className="text-slate-400 font-extrabold tracking-widest uppercase mb-0.5">Est. Cost (Demo)</div>
                  <div className="font-medium text-slate-700">₹{intervention.cost_estimated.toLocaleString('en-IN')}</div>
                </div>
                <div className="text-right">
                  <div className="text-slate-400 font-extrabold tracking-widest uppercase mb-0.5">ROI Score per ₹1k</div>
                  <div className="font-black text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-100 inline-block">
                    {((intervention.score_impact / intervention.cost_estimated) * 1000).toFixed(4)}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'Evidence' && (
          <div className="flex flex-col gap-4">
            <div className="bg-white border border-slate-200 shadow-sm rounded-xl p-5">
              <h3 className="text-xs font-extrabold text-slate-800 mb-3 uppercase tracking-widest border-b border-slate-100 pb-2">Impact Score Breakdown</h3>
              <div className="flex flex-col gap-2 text-xs">
                <div className="flex justify-between items-center"><span className="text-slate-600 font-medium">Vegetation (SAVI)</span><span className="font-bold text-slate-800">+{intervention.impact_veg || 0}</span></div>
                <div className="w-full bg-slate-100 rounded-full h-1.5 mb-1"><div className="bg-green-500 h-1.5 rounded-full" style={{width: `${(intervention.impact_veg / intervention.score_impact) * 100}%`}}></div></div>
                
                <div className="flex justify-between items-center"><span className="text-slate-600 font-medium">Water (MNDWI)</span><span className="font-bold text-slate-800">+{intervention.impact_water || 0}</span></div>
                <div className="w-full bg-slate-100 rounded-full h-1.5 mb-1"><div className="bg-blue-500 h-1.5 rounded-full" style={{width: `${(intervention.impact_water / intervention.score_impact) * 100}%`}}></div></div>
                
                <div className="flex justify-between items-center"><span className="text-slate-600 font-medium">Structural (LULC)</span><span className="font-bold text-slate-800">+{intervention.impact_lulc || 0}</span></div>
                <div className="w-full bg-slate-100 rounded-full h-1.5 mb-1"><div className="bg-amber-500 h-1.5 rounded-full" style={{width: `${(intervention.impact_lulc / intervention.score_impact) * 100}%`}}></div></div>
                
                <div className="flex justify-between items-center"><span className="text-slate-600 font-medium">Temporal Trend</span><span className="font-bold text-slate-800">+{intervention.impact_temporal || 0}</span></div>
                <div className="w-full bg-slate-100 rounded-full h-1.5 mb-1"><div className="bg-indigo-500 h-1.5 rounded-full" style={{width: `${(intervention.impact_temporal / intervention.score_impact) * 100}%`}}></div></div>
                
                <div className="flex justify-between items-center"><span className="text-slate-600 font-medium">Field Evidence</span><span className="font-bold text-slate-800">+{intervention.impact_field || 0}</span></div>
                <div className="w-full bg-slate-100 rounded-full h-1.5"><div className="bg-teal-500 h-1.5 rounded-full" style={{width: `${(intervention.impact_field / intervention.score_impact) * 100}%`}}></div></div>
              </div>
            </div>

            <div className="bg-white border border-slate-200 shadow-sm rounded-xl p-5">
              <h3 className="text-xs font-extrabold text-slate-800 mb-3 uppercase tracking-widest border-b border-slate-100 pb-2">Drishti Field Photo</h3>
              <div className="h-48 bg-slate-100 border border-slate-300 rounded-lg flex items-center justify-center text-sm text-slate-500 font-medium shadow-inner overflow-hidden relative group">
                <img 
                  src={`/field_photos/${intervention.work_code}.jpg`}
                  alt="Field Evidence" 
                  className="absolute inset-0 w-full h-full object-cover z-10"
                  onError={(e) => {
                    e.currentTarget.style.display = 'none';
                  }}
                />
                <div className="z-0 flex flex-col items-center gap-1">
                  <span className="text-xl">📷</span>
                  <span>Proxy Geotagged Photo</span>
                  <span className="text-[10px] text-slate-400">Add {intervention.work_code}.jpg to /public/field_photos/</span>
                </div>
              </div>
              {intervention.cv_signal_text && (
                <div className="mt-3 text-xs bg-emerald-50 border border-emerald-100 text-emerald-800 p-2 rounded flex items-center gap-2 font-medium">
                  <span>🔬</span> {intervention.cv_signal_text}
                </div>
              )}
            </div>
            
            <div className="bg-white border border-slate-200 shadow-sm rounded-xl p-5">
              <h3 className="text-xs font-extrabold text-slate-800 mb-3 uppercase tracking-widest border-b border-slate-100 pb-2">Record Metadata</h3>
              <div className="text-xs text-slate-600 grid grid-cols-2 gap-x-4 gap-y-3 mb-4">
                <div className="flex flex-col"><span className="text-slate-400 font-bold uppercase text-[10px]">Sl.No</span><span className="font-medium text-slate-800">{intervention.drishti_sl_no || 'N/A'}</span></div>
                <div className="flex flex-col"><span className="text-slate-400 font-bold uppercase text-[10px]">Server Time</span><span className="font-medium text-slate-800">{intervention.drishti_server_time || 'N/A'}</span></div>
                <div className="flex flex-col"><span className="text-slate-400 font-bold uppercase text-[10px]">apptype</span><span className="font-medium text-slate-800">{intervention.drishti_apptype || 'N/A'}</span></div>
                <div className="flex flex-col"><span className="text-slate-400 font-bold uppercase text-[10px]">appsubtype</span><span className="font-medium text-slate-800">{intervention.drishti_appsubtype || 'N/A'}</span></div>
                <div className="flex flex-col"><span className="text-slate-400 font-bold uppercase text-[10px]">FDCprojectname</span><span className="font-medium text-slate-800">{intervention.drishti_fdcprojectname || 'N/A'}</span></div>
                <div className="flex flex-col"><span className="text-slate-400 font-bold uppercase text-[10px]">themename</span><span className="font-medium text-slate-800">{intervention.drishti_themename || 'N/A'}</span></div>
                <div className="flex flex-col"><span className="text-slate-400 font-bold uppercase text-[10px]">profilename</span><span className="font-medium text-slate-800">{intervention.drishti_profilename || 'N/A'}</span></div>
                <div className="flex flex-col"><span className="text-slate-400 font-bold uppercase text-[10px]">observername</span><span className="font-medium text-slate-800">{intervention.drishti_observername || 'N/A'}</span></div>
                <div className="flex flex-col"><span className="text-slate-400 font-bold uppercase text-[10px]">org</span><span className="font-medium text-slate-800">{intervention.drishti_org || 'N/A'}</span></div>
                <div className="flex flex-col"><span className="text-slate-400 font-bold uppercase text-[10px]">mobileno</span><span className="font-medium text-slate-800">{intervention.drishti_mobileno || '-'}</span></div>
                <div className="flex flex-col"><span className="text-slate-400 font-bold uppercase text-[10px]">creationtime</span><span className="font-medium text-slate-800">{intervention.drishti_creationtime || 'N/A'}</span></div>
                <div className="flex flex-col"><span className="text-slate-400 font-bold uppercase text-[10px]">uuid</span><span className="font-medium text-slate-800 truncate" title={intervention.drishti_uuid}>{intervention.drishti_uuid || 'N/A'}</span></div>
                <div className="flex flex-col"><span className="text-slate-400 font-bold uppercase text-[10px]">deviceid</span><span className="font-medium text-slate-800">{intervention.drishti_deviceid || 'N/A'}</span></div>
                <div className="flex flex-col"><span className="text-slate-400 font-bold uppercase text-[10px]">Name</span><span className="font-medium text-slate-800">{intervention.drishti_name || 'N/A'}</span></div>
                <div className="flex flex-col"><span className="text-slate-400 font-bold uppercase text-[10px]">StatusOfActivity</span><span className="font-medium text-slate-800">{intervention.drishti_statusofactivity || 'N/A'}</span></div>
                <div className="flex flex-col"><span className="text-slate-400 font-bold uppercase text-[10px]">WorkCode</span><span className="font-medium text-slate-800">{intervention.work_code || 'N/A'}</span></div>
                <div className="flex flex-col col-span-2"><span className="text-slate-400 font-bold uppercase text-[10px]">Location</span><span className="font-medium text-slate-800">{intervention.drishti_location || 'N/A'}</span></div>
                <div className="flex flex-col"><span className="text-slate-400 font-bold uppercase text-[10px]">DateCompletion</span><span className="font-medium text-slate-800">{intervention.drishti_datecompletion || 'N/A'}</span></div>
                <div className="flex flex-col col-span-2"><span className="text-slate-400 font-bold uppercase text-[10px]">Details</span><span className="font-medium text-slate-800">{intervention.drishti_details || 'N/A'}</span></div>
              </div>
              <div className="pt-4 border-t border-slate-100 text-center">
                <a 
                  href="https://bhuvan-app1.nrsc.gov.in/iwmp/" 
                  target="_blank" 
                  rel="noreferrer"
                  title="Built to be compatible with the DRISHTI field-record format used on the government portal."
                  className="text-[11px] text-teal-600 hover:text-teal-800 font-extrabold hover:underline flex items-center justify-center gap-1 uppercase tracking-wide"
                >
                  Source data schema: DRISHTI field record format — View reference portal ↗
                </a>
              </div>
            </div>
          </div>
        )}
        
        {activeTab === 'Change' && (
          <div className="bg-white border border-slate-200 shadow-sm rounded-xl p-5">
            <div className="flex justify-between items-center mb-3 border-b border-slate-100 pb-2">
              <h3 className="text-xs font-extrabold text-slate-800 uppercase tracking-widest">Temporal Changes (T0 - T4)</h3>
            </div>
            
            {intervention.rainfall_context && (
              <div className="mb-4 text-xs font-medium text-slate-600 bg-blue-50/50 p-2 rounded border border-blue-100 flex items-center gap-2">
                <span>🌧️</span> {intervention.rainfall_context}
              </div>
            )}
            
            <div className="flex flex-col gap-5 mt-4">
              <div>
                <div className="flex justify-between items-center mb-1">
                  <span className="text-sm font-bold text-slate-600">Water Conservation (MNDWI)</span>
                  <span className="text-lg font-black text-blue-600">{intervention.mndwi_change > 0 ? '+' : ''}{intervention.mndwi_change || 0}</span>
                </div>
                <div className="text-[10px] text-slate-400 font-medium">
                  Intervention: <span className={intervention.mndwi_change > 0 ? 'text-blue-600' : ''}>{intervention.mndwi_change > 0 ? '+' : ''}{intervention.mndwi_change || 0}</span> | Reference zone: {intervention.ref_mndwi_change > 0 ? '+' : ''}{intervention.ref_mndwi_change || 0}
                </div>
              </div>
              
              <div>
                <div className="flex justify-between items-center mb-1">
                  <span className="text-sm font-bold text-slate-600">Vegetation (SAVI)</span>
                  <span className="text-lg font-black text-green-600">{intervention.ndvi_change > 0 ? '+' : ''}{intervention.ndvi_change || 0}</span>
                </div>
                <div className="text-[10px] text-slate-400 font-medium">
                  Intervention: <span className={intervention.ndvi_change > 0 ? 'text-green-600' : ''}>{intervention.ndvi_change > 0 ? '+' : ''}{intervention.ndvi_change || 0}</span> | Reference zone: {intervention.ref_ndvi_change > 0 ? '+' : ''}{intervention.ref_ndvi_change || 0}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'Flags' && (
          <div className="flex flex-col gap-4">
            {intervention.flag_conflict && (
              <div className="bg-red-50 border border-red-200 p-5 rounded-xl shadow-sm">
                <div className="flex items-center gap-2 text-red-700 font-bold mb-2 uppercase text-xs tracking-widest">🚩 Field/Satellite Conflict</div>
                <div className="text-sm text-red-900 font-medium">Field evidence and satellite evidence disagree. On-site verification recommended.</div>
              </div>
            )}
            
            {intervention.flag_hydro && (
              <div className="bg-amber-50 border border-amber-200 p-5 rounded-xl shadow-sm">
                <div className="flex items-center gap-2 text-amber-700 font-bold mb-2 uppercase text-xs tracking-widest">⚠️ Hydrological Validity</div>
                <div className="text-sm text-amber-900 font-medium">Intervention coordinates are suspiciously distant from the modeled stream network.</div>
              </div>
            )}
            
            {intervention.data_status === 'UNAVAILABLE' && (
              <div className="bg-slate-100 border border-slate-300 p-5 rounded-xl shadow-sm">
                <div className="flex items-center gap-2 text-slate-700 font-bold mb-2 uppercase text-xs tracking-widest">📵 Missing Coordinates</div>
                <div className="text-sm text-slate-600 font-medium">Spatial location was not provided in the DRISHTI dataset.</div>
              </div>
            )}

            {!intervention.flag_conflict && !intervention.flag_hydro && intervention.data_status !== 'UNAVAILABLE' && (
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
