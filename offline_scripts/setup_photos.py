import os

frontend_files = {
    "frontend/src/components/RightPanel.tsx": """import React, { useState } from 'react';

export default function RightPanel({ intervention, demoMode }) {
  const [tab, setTab] = useState('EVIDENCE');
  const [photoError, setPhotoError] = useState(false);

  // Reset photo error when intervention changes
  React.useEffect(() => {
    setPhotoError(false);
  }, [intervention?.id]);

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
                  <h3 className="text-xs font-bold text-gray-800 mb-3 border-b border-gray-100 pb-2 uppercase tracking-wide">FIELD EVIDENCE</h3>
                  {!photoError && !intervention.flag_missing_photo ? (
                    <div className="flex flex-col gap-3">
                      <div className="bg-gray-100 border border-gray-300 rounded-md overflow-hidden shadow-inner h-48 relative">
                        <img 
                          src={`/photos/${intervention.work_code}.jpg`} 
                          alt={`Field evidence for ${intervention.work_code}`}
                          onError={() => setPhotoError(true)}
                          className="w-full h-full object-cover"
                        />
                      </div>
                      <div className="text-sm text-gray-800 font-medium bg-gray-50 border border-gray-100 p-2 rounded-md">Visible water accumulation near the structure.</div>
                    </div>
                  ) : (
                    <div className="h-28 bg-gray-50 border border-gray-200 rounded-md flex flex-col items-center justify-center text-sm text-gray-500">
                      <span className="text-2xl mb-1">📷</span>
                      <span className="font-bold">Field Photo Unavailable</span>
                      <span className="text-[10px] mt-1 text-gray-400">Add /photos/{intervention.work_code}.jpg</span>
                    </div>
                  )}
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
                    <div className="text-sm font-extrabold text-gray-800">May 2021</div>
                  </div>
                  <div className="flex-1 bg-white border border-gray-300 shadow-sm rounded-md p-3 text-center">
                    <div className="text-xs font-bold text-gray-500 mb-1 tracking-wide">AFTER</div>
                    <div className="text-sm font-extrabold text-gray-800">May 2025</div>
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
        <div className="font-extrabold mb-2 text-gray-700 uppercase tracking-wide">Data Sources</div>
        <div className="mb-1"><strong className="text-gray-600">Govt/Spatial:</strong> Bhuvan WDC 2.0, WDC PMKSY MIS</div>
        <div className="mb-1"><strong className="text-gray-600">Remote Sensing:</strong> Sentinel-2 (Bhuvan imagery where avail)</div>
        <div><strong className="text-gray-600">Field:</strong> DRISHTI geo-tagged evidence</div>
      </div>
    </div>
  );
}
"""
}

def create_files():
    # Make sure folders exist
    os.makedirs(os.path.join(os.path.dirname(__file__), "frontend", "public", "photos"), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), "frontend", "public", "rasters"), exist_ok=True)
    
    for path, content in frontend_files.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    create_files()
