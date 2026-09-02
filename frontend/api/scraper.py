import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import re

def format_whatsapp_number(phone):
    if not phone:
        return ""
    # Remove all non-numeric characters except +
    clean = re.sub(r'[^\d+]', '', phone)
    if clean.startswith('0'):
        # Usually requires country code, but we just provide it as is or expect user to handle it
        # Can default to replacing leading 0 with 92 for Pakistan for example, but it's risky
        pass
    return f"https://wa.me/{clean.replace('+', '')}"

async def scrape_google_maps(query, limit=20, progress_callback=None, on_lead_found=None, cancel_check=None):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print(f"Searching for: {query}")
        await page.goto(f'https://www.google.com/maps/search/{query.replace(" ", "+")}')
        
        try:
            # Wait for results to load
            await page.wait_for_selector('div[role="feed"]', timeout=10000)
            print("Feed loaded")
        except:
            print("Could not load feed, maybe no results or captcha")
            await browser.close()
            return []
            
        results = []
        feed = page.locator('div[role="feed"]')
        
        # Scroll to load more items
        items_count = 0
        scroll_attempts = 0
        while items_count < limit and scroll_attempts < 10:
            if cancel_check and cancel_check():
                print("Scraping cancelled during scrolling")
                break
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
                    # Update progress with items loaded so far
                    progress_callback(min(items_count, limit), limit)
            
            print(f"Loaded {items_count} items...")
            
        elements = await page.locator('div[role="article"]').all()
        elements = elements[:limit]
        
        for i, element in enumerate(elements):
            if cancel_check and cancel_check():
                print("Scraping cancelled during extraction")
                break
            try:
                # Update progress during extraction phase
                if progress_callback:
                    progress_callback(items_count + i + 1, items_count * 2)
                    
                name_element = element.locator('div.fontHeadlineSmall')
                name = await name_element.text_content() if await name_element.count() > 0 else "Unknown"
                
                # Rating (before clicking)
                rating_text = "0.0"
                rating_el = element.locator('span.MW4etd')
                if await rating_el.count() > 0:
                    rating_text = await rating_el.first.text_content()
                
                # Address (before clicking)
                address = ""
                address_texts = await element.locator('div.W4Efsd').all_inner_texts()
                for t in address_texts:
                    if '·' in t and '\n' not in t and 'Open' not in t:
                        parts = t.split('·')
                        address = parts[-1].strip().replace('\ue934', '').strip()
                        if address:
                            break
                
                # Click the item to see details (phone, website)
                await element.click()
                await page.wait_for_timeout(1500)
                
                # Get the current URL which is the Google Maps link for the business
                map_url = page.url
                    
                # Website
                website_element = page.locator('a[data-item-id="authority"]')
                website = ""
                has_website = False
                if await website_element.count() > 0:
                    website = await website_element.get_attribute('href')
                    has_website = True
                    
                # Phone
                phone_element = page.locator('button[data-item-id^="phone:tel:"]')
                phone = ""
                if await phone_element.count() > 0:
                    phone_raw = await phone_element.get_attribute('data-item-id')
                    phone = phone_raw.replace("phone:tel:", "") if phone_raw else ""
                    if not phone:
                        phone = await phone_element.text_content()
                
                wa_link = format_whatsapp_number(phone)
                
                # Email Extraction
                email = ""
                if has_website and website:
                    try:
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                        }
                        
                        async def fetch_emails(url):
                            try:
                                resp = await page.request.get(url, timeout=8000, headers=headers)
                                if resp.ok:
                                    html_c = await resp.text()
                                    found = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}', html_c)
                                    # Filter false positives like images, css, js
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
                                
                        # Return the first valid email found
                        if all_emails:
                            email = all_emails[0]
                            
                    except Exception as email_err:
                        print(f"Could not extract email for {name}: {email_err}")

                item = {
                    "Name": name,
                    "Rating": float(rating_text.replace(",", ".").strip()) if rating_text else 0.0,
                    "Phone": phone,
                    "Has Website": has_website,
                    "Website URL": website,
                    "Email": email,
                    "WhatsApp Link": wa_link,
                    "Map URL": map_url,
                    "Address": address
                }
                
                results.append(item)
                if on_lead_found:
                    on_lead_found(item)
                
            except Exception as e:
                print(f"Error extracting item: {e}")
                
        await browser.close()
        return results

def run_scraper(query, limit=20, progress_callback=None, on_lead_found=None, cancel_check=None):
    return asyncio.run(scrape_google_maps(query, limit, progress_callback, on_lead_found, cancel_check))
