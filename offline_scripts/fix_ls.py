with open("frontend/src/components/LeftSidebar.tsx", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('className="w-[300px] shrink-0', 'className="w-full lg:w-[300px] shrink-0 h-auto lg:h-full')
text = text.replace('h-full shadow-md z-20', 'shadow-md z-20')

with open("frontend/src/components/LeftSidebar.tsx", "w", encoding="utf-8") as f:
    f.write(text)
