with open("frontend/src/app/page.tsx", "r") as f:
    content = f.read()

old_status = """                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${lead.status === 'Contacted' ? 'bg-indigo-100 text-indigo-800' : 'bg-green-100 text-green-800'}`}>
                      {lead.status}
                    </span>
                  </td>"""
                  
new_status = """                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      lead.status === 'Contacted' ? 'bg-indigo-100 text-indigo-800' : 
                      lead.status === 'Duplicate' ? 'bg-amber-100 text-amber-800' : 
                      'bg-green-100 text-green-800'
                    }`}>
                      {lead.status}
                    </span>
                  </td>"""

content = content.replace(old_status, new_status)

# Fade out duplicates too
old_row = """                <tr key={idx} className={`transition-colors ${lead.status === 'Contacted' ? 'bg-slate-50/80 opacity-75 grayscale-[20%]' : 'hover:bg-slate-50/80'}`}>"""
new_row = """                <tr key={idx} className={`transition-colors ${['Contacted', 'Duplicate'].includes(lead.status) ? 'bg-slate-50/80 opacity-75 grayscale-[20%]' : 'hover:bg-slate-50/80'}`}>"""
content = content.replace(old_row, new_row)

with open("frontend/src/app/page.tsx", "w") as f:
    f.write(content)
