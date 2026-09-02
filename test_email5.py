import asyncio
from playwright.async_api import async_playwright
import re

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Test on a known working site
        website = "https://www.example.com/" # Replace with a site you know has an email
        print(f"Testing {website}")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5"
        }
        
        async def fetch_emails(url):
            try:
                response = await page.request.get(url, timeout=8000, headers=headers)
                if response.ok:
                    html_content = await response.text()
                    emails_found = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}', html_content)
                    return [e for e in emails_found if not e.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.js', '.css', '.woff', '.ttf'))]
            except:
                pass
            return []

        emails = await fetch_emails(website)
        print(f"Home emails: {emails}")
        
        await browser.close()

asyncio.run(main())
