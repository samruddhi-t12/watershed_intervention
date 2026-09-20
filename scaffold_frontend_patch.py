import os

frontend_files = {
    "frontend/src/components/InterventionDetail.tsx": """import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function InterventionDetail({ id }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    if (!id) return;
    axios.get(`http://127.0.0.1:8000/api/v1/interventions/${id}`).then(res => setData(res.data));
  }, [id]);

  if (!id) return <div className="text-gray-500 flex items-center justify-center h-full">Select an intervention on the map.</div>;
  if (!data) return <div>Loading...</div>;

  return (
    <div className="flex flex-col gap-4 text-sm">
      <h2 className="text-xl font-bold border-b pb-2">{data.type} - {data.work_code}</h2>
      
      <div className={`p-3 rounded font-bold text-white ${data.priority === 'P1' ? 'bg-red-600' : data.priority === 'P2' ? 'bg-yellow-500' : 'bg-green-600'}`}>
        Priority: {data.priority}
        <div className="font-normal text-xs mt-1">{data.priority_reason}</div>
      </div>

      <div className="bg-slate-100 p-3 rounded">
        <h3 className="font-bold mb-1">Scores</h3>
        <div>Impact: {data.score_impact.toFixed(2)}</div>
        <div>Confidence: {data.score_confidence.toFixed(2)}</div>
        {data.cv_status === "CONFLICT" && (
           <div className="text-red-600 font-bold mt-1">! Evidence Conflict Detected</div>
        )}
      </div>

      <div className="bg-slate-100 p-3 rounded">
        <h3 className="font-bold mb-1">Field Evidence</h3>
        <div>Photo: {data.field_has_photo ? 'Yes' : 'No'}</div>
        <div>Water Presence: {data.field_water_presence}</div>
      </div>

      <div className="bg-slate-100 p-3 rounded">
        <h3 className="font-bold mb-1">Satellite Context (Prototype)</h3>
        <div>SAVI Trend: {data.sat_savi_trend}</div>
        <div>MNDWI Trend: {data.sat_mndwi_trend}</div>
        <div>Hydrologically Valid: {data.ctx_hydro_valid ? 'Yes' : 'No'}</div>
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
