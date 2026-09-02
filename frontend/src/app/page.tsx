"use client";

import { useEffect, useState } from 'react';
import { useTheme } from 'next-themes';

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
  website?: string;
  email?: string;
  lead_score: number;
  lead_grade: string;
  recommended_pitch: string;
  status: string;
};

export default function Dashboard() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({ country: '', state: '', city: '', category: '', radius: '20' });

  const [isMounted, setIsMounted] = useState(false);

  // New state variables for progress tracking and modal
  const [progress, setProgress] = useState(0);
  const [progressMessage, setProgressMessage] = useState('');
  const [isScraping, setIsScraping] = useState(false);
  const [emailProgress, setEmailProgress] = useState(0);
  const [emailMessage, setEmailMessage] = useState('');
  const [isEmailing, setIsEmailing] = useState(false);
  const [sentEmailIds, setSentEmailIds] = useState<number[]>([]);
  const { theme, setTheme } = useTheme();
  const [editingLead, setEditingLead] = useState<Lead | null>(null);
  const [editedPitch, setEditedPitch] = useState('');
  const [scoreDetailsLead, setScoreDetailsLead] = useState<Lead | null>(null);
  
  const [countries, setCountries] = useState<string[]>([]);
  const [states, setStates] = useState<any[]>([]);
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

  // Fetch states when country changes
  useEffect(() => {
    setForm(f => ({ ...f, state: '', city: '' }));
    setStates([]);
    setCities([]);
    if (!form.country) return;
    
    fetch('https://countriesnow.space/api/v0.1/countries/states', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ country: form.country })
    })
      .then(res => res.json())
      .then(data => {
        if (!data.error && data.data && data.data.states) {
          setStates(data.data.states.map((s: any) => s.name));
        }
      })
      .catch(err => console.error(err));
  }, [form.country]);

  // Fetch cities when state changes
  useEffect(() => {
    setForm(f => ({ ...f, city: '' }));
    setCities([]);
    if (!form.country || !form.state) return;
    
    fetch('https://countriesnow.space/api/v0.1/countries/state/cities', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ country: form.country, state: form.state })
    })
      .then(res => res.json())
      .then(data => {
        if (!data.error && data.data) {
          setCities(data.data);
        }
      })
      .catch(err => console.error(err));
  }, [form.state]);

  const getScoreBreakdown = (lead: Lead) => {
    const breakdown = [];
    if (!lead.has_website) {
      breakdown.push({ label: 'No Website Found (High Priority)', score: '+50', type: 'text-emerald-500', icon: '⭐' });
    } else {
      breakdown.push({ label: 'Has Website (Lower Priority)', score: '0', type: 'text-amber-500', icon: '🌐' });
    }
    
    if (lead.phone) {
      breakdown.push({ label: 'Phone Number Found', score: '+20', type: 'text-emerald-500', icon: '✅' });
    } else {
      breakdown.push({ label: 'Missing Phone Number', score: '0', type: 'text-red-500', icon: '❌' });
    }
    
    if (lead.whatsapp_link) {
      breakdown.push({ label: 'WhatsApp Link Generated', score: '+20', type: 'text-emerald-500', icon: '✅' });
    } else {
      breakdown.push({ label: 'Missing WhatsApp', score: '0', type: 'text-red-500', icon: '❌' });
    }
    
    if (lead.rating > 0) {
      breakdown.push({ label: 'Google Rating Found', score: '+10', type: 'text-emerald-500', icon: '✅' });
    } else {
      breakdown.push({ label: 'Missing Rating', score: '0', type: 'text-red-500', icon: '❌' });
    }
    
    if (lead.email) {
      breakdown.push({ label: 'Email Address Extracted', score: 'Bonus', type: 'text-blue-500', icon: '📧' });
    } else {
      breakdown.push({ label: 'Missing Email', score: '-', type: 'text-muted-foreground', icon: '🚫' });
    }
    
    return breakdown;
  };

  const fetchLeads = async () => {
    try {
      const res = await fetch('/api/leads?t=' + new Date().getTime(), {
        cache: 'no-store'
      });
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
    let emailInterval: NodeJS.Timeout;
    if (isEmailing) {
      emailInterval = setInterval(async () => {
        try {
          const res = await fetch('/api/emails/status');
          const data = await res.json();
          setEmailProgress(data.progress || 0);
          setEmailMessage(data.message || '');
          if (data.sent_ids) setSentEmailIds(data.sent_ids);
          
          if (data.status === 'idle' || data.status === 'error') {
            clearInterval(emailInterval);
            setIsEmailing(false);
            if (data.status === 'idle') {
                setEmailMessage('Campaign finished!');
                setTimeout(() => setEmailMessage(''), 4000);
            }
          }
        } catch (e) {
          console.error(e);
        }
      }, 1000);
    }
    return () => clearInterval(emailInterval);
  }, [isEmailing]);

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
    <div className={`min-h-screen p-4 md:p-8 font-sans selection:bg-primary/20 bg-background text-foreground transition-colors duration-300`}>
      <div className="max-w-7xl mx-auto space-y-8">
        
        <header className="flex flex-col md:flex-row justify-between items-start md:items-center bg-card p-6 md:p-8 rounded-2xl shadow-sm border border-border gap-4 md:gap-0">
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight text-foreground flex items-center gap-2">
              <span className="text-primary">⚡</span> LeadGen Pro
            </h1>
            <p className="text-sm text-muted-foreground mt-1 font-medium">B2B Lead Generation & Outreach System</p>
          </div>
          <div className="flex flex-wrap items-center gap-3 w-full md:w-auto">
            <button onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')} className="px-4 py-2.5 rounded-lg bg-muted text-foreground hover:bg-muted/80 transition-colors" title="Toggle Dark Mode">
              {theme === 'dark' ? "☀️ Light" : "🌙 Dark"}
            </button>
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
              onClick={handleClear}
              className="flex-1 md:flex-none px-5 py-2.5 bg-rose-50 text-rose-600 border border-rose-200 rounded-lg hover:bg-rose-100 hover:border-rose-300 transition-all duration-200 font-medium text-sm"
            >
              🗑️ Clear Data
            </button>
          </div>
        </header>

        <section className="bg-card p-6 md:p-8 rounded-2xl shadow-sm border border-border relative overflow-hidden">
          <div className="absolute top-0 left-0 w-1 h-full bg-indigo-500"></div>
          <h2 className="text-xl font-bold mb-1 text-foreground">1. Target Audience</h2>
          <p className="text-sm text-muted-foreground mb-6 font-medium">Find highly-qualified B2B leads on Google Maps.</p>
          <form onSubmit={handleScrape} className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-5 items-end">
            <div>
              <label className="block text-sm font-semibold text-foreground mb-1.5">Country</label>
              <input 
                type="text" 
                list="countries-list"
                className="w-full bg-muted border border-border text-foreground rounded-lg p-3 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none placeholder:text-muted-foreground" 
                value={form.country} 
                onChange={e => setForm({...form, country: e.target.value})} 
                placeholder="Type or select a country..."
              />
              <datalist id="countries-list">
                {countries.map(c => <option key={c} value={c} />)}
              </datalist>
            </div>
            <div>
              <label className="block text-sm font-semibold text-foreground mb-1.5">State/Province</label>
              <input 
                type="text" 
                list="states-list"
                className="w-full bg-muted border border-border text-foreground rounded-lg p-3 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none placeholder:text-muted-foreground" 
                value={form.state} 
                onChange={e => setForm({...form, state: e.target.value})} 
                placeholder="Select a state..."
              />
              <datalist id="states-list">
                {states.map(s => <option key={s} value={s} />)}
              </datalist>
            </div>
            <div>
              <label className="block text-sm font-semibold text-foreground mb-1.5">City</label>
              <input 
                type="text" 
                list="cities-list"
                className="w-full bg-muted border border-border text-foreground rounded-lg p-3 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none placeholder:text-muted-foreground" 
                value={form.city} 
                onChange={e => setForm({...form, city: e.target.value})} 
                placeholder="Type or select a city..."
              />
              <datalist id="cities-list">
                {cities.map(c => <option key={c} value={c} />)}
              </datalist>
            </div>
            <div>
              <label className="block text-sm font-semibold text-foreground mb-1.5">Category (Business Type)</label>
              <input 
                type="text" 
                list="categories-list"
                className="w-full bg-muted border border-border text-foreground rounded-lg p-3 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none placeholder:text-muted-foreground" 
                value={form.category} 
                onChange={e => setForm({...form, category: e.target.value})} 
                placeholder="E.g. Real Estate, Plumber..."
              />
              <datalist id="categories-list">
                {popularCategories.map(c => <option key={c} value={c} />)}
              </datalist>
            </div>
            <div>
              <label className="block text-sm font-semibold text-foreground mb-1.5">Radius (km)</label>
              <input type="text" className="w-full bg-muted border border-border text-foreground rounded-lg p-3 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none placeholder:text-muted-foreground" value={form.radius} onChange={e => setForm({...form, radius: e.target.value})} />
            </div>
            <div>
              <button disabled={isScraping || loading} type="submit" className="w-full h-[46px] bg-indigo-600 text-white px-4 rounded-lg hover:bg-indigo-700 hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0 transform transition-all duration-200 font-semibold shadow-sm flex justify-center items-center gap-2">
                {isScraping ? (
                  <><span className="animate-spin">⏳</span> Scraping</>
                ) : (
                  <><span className="text-lg">🔍</span> Search</>
                )}
              </button>
            </div>
          </form>
          {isScraping && (
            <div className="w-full mt-6">
              <div className="flex justify-between text-sm text-foreground mb-2 font-medium">
                <span>{progressMessage}</span>
                <span>{progress}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2.5 overflow-hidden">
                <div className="bg-blue-600 h-2.5 rounded-full transition-all duration-500 ease-out" style={{ width: `${progress}%` }}></div>
              </div>
            </div>
          )}
        </section>

        <section className="bg-card p-6 md:p-8 rounded-2xl shadow-sm border border-border relative overflow-hidden">
          <div className="absolute top-0 left-0 w-1 h-full bg-violet-500"></div>
          <h2 className="text-xl font-bold mb-1 text-foreground">2. Email Outreach</h2>
          <p className="text-sm text-muted-foreground mb-6 font-medium">Send highly personalized AI pitches to all leads with an email address.</p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5 items-end">
            <div>
              <label className="block text-sm font-semibold text-foreground mb-1.5">Your Gmail Address</label>
              <input 
                type="email" 
                id="email-campaign-address"
                className="w-full bg-muted border border-border text-foreground rounded-lg p-3 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none placeholder:text-muted-foreground" 
                placeholder="you@gmail.com"
                defaultValue="asperinfotech@gmail.com"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-foreground mb-1.5">Google App Password</label>
              <input 
                type="password" 
                id="email-campaign-password"
                className="w-full bg-muted border border-border text-foreground rounded-lg p-3 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none placeholder:text-muted-foreground" 
                placeholder="16-character app password"
                defaultValue="snqr frzo ivyy pmzo"
              />
            </div>
            <div>
              <button 
                onClick={async () => {
                  const gmail = (document.getElementById('email-campaign-address') as HTMLInputElement).value;
                  const password = (document.getElementById('email-campaign-password') as HTMLInputElement).value;
                  if (!gmail || !password) return alert("Please enter both Gmail address and App Password");
                  
                  try {
                    setIsEmailing(true);
                    setEmailProgress(0);
                    setEmailMessage('Starting campaign...');
                    const res = await fetch('/api/emails/campaign', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ gmail_address: gmail, app_password: password })
                    });
                    const data = await res.json();
                    if (data.error) {
                       alert(data.error);
                       setIsEmailing(false);
                    }
                  } catch (e) {
                    console.error(e);
                  }
                }}
                disabled={isEmailing}
                className="w-full h-[46px] bg-violet-600 text-white px-4 rounded-lg hover:bg-violet-700 hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0 transform transition-all duration-200 font-semibold shadow-sm flex justify-center items-center gap-2 disabled:opacity-70 disabled:hover:-translate-y-0 disabled:cursor-not-allowed"
              >
                {isEmailing ? (
                  <><span className="animate-spin">⏳</span> Sending...</>
                ) : (
                  <>Start Email Campaign</>
                )}
              </button>
            </div>
          </div>
        </section>

        <section className="bg-card rounded-2xl shadow-sm border border-border overflow-hidden">
          <div className="px-6 py-5 border-b border-border bg-muted/50 flex justify-between items-center">
             <h2 className="text-lg font-bold text-foreground">3. Lead Database</h2>
             <span className="bg-indigo-100 text-indigo-800 text-xs font-bold px-3 py-1 rounded-full">{leads.length} Leads</span>
          </div>
          <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-100">
            <thead className="bg-muted">
              <tr>
                <th className="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Business</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Score</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Status</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Email/Web</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Action</th>
              </tr>
            </thead>
            <tbody className="bg-card divide-y divide-border">
              {leads.map((lead, idx) => (
                <tr key={idx} className={`transition-colors ${['Contacted', 'Duplicate'].includes(lead.status) ? 'bg-muted/80 opacity-75 grayscale-[20%]' : 'hover:bg-muted/50'}`}>
                  <td className="px-6 py-4">
                    <div className="font-medium text-foreground">{lead.business_name}</div>
                    <div className="text-xs text-muted-foreground">{lead.category} • {lead.city} • {lead.rating} ★</div>
                    {lead.address && <div className="text-xs text-muted-foreground mt-1">{lead.address}</div>}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <button 
                      onClick={() => setScoreDetailsLead(lead)}
                      className="text-sm font-bold text-blue-600 hover:text-blue-800 underline decoration-blue-300 underline-offset-4 flex items-center"
                    >
                      {lead.lead_score}/100 {lead.lead_score === 100 && <span className="ml-1 text-green-500 text-lg" title="Profile Complete">✅</span>}
                    </button>
                    <div className="text-xs text-muted-foreground mt-1">{lead.lead_grade}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      lead.status === 'Contacted' ? 'bg-indigo-100 text-indigo-800' : 
                      lead.status === 'Duplicate' ? 'bg-amber-100 text-amber-800' : 
                      'bg-green-100 text-green-800'
                    }`}>
                      {lead.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">
                    <div>{lead.has_website ? '✅ Web' : '❌ Web'}</div>
                    {lead.email && <div className="text-xs text-primary font-medium mt-1 w-[150px] xl:w-[200px] truncate" title={lead.email}>📧 {lead.email}</div>}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2 flex items-center pt-6">
                    <a 
                      href={lead.map_url} 
                      target="_blank" 
                      className="text-foreground hover:text-foreground bg-muted hover:bg-muted/80 px-3 py-1 rounded border border-border transition-colors inline-flex items-center text-xs font-semibold"
                    >
                      📍 Map
                    </a>
                    {lead.has_website && lead.website && (
                      <a 
                        href={lead.website} 
                        target="_blank" 
                        className="text-foreground hover:text-foreground bg-muted hover:bg-muted/80 px-3 py-1 rounded border border-border transition-colors inline-flex items-center text-xs font-semibold"
                      >
                        🌐 Web
                      </a>
                    )}
                    {(sentEmailIds.includes(lead.id) || lead.status === 'Contacted') && (
                      <span className="text-emerald-700 bg-emerald-50 px-3 py-1 rounded border border-emerald-200 text-xs font-bold flex items-center">
                        ✅ Sent
                      </span>
                    )}
                    <button 
                      className="text-blue-600 hover:text-blue-900 bg-blue-50 px-3 py-1 rounded border border-blue-200 text-xs font-semibold" 
                      onClick={() => {
                        setEditingLead(lead);
                        setEditedPitch(lead.recommended_pitch);
                      }}
                    >
                      ✉️ Pitch
                    </button>
                    {lead.phone && (
                      <>
                        <a 
                          href={`${lead.whatsapp_link}?text=${encodeURIComponent(lead.recommended_pitch)}`} 
                          target="_blank" 
                          className="text-green-600 hover:text-green-900 bg-green-50 px-3 py-1 rounded border border-green-200 transition-colors inline-flex items-center text-xs font-semibold"
                        >
                          <span className="mr-1">💬</span> WhatsApp
                        </a>
                        <button
                          onClick={async () => {
                            try {
                              const res = await fetch('/api/calls/outbound', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ phone: lead.phone, pitch: lead.recommended_pitch })
                              });
                              const data = await res.json();
                              if (data.error) {
                                alert(data.error);
                              } else {
                                alert("Calling " + lead.business_name + " via Twilio!");
                              }
                            } catch(e) {
                              console.error(e);
                              alert("Error initiating call");
                            }
                          }}
                          className="text-purple-600 hover:text-purple-900 bg-purple-50 px-3 py-1 rounded border border-purple-200 transition-colors inline-flex items-center text-xs font-semibold"
                        >
                          <span className="mr-1">🤖</span> Call
                        </button>
                      </>
                    )}
                  </td>
                </tr>
              ))}
              {leads.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-muted-foreground">No leads found. Start a new search above.</td>
                </tr>
              )}
            </tbody>
          </table>
          </div>
        </section>
      </div>

      {/* Score Breakdown Modal */}
      {scoreDetailsLead && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50" onClick={() => setScoreDetailsLead(null)}>
          <div className="bg-card rounded-2xl p-8 max-w-md w-full shadow-2xl" onClick={e => e.stopPropagation()}>
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold text-foreground">Lead Potential Score</h3>
              <button onClick={() => setScoreDetailsLead(null)} className="text-muted-foreground hover:text-foreground">
                ✖
              </button>
            </div>
            <div className="mb-4 bg-muted p-4 rounded-lg border border-border">
              <p className="text-sm text-foreground mb-1">Business</p>
              <p className="font-semibold text-foreground">{scoreDetailsLead.business_name}</p>
            </div>
            
            <div className="space-y-3">
              {getScoreBreakdown(scoreDetailsLead).map((item, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 bg-card border rounded-lg shadow-sm">
                  <div className="flex items-center space-x-3">
                    <span>{item.icon}</span>
                    <span className="text-sm font-medium text-foreground">{item.label}</span>
                  </div>
                  <span className={`font-bold ${item.type}`}>{item.score}</span>
                </div>
              ))}
            </div>
            
            <div className="mt-6 pt-4 border-t flex justify-between items-center">
              <span className="text-foreground font-medium">Total Score</span>
              <span className="text-2xl font-black text-foreground">{scoreDetailsLead.lead_score}/100</span>
            </div>
            
            <button 
              onClick={() => setScoreDetailsLead(null)}
              className="mt-6 w-full py-2 bg-muted text-gray-800 font-medium hover:bg-muted/80 rounded-md transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      )}

      {/* Edit Pitch Modal */}
      {editingLead && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-card rounded-2xl p-8 max-w-3xl w-full shadow-2xl">
            <h3 className="text-xl font-bold mb-4 text-gray-800">Edit Pitch for {editingLead.business_name}</h3>
            <textarea
              className="w-full h-96 p-4 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none mb-4 font-mono text-sm text-foreground bg-gray-50"
              value={editedPitch}
              onChange={(e) => setEditedPitch(e.target.value)}
            ></textarea>
            <div className="flex justify-between items-center">
              <span className="text-xs text-muted-foreground">You can edit the pitch directly and save it to the database.</span>
              <div className="flex space-x-3">
                <button 
                  onClick={() => setEditingLead(null)}
                  className="px-4 py-2 text-foreground hover:bg-muted font-medium rounded-md transition-colors"
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
