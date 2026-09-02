import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://www.google.com/maps/search/Beauty+Salon+in+Riyadh,+Saudi+Arabia')
        await page.wait_for_selector('div[role="feed"]', timeout=10000)
        
        elements = await page.locator('div[role="article"]').all()
        for i, el in enumerate(elements[:5]):
            address = ""
            address_texts = await el.locator('div.W4Efsd').all_inner_texts()
            for t in address_texts:
                if '·' in t and '\n' not in t and 'Open' not in t:
                    parts = t.split('·')
                    address = parts[-1].strip()
                    address = address.replace('\ue934', '').strip()
                    if address:
                        break
            print(f"Item {i}: {address}")
            
        await browser.close()

asyncio.run(run())
