import asyncio
from playwright.async_api import async_playwright
import re

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Create context with realistic User-Agent
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        website = "https://www.forestfamilydentistry.com/"
        print(f"Testing {website} using page.goto")
        try:
            # We don't need to load images/css to get text
            await page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["image", "media", "font"] else route.continue_())
            
            response = await page.goto(website, timeout=15000, wait_until="domcontentloaded")
            print(f"Status: {response.status if response else 'Unknown'}")
            
            html_content = await page.content()
            emails_found = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', html_content)
            valid_emails = [e for e in emails_found if not e.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.js', '.css'))]
            print(f"Emails found: {list(set(valid_emails))}")
        except Exception as e:
            print(f"Error: {e}")
        
        await browser.close()

asyncio.run(main())
