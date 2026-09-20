import React from 'react';

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
