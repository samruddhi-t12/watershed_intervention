import os

files = {
    "frontend/src/App.tsx": """import React, { useState, useEffect } from 'react';
import axios from 'axios';
import GISMap from './components/GISMap';
import LayerPanel from './components/LayerPanel';
import EvidencePanel from './components/EvidencePanel';

export default function App() {
  const [interventions, setInterventions] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [selectedId, setSelectedId] = useState(null);
  const [activeLayers, setActiveLayers] = useState(['Interventions', 'Watershed']);
  const [baseMap, setBaseMap] = useState('Satellite');
  const [isBefore, setIsBefore] = useState(false);

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

  const selectedInv = interventions.find(i => i.id === selectedId);

  return (
    <div className="h-screen w-full flex flex-col bg-slate-50 text-slate-900 font-sans overflow-hidden">
      <header className="bg-slate-900 text-white p-3 shrink-0 flex justify-between items-center shadow-md z-50">
        <div className="flex items-center gap-4">
          <h1 className="text-xl font-bold tracking-wide">SIH26015 | Watershed Evidence Intelligence</h1>
          <span className="text-sm px-2 py-1 bg-slate-700 rounded text-slate-300">WDC-PMKSY 2.0 — Khed, Pune</span>
        </div>
        <div className="flex gap-4 text-sm items-center">
          <div className="px-3 py-1 bg-blue-600 rounded font-bold shadow-sm cursor-pointer" onClick={() => setSelectedId(1)}>
            Demo Scenario: Case A
          </div>
          <div className="px-3 py-1 bg-blue-600 rounded font-bold shadow-sm cursor-pointer" onClick={() => setSelectedId(3)}>
            Case C (Conflict)
          </div>
          <div className="text-yellow-400 font-bold px-3 py-1 bg-slate-800 rounded">
            PROTOTYPE / DEMO DATA
          </div>
        </div>
      </header>
      
      <main className="flex-1 flex overflow-hidden">
        {/* LEFT PANEL */}
        <div className="w-64 bg-white border-r shadow-lg z-10 flex flex-col">
          <LayerPanel 
            baseMap={baseMap} setBaseMap={setBaseMap} 
            activeLayers={activeLayers} setActiveLayers={setActiveLayers}
            isBefore={isBefore} setIsBefore={setIsBefore}
          />
          <div className="mt-auto p-4 border-t bg-slate-50 text-xs text-slate-500">
            {metrics && (
              <div>
                <strong>Queue:</strong> P1: {metrics.p1} | P2: {metrics.p2} | P3: {metrics.p3}
              </div>
            )}
          </div>
        </div>
        
        {/* CENTER MAP */}
        <div className="flex-1 relative bg-slate-200">
          <GISMap 
            baseMap={baseMap} 
            activeLayers={activeLayers} 
            interventions={interventions}
            selectedId={selectedId}
            onSelect={setSelectedId}
            isBefore={isBefore}
          />
        </div>
        
        {/* RIGHT PANEL */}
        {selectedId && (
          <div className="w-96 bg-white border-l shadow-2xl z-20 flex flex-col overflow-y-auto">
            <EvidencePanel intervention={selectedInv} activeLayers={activeLayers} />
          </div>
        )}
      </main>
    </div>
  );
}
""",
    "frontend/src/components/LayerPanel.tsx": """import React from 'react';

export default function LayerPanel({ baseMap, setBaseMap, activeLayers, setActiveLayers, isBefore, setIsBefore }) {
  const toggleLayer = (layer) => {
    if (activeLayers.includes(layer)) {
      setActiveLayers(activeLayers.filter(l => l !== layer));
    } else {
      setActiveLayers([...activeLayers, layer]);
    }
  };

  const BaseMapOption = ({ label }) => (
    <label className="flex items-center gap-2 text-sm cursor-pointer p-1 hover:bg-slate-50 rounded">
      <input type="radio" checked={baseMap === label} onChange={() => setBaseMap(label)} className="text-blue-600" />
      {label}
    </label>
  );

  const LayerOption = ({ label }) => (
    <label className="flex items-center gap-2 text-sm cursor-pointer p-1 hover:bg-slate-50 rounded">
      <input type="checkbox" checked={activeLayers.includes(label)} onChange={() => toggleLayer(label)} className="rounded text-blue-600" />
      {label}
    </label>
  );

  return (
    <div className="p-4 flex flex-col gap-6 overflow-y-auto">
      <div>
        <h3 className="font-bold text-slate-700 mb-2 border-b pb-1">BASE MAPS</h3>
        <div className="flex flex-col gap-1">
          <BaseMapOption label="Map" />
          <BaseMapOption label="Satellite" />
          <BaseMapOption label="Hybrid" />
          <BaseMapOption label="Terrain" />
        </div>
      </div>

      <div>
        <h3 className="font-bold text-slate-700 mb-2 border-b pb-1">CONTEXT & HYDROLOGY</h3>
        <div className="flex flex-col gap-1">
          <LayerOption label="Watershed" />
          <LayerOption label="Hydrology" />
          <LayerOption label="Interventions" />
          <LayerOption label="Reference Zones" />
        </div>
      </div>

      <div>
        <h3 className="font-bold text-slate-700 mb-2 border-b pb-1">ANALYTICAL LAYERS</h3>
        <div className="flex flex-col gap-1">
          <LayerOption label="Vegetation - SAVI" />
          <LayerOption label="Water - MNDWI" />
        </div>
      </div>

      <div className="bg-slate-100 p-3 rounded shadow-inner">
        <h3 className="font-bold text-slate-700 mb-2">TEMPORAL STATE</h3>
        <div className="flex gap-2">
          <button 
            className={`flex-1 py-1 text-sm rounded border ${isBefore ? 'bg-white font-bold shadow' : 'bg-transparent text-slate-500'}`}
            onClick={() => setIsBefore(true)}
          >
            BEFORE
          </button>
          <button 
            className={`flex-1 py-1 text-sm rounded border ${!isBefore ? 'bg-white font-bold shadow' : 'bg-transparent text-slate-500'}`}
            onClick={() => setIsBefore(false)}
          >
            AFTER
          </button>
        </div>
      </div>
    </div>
  );
}
""",
    "frontend/src/components/EvidencePanel.tsx": """import React from 'react';

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
            <span className={`font-bold px-2 py-0.5 rounded ${intervention.ctx_hydro_valid ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
              {intervention.ctx_hydro_valid ? 'VALID' : 'FLAGGED'}
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
    </div>
  );
}
""",
    "frontend/src/components/DynamicLegend.tsx": """import React from 'react';

export default function DynamicLegend({ activeLayers }) {
  if (!activeLayers.includes('Vegetation - SAVI') && !activeLayers.includes('Water - MNDWI')) return null;

  return (
    <div className="absolute bottom-6 right-6 bg-white p-3 rounded shadow-lg z-[1000] border text-xs w-48">
      {activeLayers.includes('Vegetation - SAVI') && (
        <div className="mb-3">
          <div className="font-bold mb-1">SAVI (Vegetation)</div>
          <div className="h-3 w-full bg-gradient-to-r from-yellow-800 via-yellow-200 to-green-700 rounded mb-1"></div>
          <div className="flex justify-between text-slate-500"><span>Low</span><span>High</span></div>
        </div>
      )}
      {activeLayers.includes('Water - MNDWI') && (
        <div>
          <div className="font-bold mb-1">MNDWI (Water)</div>
          <div className="h-3 w-full bg-gradient-to-r from-orange-200 via-white to-blue-600 rounded mb-1"></div>
          <div className="flex justify-between text-slate-500"><span>Low</span><span>High</span></div>
        </div>
      )}
    </div>
  );
}
""",
    "frontend/src/components/GISMap.tsx": """import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, GeoJSON, Circle, useMap } from 'react-leaflet';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import DynamicLegend from './DynamicLegend';

import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25,41],
    iconAnchor: [12,41]
});
L.Marker.prototype.options.icon = DefaultIcon;

const MapController = ({ selectedId, interventions }) => {
  const map = useMap();
  useEffect(() => {
    if (selectedId) {
      const inv = interventions.find(i => i.id === selectedId);
      if (inv) map.flyTo([inv.lat, inv.lng], 16);
    }
  }, [selectedId, interventions, map]);
  return null;
};

export default function GISMap({ baseMap, activeLayers, interventions, selectedId, onSelect, isBefore }) {
  const [hydroData, setHydroData] = useState(null);
  const [saviData, setSaviData] = useState(null);
  const [mndwiData, setMndwiData] = useState(null);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/v1/layers/hydrology').then(res => setHydroData(res.data)).catch(()=>{});
    axios.get('http://127.0.0.1:8000/api/v1/layers/savi').then(res => setSaviData(res.data)).catch(()=>{});
    axios.get('http://127.0.0.1:8000/api/v1/layers/mndwi').then(res => setMndwiData(res.data)).catch(()=>{});
  }, []);

  const getBaseUrl = () => {
    switch (baseMap) {
      case 'Satellite': return 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
      case 'Terrain': return 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png';
      case 'Hybrid': return 'https://{s}.google.com/vt/lyrs=y&x={x}&y={y}&z={z}'; // Mocking with a generic xyz if needed, but sticking to standard OSM
      case 'Map': default: return 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    }
  };

  const styleSavi = (feature) => {
    const val = isBefore ? feature.properties.value_before : feature.properties.value_after;
    // Map -1 to 1 to color
    const g = Math.floor(((val + 1) / 2) * 255);
    return { fillColor: `rgb(50, ${g}, 50)`, weight: 0, fillOpacity: 0.5 };
  };

  const styleMndwi = (feature) => {
    const val = isBefore ? feature.properties.value_before : feature.properties.value_after;
    const b = Math.floor(((val + 1) / 2) * 255);
    return { fillColor: `rgb(50, 100, ${b})`, weight: 0, fillOpacity: 0.5 };
  };

  const selectedInv = interventions.find(i => i.id === selectedId);

  return (
    <div className="h-full w-full relative">
      <MapContainer center={[18.850, 73.850]} zoom={13} style={{ height: '100%', width: '100%' }}>
        <TileLayer 
          url={baseMap === 'Hybrid' ? 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}' : getBaseUrl()} 
        />
        {baseMap === 'Hybrid' && (
          <TileLayer url="https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lines/{z}/{x}/{y}.png" opacity={0.5} />
        )}

        <MapController selectedId={selectedId} interventions={interventions} />

        {activeLayers.includes('Vegetation - SAVI') && saviData && saviData.type === 'FeatureCollection' && (
          <GeoJSON key={`savi-${isBefore}`} data={saviData} style={styleSavi} />
        )}
        
        {activeLayers.includes('Water - MNDWI') && mndwiData && mndwiData.type === 'FeatureCollection' && (
          <GeoJSON key={`mndwi-${isBefore}`} data={mndwiData} style={styleMndwi} />
        )}

        {activeLayers.includes('Hydrology') && hydroData && hydroData.type === 'FeatureCollection' && (
          <GeoJSON 
            data={hydroData} 
            style={(f) => ({ color: f.properties.order === 1 ? '#60a5fa' : '#2563eb', weight: f.properties.order * 2 })}
            onEachFeature={(f, l) => l.bindPopup(`Stream Order: ${f.properties.order}`)}
          />
        )}

        {activeLayers.includes('Reference Zones') && selectedInv && (
          <>
            <Circle center={[selectedInv.lat, selectedInv.lng]} radius={500} pathOptions={{ color: 'white', dashArray: '5, 10', fillOpacity: 0.1 }} />
            <Circle center={[selectedInv.lat, selectedInv.lng]} radius={50} pathOptions={{ color: 'red', fillOpacity: 0.3 }} />
          </>
        )}

        {activeLayers.includes('Interventions') && interventions.map((inv) => (
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
      <DynamicLegend activeLayers={activeLayers} />
    </div>
  );
}
"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Frontend GIS Redesign completed.")
