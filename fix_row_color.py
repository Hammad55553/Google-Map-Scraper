with open("frontend/src/app/page.tsx", "r") as f:
    content = f.read()

old_row = """              {leads.map((lead, idx) => (
                <tr key={idx} className="hover:bg-slate-50/80 transition-colors">"""

new_row = """              {leads.map((lead, idx) => (
                <tr key={idx} className={`transition-colors ${lead.status === 'Contacted' ? 'bg-slate-50/80 opacity-75 grayscale-[20%]' : 'hover:bg-slate-50/80'}`}>"""

content = content.replace(old_row, new_row)

with open("frontend/src/app/page.tsx", "w") as f:
    f.write(content)

