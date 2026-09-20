import React from 'react';

export default function EvidencePanel({ intervention, activeLayers }) {
  if (!intervention) return null;

  return (
    <div className="flex flex-col gap-4 p-4 text-sm">
      <div className="pb-3 border-b">
        <h2 className="text-xl font-bold">{intervention.type}</h2>
        <div className="text-slate-500 text-xs">ID: {intervention.work_code} | Prototype Demo Coordinates</div>
      </div>

      {intervention.cv_status === "CONFLICT" && (
        <div className="bg-red-100 border border-red-400 text-red-800 p-3 rounded font-bold flex flex-col gap-1 shadow-sm">
          <div className="flex items-center gap-2">
            <span className="text-lg">⚠</span> EVIDENCE CONFLICT DETECTED
          </div>
          <div className="font-normal text-xs text-red-700 mt-1">
            Field evidence: Positive<br/>
            Satellite evidence: Weak/Negative<br/>
            Human verification strongly recommended.
          </div>
        </div>
      )}

      <div className={`p-3 rounded font-bold text-white shadow-sm flex flex-col ${intervention.priority === 'P1' ? 'bg-red-600' : intervention.priority === 'P2' ? 'bg-yellow-600' : 'bg-green-600'}`}>
        <div className="flex justify-between items-center">
          <span>PRIORITY {intervention.priority}</span>
          <span className="text-xs bg-black/20 px-2 py-1 rounded">
            IMPACT: {intervention.score_impact.toFixed(2)} | CONF: {intervention.score_confidence.toFixed(2)}
          </span>
        </div>
        <div className="font-normal text-xs mt-2 text-white/90">{intervention.priority_reason}</div>
      </div>

      <div className="bg-slate-50 p-3 rounded border">
        <h3 className="font-bold text-slate-700 mb-2 border-b pb-1">FIELD EVIDENCE</h3>
        {intervention.field_has_photo ? (
          <div className="flex flex-col gap-2">
            <div className="h-32 bg-slate-300 rounded flex items-center justify-center text-slate-500 italic">
              [ Government Field Photo Proxy ]
            </div>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div>Water: <span className="font-bold">{intervention.field_water_presence}</span></div>
              <div>Veg: <span className="font-bold">{intervention.field_vegetation}</span></div>
            </div>
          </div>
        ) : (
          <div className="text-slate-500 italic">Field photo unavailable.</div>
        )}
      </div>

      <div className="bg-slate-50 p-3 rounded border">
        <h3 className="font-bold text-slate-700 mb-2 border-b pb-1">SATELLITE & HYDROLOGY</h3>
        <div className="grid grid-cols-2 gap-2 mb-3">
          <div>SAVI Trend: <span className="font-bold">{intervention.sat_savi_trend}</span></div>
          <div>MNDWI Trend: <span className="font-bold">{intervention.sat_mndwi_trend}</span></div>
          <div>Rainfall: <span className="font-bold">{intervention.ctx_rainfall}</span></div>
        </div>
        <div className="pt-2 border-t">
          <div className="flex justify-between items-center">
            <span>Hydrological Validity:</span>
            <span className={`font-bold px-2 py-0.5 rounded ${!intervention.flag_hydro ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
              {!intervention.flag_hydro ? 'VALID' : 'FLAGGED'}
            </span>
          </div>
        </div>
      </div>

      {(activeLayers.includes('Vegetation - SAVI') || activeLayers.includes('Water - MNDWI')) && (
        <div className="bg-slate-50 p-3 rounded border">
          <h3 className="font-bold text-slate-700 mb-2 border-b pb-1">REFERENCE COMPARISON</h3>
          <div className="text-xs text-slate-600 mb-2">Intervention vs 500m Reference Zone</div>
          {/* Simulated chart using basic divs for the MVP */}
          <div className="h-24 bg-white border rounded flex items-end p-2 gap-2 justify-center relative">
            <div className="absolute top-1 left-2 text-xs text-slate-400">Trend</div>
            <div className="w-8 bg-blue-500 rounded-t" style={{height: `${Math.max(10, (intervention.sat_mndwi_trend + 1)*40)}%`}}></div>
            <div className="w-8 bg-slate-300 rounded-t" style={{height: `${Math.max(10, (intervention.ctx_ref_zone_diff + 1)*30)}%`}}></div>
          </div>
          <div className="flex justify-center gap-4 text-xs mt-1">
            <span className="flex items-center gap-1"><div className="w-2 h-2 bg-blue-500"></div> Intervention</span>
            <span className="flex items-center gap-1"><div className="w-2 h-2 bg-slate-300"></div> Reference</span>
          </div>
        </div>
      )}
      
      <div className="text-center text-xs text-slate-400 italic mt-2">
        Evidence suggests {intervention.score_impact > 0.5 ? 'improvement' : 'minimal change'}.<br/>
        Scores are prototype indicators, not causal proof.
      </div>
      
      {/* DRISHTI Metadata Section */}
      <div className="bg-slate-50 p-3 rounded border mt-4">
        <h3 className="font-bold text-slate-700 mb-2 border-b pb-1">RECORD METADATA</h3>
        <div className="text-xs text-slate-600 grid grid-cols-2 gap-x-4 gap-y-2 mb-3">
          <div className="flex flex-col"><span className="text-slate-400 font-bold">Sl.No</span><span>{intervention.drishti_sl_no || 'N/A'}</span></div>
          <div className="flex flex-col"><span className="text-slate-400 font-bold">Server Time</span><span>{intervention.drishti_server_time || 'N/A'}</span></div>
          <div className="flex flex-col"><span className="text-slate-400 font-bold">apptype</span><span>{intervention.drishti_apptype || 'N/A'}</span></div>
          <div className="flex flex-col"><span className="text-slate-400 font-bold">appsubtype</span><span>{intervention.drishti_appsubtype || 'N/A'}</span></div>
          <div className="flex flex-col"><span className="text-slate-400 font-bold">FDCprojectname</span><span>{intervention.drishti_fdcprojectname || 'N/A'}</span></div>
          <div className="flex flex-col"><span className="text-slate-400 font-bold">themename</span><span>{intervention.drishti_themename || 'N/A'}</span></div>
          <div className="flex flex-col"><span className="text-slate-400 font-bold">profilename</span><span>{intervention.drishti_profilename || 'N/A'}</span></div>
          <div className="flex flex-col"><span className="text-slate-400 font-bold">observername</span><span>{intervention.drishti_observername || 'N/A'} {intervention.data_status === 'DEMO' ? '(Demo)' : ''}</span></div>
          <div className="flex flex-col"><span className="text-slate-400 font-bold">org</span><span>{intervention.drishti_org || 'N/A'}</span></div>
          <div className="flex flex-col"><span className="text-slate-400 font-bold">mobileno</span><span>{intervention.drishti_mobileno || '-'}</span></div>
          <div className="flex flex-col"><span className="text-slate-400 font-bold">creationtime</span><span>{intervention.drishti_creationtime || 'N/A'}</span></div>
          <div className="flex flex-col"><span className="text-slate-400 font-bold">uuid</span><span className="truncate" title={intervention.drishti_uuid}>{intervention.drishti_uuid || 'N/A'}</span></div>
          <div className="flex flex-col"><span className="text-slate-400 font-bold">deviceid</span><span>{intervention.drishti_deviceid || 'N/A'}</span></div>
          <div className="flex flex-col"><span className="text-slate-400 font-bold">Name</span><span>{intervention.drishti_name || 'N/A'}</span></div>
          <div className="flex flex-col"><span className="text-slate-400 font-bold">StatusOfActivity</span><span>{intervention.drishti_statusofactivity || 'N/A'}</span></div>
          <div className="flex flex-col"><span className="text-slate-400 font-bold">WorkCode</span><span>{intervention.work_code || 'N/A'}</span></div>
          <div className="flex flex-col col-span-2"><span className="text-slate-400 font-bold">Location</span><span>{intervention.drishti_location || 'N/A'}</span></div>
          <div className="flex flex-col"><span className="text-slate-400 font-bold">DateCompletion</span><span>{intervention.drishti_datecompletion || 'N/A'}</span></div>
          <div className="flex flex-col col-span-2"><span className="text-slate-400 font-bold">Details</span><span>{intervention.drishti_details || 'N/A'}</span></div>
        </div>
        <div className="pt-3 border-t text-center">
          <a 
            href="https://bhuvan-app1.nrsc.gov.in/iwmp/" 
            target="_blank" 
            rel="noreferrer"
            title="Built to be compatible with the DRISHTI field-record format used on the government portal."
            className="text-xs text-teal-600 hover:text-teal-800 font-bold hover:underline flex items-center justify-center gap-1"
          >
            Source data schema: DRISHTI field record format — View reference portal ↗
          </a>
        </div>
      </div>
    </div>
  );
}
