import React, { useState, useEffect } from 'react';
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
