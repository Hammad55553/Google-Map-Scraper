import re
import os
import json
import urllib.request
import socket
from playwright.async_api import async_playwright
import urllib.parse
from bs4 import BeautifulSoup

def is_valid_email_domain(email):
    try:
        domain = email.split('@')[-1]
        socket.gethostbyname(domain)
        return True
    except Exception:
        return False

def extract_emails(text):
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_regex, text)
    valid_emails = [e for e in emails if not e.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.wixpress.com', 'sentry.io'))]
    valid_emails = list(set(valid_emails))
    # Domain validation
    return [e for e in valid_emails if is_valid_email_domain(e)]

def format_whatsapp_number(phone):
    if not phone: return ""
    clean = re.sub(r'[^\d+]', '', phone)
    if not clean.startswith('+'):
        if clean.startswith('0'):
            clean = '92' + clean[1:]
        elif len(clean) == 10:
            clean = '1' + clean
    return f"https://wa.me/{clean.replace('+', '')}"

def suggest_pitch_type(text):
    text_lower = text.lower()
    tech_keywords = ['software', 'development', 'it ', 'technology', 'agency', 'tech', 'app', 'web design', 'react', 'developer', 'startup', 'digital']
    tech_score = sum(1 for word in tech_keywords if word in text_lower)
    
    if tech_score >= 2:
        return 'job'
    return 'b2b'

def clean_company_name(title):
    import re
    title = re.sub(r'#\w+', '', title)
    suffixes = ['| LinkedIn', '- LinkedIn', '| Facebook', '- Facebook', ' - Home', '…']
    for s in suffixes:
        title = title.replace(s, '')
        
    # Split by | or -
    parts = [p.strip() for p in re.split(r'\||-', title) if p.strip()]
    
    if len(parts) > 1:
        last_part = parts[-1]
        first_part = parts[0]
        
        # Usually for job listings: "Job Title | Company" -> Company is the shorter last part
        if len(last_part) < len(first_part) and len(last_part) <= 30:
            return last_part
        elif len(first_part) <= 30:
            return first_part
        else:
            return last_part
            
    return parts[0] if parts else "Company"

def extract_job_title_from_text(text: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "Software Developer"
        
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        short_text = text[:3000]
        
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Extract the specific Job Title being hired for from this text. Return ONLY the job title (e.g. 'Senior React Developer', 'Node.js Backend Engineer'). If you cannot determine it, return 'Software Developer'. Do not include any other conversational text."},
                {"role": "user", "content": short_text}
            ],
            "max_tokens": 30,
            "temperature": 0.3
        }
        
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            title = result['choices'][0]['message']['content'].strip()
            title = title.replace('"', '').replace("'", "")
            return title if title else "Software Developer"
    except Exception as e:
        print(f"Error extracting job title: {e}")
        return "Software Developer"

async def extract_from_link(url):
    email = ""
    phone = ""
    pitch_type = "b2b"
    title = "Company"
    target_role = "Software Developer"
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Navigate with a timeout
            debug_err = ""
            try:
                await page.goto(url, timeout=25000, wait_until='domcontentloaded')
                await page.wait_for_timeout(5000)
            except Exception as e:
                debug_err = str(e)
            
            html = await page.content()
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text(separator=' ', strip=True)
            
            if soup.title and soup.title.string:
                title = clean_company_name(soup.title.string)
            
            # Extract Emails
            emails = extract_emails(text)
            if not emails:
                # Try finding mailto links
                mailto_links = await page.evaluate('''() => {
                    return Array.from(document.querySelectorAll('a[href^="mailto:"]')).map(a => a.href);
                }''')
                if mailto_links:
                    for link in mailto_links:
                        e = link.replace('mailto:', '').split('?')[0].strip()
                        if e:
                            emails.append(e)
            
            if emails:
                # Prioritize emails containing recruitment keywords
                keywords = ['hr', 'career', 'job', 'recruit', 'talent', 'hire', 'people']
                best_email = None
                for e in emails:
                    if any(k in e.lower() for k in keywords):
                        best_email = e
                        break
                email = best_email if best_email else emails[0]
                
            # Extract Phone (simple regex for common formats)
            phone_regex = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
            phones = re.findall(phone_regex, text)
            if not phones:
                 # Try finding tel links
                tel_links = await page.evaluate('''() => {
                    return Array.from(document.querySelectorAll('a[href^="tel:"]')).map(a => a.href);
                }''')
                if tel_links:
                    for link in tel_links:
                        p = link.replace('tel:', '').strip()
                        if p:
                            phones.append(p)
                            
            if phones:
                phone = phones[0]
            
            pitch_type = suggest_pitch_type(text)
            if pitch_type == 'job':
                target_role = extract_job_title_from_text(text)
            
            await browser.close()
    except Exception as e:
        print(f"Error extracting from {url}: {e}")
        
    wa_link = format_whatsapp_number(phone) if phone else ""
    
    return {
        "email": email,
        "phone": phone,
        "whatsapp_link": wa_link,
        "suggested_pitch_type": pitch_type,
        "company_name": title,
        "target_role": target_role
    }
