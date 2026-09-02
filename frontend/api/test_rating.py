import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://www.google.com/maps/search/Beauty+Salon+in+Riyadh,+Saudi+Arabia')
        await page.wait_for_selector('div[role="feed"]', timeout=10000)
        elements = await page.locator('div[role="article"]').all()
        html = await elements[0].inner_html()
        with open("first_element.html", "w") as f:
            f.write(html)
        await browser.close()

asyncio.run(run())
