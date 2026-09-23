import re

with open("frontend/src/components/LeftSidebar.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# Replace flex-1 with flex-none lg:flex-1 for the Top half and Bottom half wrappers
text = text.replace('<div className="flex-1 flex flex-col min-h-0">', '<div className="flex-none lg:flex-1 flex flex-col min-h-0">')
text = text.replace('<div className="flex-1 flex flex-col min-h-0 border-t border-slate-300">', '<div className="flex-none lg:flex-1 flex flex-col min-h-0 border-t border-slate-300 mt-4 lg:mt-0">')

# Also fix the inner overflow divs to not have flex-1 on mobile
text = text.replace('<div className="flex-1 p-4 flex flex-col gap-5 overflow-y-auto">', '<div className="flex-none lg:flex-1 p-4 flex flex-col gap-5 overflow-y-visible lg:overflow-y-auto">')
text = text.replace('<div className="flex-1 overflow-y-auto">', '<div className="flex-none lg:flex-1 overflow-y-visible lg:overflow-y-auto h-64 lg:h-auto">')

with open("frontend/src/components/LeftSidebar.tsx", "w", encoding="utf-8") as f:
    f.write(text)
