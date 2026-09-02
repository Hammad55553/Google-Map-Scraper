import re

with open("frontend/src/app/page.tsx", "r") as f:
    content = f.read()

# 1. Add state to form state
content = content.replace("country: '', city: '', category: '', radius: '20'", "country: '', state: '', city: '', category: '', radius: '20'")

# 2. Add states state
content = content.replace("const [cities, setCities] = useState<string[]>([]);", "const [states, setStates] = useState<any[]>([]);\n  const [cities, setCities] = useState<string[]>([]);")

# 3. Update useEffects
old_use_effect = """  // Fetch cities when country changes
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
  }, [form.country]);"""

new_use_effects = """  // Fetch states when country changes
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
  }, [form.state]);"""

content = content.replace(old_use_effect, new_use_effects)

# 4. Add State input to UI
old_ui = """            <div>
              <label className="block text-sm text-gray-600 mb-1">City</label>"""

new_ui = """            <div>
              <label className="block text-sm text-gray-600 mb-1">State/Province</label>
              <input 
                type="text" 
                list="states-list"
                className="w-full border p-2 rounded text-black" 
                value={form.state} 
                onChange={e => setForm({...form, state: e.target.value})} 
                placeholder="Select a state..."
              />
              <datalist id="states-list">
                {states.map(s => <option key={s} value={s} />)}
              </datalist>
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">City</label>"""

content = content.replace(old_ui, new_ui)

# 5. Fix grid columns
content = content.replace('className="grid grid-cols-5 gap-4 items-end"', 'className="grid grid-cols-6 gap-4 items-end"')

with open("frontend/src/app/page.tsx", "w") as f:
    f.write(content)
