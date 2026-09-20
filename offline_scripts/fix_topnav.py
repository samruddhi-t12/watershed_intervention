with open("frontend/src/components/TopNav.tsx", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("\\`", "`")
text = text.replace("\\${", "${")

with open("frontend/src/components/TopNav.tsx", "w", encoding="utf-8") as f:
    f.write(text)
