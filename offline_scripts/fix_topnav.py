import re

with open("frontend/src/components/TopNav.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update header classes to allow wrapping and wrapping padding on mobile
text = text.replace(
    '<header className="bg-white text-slate-800 flex items-center justify-between px-6 py-3 shrink-0 shadow-sm border-b border-slate-200 relative z-40 gap-4 overflow-visible">',
    '<header className="bg-white text-slate-800 flex flex-wrap md:flex-nowrap items-center justify-between px-4 md:px-6 py-3 shrink-0 shadow-sm border-b border-slate-200 relative z-40 gap-3 md:gap-4 overflow-visible">'
)

# 2. Update search bar container to wrap correctly (order-last on mobile)
text = text.replace(
    '<div className="flex-1 flex justify-center min-w-[200px] max-w-md shrink relative">',
    '<div className="flex-1 flex justify-center min-w-[200px] max-w-none md:max-w-md shrink relative w-full order-3 md:order-none mt-1 md:mt-0">'
)

# 3. Logo text size and padding adjustments for mobile
text = text.replace(
    '<div className="font-black text-xl tracking-tight text-slate-800 flex items-center gap-2">',
    '<div className="font-black text-lg md:text-xl tracking-tight text-slate-800 flex items-center gap-1.5 md:gap-2">'
)
text = text.replace(
    '<div className="text-sm font-extrabold text-slate-500 tracking-wide uppercase">PUNE-WDC-1</div>',
    '<div className="text-xs md:text-sm font-extrabold text-slate-500 tracking-wide uppercase">PUNE-WDC-1</div>'
)

# 4. Hide DEMO mode text on very small screens, keep just checkbox, or shrink it
text = text.replace(
    '<label className="flex items-center gap-2 text-xs font-bold bg-slate-50 px-3 py-1.5 rounded-full border border-slate-200 cursor-pointer whitespace-nowrap shadow-sm">',
    '<label className="flex items-center gap-1.5 md:gap-2 text-[10px] md:text-xs font-bold bg-slate-50 px-2 md:px-3 py-1 md:py-1.5 rounded-full border border-slate-200 cursor-pointer whitespace-nowrap shadow-sm">'
)
text = text.replace(
    '<span className={demoMode ? "text-amber-600" : "text-slate-500"}>DEMO MODE</span>',
    '<span className={demoMode ? "text-amber-600" : "text-slate-500"}><span className="hidden sm:inline">DEMO </span>MODE</span>'
)

# 5. Profile circle slightly smaller on mobile
text = text.replace(
    '<div className="w-9 h-9 rounded-full bg-teal-100 flex items-center justify-center text-sm font-extrabold text-teal-800 border border-teal-200 shadow-sm shrink-0">NR</div>',
    '<div className="w-7 h-7 md:w-9 md:h-9 rounded-full bg-teal-100 flex items-center justify-center text-xs md:text-sm font-extrabold text-teal-800 border border-teal-200 shadow-sm shrink-0">NR</div>'
)

with open("frontend/src/components/TopNav.tsx", "w", encoding="utf-8") as f:
    f.write(text)

print("TopNav layout updated for mobile.")
