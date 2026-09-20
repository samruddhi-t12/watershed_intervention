import React from 'react';
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
