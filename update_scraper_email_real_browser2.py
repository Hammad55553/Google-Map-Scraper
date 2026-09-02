import re

with open("frontend/api/scraper.py", "r") as f:
    content = f.read()

# I need to add email_page initialization
setup_old = """    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = await context.new_page()"""

setup_new = """    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-blink-features=AutomationControlled']
        )
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        )
        
        page = await context.new_page()
        
        # Dedicated fast page for email extraction (bypasses Cloudflare better than request.get)
        email_page = await context.new_page()
        # Block heavy resources on email page for speed
        await email_page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["image", "media", "font", "stylesheet"] else route.continue_())"""

content = content.replace(setup_old, setup_new)

old_email_extraction = """                # Email Extraction
                email = ""
                if has_website and website:
                    try:
                        # Use background request with aggressive User-Agent
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                            "Accept-Language": "en-US,en;q=0.9",
                            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                            "Sec-Ch-Ua-Mobile": "?0",
                            "Sec-Ch-Ua-Platform": '"macOS"',
                            "Sec-Fetch-Dest": "document",
                            "Sec-Fetch-Mode": "navigate",
                            "Sec-Fetch-Site": "none",
                            "Sec-Fetch-User": "?1",
                            "Upgrade-Insecure-Requests": "1"
                        }
                        
                        async def fetch_emails(url):
                            try:
                                resp = await page.request.get(url, timeout=10000, headers=headers)
                                if resp.ok:
                                    html_c = await resp.text()
                                    found = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}', html_c)
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
                                
                        if all_emails:
                            email = all_emails[0]
                            
                    except Exception as email_err:
                        print(f"Could not extract email for {name}: {email_err}")"""

new_email_extraction = """                # Email Extraction
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

content = content.replace(old_email_extraction, new_email_extraction)

with open("frontend/api/scraper.py", "w") as f:
    f.write(content)
