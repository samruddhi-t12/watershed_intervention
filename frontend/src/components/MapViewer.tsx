import React, { useEffect, useState, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, GeoJSON, ImageOverlay } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import axios from 'axios';
import 'leaflet-side-by-side';

import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25,41],
    iconAnchor: [12,41]
});
L.Marker.prototype.options.icon = DefaultIcon;

const MapController = ({ interventions, selectedId, bounds, clickedCell }) => {
  const map = useMap();
  useEffect(() => {
    map.invalidateSize();
    if (selectedId) {
      const inv = interventions.find(i => i.id === selectedId);
      if (inv && inv.lat && inv.lng) {
        map.flyTo([inv.lat, inv.lng], 16, { animate: true });
      }
    } else if (clickedCell) {
        // Fly to clicked cell center? Or just let it be.
    } else if (bounds) {
      map.fitBounds(bounds, { padding: [20, 20] });
    }
  }, [selectedId, interventions, map, bounds]);
  return null;
};

const getColor = (changeClass) => {
  switch (changeClass) {
    case 'severe_degradation': return '#8B0000';
    case 'moderate_degradation': return '#E07B39';
    case 'stable': return '#C7C7C7';
    case 'improving': return '#90C978';
    case 'strong_improvement': return '#1B5E20';
    default: return '#000000';
  }
};

const LegendControl = () => {
  const map = useMap();
  useEffect(() => {
    const legend = L.control({ position: 'bottomright' });
    legend.onAdd = () => {
      const div = L.DomUtil.create('div', 'bg-white/95 backdrop-blur-sm p-2 lg:p-4 border border-slate-200 rounded-lg lg:rounded-xl shadow-lg z-[1000] text-[9px] lg:text-xs font-sans m-2 lg:m-4 max-w-[150px] lg:max-w-none');
        div.innerHTML = `
          <div class="flex flex-col border-b border-slate-200 pb-1 lg:pb-2 mb-1 lg:mb-2">
            <div class="font-extrabold text-slate-800 uppercase tracking-widest mb-0.5 lg:mb-1 text-[9px] lg:text-xs">Analysis Index</div>
            <div class="text-[8px] lg:text-[10px] text-slate-500 font-medium flex items-center gap-1 leading-tight">
               <span class="hidden lg:inline">⚠️</span> <span class="hidden lg:inline">This analysis uses synthetic trend data — see Data Sources for details</span><span class="lg:hidden">Synthetic data</span>
            </div>
          </div>
          <div class="flex flex-col gap-1 lg:gap-2">
            <div class="flex items-center gap-1.5 lg:gap-3"><div class="w-2.5 h-2.5 lg:w-4 lg:h-4 rounded-sm border border-slate-400" style="background:#8B0000"></div><span class="font-bold text-slate-700">Severe Deg.</span></div>
            <div class="flex items-center gap-1.5 lg:gap-3"><div class="w-2.5 h-2.5 lg:w-4 lg:h-4 rounded-sm border border-slate-400" style="background:#E07B39"></div><span class="font-bold text-slate-700">Mod. Deg.</span></div>
            <div class="flex items-center gap-1.5 lg:gap-3"><div class="w-2.5 h-2.5 lg:w-4 lg:h-4 rounded-sm border border-slate-400" style="background:#C7C7C7"></div><span class="font-bold text-slate-700">Stable</span></div>
            <div class="flex items-center gap-1.5 lg:gap-3"><div class="w-2.5 h-2.5 lg:w-4 lg:h-4 rounded-sm border border-slate-400" style="background:#90C978"></div><span class="font-bold text-slate-700">Improving</span></div>
            <div class="flex items-center gap-1.5 lg:gap-3"><div class="w-2.5 h-2.5 lg:w-4 lg:h-4 rounded-sm border border-slate-400" style="background:#1B5E20"></div><span class="font-bold text-slate-700">Strong Imp.</span></div>
          </div>
        `;
      L.DomEvent.disableClickPropagation(div);
      return div;
    };
    legend.addTo(map);
    return () => { legend.remove(); };
  }, [map]);
  return null;
};

const InjectSmoothingCSS = () => {
  useEffect(() => {
    const style = document.createElement('style');
    style.innerHTML = `
      .smooth-grid-pane svg path {
        stroke: none !important;
        stroke-width: 0 !important;
      }
      .smooth-grid-pane svg {
        filter: blur(8px) saturate(1.2);
        opacity: 0.85;
      }
    `;
    document.head.appendChild(style);
    return () => document.head.removeChild(style);
  }, []);
  return null;
};

export default function MapViewer({ interventions, selectedId, onSelect, baseMap, activeLayers, demoMode, selectedYear, compareYear, swipeMode, setClickedCell }) {
  const [watershedData, setWatershedData] = useState(null);
  const [gridData, setGridData] = useState(null);
  const [streamData, setStreamData] = useState(null);
  
  const mapRef = useRef(null);
  const layerRightRef = useRef(null);
  const layerLeftRef = useRef(null);
  const sideBySideRef = useRef(null);

  useEffect(() => {
    axios.get('/watershed_real.geojson').then(res => setWatershedData(res.data)).catch(()=>{});
    axios.get('/real_streams.geojson').then(res => setStreamData(res.data)).catch(()=>{});
    axios.get('/change_grid.geojson').then(res => setGridData(res.data)).catch(()=>{});
  }, []);

  const getBaseUrl = () => {
    switch (baseMap) {
      case 'Terrain': return 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png';
      case 'Street': return 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
      case 'Satellite': default: return 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
    }
  };

  const mapYear = (tLabel) => `202${parseInt(tLabel.replace('T', '')) + 1}`;

  const styleCell = (feature, tLabel) => {
    const yearStr = mapYear(tLabel);
    const data = feature.properties.years[yearStr];
    let color = data ? getColor(data.changeClass) : 'transparent';
    return {
      fillColor: color,
      weight: 0,
      opacity: 0, 
      fillOpacity: 1 
    };
  };

  const bounds = React.useMemo(() => {
    return watershedData ? L.geoJSON(watershedData).getBounds() : [[18.80, 73.80], [18.90, 73.95]];
  }, [watershedData]);
  const showChangeMaps = activeLayers.includes('Integrated Change Index (SCI)') || activeLayers.includes('Vegetation (SAVI)') || activeLayers.includes('Water Conservation (MNDWI)');

  useEffect(() => {
    if (mapRef.current && swipeMode && showChangeMaps) {
      const map = mapRef.current;
      if (!sideBySideRef.current && L.control.sideBySide) {
        if (layerLeftRef.current && layerRightRef.current) {
          sideBySideRef.current = L.control.sideBySide(layerLeftRef.current, layerRightRef.current);
          sideBySideRef.current.addTo(map);
        }
      }
    } else {
      if (sideBySideRef.current) {
        sideBySideRef.current.remove();
        sideBySideRef.current = null;
      }
    }
  }, [swipeMode, showChangeMaps]);

  const SwipeableGeoJSON = ({ data, tLabel, isLeft, onEachFeature }) => {
    const map = useMap();
    useEffect(() => {
      const paneName = isLeft ? 'leftPane' : 'rightPane';
      if (!map.getPane(paneName)) {
        map.createPane(paneName);
        map.getPane(paneName).style.zIndex = 400;
        map.getPane(paneName).classList.add('smooth-grid-pane');
      }
      
      // We MUST use a distinct canvas renderer for EACH pane so side-by-side can clip them properly.
      const customRenderer = L.canvas({ pane: paneName });
      
      const layer = L.geoJSON(data, { 
        style: (f) => styleCell(f, tLabel), 
        onEachFeature,
        pane: paneName,
        renderer: customRenderer
      });
      
      layer.getContainer = () => map.getPane(paneName);
      
      if (isLeft) layerLeftRef.current = layer;
      else layerRightRef.current = layer;
      layer.addTo(map);
      
      return () => {
        if (sideBySideRef.current) {
          sideBySideRef.current.remove();
          sideBySideRef.current = null;
        }
        map.removeLayer(layer);
        if (isLeft) layerLeftRef.current = null;
        else layerRightRef.current = null;
      };
    }, [map, data, tLabel, isLeft, onEachFeature]);
    return null;
  };

  const CustomPanes = () => {
    const map = useMap();
    useEffect(() => {
      if (!map.getPane('labelsPane')) {
        map.createPane('labelsPane');
        map.getPane('labelsPane').style.zIndex = 450;
        map.getPane('labelsPane').style.pointerEvents = 'none';
      }
    }, [map]);
    return null;
  };

  const SmoothGeoJSON = ({ data, tLabel, onEachFeature }) => {
    const map = useMap();
    useEffect(() => {
      const paneName = 'smoothPane';
      if (!map.getPane(paneName)) {
        map.createPane(paneName);
        map.getPane(paneName).style.zIndex = 400;
        map.getPane(paneName).classList.add('smooth-grid-pane');
      }
      
      const customRenderer = L.canvas({ pane: paneName });
      const layer = L.geoJSON(data, { 
        style: (f) => styleCell(f, tLabel), 
        onEachFeature,
        pane: paneName,
        renderer: customRenderer
      });
      
      layer.addTo(map);
      return () => { map.removeLayer(layer); };
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [data, tLabel, map]);
    return null;
  };

  return (
    <div className="w-full h-full relative">
      <InjectSmoothingCSS />
      <MapContainer 
        center={[18.85, 73.85]} 
        zoom={13} 
        style={{ height: '100%', width: '100%', background: '#e2e8f0', zIndex: 0 }} 
        zoomControl={true}
        ref={mapRef}
      >
        <TileLayer url={getBaseUrl()} />
        
        {activeLayers.includes('Terrain Relief') && (
          <ImageOverlay
            url="/hillshade.png"
            bounds={[[18.56958333334275, 73.46458333327573], [19.13208333334262, 74.09374999994225]]}
            opacity={0.6}
            className="mix-blend-multiply"
          />
        )}
        
        {/* Real GIS label overlay so village names appear over imagery */}
        <CustomPanes />
        {baseMap === 'Satellite' && (
          <TileLayer 
            url="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}" 
            pane="labelsPane"
          />
        )}

        <MapController interventions={interventions} selectedId={selectedId} bounds={bounds} />

        {activeLayers.includes('Project Boundary') && watershedData && (
          <GeoJSON 
            data={watershedData} 
            style={{ color: '#0f172a', weight: 4, fillOpacity: 0, opacity: 0.8 }} 
          />
        )}
        
        {activeLayers.includes('Hydrology') && streamData && (
          <GeoJSON 
            data={streamData} 
            style={{ color: '#3b82f6', weight: 2, opacity: 0.9 }} 
          />
        )}

        {showChangeMaps && gridData && (
          <>
            {swipeMode ? (
              <>
                <SwipeableGeoJSON 
                  isLeft={true} data={gridData} tLabel={selectedYear} 
                  onEachFeature={(f, l) => l.on('click', (e) => { L.DomEvent.stopPropagation(e); setClickedCell(f); })}
                />
                <SwipeableGeoJSON 
                  isLeft={false} data={gridData} tLabel={compareYear} 
                  onEachFeature={(f, l) => l.on('click', (e) => { L.DomEvent.stopPropagation(e); setClickedCell(f); })}
                />
              </>
            ) : (
              <SmoothGeoJSON 
                key={`grid-${selectedYear}`}
                data={gridData} 
                tLabel={selectedYear}
                onEachFeature={(f, l) => {
                  l.on('click', (e) => {
                    L.DomEvent.stopPropagation(e);
                    setClickedCell(f);
                  });
                }}
              />
            )}
            <LegendControl />
          </>
        )}

        {activeLayers.includes('Interventions (Check Dams)') && interventions.filter(i => i.lat && i.lng).map(inv => (
          <Marker 
            key={inv.id} 
            position={[inv.lat, inv.lng]}
            eventHandlers={{ click: (e) => { L.DomEvent.stopPropagation(e); onSelect(inv.id); } }}
          >
            <Popup className="text-sm font-sans rounded-xl p-0 overflow-hidden border-0 shadow-lg">
              <div className="bg-slate-50 border-b border-slate-200 px-3 py-2 font-black text-slate-800 uppercase tracking-widest text-xs">Check Dam</div>
              <div className="p-3">
                <div className="text-slate-600 font-medium mb-1">{inv.work_code}</div>
                <button className="bg-teal-600 hover:bg-teal-500 text-white font-bold w-full mt-2 py-1.5 rounded transition-colors" onClick={() => onSelect(inv.id)}>Inspect Evidence</button>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
