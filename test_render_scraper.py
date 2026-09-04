import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print("Navigating...")
        await page.goto('https://asperinfotech.vercel.app/contact', timeout=30000, wait_until='networkidle')
        await page.wait_for_timeout(5000)
        html = await page.content()
        if "asperinfotech@gmail.com" in html:
            print("Email found in HTML!")
        else:
            print("Email NOT found in HTML! Saving HTML to inspect.")
            with open("debug_render.html", "w") as f:
                f.write(html)
        await browser.close()

asyncio.run(run())
