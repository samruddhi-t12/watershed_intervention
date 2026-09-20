import React from 'react';

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
