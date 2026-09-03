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
  const [newLeadIds, setNewLeadIds] = useState<Set<number>>(new Set());
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({ country: '', state: '', city: '', category: '', radius: '20' });

  const [isMounted, setIsMounted] = useState(false);
  const { theme, setTheme } = useTheme();

  // New state variables for progress tracking and modal
  const [progress, setProgress] = useState(0);
  const [progressMessage, setProgressMessage] = useState('');
  const [isScraping, setIsScraping] = useState(false);
  const [emailProgress, setEmailProgress] = useState(0);
  const [emailMessage, setEmailMessage] = useState('');
  const [isEmailing, setIsEmailing] = useState(false);
  const [sentEmailIds, setSentEmailIds] = useState<number[]>([]);
  const [editingLead, setEditingLead] = useState<Lead | null>(null);
  const [editedPitch, setEditedPitch] = useState('');
  const [scoreDetailsLead, setScoreDetailsLead] = useState<Lead | null>(null);
  
  const [countries, setCountries] = useState<string[]>([]);
  const [states, setStates] = useState<any[]>([]);
  const [cities, setCities] = useState<string[]>([]);
  
  // Tab system
  const [activeTab, setActiveTab] = useState<'leads' | 'jobs'>('leads');

  // Job Hunt state
  const [jobQuery, setJobQuery] = useState('');
  const [jobLimit, setJobLimit] = useState(30);
  const [isJobScraping, setIsJobScraping] = useState(false);
  const [jobProgress, setJobProgress] = useState(0);
  const [jobProgressMsg, setJobProgressMsg] = useState('');
  const [jobCompanies, setJobCompanies] = useState<any[]>([]);
  const [newCompanyEmails, setNewCompanyEmails] = useState<Set<string>>(new Set());
  const [isApplying, setIsApplying] = useState(false);
  const [applyProgress, setApplyProgress] = useState(0);
  const [applyMsg, setApplyMsg] = useState('');
  const [sentApplications, setSentApplications] = useState<string[]>([]);
  const [jobCustomPitch, setJobCustomPitch] = useState('');
  const [jobForm, setJobForm] = useState({ country: '', state: '', city: '', category: 'Software Company', radius: '20' });
  const [jobSenderEmail, setJobSenderEmail] = useState('hammadaslam78612@gmail.com');
  const [jobAppPassword, setJobAppPassword] = useState('tqmb xojp sjux yjjm');
  const [jobCustomResume, setJobCustomResume] = useState<string | null>(null);
  const [jobStates, setJobStates] = useState<string[]>([]);
  const [jobCities, setJobCities] = useState<string[]>([]);

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

  // ---- Job Form Location Fetching ----
  useEffect(() => {
    setJobForm(f => ({ ...f, state: '', city: '' }));
    setJobStates([]);
    setJobCities([]);
    if (!jobForm.country) return;
    
    fetch('https://countriesnow.space/api/v0.1/countries/states', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ country: jobForm.country })
    })
      .then(res => res.json())
      .then(data => {
        if (!data.error && data.data && data.data.states) {
          setJobStates(data.data.states.map((s: any) => s.name));
        }
      })
      .catch(console.error);
  }, [jobForm.country]);

  useEffect(() => {
    setJobForm(f => ({ ...f, city: '' }));
    setJobCities([]);
    if (!jobForm.country || !jobForm.state) return;
    
    fetch('https://countriesnow.space/api/v0.1/countries/state/cities', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ country: jobForm.country, state: jobForm.state })
    })
      .then(res => res.json())
      .then(data => {
        if (!data.error && data.data) {
          setJobCities(data.data);
        }
      })
      .catch(console.error);
  }, [jobForm.state]);

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
      const data: Lead[] = await res.json();
      
      // Track which IDs are NEW (not previously in the list)
      setLeads(prev => {
        const existingIds = new Set(prev.map(l => l.id));
        const freshIds = data.filter(l => !existingIds.has(l.id)).map(l => l.id);
        if (freshIds.length > 0) {
          setNewLeadIds(ids => {
            const next = new Set(ids);
            freshIds.forEach(id => next.add(id));
            // Remove highlight after 2s
            setTimeout(() => {
              setNewLeadIds(cur => {
                const cleared = new Set(cur);
                freshIds.forEach(id => cleared.delete(id));
                return cleared;
              });
            }, 2000);
            return next;
          });
        }
        return data;
      });
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    setIsMounted(true);
    fetchLeads();
  }, []);

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

  // ---- Job Hunt polling ----
  useEffect(() => {
    if (activeTab === 'jobs' && !jobCustomPitch) {
      fetch('/api/jobs/pitch/preview')
        .then(res => res.json())
        .then(data => setJobCustomPitch(data.pitch || ''))
        .catch(console.error);
    }
  }, [activeTab]);

  useEffect(() => {
    let jobInterval: NodeJS.Timeout;
    if (isJobScraping) {
      jobInterval = setInterval(async () => {
        try {
          const [statusRes, companiesRes] = await Promise.all([
            fetch('/api/jobs/status'),
            fetch('/api/jobs/companies')
          ]);
          const statusData = await statusRes.json();
          const companiesData: any[] = await companiesRes.json();
          setJobProgress(statusData.progress || 0);
          setJobProgressMsg(statusData.message || '');
          // Detect new companies
          setJobCompanies(prev => {
            const existingEmails = new Set(prev.map((c: any) => c.email));
            const fresh = companiesData.filter((c: any) => c.email && !existingEmails.has(c.email)).map((c: any) => c.email);
            if (fresh.length > 0) {
              setNewCompanyEmails(s => {
                const n = new Set(s);
                fresh.forEach(e => n.add(e));
                setTimeout(() => setNewCompanyEmails(cur => { const c = new Set(cur); fresh.forEach(e => c.delete(e)); return c; }), 2000);
                return n;
              });
            }
            return companiesData;
          });
          if (statusData.status === 'idle' || statusData.status === 'error') {
            clearInterval(jobInterval);
            setIsJobScraping(false);
          }
        } catch (e) { console.error(e); }
      }, 1000);
    }
    return () => clearInterval(jobInterval);
  }, [isJobScraping]);

  useEffect(() => {
    let applyInterval: NodeJS.Timeout;
    if (isApplying) {
      applyInterval = setInterval(async () => {
        try {
          const res = await fetch('/api/jobs/apply/status');
          const data = await res.json();
          setApplyProgress(data.progress || 0);
          setApplyMsg(data.message || '');
          setSentApplications(data.sent || []);
          if (data.status === 'idle' || data.status === 'error') {
            clearInterval(applyInterval);
            setIsApplying(false);
          }
        } catch (e) { console.error(e); }
      }, 1000);
    }
    return () => clearInterval(applyInterval);
  }, [isApplying]);

  if (!isMounted) return null;

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
            {/* Tab Switcher */}
            <div className="flex bg-muted rounded-lg p-1 gap-1">
              <button
                onClick={() => setActiveTab('leads')}
                className={`px-4 py-2 rounded-md text-sm font-bold transition-all ${
                  activeTab === 'leads'
                    ? 'bg-card text-foreground shadow-sm'
                    : 'text-muted-foreground hover:text-foreground'
                }`}
              >
                🎯 Lead Gen
              </button>
              <button
                onClick={() => setActiveTab('jobs')}
                className={`px-4 py-2 rounded-md text-sm font-bold transition-all ${
                  activeTab === 'jobs'
                    ? 'bg-indigo-600 text-white shadow-sm'
                    : 'text-muted-foreground hover:text-foreground'
                }`}
              >
                💼 Job Hunt
              </button>
            </div>
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

        {activeTab === 'leads' && (
        <>
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
             <h2 className="text-lg font-bold text-foreground flex items-center gap-2">
               3. Lead Database
               {isScraping && (
                 <span className="flex items-center gap-1.5 text-xs font-bold text-emerald-600 bg-emerald-100 dark:bg-emerald-950/40 dark:text-emerald-400 px-2 py-0.5 rounded-full animate-pulse">
                   <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full inline-block"></span>
                   LIVE
                 </span>
               )}
             </h2>
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
              {leads.map((lead) => (
                <tr 
                  key={lead.id} 
                  className={`transition-all duration-500 ${
                    newLeadIds.has(lead.id)
                      ? 'bg-emerald-50 dark:bg-emerald-950/30 animate-pulse'
                      : ['Contacted', 'Duplicate'].includes(lead.status) 
                        ? 'bg-muted/80 opacity-75 grayscale-[20%]' 
                        : 'hover:bg-muted/50'
                  }`}
                >
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
        </>
        )}

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

      {/* ========= JOB HUNT TAB ========= */}
      {activeTab === 'jobs' && (
        <div className="space-y-6">

          {/* Search Panel */}
          <section className="bg-card p-6 md:p-8 rounded-2xl shadow-sm border border-border relative overflow-hidden">
            <div className="absolute top-0 left-0 w-1 h-full bg-indigo-600"></div>
            <h2 className="text-xl font-bold mb-1 text-foreground">1. Find Tech Companies</h2>
            <p className="text-sm text-muted-foreground mb-6">Search for software companies on Google Maps and extract their emails for job applications.</p>
            <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-5 items-end">
              <div>
                <label className="block text-sm font-semibold text-foreground mb-1.5">Country</label>
                <input 
                  type="text" 
                  list="job-countries-list"
                  className="w-full bg-muted border border-border text-foreground rounded-lg p-3 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none placeholder:text-muted-foreground" 
                  value={jobForm.country} 
                  onChange={e => setJobForm({...jobForm, country: e.target.value})} 
                  placeholder="Type or select a country..."
                />
                <datalist id="job-countries-list">
                  {countries.map(c => <option key={c} value={c} />)}
                </datalist>
              </div>
              <div>
                <label className="block text-sm font-semibold text-foreground mb-1.5">State/Province</label>
                <input 
                  type="text" 
                  list="job-states-list"
                  className="w-full bg-muted border border-border text-foreground rounded-lg p-3 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none placeholder:text-muted-foreground" 
                  value={jobForm.state} 
                  onChange={e => setJobForm({...jobForm, state: e.target.value})} 
                  placeholder="Select a state..."
                />
                <datalist id="job-states-list">
                  {jobStates.map(s => <option key={s} value={s} />)}
                </datalist>
              </div>
              <div>
                <label className="block text-sm font-semibold text-foreground mb-1.5">City</label>
                <input 
                  type="text" 
                  list="job-cities-list"
                  className="w-full bg-muted border border-border text-foreground rounded-lg p-3 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none placeholder:text-muted-foreground" 
                  value={jobForm.city} 
                  onChange={e => setJobForm({...jobForm, city: e.target.value})} 
                  placeholder="Type or select a city..."
                />
                <datalist id="job-cities-list">
                  {jobCities.map(c => <option key={c} value={c} />)}
                </datalist>
              </div>
              <div>
                <label className="block text-sm font-semibold text-foreground mb-1.5">Category</label>
                <input 
                  type="text" 
                  list="job-categories-list"
                  className="w-full bg-muted border border-border text-foreground rounded-lg p-3 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none placeholder:text-muted-foreground" 
                  value={jobForm.category} 
                  onChange={e => setJobForm({...jobForm, category: e.target.value})} 
                  placeholder="e.g. Software Company"
                />
                <datalist id="job-categories-list">
                  {popularCategories.map(c => <option key={c} value={c} />)}
                </datalist>
              </div>
              <div>
                <label className="block text-sm font-semibold text-foreground mb-1.5">Radius (km)</label>
                <input type="text" className="w-full bg-muted border border-border text-foreground rounded-lg p-3 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none placeholder:text-muted-foreground" value={jobForm.radius} onChange={e => setJobForm({...jobForm, radius: e.target.value})} />
              </div>
              <div>
                <button 
                  disabled={isJobScraping || !jobForm.category} 
                  onClick={async () => {
                    const finalQuery = `${jobForm.category} ${jobForm.city} ${jobForm.state} ${jobForm.country}`.trim();
                    if (!finalQuery) return alert("Please enter at least a category");
                    setIsJobScraping(true);
                    setJobProgress(0);
                    setJobProgressMsg('Starting...');
                    setJobCompanies([]);
                    await fetch('/api/jobs/scrape', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ query: finalQuery, limit: jobLimit })
                    });
                  }}
                  className="w-full h-[46px] bg-indigo-600 text-white px-4 rounded-lg hover:bg-indigo-700 hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0 transform transition-all duration-200 font-semibold shadow-sm flex justify-center items-center gap-2">
                  {isJobScraping ? (
                    <><span className="animate-spin">⏳</span> Scraping</>
                  ) : (
                    <><span className="text-lg">🔍</span> Search</>
                  )}
                </button>
              </div>
            </div>
            
            {isJobScraping && (
              <div className="mt-4 flex gap-3">
                <button
                  onClick={() => fetch('/api/jobs/stop', { method: 'POST' }).then(() => setIsJobScraping(false))}
                  className="px-6 py-2.5 bg-rose-100 text-rose-600 border border-rose-200 rounded-lg font-bold hover:bg-rose-200 transition-all"
                >
                  ⛔ Stop Scraping
                </button>
              </div>
            )}

            {(isJobScraping || jobProgressMsg) && (
              <div className="mt-4">
                <div className="flex justify-between text-xs text-muted-foreground mb-1">
                  <span>{jobProgressMsg}</span>
                  <span>{jobProgress}%</span>
                </div>
                <div className="w-full bg-muted rounded-full h-2">
                  <div className="h-2 rounded-full bg-indigo-500 transition-all duration-300" style={{ width: `${jobProgress}%` }}></div>
                </div>
              </div>
            )}
          </section>

          {/* Start Email Campaign (Always Visible Now) */}
          <section className="bg-card p-6 md:p-8 rounded-2xl shadow-sm border border-border relative overflow-hidden">
              <div className="absolute top-0 left-0 w-1 h-full bg-emerald-500"></div>
              <h2 className="text-xl font-bold mb-1 text-foreground">2. Start Email Campaign</h2>
              <p className="text-sm text-muted-foreground mb-4">Auto-send your CV + professional pitch to all {jobCompanies.filter(c => c.email).length} companies with emails. Resume will be auto-attached.</p>
              <div className="bg-indigo-50 dark:bg-indigo-950/20 border border-indigo-200 dark:border-indigo-800 rounded-lg p-4 mb-4 flex justify-between items-center flex-wrap gap-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full">
                  <div>
                    <label className="block text-xs font-bold text-indigo-700 dark:text-indigo-300 mb-1">Sender Email</label>
                    <input 
                      type="email" 
                      value={jobSenderEmail}
                      onChange={e => setJobSenderEmail(e.target.value)}
                      className="w-full bg-white dark:bg-indigo-950 border border-indigo-200 dark:border-indigo-800 text-sm rounded p-2 focus:ring-1 focus:ring-indigo-500 outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-indigo-700 dark:text-indigo-300 mb-1">App Password</label>
                    <input 
                      type="password" 
                      value={jobAppPassword}
                      onChange={e => setJobAppPassword(e.target.value)}
                      className="w-full bg-white dark:bg-indigo-950 border border-indigo-200 dark:border-indigo-800 text-sm rounded p-2 focus:ring-1 focus:ring-indigo-500 outline-none"
                    />
                  </div>
                </div>
                <div className="w-full flex justify-between items-center mt-2 border-t border-indigo-200 dark:border-indigo-800 pt-3 flex-wrap gap-3">
                  <div>
                    <p className="text-sm font-bold text-indigo-700 dark:text-indigo-300">
                      📎 Attached: {jobCustomResume ? jobCustomResume : 'Hammad_Aslam_CV.pdf (Auto-generated)'}
                    </p>
                    <label className="text-xs text-indigo-600 dark:text-indigo-400 mt-1 cursor-pointer hover:underline inline-block">
                      + Upload Custom PDF Resume
                      <input 
                        type="file" 
                        accept="application/pdf"
                        className="hidden"
                        onChange={async (e) => {
                          const file = e.target.files?.[0];
                          if (!file) return;
                          
                          const formData = new FormData();
                          formData.append('file', file);
                          
                          try {
                            const res = await fetch('/api/jobs/resume/upload', {
                              method: 'POST',
                              body: formData
                            });
                            const data = await res.json();
                            if (data.status === 'success') {
                              setJobCustomResume(file.name);
                              alert("Resume uploaded successfully!");
                            } else {
                              alert("Failed to upload resume.");
                            }
                          } catch (err) {
                            console.error(err);
                            alert("Failed to upload resume.");
                          }
                          e.target.value = '';
                        }}
                      />
                    </label>
                  </div>
                  <a href="/api/jobs/resume/download" target="_blank" className="px-4 py-2 bg-indigo-600 text-white rounded-md text-sm font-bold hover:bg-indigo-700 transition-colors shadow-sm">
                    👁️ Preview CV
                  </a>
                </div>
              </div>

              <div className="mb-6">
                <label className="block text-sm font-bold text-foreground mb-2">Edit Email Pitch Before Sending</label>
                <textarea
                  className="w-full h-40 p-4 bg-muted border border-border rounded-lg text-sm text-foreground focus:ring-2 focus:ring-emerald-500 outline-none resize-y font-mono"
                  value={jobCustomPitch}
                  onChange={(e) => setJobCustomPitch(e.target.value)}
                  placeholder="Dear [Company Name], I am a software engineer..."
                ></textarea>
                <p className="text-xs text-muted-foreground mt-1">* Note: [Company Name] will be automatically replaced with the actual company's name.</p>
              </div>

              {isApplying && (
                <div className="mb-4">
                  <div className="flex justify-between text-xs text-muted-foreground mb-1">
                    <span>{applyMsg}</span>
                    <span>{applyProgress}%</span>
                  </div>
                  <div className="w-full bg-muted rounded-full h-2">
                    <div className="h-2 rounded-full bg-emerald-500 transition-all duration-300" style={{ width: `${applyProgress}%` }}></div>
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">{sentApplications.length} applications sent so far</p>
                </div>
              )}
              {applyMsg && !isApplying && (
                <div className="mb-4 p-3 bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-200 rounded-lg">
                  <p className="text-sm font-medium text-emerald-700 dark:text-emerald-400">{applyMsg}</p>
                </div>
              )}
              <button
                disabled={isApplying || jobCompanies.filter(c => c.email).length === 0}
                onClick={async () => {
                  if (!jobSenderEmail || !jobAppPassword) return alert("Please enter Sender Email and App Password.");
                  
                  setIsApplying(true);
                  setApplyProgress(0);
                  setApplyMsg('Starting...');
                  setSentApplications([]);
                  await fetch('/api/jobs/apply', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                      gmail_address: jobSenderEmail,
                      app_password: jobAppPassword,
                      custom_pitch: jobCustomPitch,
                      companies: jobCompanies
                    })
                  });
                }}
                className="px-8 py-3 bg-emerald-600 text-white rounded-lg font-bold hover:bg-emerald-700 disabled:opacity-50 transition-all shadow-md w-full md:w-auto"
              >
                {isApplying ? `⏳ Sending... (${sentApplications.length} sent)` : `Start Email Campaign (${jobCompanies.filter(c => c.email).length} ready)`}
              </button>
            </section>
{/* Companies Table */}
          {jobCompanies.length > 0 && (
            <section className="bg-card rounded-2xl shadow-sm border border-border overflow-hidden">
              <div className="px-6 py-5 border-b border-border bg-muted/50 flex justify-between items-center">
                <h2 className="text-lg font-bold text-foreground flex items-center gap-2">
                  3. Lead Database
                  {isJobScraping && (
                    <span className="flex items-center gap-1.5 text-xs font-bold text-indigo-600 bg-indigo-100 dark:bg-indigo-950/40 dark:text-indigo-400 px-2 py-0.5 rounded-full animate-pulse">
                      <span className="w-1.5 h-1.5 bg-indigo-500 rounded-full inline-block"></span>
                      LIVE
                    </span>
                  )}
                </h2>
                <span className="bg-indigo-100 text-indigo-800 text-xs font-bold px-3 py-1 rounded-full">
                  {jobCompanies.filter(c => c.email).length} with email / {jobCompanies.length} total
                </span>
              </div>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-border">
                  <thead className="bg-muted">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-bold text-muted-foreground uppercase">Company</th>
                      <th className="px-6 py-3 text-left text-xs font-bold text-muted-foreground uppercase">Email</th>
                      <th className="px-6 py-3 text-left text-xs font-bold text-muted-foreground uppercase">Website</th>
                      <th className="px-6 py-3 text-left text-xs font-bold text-muted-foreground uppercase">Status</th>
                      <th className="px-6 py-3 text-left text-xs font-bold text-muted-foreground uppercase">Action</th>
                    </tr>
                  </thead>
                  <tbody className="bg-card divide-y divide-border">
                    {jobCompanies.map((company, idx) => (
                      <tr key={idx} className={`transition-all duration-500 ${
                        company.email && newCompanyEmails.has(company.email)
                          ? 'bg-indigo-50 dark:bg-indigo-950/30 animate-pulse'
                          : 'hover:bg-muted/50'
                      }`}>
                        <td className="px-6 py-4">
                          <div className="font-medium text-foreground">{company.name}</div>
                          <div className="text-xs text-muted-foreground">{company.address}</div>
                        </td>
                        <td className="px-6 py-4">
                          {company.email
                            ? <span className="text-sm font-medium text-emerald-600 dark:text-emerald-400">{company.email}</span>
                            : <span className="text-xs text-muted-foreground italic">No email found</span>
                          }
                        </td>
                        <td className="px-6 py-4">
                          {company.website
                            ? <a href={company.website} target="_blank" className="text-xs text-blue-500 hover:underline">🌐 Visit</a>
                            : <span className="text-xs text-muted-foreground">-</span>
                          }
                        </td>
                        <td className="px-6 py-4">
                          {sentApplications.includes(company.email)
                            ? <span className="px-2 py-1 text-xs font-bold bg-emerald-100 text-emerald-700 rounded-full">✅ Sent</span>
                            : company.email
                              ? <span className="px-2 py-1 text-xs font-bold bg-indigo-100 text-indigo-700 rounded-full">Ready</span>
                              : <span className="px-2 py-1 text-xs bg-muted text-muted-foreground rounded-full">No Email</span>
                          }
                        </td>
                        <td className="px-6 py-4">
                          {company.email && !sentApplications.includes(company.email) && (
                            <button 
                              onClick={async () => {
                                if (!jobSenderEmail || !jobAppPassword) return alert("Please enter Sender Email and App Password below first.");
                                
                                setIsApplying(true);
                                setApplyMsg(`Sending to ${company.name}...`);
                                
                                await fetch('/api/jobs/apply', {
                                  method: 'POST',
                                  headers: { 'Content-Type': 'application/json' },
                                  body: JSON.stringify({
                                    gmail_address: jobSenderEmail,
                                    app_password: jobAppPassword,
                                    custom_pitch: jobCustomPitch,
                                    target_company: company.name,
                                    target_email: company.email
                                  })
                                });
                                
                                setSentApplications(prev => [...prev, company.email]);
                                setIsApplying(false);
                                setApplyMsg('Sent successfully!');
                              }}
                              disabled={isApplying}
                              className="text-emerald-600 hover:text-emerald-900 bg-emerald-50 px-3 py-1 rounded border border-emerald-200 text-xs font-semibold disabled:opacity-50"
                            >
                              📤 Send
                            </button>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          )}

                  </div>
      )}

    </div>
    </div>
  );
}
