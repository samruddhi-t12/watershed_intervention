import React, { useEffect, useState } from 'react';
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
