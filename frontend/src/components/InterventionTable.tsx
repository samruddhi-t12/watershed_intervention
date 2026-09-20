import React from 'react';

export default function InterventionTable({ interventions, selectedId, onSelect }) {
  const sorted = [...interventions].sort((a, b) => {
    const order = { 'FLAGGED': 1, 'REVIEW': 2, 'VERIFIED': 3 };
    if (order[a.status_badge] !== order[b.status_badge]) return order[a.status_badge] - order[b.status_badge];
    return (b.score_impact || 0) - (a.score_impact || 0);
  });

  return (
    <table className="w-full text-left border-collapse text-sm bg-white">
      <thead className="bg-slate-50 sticky top-0 z-10 shadow-sm border-b border-slate-200">
        <tr>
          <th className="px-4 py-2 font-bold text-slate-500 uppercase tracking-wider text-xs">Work Code</th>
          <th className="px-4 py-2 font-bold text-slate-500 uppercase tracking-wider text-xs">Type</th>
          <th className="px-4 py-2 font-bold text-slate-500 uppercase tracking-wider text-xs">Impact</th>
          <th className="px-4 py-2 font-bold text-slate-500 uppercase tracking-wider text-xs">Conf</th>
          <th className="px-4 py-2 font-bold text-slate-500 uppercase tracking-wider text-xs">Status</th>
          <th className="px-4 py-2 font-bold text-slate-500 uppercase tracking-wider text-xs">Reason</th>
        </tr>
      </thead>
      <tbody>
        {sorted.map(inv => (
          <tr 
            key={inv.id} 
            onClick={() => onSelect(inv.id)}
            className={`cursor-pointer transition-colors border-b border-slate-100 ${selectedId === inv.id ? 'bg-blue-50/60' : 'hover:bg-slate-50'}`}
          >
            <td className="px-4 py-2 font-bold text-slate-800">{inv.work_code}</td>
            <td className="px-4 py-2 text-slate-600 font-medium">{inv.type}</td>
            <td className="px-4 py-2 font-extrabold text-blue-600">{inv.score_impact || '--'}</td>
            <td className="px-4 py-2 font-extrabold text-slate-700">{inv.score_confidence || '--'}</td>
            <td className="px-4 py-2">
              <span className={`text-[10px] font-extrabold px-2 py-1 rounded shadow-sm border ${inv.status_badge === 'REVIEW' ? 'bg-amber-100 text-amber-800 border-amber-300' : inv.status_badge === 'FLAGGED' ? 'bg-red-100 text-red-800 border-red-300' : 'bg-green-100 text-green-800 border-green-300'}`}>
                {inv.status_badge}
              </span>
            </td>
            <td className="px-4 py-2 text-xs text-slate-600 font-medium truncate max-w-xs">{inv.priority_reason}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
