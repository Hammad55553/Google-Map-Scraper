with open("frontend/api/scraper.py", "r") as f:
    content = f.read()

# Update signature
old_sig = "async def scrape_google_maps(query, limit=20, progress_callback=None, on_lead_found=None):"
new_sig = "async def scrape_google_maps(query, limit=20, progress_callback=None, on_lead_found=None, cancel_check=None):"
content = content.replace(old_sig, new_sig)

old_run = "def run_scraper(query, limit=20, progress_callback=None, on_lead_found=None):"
new_run = "def run_scraper(query, limit=20, progress_callback=None, on_lead_found=None, cancel_check=None):"
content = content.replace(old_run, new_run)

old_run_async = "return asyncio.run(scrape_google_maps(query, limit, progress_callback, on_lead_found))"
new_run_async = "return asyncio.run(scrape_google_maps(query, limit, progress_callback, on_lead_found, cancel_check))"
content = content.replace(old_run_async, new_run_async)

# Add cancel check in scroll loop
old_scroll_loop = """        while items_count < limit and scroll_attempts < 10:
            await feed.hover()"""
new_scroll_loop = """        while items_count < limit and scroll_attempts < 10:
            if cancel_check and cancel_check():
                print("Scraping cancelled during scrolling")
                break
            await feed.hover()"""
content = content.replace(old_scroll_loop, new_scroll_loop)

# Add cancel check in extraction loop
old_ext_loop = """        for i, element in enumerate(elements):
            try:"""
new_ext_loop = """        for i, element in enumerate(elements):
            if cancel_check and cancel_check():
                print("Scraping cancelled during extraction")
                break
            try:"""
content = content.replace(old_ext_loop, new_ext_loop)

with open("frontend/api/scraper.py", "w") as f:
    f.write(content)

# Update index.py to pass cancel_check
with open("frontend/api/index.py", "r") as f:
    index_content = f.read()

old_call = """        run_scraper(
            query=query, 
            limit=50, 
            progress_callback=update_progress,
            on_lead_found=handle_lead
        )"""
new_call = """        run_scraper(
            query=query, 
            limit=50, 
            progress_callback=update_progress,
            on_lead_found=handle_lead,
            cancel_check=lambda: scrape_status.get("cancel", False)
        )"""
index_content = index_content.replace(old_call, new_call)

with open("frontend/api/index.py", "w") as f:
    f.write(index_content)
