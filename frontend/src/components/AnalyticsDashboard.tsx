import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

export default function AnalyticsDashboard({ interventions, demoMode }) {
  const p1 = interventions.filter(i => i.priority === 'P1').length;
  const p2 = interventions.filter(i => i.priority === 'P2').length;
  const p3 = interventions.filter(i => i.priority === 'P3').length;

  const priorityData = [
    { name: 'P1 (Critical)', count: p1, fill: '#ef4444' }, // red-500
    { name: 'P2 (Review)', count: p2, fill: '#f59e0b' },   // amber-500
    { name: 'P3 (Verified)', count: p3, fill: '#10b981' }  // green-500
  ];

  const conflictCount = interventions.filter(i => i.flag_conflict).length;
  const agreementCount = interventions.filter(i => i.data_status !== 'UNAVAILABLE' && !i.flag_conflict).length;
  const agreementData = [
    { name: 'Conflict', value: conflictCount, fill: '#ef4444' },
    { name: 'Agreement', value: agreementCount, fill: '#3b82f6' }
  ];

  const highConf = interventions.filter(i => (i.score_confidence || 0) >= 75).length;
  const medConf = interventions.filter(i => (i.score_confidence || 0) >= 50 && (i.score_confidence || 0) < 75).length;
  const lowConf = interventions.filter(i => (i.score_confidence || 0) < 50 && i.data_status !== 'UNAVAILABLE').length;

  const confData = [
    { name: 'High', count: highConf, fill: '#10b981' },
    { name: 'Medium', count: medConf, fill: '#f59e0b' },
    { name: 'Low', count: lowConf, fill: '#ef4444' }
  ];

  const impactScores = interventions.filter(i => i.score_impact !== null).map(i => ({ name: i.work_code, impact: i.score_impact }));

  return (
    <div className="max-w-6xl mx-auto flex flex-col gap-6">
      <div className="flex justify-between items-center bg-white p-4 rounded-md shadow-sm border border-gray-300">
        <div>
          <h2 className="text-xl font-bold text-gray-800 uppercase tracking-wide">Analytics Dashboard</h2>
          <p className="text-sm text-gray-500 font-medium mt-1">Aggregated insights for PUNE-WDC-1</p>
        </div>
        {demoMode && <div className="bg-amber-100 text-amber-800 border border-amber-300 font-bold px-3 py-1.5 rounded-md shadow-sm text-sm tracking-wide">DEMO MODE ACTIVE</div>}
      </div>

      <div className="grid grid-cols-2 grid-rows-2 gap-6">
        <div className="bg-white p-6 rounded-md border border-gray-300 shadow-sm h-80 flex flex-col">
          <h3 className="text-sm font-bold text-gray-700 uppercase mb-4 tracking-wide border-b border-gray-100 pb-2">Priority Queue Distribution</h3>
          <div className="flex-1 min-h-0">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={priorityData} layout="vertical" margin={{ left: 20, right: 20, top: 10, bottom: 10 }}>
                <XAxis type="number" />
                <YAxis dataKey="name" type="category" width={110} tick={{ fontSize: 12, fill: '#475569', fontWeight: 600 }} />
                <Tooltip cursor={{ fill: '#f8fafc' }} contentStyle={{ borderRadius: '6px', border: '1px solid #cbd5e1' }} />
                <Bar dataKey="count" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white p-6 rounded-md border border-gray-300 shadow-sm h-80 flex flex-col">
          <h3 className="text-sm font-bold text-gray-700 uppercase mb-4 tracking-wide border-b border-gray-100 pb-2">Evidence Source Agreement</h3>
          <div className="flex-1 min-h-0">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={agreementData} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={70} outerRadius={100} label={{ fill: '#334155', fontSize: 12, fontWeight: 600 }}>
                  {agreementData.map((entry, index) => <Cell key={`cell-${index}`} fill={entry.fill} />)}
                </Pie>
                <Tooltip contentStyle={{ borderRadius: '6px', border: '1px solid #cbd5e1' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white p-6 rounded-md border border-gray-300 shadow-sm h-80 flex flex-col">
          <h3 className="text-sm font-bold text-gray-700 uppercase mb-4 tracking-wide border-b border-gray-100 pb-2">Confidence Score Distribution</h3>
          <div className="flex-1 min-h-0">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={confData} margin={{ left: -10, right: 20, top: 10, bottom: 10 }}>
                <XAxis dataKey="name" tick={{ fontSize: 12, fill: '#475569', fontWeight: 600 }} />
                <YAxis />
                <Tooltip cursor={{ fill: '#f8fafc' }} contentStyle={{ borderRadius: '6px', border: '1px solid #cbd5e1' }} />
                <Bar dataKey="count" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white p-6 rounded-md border border-gray-300 shadow-sm h-80 flex flex-col">
          <h3 className="text-sm font-bold text-gray-700 uppercase mb-4 tracking-wide border-b border-gray-100 pb-2">Impact Score Distribution</h3>
          <div className="flex-1 min-h-0">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={impactScores} margin={{ left: -10, right: 20, top: 10, bottom: 10 }}>
                <XAxis dataKey="name" tick={false} />
                <YAxis domain={[0, 100]} />
                <Tooltip cursor={{ fill: '#f8fafc' }} contentStyle={{ borderRadius: '6px', border: '1px solid #cbd5e1' }} />
                <Bar dataKey="impact" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
