with open("frontend/src/app/page.tsx", "r") as f:
    content = f.read()

# 1. Add states
old_states = """  const [progressMessage, setProgressMessage] = useState('');
  const [isScraping, setIsScraping] = useState(false);"""
new_states = """  const [progressMessage, setProgressMessage] = useState('');
  const [isScraping, setIsScraping] = useState(false);
  const [emailProgress, setEmailProgress] = useState(0);
  const [emailMessage, setEmailMessage] = useState('');
  const [isEmailing, setIsEmailing] = useState(false);
  const [sentEmailIds, setSentEmailIds] = useState<number[]>([]);"""
content = content.replace(old_states, new_states)

# 2. Add polling effect for email campaign
old_effect = """  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isScraping) {"""
new_effect = """  useEffect(() => {
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
    if (isScraping) {"""
content = content.replace(old_effect, new_effect)

# 3. Update Email Form button logic
old_btn = """                  try {
                    const res = await fetch('/api/emails/campaign', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ gmail_address: gmail, app_password: password })
                    });
                    const data = await res.json();
                    if (data.error) alert(data.error);
                    else {
                      alert("Email Campaign Started! Check backend logs for progress.");
                    }
                  } catch (e) {"""
new_btn = """                  try {
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
                  } catch (e) {"""
content = content.replace(old_btn, new_btn)

# 4. Update the Button text & disabled state
old_btn_element = """className="w-full h-[46px] bg-violet-600 text-white px-4 rounded-lg hover:bg-violet-700 hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0 transform transition-all duration-200 font-semibold shadow-sm flex justify-center items-center gap-2"
              >
                Start Email Campaign
              </button>"""
new_btn_element = """disabled={isEmailing}
                className="w-full h-[46px] bg-violet-600 text-white px-4 rounded-lg hover:bg-violet-700 hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0 transform transition-all duration-200 font-semibold shadow-sm flex justify-center items-center gap-2 disabled:opacity-70 disabled:hover:-translate-y-0 disabled:cursor-not-allowed"
              >
                {isEmailing ? (
                  <><span className="animate-spin">⏳</span> Sending...</>
                ) : (
                  <>Start Email Campaign</>
                )}
              </button>"""
content = content.replace(old_btn_element, new_btn_element)

# 5. Add Progress bar under Email Form
old_email_form_end = """              </button>
            </div>
          </div>
        </div></section>"""
new_email_form_end = """              </button>
            </div>
          </div>
          {isEmailing && (
            <div className="w-full mt-6">
              <div className="flex justify-between text-sm text-violet-700 mb-2 font-medium">
                <span>{emailMessage}</span>
                <span>{emailProgress}%</span>
              </div>
              <div className="w-full bg-violet-100 rounded-full h-2.5 overflow-hidden">
                <div className="bg-violet-600 h-2.5 rounded-full transition-all duration-500 ease-out" style={{ width: `${emailProgress}%` }}></div>
              </div>
            </div>
          )}
        </div></section>"""
content = content.replace(old_email_form_end, new_email_form_end)

# 6. Add "✅ Sent" badge in the table
old_table_btn = """<button 
                      className="text-blue-600 hover:text-blue-900 bg-blue-50 px-3 py-1 rounded border border-blue-200 text-xs font-semibold" 
                      onClick={() => {"""
new_table_btn = """{sentEmailIds.includes(lead.id) && (
                      <span className="text-emerald-700 bg-emerald-50 px-3 py-1 rounded border border-emerald-200 text-xs font-bold flex items-center">
                        ✅ Sent
                      </span>
                    )}
                    <button 
                      className="text-blue-600 hover:text-blue-900 bg-blue-50 px-3 py-1 rounded border border-blue-200 text-xs font-semibold" 
                      onClick={() => {"""
content = content.replace(old_table_btn, new_table_btn)

with open("frontend/src/app/page.tsx", "w") as f:
    f.write(content)
