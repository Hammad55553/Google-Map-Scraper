import re

with open("frontend/api/scraper.py", "r") as f:
    content = f.read()

old_email_extraction = """                # Email Extraction
                email = ""
                if has_website and website:
                    try:
                        # Quick fetch of the homepage
                        response = await page.request.get(website, timeout=5000)
                        if response.ok:
                            html_content = await response.text()
                            # Basic regex for email, ignoring some common image extensions
                            emails_found = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', html_content)
                            valid_emails = [e for e in emails_found if not e.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'))]
                            if valid_emails:
                                email = valid_emails[0]
                    except Exception as email_err:
                        print(f"Could not extract email for {name}: {email_err}")"""

new_email_extraction = """                # Email Extraction
                email = ""
                if has_website and website:
                    try:
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                        }
                        
                        async def fetch_emails(url):
                            try:
                                resp = await page.request.get(url, timeout=8000, headers=headers)
                                if resp.ok:
                                    html_c = await resp.text()
                                    found = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}', html_c)
                                    # Filter false positives like images, css, js
                                    return [e for e in found if not e.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.js', '.css', '.woff', '.ttf', '.mp4')) and not e.startswith('sentry-')]
                            except:
                                pass
                            return []

                        # Check homepage and contact page concurrently
                        contact_url = website.rstrip('/') + '/contact'
                        contact_us_url = website.rstrip('/') + '/contact-us'
                        
                        results_emails = await asyncio.gather(
                            fetch_emails(website),
                            fetch_emails(contact_url),
                            fetch_emails(contact_us_url),
                            return_exceptions=True
                        )
                        
                        all_emails = []
                        for res in results_emails:
                            if isinstance(res, list):
                                all_emails.extend(res)
                                
                        # Return the first valid email found
                        if all_emails:
                            email = all_emails[0]
                            
                    except Exception as email_err:
                        print(f"Could not extract email for {name}: {email_err}")"""

content = content.replace(old_email_extraction, new_email_extraction)

with open("frontend/api/scraper.py", "w") as f:
    f.write(content)
