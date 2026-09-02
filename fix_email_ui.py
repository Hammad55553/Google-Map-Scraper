with open("frontend/src/app/page.tsx", "r") as f:
    content = f.read()

# 1. Add email field to Lead type
old_type = """  has_website: boolean;
  lead_score: number;"""
new_type = """  has_website: boolean;
  email?: string;
  lead_score: number;"""
content = content.replace(old_type, new_type)

# 2. Render the email in the table
old_col = """                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                    {lead.has_website ? '✅ Yes' : '❌ No'}
                  </td>"""
new_col = """                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                    <div>{lead.has_website ? '✅ Web' : '❌ Web'}</div>
                    {lead.email && <div className="text-xs text-indigo-600 font-medium mt-1">📧 {lead.email}</div>}
                  </td>"""
content = content.replace(old_col, new_col)

with open("frontend/src/app/page.tsx", "w") as f:
    f.write(content)
