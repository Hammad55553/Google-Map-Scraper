with open("frontend/src/app/page.tsx", "r") as f:
    content = f.read()

# Update the "Status" column display
old_status = """                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                      {lead.status}
                    </span>
                  </td>"""

new_status = """                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${lead.status === 'Contacted' ? 'bg-indigo-100 text-indigo-800' : 'bg-green-100 text-green-800'}`}>
                      {lead.status}
                    </span>
                  </td>"""
content = content.replace(old_status, new_status)

# Replace the temporary React state badge with the persistent DB status check
old_badge = """{sentEmailIds.includes(lead.id) && (
                      <span className="text-emerald-700 bg-emerald-50 px-3 py-1 rounded border border-emerald-200 text-xs font-bold flex items-center">
                        ✅ Sent
                      </span>
                    )}"""
                    
new_badge = """{(sentEmailIds.includes(lead.id) || lead.status === 'Contacted') && (
                      <span className="text-emerald-700 bg-emerald-50 px-3 py-1 rounded border border-emerald-200 text-xs font-bold flex items-center">
                        ✅ Sent
                      </span>
                    )}"""
                    
content = content.replace(old_badge, new_badge)

with open("frontend/src/app/page.tsx", "w") as f:
    f.write(content)
