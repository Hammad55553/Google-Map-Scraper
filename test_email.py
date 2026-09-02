import asyncio
from playwright.async_api import async_playwright
import re

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        website = "https://www.forestfamilydentistry.com/"
        print(f"Testing {website}")
        try:
            response = await page.request.get(website, timeout=10000)
            print(f"Status: {response.status}")
            if response.ok:
                html_content = await response.text()
                emails_found = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', html_content)
                valid_emails = [e for e in emails_found if not e.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'))]
                print(f"Emails found: {valid_emails}")
            else:
                print("Response not OK")
        except Exception as e:
            print(f"Error: {e}")
        
        await browser.close()

asyncio.run(main())
