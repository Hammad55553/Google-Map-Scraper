import re
import urllib.parse

with open("frontend/api/scraper.py", "r") as f:
    content = f.read()

old_email_extraction = """                # Email Extraction
                email = ""
                if has_website and website:
                    try:
                        async def fetch_emails_real(url):
                            try:
                                # We use a real browser page navigation which completely bypasses 403 blocks from Cloudflare
                                await email_page.goto(url, timeout=8000, wait_until="domcontentloaded")
                                html_c = await email_page.content()
                                found = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}', html_c)
                                return [e for e in found if not e.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.js', '.css', '.woff', '.ttf', '.mp4', '.pdf')) and not e.startswith('sentry-')]
                            except:
                                return []

                        # Try homepage first
                        all_emails = await fetch_emails_real(website)
                        
                        # If no email on homepage, try contact page
                        if not all_emails:
                            contact_url = website.rstrip('/') + '/contact'
                            all_emails = await fetch_emails_real(contact_url)
                            
                        if not all_emails:
                            contact_us_url = website.rstrip('/') + '/contact-us'
                            all_emails = await fetch_emails_real(contact_us_url)
                                
                        if all_emails:
                            email = all_emails[0]
                            
                    except Exception as email_err:
                        print(f"Could not extract email for {name}: {email_err}")"""

new_email_extraction = """                # Email Extraction
                email = ""
                
                async def fetch_emails_real(url):
                    try:
                        await email_page.goto(url, timeout=8000, wait_until="domcontentloaded")
                        html_c = await email_page.content()
                        found = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}', html_c)
                        valid_emails = [e for e in found if not e.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.js', '.css', '.woff', '.ttf', '.mp4', '.pdf')) and not e.startswith('sentry-')]
                        # Filter out common google/microsoft random strings
                        valid_emails = [e for e in valid_emails if 'sentry' not in e.lower() and 'example' not in e.lower() and 'wixpress' not in e.lower()]
                        return valid_emails
                    except:
                        return []

                # Method 1: Scan Official Website
                if has_website and website:
                    try:
                        all_emails = await fetch_emails_real(website)
                        if not all_emails:
                            all_emails = await fetch_emails_real(website.rstrip('/') + '/contact')
                        if not all_emails:
                            all_emails = await fetch_emails_real(website.rstrip('/') + '/contact-us')
                        if all_emails:
                            email = all_emails[0]
                    except Exception as email_err:
                        pass
                
                # Method 2: AI / Google Search Fallback
                if not email:
                    import urllib.parse
                    try:
                        search_query = f'"{name}" email'
                        encoded_query = urllib.parse.quote(search_query)
                        # We use udm=50 as suggested, or standard search
                        google_search_url = f'https://www.google.com/search?q={encoded_query}&udm=50'
                        
                        all_emails = await fetch_emails_real(google_search_url)
                        if all_emails:
                            email = all_emails[0]
                    except Exception as e:
                        pass"""

content = content.replace(old_email_extraction, new_email_extraction)

with open("frontend/api/scraper.py", "w") as f:
    f.write(content)
