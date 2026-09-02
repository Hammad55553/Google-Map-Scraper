import re

with open("frontend/api/scraper.py", "r") as f:
    content = f.read()

old_block = """                # Method 1: Scan Official Website
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
                        encoded_query = urllib.parse.quote(search_query)"""

new_block = """                # Check if website is a social media page
                is_social = False
                if has_website and website:
                    if any(domain in website.lower() for domain in ['facebook.com', 'instagram.com', 'twitter.com', 'linkedin.com', 'tiktok.com']):
                        is_social = True

                # Method 1: Scan Official Website (Skip for social media, directly use Google Search to bypass login walls)
                if has_website and website and not is_social:
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
                        # If it's a social link, add the platform name to search query to pull their public About page details
                        search_query = f'"{name}" email'
                        if is_social:
                            search_query = f'"{name}" email contact'
                            
                        encoded_query = urllib.parse.quote(search_query)"""

content = content.replace(old_block, new_block)

with open("frontend/api/scraper.py", "w") as f:
    f.write(content)
