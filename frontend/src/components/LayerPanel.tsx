import React from 'react';

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
