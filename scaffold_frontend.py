import os

frontend_files = {
    "frontend/tailwind.config.js": """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
""",
    "frontend/postcss.config.js": """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
""",
    "frontend/src/index.css": """@tailwind base;
@tailwind components;
@tailwind utilities;

html, body, #root {
  height: 100%;
  margin: 0;
  padding: 0;
  font-family: system-ui, -apple-system, sans-serif;
  background-color: #f3f4f6;
}
""",
    "frontend/src/App.tsx": """import React from 'react';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <div className="h-full w-full flex flex-col">
      <header className="bg-slate-900 text-white p-4 shrink-0 flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold">SIH26015 MVP</h1>
          <p className="text-sm text-slate-400">Study Area: WDC-PMKSY 2.0 — Khed, Pune</p>
        </div>
        <div className="text-sm px-3 py-1 bg-slate-800 rounded">
          Demo Mode
        </div>
      </header>
      <main className="flex-1 overflow-hidden">
        <Dashboard />
      </main>
    </div>
  );
}
export default App;
""",
    "frontend/src/components/Dashboard.tsx": """import React, { useState, useEffect } from 'react';
import InteractiveMap from './InteractiveMap';
import InterventionDetail from './InterventionDetail';
import PriorityQueue from './PriorityQueue';
import axios from 'axios';

export default function Dashboard() {
  const [interventions, setInterventions] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [selectedId, setSelectedId] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/v1/interventions');
      setInterventions(res.data);
      const metricsRes = await axios.get('http://127.0.0.1:8000/api/v1/dashboard/metrics');
      setMetrics(metricsRes.data);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="flex h-full w-full p-4 gap-4">
      <div className="w-1/4 flex flex-col gap-4 overflow-y-auto">
        {metrics && (
          <div className="bg-white p-4 rounded shadow">
            <h2 className="font-bold text-lg mb-2">Metrics</h2>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div className="bg-slate-100 p-2 rounded">Total: {metrics.total}</div>
              <div className="bg-red-100 p-2 rounded">P1: {metrics.p1}</div>
              <div className="bg-yellow-100 p-2 rounded">P2: {metrics.p2}</div>
              <div className="bg-green-100 p-2 rounded">P3: {metrics.p3}</div>
              <div className="bg-blue-100 p-2 rounded">Conflicts: {metrics.conflicts}</div>
            </div>
          </div>
        )}
        <PriorityQueue interventions={interventions} onSelect={setSelectedId} />
      </div>
      
      <div className="w-1/2 rounded shadow overflow-hidden bg-white relative">
         <InteractiveMap interventions={interventions} selectedId={selectedId} onSelect={setSelectedId} />
      </div>
      
      <div className="w-1/4 rounded shadow bg-white p-4 overflow-y-auto">
        <InterventionDetail id={selectedId} />
      </div>
    </div>
  );
}
""",
    "frontend/src/components/InteractiveMap.tsx": """import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25,41],
    iconAnchor: [12,41]
});
L.Marker.prototype.options.icon = DefaultIcon;

export default function InteractiveMap({ interventions, selectedId, onSelect }) {
  // Center roughly on Pune: 18.847, 73.896
  return (
    <MapContainer center={[18.848, 73.897]} zoom={15} style={{ height: '100%', width: '100%' }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {interventions.map((inv) => (
        <Marker 
          key={inv.id} 
          position={[inv.lat, inv.lng]}
          eventHandlers={{ click: () => onSelect(inv.id) }}
        >
          <Popup>
            <strong>{inv.work_code}</strong><br/>
            Priority: {inv.priority}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
""",
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
           <div className="text-red-600 font-bold mt-1">⚠️ Evidence Conflict Detected</div>
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
""",
    "frontend/src/components/PriorityQueue.tsx": """import React from 'react';

export default function PriorityQueue({ interventions, onSelect }) {
  const sorted = [...interventions].sort((a,b) => a.priority.localeCompare(b.priority));
  
  return (
    <div className="bg-white p-4 rounded shadow flex-1 overflow-y-auto">
      <h2 className="font-bold text-lg mb-2">Priority Queue</h2>
      <div className="flex flex-col gap-2 text-sm">
        {sorted.map(inv => (
          <div 
            key={inv.id} 
            className="p-2 border rounded cursor-pointer hover:bg-slate-50 flex justify-between items-center"
            onClick={() => onSelect(inv.id)}
          >
            <div>
              <div className="font-bold">{inv.work_code}</div>
              <div className="text-xs text-gray-500">{inv.type}</div>
            </div>
            <div className={`px-2 py-1 rounded text-white font-bold ${inv.priority === 'P1' ? 'bg-red-600' : inv.priority === 'P2' ? 'bg-yellow-500' : 'bg-green-600'}`}>
              {inv.priority}
            </div>
          </div>
        ))}
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
