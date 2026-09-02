import re

with open("frontend/src/app/page.tsx", "r") as f:
    content = f.read()

# 1. Update main container and header
old_header = """    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        
        <header className="flex justify-between items-center bg-white p-6 rounded-lg shadow">
          <h1 className="text-2xl font-bold text-gray-800">B2B Lead Generation System</h1>
          <div className="flex items-center space-x-4">
            <a
              href="/api/export"
              target="_blank"
              className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition"
            >
              Export to Excel
            </a>
            <button
              onClick={handleClear}
              className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
            >
              Clear All Leads
            </button>
          </div>
        </header>"""

new_header = """    <div className="min-h-screen bg-slate-50 p-4 md:p-8 text-slate-900 font-sans selection:bg-indigo-100">
      <div className="max-w-7xl mx-auto space-y-8">
        
        <header className="flex flex-col md:flex-row justify-between items-start md:items-center bg-white p-6 md:p-8 rounded-2xl shadow-sm border border-slate-100 gap-4 md:gap-0">
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight text-slate-900 flex items-center gap-2">
              <span className="text-indigo-600">⚡</span> LeadGen Pro
            </h1>
            <p className="text-sm text-slate-500 mt-1 font-medium">B2B Lead Generation & Outreach System</p>
          </div>
          <div className="flex items-center space-x-3 w-full md:w-auto">
            <a
              href="/api/export"
              target="_blank"
              className="flex-1 md:flex-none text-center px-5 py-2.5 bg-emerald-500 text-white rounded-lg hover:bg-emerald-600 hover:shadow-md transition-all duration-200 font-medium text-sm"
            >
              📊 Export Excel
            </a>
            <button
              onClick={handleClear}
              className="flex-1 md:flex-none px-5 py-2.5 bg-rose-50 text-rose-600 border border-rose-200 rounded-lg hover:bg-rose-100 hover:border-rose-300 transition-all duration-200 font-medium text-sm"
            >
              🗑️ Clear Data
            </button>
          </div>
        </header>"""

content = content.replace(old_header, new_header)

# 2. Update Search Section
old_search_start = """        <section className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4 text-gray-700">Find Businesses That Need Your Service</h2>
          <form onSubmit={handleScrape} className="grid grid-cols-6 gap-4 items-end">"""

new_search_start = """        <section className="bg-white p-6 md:p-8 rounded-2xl shadow-sm border border-slate-100 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-1 h-full bg-indigo-500"></div>
          <h2 className="text-xl font-bold mb-1 text-slate-800">1. Target Audience</h2>
          <p className="text-sm text-slate-500 mb-6 font-medium">Find highly-qualified B2B leads on Google Maps.</p>
          <form onSubmit={handleScrape} className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-5 items-end">"""

content = content.replace(old_search_start, new_search_start)

# 3. Update Inputs
def replace_inputs(text):
    text = text.replace('className="w-full border p-2 rounded text-black"', 'className="w-full bg-slate-50 border border-slate-200 text-slate-900 rounded-lg p-3 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none placeholder:text-slate-400"')
    text = text.replace('className="block text-sm text-gray-600 mb-1"', 'className="block text-sm font-semibold text-slate-700 mb-1.5"')
    return text

content = replace_inputs(content)

# 4. Search Button
old_btn = """              <button disabled={isScraping || loading} type="submit" className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 font-medium">
                {isScraping ? 'Scraping...' : 'Find Leads'}
              </button>"""
new_btn = """              <button disabled={isScraping || loading} type="submit" className="w-full h-[46px] bg-indigo-600 text-white px-4 rounded-lg hover:bg-indigo-700 hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0 transform transition-all duration-200 font-semibold shadow-sm flex justify-center items-center gap-2">
                {isScraping ? (
                  <><span className="animate-spin">⏳</span> Scraping</>
                ) : (
                  <><span className="text-lg">🔍</span> Search</>
                )}
              </button>"""
content = content.replace(old_btn, new_btn)

# 5. Email Campaign Section
old_email = """        <section className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4 text-gray-700">Automated Email Campaign</h2>
          <p className="text-sm text-gray-500 mb-4">Send personalized pitches to all scraped leads that have an email address.</p>
          <div className="grid grid-cols-3 gap-4 items-end">"""
new_email = """        <section className="bg-white p-6 md:p-8 rounded-2xl shadow-sm border border-slate-100 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-1 h-full bg-violet-500"></div>
          <h2 className="text-xl font-bold mb-1 text-slate-800">2. Email Outreach</h2>
          <p className="text-sm text-slate-500 mb-6 font-medium">Send highly personalized AI pitches to all leads with an email address.</p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5 items-end">"""
content = content.replace(old_email, new_email)

old_email_btn = """className="w-full bg-indigo-600 text-white p-2 rounded hover:bg-indigo-700 font-medium\""""
new_email_btn = """className="w-full h-[46px] bg-violet-600 text-white px-4 rounded-lg hover:bg-violet-700 hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0 transform transition-all duration-200 font-semibold shadow-sm flex justify-center items-center gap-2\""""
content = content.replace(old_email_btn, new_email_btn)

# 6. Table Section
old_table_sec = """        <section className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Business</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Score</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Website</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">"""

new_table_sec = """        <section className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
          <div className="px-6 py-5 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
             <h2 className="text-lg font-bold text-slate-800">3. Lead Database</h2>
             <span className="bg-indigo-100 text-indigo-800 text-xs font-bold px-3 py-1 rounded-full">{leads.length} Leads</span>
          </div>
          <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-100">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Business</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Score</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Status</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Email/Web</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Action</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-slate-50">"""
content = content.replace(old_table_sec, new_table_sec)

content = content.replace("</section>", "</div></section>")

# 7. Table Rows
content = content.replace('className="hover:bg-gray-50"', 'className="hover:bg-slate-50/80 transition-colors"')
content = content.replace('text-gray-900', 'text-slate-800')
content = content.replace('text-gray-500', 'text-slate-500')
content = content.replace('text-gray-400', 'text-slate-400')
content = content.replace('text-gray-700', 'text-slate-700')
content = content.replace('bg-gray-100', 'bg-slate-100')
content = content.replace('border-gray-300', 'border-slate-200')
content = content.replace('border-gray-200', 'border-slate-200')

# Simplify actions to icons
content = content.replace("✉️ View / Edit Pitch", "✉️ Pitch")
content = content.replace("📍 View on Map", "📍 Map")
content = content.replace("💬</span> Send on WhatsApp", "💬</span> WhatsApp")
content = content.replace("🤖</span> AI Call Lead", "🤖</span> Call")

# 8. Modal styling
content = content.replace('bg-black bg-opacity-50', 'bg-slate-900/60 backdrop-blur-sm')
content = content.replace('bg-white rounded-xl p-6', 'bg-white rounded-2xl p-8')
content = content.replace('border-transparent outline-none mb-4 font-mono text-sm text-gray-700 bg-gray-50', 'border-indigo-500 outline-none mb-4 font-mono text-sm text-slate-700 bg-slate-50/50 leading-relaxed shadow-inner')

with open("frontend/src/app/page.tsx", "w") as f:
    f.write(content)
