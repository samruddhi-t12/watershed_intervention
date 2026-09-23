import re

with open("frontend/src/components/MapViewer.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# We will use re.sub to replace the entire div.innerHTML assignment for the legend
pattern = re.compile(r"const div = L\.DomUtil\.create\('div', 'bg-white[^;]+;\s+div\.innerHTML = `.*?`;", re.DOTALL)

replacement = """const div = L.DomUtil.create('div', 'bg-white/95 backdrop-blur-sm p-2 lg:p-4 border border-slate-200 rounded-lg lg:rounded-xl shadow-lg z-[1000] text-[9px] lg:text-xs font-sans m-2 lg:m-4 max-w-[150px] lg:max-w-none');
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
        `;"""

new_text = pattern.sub(replacement, text)

with open("frontend/src/components/MapViewer.tsx", "w", encoding="utf-8") as f:
    f.write(new_text)
