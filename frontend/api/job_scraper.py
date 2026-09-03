import asyncio
from playwright.async_api import async_playwright
import re
import urllib.parse

def clean_emails(raw_emails):
    blacklist = ['sentry', 'example', 'wixpress', 'schema', 'w3.org', 'cloudflare', 'amazonaws',
                 'google', 'apple', 'microsoft', 'placeholder', 'noreply', 'no-reply', 'support@sentry']
    skip_exts = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.js', '.css', '.woff', '.ttf', '.mp4', '.pdf')
    result = []
    seen = set()
    for e in raw_emails:
        el = e.lower()
        if el.endswith(skip_exts): continue
        if any(b in el for b in blacklist): continue
        if el in seen: continue
        seen.add(el)
        result.append(e)
    return result

async def scrape_tech_companies(query, limit=30, progress_callback=None, on_company_found=None, cancel_check=None):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-blink-features=AutomationControlled']
        )
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        )

        page = await context.new_page()
        email_page = await context.new_page()

        maps_query = f'{query} software company'
        print(f"Searching: {maps_query}")
        await page.goto(f'https://www.google.com/maps/search/{maps_query.replace(" ", "+")}')

        try:
            await page.wait_for_selector('div[role="feed"]', timeout=10000)
        except:
            await browser.close()
            return []

        feed = page.locator('div[role="feed"]')
        items_count = 0
        scroll_attempts = 0
        while items_count < limit and scroll_attempts < 10:
            if cancel_check and cancel_check(): break
            await feed.hover()
            await page.mouse.wheel(0, 10000)
            await page.wait_for_timeout(2000)
            elements = await page.locator('div[role="article"]').all()
            if len(elements) == items_count:
                scroll_attempts += 1
            else:
                scroll_attempts = 0
                items_count = len(elements)
                if progress_callback:
                    progress_callback(items_count, limit, f"Loading: {items_count} companies found...")

        elements = await page.locator('div[role="article"]').all()
        total = len(elements)

        async def get_email(website):
            if not website: return ""
            
            is_social = any(
                d in website.lower() for d in ['facebook.com', 'instagram.com', 'twitter.com', 'linkedin.com', 'tiktok.com']
            )
            if is_social: return ""

            for url in [website, website.rstrip('/') + '/contact', website.rstrip('/') + '/about']:
                try:
                    await email_page.goto(url, timeout=7000, wait_until="domcontentloaded")
                    html = await email_page.content()
                    mailto = re.findall(r'mailto:([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,})', html)
                    cleaned = clean_emails(mailto)
                    if cleaned: return cleaned[0]
                    found = clean_emails(re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}', html))
                    if found: return found[0]
                except: pass
            
            # Domain pattern fallback
            try:
                from urllib.parse import urlparse
                domain = urlparse(website).netloc.replace('www.', '')
                if domain: return f"info@{domain}"
            except: pass
            return ""

        results = []
        for i, el in enumerate(elements[:limit]):
            if cancel_check and cancel_check(): break
            try:
                await el.click()
                await page.wait_for_timeout(1200)

                name_el = page.locator('h1.DUwDvf')
                name = await name_el.text_content() if await name_el.count() > 0 else "Unknown"

                address_el = page.locator('button[data-item-id="address"]')
                address = await address_el.text_content() if await address_el.count() > 0 else ""
                address = address.replace("", "").strip() # Remove google map icon character

                website_element = page.locator('a[data-item-id="authority"]')
                website = ""
                if await website_element.count() > 0:
                    website = await website_element.get_attribute('href') or ""

                phone_element = page.locator('button[data-item-id^="phone:tel:"]')
                phone = ""
                if await phone_element.count() > 0:
                    phone_raw = await phone_element.get_attribute('data-item-id')
                    phone = (phone_raw or "").replace("phone:tel:", "")

                email = await get_email(website)

                item = {
                    "name": name,
                    "address": address,
                    "website": website,
                    "phone": phone,
                    "email": email,
                    "map_url": page.url
                }
                results.append(item)
                if on_company_found: on_company_found(item)
                if progress_callback:
                    progress_callback(i + 1, total, f"Processing {i+1}/{total}: {name}")
            except Exception as ex:
                print(f"Error: {ex}")

        await browser.close()
        return results

def run_job_scraper(query, limit=30, progress_callback=None, on_company_found=None, cancel_check=None):
    return asyncio.run(scrape_tech_companies(query, limit, progress_callback, on_company_found, cancel_check))
