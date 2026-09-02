with open("frontend/src/app/page.tsx", "r") as f:
    content = f.read()

# 1. Truncate Email
old_email = """{lead.email && <div className="text-xs text-indigo-600 font-medium mt-1">📧 {lead.email}</div>}"""
new_email = """{lead.email && <div className="text-xs text-indigo-600 font-medium mt-1 w-[150px] xl:w-[200px] truncate" title={lead.email}>📧 {lead.email}</div>}"""
content = content.replace(old_email, new_email)

# 2. Update Header buttons
old_buttons = """          <div className="flex items-center space-x-3 w-full md:w-auto">
            <a
              href="/api/export"
              target="_blank"
              className="flex-1 md:flex-none text-center px-5 py-2.5 bg-emerald-500 text-white rounded-lg hover:bg-emerald-600 hover:shadow-md transition-all duration-200 font-medium text-sm"
            >
              📊 Export Excel
            </a>
            <button
              onClick={handleClear}"""

new_buttons = """          <div className="flex flex-wrap items-center gap-3 w-full md:w-auto">
            <a
              href="/api/export"
              target="_blank"
              className="flex-1 md:flex-none text-center px-5 py-2.5 bg-emerald-500 text-white rounded-lg hover:bg-emerald-600 hover:shadow-md transition-all duration-200 font-medium text-sm whitespace-nowrap"
            >
              📊 Export Excel
            </a>
            <label className="flex-1 md:flex-none text-center px-5 py-2.5 bg-blue-500 text-white rounded-lg hover:bg-blue-600 hover:shadow-md transition-all duration-200 font-medium text-sm cursor-pointer whitespace-nowrap">
              📥 Import Excel/CSV
              <input 
                type="file" 
                accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel" 
                className="hidden" 
                onChange={async (e) => {
                  const file = e.target.files?.[0];
                  if (!file) return;
                  
                  const formData = new FormData();
                  formData.append('file', file);
                  
                  try {
                    const res = await fetch('/api/import', {
                      method: 'POST',
                      body: formData
                    });
                    const data = await res.json();
                    if (data.error) alert(data.error);
                    else {
                      alert(data.message);
                      fetchLeads();
                    }
                  } catch (err) {
                    console.error(err);
                    alert("Failed to upload file");
                  }
                  e.target.value = '';
                }}
              />
            </label>
            <button
              onClick={handleClear}"""

content = content.replace(old_buttons, new_buttons)

with open("frontend/src/app/page.tsx", "w") as f:
    f.write(content)
