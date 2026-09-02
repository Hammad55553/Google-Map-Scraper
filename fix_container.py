with open("frontend/src/app/page.tsx", "r") as f:
    content = f.read()

import re

# Find the main container
pattern = r'<div className="min-h-screen[^"]*">'
replacement = '<div className={`min-h-screen p-4 md:p-8 font-sans selection:bg-indigo-100 transition-colors duration-300 ${isDarkMode ? "dark bg-slate-900 text-slate-100" : "bg-slate-50 text-slate-900"}`}>'

content = re.sub(pattern, replacement, content, count=1)

with open("frontend/src/app/page.tsx", "w") as f:
    f.write(content)
