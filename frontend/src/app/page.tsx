"use client";

import { useEffect, useState } from 'react';

type Lead = {
  id: number;
  business_name: string;
  category: string;
  city: string;
  rating: number;
  phone: string;
  whatsapp_link: string;
  map_url: string;
  address: string;
  has_website: boolean;
  lead_score: number;
  lead_grade: string;
  recommended_pitch: string;
  status: string;
};

export default function Dashboard() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({ country: 'Saudi Arabia', city: 'Riyadh', category: 'Beauty Salon', radius: '20' });

  const [isMounted, setIsMounted] = useState(false);

  // New state variables for progress tracking and modal
  const [progress, setProgress] = useState(0);
  const [progressMessage, setProgressMessage] = useState('');
  const [isScraping, setIsScraping] = useState(false);
  const [editingLead, setEditingLead] = useState<Lead | null>(null);
  const [editedPitch, setEditedPitch] = useState('');
  const [scoreDetailsLead, setScoreDetailsLead] = useState<Lead | null>(null);
  
  const [countries, setCountries] = useState<string[]>([]);
  const [cities, setCities] = useState<string[]>([]);
  
  const popularCategories = [
    "Real Estate Agency", "Dental Clinic", "Plumbing Service", "Restaurant", 
    "Law Firm", "Accounting Firm", "Spa and Wellness", "Beauty Salon", 
    "HVAC Contractor", "Roofing Contractor", "Medical Clinic", "Gym",
    "Car Dealership", "Travel Agency", "Software Company", "Logistics Company"
  ];

  // Fetch countries on component mount
  useEffect(() => {
    fetch('https://countriesnow.space/api/v0.1/countries')
      .then(res => res.json())
      .then(data => {
        if (!data.error) {
          setCountries(data.data.map((c: any) => c.country));
        }
      })
      .catch(err => console.error("Error fetching countries:", err));
  }, []);

  // Fetch cities when country changes
  useEffect(() => {
    if (!form.country) return;
    
    // Simple way to fetch cities for a country
    fetch('https://countriesnow.space/api/v0.1/countries/cities', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ country: form.country })
    })
      .then(res => res.json())
      .then(data => {
        if (!data.error) {
          setCities(data.data);
        } else {
          setCities([]); // reset if country not found in API
        }
      })
      .catch(err => {
        console.error("Error fetching cities:", err);
        setCities([]);
      });
  }, [form.country]);

  const getScoreBreakdown = (lead: Lead) => {
    const breakdown = [];
    if (lead.has_website) {
      breakdown.push({ label: 'Website Found', score: '+40', type: 'text-green-600', icon: '✅' });
    } else {
      breakdown.push({ label: 'Missing Website', score: '0', type: 'text-red-500', icon: '❌' });
    }
    
    if (lead.phone) {
      breakdown.push({ label: 'Phone Number Found', score: '+20', type: 'text-green-600', icon: '✅' });
    } else {
      breakdown.push({ label: 'Missing Phone Number', score: '0', type: 'text-red-500', icon: '❌' });
    }
    
    if (lead.whatsapp_link) {
      breakdown.push({ label: 'WhatsApp Link Generated', score: '+20', type: 'text-green-600', icon: '✅' });
    } else {
      breakdown.push({ label: 'Missing WhatsApp', score: '0', type: 'text-red-500', icon: '❌' });
    }
    
    if (lead.rating > 0) {
      breakdown.push({ label: 'Google Rating Found', score: '+20', type: 'text-green-600', icon: '✅' });
    } else {
      breakdown.push({ label: 'Missing Rating', score: '0', type: 'text-red-500', icon: '❌' });
    }
    
    return breakdown;
  };

  const fetchLeads = async () => {
    try {
      const res = await fetch('/api/leads');
      const data = await res.json();
      setLeads(data);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    setIsMounted(true);
    fetchLeads();
    
    // Auto-refresh removed to prevent network spam when idle
  }, [isScraping]);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isScraping) {
      interval = setInterval(async () => {
        try {
          const res = await fetch('/api/scrape/status');
          const statusData = await res.json();
          
          setProgress(statusData.progress);
          setProgressMessage(statusData.message);
          
          // Fetch leads continuously so table updates live!
          await fetchLeads();

          if (statusData.status === 'idle' || statusData.status === 'error') {
            clearInterval(interval);
            setIsScraping(false);
            if (statusData.status === 'idle') {
              setProgressMessage('Scraping complete!');
              setProgress(100);
            } else {
              setProgressMessage(statusData.message);
            }
            setTimeout(() => setProgressMessage(''), 3000);
          }
        } catch (e) {
          console.error(e);
        }
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isScraping]);

  if (!isMounted) return null;

  const handleScrape = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setIsScraping(true);
    setProgress(0);
    setProgressMessage('Starting...');
    try {
      await fetch('/api/scrape', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      });
      // The background task started. Polling will handle the rest.
    } catch (e) {
      console.error(e);
      setIsScraping(false);
    }
    setLoading(false);
  };

  const handleSavePitch = async () => {
    if (!editingLead) return;
    try {
      await fetch(`/api/leads/${editingLead.id}/pitch`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pitch: editedPitch })
      });
      setEditingLead(null);
      fetchLeads();
    } catch (e) {
      console.error(e);
    }
  };

  const handleClear = async () => {
    if (!confirm('Are you sure you want to clear all leads?')) return;
    try {
      await fetch('/api/leads', { method: 'DELETE' });
      fetchLeads();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        
        <header className="flex justify-between items-center bg-white p-6 rounded-lg shadow">
          <h1 className="text-2xl font-bold text-gray-800">B2B Lead Generation System</h1>
          <button onClick={handleClear} className="bg-red-50 text-red-600 px-4 py-2 rounded-md text-sm font-medium hover:bg-red-100 transition-colors">
            Clear All Leads
          </button>
        </header>

        <section className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4 text-gray-700">Find Businesses That Need Your Service</h2>
          <form onSubmit={handleScrape} className="grid grid-cols-5 gap-4 items-end">
            <div>
              <label className="block text-sm text-gray-600 mb-1">Country</label>
              <input 
                type="text" 
                list="countries-list"
                className="w-full border p-2 rounded text-black" 
                value={form.country} 
                onChange={e => setForm({...form, country: e.target.value})} 
                placeholder="Type or select a country..."
              />
              <datalist id="countries-list">
                {countries.map(c => <option key={c} value={c} />)}
              </datalist>
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">City</label>
              <input 
                type="text" 
                list="cities-list"
                className="w-full border p-2 rounded text-black" 
                value={form.city} 
                onChange={e => setForm({...form, city: e.target.value})} 
                placeholder="Type or select a city..."
              />
              <datalist id="cities-list">
                {cities.map(c => <option key={c} value={c} />)}
              </datalist>
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Category (Business Type)</label>
              <input 
                type="text" 
                list="categories-list"
                className="w-full border p-2 rounded text-black" 
                value={form.category} 
                onChange={e => setForm({...form, category: e.target.value})} 
                placeholder="E.g. Real Estate, Plumber..."
              />
              <datalist id="categories-list">
                {popularCategories.map(c => <option key={c} value={c} />)}
              </datalist>
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Radius (km)</label>
              <input type="text" className="w-full border p-2 rounded text-black" value={form.radius} onChange={e => setForm({...form, radius: e.target.value})} />
            </div>
            <div>
              <button disabled={isScraping || loading} type="submit" className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 font-medium">
                {isScraping ? 'Scraping...' : 'Find Leads'}
              </button>
            </div>
          </form>
          {isScraping && (
            <div className="w-full mt-6">
              <div className="flex justify-between text-sm text-gray-600 mb-2 font-medium">
                <span>{progressMessage}</span>
                <span>{progress}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2.5 overflow-hidden">
                <div className="bg-blue-600 h-2.5 rounded-full transition-all duration-500 ease-out" style={{ width: `${progress}%` }}></div>
              </div>
            </div>
          )}
        </section>

        <section className="bg-white rounded-lg shadow overflow-hidden">
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
            <tbody className="bg-white divide-y divide-gray-200">
              {leads.map((lead, idx) => (
                <tr key={idx} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div className="font-medium text-gray-900">{lead.business_name}</div>
                    <div className="text-xs text-gray-500">{lead.category} • {lead.city} • {lead.rating} ★</div>
                    {lead.address && <div className="text-xs text-gray-400 mt-1">{lead.address}</div>}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <button 
                      onClick={() => setScoreDetailsLead(lead)}
                      className="text-sm font-bold text-blue-600 hover:text-blue-800 underline decoration-blue-300 underline-offset-4 flex items-center"
                    >
                      {lead.lead_score}/100 {lead.lead_score === 100 && <span className="ml-1 text-green-500 text-lg" title="Profile Complete">✅</span>}
                    </button>
                    <div className="text-xs text-gray-500 mt-1">{lead.lead_grade}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                      {lead.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {lead.has_website ? '✅ Yes' : '❌ No'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2 flex items-center pt-6">
                    <a 
                      href={lead.map_url} 
                      target="_blank" 
                      className="text-gray-700 hover:text-gray-900 bg-gray-100 hover:bg-gray-200 px-3 py-1 rounded border border-gray-300 transition-colors inline-flex items-center text-xs font-semibold"
                    >
                      📍 View on Map
                    </a>
                    <button 
                      className="text-blue-600 hover:text-blue-900 bg-blue-50 px-3 py-1 rounded border border-blue-200 text-xs font-semibold" 
                      onClick={() => {
                        setEditingLead(lead);
                        setEditedPitch(lead.recommended_pitch);
                      }}
                    >
                      ✉️ View / Edit Pitch
                    </button>
                    {lead.phone && (
                      <a 
                        href={`${lead.whatsapp_link}?text=${encodeURIComponent(lead.recommended_pitch)}`} 
                        target="_blank" 
                        className="text-green-600 hover:text-green-900 bg-green-50 px-3 py-1 rounded border border-green-200 transition-colors inline-flex items-center text-xs font-semibold"
                      >
                        <span className="mr-1">💬</span> Send on WhatsApp
                      </a>
                    )}
                  </td>
                </tr>
              ))}
              {leads.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-gray-500">No leads found. Start a new search above.</td>
                </tr>
              )}
            </tbody>
          </table>
        </section>
      </div>

      {/* Score Breakdown Modal */}
      {scoreDetailsLead && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" onClick={() => setScoreDetailsLead(null)}>
          <div className="bg-white rounded-xl p-6 max-w-md w-full shadow-2xl" onClick={e => e.stopPropagation()}>
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold text-gray-800">Profile Data Completeness</h3>
              <button onClick={() => setScoreDetailsLead(null)} className="text-gray-400 hover:text-gray-600">
                ✖
              </button>
            </div>
            <div className="mb-4 bg-gray-50 p-4 rounded-lg border border-gray-100">
              <p className="text-sm text-gray-600 mb-1">Business</p>
              <p className="font-semibold text-gray-900">{scoreDetailsLead.business_name}</p>
            </div>
            
            <div className="space-y-3">
              {getScoreBreakdown(scoreDetailsLead).map((item, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 bg-white border rounded-lg shadow-sm">
                  <div className="flex items-center space-x-3">
                    <span>{item.icon}</span>
                    <span className="text-sm font-medium text-gray-700">{item.label}</span>
                  </div>
                  <span className={`font-bold ${item.type}`}>{item.score}</span>
                </div>
              ))}
            </div>
            
            <div className="mt-6 pt-4 border-t flex justify-between items-center">
              <span className="text-gray-600 font-medium">Total Score</span>
              <span className="text-2xl font-black text-gray-900">{scoreDetailsLead.lead_score}/100</span>
            </div>
            
            <button 
              onClick={() => setScoreDetailsLead(null)}
              className="mt-6 w-full py-2 bg-gray-100 text-gray-800 font-medium hover:bg-gray-200 rounded-md transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      )}

      {/* Edit Pitch Modal */}
      {editingLead && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl p-6 max-w-3xl w-full shadow-2xl">
            <h3 className="text-xl font-bold mb-4 text-gray-800">Edit Pitch for {editingLead.business_name}</h3>
            <textarea
              className="w-full h-96 p-4 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none mb-4 font-mono text-sm text-gray-700 bg-gray-50"
              value={editedPitch}
              onChange={(e) => setEditedPitch(e.target.value)}
            ></textarea>
            <div className="flex justify-between items-center">
              <span className="text-xs text-gray-500">You can edit the pitch directly and save it to the database.</span>
              <div className="flex space-x-3">
                <button 
                  onClick={() => setEditingLead(null)}
                  className="px-4 py-2 text-gray-600 hover:bg-gray-100 font-medium rounded-md transition-colors"
                >
                  Cancel
                </button>
                <button 
                  onClick={(e) => {
                    navigator.clipboard.writeText(editedPitch);
                    const btn = e.currentTarget;
                    const original = btn.innerHTML;
                    btn.innerHTML = '✅ Copied!';
                    setTimeout(() => btn.innerHTML = original, 2000);
                  }}
                  className="px-4 py-2 text-blue-600 border border-blue-200 font-medium hover:bg-blue-50 rounded-md transition-colors"
                >
                  Copy to Clipboard
                </button>
                <button 
                  onClick={handleSavePitch}
                  className="px-5 py-2 bg-blue-600 text-white font-medium hover:bg-blue-700 rounded-md shadow-sm transition-colors"
                >
                  Save Changes
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
