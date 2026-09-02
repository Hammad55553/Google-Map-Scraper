import asyncio
from playwright.async_api import async_playwright
import re

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://www.google.com/maps/search/Plumber+in+New+York')
        await page.wait_for_selector('div[role="feed"]', timeout=10000)
        await page.wait_for_timeout(2000)
        
        elements = await page.locator('div[role="article"]').all()
        for i, el in enumerate(elements[:5]):
            html = await el.inner_html()
            # Try to find "years in business"
            match = re.search(r'(\d+\+?\s+years in business)', html)
            if match:
                print(f"Item {i}: Found -> {match.group(1)}")
            else:
                print(f"Item {i}: Not found")
                
        await browser.close()

asyncio.run(run())
