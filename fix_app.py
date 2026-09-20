with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the start of the damage
# The damage started right after the reasonText div
for i, line in enumerate(lines):
    if "clickedCell.properties.years" in line and "reasonText" in line:
        start_idx = i + 1
        break

# The damage ends where `<li><strong>Administrative Boundary:` is
end_idx = 0
for i, line in enumerate(lines):
    if "Administrative Boundary:</strong>" in line:
        end_idx = i
        break

# The missing content is:
missing = """
              </div>
            </div>
          </div>
        ) : null}
      </main>

      {showSources && <DataSourcesModal onClose={() => setShowSources(false)} interventions={interventions} />}
    </div>
  );
}

function DataSourcesModal({ onClose, interventions = [] }) {
  const conflictCount = interventions.filter(i => i.flag_conflict).length;
  const invalidHydroCount = interventions.filter(i => i.flag_hydro).length;
  const missingCoordsCount = interventions.filter(i => i.data_status === 'UNAVAILABLE').length;

  return (
    <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-[3000] flex items-center justify-center">
      <div className="bg-white rounded-xl shadow-2xl w-[700px] max-h-[80vh] flex flex-col overflow-hidden border border-slate-200">
        <div className="px-6 py-5 border-b border-slate-200 bg-slate-50 flex justify-between items-center">
          <h2 className="text-lg font-black text-slate-800">Data Sources & Authoritative Scope</h2>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-700 text-xl font-bold">&times;</button>
        </div>
        <div className="p-6 overflow-y-auto flex flex-col gap-6">
        
          <div className="bg-blue-50/50 border border-blue-100 rounded-lg p-5">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-2 h-2 rounded-full bg-blue-500"></div>
              <h3 className="text-sm font-bold text-blue-900 uppercase tracking-widest">Accountability Signals (Audit)</h3>
            </div>
            <p className="text-sm text-slate-600 mb-3">The Evidence Engine acts as an automated audit layer, identifying misreporting and anomalies in field data:</p>
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-white border border-blue-100 p-3 rounded shadow-sm text-center">
                <div className="text-2xl font-black text-blue-600 mb-1">{conflictCount}</div>
                <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Evidence Conflicts</div>
              </div>
              <div className="bg-white border border-blue-100 p-3 rounded shadow-sm text-center">
                <div className="text-2xl font-black text-blue-600 mb-1">{invalidHydroCount}</div>
                <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Hydrology Failures</div>
              </div>
              <div className="bg-white border border-blue-100 p-3 rounded shadow-sm text-center">
                <div className="text-2xl font-black text-blue-600 mb-1">{missingCoordsCount}</div>
                <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Missing Coordinates</div>
              </div>
            </div>
          </div>
          
          <div className="bg-green-50/50 border border-green-100 rounded-lg p-5">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-2 h-2 rounded-full bg-green-500"></div>
              <h3 className="text-sm font-bold text-green-900 uppercase tracking-widest">Real & Computed Data</h3>
            </div>
            <ul className="text-sm text-slate-700 flex flex-col gap-3 ml-4 list-disc marker:text-green-300">
"""

new_lines = lines[:start_idx] + [missing] + lines[end_idx:]

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
